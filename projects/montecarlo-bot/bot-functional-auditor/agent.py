#!/usr/bin/env python3
"""Bot Functional Auditor — end-to-end audit of bot modules."""

import os, sys, subprocess, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from agents.base.base_agent import BaseAgent

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'scripts')

class BotFunctionalAuditorAgent(BaseAgent):
    def __init__(self):
        super().__init__('bot-functional-auditor')
        self.scripts = {
            'full_audit':    ['bash', 'full_audit.sh'],
            'maintenance_prod':   ['bash', 'run_maintenance_prod.sh'],
            'maintenance_system': ['bash', 'run_maintenance_system.sh'],
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
        env = {'servers': {}, 'bot_pid': None}
        for host in ['100.74.53.2', '192.168.1.149']:
            r = subprocess.run(['ssh', '-o', 'ConnectTimeout=3', f'arturo@{host}', 'echo ok'],
                               capture_output=True, text=True, timeout=10)
            alive = r.returncode == 0
            env['servers'][host] = 'alive' if alive else 'dead'
            if alive:
                pid = subprocess.run(['ssh', f'arturo@{host}', 'pgrep -f trading_bot'],
                                     capture_output=True, text=True, timeout=5)
                env['bot_pid'] = pid.stdout.strip() if pid.returncode == 0 else None
                cpu = subprocess.run(['ssh', f'arturo@{host}',
                                      "ps -o %cpu,%mem,rss -p $(pgrep -f trading_bot) 2>/dev/null"],
                                     capture_output=True, text=True, timeout=5)
                env['bot_resources'] = cpu.stdout.strip() if cpu.returncode == 0 else None
                db = subprocess.run(['ssh', f'arturo@{host}',
                                     'ls -lh /home/arturo/monteCarlo/cpp_bot/data/trading_data.db 2>/dev/null'],
                                    capture_output=True, text=True, timeout=5)
                env['db_size'] = db.stdout.strip() if db.returncode == 0 else 'no db'
                break
        return env

    def _select_audits(self, env):
        selected = []
        if any(v == 'alive' for v in env['servers'].values()):
            selected.append('full_audit')
        return selected

    async def run_all(self):
        return {'audits': await self._run_selected(list(self.scripts.keys()))}

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
    result = asyncio.run(BotFunctionalAuditorAgent().run({'mode': mode}))
    print(json.dumps(result, indent=2))
