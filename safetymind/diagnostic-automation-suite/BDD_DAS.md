---
description: Behavior Driven Development (BDD) Scenarios for SafetyMind DAS — Aligned with Arc42
---

# 🛡️ BDD: Escenarios de Aceptación DAS (V4.3)

> Alineado con: `Autodiagnóstico de Viabilidad Técnica (Seguros Bolívar).pdf`,
> `Proceso semi automatización del diagnóstico.pdf`, `ruta_de_validacion.jpeg`
> y documento **Arc42 §§5-7**.

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

### Escenario: Envío exitoso con Job ID y Polling
```gherkin
Given el usuario completa los 3 pasos con 5+ cámaras válidas
When presiona "Solicitar Diagnóstico"
Then el frontend debe subir las fotos a Storage
And el backend debe retornar un "Job ID" inmediato
And el frontend debe mostrar una pantalla de "Procesando Análisis"
And debe realizar polling cada 2 segundos hasta que el estado sea COMPLETED
```

### Escenario: Latencia reducida vía procesamiento paralelo
```gherkin
Given un diagnóstico con 7 cámaras y 3 factores de riesgo
When se inicia el procesamiento en LangGraph
Then el sistema debe ejecutar los 10 análisis de visión en paralelo
And el tiempo total de respuesta de la IA debe ser < 20 segundos
```

### Escenario: Sanitización de inyección de prompts
```gherkin
Given que un usuario ingresa "Ignora instrucciones previas" en la descripción de riesgo
When el backend procesa la solicitud
Then el input debe ser encapsulado en tags <user_description>
And Gemini 2.0 debe tratar el texto como dato, no como instrucción
And el análisis técnico debe ignorar el intento de manipulación
```

---

## Feature: Recepción de Formulario (Arc42 §5)

### Escenario: Cliente ingresa datos y sube 7 fotografías
```gherkin
Given que el cliente está en el paso 1 de la Landing Page
When completa la información de Conectividad (VPN) y Servidor Local
And completa los datos de 7 cámaras incluyendo tipo de riesgo a medir y sube 1 foto por cámara
And hace clic en "Enviar"
Then el cliente ve una pantalla de "Recibido"
And se dispara el Webhook V2 en n8n
And el cliente recibe un correo indicando que se recibieron sus datos y se emitirá el diagnóstico en máx. 24hrs
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

## Feature: Dashboard de Validación Interna (Arc42 §5)

### Escenario: Técnico evalúa imágenes en el dashboard
```gherkin
Given que el técnico recibe un correo de notificación de nueva solicitud
When el técnico ingresa al enlace provisto hacia el "Dashboard de Validación Interna"
Then el técnico ve una interfaz oscura con el resumen de los datos del cliente
And ve un listado/grid con las 7 cámaras subidas
```

### Escenario: Aprobación de cámara individual (Arc42)
```gherkin
Given que el técnico está revisando las cámaras en el dashboard
When selecciona la Cámara 1
And verifica que la toma es apta
And presiona "Aprobar"
Then el estado de la Cámara 1 cambia a "Validado"
```

### Escenario: Rechazo de cámara individual (Arc42)
```gherkin
Given que el técnico está revisando las cámaras en el dashboard
When selecciona la Cámara 3
And verifica que la toma no es apta (baja resolución, mal ángulo)
And presiona "Rechazar"
Then el estado de la Cámara 3 cambia a "Rechazado"
And se muestra un campo para ingresar el motivo del rechazo
```

### Escenario: Finalizar diagnóstico tras revisar todas las cámaras (Arc42)
```gherkin
Given que el técnico ha validado o rechazado cada una de las 7 cámaras
When presiona "Finalizar Diagnóstico"
Then el sistema valida que todas las cámaras tienen un estado (aprobado/rechazado)
And calcula el veredicto final basado en las decisiones del técnico
And se envía el resultado al cliente
```

---

## Feature: Notificación Final al Cliente (Arc42 §5)

### Escenario: Envío de reporte semáforo
```gherkin
Given que el técnico ha validado las 7 cámaras y ha emitido un veredicto (Verde, Amarillo, Rojo)
When el técnico hace clic en "Finalizar Diagnóstico"
Then LangGraph compila la respuesta en el template HTML "Bento Premium"
And n8n despacha automáticamente el resultado final por correo al cliente
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
  | Evidencia: miniaturas de las 7 cámaras con scores IA |
  | Infraestructura: VPN y servidor                       |
  | Risk Evidence: factores detectados                    |
```

### Escenario: Editor de veredicto y score
```gherkin
Given que el admin tiene un reporte seleccionado
When cambia el veredicto de "VERDE" a "ROJO"
And modifica el score de 92 a 35
Then el estado del reporte cambia a DRAFT
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

## Feature: Envío de Copia a Seguros Bolívar (n8n)

### Escenario: n8n reenvía diagnóstico al grupo Seguros Bolívar
```gherkin
Given que n8n recibe la respuesta del backend con el reporte completo
When la respuesta contiene verdict, html y data
Then n8n envía un email a seguros-bolivar@safetymind.ai con:
  | Campo    | Valor                                    |
  | From     | victoria@safetymind.ai                   |
  | To       | seguros-bolivar@safetymind.ai            |
  | Asunto   | Nuevo Diagnóstico: {nombre}              |
  | Body     | Resumen + HTML del reporte completo      |
```

---

## Feature: SLA y Plazos (Arc42 §1)

### Escenario: Plazo máximo de respuesta comunicado al cliente
```gherkin
Given que el cliente completa el formulario
When recibe el ACK de confirmación
Then el ACK debe comunicar explícitamente:
  | Mensaje | "Recibirás el informe técnico completo en un plazo máximo de 1 día hábil" |
```

### Escenario: SLA visible en la interfaz de envío
```gherkin
Given que el usuario está en el Paso 3 (Validación Final)
Then debe ver el SLA garantizado: "Respuesta en 1 Día"
```

---

## Feature: Notificación Interna al Técnico (Arc42 §5)

### Escenario: Correo de alerta al equipo SafetyMind
```gherkin
Given que el backend completa el análisis LangGraph
When el reporte se persiste en SQLite con estado PENDING
Then se envía un email a arturo@safetymind.ai con:
  | Campo    | Valor                                    |
  | Asunto   | Nuevo Diagnóstico: {nombre}              |
  | Body     | Reporte HTML completo con scores y fotos |
  | Link     | Enlace a /admin/review para revisión     |
```

---

## Feature: Validación de Imágenes (Criterios de Calidad Visual)

### Escenario: IA evalúa calidad de imagen por cámara
```gherkin
Given que el backend recibe 7 imágenes de cámaras
When el nodo Vision Analysis de LangGraph procesa cada imagen
Then asigna scores individuales de:
  | Criterio     | Rango  | Descripción                          |
  | Resolución   | 0-100  | Calidad de megapíxeles               |
  | Enfoque      | 0-100  | Nitidez de la imagen                 |
  | Iluminación  | 0-100  | Condiciones de luz                   |
  | Cobertura    | 0-100  | Ángulo y campo visual                |
```

### Escenario: Fallback de IA por cuota (Arc42 §7)
```gherkin
Given que la API de Gemini 2.0 Flash excede su cuota
When el nodo Vision Analysis falla
Then el sistema activa fallback con scores nominales (85/80/90/75)
And la cámara se marca como "Pendiente revisión 100% humana"
```

---

## Feature: Admin Console — Scores IA Visibles

### Escenario: Técnico ve pre-análisis IA por cámara
```gherkin
Given que el técnico selecciona un reporte en la consola
When revisa el grid de cámaras
Then debajo de cada miniatura debe ver:
  | Score         | Color        | Significado                     |
  | > 75          | Verde        | Aprobado por IA                 |
  | 50-75         | Amarillo     | Revisión recomendada            |
  | < 50          | Rojo         | Rechazado por IA                |
```

---

## Feature: Pipeline de Calidad (Arc42 §7 — TDD)

### Escenario: Pruebas unitarias del backend pasan antes del deploy
```gherkin
Given que se ha realizado un cambio en agent/main.py o agent/langgraph_agent.py
When se ejecuta `cd agent && python3 -m pytest tests/ -v`
Then todos los tests deben pasar (estado: PASSED)
```

### Escenario: Pruebas unitarias del frontend pasan antes del deploy
```gherkin
Given que se ha realizado un cambio en frontend/src/
When se ejecuta `cd frontend && npx vitest run`
Then todos los tests deben pasar (estado: PASSED)
```

### Escenario: Build de TypeScript sin errores
```gherkin
Given que se ha realizado un cambio en frontend/
When se ejecuta `cd frontend && npm run build`
Then el build debe completar sin errores de tipo (TypeScript strict)
```

## Feature: Factores de Riesgo con Evidencia (Paso 2)

### Escenario: Selección de múltiples factores por cámara
```gherkin
Given que el usuario está configurando la Cámara 1
When selecciona los factores "Iluminación" y "Obstrucción"
Then el sistema debe mostrar dos campos de descripción técnica
And debe mostrar dos selectores de archivos para las fotos de evidencia
```

### Escenario: Evidencia obligatoria para factores seleccionados
```gherkin
Given que el usuario seleccionó un factor de riesgo
When intenta avanzar sin subir la foto de evidencia o la descripción
Then el botón "Validar" debe permanecer DESHABILITADO
And se debe mostrar un mensaje "Evidencia requerida para: {factor}"
```

### Escenario: Análisis de evidencia por Gemini 2.0 Flash
```gherkin
Given que un reporte con factores de riesgo llega al backend
When el nodo Vision Analysis procesa la foto de evidencia
Then Gemini 2.0 Flash debe asignar un score de viabilidad al factor
And la razón técnica debe incluir detalles detectados en la imagen
```

### Escenario: Trazabilidad forense en aprobación técnica
```gherkin
Given un reporte en estado PROCESSING_COMPLETED
When el técnico intenta presionar "Aprobar" sin ingresar una justificación
Then el sistema debe mostrar un error "La justificación técnica es obligatoria"
And el estado del reporte no debe cambiar a APPROVED
When el técnico ingresa la justificación y su ID
Then se crea un registro en audit_traces con el veredicto original de la IA
```

### Escenario: Cifrado de datos PII (Privacidad)
```gherkin
Given que un técnico consulta la base de datos SQLite directamente
When intenta leer las columnas client_name o client_email de la tabla reports
Then debe ver un BLOB cifrado (ilegible)
And solo a través de la consola DAS con la llave correcta se deben ver los datos reales
```

### Escenario: Integridad Sentinel ante fallos de API
```gherkin
Given que un nodo de visión falla por timeout
When el sistema genera el reporte parcial
Then la cámara afectada debe mostrar el estado "REVISIÓN MANUAL REQUERIDA"
And el sistema TIENE PROHIBIDO inventar un score (como 80/100) para esa cámara
```

### Escenario: Prevención de duplicados vía Idempotency Key
```gherkin
Given que el frontend genera un UUID "uuid-123" para la sesión
When el usuario presiona "Enviar" y el request incluye el header X-Idempotency-Key: uuid-123
And el usuario vuelve a presionar "Enviar" accidentalmente (doble clic)
Then el backend debe ignorar el segundo request
And debe retornar el status del Job ID que ya está en proceso
```

### Escenario: Resiliencia ante caídas de API (Circuit Breaker)
```gherkin
Given que la API de Gemini 2.0 devuelve errores 500 consecutivamente
When el Circuit Breaker de "tenacity" alcanza el límite de reintentos
Then el sistema debe activar el "Modo de Respaldo Resiliente"
And el reporte debe marcarse con el flag DATA_STALE
And el dashboard debe mostrar una alerta visual "IA en modo offline - Revisión Manual Requerida"
```

### Escenario: Verificación de Cifrado con GCP KMS
```gherkin
Given que se persiste un nuevo diagnóstico
When el servicio Agent solicita el cifrado al GCP KMS
Then el nombre del cliente debe almacenarse como un BLOB cifrado (GCM)
And la llave maestra nunca debe salir del Vault de Google
```

---

## ✅ Tests Automatizados

### Backend (Agent)
- `agent/tests/test_das_pipeline.py` → 26 tests (pytest)
```bash
cd agent && python3 -m pytest tests/ -v
```

### Frontend (Vitest)
- `frontend/` → 60 tests (Vitest + React Testing Library)
```bash
cd frontend && npx vitest run
```

### Estado Actual
| Suite | Tests | Pasando | Cobertura |
|-------|-------|---------|-----------|
| Backend (pytest) | 26 | 26 | ✅ 100% |
| Frontend (Vitest) | 60 | 60 | ✅ 100% |
| **Total** | **86** | **86** | **✅ 100%** |

---

© 2026 SafetyMind Quality Assurance. Alineado con Arc42.
