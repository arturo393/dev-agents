---
name: Bot Functional Auditor
description: End-to-end technical audit. SKILL.md = dynamic review. agent.py = static scripts.
---

# Bot Functional Auditor

1. **SKILL.md** — revisión de todos los módulos del bot en vivo
2. **`python3 agent.py discover`** — descubre proceso, DB, API keys + corre audits
3. **Aprendizaje** — codificá nuevos checks de auditoría

## 1. Revisión Dinámica

```bash
cd /Users/arturo/development/lumina/monteCarlo/cpp_bot
# Cadena de señales activa
grep -n 'analyze_and_trade\|strategy.analyze\|get_score\|should_enter' src/main.cpp | head -20

# Risk management
grep -n 'drawdown\|max_dd\|circuit\|stop_loss\|take_profit' src/main.cpp | head -15

# Conexiones API
grep -n 'BybitAPI\|api\..*timeout\|retry\|try.*catch' src/*.cpp | head -15

# En vivo en servidor
ssh arturo@100.74.53.2 "
  pgrep -f trading_bot && echo 'BOT ALIVE' || echo 'BOT DEAD'
  ls -lh /home/arturo/monteCarlo/cpp_bot/data/trading_data.db
  head -3 /home/arturo/monteCarlo/cpp_bot/.env
"
```

## 2. Descubrimiento

```bash
python3 agent.py discover
```

## 3. Audits Estáticos

```bash
python3 agent.py full_audit
python3 agent.py maintenance_prod
python3 agent.py maintenance_system
```

## 4. Aprendizaje

Si descubrís un nuevo módulo o failure mode, codificalo:
```bash
echo '# $(date): nuevo audit check' >> scripts/full_audit.sh
```
