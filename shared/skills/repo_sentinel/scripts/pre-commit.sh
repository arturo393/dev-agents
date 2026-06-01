#!/bin/bash
# pre-commit hook — runs repo sentinel before each commit
DIR="$(cd "$(dirname "$0")/../../.." && pwd)"
bash "$DIR/.agents/skills/repo_sentinel/scripts/repo_sentinel.sh"
if [ $? -ne 0 ]; then
  echo "❌ Repo Sentinel checks failed. Commit blocked."
  echo "   To bypass: git commit --no-verify"
  exit 1
fi
exit 0
