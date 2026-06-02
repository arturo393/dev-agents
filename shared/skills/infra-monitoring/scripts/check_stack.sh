#!/bin/bash
REMOTE_USER="arturo"
REMOTE_HOST="192.168.1.149"
PASSWORD="${SSH_PASSWORD:?SSH_PASSWORD env var required}"

echo "=========================================="
echo "  Infra Stack Check - $(date)"
echo "=========================================="

echo ""
echo "=== Docker Containers ==="
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'"

echo ""
echo "=== Portal Health ==="
curl -sf http://192.168.1.149:3000/api/health 2>/dev/null && echo " (HTTP 200)" || echo "❌ FAILED"

echo ""
echo "=== Prometheus Targets ==="
curl -sf http://192.168.1.149:9091/api/v1/targets 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"Active: {len([t for t in d['data']['activeTargets'] if t['health']=='up'])}/{len(d['data']['activeTargets'])}\")" 2>/dev/null || echo "❌ FAILED"

echo ""
echo "=== Grafana Health ==="
curl -sf http://192.168.1.149:8090/api/health 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"DB: {d['database']}, Version: {d['version']}\")" 2>/dev/null || echo "❌ FAILED"
