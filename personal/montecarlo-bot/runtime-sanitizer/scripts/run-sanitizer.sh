#!/bin/bash
# run-sanitizer.sh — Conocimiento acumulado de memory safety y UB
# Aprendizaje: si descubrís un nuevo patrón, agregalo acá abajo
# Última actualización: 2026-06-01
# ============================================================

REMOTE_USER="arturo"
REMOTE_HOST="100.74.53.2"
REMOTE_DIR="/home/arturo/monteCarlo/cpp_bot"
LOCAL_DIR="/Users/arturo/development/lumina/monteCarlo/cpp_bot"

echo "=== SANITIZER STATIC CHECKS ==="

# 1. Tools instalados en servidor
echo "[1/6] Herramientas de sanitización..."
ssh ${REMOTE_USER}@${REMOTE_HOST} "
  echo -n '  valgrind: '; which valgrind 2>&1 || echo 'NOT INSTALLED ❌'
  echo -n '  cppcheck: '; which cppcheck 2>&1 || echo 'NOT INSTALLED ❌'
  echo -n 'clang-tidy: '; which clang-tidy 2>&1 || echo 'NOT INSTALLED ❌'
  echo -n '      g++: '; g++ --version | head -1
"

# 2. Flags de compilación (sanitizers activos?)
echo "[2/6] Flags de compilación..."
grep -E 'CMAKE_CXX_FLAGS|sanitize|fsanitize' "${LOCAL_DIR}/CMakeLists.txt" 2>/dev/null || echo "  No se encontraron flags sanitizer en CMakeLists.txt"

# 3. Patrones de UB en código fuente (conocimiento acumulado)
echo "[3/6] Patrones de undefined behavior conocidos..."
cd "${LOCAL_DIR}"
# Raw pointers sin delete emparejado
echo -n "  new sin delete: "
grep -rn 'new ' src/ --include="*.cpp" | grep -v '//' | grep -v 'delete' | wc -l | tr -d ' '
# memset en objetos no-triviales (clásico UB)
echo -n "  memset en structs no-POD: "
grep -rn 'memset' src/ --include="*.cpp" --include="*.hpp" | wc -l | tr -d ' '
# signed overflow (UB en C++)
echo -n "  posibles signed overflows (INT_MAX+): "
grep -rn 'INT_MAX\|INT_MIN.*+\|overflow' src/ --include="*.cpp" --include="*.hpp" | wc -l | tr -d ' '
# C-style casts peligrosos
echo -n "  C-style casts: "
grep -rn '(int)\|(float)\|(double)' src/ --include="*.cpp" --include="*.hpp" | wc -l | tr -d ' '

# 4. Leaks conocidos (por stacktraces previos)
echo "[4/6] Leaks conocidos (por stacktraces previos)..."
# Buscar patrones de memory leak ya descubiertos
grep -n 'unique_ptr\|shared_ptr\|make_unique' "${LOCAL_DIR}/src/main.cpp" | head -5

# 5. Variables sin inicializar
echo "[5/6] Variables sin inicializar..."
grep -rn 'int \w\+;\|double \w\+;\|bool \w\+;' src/*.cpp --include="*.cpp" | grep -v '= ' | grep -v '//' | head -5

# === PATRONES DESCUBIERTOS DINÁMICAMENTE ===

# 7. Shared globals sin mutex (data race en multi-thread)
# Descubierto: 2026-06-01 — main.cpp tiene static g_daily_pnl, g_last_day sin mutex
echo "[7/8] Shared globals sin mutex..."
grep -rn 'static.*\(double\|int\|float\|long\|bool\|string\)' src/main.cpp | grep -v 'const\|//'

# 8. Threads sin join/detach en destructores
echo "[8/8] Objetos thread potencialmente inseguros..."
grep -rn 'std::thread\|std::jthread' src/ --include="*.cpp" --include="*.hpp" | head -10

# 6. Testing con ASan (si hay binarios compilados)
echo "[6/6] Compilación con ASan..."
ssh ${REMOTE_USER}@${REMOTE_HOST} "
  cd ${REMOTE_DIR}
  if [ -d build_san ]; then
    echo '  build_san/ existe ✅'
    ls build_san/trading_bot 2>/dev/null && echo '  trading_bot (ASan): exists' || echo '  trading_bot (ASan): not compiled'
  else
    echo '  build_san/ no existe — compilar con: cmake -B build_san -DCMAKE_CXX_FLAGS=\"-fsanitize=address,undefined -g -O1\"'
  fi
"
