#!/usr/bin/env python3
"""Strategy Reviewer Agent — extends BaseAgent, audits trading strategy parameters, filters, and performance."""

import os, sys, subprocess, json, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from agents.base.base_agent import BaseAgent

class StrategyReviewerAgent(BaseAgent):
    def __init__(self):
        super().__init__('strategy-reviewer')

    async def run(self, input_data=None):
        """
        Run strategy audit. input_data specifies parameters:
          {"mode": "discover"} — discover environment and run full audit
        """
        if input_data is None:
            input_data = {}

        mode = input_data.get('mode', 'discover')
        self._env = await self._discover_environment()

        if self._env['servers'].get('100.74.53.2') != 'alive':
            return {'error': 'Production server 100.74.53.2 is not reachable.'}

        results = {'environment': self._env}
        results['audits'] = {
            'filter_throughput': await self._audit_filter_throughput(),
            'weights_alignment': await self._audit_weights_alignment(),
            'kelly_safety': await self._audit_kelly_safety()
        }
        return results

    async def _discover_environment(self):
        """Dynamic discovery: find live server and database path."""
        env = {'servers': {}}
        host = '100.74.53.2'
        result = subprocess.run(
            ['ssh', '-o', 'ConnectTimeout=3', f'arturo@{host}', 'echo ok'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and 'ok' in result.stdout:
            env['servers'][host] = 'alive'
        else:
            env['servers'][host] = 'dead'
        return env

    async def _audit_filter_throughput(self):
        """Audit what percentage of signals are filtered by each gate in the C++ bot log."""
        host = '100.74.53.2'
        log_path = '/home/arturo/monteCarlo/data/logs/bot_production.log'
        cmd = f"tail -n 1000 {log_path}"
        
        result = subprocess.run(
            ['ssh', f'arturo@{host}', cmd],
            capture_output=True, text=True, timeout=15
        )
        
        if result.returncode != 0:
            return {'error': 'Failed to read production log.'}

        lines = result.stdout.split('\n')
        total_signals = sum(1 for l in lines if 'Analizando' in l)
        
        blocked_learner = sum(1 for l in lines if 'BLOQUEADO por StatisticalLearner' in l)
        blocked_convexity = sum(1 for l in lines if 'CONVEXITY FILTER' in l)
        blocked_correlation = sum(1 for l in lines if 'Hard correlation filter' in l)
        blocked_spread = sum(1 for l in lines if 'SPREAD ALTO' in l)
        no_qualify = sum(1 for l in lines if 'HOLD / No califica' in l)

        throughput = {
            'total_signals_scanned': total_signals,
            'blocked_by_statistical_learner': {
                'count': blocked_learner,
                'pct': round(blocked_learner / max(1, total_signals) * 100.0, 1)
            },
            'blocked_by_convexity_filter': {
                'count': blocked_convexity,
                'pct': round(blocked_convexity / max(1, total_signals) * 100.0, 1)
            },
            'blocked_by_correlation_filter': {
                'count': blocked_correlation,
                'pct': round(blocked_correlation / max(1, total_signals) * 100.0, 1)
            },
            'blocked_by_high_spread': {
                'count': blocked_spread,
                'pct': round(blocked_spread / max(1, total_signals) * 100.0, 1)
            },
            'held_no_qualify_technical': {
                'count': no_qualify,
                'pct': round(no_qualify / max(1, total_signals) * 100.0, 1)
            }
        }
        
        # Determine if any filter is "absurdly" restrictive (e.g. blocking > 80% on its own)
        warnings = []
        if throughput['blocked_by_convexity_filter']['pct'] > 50.0:
            warnings.append("WARNING: Convexity filter is highly restrictive. Verify adaptive targets.")
        if throughput['blocked_by_statistical_learner']['pct'] > 30.0:
            warnings.append("WARNING: Statistical learner is blocking a high percentage of trades. Verify regime stability.")
            
        throughput['warnings'] = warnings
        return throughput

    async def _audit_weights_alignment(self):
        """Audit the alignment of regime weights against realized DB returns."""
        host = '100.74.53.2'
        db_path = '/home/arturo/monteCarlo/cpp_bot/data/trading_data.db'
        weights_path = '/home/arturo/monteCarlo/cpp_bot/config/adaptive_weights.json'
        
        # Read weights
        w_cmd = f"cat {weights_path}"
        w_result = subprocess.run(
            ['ssh', f'arturo@{host}', w_cmd],
            capture_output=True, text=True, timeout=10
        )
        
        # Read performance by regime from database
        db_cmd = f"sqlite3 {db_path} \"SELECT s.regime, COUNT(*), ROUND(SUM(o.pnl_usd), 2), ROUND(SUM(CASE WHEN o.pnl_usd > 0 THEN 1 ELSE 0 END)*100.0/COUNT(*), 1) FROM trade_outcomes o JOIN trades t ON o.trade_id = t.id JOIN signals s ON t.signal_id = s.id GROUP BY s.regime;\""
        db_result = subprocess.run(
            ['ssh', f'arturo@{host}', db_cmd],
            capture_output=True, text=True, timeout=15
        )

        if w_result.returncode != 0 or db_result.returncode != 0:
            return {'error': 'Failed to read weights JSON or Database stats.'}

        try:
            weights = json.loads(w_result.stdout).get('regime_weights', {})
        except:
            return {'error': 'Failed to parse weights JSON.'}

        db_stats = {}
        for line in db_result.stdout.strip().split('\n'):
            if not line: continue
            parts = line.split('|')
            if len(parts) == 4:
                db_stats[parts[0]] = {
                    'trades': int(parts[1]),
                    'pnl_usd': float(parts[2]),
                    'win_rate': float(parts[3])
                }

        alignment = []
        for regime, w_data in weights.items():
            stats = db_stats.get(regime, {'trades': 0, 'pnl_usd': 0.0, 'win_rate': 0.0})
            
            # Simple heuristic: if PnL is deeply negative but regime weights focus on trend over reversion, warn.
            alert = "OK"
            if stats['pnl_usd'] < -100.0:
                if w_data.get('trend', 0.0) > 0.40:
                    alert = "WARNING: Deep losses in this regime, but trend weights are extremely aggressive (>40%). Consider shifting weights to mean-reversion."
            
            alignment.append({
                'regime': regime,
                'configured_weights': w_data,
                'realized_performance': stats,
                'status': alert
            })
            
        return alignment

    async def _audit_kelly_safety(self):
        """Scans the local risk_manager.cpp file to verify that the win rate robustness checks are active."""
        local_path = '/Users/arturo/development/lumina/monteCarlo/cpp_bot/src/risk_manager.cpp'
        if not os.path.exists(local_path):
            return {'error': 'Local risk_manager.cpp not found.'}
            
        with open(local_path, 'r') as f:
            content = f.read()
            
        has_normalizer = 'wr /= 100.0' in content
        has_small_acct = 'min_size_pct = 5.5 / balance' in content
        
        return {
            'kelly_winrate_normalization_active': has_normalizer,
            'adaptive_small_account_protection_active': has_small_acct,
            'status': "EXCELLENT" if (has_normalizer and has_small_acct) else "WARNING: Missing safety features in risk manager."
        }

if __name__ == '__main__':
    import asyncio
    reviewer = StrategyReviewerAgent()
    print(json.dumps(asyncio.run(reviewer.run({'mode': 'discover'})), indent=2))
