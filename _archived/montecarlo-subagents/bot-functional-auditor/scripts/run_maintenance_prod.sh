#!/bin/bash
# run_maintenance_prod.sh
# Triggers the production maintenance pipeline on the remote host.

REMOTE_USER="arturo"
REMOTE_HOST="100.74.53.2"
PASSWORD="${SSH_PASSWORD:?SSH_PASSWORD env var required}"

echo "🚀 Iniciando Pipeline de Mantenimiento Producción en $REMOTE_HOST..."
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" "bash /home/arturo/monteCarlo/tools/maintenance_prod.sh"
