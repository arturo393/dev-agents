#!/bin/bash
REMOTE_USER="arturo"
REMOTE_HOST="192.168.1.149"
PASSWORD="Admin.123"

echo "=========================================="
echo "  DWService Tunnel Check - $(date)"
echo "=========================================="

echo ""
echo "=== DWAgent Process ==="
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" "ps aux | awk '/dwagent/ && !/awk/'"

echo ""
echo "=== Installation Files ==="
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" "ls -lah /usr/share/dwagent/ 2>/dev/null || echo '❌ DWService not installed'"
