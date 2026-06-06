#!/usr/bin/env python3
"""DAS Validation Agent — webhook health, agent health, container status, n8n config."""

import os, sys, subprocess, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from agents.base.base_agent import BaseAgent

SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), 'scripts')
REMOTE_HOST = '100.74.53.2'
SSH_USER = 'arturo'

N8N_URL = f'http://{REMOTE_HOST}:5679'
AGENT_URL = f'http://{REMOTE_HOST}:8002'
FRONTEND_URL = f'http://{REMOTE_HOST}:3002'

class DasValidationAgent(BaseAgent):
    def __init__(self):
        super().__init__('das-validation')
        self.scripts = {
            'webhook': ['bash', 'check-webhook.sh'],
            'agent': ['bash', 'check-agent.sh'],
            'containers': ['bash', 'check-containers.sh'],
        }

    async def run(self, input_data=None):
        mode = (input_data or {}).get('mode', 'discover')
        if mode == 'discover':
            env = await self._discover_environment()
            return {'environment': env, 'audits': await self._run_selected(self._select_audits(env))}
        return {'audits': await self._run_selected(list(self.scripts.keys()))}

    async def _discover_environment(self):
        env = {'servers': {}, 'n8n': {}, 'agent': {}, 'frontend': {}, 'containers': []}

        r = subprocess.run(['ssh', '-o', 'ConnectTimeout=3', f'{SSH_USER}@{REMOTE_HOST}', 'echo ok'],
                           capture_output=True, text=True, timeout=10)
        env['servers'][REMOTE_HOST] = 'alive' if r.returncode == 0 else 'dead'

        if env['servers'][REMOTE_HOST] == 'dead':
            return env

        r = subprocess.run(['ssh', REMOTE_HOST, 'docker ps --format "{{.Names}}"'],
                           capture_output=True, text=True, timeout=15)
        if r.returncode == 0:
            env['containers'] = [c.strip() for c in r.stdout.strip().split('\n') if c.strip()]

        r = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', f'{N8N_URL}/healthz'],
                           capture_output=True, text=True, timeout=10)
        env['n8n']['http_code'] = r.stdout.strip()

        r = subprocess.run(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', f'{AGENT_URL}/health'],
                           capture_output=True, text=True, timeout=10)
        env['agent']['http_code'] = r.stdout.strip()

        return env

    def _select_audits(self, env):
        if env['servers'].get(REMOTE_HOST) == 'dead':
            return []
        return list(self.scripts.keys())

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
    result = asyncio.run(DasValidationAgent().run({'mode': mode}))
    print(json.dumps(result, indent=2))
