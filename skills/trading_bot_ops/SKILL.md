---
name: Trading Bot Ops
description: Unified operations for the MonteCarlo trading bot — process health, logs, PnL, wallet, maintenance.
---

# Trading Bot Ops

This skill merges the functionality of Bot Functional Auditor, Check Server Logs, and Database Auditor into a single unified interface.

## Usage

### Full Bot Audit (all checks)
```bash
./.agent/skills/trading_bot_ops/scripts/full_bot_audit.sh
```

## What It Checks
- **Process:** C++ binary status (systemctl)
- **Signals:** Signal frequency from Ensemble (Markov/RL) in last hour
- **Risk:** Current correlation levels and time-exits
- **Logs:** Last 50 lines of bot_production.log
- **Maintenance:** Last maintenance pipeline execution
- **PnL:** Grouped by exit reason + last 5 trades
- **RAM:** Current memory usage
