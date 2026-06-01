import fs from 'fs/promises';
import path from 'path';
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';

const args = process.argv.slice(2);
const getArg = (name, fallback) => {
  const index = args.findIndex(arg => arg === name);
  if (index >= 0 && index + 1 < args.length) return args[index + 1];
  return fallback;
};

const url = process.env.AUDIT_URL || getArg('--url', 'http://localhost:3000');
const outputDir = process.env.AUDIT_OUTPUT || getArg('--output', 'ui-audit-output');
const screenshotPath = path.join(outputDir, 'ui-audit-screenshot.png');
const reportPath = path.join(outputDir, 'ui-audit-report.json');

async function ensureOutputDir() {
  await fs.mkdir(outputDir, { recursive: true });
}

function serializeResult(result) {
  return JSON.stringify(result, null, 2);
}

async function runAudit() {
  await ensureOutputDir();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

  await page.goto(url, { waitUntil: 'networkidle' });

  // 1. Accessibility (axe-core)
  const axeResults = await new AxeBuilder({ page }).analyze();

  // 2. Touch targets >= 48px
  const smallTargets = await page.evaluate(() => {
    const elements = document.querySelectorAll(
      'button, a, input, [role="button"], [tabindex]:not([tabindex="-1"])'
    );
    return Array.from(elements)
      .map(el => {
        const rect = el.getBoundingClientRect();
        return {
          tag: el.tagName,
          text: el.textContent?.trim().slice(0, 40),
          width: Math.round(rect.width),
          height: Math.round(rect.height),
          selector: el.id ? `#${el.id}` : el.className ? `.${Array.from(el.classList).join('.')}` : el.tagName,
        };
      })
      .filter(el => el.width < 48 || el.height < 48);
  });

  // 3. Missing ARIA labels
  const missingAria = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('button:not([aria-label]):not([aria-labelledby]), a:not([aria-label]):not([aria-labelledby])'))
      .filter(el => !el.textContent?.trim())
      .map(el => ({ tag: el.tagName, html: el.outerHTML.slice(0, 100) }));
  });

  // 4. Color contrast snapshot
  const contrastSamples = await page.evaluate(() => {
    const getColor = (value) => value;
    const samples = [];
    const elements = Array.from(document.querySelectorAll('*')).slice(0, 200);
    elements.forEach(el => {
      const style = getComputedStyle(el);
      if (!style || !style.color || !style.backgroundColor) return;
      if (style.color === 'rgba(0, 0, 0, 0)') return;
      samples.push({
        tag: el.tagName,
        text: el.textContent?.trim().slice(0, 30),
        color: getColor(style.color),
        background: getColor(style.backgroundColor),
      });
    });
    return samples;
  });

  await page.screenshot({ path: screenshotPath, fullPage: true });
  await browser.close();

  const report = {
    auditUrl: url,
    timestamp: new Date().toISOString(),
    axe: {
      violations: axeResults.violations,
      incomplete: axeResults.incomplete,
      passes: axeResults.passes,
    },
    smallTouchTargets: smallTargets,
    missingAria: missingAria,
    contrastSamples: contrastSamples,
    screenshot: screenshotPath,
  };

  await fs.writeFile(reportPath, serializeResult(report), 'utf8');
  console.log('UI audit complete');
  console.log(`Report saved: ${reportPath}`);
  console.log(`Screenshot saved: ${screenshotPath}`);
}

runAudit().catch(error => {
  console.error('Audit failed:', error);
  process.exit(1);
});
