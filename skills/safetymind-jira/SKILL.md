---
name: safetymind-jira
description: >
  Acceder a la instancia de Jira de SafetyMind (safetymind-team-ogsoj2pu.atlassian.net,
  proyectos IM y O2). Usar SOLO cuando se necesite consultar/crear/actualizar issues
  o registrar worklogs de proyectos SafetyMind (infrastructure_monitoring, ORBIT-2, etc.).
  IMPORTANTE: el MCP jira central (uqomm-teams) NO accede a esta instancia — usar el
  script safetymind_jira.py con las credenciales del cabinet-test.
---

# SafetyMind Jira — Instancia safetymind

## Contexto

- **Instancia:** `https://safetymind-team-ogsoj2pu.atlassian.net`
- **Credenciales:** `JIRA_EMAIL` / `JIRA_TOKEN` en `safetymind-cabinet-test/gabinete/jira/.env`
- **Script:** `safetymind-cabinet-test/gabinete/jira/safetymind_jira.py`
- **Proyectos:** `IM` (Infrastructure monitoring) · `O2` (ORBIT-2) · etc.
- Usuario: `arturo@safetymind.ai` (distinto al de uqomm).

## Regla crítica

El MCP jira central (sw-jiraanalysis) apunta a `uqomm-teams.atlassian.net` con
`arturo@uqomm.com` — **es otra instancia, no accede a SafetyMind**. No usar las
herramientas `jira_*` para proyectos de SafetyMind; usar este script.

## Uso

```bash
cd /home/arturo/safetymind/safetymind-cabinet-test/gabinete/jira

# Buscar issues (JQL sin LIMIT — se controla con maxResults interno, default 20)
python3 safetymind_jira.py search "project = IM ORDER BY created DESC"
python3 safetymind_jira.py search "project = IM AND status = 'Tareas por hacer'"

# Ver un issue + tiempo registrado
python3 safetymind_jira.py get IM-123

# Crear tarea
python3 safetymind_jira.py create IM "Summary" "Descripción" Tarea

# Registrar worklog (timeSpent: 30m, 2h, 1h 30m)
python3 safetymind_jira.py worklog IM-123 "2h" "Comentario del trabajo"
```

## Buenas prácticas

1. **Nunca inventes issues ni worklogs.** Si no existe un issue claramente
   relacionado, reportalo y proponé crearlo con el summary correcto.
2. **Antes de crear**, buscá si ya existe (duplicados).
3. **Worklogs temáticos**: dividí la sesión en bloques lógicos (~1h cada uno),
   uno por tipo de trabajo, con comentario descriptivo.
4. **JQL**: no usar `LIMIT` (es palabra reservada); la cantidad se controla
   con el parámetro `maxResults` del script.
5. Descripción en texto plano (el script la convierte a ADF).

## Verificación

```bash
python3 safetymind_jira.py get <KEY>   # confirmar timespent y estado
```
