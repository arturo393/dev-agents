---
name: CPP Trading Reviewer
description: C++ static analysis, trading safety, distributed systems audit. SKILL.md = dynamic review. agent.py = static analyzer.
---

# CPP Trading Reviewer

1. **SKILL.md** — revisión dinámica de código C++ y patrones de trading
2. **`python3 agent.py discover`** — descubre archivos, patrones peligrosos, compilador + corre analyzer
3. **Aprendizaje** — codificá nuevos anti-patrones

## 1. Revisión Dinámica

```bash
cd /Users/arturo/development/lumina/monteCarlo/cpp_bot

# Financial Integrity
echo '=== round_qty en órdenes ==='
grep -n 'round_qty\|round_price\|lot_size\|price_filter' src/*.cpp

echo '=== Stop Loss en cada orden ==='
grep -B5 'send_order\|place_order' src/*.cpp | grep -c 'stop_loss\|sl\|take_profit\|tp'

# C++ Safety
echo '=== Raw new/delete ==='
grep -rn 'new \|delete ' src/*.cpp | grep -v '//\|delete\[\]' | head -15

echo '=== Mutex sin RAII ==='
grep -rn 'lock()\|unlock()' src/*.cpp | grep -v 'lock_guard\|unique_lock\|scoped_lock'

# Rate limiting
echo '=== 429 / timeout handling ==='
grep -rn '429\|too_many\|rate_limit\|retry_after\|backoff\|timeout' src/*.cpp
```

## 2. Descubrimiento

```bash
python3 agent.py discover
```

## 3. Análisis Estático

```bash
python3 agent.py full_audit
python3 agent.py analyzer
```

## 4. Aprendizaje

Si descubrís un nuevo anti-patrón C++ o de trading, codificalo:
```bash
echo '# $(date): nuevo anti-patron' >> scripts/run_full_audit.sh
```
