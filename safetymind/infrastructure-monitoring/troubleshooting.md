---
description: Troubleshooting guide for SafetyMind Monitoring (Master & Edge)
---

# 🩺 Auditoría de Servicios Stack (Prometheus, Grafana, Portal)

Comprueba la salud del triplete de Docker en el servidor remoto para asegurar que no hay cuellos de botella y que los tres componentes de monitorización estén en pie (status "Up") y en los puertos correctos.

// turbo-all

1. Verificar el estado del engine de Docker y que los contenedores existan
```bash
ssh -o StrictHostKeyChecking=no arturo@192.168.1.149 "sudo docker ps -a | grep safetymind"
```

2. Listar todos los puertos abiertos en estado LISTENING ligados a nuestra pila
```bash
ssh -o StrictHostKeyChecking=no arturo@192.168.1.149 "sudo ss -tulpn | awk '/:(3000|3001|9090)/'"
```

3. Obtener los últimos logs (10 lineas) del Portal en Next.js para detectar errores de renderizado
```bash
ssh -o StrictHostKeyChecking=no arturo@192.168.1.149 "sudo docker logs --tail 20 safetymind-portal-v3"
```

4. Asegurarse que Grafana está aprovisionado y arrancado
```bash
ssh -o StrictHostKeyChecking=no arturo@192.168.1.149 "sudo docker logs --tail 10 safetymind-grafana"
```
