---
name: SafetyMind Full Sync
description: End-of-session sync flow that aligns Git, Jira, and documentation for SafetyMind projects.
---

# Skill: SafetyMind Full Sync (Git + Jira + Docs)

Este flujo es el comando definitivo para cerrar una sesión de trabajo, asegurando que el código, la gestión (Jira) y la documentación estén 100% alineados.

## 🚀 Pasos de Ejecución:
// turbo
1. **Sincronizar Jira (Worklogs):**
   - Ejecutar `@[/jira-sync]`.
   - Asegurar que `JIRA_STATUS.md` tiene las últimas tareas.

2. **Actualizar Historial (Docs):**
   - Inyectar las nuevas funcionalidades en `CHANGELOG.md`.
   - Verificar que el `README.md` refleja los cambios de arquitectura.

3. **Operación de Repositorio (Git Ops):**
   - Ejecutar `@[/git-ops]`.
   - Generar un commit semántico que mencione los IDs de Jira afectados.
   
4. **Resumen de Sesión:**
   - Generar un reporte final para el usuario con el Hash del commit y el estado de Jira.

## 🛠️ Comando Sugerido:
`python3 tools/sync_master.py --full`
