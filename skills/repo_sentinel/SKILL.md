---
name: Repo Sentinel
description: Pre-commit health checker for the infrastructure_monitoring repository — credentials, IPs, permissions, consistency.
---

# Repo Sentinel

This skill runs automated checks on the repository itself to catch common issues before they reach production.

## Usage

```bash
# Run manually
./.agent/skills/repo_sentinel/scripts/repo_sentinel.sh

# Or install as pre-commit hook
ln -sf ../../.agents/skills/repo_sentinel/scripts/pre-commit.sh .git/hooks/pre-commit
```

## What It Checks

| # | Check | Severity |
|---|-------|----------|
| 1 | Hardcoded credentials (`Admin.123`, tokens) | 🔴 Warning |
| 2 | Banned legacy IPs (`34.x.x.x`) | 🔴 FAIL |
| 3 | Scripts without executable permission | 🔴 FAIL |
| 4 | Skills missing `SKILL.md` | 🔴 FAIL |
| 5 | Docker compose syntax | 🔴 FAIL |
| 6 | Unrelated workflows (sales, docs) | 🟡 Warning |
| 7 | Missing `.gitignore` | 🔴 FAIL |
