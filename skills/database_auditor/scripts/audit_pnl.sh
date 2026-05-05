#!/bin/bash
# audit_pnl.sh
# Generates a quick PnL report and grabs recent trades from the remote SQLite database.

REMOTE_USER="arturo"
REMOTE_HOST="192.168.1.149"
PASSWORD="Admin.123"
REMOTE_DB="/home/arturo/monteCarlo/data/trading_data.db"

echo "📊 Fetching PnL stats from $REMOTE_HOST..."
echo "--- Grouped by Exit Reason ---"
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" "sqlite3 $REMOTE_DB 'SELECT exit_reason, COUNT(*), SUM(pnl_usd), AVG(pnl_pct) FROM trade_outcomes GROUP BY exit_reason;'"

echo ""
echo "--- Last 5 Trades ---"
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" "sqlite3 $REMOTE_DB '.mode column' '.headers on' 'SELECT o.trade_id, t.symbol, t.side, o.exit_price, o.pnl_usd, ROUND(o.pnl_pct, 2) AS pnl_pct, o.exit_reason FROM trade_outcomes o JOIN trades t ON o.trade_id = t.timestamp ORDER BY o.exit_timestamp DESC LIMIT 5;'"
