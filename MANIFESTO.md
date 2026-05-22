# 🛡️ SafetyMind Manifesto: Operational Chain First (V4.1)

## 🎯 El "Para Qué" (Misión Crítica)
Este sistema no existe para monitorear servidores; existe para garantizar la **Seguridad del Cliente**. 
La única métrica que importa es la integridad de la **Cadena Operativa**:
`Cámara (Origen) ➔ Edge AI (Procesamiento) ➔ Telegram (Alerta)`.

Si el cliente no recibe la alerta, el sistema ha fallado, sin importar si el CPU está al 1%.

---

## 💎 Estándares de Calidad "Guardian Prime"

### 1. Estética Industrial Premium
*   **Negro Puro (#000000)**: Fondo obligatorio para máximo contraste.
*   **Amarillo SafetyMind (#ffed01)**: Color de acción y marca.
*   **Tipografía**: `Outfit` para encabezados (Industrial Moderno), `JetBrains Mono` para datos de telemetría.
*   **Efecto WOW**: Sombras sutiles, micro-animaciones (Framer Motion), y layouts limpios (Bento Grid).

### 2. Arquitectura de Software
*   **React 19 / Next.js 16**: Uso de Server Components donde sea posible.
*   **Estado**: TanStack Query (Telemetría) y Zustand (Preferencias Globales).
*   **Zero Tolerance**: Prohibido el uso de `any`. Tipado estricto para `Project` y `MetricData`.
*   **Atomic Design**: Estructura rígida en `atoms`, `molecules`, `organisms`.

### 3. Principios de Interfaz (UX)
*   **Visibilidad de Fallo**: El fallo debe ser "escandaloso". Si la cadena se rompe, la UI debe mostrarlo en < 1 segundo.
*   **Multi-Tenancy**: Aislamiento total entre clientes/proyectos. El usuario siempre debe saber qué "Misión" está visualizando.
*   **Stale State**: Si los datos tienen > 5 minutos de antigüedad, la UI debe mostrar opacidad y advertencia de "Datos no frescos".

---

## 🚫 Prohibiciones Estrictas (Audit Rule)
*   No usar IPs legacy (`34.x.x.x`). Solo IP Maestra: `192.168.1.149`.
*   No instalar servicios directamente en el OS. **Todo** es Docker.
*   No usar `localStorage` para datos críticos de telemetría (usar caché de React Query).

© 2026 SafetyMind Elite Engineering. 🏮✨🛡️
