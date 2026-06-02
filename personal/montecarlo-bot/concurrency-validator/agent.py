#!/usr/bin/env python3
"""Concurrency Validator Agent — thread-safety and dynamic race auditing."""

import os, sys, subprocess, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from agents.base.base_agent import BaseAgent

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'scripts')
LOCAL_CPP_BOT = '/Users/arturo/development/lumina/monteCarlo/cpp_bot'

class ConcurrencyValidatorAgent(BaseAgent):
    def __init__(self):
        super().__init__('concurrency-validator')
        self.scripts = {'concurrency': ['bash', 'run-concurrency.sh']}

    async def run(self, input_data=None):
        mode = (input_data or {}).get('mode', 'discover')
        if mode == 'discover':
            env = await self._discover_environment()
            return {'environment': env, 'audits': await self._run_selected(self._select_audits(env))}
        return {'audits': await self._run_selected(list(self.scripts.keys()))}

    async def _discover_environment(self):
        env = {'servers': {}, 'compiler': None, 'cpp_bot_exists': False, 'tsan_supported': False}

        if os.path.isdir(LOCAL_CPP_BOT):
            env['cpp_bot_exists'] = True

        r = subprocess.run(['g++', '--version'], capture_output=True, text=True, timeout=5)
        env['compiler'] = r.stdout.split('\n')[0] if r.returncode == 0 else None

        # Check local ThreadSanitizer support
        tsan_test = subprocess.run(['g++', '-fsanitize=thread', '-x', 'c++', '-', '-o', '/dev/null'],
                                   input='int main() {}', capture_output=True, text=True, timeout=5)
        env['tsan_supported'] = tsan_test.returncode == 0

        # Server
        host = '100.74.53.2'
        r = subprocess.run(['ssh', '-o', 'ConnectTimeout=3', f'arturo@{host}', 'echo ok'],
                           capture_output=True, text=True, timeout=10)
        env['servers'][host] = 'alive' if r.returncode == 0 else 'dead'

        return env

    def _select_audits(self, env):
        selected = []
        if env['cpp_bot_exists']:
            selected.append('concurrency')
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
    result = asyncio.run(ConcurrencyValidatorAgent().run({'mode': mode}))
    print(json.dumps(result, indent=2))
