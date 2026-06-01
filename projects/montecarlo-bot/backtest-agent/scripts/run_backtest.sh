#!/bin/bash
# run_backtest.sh — GA Optimization pipeline
# Aprendizaje: si descubrís un nuevo failure mode, agregalo acá abajo
# Última actualización: 2026-06-01

REMOTE_USER="arturo"
REMOTE_DIR="/home/arturo/monteCarlo"

# === SERVER DISCOVERY ===
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

echo "🚀 Starting Backtest & GA Optimization on $REMOTE_HOST..."

# Check if GA already running
ga_running=$(ssh "${REMOTE_USER}@${REMOTE_HOST}" "pgrep -a ga_optimizer" 2>/dev/null)
if [ -n "$ga_running" ]; then
  echo "⚠️  GA already running: $ga_running"
  exit 0
fi

# Check binary exists
ssh "${REMOTE_USER}@${REMOTE_HOST}" "ls ${REMOTE_DIR}/cpp_bot/build/ga_optimizer" 2>/dev/null || {
  echo "❌ ga_optimizer binary not found — compile first"
  exit 1
}

nohup ssh "${REMOTE_USER}@${REMOTE_HOST}" "cd ${REMOTE_DIR} && nohup ./cpp_bot/build/ga_optimizer > data/logs/ga_optimizer.log 2>&1 &" &

echo "✅ GA Optimization started on $REMOTE_HOST (PID: $(ssh ${REMOTE_USER}@${REMOTE_HOST} "pgrep -f ga_optimizer" 2>/dev/null))"
echo "Logs: ${REMOTE_DIR}/data/logs/ga_optimizer.log"
