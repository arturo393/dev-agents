---
name: Cleanup Walkthrough
description: Cómo identificar, auditar y eliminar código muerto del bot MonteCarlo sin romper nada.
---

# 🧹 Cleanup Walkthrough — Dead Code & Repo Sanitation

Eres un agente de **limpieza quirúrgica**. No se trata de borrar por borrar, sino de eliminar lo que sobra SIN romper lo que funciona.

## 🧠 Proceso de Pensamiento

### Paso 1: Identificar código muerto

Un archivo es "código muerto" si cumple TODAS estas condiciones:
1. ✅ Se compila en el binario de producción (`trading_bot`)
2. ❌ Su señal/función nunca se consume en el pipeline de producción
3. ❌ No hay planes inmediatos de reactivarlo

### Paso 2: Clasificar el riesgo

| Tipo | Ejemplo | Riesgo |
|------|---------|--------|
| **Nunca instanciado** | EnsembleEngine, MeanReversionStrategy | ⚪ Bajo — solo existe en backtest |
| **Instanciado pero no usado** | RLStrategy | 🟡 Medio — constructor corre pero señal se ignora |
| **Header only** | simple_daily_trend_strategy.hpp | ⚪ Bajo — código inerte |
| **Base class de dead code** | strategy_base.hpp | 🟠 Medio — puede afectar herencia |

### Paso 3: Verificar dependencias

Antes de tocar CMakeLists.txt:
```bash
# Verificar que ningún otro target usa estos archivos
grep -r "ensemble_engine" tools/ --include="*.cpp" --include="*.hpp"
grep -r "MeanReversionStrategy" cpp_bot/ --include="*.cpp" --include="*.hpp"
```

Si solo aparece en `backtest_simulator` → seguro de remover de `trading_bot`.

## 📋 Procedimiento

### Fase 1: Auditoría
```bash
./tools/skills/cleanup_engine/scripts/audit_dead_code.sh
```
Genera `docs/dead_code_audit.md` con:
- Archivos muertos y su tamaño
- Si están referenciados en backtest_simulator
- Total de bytes recuperables

### Fase 2: Remover (dry-run)
```bash
./tools/skills/cleanup_engine/scripts/remove_dead_code.sh --dry-run
```
Muestra qué líneas se eliminarían de CMakeLists.txt sin modificar nada.

### Fase 3: Remover (real)
```bash
./tools/skills/cleanup_engine/scripts/remove_dead_code.sh
```
Hace backup automático de CMakeLists.txt y elimina las líneas.

### Fase 4: Verificar
```bash
cmake -B build && cmake --build build -j$(nproc)
```
Si compila sin errores → ✅ listo.

## 📊 Estado Actual del Bot

| Archivo | Tamaño | En trading_bot | En backtest | Consumido en prod | Acción |
|---------|--------|----------------|-------------|-------------------|--------|
| `ensemble_engine.cpp` | ~8KB | ✅ | ✅ | ❌ | Remover de trading_bot |
| `quant_scorer_strategy.cpp` | ~4KB | ✅ | ✅ | ❌ | Remover de trading_bot |
| `mean_reversion_strategy.cpp` | ~5KB | ✅ | ✅ | ❌ | Remover de trading_bot |
| `volatility_breakout_strategy.cpp` | ~5KB | ✅ | ✅ | ❌ | Remover de trading_bot |
| `rl_strategy.cpp` | ~6KB | ✅ | ✅ | ❌ (cargada, no usada) | Remover de trading_bot |
| `simple_daily_trend_strategy.hpp` | ~2KB | ❌ (header) | ✅ | ❌ | Mantener (backtest) |
| `strategy_base.hpp` | ~3KB | ❌ (header) | ✅ | ❌ | Mantener (backtest) |

**Total recuperable**: ~28KB del binario, ~5 archivos menos que compilar.

## 🧹 Repo Sanitation

Además del dead code, ejecutar limpieza general:
```bash
./tools/skills/cleanup_engine/scripts/clean_repo.sh
```

Elimina automáticamente:
- `.DS_Store` — archivos de macOS
- `__pycache__` — caches de Python
- `*.pyc` — bytecode compilado
- Directorios vacíos

NO elimina automáticamente (requiere revisión manual):
- `*.bak`, `*.backup` — backups intencionales
- `venv/`, `.venv/` — entornos virtuales activos

## 🚀 Output Esperado

```
Cleanup Report — 2026-06-01
  Dead code audit:
    5 source files, 7 headers = ~28KB
    All confirmed unused in production signal chain
    All confirmed used only in backtest_simulator
  
  Action: Remove from trading_bot source list
  Backup: CMakeLists.txt.bak.20260601
  
  Repo sanitation:
    Removed 8 .DS_Store files
    Removed 2 __pycache__ directories
    Freed: 53KB
  
  Veredicto: ✅ BINARIO MÁS LIMPIO, COMPILACIÓN VERIFICADA
```
