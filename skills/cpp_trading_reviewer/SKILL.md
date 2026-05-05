---
name: CPP Trading Reviewer v2.0
description: Auditor avanzado de código C++ y sistemas de trading algorítmico con análisis estático heurístico.
---

# CPP Trading Reviewer v2.0

Este agente avanzado realiza auditorías profundas del bot MonteCarlo, enfocándose en la intersección entre la seguridad financiera y la eficiencia de sistemas de baja latencia.

## Capacidades de Análisis

### 1. Auditoría de Seguridad Financiera (Financial Integrity)
- **Check de Redondeo:** Verifica que el `lotSizeFilter` y `priceFilter` de Bybit sean respetados mediante llamadas a `round_qty` y `round_price`.
- **Análisis de Margin Leakage:** Busca órdenes que puedan quedar abiertas sin Stop Loss o posiciones "fantasmas" no registradas en DB.
- **Circuit Breaker Check:** Asegura que el bot monitorea el capital total y detiene operaciones ante drawdowns configurados.

### 2. Auditoría Técnica de C++ (Engineering Excellence)
- **Modern C++ Standards:** Escanea el uso de `new/delete` y sugiere migración a smart pointers (`std::unique_ptr`).
- **RAII Patterns:** Verifica que los bloqueos de Mutex y conexiones de DB usen el patrón *Resource Acquisition Is Initialization*.
- **Copy Optimization:** Detecta pasos por valor de contenedores grandes (vectores, mapas) y sugiere `const&`.

### 3. Robustez de Sistemas Distributed
- **API Error Handling:** Verifica que todas las llamadas de red estén envueltas en bloques `try-catch` específicos.
- **Database Integrity:** Asegura que las transacciones SQL sean atómicas cuando sea necesario.

## Herramientas Incluidas

### `analyzer.py`
Un motor de análisis estático basado en Python que genera reportes en formato Markdown con severidades:
- **Critical:** Riesgo inmediato de pérdida de capital o crash.
- **High:** Bug lógico severo o mala gestión de memoria.
- **Medium/Low:** Mejoras de performance o estilo de código.

### `full_audit.sh`
Script maestro que ejecuta el analizador en todo el proyecto y genera un reporte consolidado.

## Cómo Ejecutar una Auditoría Completa

```bash
./.agent/skills/cpp_trading_reviewer/scripts/run_full_audit.sh
```

## Checklist Premium de Trading

- [ ] **Slippage Control:** ¿El bot usa precios límite o mercado? ¿Se considera el slippage?
- [ ] **Order Overlap:** ¿Se verifica si ya hay una orden pendiente antes de enviar una nueva?
- [ ] **Rate Limiting:** ¿Se maneja el error `Too Many Requests` de Bybit?
- [ ] **Timeouts:** ¿Las llamadas síncronas tienen un timeout para evitar el bloqueo del main loop?
