#!/usr/bin/env python3
"""Backtest Agent — extends BaseAgent, runs GA optimization pipeline."""

import os, sys, subprocess, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from agents.base.base_agent import BaseAgent

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'scripts')

class BacktestAgent(BaseAgent):
    def __init__(self):
        super().__init__('backtest-agent')
        self.scripts = {'backtest': ['bash', 'run_backtest.sh']}

    async def run(self, input_data=None):
        mode = (input_data or {}).get('mode', 'discover')
        if mode == 'discover':
            env = await self._discover_environment()
            return {'environment': env, 'audits': await self._run_selected(self._select_audits(env))}
        return {'audits': await self._run_selected(list(self.scripts.keys()))}

    async def _discover_environment(self):
        env = {'servers': {}, 'ga_running': False, 'disk': None, 'last_run': None}
        for host in ['100.74.53.2', '192.168.1.149']:
            r = subprocess.run(['ssh', '-o', 'ConnectTimeout=3', f'arturo@{host}', 'echo ok'],
                               capture_output=True, text=True, timeout=10)
            alive = r.returncode == 0
            env['servers'][host] = 'alive' if alive else 'dead'
            if alive:
                ga = subprocess.run(['ssh', f'arturo@{host}', 'pgrep -a ga_optimizer'],
                                    capture_output=True, text=True, timeout=5)
                env['ga_running'] = ga.returncode == 0
                env['ga_cmd'] = ga.stdout.strip() if ga.returncode == 0 else None
                disk = subprocess.run(['ssh', f'arturo@{host}', "df -h /home/arturo/monteCarlo/data/ | tail -1"],
                                      capture_output=True, text=True, timeout=5)
                env['disk'] = disk.stdout.strip() if disk.returncode == 0 else None
                last = subprocess.run(['ssh', f'arturo@{host}',
                                       'ls -lt /home/arturo/monteCarlo/data/backtest_results/ 2>/dev/null | head -3'],
                                      capture_output=True, text=True, timeout=5)
                env['last_run'] = last.stdout.strip() if last.returncode == 0 else 'no results dir'
                break
        return env

    def _select_audits(self, env):
        selected = []
        if any(v == 'alive' for v in env['servers'].values()):
            selected.append('backtest')
        return selected

    async def _run_selected(self, names):
        results = {}
        for name in names:
            if name not in self.scripts:
                continue
            interp, script = self.scripts[name]
            sp = os.path.join(SCRIPTS_DIR, script)
            if not os.path.exists(sp):
                results[name] = {'error': 'script not found'}
                continue
            r = subprocess.run([interp, sp], capture_output=True, text=True, timeout=120)
            results[name] = {'stdout': r.stdout, 'stderr': r.stderr, 'returncode': r.returncode}
        return results


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'discover'
    result = asyncio.run(BacktestAgent().run({'mode': mode}))
    print(json.dumps(result, indent=2))
