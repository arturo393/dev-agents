#!/usr/bin/env python3
"""Check Server Logs Agent — fetches and analyzes production logs."""

import os, sys, subprocess, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from agents.base.base_agent import BaseAgent

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'scripts')

class CheckServerLogsAgent(BaseAgent):
    def __init__(self):
        super().__init__('check-server-logs')
        self.scripts = {'fetch_logs': ['bash', 'fetch_logs.sh']}

    async def run(self, input_data=None):
        mode = (input_data or {}).get('mode', 'discover')
        lines = (input_data or {}).get('lines', 100)
        logfile = (input_data or {}).get('logfile', 'bot_production.log')
        if mode == 'discover':
            env = await self._discover_environment()
            return {'environment': env, 'audits': await self._run_selected(self._select_audits(env), lines, logfile)}
        return {'audits': await self._run_selected(list(self.scripts.keys()), lines, logfile)}

    async def _discover_environment(self):
        env = {'servers': {}, 'log_files': [], 'error_count': 0}
        for host in ['100.74.53.2', '192.168.1.149']:
            r = subprocess.run(['ssh', '-o', 'ConnectTimeout=3', f'arturo@{host}', 'echo ok'],
                               capture_output=True, text=True, timeout=10)
            alive = r.returncode == 0
            env['servers'][host] = 'alive' if alive else 'dead'
            if alive:
                logs = subprocess.run(['ssh', f'arturo@{host}',
                                       'ls /home/arturo/monteCarlo/data/logs/*.log 2>/dev/null | head -10'],
                                      capture_output=True, text=True, timeout=5)
                env['log_files'] = logs.stdout.strip().split('\n') if logs.stdout.strip() else []
                errs = subprocess.run(['ssh', f'arturo@{host}',
                                       "tail -100 /home/arturo/monteCarlo/data/logs/bot_production.log 2>/dev/null | grep -ci 'error\\|exception\\|fail\\|timeout'"],
                                      capture_output=True, text=True, timeout=5)
                env['error_count'] = int(errs.stdout.strip() or 0)
                break
        return env

    def _select_audits(self, env):
        return list(self.scripts.keys()) if env['log_files'] else []

    async def _run_selected(self, names, lines=100, logfile='bot_production.log'):
        results = {}
        for name in names:
            if name not in self.scripts:
                continue
            interp, script = self.scripts[name]
            sp = os.path.join(SCRIPTS_DIR, script)
            if not os.path.exists(sp):
                results[name] = {'error': 'script not found'}
                continue
            r = subprocess.run([interp, sp, str(lines), logfile],
                               capture_output=True, text=True, timeout=30)
            results[name] = {'stdout': r.stdout, 'stderr': r.stderr, 'returncode': r.returncode}
        return results


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'discover'
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', nargs='?', default='discover')
    parser.add_argument('--lines', type=int, default=100)
    parser.add_argument('--logfile', default='bot_production.log')
    args = parser.parse_args()
    result = asyncio.run(CheckServerLogsAgent().run({'mode': args.mode, 'lines': args.lines, 'logfile': args.logfile}))
    print(json.dumps(result, indent=2))
