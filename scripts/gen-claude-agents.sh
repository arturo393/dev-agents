#!/usr/bin/env bash
# Genera .claude/agents/<nombre>.md desde .opencode/agents/<nombre>.md
#
# Uso:  scripts/gen-claude-agents.sh            (regenera todos)
#       scripts/gen-claude-agents.sh jira-plan  (solo uno)
# Editar SIEMPRE la version de .opencode/ y volver a correr esto.
#
# Existe porque las dos herramientas nombran distinto las tools del MCP:
#   opencode      jira_jira_get_issue
#   Claude Code   mcp__jira__jira_get_issue
# y porque el frontmatter difiere: opencode declara permisos, Claude declara la lista de tools.
# La `description` NO se duplica: se lee del fuente, que es su unica copia.
set -euo pipefail
DA="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# La lista de tools de cada agente: es lo unico que Claude pide y opencode no.
tools_jira_report="Bash, Read, Write, Edit, Glob, Grep, mcp__jira__jira_get_issue, mcp__jira__jira_search_issues, mcp__jira__jira_search_issues_in_project, mcp__jira__jira_create_issue, mcp__jira__jira_update_issue, mcp__jira__jira_add_worklog, mcp__jira__jira_add_comment, mcp__jira__jira_transition_issue, mcp__jira__jira_get_transitions, mcp__jira__jira_create_subtask, mcp__jira__jira_link_issues, mcp__jira__jira_weekly_plan, mcp__jira__jira_weekly_update, mcp__jira__jira_bbdd_create, mcp__jira__jira_bbdd_update, mcp__jira__jira_bbdd_append_comment, mcp__jira__sheets_read, mcp__jira__sheets_write, mcp__jira__sheets_metadata, mcp__jira__sheets_analyze, mcp__jira__sheets_find_columns, mcp__jira__confluence_search"
tools_jira_plan="Bash, Read, Write, Edit, Glob, Grep, mcp__jira__jira_get_issue, mcp__jira__jira_search_issues, mcp__jira__jira_update_issue, mcp__jira__jira_add_comment, mcp__jira__jira_create_issue, mcp__jira__jira_create_subtask, mcp__jira__jira_get_transitions, mcp__jira__jira_transition_issue, mcp__jira__jira_link_issues"

generar(){
  local nombre="$1" src="$DA/.opencode/agents/$1.md" dst="$DA/.claude/agents/$1.md"
  local var="tools_${nombre//-/_}"
  [ -r "$src" ] || { echo "error: no existe $src" >&2; return 1; }
  [ -n "${!var:-}" ] || { echo "error: falta la lista de tools de $nombre (\$$var)" >&2; return 1; }
  local desc
  desc=$(awk -F': ' '/^description: /{sub(/^description: /,""); print; exit}' "$src")
  [ -n "$desc" ] || { echo "error: $src no declara description" >&2; return 1; }
  {
    printf -- '---\nname: %s\ndescription: %s\ntools: %s\n---\n\n' "$nombre" "$desc" "${!var}"
    printf -- '<!-- GENERADO por scripts/gen-claude-agents.sh desde .opencode/agents/%s.md -->\n' "$nombre"
    printf -- '<!-- No editar aca: editar la version de .opencode/ y regenerar. -->\n'
    # cuerpo: todo despues del frontmatter, con los nombres de tool traducidos
    awk 'f{print} !f && NR>1 && /^---$/{f=1}' "$src" \
      | sed -e 's/\bjira_jira_/mcp__jira__jira_/g' \
            -e 's/\bjira_sheets_/mcp__jira__sheets_/g' \
            -e 's/\bjira_confluence_/mcp__jira__confluence_/g' \
            -e 's/\bjira_bbdd_/mcp__jira__jira_bbdd_/g' \
            -e 's/\*\*jira_\(add_worklog\|add_comment\|create_issue\|update_issue\|get_issue\|search_issues\|transition_issue\|create_subtask\)\*\*/**mcp__jira__jira_\1**/g'
    # Deliberadamente NO se traducen:
    #   jira_link_to_epic -> la doc lo nombra justamente para decir que no se use
    #   jira_key          -> campo de una plantilla YAML, no es una tool
    #   jira_admin        -> nombre de columna de la planilla BBDD
  } > "$dst"
  echo "generado: .claude/agents/$nombre.md ($(wc -l < "$dst") lineas)"
}

if [ $# -gt 0 ]; then
  for a in "$@"; do generar "$a"; done
else
  for f in "$DA"/.opencode/agents/jira-*.md; do generar "$(basename "$f" .md)"; done
fi
