#!/bin/bash
# run-cleanup.sh — Conocimiento acumulado de limpieza de código muerto
# Aprendizaje: si descubrís un nuevo patrón de dead code, agregalo acá abajo
# ==========================================================================

REMOTE_USER="arturo"
REMOTE_HOST="100.74.53.2"
REMOTE_DIR="/home/arturo/monteCarlo"
LOCAL_DIR="/Users/arturo/development/lumina/monteCarlo"

echo "=== CLEANUP STATIC CHECKS ==="

# === DEAD CODE ===
echo "[SOURCES] Archivos compilados en trading_bot..."
cd "${LOCAL_DIR}/cpp_bot"
grep -A50 'set(SOURCES' CMakeLists.txt | grep 'src/' | sed 's/^[[:space:]]*//' | while read src; do
  basename=$(basename "$src" .cpp)
  # Check if it's referenced in main.cpp (production code path)
  main_refs=$(grep -c "$basename" src/main.cpp 2>/dev/null)
  if [ "$main_refs" -eq 0 ]; then
    # Check if only used in backtest
    backtest_refs=$(grep -c "$basename" src/backtest_simulator.cpp 2>/dev/null)
    echo "  ? $src — solo en backtest ($backtest_refs refs)"
  fi
done

# === BASURA ===
echo "[JUNK] Basura de repo..."
ssh ${REMOTE_USER}@${REMOTE_HOST} "
  echo -n '  .DS_Store: '
  find ${REMOTE_DIR} -name '.DS_Store' -type f 2>/dev/null | wc -l
  echo -n '  __pycache__: '
  find ${REMOTE_DIR} -type d -name '__pycache__' 2>/dev/null | wc -l
  echo -n '  *.bak: '
  find ${REMOTE_DIR} -name '*.bak' -type f 2>/dev/null | wc -l
  echo -n '  *.pyc: '
  find ${REMOTE_DIR} -name '*.pyc' -type f 2>/dev/null | wc -l
"

# === HEADERS HUÉRFANOS ===
echo "[HEADERS] Headers en include/ no referenciados..."
cd "${LOCAL_DIR}/cpp_bot"
for hdr in include/*.hpp; do
  name=$(basename "$hdr")
  refs=$(grep -rn "$name" src/ --include="*.cpp" --include="*.hpp" 2>/dev/null | wc -l)
  if [ "$refs" -eq 0 ]; then
    echo "  ? $hdr — 0 referencias en src/"
  fi
done

# === ARCHIVOS VACÍOS ===
echo "[EMPTY] Archivos vacíos..."
find ${LOCAL_DIR} -type f -empty -not -path '*/.git/*' -not -path '*/__pycache__/*' 2>/dev/null | head -10

echo ""
echo "⚠️  NADA SE ELIMINA SIN CONFIRMACIÓN"
