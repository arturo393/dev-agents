---
description: Despliegue Total On-Premise Master (192.168.1.149)
---

# 🚀 Despliegue en Servidor Local 192.168.1.149

Este flujo sincroniza y despliega automáticamente el Master Node al servidor local de SafetyMind en la red `192.168.1.149`, asegurándose de eliminar servicios conflictivos y compilar la última versión de los contenedores Docker ("Lean UI").

// turbo-all

1. Hacer ping al servidor local para verificar que está accesible
```bash
ping -c 1 192.168.1.149
```

2. Crear las carpetas e inyectar el código vía rsync
```bash
ssh -o StrictHostKeyChecking=no arturo@192.168.1.149 "mkdir -p /opt/safetymind/infrastructure_monitoring"
rsync -avz --exclude '.git' --exclude 'node_modules' --exclude '.next' --exclude 'terraform' -e "ssh -o StrictHostKeyChecking=no" ./ arturo@192.168.1.149:/opt/safetymind/infrastructure_monitoring/
```

3. Destruir servicios legacy nativos y matar procesos zombies
```bash
ssh -o StrictHostKeyChecking=no -t arturo@192.168.1.149 "sudo systemctl stop grafana-server || true; sudo systemctl stop prometheus || true; sudo fuser -k 3000/tcp || true"
```

4. Orquestar los contenedores Docker (Portal + Metrics Analytics)
```bash
ssh -o StrictHostKeyChecking=no -t arturo@192.168.1.149 "cd /opt/safetymind/infrastructure_monitoring && sudo docker compose down -v || true && sudo docker compose up --build -d"
```

5. Confirmar que los puertos de infraestructura quedaron operativos
```bash
ssh -o StrictHostKeyChecking=no arturo@192.168.1.149 "sudo docker ps"
```
