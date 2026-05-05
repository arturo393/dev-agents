# 🛠️ Skill: Audit-UI-Industrial

Esta habilidad permite al Agente Guardian realizar una auditoría técnica profunda sobre un repositorio React/Next.js de SafetyMind.

## 📋 Checklist Técnico de Ejecución (Context-Aware)

### 1. Verificación de Resiliencia y Hardware
- [ ] **Touch Targets:** ¿Los botones son de min 48px? (Verificar en CSS/inspect).
- [ ] **Offline Check:** ¿Existe un `service-worker.js` o configuración de `PWA`?
- [ ] **Contrast Stress:** ¿Los colores de las gráficas tienen suficiente contraste para exteriores?

### 2. Verificación de Estética (Visual Audit)
- [ ] **Background Check:** Ejecutar inspección o revisar CSS buscando `background-color`. Debe ser `#000000`.
- [ ] **Token Check:** Buscar colores hardcoded. Reemplazar cualquier `#333`, `#222`, `#fff` genérico por los tokens de SM.
- [ ] **Geometry:** Verificar que los containers tienen `border-radius: 12px`.
- [ ] **Glow/Shadows:** Verificar presencia de `box-shadow` sutiles o `drop-shadow` en indicadores de estado.

### 2. Accesibilidad (WCAG AAA)
- [ ] **Contrast Ratio:** Verificar que los indicadores de estado (ej: Alerta Roja sobre fondo Negro) superen el ratio 7:1.
- [ ] **Focus Visible:** Verificar que `globals.css` tenga una regla global para que el `focus-ring` sea `#ffed01`.
- [ ] **Interactive Elements:** Escanear componentes buscando botones o enlaces sin `aria-label`.

### 3. Buenas Prácticas React
- [ ] **Props Typing:** Verificar que no haya `prop-types` obsoletos, usar TypeScript estrictamente.
- [ ] **State Management:** Verificar que la carga de datos tenga estados de `loading`.
- [ ] **Component Structure:** Los componentes de UI deben estar en `src/components/ui`.

## 🛠️ Comandos de Auditoría Automatizados

El agente debe ejecutar estos comandos para obtener evidencia objetiva:

1.  **Scan de Colores No-Estándar:**
    `grep -rE "#([0-9a-fA-F]{3,6})" . --exclude-dir=node_modules | grep -vE "(ffed01|000000|0a0a0a|1e2532|ff3b3b)"`
2.  **Scan de Touch-Targets (Tailwind):**
    `grep -rE "h-[1-9]|w-[1-9]" src/ | grep -vE "(h-12|w-12|h-14|w-14|h-16|w-16)"` (Buscar elementos < 48px/h-12).
3.  **Auditoría de Any & Types:**
    `grep -r ": any" src/ --include="*.ts" --include="*.tsx" | wc -l`
4.  **Chequeo de Accesibilidad (Aria Missing):**
    `grep -rE "<(button|a|input)[^>]*>" src/ | grep -v "aria-label"`

---

## 📊 Plantilla de Reporte: SafetyMind Audit Report V4.1

# 🛡️ SafetyMind Audit Report: [Nombre del Proyecto]
**Estado Global:** [🔴 CRITICAL | 🟡 WARNING | 🟢 NOMINAL]

### 🚨 Hallazgos P1 (CRITICAL) - Acción Inmediata
- [Error] -> [Impacto en Planta] -> [Fix]

### ⚠️ Hallazgos P2 (WARNING) - Calidad de Marca
- [Error] -> [Impacto Visual/A11y] -> [Fix]

### ⚛️ Calidad de Código & Resiliencia
- [Análisis de TypeScript, Performance y Modo Offline]


### 🔗 Integración Jira (Auto-Ticket Format)
Si el estado es **CRITICAL**, adjuntar este bloque al final del reporte para procesarlo con `jira-automation`:

```json
{
  "issue_type": "Bug",
  "priority": "Highest",
  "summary": "[GUARD] Critical A11y/Industrial Failure in [Component]",
  "description": "Rule Violated: [Rule Name]. Impact: [Critical Operation Risk]. Suggested Fix: [Code Block]",
  "labels": ["SafetyMind-Guardian", "Industrial-Safety"]
}
```

---
*Audit carried out by Guardian Prime Logic Matrix.*

---
© 2026 SafetyMind Audit Suite. 🛡️
