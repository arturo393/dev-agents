#!/bin/bash
# run_full_audit.sh
# Ejecuta el análisis avanzado en todos los archivos fuente del proyecto.

OUTPUT_FILE="docs/audit_report_$(date +%Y%m%d).md"
mkdir -p docs

echo "🚀 INICIANDO AUDITORÍA INTEGRAL DE C++/TRADING"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

cat <<EOF > "$OUTPUT_FILE"
# Reporte Integral de Auditoría - MonteCarlo Bot
Fecha: $(date)

EOF

for file in cpp_bot/src/*.cpp cpp_bot/src/*.hpp include/*.hpp; do
    if [ -f "$file" ]; then
        echo "Processing $file..."
        echo "## Análisis de $file" >> "$OUTPUT_FILE"
        python3 .agent/skills/cpp_trading_reviewer/scripts/analyzer.py "$file" >> "$OUTPUT_FILE"
        echo -e "\n---\n" >> "$OUTPUT_FILE"
    fi
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Auditoría completada."
echo "📄 Reporte generado en: $OUTPUT_FILE"
