---
description: Gestión de Git y Commits (V1.0)
---

# 📦 Skill: Git Operations (SafetyMind Sync)

Este agente permite al sistema subir cambios, crear ramas y mantener el repositorio actualizado de forma autónoma.

## 🚀 Pasos de Ejecución:
// turbo
1. **Verificar Status:**
   - `git status` para detectar cambios no commiteados.
   
2. **Generar Commit Semántico:**
   - Detectar la naturaleza del cambio (Feature, Fix, Refactor).
   - Generar un mensaje que siga el formato: `feat(portal): initial next.js setup` o `fix(dashboards): update yellow color`.
   
3. **Commit & Push:**
   - `git add .`
   - `git commit -m "[MENSAJE]"`
   - `git push origin [RAMA_ACTUAL]`

## 🛠️ Herramienta de Soporte:
`python3 tools/git_helper.py --commit [mensaje]`
