#!/bin/bash
echo "=========================================="
echo "  SAFETYMIND FULL INFRASTRUCTURE AUDIT"
echo "  $(date)"
echo "=========================================="

DIR="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo ">>> STACK CHECK"
bash "$DIR/check_stack.sh"

echo ""
echo ">>> SYSTEM RESOURCES"
bash "$DIR/check_system.sh"

echo ""
echo ">>> DWSERVICE TUNNEL"
bash "$DIR/check_dwservice.sh"

echo ""
echo "=========================================="
echo "  AUDIT COMPLETE"
echo "=========================================="
