---
name: Check Server Logs
description: Fetches and reviews the trading bot logs from the production server (192.168.1.149).
---

# Check Server Logs

This skill is used to quickly retrieve and analyze the log outputs from the production server.

## Usage

You can use the helper script `fetch_logs.sh` provided in the `scripts/` directory to fetch the logs without having to remember the SSH password or path.

1.  **To get the default (last 100 lines of bot_production.log):**
    ```bash
    ./.agent/skills/check_server_logs/scripts/fetch_logs.sh
    ```

2.  **To get a specific number of lines:**
    ```bash
    ./.agent/skills/check_server_logs/scripts/fetch_logs.sh 500
    ```

3.  **To specify a different log file (e.g., trading_bot.log):**
    ```bash
    ./.agent/skills/check_server_logs/scripts/fetch_logs.sh 50 trading_bot.log
    ```

## Analysis Guide

After fetching the logs, analyze them to look for:
- 📋 `POSICIONES ABIERTAS:` to monitor current holdings.
- 💰 `BALANCE:` updates to track PnL and Equity.
- ❌ Errors, JSON parsing warnings, or crashes.
- 🧠 Activity from the GA, Markov, and RL models.
- ⚙️ Order executions (Hedge Mode status, positionIdx, TP/SL hits).

**Important:** Read the output of the script carefully to determine the real state of the bot on the production machine.
