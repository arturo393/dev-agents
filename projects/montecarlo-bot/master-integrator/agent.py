#!/usr/bin/env python3
"""Master Integrator Agent — orchestrates all agents and consolidates results."""

import os, sys, subprocess, json, asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from agents.base.base_agent import BaseAgent

AGENTS_DIR = os.path.join(os.path.dirname(__file__), '..')

class MasterIntegratorAgent(BaseAgent):
    def __init__(self):
        super().__init__('master-integrator')
        self.agent_order = [
            'backtest-agent',
            'bio-cognitive-guard',
            'bot-functional-auditor',
            'runtime-sanitizer',
            'btd-sdd-validation',
            'cleanup-engine',
            'check-server-logs',
            'cpp-trading-reviewer',
            'database-auditor',
            'strategy-reviewer',
            'concurrency-validator',
        ]

    async def run(self, input_data=None):
        mode = (input_data or {}).get('mode', 'discover')
        results = {}

        for agent_name in self.agent_order:
            agent_dir = os.path.join(AGENTS_DIR, agent_name)
            agent_py = os.path.join(agent_dir, 'agent.py')
            if not os.path.exists(agent_py):
                results[agent_name] = {'error': 'agent.py not found'}
                continue

            r = subprocess.run(
                ['python3', agent_py, mode],
                capture_output=True, text=True, timeout=180
            )
            results[agent_name] = {
                'stdout': r.stdout,
                'stderr': r.stderr,
                'returncode': r.returncode
            }

        return results


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'discover'
    result = asyncio.run(MasterIntegratorAgent().run({'mode': mode}))
    print(json.dumps(result, indent=2))
