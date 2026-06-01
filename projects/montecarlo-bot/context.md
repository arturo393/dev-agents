# Context: MonteCarlo Trading Bot

## 1. Metadata
- **Tenant:** Personal Projects
- **Primary Platform:** High-Frequency Trading Bot & Quantitative GA Optimizers
- **Target Language:** Modern C++17, SQLite3, Python3, ONNX Runtime

## 2. Path Mappings
- **Root Directory:** `/Users/arturo/development/lumina/monteCarlo/cpp_bot/`
- **Production Server:** `100.74.53.2`
- **Local Source:** `src/main.cpp`, `src/database_manager.cpp`, `src/bybit_api.cpp`
- **Include Directories:** `include/`
- **Database Path (Prod):** `/home/arturo/monteCarlo/cpp_bot/data/trading_data.db`
- **Weights Path (Prod):** `/home/arturo/monteCarlo/cpp_bot/config/adaptive_weights.json`

## 3. Build & Test Toolchain
- **Local C++ Compile:** `cd cpp_bot && cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j$(nproc)`
- **Unit Tests:** `test_statistical_learner`, `test_portfolio`, `test_latency`
- **Production Restart:** `sudo systemctl restart montecarlo_bot`

## 4. Bounded Conventions
- **Hedge Mode Sizing:** Bybit API place orders must explicitly assign `positionIdx = 1` for Long and `positionIdx = 2` for Short. One-Way index `0` is prohibited for this tenant.
- **Concurrency Locks:** All SQLite operations must be wrapped in `std::lock_guard<std::recursive_mutex> lock(db_mutex);` to prevent deadlocks and races under async pipeline steps.
- **RSI Regime-Adaptive Trigger:** Buying dips on STRONG trends allows lower RSI (35), while WEAK trends require conservative momentum confirmation (45).
- **Small-Account Sizing:** Positions must scale up to at least $5.5 on small accounts (<$100) to exceed Bybit exchange absolute $5 limit.
