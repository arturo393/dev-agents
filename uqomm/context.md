# Context: Uqomm Corporation

## 1. Metadata
- **Tenant:** Uqomm Corporation
- **Primary Platforms:** 
  - **Embedded Firmware:** `fw-ulad` (STM32, Lora, C99/C++)
  - **Desktop Tools:** `sw-vlad-dac-tools` (C++17, FTXUI TUI, Qt6 GUI)
  - **Doc Compiler:** `sw-documentation` (Python, Pypandoc, MD-to-DOCX, Live Server)

## 2. Path Mappings
- **Root Directory:** `/Users/arturo/development/Uqomm/`
- **Firmware Workspace (`fw-ulad`):** `/Users/arturo/development/Uqomm/fw-ulad/`
- **Doc Compiler Workspace (`sw-documentation`):** `/Users/arturo/development/Uqomm/sw-documentation/`
- **TUI Source:** `shared/sw-vlad-dac-tools/tui/`
- **GUI Source:** `shared/sw-vlad-dac-tools/gui/`
- **Tests Source:** `shared/sw-vlad-dac-tools/shared/tests/` (Catch2 v3 Catch-standalone)

## 3. Build, Compile & Test Toolchains

### A) Embedded Firmware (`fw-ulad`):
- **Compiler:** `arm-none-eabi-gcc` makefiles
- **Build Path:** `firmware/`
- **Unit Tests:** `tests/` directory

### B) Doc Compiler (`sw-documentation`):
- **Stack:** Python 3.12, `uv` package manager (`pyproject.toml`, `uv.lock`)
- **Compile HTML/DOCX Command:** `python3 compile.py` or `./compile.sh`
- **Live Preview Server:** `python3 live-server.py` or `python3 reload.py` (hosts a local hot-reloading doc viewer)

### C) Desktop Tools (`sw-vlad-dac-tools`):
- **TUI Build:** `cmake --build /Users/arturo/development/shared/sw-vlad-dac-tools/tui/build -j4`
- **GUI Build:** `cmake -B /tmp/gui-build -S /Users/arturo/development/shared/sw-vlad-dac-tools/gui -DCMAKE_BUILD_TYPE=Release && cmake --build /tmp/gui-build -j4`
- **CTest Suite:** `cmake -B /tmp/proto-tests -S /Users/arturo/development/shared/sw-vlad-dac-tools/shared/tests -DCMAKE_BUILD_TYPE=Release && cmake --build /tmp/proto-tests -j4 && cd /tmp/proto-tests && ctest --output-on-failure`

## 4. Bounded Conventions
- **Embedded STM32 (`fw-ulad`):** MISRA-C guidelines, HAL drivers, strictly no dynamic allocations (`malloc`), volatile keywords inside ISRs.
- **TUI/GUI Desktop:** Modern C++17, RAII and standard smart pointers, strictly **no C++ standard exceptions** in low-level library code (return `std::optional` or error code structs instead).
- **Qt6 GUI:** Explicit signal-slot bindings, QObject memory hierarchy, no raw Qt pointers without parent assignments.
- **Doc Compiler (`sw-documentation`):** Strictly valid markdown formatting, relative asset links, clean styling using custom css templates in `styles/`.

