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
  | Asunto   | Solicitud Recibida: {nombre}   |
  | SLA      | 24 horas hábiles               |
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

## Feature: Wizard Frontend — Paso 1 Identificación

### Escenario: Todos los campos de infraestructura son obligatorios
```gherkin
Given que el usuario está en el Paso 1 (Identificación)
When solo completa nombre de empresa y correo
But NO selecciona VPN, ni distribución de red, ni ubicación de servidor
Then el botón "Siguiente" debe estar DESHABILITADO
```

### Escenario: Avance exitoso al Paso 2
```gherkin
Given que el usuario completa TODOS los campos del Paso 1
When presiona "Siguiente"
Then el wizard avanza al Paso 2 (Inventario y Riesgos)
And el ProgressBar muestra 66%
```

## Feature: Wizard Frontend — Paso 2 Inventario

### Escenario: Selector de toma fija con 2 opciones
```gherkin
Given que el usuario registra una cámara
When abre el selector "¿Toma Fija?"
Then debe ver las opciones "Sí, es fija" y "No, es móvil"
```

### Escenario: 6 factores de riesgo seleccionables por cámara
```gherkin
Given que el usuario está configurando una cámara
When revisa los riesgos disponibles
Then debe ver estos 6 factores:
  | Uso de EPP          |
  | Hombre-Máquina      |
  | Zonas Peligro       |
  | Cargas Susp.        |
  | Línea de Fuego      |
  | Cond. Críticas      |
```

### Escenario: 5 cámaras válidas permite validar
```gherkin
Given que el usuario ha subido 5 cámaras con foto, marca y modelo
When presiona "Validar"
Then el wizard avanza al Paso 3 (Validación Final)
And el ProgressBar muestra 100%
```

## Feature: Wizard Frontend — Paso 3 Validación

### Escenario: SLA visible en pantalla de confirmación
```gherkin
Given que el usuario está en el Paso 3
Then debe ver el panel con "SLA Garantizado: Respuesta en 1 Día"
And debe ver el contador de "Cámaras Válidas: X de 7"
And debe ver "Revisión: Manual + IA"
```

### Escenario: Error de conexión en envío
```gherkin
Given que el usuario completa los 3 pasos
When presiona "Solicitar Diagnóstico"
And el servidor NO responde (timeout)
Then el sistema muestra mensaje de error "Error de conexión con el servidor"
```

## Feature: Consola HITL Frontend — Editor

### Escenario: Acceso con código de respaldo
```gherkin
Given que un técnico accede a /admin/review
When ingresa "DAS2026" como passcode de respaldo
And presiona "Entrar"
Then accede al panel con notificación de "Acceso verificado"
```

### Escenario: Código inválido muestra error
```gherkin
Given que un técnico intenta acceder
When ingresa un código incorrecto
Then ve el mensaje "Código de acceso inválido"
```

### Escenario: Selección de reporte en cola
```gherkin
Given que el técnico está autenticado en la consola
When hace clic en un reporte de la cola lateral
Then se muestra el detalle en el panel central:
  | Evidencia: miniaturas de las 7 cámaras |
  | Infraestructura: VPN y servidor         |
  | Risk Evidence: factores detectados      |
```

### Escenario: Editor de veredicto y score
```gherkin
Given que el admin tiene un reporte seleccionado
When cambia el veredicto de "VERDE" a "ROJO"
And modifica el score de 92 a 35
Then el estado del reporte cambia a DRAFT
And el color del score cambia según el veredicto
```

### Escenario: Reporte aprobado no permite edición
```gherkin
Given un reporte en estado APPROVED
When el admin intenta modificar veredicto, score o notas
Then todos los campos están DESHABILITADOS
```

## Feature: Tema Claro/Oscuro

### Escenario: Alternar tema desde la barra de navegación
```gherkin
Given que el usuario está en el wizard
When presiona el botón de sol/luna en la navbar
Then el tema alterna entre dark y light
And el cambio persiste al recargar la página
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

### Backend (Agent)
- `agent/tests/test_das_pipeline.py` → 21 tests (100% pass) — cubre DB, LangGraph state, templates y escenarios BDD del backend.
```bash
cd agent && python3 -m pytest tests/ -v
```

### Frontend (Propuesto)
- `frontend/` con Vitest + React Testing Library — cubre helpers, hooks, componentes (atoms/molecules/organisms), páginas y E2E.
```bash
cd frontend && npx vitest run
```

---
© 2026 SafetyMind Quality Assurance.
