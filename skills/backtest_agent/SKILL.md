---
name: Backtest Agent
description: Orchestrates the downloading of historical data and runs the Genetic Algorithm optimization on the remote server.
---

# Backtest Agent

This skill is meant to automate the nightly execution of the Genetic Algorithm optimizer.

## Usage

Use the provided script to start the backtest pipeline on the production host (192.168.1.149). This will run the `ga_optimizer` tool located on the server.

```bash
./.agent/skills/backtest_agent/scripts/run_backtest.sh
```

If you need to change symbols, duration, or population size, you can edit the script parameters or run the commands manually.
