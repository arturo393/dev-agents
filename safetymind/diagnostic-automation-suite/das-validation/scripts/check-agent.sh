#!/bin/bash
# Check DAS agent health
set -euo pipefail

HOST="100.74.53.2"
AGENT_URL="http://${HOST}:8002"

echo "=== Agent Health Check ==="

# Health endpoint
echo -n "GET /health: "
curl -s "${AGENT_URL}/health" 2>/dev/null || echo "UNREACHABLE"
echo ""

# Last 20 lines of agent logs
echo "=== Agent Logs (last 20) ==="
ssh "arturo@${HOST}" "docker logs das-agent --tail 20" 2>/dev/null || echo "Log fetch failed"
