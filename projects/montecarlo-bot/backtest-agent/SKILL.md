---
name: Backtest Agent
description: GA optimization orchestrator. SKILL.md = dynamic review. agent.py = static pipeline.
---

# Backtest Agent

1. **SKILL.md** — revisión dinámica del pipeline de optimización
2. **`python3 agent.py discover`** — descubre servidor, GA status, disk space + corre pipeline
3. **Aprendizaje** — codificá nuevos failure modes

## 1. Revisión Dinámica

```bash
cd /Users/arturo/development/lumina/monteCarlo/cpp_bot
# ¿Cómo se configura el GA?
grep -n 'population\|generation\|mutation\|crossover\|fitness' src/ga_optimizer.cpp | head -15

# ¿Qué symbols optimiza?
grep -A20 'symbols\|SYMBOLS\|tickers' src/ga_optimizer.cpp | head -20
```

## 2. Descubrimiento

```bash
python3 agent.py discover
```

## 3. Pipeline Estático

```bash
python3 agent.py backtest
```

## 4. Aprendizaje

Si descubrís un nuevo error de compilación, límite de hardware, o flag de optimización, codificalo:
```bash
echo '# $(date): nuevo failure mode' >> scripts/run_backtest.sh
```
