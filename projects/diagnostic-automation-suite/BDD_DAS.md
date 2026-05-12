---
description: Behavior Driven Development (BDD) Scenarios for SafetyMind DAS — Aligned with Source of Truth
---

# 🛡️ BDD: Escenarios de Aceptación DAS (V4.3)

> Alineado con: `Autodiagnóstico de Viabilidad Técnica (Seguros Bolívar).pdf`,
> `Proceso semi automatización del diagnóstico.pdf` y `ruta_de_validacion.jpeg`

---

## Feature: Formulario de Autodiagnóstico

### Escenario: Validación completa del Paso 1
```gherkin
Given que el usuario está en el Paso 1 del Wizard
When ingresa nombre de empresa y correo válido
And selecciona "FortiClient" como VPN
But NO selecciona distribución de red ni ubicación de servidor
Then el botón "Siguiente" debe estar DESHABILITADO
And el usuario NO puede avanzar al Paso 2
```

### Escenario: VPN tipo "Otra" requiere especificación
```gherkin
Given que el usuario selecciona "Otra" en Cliente VPN
Then debe aparecer un campo de texto obligatorio "¿Cuál?"
And el botón "Siguiente" se deshabilita hasta que lo complete
```

### Escenario: Campos separados de Marca y Modelo
```gherkin
Given que el usuario está en el Paso 2
When sube una foto de cámara
Then debe ver DOS campos separados: "Marca" y "Modelo"
And ambos son requeridos para contar como cámara válida
```

### Escenario: 4 opciones de administrador de cámara
```gherkin
Given que el usuario registra una cámara
When abre el selector "¿Quién administra?"
Then debe ver las opciones:
  | Informática interna       |
  | Patrimonial / Seguridad   |
  | Proveedor externo         |
  | No lo sé / Otra área      |
```

### Escenario: Mínimo 5 cámaras válidas para avanzar
```gherkin
Given que el usuario ha subido 4 cámaras con foto, marca y modelo
When intenta avanzar al Paso 3
Then el botón "Validar" debe estar DESHABILITADO
And el contador debe mostrar "4 / 7 CÁMARAS"
```

### Escenario: Envío exitoso con confirmación y SLA
```gherkin
Given el usuario completa los 3 pasos con 5+ cámaras válidas
When presiona "Solicitar Diagnóstico"
Then el sistema muestra "Recibido"
And menciona que recibirá un correo de confirmación
And el panel de SLA muestra "Respuesta en 1 Día"
```

---

## Feature: Correo de Acuse de Recibo (ACK)

### Escenario: ACK inmediato al cliente
```gherkin
Given que el formulario se envía correctamente
When el backend procesa los datos
Then envía un email al correo del cliente con:
  | Campo    | Valor                          |
  | Asunto   | 🛡️ Solicitud Recibida: {nombre} |
  | SLA      | 24 horas hábiles               |
  | Motor IA | Guardian Prime                 |
```

---

## Feature: Validación Administrativa (HITL)

### Escenario: Login en consola de revisión
```gherkin
Given que un técnico accede a /admin/review
When ingresa el código operativo "DAS2026"
Then accede al panel de validación
```

### Escenario: Aprobar reporte y enviar resultado
```gherkin
Given un reporte en estado PENDING
When el admin presiona "Aprobar"
Then el estado cambia a APPROVED
And se envía el reporte técnico final al cliente
And el Audit Trace muestra quién aprobó y cuándo
```

### Escenario: Rechazar reporte
```gherkin
Given un reporte en estado PENDING
When el admin presiona "Rechazar"
Then el estado cambia a REJECTED
And se envía un email al cliente informando "No Compatible"
And el botón muestra "DIAGNÓSTICO RECHAZADO" en rojo
```

### Escenario: Solicitar ajustes
```gherkin
Given un reporte en estado PENDING
When el admin presiona "Ajustes"
Then el estado cambia a ADJUSTMENTS_REQUIRED
And se envía un email al cliente informando "Ajustes Pendientes"
And el botón muestra "AJUSTES SOLICITADOS" en amarillo
```

---

## Feature: Semáforo de Viabilidad

### Escenario: Veredicto según score
```gherkin
Given los scores de las cámaras y la infraestructura
When el motor de IA calcula el viability_score
Then aplica la siguiente tabla:

  | Score    | Veredicto | Significado           | Acción                                      |
  | > 85     | VERDE     | Infraestructura Óptima | Proceder al pago de licencia               |
  | 60 - 84  | AMARILLO  | Ajustes Pendientes    | Corregir posición de cámaras o red          |
  | < 60     | ROJO      | No Compatible         | Reemplazar hardware o cámaras defectuosas   |
```

---

## ✅ Tests Automatizados

Todos estos escenarios están materializados en:
- `agent/tests/test_das_pipeline.py` → 21 tests (100% pass)

```bash
cd agent && python3 -m pytest tests/ -v
```

---
© 2026 SafetyMind Quality Assurance.
