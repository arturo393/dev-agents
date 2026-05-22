#!/bin/bash
REMOTE_USER="arturo"
REMOTE_HOST="192.168.1.149"
PASSWORD="Admin.123"

echo "=========================================="
echo "  System Resources - $(date)"
echo "=========================================="

echo ""
echo "=== Disk ==="
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" "df -h / | tail -1 | awk '{print \"Used: \" \$3 \" / \" \$2 \" (\" \$5 \")\"}'"

echo ""
echo "=== RAM ==="
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" "free -h | grep Mem | awk '{print \"Used: \" \$3 \" / \" \$2}'"

echo ""
echo "=== Load / Uptime ==="
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" "uptime | awk -F'up ' '{print \$2}'"

echo ""
echo "=== Docker Disk Usage ==="
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" "docker system df 2>/dev/null | head -5"

echo ""
echo "=== Docker Prune Dry-Run (reclaimable) ==="
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" "docker system df 2>/dev/null | awk '/Build Cache/{print \"Build cache: \" \$4 \" reclaimable\"}'"
