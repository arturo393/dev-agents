#!/usr/bin/env python3
"""Validation Agent — BDD/TDD/ATT/SDD multi-layer validation."""

import os, sys, subprocess, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from agents.base.base_agent import BaseAgent

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'scripts')

class ValidationAgent(BaseAgent):
    def __init__(self):
        super().__init__('btd-sdd-validation')
        self.scripts = {'validation': ['bash', 'run-validation.sh']}

    async def run(self, input_data=None):
        mode = (input_data or {}).get('mode', 'discover')
        if mode == 'discover':
            env = await self._discover_environment()
            return {'environment': env, 'audits': await self._run_selected(self._select_audits(env))}
        return {'audits': await self._run_selected(list(self.scripts.keys()))}

    async def _discover_environment(self):
        env = {'servers': {}, 'env_file': None, 'binaries': [], 'test_binaries': []}
        for host in ['100.74.53.2', '192.168.1.149']:
            r = subprocess.run(['ssh', '-o', 'ConnectTimeout=3', f'arturo@{host}', 'echo ok'],
                               capture_output=True, text=True, timeout=10)
            alive = r.returncode == 0
            env['servers'][host] = 'alive' if alive else 'dead'
            if alive:
                has_env = subprocess.run(['ssh', f'arturo@{host}',
                                          'ls /home/arturo/monteCarlo/cpp_bot/.env 2>/dev/null && echo EXISTS'],
                                         capture_output=True, text=True, timeout=5)
                env['env_file'] = 'EXISTS' in has_env.stdout

                bins = subprocess.run(['ssh', f'arturo@{host}',
                                       'ls /home/arturo/monteCarlo/cpp_bot/build/trading_bot 2>/dev/null && echo OK'],
                                      capture_output=True, text=True, timeout=5)
                env['binaries'] = ['trading_bot'] if 'OK' in bins.stdout else []

                tests = subprocess.run(['ssh', f'arturo@{host}',
                                        'ls /home/arturo/monteCarlo/cpp_bot/build/test_* 2>/dev/null'],
                                       capture_output=True, text=True, timeout=5)
                env['test_binaries'] = [t.strip() for t in tests.stdout.strip().split('\n') if t.strip()]

                bybit = subprocess.run(['ssh', f'arturo@{host}',
                                        'curl -s -o /dev/null -w "%{http_code}" https://api.bybit.com'],
                                       capture_output=True, text=True, timeout=10)
                env['bybit_api'] = bybit.stdout.strip()

                bot = subprocess.run(['ssh', f'arturo@{host}', 'pgrep -f trading_bot'],
                                     capture_output=True, text=True, timeout=5)
                env['bot_alive'] = bot.returncode == 0
                break
        return env

    def _select_audits(self, env):
        selected = []
        if any(v == 'alive' for v in env['servers'].values()):
            selected.append('validation')
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
    result = asyncio.run(ValidationAgent().run({'mode': mode}))
    print(json.dumps(result, indent=2))
