---
description: SafetyMind React Development Standard - Modern Industrial Frontend
---

# ⚛️ Estándar de Desarrollo React - SafetyMind V4.0

Este documento define las estrategias y buenas prácticas para el desarrollo de aplicaciones frontend dentro del ecosistema SafetyMind.

## 🏗️ Arquitectura de Software
Adoptamos una arquitectura orientada a la mantenibilidad y modularidad industrial.

*   **Atomic Design (Lite):**
    *   `atoms/`: Botones, inputs, labels puros.
    *   `molecules/`: Search bars, form fields.
    *   `organisms/`: Headers, Tables, Video Feeds.
    *   `templates/`: Layouts de Dashboard.
*   **Hooks-First:** Toda la lógica de negocio y telemetría debe residir en Custom Hooks (`useTelemetry`, `useAuth`, `useAlerts`).

## 💎 Estándares Técnicos Modernos

### 1. TypeScript Estricto
- Prohibido el uso de `any`.
- Uso de `Interface` para objetos de datos de sensores.
- Tipado exhaustivo de eventos y Props.

### 2. Tailwind CSS V4 Architecture
Utilizar el motor de Tailwind V4 para maximizar el rendimiento.
- Centralizar variables en `@theme`.
- Usar clases utilitarias para el 90% del diseño.
- Solo usar CSS puro para animaciones complejas de "Industrial Glow".

### 3. State Management & Data Fetching
- **TanStack Query (React Query):** Obligatorio para fetching de telemetría e integración con backend. Proporciona manejo de caché y estados de carga out-of-the-box.
- **Zustand:** Para estado global ligero (preferencias de UI, usuario actual).

## 🚀 Performance & Visibilidad
Un dashboard industrial no puede ser lento.
- **Code Splitting:** Lazy loading para secciones pesadas (analítica, mapas).
- **Z-Index Strategy:** Mantener un sistema coherente de capas (Modales: 50, Dashboard: 10, Background: 0).
- **Edge cases:** Siempre manejar el estado `Empty` y `Error`. Un "Monitor de Red" vacío debe explicar por qué está vacío.
- **Sentinel Compliance (V8.2):** Obligatorio cumplir con el Protocolo de Integridad Semántica: cero hardcoding de nombres, cero branding inventado y cero mensajes predictivos sin datos reales.

## 🧪 Calidad y Testing (Mandatorio)
- **BDD Acceptance:** Antes de implementar una vista, se deben validar los escenarios en `BDD_DAS.md`.
- **TDD Flow:** Escribir pruebas unitarias para Hooks personalizados y lógica de validación de formularios antes de la implementación.
- **Self-Audit:** Antes de enviar un PR, el desarrollador debe pasar el Agente `Guardian Prime` para validar UI y A11y.
- **SDD Integrity:** Cualquier cambio en el flujo de datos o arquitectura debe ser reflejado primero en el `SDD_DAS.md`.

---
© 2026 SafetyMind Dev Engineering. ⚙️⚛️
