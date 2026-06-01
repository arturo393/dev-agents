#!/usr/bin/env python3
"""Cleanup Engine Agent — dead code removal and repo sanitation."""

import os, sys, subprocess, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from agents.base.base_agent import BaseAgent

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'scripts')
LOCAL_CPP_BOT = '/Users/arturo/development/lumina/monteCarlo/cpp_bot'
LOCAL_MONTE = '/Users/arturo/development/lumina/monteCarlo'

class CleanupEngineAgent(BaseAgent):
    def __init__(self):
        super().__init__('cleanup-engine')
        self.scripts = {'cleanup': ['bash', 'run-cleanup.sh']}

    async def run(self, input_data=None):
        mode = (input_data or {}).get('mode', 'discover')
        if mode == 'discover':
            env = await self._discover_environment()
            return {'environment': env, 'audits': await self._run_selected(self._select_audits(env))}
        return {'audits': await self._run_selected(list(self.scripts.keys()))}

    async def _discover_environment(self):
        env = {'cpp_bot_exists': os.path.isdir(LOCAL_CPP_BOT), 'cmake_sources': [], 'dead_code': [], 'junk': {}}

        if os.path.isdir(LOCAL_CPP_BOT):
            # Parse CMakeLists.txt for compiled sources
            cmake_path = os.path.join(LOCAL_CPP_BOT, 'CMakeLists.txt')
            if os.path.exists(cmake_path):
                r = subprocess.run(['grep', '-A50', 'set(SOURCES', cmake_path],
                                   capture_output=True, text=True, timeout=10)
                env['cmake_sources'] = [l.strip() for l in r.stdout.split('\n')
                                        if l.strip().startswith('src/')]

            # Check which are referenced in main.cpp
            main_path = os.path.join(LOCAL_CPP_BOT, 'src', 'main.cpp')
            for src in env['cmake_sources']:
                basename = os.path.basename(src).replace('.cpp', '')
                r = subprocess.run(['grep', '-c', basename, main_path],
                                   capture_output=True, text=True, timeout=5)
                if int(r.stdout.strip() or 0) == 0:
                    env['dead_code'].append(src)

            # Junk files
            for pattern, cmd in [('.DS_Store', ['find', LOCAL_MONTE, '-name', '.DS_Store', '-type', 'f']),
                                  ('__pycache__', ['find', LOCAL_MONTE, '-type', 'd', '-name', '__pycache__']),
                                  ('*.bak', ['find', LOCAL_MONTE, '-name', '*.bak', '-type', 'f'])]:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                env['junk'][pattern] = len(r.stdout.strip().split('\n')) if r.stdout.strip() else 0

        # Server-side checks
        env['servers'] = {}
        for host in ['100.74.53.2', '192.168.1.149']:
            r = subprocess.run(['ssh', '-o', 'ConnectTimeout=3', f'arturo@{host}', 'echo ok'],
                               capture_output=True, text=True, timeout=10)
            env['servers'][host] = 'alive' if r.returncode == 0 else 'dead'

        return env

    def _select_audits(self, env):
        return list(self.scripts.keys()) if env['cpp_bot_exists'] else []

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
    result = asyncio.run(CleanupEngineAgent().run({'mode': mode}))
    print(json.dumps(result, indent=2))
