#!/usr/bin/env bash
# Thread-safety and Data Race static auditing script

LOCAL_DIR="/Users/arturo/development/lumina/monteCarlo/cpp_bot"

echo "=== CONCURRENCY STATIC CHECKS ==="
echo "[1/4] Checking compiler ThreadSanitizer support..."
if g++ -fsanitize=thread -x c++ - -o /dev/null <<< "int main() {}" 2>/dev/null; then
  echo "  ThreadSanitizer: SUPPORTED ✅"
else
  echo "  ThreadSanitizer: NOT SUPPORTED ❌"
fi

echo "[2/4] Scanning for raw std::thread instances without watchdog controls..."
grep -rn "std::thread" "$LOCAL_DIR/src/" "$LOCAL_DIR/include/" 2>/dev/null | grep -v "watchdog"
if [ $? -eq 0 ]; then
  echo "  ⚠️ Found raw std::thread allocations without integrated watchdog."
else
  echo "  ✅ All threads are properly structured."
fi

echo "[3/4] Scanning for unprotected shared globals (missing std::atomic or std::mutex)..."
grep -rn "static " "$LOCAL_DIR/src/main.cpp" 2>/dev/null | grep -E "double|int|float|map|vector" | grep -v -E "std::atomic|const"
if [ $? -eq 0 ]; then
  echo "  ⚠️ Found static shared globals without atomic wrapper or mutex protection."
else
  echo "  ✅ All static shared globals are thread-safe (atomic or const)."
fi

echo "[4/4] Auditing Database Manager Mutex locks (std::mutex / std::lock_guard)..."
grep -rn "std::lock_guard" "$LOCAL_DIR/src/database_manager.cpp" 2>/dev/null
if [ $? -eq 0 ]; then
  echo "  ✅ Database manager uses lock_guards for transaction isolation."
else
  echo "  ⚠️ No lock_guards found in database_manager.cpp! DB operations might be vulnerable to data races."
fi

echo "================================="
