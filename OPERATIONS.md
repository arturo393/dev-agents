# ⚙️ SafetyMind Operations: Deployment & Audit

## 🚀 Despliegue de Infraestructura
Todo el stack se orquesta mediante `docker-compose.yml` en la IP Maestra `192.168.1.149`.

### Servicios Core:
- **im-portal**: Next.js App (Puerto 3000)
- **im-prometheus**: Time-series Data (Puerto 9091)
- **im-grafana**: Visualización Avanzada (Puerto 8090)
- **im-node-exporter**: Métricas de Hardware (Puerto 9101)

### Comando de Actualización:
```bash
docker compose up -d --build
```

---

## 🔍 Protocolo de Auditoría
Antes de considerar una tarea "Finalizada", se debe auditar:

1.  **Conectividad de Datos**: ¿El Portal está recibiendo métricas reales de Prometheus?
2.  **Naming Convention**: ¿Todos los contenedores tienen el prefijo `im-`?
3.  **No Direct Port Leaks**: Las APIs internas deben comunicarse vía nombre de servicio Docker (ej: `http://im-prometheus:9090`).
4.  **Audit Links**: Verificar que no existan links rotos a Grafana o dashboards obsoletos.

---

## 🛠️ Troubleshooting Rápido
- **Node Exporter falla**: Verificar conflicto en puerto 9100. Cambiar a 9101.
- **Portal sin datos**: Revisar `next.config.ts` rewrites y nombres de contenedores.
- **Prometheus vacío**: Verificar que el agente Alloy remoto tenga acceso a la IP Maestra puerto 9091.

© 2026 SafetyMind Engineering Operations. 🛡️⚙️
