---
description: Auditoría de Diseño y Accesibilidad SafetyMind (WCAG AAA)
---

Este workflow actúa como el "Agente de Calidad" para asegurar que la interfaz cumple con los estándares industriales de SafetyMind.

### 1. Verificación de Identidad Visual
El agente debe verificar que los colores primarios y secundarios coinciden con los tokens de marca:
- **Navy**: `oklch(0.25 0.04 261)` (#1e2532)
- **Yellow**: `oklch(0.92 0.20 95)` (#ffed01)

### 2. Auditoría de Accesibilidad (WCAG AAA)
- **Contraste**: El texto sobre fondo Navy debe ser Blanco Puro o Amarillo (#ffed01) con un ratio > 7:1.
- **Roles ARIA**: Todos los elementos interactivos (Select, Tabs, Botones) deben tener etiquetas descriptivas.
- **Navegación por Teclado**: Asegurar que el `ring` de enfoque use el Amarillo de SafetyMind para visibilidad máxima.

### 3. Pasos de Ejecución
1. Revisar `src/app/globals.css` para validar variables de tema.
2. Escanear `src/app/page.tsx` buscando elementos sin `aria-label`.
3. Validar que no hay colores "hardcoded" fuera del sistema de Tailwind.

// turbo
4. Ejecutar validación de compilación: `npm run build`
