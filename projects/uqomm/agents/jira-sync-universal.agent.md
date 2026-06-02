---
name: jira-sync-universal
description: "Sincroniza actividad entre Git, Jira, y un archivo de sync local para cualquier proyecto. Triggers: sincroniza con jira, sync jira, sync con [archivo], actualiza [ID-XXXX], jira sync, worklog."
tools: [read, edit, grep, terminal, jira_get_issue, jira_add_worklog, jira_add_comment, jira_create_issue, jira_search_issues, jira_transition_issue, jira_update_issue]
user-invocable: true
---

# Jira Sync Universal — Agente de sincronización Git ↔ Jira

> **Propósito**: Mantener alineado el trabajo real (commits, archivos) con Jira (worklogs, estados, comentarios) para cualquier proyecto, usando un archivo de sync como fuente de configuración.

## Parámetros esperados del usuario

| Parámetro | Obligatorio | Descripción |
|-----------|:----------:|-------------|
| `sync_file` | ✅ | Ruta al archivo de sync (ej. `docs/AGENT_SYNC.md`, `jira/ID-1374-sync.md`) |
| `issue_key` | ✅ | Clave Jira a sincronizar (ej. `ID-1374`, `ID-1373`) |
| `work_desc` | ❌ | Descripción del trabajo realizado (si no se infiere de git) |
| `hours` | ❌ | Horas trabajadas (si no se infieren) |

## Flujo de ejecución

### Paso 0 — Leer configuración desde el archivo de sync

Leer `sync_file`. Extraer de sus metadatos:

- **Jira parent**: clave del issue padre (ej. `ID-1374`)
- **Epic**: clave de la épica (ej. `ID-1291`)
- **Repositorio(s)**: rutas dentro del workspace
- **Rama activa**: branch principal de trabajo
- **Subtareas conocidas**: tabla de `| Key | Resumen | Estado |` si existe
- **Formato de worklogs**: sección de worklogs previos

> Si el archivo no tiene estos metadatos → inferirlos consultando Jira y git.

### Paso 1 — Recopilar trabajo reciente

```bash
cd <repo> && git log --oneline -15 && git status --short
```

Clasificar commits no sincronizados:
- `feat:` / `fix:` / `docs:` / `chore:` → bloques de trabajo
- Agrupar commits relacionados en bloques temáticos

### Paso 2 — Consultar estado Jira actual

```
jira_get_issue("<issue_key>")
```

Extraer: estado, subtareas (si es padre), tiempo registrado, asignado, vencimiento.

Si el issue es tipo `Epic` o tiene subtareas → obtener la lista completa de hijos.

### Paso 3 — Clasificar trabajo nuevo contra subtareas

Para cada bloque de trabajo:

| Situación | Acción |
|-----------|--------|
| Encaja en subtarea existente **En curso** | Agregar worklog a esa subtarea |
| Encaja en subtarea **Finalizada** | Crear nueva subtarea (no reabrir) |
| Trabajo nuevo sin categoría | Crear subtarea bajo el issue padre |
| Trabajo directamente sobre el issue padre | Worklog al issue principal |

### Paso 4 — Crear subtareas si es necesario

```
jira_create_issue(
  project="<extraído del issue_key>",
  issuetype="Subtarea",
  parentKey="<issue_key>",
  summary="<título conciso>",
  description="<componentes, archivos, decisiones>"
)
```

### Paso 5 — Registrar worklogs

```
jira_add_worklog(
  issueKey="<ID-XXXX>",
  timeSpent="<Xh Ym>",
  comment="<descripción en español: qué, cómo, resultado>"
)
```

Reglas:
- 1 worklog por bloque temático (no mezclar áreas)
- Si el usuario no especificó horas → estimar del volumen de commits
- Usar lenguaje del archivo de sync (español si está en español)

### Paso 6 — Actualizar archivo de sync

Editar `sync_file`:
1. Si tiene tabla de subtareas → actualizar estados
2. Agregar entradas de worklog en la tabla correspondiente
3. Actualizar sección TL;DR o estado general si existe
4. Agregar nueva sesión con fecha y resumen

### Paso 7 — Resumen final

Producir tabla con:
- Worklogs agregados (issue, tiempo, descripción)
- Subtareas creadas (si las hay)
- Archivo sync actualizado
- Commits sincronizados

---

## Reglas universales

- **Nunca inventar worklogs** — solo de trabajo real confirmado por git o por el usuario.
- **Nunca hacer force push ni amend** a menos que el usuario lo pida explícitamente.
- **Leer antes de escribir** — siempre GET el issue y el archivo antes de modificar.
- **Un worklog por bloque temático** — no granularidad excesiva (cada commit) ni demasiado vaga ("varias cosas").
- **Idioma del worklog = idioma del archivo de sync** (español por defecto para proyectos UQOMM).
- **Zona horaria**: `America/Santiago` (`-0400`).
- **Formato de horas**: `Xh Ym` (ej. `2h 30m`, `45m`, `1h`).

---

## Ejemplo de sync file mínimo

```markdown
# Jira Sync — ID-XXXX: Título del issue

> Epic: ID-YYYY — Nombre de la épica
> Proyecto: I+D+S (`ID`)
> Rama activa: `nombre-rama`
> Repo: `path/dentro/del/workspace`

## Subtareas

| Key | Resumen | Estado |
|-----|---------|--------|
| ID-XXXX | ... | 🔄 En curso |

## Worklogs

| Fecha | Issue | Tiempo | Descripción |
|-------|-------|--------|-------------|
| ... | ... | ... | ... |
```

---

## Diferencias con otros agentes de sync

| Característica | `jira-1374-sync` (viejo) | `jira-sync` (DRSMON) | **`jira-sync-universal`** |
|---|---|---|---|
| Proyecto | Hardcodeado a ID-1374 | Hardcodeado a DRSMON | **Lo lee del sync file** |
| Sync file | Fijo `jira/ID-1374-sync.md` | No usa sync file | **Parámetro `sync_file`** |
| Worklogs | Manual | Via PowerShell | **Automático desde git** |
| Subtareas | Lista hardcodeada | No maneja | **Consulta Jira real** |
| Idioma | Español | Inglés | **Auto-detecta del sync file** |
| Creación de issues | ✅ | ❌ | ✅ |
