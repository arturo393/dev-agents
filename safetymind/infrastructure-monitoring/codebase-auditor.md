---
description: Auditoría de Incoherencias SafetyMind V2.1 (IPs, Puertos, Simuladores)
---

# 🛡️ Skill: Auditoría de Incoherencias (SafetyMind V3.1)

Este flujo permite asegurar la coherencia absoluta de la producción multi-cliente y purgar cualquier rastro de la era legacy o prototipos.

## 🚀 Pasos de Ejecución Master:
// turbo-all
1. **Validación de Identidad de Red (IPs):**
   - Buscar la IP obsoleta `34.132.200.128` (Demo) o `34.70.213.25` (Legacy).
   - Asegurar que la referencia maestra sea la nueva IP On-Premise: **`192.168.1.149`**.
   - `grep -rE "34\.132\.200\.128|34\.70\.213\.25|34\.45\.4\.76" .`
   
2. **Auditoría de Despliegue (Docker vs OS):**
   - Verificar que no haya comandos `apt install` para Grafana/Prometheus en los scripts de despliegue modernos.
   - Todo debe estar orquestado vía `docker-compose.yml`.

3. **Integridad Multi-Tenant (Provisioning):**
   - 21. Validar que `portal/public/data/clients.json` existe y tiene el formato correcto.
   - Asegurar que el API de Proyectos (`api/projects/route.ts`) apunte a la ruta de datos correcta.

4. **Verificación de Puertos de Control:**
   - Asegurar que no hay leaks del puerto `:3000` (Grafana) que no pasen por el puerto `80` (Nginx Proxy).
   - `grep -r ":3000" portal/src/app` (Solo links internos iframe son válidos).

5. **Auditoría UX Industrial (Watchdog V3):**
   - Invocar `@[/ux-a11y-agent]` para validar integridad de layout (No solapes, Premium Dark Mode).

6. **Certificación de "Efecto WOW" (Art Director):**
   - Invocar `@[/ux-director-agent]` para confirmar el uso de Negros Profundos (#000000) y Amarillo Industrial (#ffed01).

7. **Reporte de Producción:**
   - Generar tabla de remediación final y ejecutar `git push` de limpieza.

