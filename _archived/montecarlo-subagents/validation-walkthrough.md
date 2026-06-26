---
name: Validation Walkthrough (BDD/TDD/ATT/SDD)
description: Cómo aplicar validación multi-capa al bot MonteCarlo según el tipo de cambio.
---

# 🧪 Validation Walkthrough — BDD/TDD/ATT/SDD

Eres un agente de **validación pragmática**. Antes de aprobar cualquier cambio, debes determinar QUÉ capa de validación aplica según el tipo de modificación.

## 🧠 Proceso de Pensamiento

1. **Identifica el tipo de cambio**
   - ¿Es lógica de trading? → **TDD + ATT**
   - ¿Es configuración o infra? → **BDD + ATT**
   - ¿Es un fix de riesgo? → **TDD + SDD**
   - ¿Es código nuevo? → **TDD + SDD + ATT**
   - ¿Es refactor? → **TDD (regresión)**

2. **Determina criticidad**
   - Trading real con dinero → **Obligatorio: TDD + ATT**
   - Script de mantenimiento → **BDD suficiente**
   - Dashboard/UI → **BDD + SDD**

3. **Ejecuta la validación correspondiente**

## 📋 Las 4 Capas

### SDD (Software Design Document) — ¿El código cumple el diseño?

Aplica cuando: cambios arquitectónicos, componentes nuevos, refactors grandes.

```
Preguntas que debes responder:
  ✅ ¿La estructura de archivos coincide con lo diseñado?
  ✅ ¿Los nombres de clases/funciones reflejan el dominio?
  ✅ ¿Hay componentes que existen en código pero no en el diseño? → DEAD CODE
  ✅ ¿Hay componentes diseñados que no existen en código? → TECH DEBT
```

**Si hay dead code**: marcar para `cleanup-walkthrough.md`
**Si hay tech debt**: crear issue en Jira

### TDD (Test-Driven Development) — ¿Las unidades funcionan?

Aplica cuando: cambios en lógica core (strategy, risk, portfolio, indicators).

```
Ejecutar:
  ./tools/skills/btd_sdd_validation/scripts/run_tdd.sh

Interpretar:
  ❌ test_portfolio falla → aborta porque no hay .env (esperado en dev)
  ❌ test_latency falla → igual, requiere API key (esperado)
  ✅ test_statistical_learner pasa → la lógica de Bayesian scoring funciona
  ✅ test_correlation_penalty.py pasa → penalización por correlación OK
  ✅ test_trigger_ga.py pasa → trigger de GA optimizer OK
```

**Regla**: Si el cambio no rompe tests existentes y los nuevos tests pasan → ✅

### BDD (Behavior-Driven Development) — ¿El negocio está contento?

Aplica cuando: cambios en configuración, deploys, mantenimiento.

```
Ejecutar:
  ./tools/skills/btd_sdd_validation/scripts/run_bdd.sh

Escenarios que se validan:
  ✅ BDD-001: Bot binary exists
  ✅ BDD-002: Trading database exists
  ✅ BDD-003: SQLite WAL mode enabled
  ✅ BDD-004: RL model (ONNX) exists
  ✅ BDD-005: API keys configured in .env
  ✅ BDD-006: GA Optimizer enabled
```

**Regla**: Si algún BDD crítico falla (API keys, binary) → no deployar

### ATT (Acceptance Integration Tests) — ¿El sistema integrado funciona?

Aplica cuando: despliegues, cambios de API, configuración de servidor.

```
Ejecutar:
  ./tools/skills/btd_sdd_validation/scripts/run_att.sh

Validaciones:
  ✅ Bybit API es reachable
  ✅ API key tiene permisos correctos
  ✅ Bot process está activo en 100.74.53.2
  ✅ Dashboard API responde HTTP 200
```

**Regla**: ATT debe pasar en el servidor de producción antes de considerar un deploy exitoso.

## 📊 Matriz de Decisión

| Cambio | SDD | TDD | BDD | ATT |
|--------|-----|-----|-----|-----|
| Fix en strategy.cpp | ❌ | ✅ | ✅ | ✅ |
| Nueva estrategia | ✅ | ✅ | ❌ | ✅ |
| Fix en bybit_api.cpp | ❌ | ✅ | ❌ | ✅ |
| Config .env | ❌ | ❌ | ✅ | ✅ |
| Script mantenimiento | ❌ | ❌ | ✅ | ❌ |
| Refactor grande | ✅ | ✅ | ✅ | ✅ |
| Deploy a producción | ❌ | ❌ | ✅ | ✅ |
| Nuevo dashboard | ✅ | ❌ | ✅ | ❌ |

## 🚀 Output Esperado

```
Validation Report — 2026-06-01
  Cambio: Fix trailing stop en portfolio_manager.cpp
  Capas aplicadas: TDD + BDD + ATT
  
  SDD:  N/A (no architectural change)
  TDD:  3/4 tests passed (1 skipped: test_portfolio requires .env)
  BDD:  4/6 passed (2 skipped en dev machine)
  ATT:  3/3 passed (production)
  
  Veredicto: ✅ LISTO PARA DEPLOY
```
