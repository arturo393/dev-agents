#!/bin/bash
# run_backtest.sh
# Runs the GA Optimization process on the remote server in the background.

REMOTE_USER="arturo"
REMOTE_HOST="192.168.1.149"
PASSWORD="Admin.123"
REMOTE_DIR="/home/arturo/monteCarlo"

echo "🚀 Starting Backtest & GA Optimization on $REMOTE_HOST..."

sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" "cd $REMOTE_DIR && nohup ./cpp_bot/build/ga_optimizer > data/logs/ga_optimizer.log 2>&1 &"

echo "✅ Optimization triggered. Logs are being written to data/logs/ga_optimizer.log on the server."
