#!/bin/bash
# fetch_logs.sh — Conocimiento acumulado de log fetching
# Aprendizaje: si descubrís un nuevo log file o patrón, agregalo acá abajo
# Última actualización: 2026-06-01

LINES=${1:-100}
LOG_FILE=${2:-bot_production.log}
REMOTE_USER="arturo"
REMOTE_LOG_PATH="/home/arturo/monteCarlo/data/logs/${LOG_FILE}"

# === SERVER DISCOVERY (aprendido: 2026-06-01) ===
for host in 100.74.53.2 192.168.1.149; do
  ssh -o ConnectTimeout=2 -o StrictHostKeyChecking=no "${REMOTE_USER}@${host}" 'echo ok' 2>/dev/null && {
    REMOTE_HOST="$host"
    break
  }
done
if [ -z "$REMOTE_HOST" ]; then
  echo "❌ Ningún servidor responde"
  exit 1
fi

echo "Fetching last $LINES lines from $LOG_FILE on $REMOTE_HOST..."
ssh -o ConnectTimeout=5 "${REMOTE_USER}@${REMOTE_HOST}" "tail -n $LINES $REMOTE_LOG_PATH"
