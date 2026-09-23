---
name: spec-first
description: Especificación antes de código para una app, módulo o funcionalidad NUEVA. Redacta un borrador de spec con supuestos explícitos, lo itera hasta que el usuario lo aprueba, y recién entonces implementa lo documentado y nada más. Usar cuando el usuario pida: crear una app, un módulo, un servicio, un driver o una funcionalidad nueva, "armemos X", "empecemos el proyecto Y", o pasar un prototipo a producto. NO usar para: arreglar un bug, un script de una vez, documentación, un refactor sin cambio de comportamiento.
---

# Spec-first

Qué hace: no se escribe código de algo nuevo sin una spec que el usuario **aprobó explícitamente**.
Cómo se usa: fase 0 (nivel) → 1 (borrador) → 2 (aprobación) → 3 (implementación), en ese orden.
Qué NO hace: no aplica a bugs (van con un test que reproduce primero, XDD) ni a scripts o docs.

## Fase 0 — ¿Aplica, y a qué nivel?

| Pedido | Qué corresponde |
|---|---|
| Bug, script de una vez, doc, refactor sin cambio de comportamiento | **No aplica.** Seguir el flujo normal |
| Ya existe una spec aprobada que lo cubre | Ir a la fase 3 con esa spec |
| Algo nuevo para **validar** (hardware, idea, mercado) | Spec de **prototipo** |
| Algo nuevo que va a producción, a un cliente o lo mantendrá otro | Spec de **producto** |
| Un prototipo que pasa a producto | **Puerta de promoción**, abajo |

Si no está claro qué nivel es, proponer uno en el borrador y dejar que el usuario lo corrija.

Antes de redactar, leer lo que ya existe: `docs/`, `CLAUDE.md`, specs anteriores, y el código que
se puede reutilizar (`software-foundation.md` → Method Before Diagnosis). Una spec que propone
reescribir lo que ya funciona tiene que decir por qué.

## Fase 1 — Borrador con supuestos, no cuestionario

No abrir con una lista de preguntas. Redactar el borrador completo y marcar cada supuesto:

> **[SUPUESTO]** el equipo reporta cada 60 s por LoRa — corregir si no

Preguntar **solo** lo que no se puede suponer sin riesgo: una decisión de negocio, un contrato con
otro equipo, algo que dañe hardware si se adivina mal. Todo lo demás va como supuesto.

**Firmware:** se permite un smoke test mínimo contra el hardware **antes** de la spec
(`firmware-foundation.md` → Regla de Oro): `AT` → `OK`, sin RTOS, sin DMA. Lo que confirma o refuta
va a la spec como hecho medido. Es la única excepción a «nada de código antes de la aprobación», y
ese código se descarta o queda como test; no es la base de la implementación.

### Spec de prototipo (media página)

```markdown
# <nombre> — prototipo
- **Qué se valida:** la pregunta que este prototipo responde, y cómo se mide la respuesta
- **Qué se reutiliza:** código, drivers o herramientas existentes, con su ruta
- **Qué deuda se acepta:** lo que queda mal a propósito, y por qué no importa ahora
- **Fuera de alcance:** lo que NO se hace aunque parezca obvio
- **Criterio de terminado:** el resultado que cierra la validación
```

### Spec de producto (completa)

```markdown
# <nombre>
1. Objetivo y usuario — para qué y para quién
2. Arquitectura y flujo de datos — bloques con nombre real, qué viaja entre ellos (diagrama)
3. Modelos y estructuras de datos — esquemas, tipos, contratos con otros repos
4. Reglas de negocio y restricciones
5. Casos límite y manejo de errores — qué pasa si falla la red, el dato llega vacío, el HW no responde
6. Verificación — qué test o medición prueba cada requisito
7. Fuera de alcance
```

Dónde vive: `docs/specs/<nombre>.md` en el repo (o `spec.md` en la raíz si es una app nueva). Se
commitea junto con el código, no en un chat.

## Fase 2 — Aprobación

Iterar el borrador con el usuario hasta un **sí explícito**. «Se ve bien» sobre un borrador con
supuestos sin resolver no es aprobación: listar los supuestos que siguen abiertos y preguntar si
quedan como están.

Registrar la aprobación en la spec: `Aprobada: <fecha> por <usuario>`.

## Fase 3 — Implementación

- Implementar **solo** lo que la spec dice. Nada de funciones "de paso" que no estén escritas.
- Si aparece un callejón sin salida o un supuesto resulta falso: **parar**, proponer el cambio a la
  spec, y seguir cuando el usuario lo aprueba. La spec se actualiza en el mismo commit que el
  código que cambia por ella.
- Cada requisito termina con la verificación que la spec le asignó.

## Puerta de promoción: prototipo → producto

El riesgo de tener dos niveles es que un prototipo llegue a producción sin pasar nunca por la
spec completa. Por eso:

1. Un prototipo **no** se entrega a un cliente, a terreno ni a otro equipo sin la spec de producto
   aprobada.
2. La spec de producto parte de lo que el prototipo **midió**: reemplaza supuestos por hechos.
3. La deuda que el prototipo aceptó se lista una por una: cada ítem se paga o se declara como
   decisión, con el motivo y la observación que la haría cambiar.

Si se detecta código de prototipo en producción sin spec de producto, decirlo como hallazgo; no
escribir la spec a posteriori en silencio como si hubiera existido.
