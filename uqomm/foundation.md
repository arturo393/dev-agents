# UQOMM Foundation

Contenido específico del proyecto UQOMM. Para fundamentos de software, hardware y firmware, ver:
- `shared/software-foundation.md`
- `shared/hardware-foundation.md`
- `shared/firmware-foundation.md`

---

## Brand & Design Tokens

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

---

## UI Principles

- **Keyboard-first**: Todo operable sin mouse
- **Botones**: Máximo 3 variantes — primary (naranja), secondary (outline), destructive (rojo)
- **Log panel**: Siempre presente, buffer circular 1000 líneas
- **Empty state**: [icono] + descripción + causa + acción
- **WCAG 2.2 AAA**: contraste >= 7:1 normal, >= 4.5:1 grande, touch target >= 44px
- **Viewports**: HD (1280x720) y FHD (1920x1080)

---

## SOLID en UQOMM

| Principio | Regla |
|-----------|-------|
| **S** — Single Responsibility | Cada módulo hace una cosa. `frame_codec.py` solo codifica/decodifica. `serial_thread.py` solo maneja el puerto. |
| **O** — Open/Closed | Nuevos dispositivos = nueva clase, no modificar el polling loop. |
| **L** — Liskov | Controladores de instrumentos intercambiables (simulación ↔ real). |
| **I** — Interface Segregation | Preferir interfaces chicas: `Switchable`, `Measurable`, `Configurable`. No `Instrument` gigante. |
| **D** — Dependency Inversion | El código de negocio no conoce el hardware. Inyectar dependencias. |

---

## Products Map

| Producto | Stack | Testing |
|----------|-------|---------|
| **DRS** (sw-drs-control, sw-drsmonitoring, sw-DrsValidator) | Python, C++, Docker | pytest, Hypothesis |
| **VLAD** (fw-vlad, sw-diagnosticoremoto, sw-vlad-certificador) | C STM32, Python | pytest, Catch2 |
| **Leaky Feeder** (fw-gateway2Lora, fw-headend, fw-ulad, fw-lnavhf) | C STM32, C++ | Catch2, On-target UART |
| **SmartLocate / Sniffer / Noise Analyzer** | C STM32, Python, React | pytest, Jest |

| Shared | Stack | Rol |
|--------|-------|-----|
| sw-vlad-dac-tools | C++17, FTXUI, Qt6 | Herramientas DAC VLAD |
| sw-testbench | Python | Test bench automation |
| sw-jiraanalysis / uqomm-updater / ops-tooling | Python, Shell | Métricas, OTA, ops |

---

## Post-Install Verification

Ejecutar después de cada deploy contra servidor de pruebas `192.168.60.141`:

```bash
pytest -v --tb=line                     # Unit tests
npx playwright test --project=chromium-light-fhd  # UI tests
```

---

## Documentación Mínima por Proyecto

Cada proyecto debe tener:
- `docs/` con:
  - Pipeline principal documentado
  - Security standards contextuales
  - Testing guidelines
- ADR para decisiones arquitectónicas no triviales (>30 min de discusión)

**NO crear:**
- README.md repetitivo
- Documentación generada que nadie lee
- arc42 completo para un script de 200 líneas
