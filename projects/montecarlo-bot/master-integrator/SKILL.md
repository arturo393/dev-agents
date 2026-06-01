---
name: Master Integrator
description: Invoca los 9 agentes en secuencia, consolida resultados. SKILL.md = orquestación. agent.py = ejecución secuencial.
---

# Master Integrator

1. **SKILL.md** — plan de orquestación, orden de agentes, interpretación
2. **`python3 agent.py discover`** — ejecuta los 9 agentes secuencialmente y consolida

## 1. Orden de Ejecución

Los agentes se ejecutan en este orden para maximizar información compartida:

```
 1. backtest-agent         → estado del GA optimizer
 2. bio-cognitive-guard    → carga cognitiva y fatiga de alertas
 3. bot-functional-auditor → auditoría end-to-end del bot
 4. runtime-sanitizer      → memory safety y UB
 5. btd-sdd-validation     → BDD/TDD/ATT/SDD
 6. cleanup-engine         → dead code y basura
 7. check-server-logs      → análisis de logs
 8. cpp-trading-reviewer   → C++ static analysis
 9. database-auditor       → PnL y anomalías
```

## 2. Ejecución

```bash
python3 agent.py discover
```

## 3. Interpretación de Resultados

Cada agente devuelve:
- `environment`: estado dinámico del entorno (servidores, tools, schema)
- `audits`: resultados de los scripts estáticos

Revisá especialmente:
- `returncode: 0` ✅ = pasó
- `returncode: != 0` ❌ = falló, revisar `stdout`/`stderr`
- `error: not found` = script o entorno faltante
