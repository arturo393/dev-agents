#!/bin/bash
# audit_pnl.sh — Conocimiento acumulado de auditoría de DB
# Aprendizaje: si descubrís una nueva query o anomalía, agregala acá abajo
# Última actualización: 2026-06-01

REMOTE_USER="arturo"
PASSWORD="${SSH_PASSWORD:?SSH_PASSWORD env var required}"

# === SERVER DISCOVERY (aprendido: 2026-06-01) ===
# Original: 192.168.1.149 (legacy, no responde)
# Fallback:  100.74.53.2 (server actual)
for host in 100.74.53.2 192.168.1.149; do
  ssh -o ConnectTimeout=3 -o StrictHostKeyChecking=no "${REMOTE_USER}@${host}" 'echo ok' 2>/dev/null && {
    REMOTE_HOST="$host"
    break
  }
done
if [ -z "$REMOTE_HOST" ]; then
  echo "❌ Ningún servidor responde"
  exit 1
fi
echo "📊 Fetching PnL stats from $REMOTE_HOST..."

REMOTE_DB="/home/arturo/monteCarlo/cpp_bot/data/trading_data.db"
# Fallback a path legacy
ssh "${REMOTE_USER}@${REMOTE_HOST}" "ls $REMOTE_DB" 2>/dev/null || REMOTE_DB="/home/arturo/monteCarlo/data/trading_data.db"

echo "--- Grouped by Exit Reason ---"
ssh "${REMOTE_USER}@${REMOTE_HOST}" "sqlite3 $REMOTE_DB 'SELECT exit_reason, COUNT(*), SUM(pnl_usd), AVG(pnl_pct) FROM trade_outcomes GROUP BY exit_reason;'"

echo ""
echo "--- Last 5 Trades ---"
ssh "${REMOTE_USER}@${REMOTE_HOST}" "sqlite3 $REMOTE_DB '.mode column' '.headers on' 'SELECT o.trade_id, t.symbol, t.side, o.exit_price, o.pnl_usd, ROUND(o.pnl_pct, 2) AS pnl_pct, o.exit_reason FROM trade_outcomes o JOIN trades t ON o.trade_id = t.timestamp ORDER BY o.exit_timestamp DESC LIMIT 5;'"
