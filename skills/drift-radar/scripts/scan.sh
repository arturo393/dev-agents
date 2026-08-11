#!/usr/bin/env bash
# Detecta codigo duplicado y divergido entre los repos de ~/uqomm. SOLO LECTURA.
# Uso: scan.sh [raiz]        (por defecto /home/arturo/uqomm)
# NO escribe nada en ningun repo: solo imprime el informe.
set -uo pipefail

ROOT="${1:-/home/arturo/uqomm}"
cd "$ROOT" || { echo "no existe $ROOT" >&2; exit 1; }

EXCLUDE='/(\.git|node_modules|Drivers|Middlewares|build|_deps|target|\.next|venv|\.venv|dist|Debug|Release|catch2-src)/'

# Lista de fuentes propias: path<TAB>basename<TAB>md5
sources() {
  find . -type f \( -name '*.c' -o -name '*.cpp' -o -name '*.h' -o -name '*.hpp' \) 2>/dev/null \
    | grep -vE "$EXCLUDE" \
    | while read -r f; do printf '%s\t%s\t%s\n' "$f" "$(basename "$f")" "$(md5sum "$f" | cut -d' ' -f1)"; done
}

TMP=$(mktemp); trap 'rm -f "$TMP"' EXIT
sources > "$TMP"

repo_of() { echo "$1" | cut -d/ -f2; }

echo "=============================================================="
echo " RADAR DE DERIVA  ·  $ROOT"
echo " $(wc -l < "$TMP") archivos fuente propios analizados"
echo "=============================================================="

echo
echo "## 1. DIVERGIDOS — mismo nombre, contenido distinto, en >1 repo"
echo "   (bugfix en uno NO llega a los otros)"
echo
cut -f2 "$TMP" | sort | uniq -d | while read -r base; do
  rows=$(awk -F'\t' -v b="$base" '$2==b' "$TMP")
  nrepos=$(echo "$rows" | cut -f1 | cut -d/ -f2 | sort -u | wc -l)
  nhash=$(echo "$rows" | cut -f3 | sort -u | wc -l)
  [ "$nrepos" -lt 2 ] && continue
  [ "$nhash" -lt 2 ] && continue
  printf '  %-28s %s versiones distintas en %s repos\n' "$base" "$nhash" "$nrepos"
  echo "$rows" | while IFS=$'\t' read -r p _ h; do
    printf '      %-8s %-6s %s\n' "${h:0:8}" "$(wc -l < "$p")L" "$p"
  done
done

echo
echo "## 2. AUN IDENTICOS — misma copia en >1 repo"
echo "   (todavia se unifican barato; van a divergir)"
echo
cut -f2 "$TMP" | sort | uniq -d | while read -r base; do
  rows=$(awk -F'\t' -v b="$base" '$2==b' "$TMP")
  nrepos=$(echo "$rows" | cut -f1 | cut -d/ -f2 | sort -u | wc -l)
  nhash=$(echo "$rows" | cut -f3 | sort -u | wc -l)
  [ "$nrepos" -lt 2 ] && continue
  [ "$nhash" -ne 1 ] && continue
  printf '  %-28s identico en %s ubicaciones / %s repos\n' "$base" "$(echo "$rows" | wc -l)" "$nrepos"
done

echo
echo "## 3. CRC-16 — implementaciones independientes del mismo algoritmo"
echo "   (solo definiciones con el polinomio 0x1021; se excluyen tests y usos)"
echo
grep -rlE '0x1021|0X1021' --include='*.c' --include='*.cpp' --include='*.h' --include='*.hpp' . 2>/dev/null \
  | grep -vE "$EXCLUDE" | grep -vE '/tests?/|test_' \
  | while read -r f; do
      # una definicion tiene el polinomio Y un bucle de desplazamiento
      if grep -qE '<<= *1|<< *1|>>= *1' "$f"; then
        printf '  %-26s %s\n' "$(repo_of "$f")" "$f"
      fi
    done | sort -u
n=$(grep -rlE '0x1021|0X1021' --include='*.c' --include='*.cpp' --include='*.h' --include='*.hpp' . 2>/dev/null \
    | grep -vE "$EXCLUDE" | grep -vE '/tests?/|test_' \
    | while read -r f; do grep -qE '<<= *1|<< *1|>>= *1' "$f" && echo x; done | wc -l)
echo "  -> $n implementaciones del mismo CRC-16/XMODEM"

echo
echo "## 4. OPCODES fuera del contrato"
echo "   contrato: sw-diagnosticoremoto/contracts/tg-protocol.json"
echo
CONTRACT="sw-diagnosticoremoto/contracts/tg-protocol.json"
if [ -f "$CONTRACT" ]; then
  echo "  contrato presente ($(wc -l < "$CONTRACT")L). Declaraciones de opcode fuera de el:"
  grep -rlniE 'CMD_[A-Z_]+ *=|#define +CMD_' --include='*.h' --include='*.hpp' --include='*.go' --include='*.rs' --include='*.py' . 2>/dev/null \
    | grep -vE "$EXCLUDE" | sed 's/^/    /' | head -20
else
  echo "  *** el contrato NO esta en $CONTRACT ***"
fi

echo
echo "## 5. jira-report — las dos variantes del mismo agente"
echo "   (.claude/ se GENERA desde .opencode/; si difieren en estructura, regenerar)"
echo
DA=/home/arturo/.config/opencode/dev-agents
if [ -f "$DA/.opencode/agents/jira-report.md" ] && [ -f "$DA/.claude/agents/jira-report.md" ]; then
  a=$(grep -cE '^#{1,4} ' "$DA/.opencode/agents/jira-report.md")
  b=$(grep -cE '^#{1,4} ' "$DA/.claude/agents/jira-report.md")
  if [ "$a" -eq "$b" ]; then
    echo "  OK — misma estructura ($a secciones en las dos)"
  else
    echo "  *** DERIVARON: .opencode tiene $a secciones, .claude tiene $b ***"
    echo "      correr: $DA/scripts/gen-claude-jira-report.sh"
  fi
else
  echo "  falta alguna de las dos variantes"
fi

echo
echo "=============================================================="
echo " Fin. Nada fue modificado."
echo "=============================================================="
