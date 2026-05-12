#!/bin/bash
# run_maintenance_system.sh
# Triggers the system maintenance pipeline on the remote host (requires sudo for systemctl).

REMOTE_USER="arturo"
REMOTE_HOST="100.74.53.2"
PASSWORD="Admin.123"

echo "🔧 Iniciando Mantenimiento de Sistema en $REMOTE_HOST..."
# maintenance_system.sh usually needs to stop/start services, so it might need sudo or be run as root.
# The local maintenance_system.sh says "Runs as Root".
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" "echo $PASSWORD | sudo -S bash /home/arturo/monteCarlo/tools/maintenance_system.sh"
