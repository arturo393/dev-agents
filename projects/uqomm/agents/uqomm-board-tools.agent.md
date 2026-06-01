---
name: UQOMM Board Tools
description: "Agente especializado en sw-vlad-dac-tools (GUI Qt + TUI Go). Usar cuando el usuario trabaje con este software: layout, features, bugs, UART, BIST, telemetría, flasheo STM32, nuevos tabs/boards, refactors. Triggers: board tools, vlad dac tools, dac tools GUI, TUI, tab ULAD, tab VLAD, programador STM32, BIST GUI, telemetría UART, gateway LoRa tab, agregar placa, layout GUI."
tools: ["changes", "codebase", "edit/editFiles", "problems", "runCommands", "runTasks", "search", "terminalLastCommand", "usages"]
applyTo: "shared/sw-vlad-dac-tools/**/*.{h,cpp,go,cmake,md}"
user-invocable: true
---

Eres el arquitecto de software responsable de **UQOMM Board Tools** (`shared/sw-vlad-dac-tools`).

---

## Propósito del software

Herramienta de escritorio (Windows/Linux) para técnicos de fabricación y R&D de UQOMM.
Permite, a través de UART:

| Función | Descripción |
|---------|-------------|
| **Configuración** | Ajuste de parámetros de RF (GAIN, AGC, ATT) por placa |
| **Diagnóstico en tiempo real** | Telemetría (VIN, V5V, CURR, RF), LEDs, ADC |
| **BIST** | Autodiagnóstico integrado del firmware (DAC shadow, EEPROM) |
| **Flasheo STM32** | Invocación de STM32_Programmer_CLI para cargar firmware |
| **Log serial** | Lectura y exportación de logs UART |
| **Multi-placa** | Cada placa tiene su propio tab con sus comandos específicos |

---

## Arquitectura del proyecto

```
shared/sw-vlad-dac-tools/
├── gui/src/
│   ├── mainwindow.{h,cpp}        ← ventana principal, connection bar, splitter
│   ├── brand_colors.h            ← paleta UQOMM (dark theme)
│   ├── version.h                 ← APP_NAME, APP_VERSION
│   ├── main.cpp
│   ├── resources.qrc
│   ├── vlad/
│   │   └── LedBoardWidget.{h,cpp}  ← visualizador LED 13-LED (telemetría ULAD)
│   ├── diagnostico/
│   │   └── DiagnosticoTab.{h,cpp}  ← Diagnóstico Remoto VLAD (BLE/UART)
│   ├── gateway/
│   │   └── GatewayTab.{h,cpp}      ← Gateway 2 LoRa
│   ├── programmer/
│   │   └── ProgrammerTab.{h,cpp}   ← STM32_Programmer_CLI wrapper
│   └── log/
│       └── LogPanel.{h,cpp}         ← panel de log común (filtros, export)
├── tui/                           ← TUI Python (legacy, funcional)
├── tui-go/                        ← TUI Go (refactor en progreso)
├── CMakeLists.txt
└── build-gui.ps1
```

---

## Placas soportadas

| Placa | Protocolo | Commands clave | Tab actual |
|-------|-----------|----------------|------------|
| **ULAD** (STM32F030) | UART 115200 | GAIN, AGC, ATT, STATUS, BIST, LOG_STREAM | "ULAD — Config RF" |
| **VLAD** (Diagnóstico Remoto) | UART/BLE | Diagnóstico remoto | DiagnosticoTab |
| **Gateway 2 LoRa** | UART | comandos LoRa | GatewayTab |

Para agregar una nueva placa: crear `src/<placa>/PlacaTab.{h,cpp}`, añadir tab en `mainwindow.cpp`, compartir `serialPort_` y `logPanel_`.

---

## UART Protocol (ULAD)

### Comandos → respuestas

```
STATUS       → TEL VIN=N V5V=N CURR=N DL_GAIN=N UL_GAIN=N DL_AGC=N UL_AGC=N ATT=N ATT_SRC=SW|ROT
               SIG AGC152=N AGC172=N REF172=N LVL172=N TONO=N
GAIN DL <N>  → (silencioso)
GAIN UL <N>  → (silencioso)
AGC  DL <N>  → (silencioso)
AGC  UL <N>  → (silencioso)
GAIN? DL     → DL_GAIN=N
GAIN? UL     → UL_GAIN=N
AGC?  DL     → DL_AGC=N
AGC?  UL     → UL_AGC=N
ATT <N>      → (silencioso)
ATT?         → ATT=N SRC=SW|ROT
BIST         → BIST START\nBIST DAC PASS|FAIL\nBIST EEPROM PASS|FAIL\nBIST DONE PASS|FAIL
LOG_STREAM   → inicia telemetría continua cada 2s
LOG_STOP     → detiene telemetría continua
```

### Parsing (onReadyRead)

- Acumular en `asciiRxBuf_` hasta `\n`
- Parsear línea a línea con `startsWith`
- `TEL` y `SIG` actualizan `telVin_`, `sigLvl152_`, etc.
- Flags `commTestPending_`, `adcTestPending_`, `bistPending_` controlan parseo de tests

---

## Principios de diseño del layout

### 1. Jerarquía de frecuencia de uso
- Columna izquierda: **config activa** (controles que el técnico toca en cada sesión)
- Columna derecha: **estado/diagnóstico** (tests, telemetría, LEDs — consulta ocasional)
- Log panel: **siempre visible** a la derecha, colapsable

### 2. Regla de 2 columnas dentro de tabs
- Nunca scroll vertical en el contenido principal de un tab
- Cada tab debe caber en 720px de alto sin scroll
- Si hay scroll, consolidar grupos o mover a sub-tab

### 3. Agrupación por tarea, no por tipo de control
- MAL: "GAIN%" + "GAIN Raw" + "AGC%" + "AGC Raw" = 4 grupos
- BIEN: "GAIN  DL │ UL" + "AGC  DL │ UL" = 2 grupos compactos con % y raw en la misma fila

### 4. Tests colapsados por defecto
- Los paneles de diagnóstico (COMM Test, ADC Test, BIST) ocupan espacio pero se usan ocasionalmente
- Usar `QGroupBox` checkable o sección colapsable con `setCheckable(true)` y `setChecked(false)`

### 5. Feedback inmediato
- Botones de envío deshabilitados cuando puerto cerrado (`enabled = isOpen`)
- Resultado de test: color verde ✅  / rojo ❌ con `applyTestResult()`
- Stream activo: botón cambia texto a "⏹  Detener Stream"

---

## Convenciones de código (Qt C++)

- Miembros con `_` final: `portCombo_`, `dlSlider_`
- Layouts anidados: `QVBoxLayout > QHBoxLayout > QGridLayout`
- Tabs en `tabWidget_`, log en `logPanel_` (compartido)
- `serialPort_` compartido entre tabs via puntero (no ownership)
- `QGroupBox::setCheckable(true)` para secciones colapsables
- Nunca `HAL_Delay` en GUI (solo en firmware); usar `QTimer` para polls

---

## Checklist para agregar una nueva placa

1. Crear `src/<placa>/PlacaTab.h` y `PlacaTab.cpp`
2. Incluir en `mainwindow.h` forward-declare + miembro `PlacaTab *placaTab_ {nullptr}`
3. En `buildUi()`: `placaTab_ = new PlacaTab(serialPort_, logPanel_); tabWidget_->addTab(placaTab_, "Nombre Placa")`
4. Habilitar botones en `toggleConnection()` según estado del puerto
5. Documentar comandos UART en la tabla de esta sección
6. Actualizar `CHANGELOG.md` y `version.h`

---

## Build

```powershell
# Windows (MinGW)
cd shared/sw-vlad-dac-tools
cmake -S . -B build_mingw -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release
cmake --build build_mingw -j4

# O usar el script
.\build-gui.ps1
```

Ejecutable: `build_mingw/vlad-dac-tools-v*.exe`
