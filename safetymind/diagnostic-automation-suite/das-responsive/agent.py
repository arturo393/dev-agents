#!/usr/bin/env python3
"""DAS Responsive Agent — Playwright-based viewport responsiveness audit."""

import os
import sys
import subprocess
import json
import asyncio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from agents.base.base_agent import BaseAgent

REMOTE_HOST = '100.74.53.2'
SSH_USER = 'arturo'
REMOTE_PROJECT_DIR = '/opt/safetymind/diagnostic-automation-suite'

class DasResponsiveAgent(BaseAgent):
    def __init__(self):
        super().__init__('das-responsive')

    async def run(self, input_data=None):
        mode = (input_data or {}).get('mode', 'discover')
        if mode == 'discover':
            print("Discovering environment...")
            # Verify server is reachable
            r = subprocess.run(['ssh', '-o', 'ConnectTimeout=3', f'{SSH_USER}@{REMOTE_HOST}', 'echo ok'],
                               capture_output=True, text=True, timeout=10)
            if r.returncode != 0:
                return {'status': 'error', 'message': f'Remote host {REMOTE_HOST} is unreachable'}
            
        print("Running Playwright responsiveness audit on the server...")
        # Trigger the npm test:responsive script on the production server
        cmd = f"cd {REMOTE_PROJECT_DIR}/frontend && REMOTE_HOST=localhost node ui-responsive-audit.cjs"
        r = subprocess.run(['ssh', f'{SSH_USER}@{REMOTE_HOST}', cmd], capture_output=True, text=True, timeout=120)
        
        # Read the generated report from the server
        read_cmd = f"cat {REMOTE_PROJECT_DIR}/test-results/responsive-audit.json"
        r_report = subprocess.run(['ssh', f'{SSH_USER}@{REMOTE_HOST}', read_cmd], capture_output=True, text=True, timeout=10)
        
        report_data = {}
        if r_report.returncode == 0:
            try:
                report_data = json.loads(r_report.stdout.strip())
            except json.JSONDecodeError:
                pass
                
        # Generate markdown audit report
        markdown_report = self._generate_markdown_report(report_data, r.stdout, r.stderr)
        
        return {
            'status': 'success',
            'exit_code': r.returncode,
            'report': report_data,
            'markdown': markdown_report
        }

    def _generate_markdown_report(self, data, stdout, stderr):
        score = data.get('globalScore', 0)
        status = data.get('status', 'CRITICAL')
        
        status_emoji = '🟢' if status == 'NOMINAL' else ('🟡' if status == 'WARNING' else '🔴')
        
        lines = [
            f"# {status_emoji} SafetyMind Responsive Audit Report",
            f"**Global Status:** {status} | **Branding Score:** {score}/100",
            f"**Execution Timestamp:** {data.get('timestamp', 'N/A')}",
            f"**Target URL:** {data.get('targetUrl', 'N/A')}",
            "",
            "## 📊 Viewport Audit Results",
            "",
            "| Page | Viewport | Width | Height | H-Scroll | Status |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |"
        ]
        
        failures = []
        for res in data.get('results', []):
            icon = '✅' if res['status'] == 'PASS' else '❌'
            hscroll = 'Yes ⚠️' if res['hasHScroll'] else 'No'
            lines.append(f"| {res['page']} | {res['viewport'].capitalize()} | {res['width']}px | {res['height']}px | {hscroll} | {icon} {res['status']} |")
            if res['status'] == 'FAIL':
                failures.append(res)
                
        lines.append("")
        
        if failures:
            lines.append("## 🚨 Responsiveness Failures")
            for f in failures:
                lines.append(f"### ❌ {f['page']} @ {f['viewport'].capitalize()} ({f['width']}x{f['height']}px)")
                lines.append("Overlapping or out-of-bounds elements:")
                for el in f.get('outOfBounds', []):
                    lines.append(f"- `{el}`")
                lines.append("")
        else:
            lines.append("## 🟢 Layout Compliance")
            lines.append("All layout views are fully responsive with no horizontal scrolling or overlapping container issues.")
            lines.append("")
            
        lines.append("---")
        lines.append("*Audit carried out by DAS Responsive Agent matrix.*")
        
        return '\n'.join(lines)

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'discover'
    result = asyncio.run(DasResponsiveAgent().run({'mode': mode}))
    if result.get('status') == 'success':
        print(result['markdown'])
    else:
        print(f"Error: {result.get('message')}")
