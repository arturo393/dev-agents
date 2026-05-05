# 🚀 Skill: Master Production Provisioner (SafetyMind Cloud)

Este flujo es el mando supremo para el despliegue de infraestructura y aplicación en GCP. Garantiza estabilidad nominal (99.9% uptime).

## 📋 Pre-Requisitos:
- Acceso SSH a la Master IP Real (**`34.45.4.76`**).
- Build verificado localmente.

## 🚀 Pasos de Ejecución Master:
// turbo-all
1. **Certificación de Build Industrial:**
   - `npm run build` en la carpeta `/portal`. No se permite despliegue si hay lints o errores de tipo.
   
2. **Sincronización Transversal (Full Sync):**
   - Ejecutar `@[/full-sync]`. Actualiza Git, Jira y Changelog de una sola vez.

3. **Provisión de Infraestructura (Cloud Apply):**
   - `terraform apply -auto-approve` para consolidar Firewall y VMS.

4. **Hot-Deploy en Master Node:**
   - Conectar y ejecutar: `docker-compose up -d --build portal`.

5. **Certificación de Salud (Smoke Test):**
   - Verificar conectividad: `curl -I http://34.45.4.76:3000`.
   - Si responde **200 OK**, la misión ha sido un éxito.

## 🛠️ Herramienta de Soporte:
`./scripts/deploy_cloud_v3.sh`
