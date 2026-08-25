#!/usr/bin/env bash
# Genera skills de Hermes desde .claude/agents/<nombre>.md
#
# Uso:  scripts/gen-hermes-agents.sh            (regenera todos)
#       scripts/gen-hermes-agents.sh jira-plan  (solo uno)
#
# En Hermes, cada skill es un directorio bajo ~/.hermes/skills/dev-agents/<nombre>/SKILL.md
# Este script crea los directorios y copia los archivos generados para Claude (ya que el formato es compatible).
set -euo pipefail
DA="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

DEST_DIR="$HOME/.hermes/skills/dev-agents"
mkdir -p "$DEST_DIR"

generar(){
  local nombre="$1" src="$DA/.claude/agents/$1.md"
  [ -r "$src" ] || { echo "error: no existe $src (asegurate de correr gen-claude-agents.sh primero)" >&2; return 1; }
  
  # Crea la carpeta del skill y copia el archivo
  mkdir -p "$DEST_DIR/$nombre"
  cp "$src" "$DEST_DIR/$nombre/SKILL.md"
  
  echo "generado: $DEST_DIR/$nombre/SKILL.md ($(wc -l < "$DEST_DIR/$nombre/SKILL.md") lineas)"
}

if [ $# -gt 0 ]; then
  for a in "$@"; do generar "$a"; done
else
  for f in "$DA"/.claude/agents/*.md; do 
    if [ -f "$f" ]; then
      generar "$(basename "$f" .md)"
    fi
  done
fi
