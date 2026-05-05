---
description: Sincronización de Jira y Worklogs (V1.0)
---

# 🎫 Skill: Jira Sync & Worklogs

Este flujo permite al agente llevar el control de tareas en Jira (mediante una interfaz de puente) y sincronizar los registros de trabajo del proyecto.

## 📋 Estructura de Control
El archivo `JIRA_STATUS.md` en la raíz actúa como el "Buffer de Sincronización".

## 🚀 Pasos de Ejecución:
// turbo
1. **Verificar Tareas Pendientes:**
   - Leer `JIRA_STATUS.md` y contrastar con el progreso actual del código.
   
2. **Actualizar Worklogs:**
   - Añadir una nueva entrada en `JIRA_STATUS.md` con la marca de tiempo y las tareas completadas.
   - Formato: `[YYYY-MM-DD HH:MM] - [Componente] - [Acción] - [Tiempo Est.]`

3. **Empujar a API (Opcional):**
   - Si la variable `JIRA_API_TOKEN` está presente, ejecutar `python3 tools/jira_bridge.py --push`.

## 🛠️ Herramienta de Soporte:
`python3 tools/jira_bridge.py [status|update|sync]`
