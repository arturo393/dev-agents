# Strategy Reviewer Agent — Skill Instructions

This agent is specialized in performing quantitative audits of the trading bot's strategy parameters, active risk filters, and regime-based weights.

## Core Workflows

1. **Filter Throughput Audit:**
   - Reads the live log file (`bot_production.log`) on the server.
   - Calculates the exact throughput and blockage percentage of each filter gate (Statistical Learner, Convexity Filter, Correlation, Spread).
   - Generates alerts if any filter gate blocks a disproportionate percentage of profitable setups ("death by a thousand filters").

2. **Regime Weight Alignment:**
   - Compares the configured weights in `adaptive_weights.json` with the actual realized PnL and Win Rate inside `trade_outcomes` grouped by regime.
   - Identifies if the bot is losing money in a specific regime due to aggressive trend weights when it should be using mean-reversion, prompting parameter recalibration.

3. **Risk-Safety Verification:**
   - Validates that the C++ `RiskManager` has active protections against database win rate percentage representation mismatches and small-account execution limitations.

## Command Execution

To execute this agent:
```bash
python3 projects/montecarlo-bot/strategy-reviewer/agent.py
```
