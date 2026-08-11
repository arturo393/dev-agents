#!/usr/bin/env bash
# Genera .claude/agents/jira-report.md desde .opencode/agents/jira-report.md
#
# Existe porque las dos herramientas nombran distinto las tools del MCP:
#   opencode      jira_jira_get_issue
#   Claude Code   mcp__jira__jira_get_issue
# Editar SIEMPRE la version de .opencode/ y volver a correr esto.
set -euo pipefail
DA="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$DA/.opencode/agents/jira-report.md"
DST="$DA/.claude/agents/jira-report.md"

{
  cat <<'FM'
---
name: jira-report
description: "Sincroniza trabajo de git con Jira y genera resumen ejecutivo. Usar cuando el usuario pida: resumen jira, sync jira, actualiza issue, worklog, briefing, update ejecutivo, estado del proyecto, qué hicimos, cierre de semana."
tools: Bash, Read, Write, Edit, Glob, Grep, mcp__jira__jira_get_issue, mcp__jira__jira_search_issues, mcp__jira__jira_search_issues_in_project, mcp__jira__jira_create_issue, mcp__jira__jira_update_issue, mcp__jira__jira_add_worklog, mcp__jira__jira_add_comment, mcp__jira__jira_transition_issue, mcp__jira__jira_get_transitions, mcp__jira__jira_create_subtask, mcp__jira__jira_weekly_plan, mcp__jira__jira_weekly_update, mcp__jira__jira_bbdd_create, mcp__jira__jira_bbdd_update, mcp__jira__jira_bbdd_append_comment, mcp__jira__sheets_read, mcp__jira__sheets_write, mcp__jira__sheets_metadata, mcp__jira__sheets_analyze, mcp__jira__sheets_find_columns, mcp__jira__confluence_search
---

<!-- GENERADO por scripts/gen-claude-jira-report.sh desde .opencode/agents/jira-report.md -->
<!-- No editar aca: editar la version de .opencode/ y regenerar. -->
FM
  # cuerpo: todo despues del frontmatter, con los nombres de tool traducidos
  awk 'f{print} !f && NR>1 && /^---$/{f=1}' "$SRC" \
    | sed -e 's/\bjira_jira_/mcp__jira__jira_/g' \
          -e 's/\bjira_sheets_/mcp__jira__sheets_/g' \
          -e 's/\bjira_confluence_/mcp__jira__confluence_/g' \
          -e 's/\bjira_bbdd_/mcp__jira__jira_bbdd_/g' \
          -e 's/\*\*jira_\(add_worklog\|add_comment\|create_issue\|update_issue\|get_issue\|search_issues\|transition_issue\|create_subtask\)\*\*/**mcp__jira__jira_\1**/g'
  # Deliberadamente NO se traducen:
  #   jira_link_to_epic -> la doc lo nombra justamente para decir que no se use
  #   jira_key          -> campo de una plantilla YAML, no es una tool
  #   jira_admin        -> nombre de columna de la planilla BBDD
} > "$DST"
echo "generado: $DST ($(wc -l < "$DST") lineas)"
