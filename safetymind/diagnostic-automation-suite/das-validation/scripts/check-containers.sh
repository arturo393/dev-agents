#!/bin/bash
# Check Docker container status
set -euo pipefail

HOST="100.74.53.2"

echo "=== Docker Containers on ${HOST} ==="
ssh "arturo@${HOST}" "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'" 2>/dev/null || echo "SSH failed"

echo ""
echo "=== All containers (including stopped) ==="
ssh "arturo@${HOST}" "docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'" 2>/dev/null || echo "SSH failed"
