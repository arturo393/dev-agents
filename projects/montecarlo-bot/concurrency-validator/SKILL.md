# Concurrency Validator Agent — Skill Instructions

This agent is specialized in auditing thread-safety, race conditions, and synchronization mechanisms inside the trading engine's C++ code.

## Core Workflows

1. **ThreadSanitizer (TSan) Verification:**
   - Detects if TSan is supported by local or remote compilers.
   - Compiles targets with `-fsanitize=thread` to dynamically intercept race conditions.

2. **Static Locking Audits:**
   - Scans source code for raw thread pools or background threads.
   - Audits `database_manager.cpp` to ensure that standard C++ `lock_guard` mutex allocations protect concurrent reads and writes, protecting SQLite against `SQLITE_BUSY` conflicts.

3. **Shared Globals Check:**
   - Verifies that any static variables shared across multiple ticker evaluations are properly wrapped in `std::atomic<>` or protected by thread locks.

## Command Execution

To execute this agent:
```bash
python3 projects/montecarlo-bot/concurrency-validator/agent.py
```
