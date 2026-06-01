#!/usr/bin/env python3
"""CPP Trading Reviewer — C++ static analysis and trading safety auditor."""

import os, sys, subprocess, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from agents.base.base_agent import BaseAgent

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'scripts')
LOCAL_CPP_BOT = '/Users/arturo/development/lumina/monteCarlo/cpp_bot'

class CppReviewerAgent(BaseAgent):
    def __init__(self):
        super().__init__('cpp-trading-reviewer')
        self.scripts = {
            'full_audit':  ['bash', 'run_full_audit.sh'],
            'analyzer':    ['python3', 'analyzer.py'],
            'review':      ['bash', 'review_module.sh'],
        }

    async def run(self, input_data=None):
        mode = (input_data or {}).get('mode', 'discover')
        if mode == 'discover':
            env = await self._discover_environment()
            return {'environment': env, 'audits': await self._run_selected(self._select_audits(env))}
        if mode in self.scripts:
            return {'audits': await self._run_selected([mode])}
        return {'audits': await self._run_selected(list(self.scripts.keys()))}

    async def _discover_environment(self):
        env = {'cpp_bot_exists': os.path.isdir(LOCAL_CPP_BOT), 'files': {}, 'patterns': {}}

        if os.path.isdir(LOCAL_CPP_BOT):
            # File counts
            for ext in ['.cpp', '.hpp', '.h']:
                r = subprocess.run(['find', LOCAL_CPP_BOT + '/src', '-name', f'*{ext}', '-type', 'f'],
                                   capture_output=True, text=True, timeout=10)
                env['files'][ext] = len(r.stdout.strip().split('\n')) if r.stdout.strip() else 0

            # Known patterns
            checks = {
                'raw_new_delete': ['grep', '-rn', r'new \|delete ', LOCAL_CPP_BOT + '/src', '--include=*.cpp'],
                'noexcept_violations': ['grep', '-rn', 'noexcept', LOCAL_CPP_BOT + '/src', '--include=*.cpp', '--include=*.hpp'],
                'reinterpret_cast': ['grep', '-rn', 'reinterpret_cast', LOCAL_CPP_BOT + '/src', '--include=*.cpp', '--include=*.hpp'],
                'c_style_casts': ['grep', '-rn', '(int)\|(float)\|(double)', LOCAL_CPP_BOT + '/src', '--include=*.cpp'],
            }
            for name, cmd in checks.items():
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                env['patterns'][name] = len(r.stdout.strip().split('\n')) if r.stdout.strip() else 0

            # Compiler info
            r = subprocess.run(['g++', '--version'], capture_output=True, text=True, timeout=5)
            env['compiler'] = r.stdout.split('\n')[0] if r.returncode == 0 else None

        return env

    def _select_audits(self, env):
        selected = []
        if env['cpp_bot_exists']:
            selected.append('full_audit')
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
            # run from cpp_bot dir since scripts use relative paths
            cwd = LOCAL_CPP_BOT if os.path.isdir(LOCAL_CPP_BOT) else None
            r = subprocess.run([interp, sp], capture_output=True, text=True, timeout=120, cwd=cwd)
            results[name] = {'stdout': r.stdout, 'stderr': r.stderr, 'returncode': r.returncode}
        return results


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'discover'
    result = asyncio.run(CppReviewerAgent().run({'mode': mode}))
    print(json.dumps(result, indent=2))
