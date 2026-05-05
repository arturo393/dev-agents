#!/bin/bash
# fetch_logs.sh
# Usage: ./fetch_logs.sh [lines] [log-file]
# Examples: 
# ./fetch_logs.sh 100
# ./fetch_logs.sh 50 bot_production.log

LINES=${1:-100}
LOG_FILE=${2:-bot_production.log}
REMOTE_USER="arturo"
REMOTE_HOST="192.168.1.149"
PASSWORD="Admin.123"
REMOTE_LOG_PATH="/home/arturo/monteCarlo/data/logs/${LOG_FILE}"

echo "Fetching last $LINES lines from $LOG_FILE on $REMOTE_HOST..."

sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" "tail -n $LINES $REMOTE_LOG_PATH"
