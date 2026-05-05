---
description: Reconciliación Mensual y Generación de Dashboard (Python Engine)
---
Este flujo de trabajo automatiza la validación de datos, el análisis financiero mediante el motor Python y la actualización de la visualización.

1. Validar integridad del CSV de transacciones.
// turbo
2. Ejecutar limpieza y análisis: `make clean analyze`
// turbo
3. Generar reporte Markdown.
4. Sincronizar reporte con Trello (si está configurado).
5. Abrir `dashboard.html` en el navegador para revisión visual.
