#!/usr/bin/env python3
"""Quant-Auditor-4D: Merged strategy auditor — original filter audit + 4-pillar quantitative compliance."""

import os, sys, subprocess, json, re, math
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from agents.base.base_agent import BaseAgent

HOST = '100.74.53.2'
BOT_DIR = '/home/arturo/monteCarlo'
CPP_DIR = f'{BOT_DIR}/cpp_bot'
DB_PATH = f'{BOT_DIR}/data/trading_data.db'
LOG_PATH = f'{BOT_DIR}/data/logs/bot_production.log'
WEIGHTS_PATH = f'{CPP_DIR}/config/adaptive_weights.json'
GA_PATH = f'{CPP_DIR}/experimental/ga_params_compatible.json'
LOCAL_CPP = '/Users/arturo/development/lumina/monteCarlo/cpp_bot'

def _ssh(cmd, timeout=15):
    r = subprocess.run(['ssh', '-o', 'ConnectTimeout=5', f'arturo@{HOST}', cmd], capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0: return None
    return r.stdout.strip()

def _sql(query):
    return _ssh(f'sqlite3 {DB_PATH} "{query}"')

class QuantAuditor4D(BaseAgent):
    def __init__(self):
        super().__init__('quant-auditor-4d')

    async def run(self, input_data=None):
        env = await self._discover()
        if env.get('server') != 'alive':
            return {'error': f'Server {HOST} not reachable'}

        results = {'environment': env, 'timestamp': datetime.now().isoformat()}

        results['audits'] = {
            'pillar_1_antifragility': await self._audit_antifragility(),
            'pillar_2_microstructure': await self._audit_microstructure(),
            'pillar_3_financial_ai': await self._audit_financial_ai(),
            'pillar_4_moneyball': await self._audit_moneyball(),
            'filter_throughput': await self._audit_filter_throughput(),
            'regime_weights_alignment': await self._audit_weights_alignment(),
            'risk_safety': await self._audit_risk_safety(),
        }
        results['scorecard'] = self._scorecard(results['audits'])
        return results

    async def _discover(self):
        r = subprocess.run(['ssh', '-o', 'ConnectTimeout=5', f'arturo@{HOST}', 'echo ok'], capture_output=True, text=True, timeout=10)
        alive = (r.returncode == 0 and 'ok' in r.stdout)
        if not alive:
            return {'server': 'dead'}
        return {
            'server': 'alive',
            'host': HOST,
            'db_size_mb': _sql("SELECT ROUND(page_count * page_size / 1024.0 / 1024.0, 1) FROM pragma_page_count, pragma_page_size") or '?',
            'total_trades': _sql("SELECT COUNT(*) FROM trades") or '?',
            'total_signals': _sql("SELECT COUNT(*) FROM signals") or '?',
            'total_outcomes': _sql("SELECT COUNT(*) FROM trade_outcomes") or '?'
        }

    # ─── PILLAR 1: ANTIFRAGILITY (Taleb) ────────────────────────────────
    async def _audit_antifragility(self):
        findings = []

        # 1a. Concave vs convex payoff: check recent PnL distribution
        recent_pnl = _sql("SELECT pnl_usd FROM trade_outcomes ORDER BY exit_timestamp DESC LIMIT 30")
        if recent_pnl:
            vals = [float(x) for x in recent_pnl.split('\n') if x]
            wins = [v for v in vals if v > 0]
            losses = [v for v in vals if v < 0]
            avg_win = sum(wins)/len(wins) if wins else 0
            avg_loss = abs(sum(losses)/len(losses)) if losses else 0
            ratio = round(avg_win / avg_loss, 2) if avg_loss > 0 else 0
            # Taleb: need avg_win / avg_loss > 1.5 for convexity
            if ratio < 1.5:
                findings.append({
                    'test': 'Payoff convexity (Taleb)',
                    'status': 'FAIL',
                    'detail': f'Avg win/avg loss ratio = {ratio}x (need ≥1.5x for convex payoff). Current payoff structure is concave — small wins don\'t cover tail losses.',
                    'value': ratio,
                    'threshold': '≥ 1.5'
                })
            else:
                findings.append({
                    'test': 'Payoff convexity (Taleb)',
                    'status': 'PASS',
                    'detail': f'Avg win/avg loss = {ratio}x — convex',
                    'value': ratio
                })

        # 1b. Check if SL is static or liquidity-aware
        sl_code = subprocess.run(['grep', '-n', 'stop_loss', f'{LOCAL_CPP}/src/risk_manager.cpp'], capture_output=True, text=True, timeout=5)
        has_liquidity_sl = 'liquidity' in sl_code.stdout.lower() or 'spread' in sl_code.stdout.lower() or 'order_book' in sl_code.stdout.lower()
        findings.append({
            'test': 'Liquidity-aware stop-loss',
            'status': 'WARN' if not has_liquidity_sl else 'PASS',
            'detail': 'SL uses ATR-based dynamic calculation but no explicit liquidity/order-book depth integration.' if not has_liquidity_sl else 'SL incorporates liquidity data.',
        })

        # 1c. Catastrophic failure handling
        has_sigterm = subprocess.run(['grep', '-n', 'SIGTERM\\|SIGINT\\|signal', f'{LOCAL_CPP}/src/main.cpp'], capture_output=True, text=True, timeout=5)
        has_graceful = 'catch' in has_sigterm.stdout.lower() or 'signal' in has_sigterm.stdout.lower()
        findings.append({
            'test': 'Graceful shutdown / signal handling',
            'status': 'WARN' if not has_graceful else 'PASS',
            'detail': 'No SIGTERM/SIGINT handler found — kill -9 only. Positions may not be saved on crash.' if not has_graceful else 'Signal handlers present.',
        })

        # 1d. Connection drop resilience
        has_retry = subprocess.run(['grep', '-n', 'retry\\|reconnect\\|backoff', f'{LOCAL_CPP}/src/bybit_api.cpp'], capture_output=True, text=True, timeout=5)
        findings.append({
            'test': 'API retry & reconnection',
            'status': 'PASS' if has_retry.stdout else 'WARN',
            'detail': 'Retry logic found' if has_retry.stdout else 'No retry/backoff in bybit_api.cpp',
        })

        return findings

    # ─── PILLAR 2: QUANTUM & MICROSTRUCTURE ─────────────────────────────
    async def _audit_microstructure(self):
        findings = []

        # 2a. Price as continuous scalar vs discrete jumps
        has_gap_check = subprocess.run(['grep', '-n', 'gap\\|jump\\|limit_up\\|limit_down', f'{LOCAL_CPP}/src/main.cpp'], capture_output=True, text=True, timeout=5)
        findings.append({
            'test': 'Price gap / discrete jump handling',
            'status': 'WARN' if not has_gap_check.stdout else 'PASS',
            'detail': 'No explicit gap detection in main loop. Price treated as continuous — dangerous in HFT gaps.' if not has_gap_check.stdout else 'Gap detection present.',
        })

        # 2b. Timeframe — ticks vs time-bars
        has_tick = subprocess.run(['grep', '-n', 'tick\\|order_book\\|LOB\\|bid.*ask\\|spread', f'{LOCAL_CPP}/src/strategy.cpp'], capture_output=True, text=True, timeout=5)
        findings.append({
            'test': 'Microstructure data (tick/LOB)',
            'status': 'FAIL' if not has_tick.stdout else 'INFO',
            'detail': 'Strategy uses time-based 1h bars only — no tick/LOB data. Missing microstructure edge.' if not has_tick.stdout else 'Some microstructure data used.',
        })

        # 2c. Execution slippage model
        has_slippage = subprocess.run(['grep', '-n', 'slippage\\|spread', f'{LOCAL_CPP}/src/bybit_api.cpp'], capture_output=True, text=True, timeout=5)
        findings.append({
            'test': 'Slippage modeling in execution',
            'status': 'WARN' if not has_slippage.stdout else 'PASS',
            'detail': 'No explicit slippage model in bybit_api.cpp' if not has_slippage.stdout else 'Slippage/spread handling found.',
        })

        return findings

    # ─── PILLAR 3: FINANCIAL AI / ML (López de Prado) ───────────────────
    async def _audit_financial_ai(self):
        findings = []

        # 3a. Fractional differentiation
        has_fractional = subprocess.run(['grep', '-n', 'fractional\\|frac_diff\\|frac_diff_ffd', f'{LOCAL_CPP}/src/quantitative_scorer.cpp'], capture_output=True, text=True, timeout=5)
        has_returns = subprocess.run(['grep', '-n', 'log_return\\|pct_change\\|return', f'{LOCAL_CPP}/src/indicators.cpp'], capture_output=True, text=True, timeout=5)
        findings.append({
            'test': 'Fractional differentiation (López de Prado)',
            'status': 'FAIL' if not has_fractional.stdout else 'PASS',
            'detail': 'No fractional differentiation found. Using log-returns or raw prices wipes market memory. Need frac_diff_ffd().' if not has_fractional.stdout else 'Fractional diff used.',
        })

        # 3b. Triple-Barrier labeling
        has_triple_barrier = subprocess.run(['grep', '-n', 'triple\\|barrier\\|horizontal', f'{LOCAL_CPP}/src/strategy.cpp'], capture_output=True, text=True, timeout=5)
        findings.append({
            'test': 'Triple-Barrier labeling method',
            'status': 'FAIL' if not has_triple_barrier.stdout else 'PASS',
            'detail': 'No Triple-Barrier method found. Model likely predicts direction directly (P_up/P_down) instead of using vertical/horizontal barriers.' if not has_triple_barrier.stdout else 'Triple-Barrier used.',
        })

        # 3c. Meta-Labeling
        has_metalabel = subprocess.run(['grep', '-n', 'meta\\|bet_size\\|confidence_weighted', f'{LOCAL_CPP}/src/ensemble_engine.cpp'], capture_output=True, text=True, timeout=5)
        findings.append({
            'test': 'Meta-Labeling (secondary bet-size model)',
            'status': 'FAIL' if not has_metalabel.stdout else 'PASS',
            'detail': 'No meta-labeling found. Bet size is deterministic (Kelly) rather than using a secondary ML model to size bets based on probability of success.' if not has_metalabel.stdout else 'Meta-labeling present.',
        })

        # 3d. Purged CV
        has_purged = subprocess.run(['grep', '-n', 'purge\\|embargo\\|purged_cv', f'{LOCAL_CPP}/tools/ga_optimizer_cli.cpp'], capture_output=True, text=True, timeout=5)
        findings.append({
            'test': 'Purged/Embargoed Cross-Validation',
            'status': 'FAIL' if not has_purged.stdout else 'PASS',
            'detail': 'GA optimizer likely uses standard CV — information leakage from serial correlation.' if not has_purged.stdout else 'Purged CV used.',
        })

        return findings

    # ─── PILLAR 4: MONEYBALL METRICS ────────────────────────────────────
    async def _audit_moneyball(self):
        findings = []

        # 4a. Overall PnL stats
        pf = _sql("SELECT ROUND(SUM(CASE WHEN pnl_usd > 0 THEN pnl_usd ELSE 0 END) / ABS(SUM(CASE WHEN pnl_usd < 0 THEN pnl_usd ELSE 0 END)), 4) FROM trade_outcomes")
        win_rate = _sql("SELECT ROUND(SUM(CASE WHEN pnl_usd > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) FROM trade_outcomes")
        total_pnl = _sql("SELECT ROUND(SUM(pnl_usd), 2) FROM trade_outcomes")
        avg_win = _sql("SELECT ROUND(AVG(pnl_usd), 4) FROM trade_outcomes WHERE pnl_usd > 0")
        avg_loss = _sql("SELECT ROUND(AVG(pnl_usd), 4) FROM trade_outcomes WHERE pnl_usd < 0")

        findings.append({
            'test': 'Profit Factor (Moneyball)',
            'status': 'PASS' if pf and float(pf) > 1.5 else 'WARN',
            'detail': f'PF = {pf} (target > 1.5)',
            'value': float(pf) if pf else 0,
        })

        findings.append({
            'test': 'Win Rate (demoted — not optimized for)',
            'status': 'INFO',
            'detail': f'WR = {win_rate}% (tracked but not optimized. Asymmetry matters more.)',
            'value': float(win_rate) if win_rate else 0,
        })

        findings.append({
            'test': 'Net PnL',
            'status': 'INFO',
            'detail': f'Net PnL = ${total_pnl}',
            'value': float(total_pnl) if total_pnl else 0,
        })

        # 4b. Max drawdown duration (recovery time)
        dd_duration = _sql("""
            WITH daily AS (
                SELECT DATE(exit_timestamp, 'unixepoch') as day, SUM(pnl_usd) as pnl
                FROM trade_outcomes GROUP BY day ORDER BY day
            ), running AS (
                SELECT day, pnl, SUM(pnl) OVER (ORDER BY day) as equity
                FROM daily
            ), peaks AS (
                SELECT day, equity, MAX(equity) OVER (ORDER BY day) as peak
                FROM running
            ), dd AS (
                SELECT day, equity, peak, (equity - peak) / NULLIF(peak, 0) * 100 as dd_pct
                FROM peaks
            )
            SELECT ROUND(MIN(dd_pct), 2) as max_dd,
                   ROUND(AVG(CASE WHEN dd_pct < 0 THEN 1 ELSE 0 END), 4) as pct_time_in_dd
            FROM dd
        """)
        if dd_duration:
            parts = dd_duration.split('|')
            findings.append({
                'test': 'Max Drawdown (Moneyball)',
                'status': 'WARN' if len(parts) > 0 and parts[0] and abs(float(parts[0])) > 15 else 'INFO',
                'detail': f'Max DD = {parts[0]}% | Time in DD = {parts[1] if len(parts) > 1 else "?"}% of days',
            })

        # 4c. Regime-level PnL
        regime_pnl = _sql("SELECT s.regime, COUNT(*), ROUND(SUM(o.pnl_usd), 2), ROUND(AVG(o.pnl_usd), 4), ROUND(SUM(CASE WHEN o.pnl_usd > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) FROM trade_outcomes o JOIN trades t ON o.trade_id = t.id JOIN signals s ON t.signal_id = s.id GROUP BY s.regime ORDER BY SUM(o.pnl_usd) ASC")
        if regime_pnl:
            regimes = []
            for line in regime_pnl.split('\n'):
                parts = line.split('|')
                if len(parts) >= 5:
                    regimes.append({
                        'regime': parts[0],
                        'trades': int(parts[1]),
                        'pnl': float(parts[2]),
                        'avg_pnl': float(parts[3]),
                        'wr': float(parts[4]),
                    })
            # Flag losing regimes
            losing = [r for r in regimes if r['pnl'] < 0]
            if losing:
                findings.append({
                    'test': 'Regime PnL breakdown',
                    'status': 'WARN',
                    'detail': 'Losing regimes: ' + ', '.join([f"{r['regime']}(${r['pnl']})" for r in losing]),
                    'regimes': regimes,
                })
            else:
                findings.append({
                    'test': 'Regime PnL breakdown',
                    'status': 'PASS',
                    'detail': 'All regimes profitable',
                    'regimes': regimes,
                })

        # 4d. Hidden alpha micro-variables
        has_micro_vars = subprocess.run(['grep', '-n', 'micro\\|alpha\\|hidden\\|feature', f'{LOCAL_CPP}/src/analytics_engine.cpp'], capture_output=True, text=True, timeout=5)
        findings.append({
            'test': 'Hidden alpha micro-variables tracked',
            'status': 'WARN' if not has_micro_vars.stdout else 'PASS',
            'detail': 'No micro-variable tracking found (funding rate, order book imbalance, etc). Potential hidden alpha not being captured.' if not has_micro_vars.stdout else 'Micro-variables tracked.',
        })

        return findings

    # ─── EXISTING: FILTER THROUGHPUT ────────────────────────────────────
    async def _audit_filter_throughput(self):
        log = _ssh(f'tail -n 2000 {LOG_PATH}') if _ssh(f'test -f {LOG_PATH} && echo ok') else _ssh(f'tail -n 2000 {CPP_DIR}/data/logs/bot_output.log')
        if not log:
            return {'error': 'No log file accessible'}
        lines = log.split('\n')
        total = sum(1 for l in lines if 'Analizando' in l)

        gates = {
            'blocked_by_learner': ('BLOQUEADO por StatisticalLearner', '🚫'),
            'blocked_by_convexity': ('CONVEXITY FILTER', '🚫'),
            'blocked_by_vol_squeeze': ('VOL SQUEEZE', '🔇'),
            'blocked_by_funding_cap': ('FUNDING DOMINANT', '📡'),
            'blocked_by_correlation': ('Hard correlation filter', '🚫'),
            'blocked_by_spread': ('SPREAD ALTO', '🚫'),
            'held_no_qualify': ('HOLD / No califica', '⏸️'),
            'canceled_by_learner': ('CANCELADO (LEARNER)', '🚫'),
        }
        result = {}
        warnings = []
        for key, (pattern, _) in gates.items():
            cnt = sum(1 for l in lines if pattern in l)
            pct = round(cnt / max(1, total) * 100, 1) if total > 0 else 0
            result[key] = {'count': cnt, 'pct': pct}

            # thresholds
            if key == 'blocked_by_convexity' and pct > 40:
                warnings.append(f'Convexity filter blocking {pct}% — regime-adaptive R:R too strict for current market')
            if key == 'blocked_by_learner' and pct > 20:
                warnings.append(f'Learner blocking {pct}% — symbol blacklist growing, check recent PnL')
            if key == 'canceled_by_learner' and pct > 5:
                warnings.append(f'Learner canceling {pct}% of viable signals — recovery tracking creating deadweight')

        result['total_signals'] = total
        result['warnings'] = warnings
        return result

    # ─── EXISTING: REGIME WEIGHTS ALIGNMENT ─────────────────────────────
    async def _audit_weights_alignment(self):
        weights_raw = _ssh(f'cat {WEIGHTS_PATH}')
        if not weights_raw:
            return {'error': 'Cannot read weights'}
        try:
            w = json.loads(weights_raw)
        except:
            return {'error': 'Parse weights failed'}

        regimes_w = w.get('regime_weights', {})
        db = _sql("SELECT s.regime, COUNT(*), ROUND(SUM(o.pnl_usd), 2), ROUND(SUM(CASE WHEN o.pnl_usd > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) FROM trade_outcomes o JOIN trades t ON o.trade_id = t.id JOIN signals s ON t.signal_id = s.id GROUP BY s.regime")
        if not db:
            return {'error': 'No DB regime data'}

        perf = {}
        for line in db.split('\n'):
            parts = line.split('|')
            if len(parts) == 4:
                perf[parts[0]] = {'trades': int(parts[1]), 'pnl': float(parts[2]), 'wr': float(parts[3])}

        alignment = []
        for regime, cfg in regimes_w.items():
            p = perf.get(regime, {'trades': 0, 'pnl': 0, 'wr': 0})
            alert = 'OK'
            if p['pnl'] < -3.0:
                if cfg.get('trend', 0) > 0.35:
                    alert = f'WARN: ${p["pnl"]} loss in {regime} but trend weight is {cfg["trend"]} — consider mean-reversion shift'
            alignment.append({'regime': regime, 'weights': cfg, 'performance': p, 'alert': alert})

        return alignment

    # ─── EXISTING: RISK SAFETY ──────────────────────────────────────────
    async def _audit_risk_safety(self):
        path = f'{LOCAL_CPP}/src/risk_manager.cpp'
        if not os.path.exists(path):
            return {'error': 'risk_manager.cpp not found'}
        with open(path) as f:
            c = f.read()
        return {
            'kelly_winrate_normalization': 'wr /= 100.0' in c,
            'small_account_protection': 'min_size_pct' in c and '5.5' in c,
            'max_drawdown_circuit': 'drawdown' in c and 'halt' in c or 'stop' in c,
            'position_sizing_ga_override': 'ga_params' in c.lower() or 'base_pct' in c,
        }

    # ─── SCORECARD ──────────────────────────────────────────────────────
    def _scorecard(self, audits):
        score = 0
        max_score = 0
        items = []

        for pillar_key in ['pillar_1_antifragility', 'pillar_2_microstructure', 'pillar_3_financial_ai', 'pillar_4_moneyball']:
            for finding in audits.get(pillar_key, []):
                max_score += 10
                if finding.get('status') == 'PASS':
                    score += 10
                elif finding.get('status') == 'WARN':
                    score += 5
                items.append({
                    'test': finding.get('test', '?'),
                    'status': finding.get('status', '?'),
                    'score': 10 if finding.get('status') == 'PASS' else (5 if finding.get('status') == 'WARN' else 0),
                })

        pct = round(score / max(1, max_score) * 100, 1)
        grade = 'A' if pct >= 80 else 'B' if pct >= 60 else 'C' if pct >= 40 else 'D' if pct >= 20 else 'F'

        return {
            'score': score,
            'max_score': max_score,
            'percentage': pct,
            'grade': grade,
        }


if __name__ == '__main__':
    import asyncio
    a = QuantAuditor4D()
    print(json.dumps(asyncio.run(a.run()), indent=2, default=str))
