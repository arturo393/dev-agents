#!/bin/bash
# run-validation.sh — Conocimiento acumulado de validación BDD/TDD/ATT/SDD
# Aprendizaje: si descubrís un nuevo escenario, agregalo acá abajo
# ==================================================================

REMOTE_USER="arturo"
REMOTE_HOST="100.74.53.2"
REMOTE_DIR="/home/arturo/monteCarlo/cpp_bot"
LOCAL_DIR="/Users/arturo/development/lumina/monteCarlo/cpp_bot"

echo "=== VALIDATION STATIC CHECKS ==="

# === BDD ===
echo "[BDD] Business scenarios..."

# BDD-001: Binary existe
ssh ${REMOTE_USER}@${REMOTE_HOST} "ls -la ${REMOTE_DIR}/build/trading_bot 2>&1" | \
  awk '{print "  BDD-001 Bot binary: " ($1 ~ /^-/ ? "✅ " $9 " (" $5 ")" : "❌ not found")}'

# BDD-002: DB existe y tamaño
ssh ${REMOTE_USER}@${REMOTE_HOST} "ls -lh ${REMOTE_DIR}/data/trading_data.db 2>&1" | \
  awk '{print "  BDD-002 Trading DB: " ($1 ~ /^-/ ? "✅ " $5 : "❌ not found")}'

# BDD-003: WAL mode
ssh ${REMOTE_USER}@${REMOTE_HOST} "sqlite3 ${REMOTE_DIR}/data/trading_data.db 'PRAGMA journal_mode;' 2>&1" | \
  awk '{print "  BDD-003 WAL mode: " ($0 == "wal" ? "✅" : "❌ got: " $0)}'

# BDD-004: API keys format
ssh ${REMOTE_USER}@${REMOTE_HOST} "
  if [ -f ${REMOTE_DIR}/.env ]; then
    echo '  BDD-004 .env exists ✅'
    head -1 ${REMOTE_DIR}/.env | grep -q '#' && echo '  BDD-005 Has header comment ✅'
    grep BYBIT_API_KEY ${REMOTE_DIR}/.env | grep -q '=' && echo '  BDD-006 API_KEY format ✅' || echo '  BDD-006 API_KEY format ❌'
  else
    echo '  BDD-004 .env missing ❌'
  fi
"

# === TDD ===
echo "[TDD] Unit tests..."
ssh ${REMOTE_USER}@${REMOTE_HOST} "
  for t in test_statistical_learner test_latency test_portfolio; do
    if [ -f ${REMOTE_DIR}/build/\$t ]; then
      timeout 10 ${REMOTE_DIR}/build/\$t 2>&1 | tail -1
      echo \"  \$t exit: \$?\"
    else
      echo \"  \$t: binary not found ❌\"
    fi
  done
"

# === ATT ===
echo "[ATT] Integration..."
API_STATUS=$(ssh ${REMOTE_USER}@${REMOTE_HOST} "curl -s -o /dev/null -w '%{http_code}' https://api.bybit.com 2>&1")
echo "  Bybit API reachable: ${API_STATUS} ($([ "$API_STATUS" = "200" ] && echo "✅" || echo "❌"))"

BOT_PID=$(ssh ${REMOTE_USER}@${REMOTE_HOST} "pgrep -f trading_bot 2>&1")
if [ -n "$BOT_PID" ]; then
  BOT_PID_LIST=$(echo "$BOT_PID" | tr '\n' ' ' | xargs)
  echo "  Bot PID: ${BOT_PID_LIST} ✅"
else
  echo "  Bot PID: not running ❌"
fi

# === SDD ===
echo "[SDD] Design audit..."
cd "${LOCAL_DIR}"
grep -A50 'set(SOURCES' CMakeLists.txt | grep 'src/' | sed 's/^[[:space:]]*//' > /tmp/_active_sources.txt
echo "  Active source files: $(wc -l < /tmp/_active_sources.txt)"

echo "[SDD] Production signal chain..."
grep -n 'analyze_and_trade\|strategy.analyze\|rl_strategy\|pa_strat\|StatisticalLearner\|VolatilityHarvester' src/main.cpp 2>/dev/null | head -10
