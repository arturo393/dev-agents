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

for file in src/*.cpp include/*.hpp; do
    if [ -f "$file" ]; then
        echo "Processing $file..."
        echo "## Análisis de $file" >> "$OUTPUT_FILE"
        python3 "$(dirname "$0")/analyzer.py" "$file" >> "$OUTPUT_FILE"
        echo -e "\n---\n" >> "$OUTPUT_FILE"
    fi
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Auditoría completada."
echo "📄 Reporte generado en: $OUTPUT_FILE"
