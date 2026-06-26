---
name: Database Auditor
description: SQLite PnL and anomaly auditor. SKILL.md = dynamic review. agent.py = static tests.
---

# Database Auditor

Carga este skill para que opencode actúe como auditor de base de datos. El flujo:

1. **SKILL.md** (esto) — revisión dinámica del código y la DB en vivo
2. **`python3 agent.py discover`** — descubre el entorno y corre los tests estáticos acumulados
3. **Aprendizaje** — si encontrás una anomalía nueva, codificala en `agent.py` o `scripts/`

---

## 1. Revisión Dinámica de Código

Como auditor, inspeccioná el código fuente del bot para entender cómo se maneja la DB:

```bash
cd /Users/arturo/development/lumina/monteCarlo/cpp_bot

# ¿Cómo se crean/leen las tablas?
grep -n 'sqlite3\|CREATE TABLE\|INSERT INTO\|SELECT.*FROM' src/database_manager.cpp | head -20

# ¿Hay manejo de errores SQL?
grep -n 'sqlite3_exec\|sqlite3_prepare\|SQLITE_OK\|rc !=\|error_msg' src/database_manager.cpp | head -15

# ¿Las transacciones son atómicas?
grep -n 'BEGIN\|COMMIT\|ROLLBACK\|sqlite3_exec.*BEGIN\|sqlite3_exec.*COMMIT' src/database_manager.cpp

# ¿Se cierran las conexiones?
grep -n 'sqlite3_close\|database.close\|close()' src/database_manager.cpp
```

## 2. Descubrimiento del Entorno

```bash
python3 agent.py discover
```

Esto descubre: servidor vivo, schema de la DB, tools disponibles. El JSON de salida te dice qué correr.

## 3. Revisión de Schema en Vivo

SSH al servidor y revisá el schema directamente:

```bash
# Conectate al servidor activo (agent.py discover te dice cuál)
ssh arturo@100.74.53.2 "sqlite3 /home/arturo/monteCarlo/cpp_bot/data/trading_data.db '.schema'"

# Buscá anomalías
ssh arturo@100.74.53.2 "
  # Trades abiertos > 24h
  sqlite3 /home/arturo/monteCarlo/cpp_bot/data/trading_data.db '
    SELECT symbol, side, entry_price, datetime(timestamp, \"unixepoch\")
    FROM trades WHERE status = \"open\"
    AND timestamp < strftime(\"%s\", \"now\", \"-1 day\");'

  # Gaps en timestamps > 5 min
  sqlite3 /home/arturo/monteCarlo/cpp_bot/data/trading_data.db '
    SELECT datetime(a.timestamp), datetime(b.timestamp),
           (b.timestamp - a.timestamp) / 60.0 as gap_min
    FROM trades a, trades b
    WHERE b.rowid = a.rowid + 1
      AND (b.timestamp - a.timestamp) > 300
    ORDER BY gap_min DESC LIMIT 5;'

  # Profit factor
  sqlite3 /home/arturo/monteCarlo/cpp_bot/data/trading_data.db '
    SELECT COUNT(CASE WHEN pnl_usd > 0 THEN 1 END) as wins,
           COUNT(CASE WHEN pnl_usd < 0 THEN 1 END) as losses,
           ROUND(AVG(CASE WHEN pnl_usd > 0 THEN pnl_usd END), 2) as avg_win,
           ROUND(AVG(CASE WHEN pnl_usd < 0 THEN pnl_usd END), 2) as avg_loss
    FROM trade_outcomes
    WHERE exit_timestamp > strftime(\"%s\", \"now\", \"-7 days\");'
"
```

## 4. Tests Estáticos

```bash
# Todos los audits
python3 agent.py full

# Solo PnL
python3 agent.py pnl

# Solo fees
python3 agent.py fees
```

## 5. Aprendizaje

Si durante la revisión dinámica descubrís:
- Una **nueva anomalía** (trade duplicado, price spike, orphan trade) → agregala a `agent.py` como nuevo audit
- Un **nuevo failure mode** (schema que cambió, columna renombrada) → actualizá `agent.py` para detectarlo automáticamente en `_discover_environment()`
- Una **nueva query útil** → agregala a `scripts/audit_pnl.sh`

```bash
# Ejemplo: codificar un nuevo patrón
echo '# $(date): detectar trades con entry_price > 2x mark_price' >> scripts/audit_pnl.sh
echo "sqlite3 \$REMOTE_DB 'SELECT COUNT(*) FROM trades WHERE entry_price > mark_price * 2'" >> scripts/audit_pnl.sh
```
