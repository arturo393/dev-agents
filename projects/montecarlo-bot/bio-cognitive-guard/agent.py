#!/usr/bin/env python3
"""Bio-Cognitive Guard Agent — cognitive load, alert fatigue, circadian resilience."""

import os, sys, subprocess, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from agents.base.base_agent import BaseAgent

MONTE_REPO = '/Users/arturo/development/lumina/monteCarlo'
SCRIPTS_DIR = os.path.join(MONTE_REPO, 'tools', 'skills', 'bio_cognitive_guard', 'scripts')

class BioCognitiveGuardAgent(BaseAgent):
    def __init__(self):
        super().__init__('bio-cognitive-guard')
        self.scripts = {
            'cognitive_load': ['bash', 'audit_cognitive_load.sh'],
            'alert_fatigue':  ['bash', 'audit_alert_fatigue.sh'],
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
        env = {'cpp_bot_dir': os.path.join(MONTE_REPO, 'cpp_bot'), 'servers': {}, 'systemd_errors': None}
        for host in ['100.74.53.2', '192.168.1.149']:
            r = subprocess.run(['ssh', '-o', 'ConnectTimeout=3', f'arturo@{host}', 'echo ok'],
                               capture_output=True, text=True, timeout=10)
            alive = r.returncode == 0
            env['servers'][host] = 'alive' if alive else 'dead'
            if alive:
                err = subprocess.run(['ssh', f'arturo@{host}',
                                      "journalctl -u montecarlo_bot --since '1 hour ago' -p err --no-pager 2>/dev/null | tail -10"],
                                     capture_output=True, text=True, timeout=10)
                env['systemd_errors'] = err.stdout.strip() if err.returncode == 0 else None
                break
        return env

    def _select_audits(self, env):
        return list(self.scripts.keys())

    async def _run_selected(self, names):
        results = {}
        for name in names:
            if name not in self.scripts:
                continue
            interp, script = self.scripts[name]
            sp = os.path.join(SCRIPTS_DIR, script)
            if not os.path.exists(sp):
                results[name] = {'error': f'script not found at {sp}'}
                continue
            r = subprocess.run([interp, sp], capture_output=True, text=True, timeout=120)
            results[name] = {'stdout': r.stdout, 'stderr': r.stderr, 'returncode': r.returncode}
        return results


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'discover'
    result = asyncio.run(BioCognitiveGuardAgent().run({'mode': mode}))
    print(json.dumps(result, indent=2))
