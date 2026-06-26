#!/bin/bash
REMOTE_USER="arturo"
REMOTE_HOST="100.74.53.2"
PASSWORD="${SSH_PASSWORD:?SSH_PASSWORD env var required}"
REMOTE_DB="/home/arturo/monteCarlo/data/trading_data.db"
REMOTE_LOG="/home/arturo/monteCarlo/data/logs/bot_production.log"
MAINTENANCE_LOG="/home/arturo/monteCarlo/cpp_bot/data/logs/maintenance.log"

echo "=== 1. Process ==="
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" "systemctl is-active montecarlo_bot.service"

echo "=== 2. Signals ==="
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" "sqlite3 $REMOTE_DB \"SELECT symbol, COUNT(*) as signals FROM signals WHERE timestamp > (strftime('%s', 'now') - 3600) GROUP BY symbol;\""

echo "=== 3. Risk ==="
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" "grep 'Correlation:' $REMOTE_LOG | tail -n 5"

echo "=== 4. Maintenance ==="
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" "tail -n 5 $MAINTENANCE_LOG"

echo "=== 5. RAM ==="
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" "free -m | grep Mem"
