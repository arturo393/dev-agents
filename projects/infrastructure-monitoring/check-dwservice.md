---
description: Auditoría y Verificación de Estado (Túnel DWService)
---

# 🛡️ Auditoría de Conectividad Base DWService

Este flujo comprueba que el agente en la sombra de DWService siga ejecutándose sin errores en el nodo Maestro. Mide que el instalador interactivo o el demonio hayan persistido correctamemte.

// turbo-all

1. Comprobar si el proceso core dwagent se encuentra persistente en memoria RAM
```bash
ssh -o StrictHostKeyChecking=no arturo@192.168.1.149 "ps aux | awk '/dwagent/ && !/awk/'"
```

2. Confirmar los archivos de instalación
```bash
ssh -o StrictHostKeyChecking=no arturo@192.168.1.149 "ls -lah /usr/share/dwagent/ || echo 'DWService no instalado correctamente'"
```

3. Verificar las llamadas de red externas del puente DWService
```bash
ssh -o StrictHostKeyChecking=no arturo@192.168.1.149 "sudo ssh -V || true; netstat -tupan 2>/dev/null | grep dwagent || ss -tupan 2>/dev/null | awk '/dwagent/' || echo 'No ports found'"
```
