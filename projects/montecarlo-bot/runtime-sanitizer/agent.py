#!/usr/bin/env python3
"""Runtime Sanitizer Agent — memory safety and UB profiling."""

import os, sys, subprocess, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from agents.base.base_agent import BaseAgent

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'scripts')
LOCAL_CPP_BOT = '/Users/arturo/development/lumina/monteCarlo/cpp_bot'

class RuntimeSanitizerAgent(BaseAgent):
    def __init__(self):
        super().__init__('runtime-sanitizer')
        self.scripts = {'sanitizer': ['bash', 'run-sanitizer.sh']}

    async def run(self, input_data=None):
        mode = (input_data or {}).get('mode', 'discover')
        if mode == 'discover':
            env = await self._discover_environment()
            return {'environment': env, 'audits': await self._run_selected(self._select_audits(env))}
        return {'audits': await self._run_selected(list(self.scripts.keys()))}

    async def _discover_environment(self):
        env = {'servers': {}, 'tools': {}, 'compiler': None, 'cmake_flags': None, 'cpp_bot_exists': False}

        # Local
        if os.path.isdir(LOCAL_CPP_BOT):
            env['cpp_bot_exists'] = True
            cmake = os.path.join(LOCAL_CPP_BOT, 'CMakeLists.txt')
            if os.path.exists(cmake):
                r = subprocess.run(['grep', 'CMAKE_CXX_FLAGS', cmake], capture_output=True, text=True, timeout=5)
                env['cmake_flags'] = r.stdout.strip() if r.stdout.strip() else None

        r = subprocess.run(['g++', '--version'], capture_output=True, text=True, timeout=5)
        env['compiler'] = r.stdout.split('\n')[0] if r.returncode == 0 else None

        # Server tools
        for host in ['100.74.53.2', '192.168.1.149']:
            r = subprocess.run(['ssh', '-o', 'ConnectTimeout=3', f'arturo@{host}', 'echo ok'],
                               capture_output=True, text=True, timeout=10)
            alive = r.returncode == 0
            env['servers'][host] = 'alive' if alive else 'dead'
            if alive:
                for tool in ['valgrind', 'cppcheck', 'clang-tidy']:
                    r = subprocess.run(['ssh', f'arturo@{host}', f'which {tool} 2>/dev/null || echo MISSING'],
                                       capture_output=True, text=True, timeout=5)
                    env['tools'][tool] = r.stdout.strip() if 'MISSING' not in r.stdout else None
                break

        return env

    def _select_audits(self, env):
        selected = []
        if env['cpp_bot_exists'] or any(v == 'alive' for v in env['servers'].values()):
            selected.append('sanitizer')
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
    result = asyncio.run(RuntimeSanitizerAgent().run({'mode': mode}))
    print(json.dumps(result, indent=2))
