# UQOMM Shared Foundation

Esta fundación se inyecta automáticamente en todos los agentes UQOMM vía `sync-opencode-agents.ps1`.

---

## UQOMM Brand & Design Tokens

| Token | Hex | Uso |
|-------|-----|-----|
| Negro | `#10182B` | Fondos, paneles dark |
| Naranja | `#FF5000` | Acciones primarias, branding. **Nunca** para estados |
| Blanco | `#FFFFFF` | Texto sobre fondos oscuros |
| Gris | `#575756` | Textos secundarios |
| Verde OK | `#2FAF58` | Estado healthy |
| Amarillo | `#FFB020` | Advertencia |
| Rojo | `#E53935` | Error/crítico |

**Gradiente oficial:** `linear-gradient(45deg, #10182B, #FF5000)`

**Principios de UI universal:**
- Keyboard-first. Todo operable sin mouse.
- Máximo 3 variantes de botón: primary (naranja), secondary (outline), destructive (rojo)
- Log panel siempre presente, buffer circular 1000 líneas
- Empty state: [icono] + descripción + causa + acción
- WCAG 2.2 AAA: contraste >= 7:1 normal, >= 4.5:1 grande, touch target >= 44px
- Viewports: HD (1280x720) y FHD (1920x1080)

---

## SOLID aplicado a UQOMM

| Principio | Regla |
|-----------|-------|
| **S** — Single Responsibility | Cada módulo hace una cosa. `frame_codec.py` solo codifica/decodifica. `serial_thread.py` solo maneja el puerto. |
| **O** — Open/Closed | Nuevos dispositivos = nueva clase, no modificar el polling loop. |
| **L** — Liskov | Los controladores de instrumentos deben ser intercambiables (simulación ↔ real). |
| **I** — Interface Segregation | Preferir interfaces chicas y específicas. No `Instrument` gigante, sino `Switchable`, `Measurable`, `Configurable`. |
| **D** — Dependency Inversion | El código de negocio no conoce el hardware. Inyectar dependencias. |

---

## Cognitive-Doc-Design (big-cognitive)

Aplica a toda documentación, PRs, y comentarios:

| Patrón | Regla |
|--------|-------|
| Lead with answer | Decisión o acción primero, contexto después |
| Progressive disclosure | Happy path → detalles → edge cases |
| Chunking | Secciones pequeñas, listas cortas |
| Signposting | Headings, labels, callouts |
| Recognition over recall | Tablas, checklists, templates |
| Review empathy | Diseñar para que el revisor verifique sin reconstruir |

Estructura por defecto: `Quick path` → `Details` (tabla) → `Checklist` → `Next step`.

---

## Antifragilidad en Hardware

Aplica a todo proyecto que toque instrumentos físicos:

1. **Simulation Mode Fallback**: si el driver no existe (CI sin hardware), entrar en Modo Simulación. Nunca abortar.
2. **Tests tolerantes**: `response["status"] in {"ok", "degraded"}`. Degraded es esperable con HW real.
3. **LD_PRELOAD**: SDKs compilados contra librerías deprecadas necesitan inyectar la compatible.
4. **Hostname offline-first**: formato `<client>-<role>-<location>-<mac-last4>`. Prohibido IDs secuenciales.

---

## Testing (XDD) — Cómo elegir

| Contexto | Metodología |
|----------|-------------|
| Definir qué construir con el negocio | **ATDD** — Criterios de aceptación medibles |
| Documentar comportamiento observable | **BDD** — Given-When-Then |
| Diseñar función correcta por construcción | **TDD** — Red-Green-Refactor |
| Encontrar casos borde | **PBT** — Propiedades + fuzzing |
| Múltiples dispositivos/configuraciones | **DDT** — Tests parametrizados con datos externos |

**E2E**: solo cuando el flujo completo (HW → backend → UI) no se pueda cubrir con tests de integración. Preferir integración sobre E2E.

**Regla de oro:** Sin test no hay cambio en producción. Cada fix incluye su test.

---

## Post-Install Verification

Ejecutar después de cada deploy contra servidor de pruebas `192.168.60.141`:

```bash
pytest -v --tb=line                     # Unit tests
npx playwright test --project=chromium-light-fhd  # UI tests
```
