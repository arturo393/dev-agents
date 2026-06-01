---
name: SafetyMind UI Audit
description: Full-spectrum UI audit for SafetyMind projects. Validates Guardian Prime compliance, dashboard standards, GUI principles, and runs Playwright-based visual/accessibility tests.
---

# SafetyMind UI Audit

Skill de auditoría UI/UX unificada para SafetyMind. Integra los estándares de `shared/ui-standards.md` con dash standards, principios GUI y revisión visual automatizada via Playwright.

## Use Case

Esta skill está diseñada para auditar aplicaciones industriales, dashboards de telemetría y entornos React/Next.js que deben cumplir con los estándares Guardian Prime de SafetyMind.

## Qué comprueba

- Accesibilidad WCAG / ARIA
- Contraste de color y tokens de diseño
- Touch targets y usabilidad móvil
- Estados de componentes: loading, empty, error, offline
- Dashboard rules: KPI cards, charts, tablas y status indicators
- Variables estáticas: colores no estándar, console.log, `any`, `prop-types`

## Cómo se usa

1. Asegúrate de tener instalado el proyecto que quieres auditar.
2. Ejecuta `npm install -D @playwright/test axe-core playwright` en el proyecto si no está instalado.
3. Ejecuta `npx playwright install chromium`.
4. Ejecuta:

```bash
AUDIT_URL=http://localhost:3000 node ./dev-agents/skills/ui-audit/scripts/ui-audit.mjs
```

También puedes pasar parámetros:

```bash
node ./dev-agents/skills/ui-audit/scripts/ui-audit.mjs --url http://localhost:3000 --output ./ui-audit-output
```

## Output

La auditoría genera:

- `ui-audit-output/ui-audit-report.json` con resultados estructurados
- `ui-audit-output/ui-audit-screenshot.png` con captura de pantalla completa

## SafetyMind Principles


### Industrial Clarity
- Todo elemento comunica su propósito sin ambigüedad
- Datos numéricos en `JetBrains Mono` con `font-variant-numeric: tabular-nums`
- Unidades SI siempre visibles junto al valor
- Sin decoración que no aporte información

### Data Integrity
- Nunca mostrar datos mock, placeholders o valores predichos
- Cero hardcoding de nombres, marcas o identificadores
- Estados vacíos descriptivos: "Esperando selección de nodo" en vez de "0" o "--"
- Timestamps con timezone explícito

### Zero Friction
- Glove-ready: touch targets >= 48x48px, sin hover-dependencia
- Offline resilience: último estado conocido con opacidad 50%
- High-glare ready: paletas de contraste máximo para luz solar directa
- Tiempo de carga máximo: 2s en LAN industrial, 5s en WAN

### Consistency
- Un solo sistema de design tokens en toda la aplicación
- Un solo breakpoint system
- Un solo spacing scale (4px base)
- Un solo border-radius (12px containers, 6px inputs, 4px badges)

## Dashboard Standards (Dash)

Son estándares específicos para pantallas de monitoreo, telemetría y control industrial.

### KPI Cards
- Cada KPI debe mostrar: valor, unidad, label, tendencia (flecha up/down/flat)
- Estados: loading (skeleton), ok, warning, critical, stale (offline)
- Thresholds visibles: valor actual vs límite (ej: "78% / 85% max")
- Sparkline opcional, no obligatorio
- Ancho mínimo: 200px, máximo: 1fr

### Charts (Time-Series, Gauges, Bars)
- Eje Y siempre con label de unidad
- Time-series: zoomable, con tooltip preciso (valor + timestamp)
- Gauges: arco de 180°, warning zone en amarillo, critical zone en rojo
- Barras: colores según estado (verde ok, amarillo warning, rojo critical)
- States: loading (skeleton), no-data (línea punteada + label), error (icono + retry)
- Offline: datos históricos se muestran sólidos, gap sin datos se marca con línea punteada

### Data Tables
- Primera columna fija (sticky) cuando hay scroll horizontal
- Sorting visual: flecha en header, columna activa resaltada
- Row hover: background change sutil (`--bg-secondary`)
- Estados de fila: row completa con borde izquierdo de color (verde/amarillo/rojo)
- Paginación o infinite scroll con contador ("Mostrando 1-20 de 156")
- Empty state: "No hay datos para los filtros seleccionados" con acción de limpiar filtros

### Status Indicators
- Formato: icono + label de texto (nunca solo color)
- Colores: `#00ff88` ok, `#ffed01` warning, `#ff3b3b` critical, `#888888` offline
- Parpadeo solo en estado crítico no acknowledge, máximo 2Hz
- Tooltip con detalle: "Sensor 3 - Sin lectura desde 2026-05-19 14:32:01 UTC"

### Navigation & Layout
- Sidebar colapsable con iconos + labels
- Breadcrumbs en páginas internas
- Header: nombre de proyecto + estado global + usuario
- Responsive: sidebar se colapsa a iconos en <1024px, menú hamburguesa en <768px

## GUI Standards

### Atomic Design Structure
```
atoms/         Botones, inputs, labels, badges, spinners
molecules/     Search bars, form fields, KPI cards, chart wrappers
organisms/     Data tables, dashboards headers, filter panels
templates/     Layouts de dashboard, login layout, admin layout
```

### Component States
Cada componente debe implementar:
- **loading**: skeleton o spinner (nunca blank screen)
- **empty**: mensaje descriptivo + acción sugerida
- **error**: mensaje + retry button
- **success**: confirmación visual
- **disabled**: opacidad reducida + cursor not-allowed
- **offline**: datos en opacidad 50% + indicador de stale

### Typography System
| Uso | Font | Weight | Size |
|-----|------|--------|------|
| Display | Chakra Petch | 700 | 2.25rem |
| Titles | Chakra Petch | 600 | 1.5rem |
| Section headers | Chakra Petch | 600 | 1.125rem |
| Body | Outfit / Inter | 400 | 0.875rem |
| Data (mono) | JetBrains Mono | 400 | 0.875rem |
| Small / Meta | Outfit / Inter | 400 | 0.75rem |

### Spacing Grid
- Base: 4px
- Scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64
- Padding contenedores: 24px
- Gap entre cards: 16px
- Gap entre elementos de formulario: 20px

### Design Tokens (from shared/ui-standards.md)
| Token | Dark | Light |
|-------|------|-------|
| `--bg-primary` | `#000000` | `#ffffff` |
| `--bg-secondary` | `#0a0a0a` | `#f5f5f5` |
| `--text-primary` | `#ffffff` | `#000000` |
| `--text-secondary` | `#888888` | `#666666` |
| `--accent` | `#ffed01` | `#ffed01` |
| `--status-green` | `#00ff88` | `#00cc66` |
| `--status-red` | `#ff3b3b` | `#ff0000` |

## Playwright Audit

### Setup
```bash
npx playwright install chromium
npm install -D @playwright/test axe-core playwright
```

### Audit Script
Crea `scripts/ui-audit.mjs` en el proyecto a auditar:

```javascript
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';

const URL = process.env.AUDIT_URL || 'http://localhost:3000';

async function runAudit() {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

  await page.goto(URL, { waitUntil: 'networkidle' });

  // 1. Accesibilidad (axe-core)
  const results = await new AxeBuilder({ page }).analyze();
  console.log('=== AXE VIOLATIONS ===');
  results.violations.forEach(v => {
    console.log(`[${v.impact}] ${v.id}: ${v.description}`);
    v.nodes.forEach(n => console.log(`  → ${n.target}`, n.failureSummary));
  });

  // 2. Touch targets >= 48px
  const smallTargets = await page.evaluate(() => {
    const elements = document.querySelectorAll(
      'button, a, input, [role="button"], [tabindex]:not([tabindex="-1"])'
    );
    return Array.from(elements)
      .filter(el => {
        const rect = el.getBoundingClientRect();
        return rect.width < 48 || rect.height < 48;
      })
      .map(el => ({
        tag: el.tagName,
        text: el.textContent?.trim().slice(0, 40),
        width: Math.round(el.getBoundingClientRect().width),
        height: Math.round(el.getBoundingClientRect().height),
      }));
  });
  console.log('=== SMALL TOUCH TARGETS (<48px) ===', smallTargets);

  // 3. Color contrast (elementos con texto vs fondo)
  const contrastIssues = await page.evaluate(() => {
    const results = [];
    const elements = document.querySelectorAll('*');
    elements.forEach(el => {
      const style = getComputedStyle(el);
      if (style.color && style.backgroundColor && style.color !== 'rgba(0, 0, 0, 0)') {
        const hex = c => {
          const v = Math.round(c * 255);
          return v.toString(16).padStart(2, '0');
        };
        results.push({
          tag: el.tagName,
          text: el.textContent?.trim().slice(0, 30),
          color: style.color,
          bg: style.backgroundColor,
        });
      }
    });
    return results.slice(0, 50);
  });
  console.log('=== COLOR ISSUES (first 50) ===', contrastIssues);

  // 4. Missing ARIA labels
  const missingAria = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('button:not([aria-label]):not([aria-labelledby])'))
      .filter(el => !el.textContent?.trim())
      .map(el => ({ tag: el.tagName, html: el.outerHTML.slice(0, 80) }));
  });
  console.log('=== BUTTONS WITHOUT ARIA-LABEL ===', missingAria);

  // 5. Screenshot
  await page.screenshot({ path: 'ui-audit-screenshot.png', fullPage: true });
  console.log('Screenshot saved: ui-audit-screenshot.png');

  await browser.close();
}

runAudit().catch(console.error);
```

### Run
```bash
AUDIT_URL=http://localhost:3000 node scripts/ui-audit.mjs
```

### Visual Regression (Opcional)
```bash
npx playwright test --update-snapshots  # primera vez
AUDIT_URL=http://localhost:3000 node scripts/ui-audit.mjs  # luego comparar
```

## Static Analysis Commands

```bash
# 1. Colores no-estándar (los que no son tokens SafetyMind)
grep -rE "#([0-9a-fA-F]{3,6})" . --exclude-dir=node_modules \
  | grep -vE "(ffed01|000000|0a0a0a|1e2532|ff3b3b|00ff88|888888|ffffff|f5f5f5|666666|00cc66|ff0000)"

# 2. Touch targets < 48px en Tailwind
grep -rE "h-[1-9]|w-[1-9]" src/ | grep -vE "(h-12|w-12|h-14|w-14|h-16|w-16)"

# 3. Tipos `any` en producción
grep -r ": any" src/ --include="*.ts" --include="*.tsx" | wc -l

# 4. Elementos interactivos sin aria-label
grep -rE "<(button|a|input)[^>]*>" src/ | grep -v "aria-label"

# 5. Prop-types legacy (deberían ser TypeScript)
grep -r "prop-types" src/ --include="*.js" --include="*.jsx"

# 6. Console.log en producción
grep -r "console\.log" src/ --include="*.ts" --include="*.tsx"

# 7. Hardcoded text sin i18n (opcional)
grep -rE '>[A-Z][a-z]+ [A-Z][a-z]+<' src/components/
```

## Compliance Tiers

| Tier | Impacto | Acción | Ejemplos |
|------|---------|--------|----------|
| **P0** | Seguridad | Detener deploy inmediato | Exposición de datos, API keys en UI, auth bypass |
| **P1** | Bloqueo | No deploy sin fix | WCAG AAA fail, color drift, touch targets < 44px, sin offline mode |
| **P2** | Calidad | Fix en sprint | Missing aria-label, estados vacíos sin mensaje, tipografía incorrecta |
| **P3** | Cosmético | Backlog | Typos, padding inconsistente, animaciones sin GPU |

## Audit Flow

```
1. STATIC → grep-based analysis (código fuente)
2. PLAYWRIGHT → runtime checks on live URL (a11y, contrast, touch targets, screenshot)
3. REPORT → consolidated output con P0/P1/P2/P3 findings
```

## Report Template

```markdown
# SafetyMind UI Audit Report

**Proyecto:** [Nombre]
**URL auditada:** [URL]
**Fecha:** [2026-05-19]
**Auditor:** SafetyMind UI Audit Skill
**Estado Global:** [PASS | WARNING | CRITICAL]

## Resumen
| Dimensión | Score | Target |
|-----------|-------|--------|
| Accesibilidad (axe) | X/0 violations | 0 |
| Touch Targets | X elementos <48px | 0 |
| Tokens | X colores no-estándar | 0 |
| Tipos `any` | X | 0 |
| ARIA missing | X | 0 |

## P0 - Safety Critical
- [File:line] → Descripción → Fix

## P1 - Blocking
- [File:line] → Descripción → Fix

## P2 - Warning
- [File:line] → Descripción → Fix

## P3 - Minor
- [File:line] → Descripción

## Evidence
- Screenshot: `ui-audit-screenshot.png`
- Axe violations: N violaciones de severidad [impact]
```

## References
- `shared/ui-standards.md` — Design tokens, WCAG AAA checklist, priority matrix
- `shared/react-standard.md` — React architecture, hooks, state management
