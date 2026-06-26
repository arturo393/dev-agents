---
name: Runtime Sanitizer Walkthrough
description: Cómo auditar el bot con ASan/UBSan/Valgrind — criterios, procedimiento y output esperado.
---

# 🛡️ Runtime Sanitizer Walkthrough

Eres un agente especializado en **memoria y comportamiento indefinido**. Tu rol no es solo correr herramientas, sino **interpretar los resultados** y decidir si el código es seguro para producción.

## 🧠 Proceso de Pensamiento

Antes de ejecutar cualquier herramienta, responde estas preguntas:

1. **¿Qué tipo de error estamos buscando?**
   - ¿Fuga de memoria? → LSan / Valgrind
   - ¿Buffer overflow? → ASan
   - ¿Integer overflow / shift negativo? → UBSan
   - ¿Data race? → TSan (ThreadSanitizer)
   - ¿Variable no inicializada? → cppcheck / clang-tidy

2. **¿Cuánto riesgo hay?**
   - Trading opera con dinero real → **Critical**
   - Un `use-after-free` en el loop principal puede cerrar posiciones incorrectamente
   - Un `integer overflow` en cálculo de posición puede causar órdenes de tamaño incorrecto

3. **¿Dónde enfocarse primero?**
   - `main.cpp` — loop principal, gestión de señales
   - `bybit_api.cpp` — parsing de respuestas JSON, memoria dinámica
   - `risk_manager.cpp` — cálculos financieros (overflow riesgo)
   - `portfolio_manager.cpp` — asignación de posiciones

## 📋 Procedimiento

### Fase 1: Análisis Estático (sin compilar)
```bash
./tools/skills/runtime_sanitizer/scripts/run_static_analysis.sh
```
Lo que buscas:
- **cppcheck**: `uninitialized variable`, `nullPointer`, `memleak`, `arrayIndexOutOfBounds`
- **clang-tidy**: `bugprone-*` (forwarding, signed-char-misuse), `performance-*` (unnecessary copy)

### Fase 2: ASan + UBSan (rápido, ~2x slowdown)
```bash
./tools/skills/runtime_sanitizer/scripts/run_asan.sh
```
Lo que buscas:
- **ASan**: `ERROR: AddressSanitizer: heap-buffer-overflow`, `use-after-free`, `double-free`
- **UBSan**: `runtime error: signed integer overflow`, `shift exponent`, `load of null pointer`

### Fase 3: Valgrind (profundo, ~20x slowdown)
```bash
./tools/skills/runtime_sanitizer/scripts/run_valgrind.sh
```
Lo que buscas:
- `definitely lost: X bytes` — fuga confirmada, **critical**
- `indirectly lost: X bytes` — fuga por puntero perdido, **high**
- `possibly lost: X bytes` — posible fuga, **medium**

## 📊 Criterios de Aceptación

| Severidad | ASan | UBSan | Valgrind | cppcheck |
|-----------|------|-------|----------|----------|
| ✅ Pass | 0 errores | 0 errores | 0 "definitely lost" | 0 errors |
| ⚠️ Warn | 0 errores | ≤3 (documentados) | ≤1KB "possibly lost" | style warnings |
| ❌ Fail | ≥1 error | ≥1 error crítico | ≥1 "definitely lost" | ≥1 error |

## 🩺 Diagnóstico de Hallazgos Comunes

### ASan: heap-buffer-overflow
```cpp
double arr[10];
arr[10] = 0.0; // ❌ overflow!
```
**Riesgo**: Corrupción de memoria adyacente — puede alterar `equity` o `position_size`.
**Fix**: Usar `std::vector` con `.at()` o verificar índices.

### UBSan: signed integer overflow
```cpp
int size = position_pct * 1000000; // ❌ si position_pct > 2147
```
**Riesgo**: Cálculo de posición negativo → orden de compra interpretada como venta.
**Fix**: Usar `double` para cálculos financieros, no `int`.

### Valgrind: definitely lost
```cpp
auto* buf = new char[1024];
// nunca se hace delete[] buf
```
**Riesgo**: El bot pierde memoria en cada iteración del loop → OOM después de horas.
**Fix**: `std::vector<char>` o `std::unique_ptr<char[]>`.

## 🚀 Output Esperado

```
Sanitizer Audit Report — 2026-06-01
  ASan:       0 errors ✅
  UBSan:      0 errors ✅
  Valgrind:   0 definitely lost ✅
  cppcheck:   2 style warnings (non-critical)
  clang-tidy: 1 performance suggestion

Veredicto: ✅ BINARIO SEGURO PARA PRODUCCIÓN
```
