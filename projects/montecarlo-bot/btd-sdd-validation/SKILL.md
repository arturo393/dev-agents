---
name: Validation Agent (BTD/SDD)
description: BDD/TDD/ATT/SDD multi-layer validation. SKILL.md = dynamic review. agent.py = static scenarios.
---

# Validation Agent

1. **SKILL.md** — revisión de tests y escenarios en vivo
2. **`python3 agent.py discover`** — descubre entorno (dev/prod), binarios, API keys + corre validación
3. **Aprendizaje** — codificá nuevos escenarios BDD

## 1. Revisión Dinámica

```bash
cd /Users/arturo/development/lumina/monteCarlo/cpp_bot

# ¿Qué tests existen?
ls build/test_* 2>/dev/null || ls build/tests/test_* 2>/dev/null

# ¿Qué cubren?
grep -rn 'TEST\|test_' src/*test*.cpp | head -20

# BDD scenarios en vivo
ssh arturo@100.74.53.2 "
  echo 'Binary:'; ls -lh /home/arturo/monteCarlo/cpp_bot/build/trading_bot 2>/dev/null
  echo 'DB:'; ls -lh /home/arturo/monteCarlo/cpp_bot/data/trading_data.db 2>/dev/null
  echo 'API:'; curl -s -o /dev/null -w '%{http_code}' https://api.bybit.com
  echo 'Bot:'; pgrep -f trading_bot && echo ALIVE || echo DEAD
"
```

## 2. Descubrimiento

```bash
python3 agent.py discover
```

## 3. Validación Estática

```bash
python3 agent.py validation
```

## 4. Aprendizaje

Si descubrís un nuevo escenario BDD o failure mode, codificalo:
```bash
echo '# $(date): nuevo BDD scenario' >> scripts/run-validation.sh
```
