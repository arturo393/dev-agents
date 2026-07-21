# Software Engineering Foundation

Contenido reutilizable para cualquier proyecto de software.

---

## Code Review Pillars

| Pillar | Checks |
|--------|--------|
| **Mantenibilidad** | Complejidad >50 líneas/4 niveles, dead code, redundancia, nomenclatura |
| **Resiliencia** | Idempotencia, `except: pass`, timeouts, estado inconsistente |
| **Seguridad** | Credenciales, validación inputs, mínimo privilegio |
| **Observabilidad** | `print()` en prod, exit codes, mensajes accionables, CI/CD |
| **Code UX** | El código invita a usarlo o a reescribirlo? (ver abajo) |

### Security por Contexto

No aplicar checklist genérico. Preguntar:

1. **¿Red aislada o con internet?**
   - Aislada → rate limiting + validación inputs + segmentación Docker
   - Internet → HTTPS + auth + RBAC + WAF
2. **¿Quién puede dañar hardware con comando erróneo?**
   - Comandos RF → rate limiting obligatorio
   - Firmware flasheable → control de acceso serial/JTAG
3. **¿Datos sensibles?** (ubicaciones, frecuencias, potencias)
   - Sí → logging mínimo, no exponer en dashboards públicos
   - No → priorizar observabilidad

Regla: **3 controles bien aplicados > 10 checklist items genéricos.**

### Security Audit (Static)

| Language | Detectors |
|----------|-----------|
| PHP | `eval`, `unserialize`, `$_GET/POST/REQUEST` |
| JS/TS | `.innerHTML`, `eval`, `document.write` |
| Python | `subprocess`, `except Exception: pass`, `eval` |
| Shell | `rm $VAR`, `curl \| bash`, `chmod 777` |

Critical/High bloquean. Medium → fix + continuar. Low → registrar.

---

## Testing Methodology (XDD)

| Context | Method |
|---------|--------|
| Define what to build with business | **ATDD** — Criterios de aceptación medibles |
| Document observable behavior | **BDD** — Given-When-Then |
| Design correct function by construction | **TDD** — Red-Green-Refactor |
| Find edge cases | **PBT** — Propiedades + fuzzing |
| Multiple devices/configurations | **DDT** — Tests parametrizados con datos externos |

**Regla de oro:** Sin test no hay cambio en producción. Cada fix incluye su test.

---

## Code UX Principles

### 3-Second Scan
Todo archivo debe tener header de 3 líneas: qué hace, cómo se usa, qué NO hace.

### API por Flujo de Uso
Métodos organizados por orden de uso, no por tipo:
1. Construir → crear instancia
2. Configurar → preparar
3. Controlar → ejecutar
4. Ejecutar paso → usar en loop
5. Consultar → verificar estado
6. Utilidades → helpers

### Nombres-Verb
| Mal (dice CÓMO) | Bien (dice QUÉ) |
|-----------------|-----------------|
| `apply_current_config()` | `start_scan()` |
| `handle_received_data()` | `on_data()` |
| `check_scan_timeout()` | `advance_or_stop()` |
| `get_detection_count()` | `detection_count()` |

### Checklist Universal
| # | Rule |
|---|------|
| 1 | Header de 3 líneas al inicio de cada archivo |
| 2 | API ordenada por flujo de uso |
| 3 | Nombres son verbs sin prefijo `get_`/`set_` |
| 4 | Sin lógica inline en headers (solo firmas) |
| 5 | Archivos < 500 líneas |
| 6 | Parámetros máx 4 por función |

---

## Documentation Principles

| Pattern | Rule |
|---------|------|
| Lead with answer | Decisión o acción primero, contexto después |
| Progressive disclosure | Happy path → detalles → edge cases |
| Chunking | Secciones pequeñas, listas cortas |
| Signposting | Headings, labels, callouts |
| Recognition over recall | Tablas, checklists, templates |

### Reglas
- Cada documento responde una pregunta real
- No crear README genéricos
- No documentar por documentar
- ADR solo para decisiones >30 min de discusión

---

## Resiliencia y Fault Tolerance

### 1. Circuit Breaker (Interruptor Automático)
Si un servicio falla repetidamente → abrir circuito → fallback amigable → recuperación automática.

**Ejemplo:** Pagos fallan → "Pago no disponible, intente después" → servicio se recupera en background.

### 2. Bulkhead (Aislamiento de Fallos)
Cada módulo crítico corre aislado en su propio "compartimento".

**Ejemplo:** Si falla reportes, autenticación y ventas siguen funcionando.

### 3. Observabilidad
- **Logs estructurados** (JSON): trazabilidad de requests entre servicios
- **Métricas**: latencia, tasa de errores, uso de memoria
- **Alertas**: notificar cuando error rate > 0.1%

### 4. Consistencia Eventual
Aceptar que datos entre servicios pueden estar desalineados temporalmente.

**Ejemplo:** Usuario actualiza perfil → otros servicios lo ven 2-5 segundos después.

### 5. Saga Pattern (Transacciones Compensatorias)
Si una operación de varios pasos falla, ejecutar acción compensatoria automática.

**Ejemplo:** Cobro exitoso + reserva fallida → emitir reembolso automático.

### 6. Feature Flags
Desplegar funcionalidades "apagadas" detrás de un interruptor.

**Beneficio:** Si hay bug grave → apagar flag sin redeploy completo.

### 7. Chaos Engineering
Inyectar fallos controlados en producción para verificar resiliencia.

**Herramienta:** Netflix Chaos Monkey.

### 8. Fuzz Testing
Enviar datos aleatorios masivos para encontrar vulnerabilidades.

**Objetivo:** Descubrir agujeros antes que un atacante.

---

## Audit Loop (Convergencia)

Cuando se pida auditar hasta convergencia (zero findings):

1. **Detectar tipo**: Web/Qt/TUI según archivos
2. **Loop** (máx 10 rondas):
   - Aplicar estándar, listar findings con severidad, aplicar fix
   - Condición de parada: `findings_total == 0` o `fixes_applied == 0`
   - Si mismo finding 3 rondas sin fix → marcar "bloqueado"
3. **Reporte final**: rondas ejecutadas, findings por ronda, issues bloqueados
