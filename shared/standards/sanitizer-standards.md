---
name: Sanitizer Standards
description: Reglas para compilación y ejecución segura con ASan/UBSan/Valgrind en proyectos C++ de trading.
---

# 🛡️ Sanitizer Standards — Memory Safety for Trading Bots

Estos estándares aplican a TODO el código C++ del bot MonteCarlo que maneje lógica de trading, conexiones de red o datos financieros.

## 📜 Reglas Obligatorias

### R1: Compilar siempre con ASan en Debug
```cmake
# CMakeLists.txt — perfil Debug
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -fsanitize=address,undefined -fno-omit-frame-pointer -g -O1")
```

### R2: Zero tolerancia a memory leaks en producción
- `definitely lost` en Valgrind = **bloqueante para deploy**
- `indirectly lost` = **fix obligatorio en siguiente sprint**
- `possibly lost` = **investigar, documentar si no se puede fixear**

### R3: Prohibido usar `new`/`delete` crudo
```cpp
// ❌ MALO
auto* buf = new char[1024];
delete[] buf;

// ✅ BUENO
auto buf = std::make_unique<char[]>(1024);
// o
std::vector<char> buf(1024);
```

### R4: Prohibido `reinterpret_cast` en código financiero
```cpp
// ❌ MALO — puede violar strict aliasing
double price = *reinterpret_cast<double*>(raw_bytes);

// ✅ BUENO
double price;
std::memcpy(&price, raw_bytes, sizeof(price));
```

### R5: Usar `std::vector::at()` en vez de `operator[]` en debug
```cpp
// ❌ MALO — sin bounds checking
double val = arr[i];

// ✅ BUENO
double val = arr.at(i);
```

### R6: Verificar divisiones por cero antes de cálculos financieros
```cpp
// ❌ MALO
double ratio = a / b;

// ✅ BUENO
if (std::abs(b) < 1e-10) {
    log_warning("Division by near-zero in risk calculation");
    return 0.0;
}
double ratio = a / b;
```

### R7: No convertir `int` → `double` sin verificar overflow
```cpp
// ❌ MALO si position_size_pct > 2147
int size_pct = position_size_pct * 100;

// ✅ BUENO
double size_pct = position_size_pct * 100.0;
```

## 📊 Clasificación de Hallazgos

| Severidad | Sanitizer | Ejemplo | Acción |
|-----------|-----------|---------|--------|
| 🔴 Critical | ASan | heap-buffer-overflow en main loop | Deploy bloqueado |
| 🔴 Critical | Valgrind | definitely lost en bybit_api | Deploy bloqueado |
| 🟠 High | UBSan | signed integer overflow en risk | Fix inmediato |
| 🟠 High | UBSan | nullptr load en portfolio | Fix inmediato |
| 🟡 Medium | LSan | memory leak en script de mantenimiento | Fix este sprint |
| 🟢 Low | cppcheck | variable no inicializada (no crítica) | Documentar |
| ⚪ Info | clang-tidy | performance suggestion | Evaluar |

## 🔁 Frecuencia Recomendada

| Cuándo | Qué ejecutar |
|--------|-------------|
| Cada commit en PR | `cppcheck` + `clang-tidy` |
| Antes de merge a main | `ASan + UBSan` (full suite) |
| Antes de deploy a producción | `Valgrind` en dry-run |
| Mensualmente | Auditoría completa (ASan + UBSan + Valgrind + cppcheck) |
