---
name: SafetyMind Universal Web UI Standard (Guardian Prime)
description: The unified UI/UX source of truth for all SafetyMind web applications - V4.0
---

# SafetyMind Universal Web UI Standard - Guardian Prime V4.0

Estándar universal de calidad UI/UX para todo el ecosistema web de SafetyMind.

## 🎯 Propósito

Este documento establece los criterios obligatorios para garantizar la concordancia, el layout profesional y la integridad visual en cualquier interfaz de SafetyMind:
- **SafetyMind Universal Design** (Estética industrial moderna)
- **WCAG AAA** (Accesibilidad máxima)
- **Sentinel Compliance** (Cero hardcode, datos reales)
- **Industrial Standards** (Optimizado para entornos de planta)

## 🏗️ Aplicaciones Cubiertas

Este estándar es la referencia única para:
1. `infrastructure_monitoring/` - Monitoreo industrial
2. `jira-automation/` - Automatización y reportes
3. `puente_grua/` - Control de grúas industriales
4. `diagnostic-automation-suite/` - Diagnóstico con IA

## 🎨 Design Tokens (Property of SafetyMind)

| Token | Dark Value | Light Value | WCAG AAA Ratio |
|-------|-------------|--------------|-----------------|
| `--bg-primary` | `#000000` | `#ffffff` | 21:1 (Pass) |
| `--bg-secondary` | `#0a0a0a` | `#f5f5f5` | 15:1 (Pass) |
| `--text-primary` | `#ffffff` | `#000000` | 21:1 (Pass) |
| `--text-secondary` | `#888888` | `#666666` | 7:1 (Pass) |
| `--accent` | `#ffed01` | `#ffed01` | 15:1 on dark (Pass) |
| `--status-green` | `#00ff88` | `#00cc66` | 10:1 (Pass) |
| `--status-red` | `#ff3b3b` | `#ff0000` | 8:1 (Pass) |

## 🖋️ Typography (SafetyMind Identity)

- **Display & Titles**: `Chakra Petch` (Industrial/Technical vibe)
- **Body & Interface**: `Outfit` or `Inter` (Readability)
- **Technical Data**: `JetBrains Mono` (Zero-ambiguity)

## 🏗️ Arquitectura Frontend Estándar

### Atomic Design (Lite)
```
atoms/        → Botones, inputs, labels
molecules/    → Search bars, form fields
organisms/    → Headers, Tables, Video Feeds
templates/   → Layouts de Dashboard
```

### Hooks First
- Toda lógica de negocio en Custom Hooks
- `useTelemetry`, `useAuth`, `useAlerts`

### State Management
- **TanStack Query**: Obligatorio para telemetría (caché automático)
- **Zustand**: Estado global ligero (UI preferences)

## ♿ WCAG AAA Strict Checklist

### Contraste y Visibilidad
✅ **Contraste**: Mínimo 7:1 para todo texto
✅ **Focus Visible**: 3px solid #ffed01 con 2px offset
✅ **Tipografía**: JetBrains Mono para datos numéricos (evita layout shift)

### ARIA Compliance
✅ **ARIA**: Todo elemento interactivo tiene `aria-label`, `aria-describedby`
✅ **Live Regions**: `aria-live="polite"` para telemetría
✅ **Empty States**: Nunca mostrar "0" para datos nulos
✅ **Roles Semánticos**: `role="region"`, `role="status"`

## 🏭 Industrial Field Standards

### Operación en Planta
✅ **Glove-Touch**: Mínimo 48x48px touch targets
✅ **High-Glare**: Paletas de alto contraste para luz solar
✅ **Offline Resilience**: Mostrar último estado conocido (50% opacidad + icono)
✅ **Vibration Tolerance**: Posicionamiento fijo, sin interacciones hover-dependientes

### Telemetría Industrial
✅ **Precisión**: Fuentes Mono para datos (tabular-nums)
✅ **Unidades**: SI/Métrico por defecto, siempre visibles
✅ **Timeouts**: Sesiones robustas >5s latencia = alerta crítica

## 🔍 Sentinel Compliance (V8.2)

### Cero Hardcode
✅ **Identidad**: No nombres de personas, no marcas falsas, no datos predichos
✅ **Branding**: No inventar nombres de productos o motores de IA
✅ **Empty States**: "Esperando Selección de Nodo" en lugar de "0" o datos mock

### Integridad Semántica
✅ **Real Data Only**: Componentes muestran valores de API reales
✅ **Industrial Timeouts**: Manejo robusto de sesiones en terminales

## 🚨 Priority Matrix

| Level | Name | Criteria | Action |
|-------|------|-----------|---------|
| **P1** | CRITICAL | Telemetría block, latency >5s, WCAG AAA fail, API key leak | Stop deploy |
| **P2** | WARNING | Color drift, missing aria-label, targets <44px, no offline mode | Fix in sprint |
| **P3** | MINOR | Typos, 1px→4px adjustments, code optimizations | Backlog |

## 🔧 Protocolo de Auditoría

### Self-Correction (Vision)
1. Comparar capturas de pantalla contra tokens de diseño
2. Verificar que no hay "ruido" (datos inventados, marcas falsas)
3. Revisar que los factores de riesgo tengan fotos de evidencia reales

### Memory Loop
1. Leer el último `safety-audit-report.md`
2. Verificar que errores anteriores no han reaparecido
3. Validar que el diseño cumple con el SafetyMind Universal Web Standard

### Human Escalation
Si un diseño es ambiguo (ej: "este amarillo parece naranja"), solicitar confirmación al USER.

## 📊 Code Quality Standards

### React/Next.js
✅ **TypeScript Strict**: No `any`, full typing for sensors/data
✅ **Component Atomic**: atoms → molecules → organisms → templates
✅ **Hooks First**: All business logic in custom hooks
✅ **Performance**: Suspense, Skeletons, Lazy loading

### CSS/Tailwind
✅ **Tailwind V4**: Uso de `@theme` y variables CSS
✅ **Glassmorphism Lite**: `backdrop-filter: blur(8px)` con 10% opacidad
✅ **Bento Grid**: `grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));`

## 🚀 Uso del Agente

### Invocación
Este agente debe ser invocado por cualquier proyecto SafetyMind:
```bash
# En cualquier proyecto
agent-safetymind-ui-check --project=infrastructure_monitoring
agent-safetymind-ui-check --project=jira-automation
agent-safetymind-ui-check --project=puente_grua
agent-safetymind-ui-check --project=diagnostic-automation-suite
```

### Auditoría Pre-Deploy
Antes de cualquier `rsync` o `deploy`:
1. Ejecutar agente de auditoría UI
2. Verificar cumplimiento del SafetyMind Universal Web Standard
3. Validar WCAG AAA
4. Solo entonces proceder con deploy

---

## 📋 Template de Reporte

```markdown
# SafetyMind UI Audit Report - [FECHA]

## Resumen Ejecutivo
- **Proyecto**: [Nombre]
- **Estado**: ✅ PASS / ❌ FAIL
- **Score**: X/100

## Hallazgos P1 (Critical)
[Lista de bloqueos]

## Hallazgos P2 (Warning)
[Lista de advertencias]

## Hallazgos P3 (Minor)
[Lista de menores]

## Compliance
- SafetyMind Universal Web Standard: ✅/❌
- WCAG AAA: ✅/❌
- Sentinel: ✅/❌
- Industrial Standards: ✅/❌
```

---

© 2026 SafetyMind Elite Engineering. 🏮✨🛡️
