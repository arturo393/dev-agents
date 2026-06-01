---
name: Testing Standards (BTD/SDD)
description: Estándares y criterios de aceptación para validación BDD, TDD, ATT y SDD en monteCarlo.
---

# 🧪 Testing Standards — BDD/TDD/ATT/SDD

Estos estándares definen cuándo y cómo aplicar cada capa de validación al bot MonteCarlo.

## 📊 Cobertura Mínima por Capa

| Capa | Cobertura Mínima | Cobertura Actual | Meta |
|------|-----------------|------------------|------|
| **TDD** (Unit) | 70% funciones core | 3 tests C++ + 2 suites Python | → 6 tests C++ + 4 suites Python |
| **BDD** (Escenarios) | 6 escenarios | 6 escenarios (SKIP en dev, PASS en prod) | ✅ |
| **ATT** (Integración) | 3 tests E2E | 3 tests (2 OK en prod) | → 5 tests E2E |
| **SDD** (Diseño) | 100% componentes documentados | 10/10 componentes OK | ✅ |

## 🧪 TDD — Unit Testing Standards

### Qué testear
- Lógica de scoring (`quantitative_scorer.cpp`)
- Cálculos de riesgo (`risk_manager.cpp`)
- Penalización por correlación (`portfolio_manager.cpp`)
- Bayesian learner (`statistical_learner.cpp`)
- Detección de régimen (`markov_regime_detector.cpp`)

### Qué NO testear
- Conexiones de red (son ATT)
- Lógica de UI (no existe)
- Constructores triviales

### Formato
```cpp
// Cada test debe verificar UNA cosa y tener nombre descriptivo
void test_kelly_calculation_with_high_win_rate() {
    double kelly = calculate_kelly(0.7, 2.0, 1.0);
    assert(kelly > 0.3);
    assert(kelly < 0.5);
}
```

## 📋 BDD — Business Scenario Standards

### Escenarios actuales
| ID | Escenario | Crítico para producción |
|----|-----------|------------------------|
| BDD-001 | Bot binary exists | ✅ Sí |
| BDD-002 | Trading database exists | ✅ Sí |
| BDD-003 | SQLite WAL mode enabled | ✅ Sí |
| BDD-004 | RL model (ONNX) exists | ⚠️ No crítico (fallback sin RL) |
| BDD-005 | API keys configured | ✅ Sí |
| BDD-006 | GA Optimizer enabled | ⚠️ No crítico (fallback a defaults) |

### Regla de deployment
Si BDD-001, BDD-003 o BDD-005 fallan → **NO DEPLOYAR**

## 🌐 ATT — Integration Standards

### Prerrequisitos
- Conexión a internet (Bybit API)
- `.env` con API keys válidas
- (Opcional) SSH a servidor de producción

### Validaciones
| ID | Validación | Dependencia | Falla bloqueante |
|----|-----------|-------------|-----------------|
| ATT-001 | Bybit API reachable | Internet | ✅ Sí |
| ATT-002 | API key permissions | .env | ✅ Sí |
| ATT-003 | Bot process active | SSH a prod | ⚠️ No (monitoreo) |
| ATT-004 | Dashboard API responds | Nginx en prod | ⚠️ No (monitoreo) |

## 📐 SDD — Design Standards

### Qué auditar
- Coherencia entre `include/` y `src/` (cada .cpp debe tener su .hpp)
- Coherencia entre CMakeLists.txt y archivos existentes
- Componentes que violan la arquitectura documentada
- Dead code (existe en build pero no en flujo de producción)

### Checklist de diseño
- [ ] ¿Cada clase tiene un solo propósito? (Single Responsibility)
- [ ] ¿Los nombres reflejan el dominio? (no `DataProcessor`, sí `RiskManager`)
- [ ] ¿Hay archivos en `include/` sin correspondencia en `src/`? (header-only OK si es pequeño)
- [ ] ¿Hay archivos en `src/` que no están en CMakeLists.txt?
- [ ] ¿Hay archivos en CMakeLists.txt que no existen en el disco?
