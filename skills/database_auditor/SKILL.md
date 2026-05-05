---
name: Database Auditor
description: Connects to the SQLite database on the remote server and extracts trading outcomes to generate a PnL report.
---

# Database Auditor

This skill connects to the `trading_data.db` database on the production server, extracts recent trades and PnL, and outputs real-time statistics.

## Usage

Run the script to fetch the latest aggregate stats and recent trades.

```bash
./.agent/skills/database_auditor/scripts/audit_pnl.sh
```

You can then format the output into an artifact markdown report for the user.
