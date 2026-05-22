#!/bin/bash
# Repo Sentinel — pre-commit health check for infrastructure_monitoring
set -o pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

PASS=0
FAIL=0
WARN=0

check() {
  local label="$1" status="$2" msg="$3"
  if [ "$status" = "PASS" ]; then
    echo -e "  ${GREEN}✓${NC} $label"
    PASS=$((PASS+1))
  elif [ "$status" = "FAIL" ]; then
    echo -e "  ${RED}✗${NC} $label"
    [ -n "$msg" ] && echo -e "    ${RED}$msg${NC}"
    FAIL=$((FAIL+1))
  else
    echo -e "  ${YELLOW}⚠${NC} $label"
    [ -n "$msg" ] && echo -e "    ${YELLOW}$msg${NC}"
    WARN=$((WARN+1))
  fi
}

echo -e "\n${CYAN}══════════════════════════════════════${NC}"
echo -e "${CYAN}  REPO SENTINEL — infrastructure_monitoring${NC}"
echo -e "${CYAN}  $(date)${NC}"
echo -e "${CYAN}══════════════════════════════════════${NC}\n"

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || { echo "Not a git repository"; exit 1; }
cd "$ROOT" || exit 1

# ── 1. Hardcoded credentials ──────────────────────────────────
echo -e "${CYAN}[1] Hardcoded Credentials${NC}"
FOUND=$(grep -rn --include="*.sh" --include="*.py" -lE "Admin\.123|[Pp]assword\s*=\s*['\"][^'\"]+['\"]" .agents/skills .agents/workflows 2>/dev/null | grep -v repo_sentinel | head -5)
if [ -n "$FOUND" ]; then
  check "SSH password 'Admin.123' found in scripts" "WARN" "$FOUND"
else
  check "No hardcoded credentials" "PASS" ""
fi

# ── 2. IP consistency ─────────────────────────────────────────
echo -e "\n${CYAN}[2] IP Consistency${NC}"
IP_34=$(grep -rn '34\.[0-9]\+\.[0-9]\+\.[0-9]\+' .agents docker-compose.yml configs \
  --include="*.sh" --include="*.yml" --include="*.yaml" --include="*.md" --include="*.py" 2>/dev/null | grep -v "34\.45\.4\.76" | head -5)
if [ -n "$IP_34" ]; then
  check "Legacy GCP IPs (34.x.x.x) detected" "FAIL" "$(echo "$IP_34" | head -3)"
else
  check "No banned (34.x.x.x) IPs" "PASS" ""
fi

# ── 3. File permissions ───────────────────────────────────────
echo -e "\n${CYAN}[3] File Permissions${NC}"
MISSING_X=$(find .agents/skills -name '*.sh' ! -executable 2>/dev/null)
if [ -n "$MISSING_X" ]; then
  check "Non-executable scripts" "FAIL" "$(echo "$MISSING_X" | tr '\n' ' ')"
else
  check "All scripts executable" "PASS" ""
fi

# ── 4. Skills without SKILL.md ────────────────────────────────
echo -e "\n${CYAN}[4] Skills Integrity${NC}"
SKILL_FAIL=0
shopt -s nullglob
for d in .agents/skills/*/; do
  name=$(basename "$d")
  [ "$name" = "repo_sentinel" ] && continue
  if [ ! -f "$d/SKILL.md" ]; then
    check "Missing SKILL.md in $name" "FAIL" ""
    SKILL_FAIL=1
  fi
done
shopt -u nullglob
if [ "$SKILL_FAIL" = "0" ]; then
  check "All skills have SKILL.md" "PASS" ""
fi

# ── 5. Docker compose validation ──────────────────────────────
echo -e "\n${CYAN}[5] Docker Compose${NC}"
if command -v docker &>/dev/null && docker compose version &>/dev/null; then
  docker compose -f docker-compose.yml config -q 2>/dev/null
  if [ $? -eq 0 ]; then
    check "docker-compose.yml syntax valid" "PASS" ""
  else
    check "docker-compose.yml syntax" "FAIL" "Invalid syntax (run 'docker compose config' to debug)"
  fi
else
  check "docker-compose.yml (skipped — Docker not available)" "WARN" ""
fi

# ── 6. Orphan workflows ───────────────────────────────────────
echo -e "\n${CYAN}[6] Workflow Consistency${NC}"
HUNTER=$(find .agents/workflows -name '*.yaml' -exec grep -l 'hunter' {} \; 2>/dev/null)
if [ -z "$HUNTER" ]; then
  check "No hunter/sales workflows" "PASS" ""
else
  check "Sales workflows detected" "WARN" "$(echo "$HUNTER")"
fi

# ── 7. Git ignore ─────────────────────────────────────────────
echo -e "\n${CYAN}[7] .gitignore${NC}"
if [ -f .gitignore ]; then
  check ".gitignore exists" "PASS" ""
else
  check ".gitignore missing" "FAIL" ""
fi

# ── Summary ───────────────────────────────────────────────────
echo -e "\n${CYAN}══════════════════════════════════════${NC}"
echo -e "  ${GREEN}$PASS passed${NC}, ${RED}$FAIL failed${NC}, ${YELLOW}$WARN warnings${NC}"
echo -e "${CYAN}══════════════════════════════════════${NC}\n"

if [ "$FAIL" -gt 0 ]; then
  exit 1
fi
exit 0
