#!/usr/bin/env python3
"""Database Auditor Agent — extends BaseAgent, runs static audits."""

import os, sys, subprocess, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from agents.base.base_agent import BaseAgent, AgentMessage

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'scripts')

class DatabaseAuditorAgent(BaseAgent):
    def __init__(self):
        super().__init__('database-auditor')
        self.scripts = {
            'pnl':      ['bash', 'audit_pnl.sh'],
            'fees':     ['python3', 'audit_fees.py'],
            'deep_pnl': ['python3', 'deep_pnl_audit.py'],
            'bybit':    ['python3', 'check_bybit_direct.py'],
            'wallet':   ['python3', 'check_wallet.py'],
        }

    async def run(self, input_data=None):
        """
        Run static audits. input_data can specify which audits to run:
          {"mode": "full"}     — all scripts
          {"mode": "pnl"}      — just pnl
          {"mode": "discover"} — discover environment first, then decide
        """
        if input_data is None:
            input_data = {}

        mode = input_data.get('mode', 'full')

        if mode == 'discover':
            self._env = await self._discover_environment()
            results = {'environment': self._env}
            results['audits'] = await self._run_selected(self._select_audits(self._env), self._env.get('env_path'))
            return results

        selected = list(self.scripts.keys()) if mode == 'full' else [mode]
        return {'audits': await self._run_selected(selected)}

    async def _discover_environment(self):
        """Dynamic discovery: find live server, check DB schema, tools, .env."""
        env = {'servers': {}, 'db': None, 'tools': [], 'env_path': None}

        for host in ['100.74.53.2', '192.168.1.149']:
            result = subprocess.run(
                ['ssh', '-o', 'ConnectTimeout=3', f'arturo@{host}', 'echo ok'],
                capture_output=True, text=True, timeout=10
            )
            alive = result.returncode == 0
            env['servers'][host] = 'alive' if alive else 'dead'

            if alive:
                # Check DB
                for db_path in [
                    '/home/arturo/monteCarlo/cpp_bot/data/trading_data.db',
                    '/home/arturo/monteCarlo/data/trading_data.db'
                ]:
                    r = subprocess.run(
                        ['ssh', f'arturo@{host}', f'ls {db_path} 2>/dev/null && echo EXISTS'],
                        capture_output=True, text=True, timeout=5
                    )
                    if 'EXISTS' in r.stdout:
                        env['db'] = {'host': host, 'path': db_path}
                        # Check tables
                        r2 = subprocess.run(
                            ['ssh', f'arturo@{host}',
                             f'sqlite3 {db_path} ".tables"'],
                            capture_output=True, text=True, timeout=5
                        )
                        env['db']['tables'] = r2.stdout.strip().split()
                        # Check columns
                        for table in ['trades', 'trade_outcomes']:
                            r3 = subprocess.run(
                                ['ssh', f'arturo@{host}',
                                 f'sqlite3 {db_path} "PRAGMA table_info({table});"'],
                                capture_output=True, text=True, timeout=5
                            )
                            cols = [line.split('|')[1] for line in r3.stdout.strip().split('\n') if line]
                            env['db'][f'{table}_columns'] = cols
                        break

                # Check tools
                for tool in ['sqlite3', 'python3', 'sshpass']:
                    r = subprocess.run(
                        ['ssh', f'arturo@{host}', f'which {tool} 2>/dev/null || echo MISSING'],
                        capture_output=True, text=True, timeout=5
                    )
                    if 'MISSING' not in r.stdout:
                        env['tools'].append(tool)

                # Discover and fetch .env for scripts that need API keys
                for env_path in [
                    '/home/arturo/monteCarlo/cpp_bot/.env',
                    '/home/arturo/monteCarlo/.env',
                ]:
                    r = subprocess.run(
                        ['ssh', f'arturo@{host}', f'ls {env_path} 2>/dev/null && echo EXISTS'],
                        capture_output=True, text=True, timeout=5
                    )
                    if 'EXISTS' in r.stdout:
                        env['env_path'] = env_path
                        break

        return env

    def _select_audits(self, env):
        """Based on environment, decide which audits to run."""
        selected = []
        if env.get('db'):
            selected.append('pnl')
        if 'python3' in env.get('tools', []):
            selected.append('fees')
            selected.append('deep_pnl')
            if env['servers'].get('100.74.53.2') == 'alive':
                selected.append('bybit')
                selected.append('wallet')
        return selected

    def _server_host(self):
        return next((h for h, s in self._env.get('servers', {}).items() if s == 'alive'), None)

    async def _run_selected(self, names, env_path=None):
        results = {}
        host = self._server_host()

        for name in names:
            if name not in self.scripts:
                results[name] = {'error': f'Unknown audit: {name}'}
                continue
            interpreter, script = self.scripts[name]
            script_path = os.path.join(SCRIPTS_DIR, script)

            # Fee/bybit/wallet scripts need .env — run on server via SSH
            if name in ('fees', 'deep_pnl', 'bybit', 'wallet') and host:
                if not os.path.exists(script_path):
                    results[name] = {'error': 'script not found'}
                    continue
                # Copy script to server, run there, capture output
                script_name = os.path.basename(script_path)
                subprocess.run(
                    ['scp', script_path, f'arturo@{host}:/tmp/{script_name}'],
                    capture_output=True, text=True, timeout=10
                )
                # Ensure .env symlink for scripts that expect /home/arturo/monteCarlo/.env
                subprocess.run(
                    ['ssh', f'arturo@{host}',
                     'ln -sf /home/arturo/monteCarlo/cpp_bot/.env /home/arturo/monteCarlo/.env 2>/dev/null'],
                    capture_output=True, text=True, timeout=5
                )
                r = subprocess.run(
                    ['ssh', f'arturo@{host}', f'cd /home/arturo/monteCarlo && python3 /tmp/{script_name}'],
                    capture_output=True, text=True, timeout=60
                )
                results[name] = {
                    'stdout': r.stdout,
                    'stderr': r.stderr,
                    'returncode': r.returncode
                }
                continue

            # Local scripts
            if not os.path.exists(script_path):
                results[name] = {'error': f'Script not found: {script_path}'}
                continue
            try:
                r = subprocess.run(
                    [interpreter, script_path],
                    capture_output=True, text=True, timeout=60
                )
                results[name] = {
                    'stdout': r.stdout,
                    'stderr': r.stderr,
                    'returncode': r.returncode
                }
            except subprocess.TimeoutExpired:
                results[name] = {'error': 'timeout'}
        return results

    def health_check(self):
        status = super().health_check()
        missing = [s for s, (i, p) in self.scripts.items()
                   if not os.path.exists(os.path.join(SCRIPTS_DIR, p))]
        status['scripts_missing'] = missing
        return status


if __name__ == '__main__':
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else 'discover'
    agent = DatabaseAuditorAgent()
    result = asyncio.run(agent.run({'mode': mode}))
    print(json.dumps(result, indent=2))
