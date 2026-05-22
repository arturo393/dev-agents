#!/bin/bash
REMOTE_USER="arturo"
REMOTE_HOST="192.168.1.149"
REMOTE_HOST_TS="100.74.53.2"
PASSWORD="Admin.123"
REMOTE_DB="/home/arturo/monteCarlo/data/trading_data.db"
REMOTE_LOG="/home/arturo/monteCarlo/data/logs/bot_production.log"
MAINTENANCE_LOG="/home/arturo/monteCarlo/cpp_bot/data/logs/maintenance.log"

echo "=========================================="
echo "  TRADING BOT FULL AUDIT"
echo "  $(date)"
echo "=========================================="

echo ""
echo "=== 1. Process Status (via Tailscale) ==="
timeout 5 sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=3 "$REMOTE_USER@$REMOTE_HOST_TS" "systemctl is-active montecarlo_bot.service" 2>/dev/null || echo "⚠️  Tailscale unreachable (trying local IP)..."

echo ""
echo "=== 2. Signals (last hour) ==="
timeout 10 sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$REMOTE_USER@$REMOTE_HOST" "sqlite3 $REMOTE_DB \"SELECT symbol, COUNT(*) as signals FROM signals WHERE timestamp > (strftime('%s', 'now') - 3600) GROUP BY symbol;\"" 2>/dev/null || echo "❌ No signals data"

echo ""
echo "=== 3. Risk / Correlation ==="
timeout 10 sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$REMOTE_USER@$REMOTE_HOST" "grep -i 'correlation' $REMOTE_LOG 2>/dev/null | tail -3" || echo "❌ No correlation data"

echo ""
echo "=== 4. Last 50 Log Lines ==="
timeout 15 sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$REMOTE_USER@$REMOTE_HOST" "tail -50 $REMOTE_LOG" || echo "❌ Failed to fetch logs"

echo ""
echo "=== 5. Maintenance Log ==="
timeout 10 sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$REMOTE_USER@$REMOTE_HOST" "tail -5 $MAINTENANCE_LOG 2>/dev/null" || echo "❌ No maintenance log"

echo ""
echo "=== 6. PnL by Exit Reason ==="
timeout 10 sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$REMOTE_USER@$REMOTE_HOST" "sqlite3 $REMOTE_DB 'SELECT exit_reason, COUNT(*), SUM(pnl_usd), AVG(pnl_pct) FROM trade_outcomes GROUP BY exit_reason;'" 2>/dev/null || echo "❌ No PnL data"

echo ""
echo "=== 7. Last 5 Trades ==="
timeout 10 sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$REMOTE_USER@$REMOTE_HOST" "sqlite3 $REMOTE_DB 'SELECT o.trade_id, t.symbol, t.side, o.exit_price, o.pnl_usd, ROUND(o.pnl_pct,2) AS pnl_pct, o.exit_reason FROM trade_outcomes o JOIN trades t ON o.trade_id = t.timestamp ORDER BY o.exit_timestamp DESC LIMIT 5;'" 2>/dev/null || echo "❌ No trades data"

echo ""
echo "=== 8. RAM Usage ==="
timeout 10 sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 "$REMOTE_USER@$REMOTE_HOST" "free -m | grep Mem | awk '{print \"Used: \" \$3 \"MB / \" \$2 \"MB\"}'"

echo ""
echo "=========================================="
echo "  AUDIT COMPLETE"
echo "=========================================="
