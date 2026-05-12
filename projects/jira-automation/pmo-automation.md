---
description: SafetyMind PMO Automation Expert - Reviews jira-automation backend and portal
---

# 🏭 SafetyMind PMO Automation Expert (V1.0)

Este documento define al experto que evalúa el sistema `jira-automation` (API + Portal) en `192.168.1.149`.

---

## 🎯 Alcance de Revisión

| Componente | Path | Puerto |
|------------|------|--------|
| FastAPI Backend | `jira-automation/api/` | 8000 |
| Next.js Portal | `jira-automation/portal/` | 8501 |
| Core Logic | `jira-automation/src/` | - |

---

## ⚡ Checklist de Auditoría

### Backend (Python/FastAPI)

| Check | Estándar | Evidencia |
|-------|---------|----------|
| CORS Security | Solo orígenes autorizados en `ALLOWED_ORIGINS` | `api/main.py:20-25` |
| Environment | Sin `.env` en repo | `.gitignore` verification |
| Error Handling | HTTPException con status codes | `api/main.py` |
| Path Traversal | Validación de filename en downloads | `api/main.py:119-121` |
| Logging | Sin exposición de secrets | Revisar `print()` statements |

### Frontend (React/Next.js)

Seguir los estándares de `.agents/workflows/safetymind-guardian-prime.md`

| Check | Estándar |
|-------|----------|
| Color Tokens | `#ffed01`, `#000000`, `#0a0a0a`, `#1e2532` |
| Hit Targets | ≥ 48px |
| Focus Ring | `#ffed01`, 3px |
| Contrast | 7:1 minimum |
| Zero-Hardcode | Sin credentials en código |

---

## 🛡️ Protocolo Sentinel (V1.0)

### 1. API Integration Check
- `NEXT_PUBLIC_API_URL` debe apuntar al backend correcto
- CORS debe incluir el dominio del portal

### 2. Empty States
- Verificar que no hay mensajes predictivos cuando no hay proyecto seleccionado
- Usar: "Seleccione un proyecto de Jira Cloud"

### 3. Hardcoded Values
- Prohibido: Credenciales, keys, tokens, nombres de personas
- Permitido: Endpoints, paths absolutos, tokens de diseño

---

## 📊 Matriz de Hallazgos

| Nivel | Criteria | Ejemplo |
|-------|----------|--------|
| **P1** | Security breach, blocking | API key expuesta, CORS abierto |
| **P2** | Design violation | Color token incorrecto, target < 44px |
| **P3** | Code quality | Typo, optimización menor |

---

## 🔧 Herramientas de Debug

```bash
# Health check
curl http://192.168.1.149:8000/health

# List projects
curl http://192.168.1.149:8000/api/projects

# Portal status
curl -s -o /dev/null -w "%{http_code}" http://192.168.1.149:8501
```

---

## 📝 Formato de Reporte

```markdown
## Auditoría jira-automation - [Fecha]

### Resumen
| P1 | P2 | P3 |
|----|----|----|
| X  | X  | X  |

### Hallazgos
[Lista por nivel]

### Recomendaciones
[Acciones priorizadas]
```

---

© 2026 SafetyMind Elite Engineering.