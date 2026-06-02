#!/bin/bash
# review_module.sh
# Realiza un análisis heurístico de patrones peligrosos en C++ y Trading.

FILE=$1

if [ -z "$FILE" ]; then
    echo "Uso: ./review_module.sh <archivo.cpp>"
    exit 1
fi

echo "🔍 AUDITANDO: $FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Chequeo de C++ Clásico (Punteros RAW)
echo "🧠 [C++] Buscando punteros raw o posibles fugas de memoria..."
grep -n "new " "$FILE" | grep -v "std::make_unique" | awk -F: '{print "   ⚠️  Línea " $1 ": Uso de 'new' detectado. ¿Usar smart pointer?"}'
grep -n "delete " "$FILE" | awk -F: '{print "   ⚠️  Línea " $1 ": Uso de 'delete' detectado."}'

# 2. Chequeo de Trading (Precisión)
echo "💰 [Trading] Buscando omisión de redondeo en cantidades..."
if grep -q "qty =" "$FILE" && ! grep -q "round_qty" "$FILE"; then
    echo "   ❌ ALERTA: Se asigna 'qty' pero no se ve llamada a 'round_qty' (Bybit precision error potential)."
fi

# 3. Chequeo de Robustez (Try/Catch)
echo "🛡️ [Robustez] Verificando manejo de excepciones en API calls..."
if grep -q "api." "$FILE" && ! grep -q "try {" "$FILE"; then
    echo "   ⚠️  ADVERTENCIA: Llamadas a la API detectadas fuera de un bloque try-catch."
fi

# 4. Chequeo de Hardcoding
echo "⚙️ [Config] Buscando valores hardcoded críticos..."
grep -n "leverage = [0-9]" "$FILE" | awk -F: '{print "   ⚠️  Línea " $1 ": Apalancamiento hardcoded detectado."}'
grep -nE "0\.0[0-9]{1}" "$FILE" | grep "size" | awk -F: '{print "   ℹ️  Línea " $1 ": Tamaño de posición fijo detectado."}'

# 5. Seguridad Financiera (TP/SL)
echo "🎯 [Riesgo] Verificando existencia de SL forzoso..."
if grep -q "Buy" "$FILE" && ! grep -q "stop_loss" "$FILE"; then
    echo "   🚫 CRÍTICO: Se detectó lógica de compra sin referencia obvia a Stop Loss."
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Auditoría heurística finalizada para $FILE"
echo "Nota: Este script no reemplaza una revisión manual detallada por el agente Antigravity."
