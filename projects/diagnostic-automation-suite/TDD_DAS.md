---
description: Test Driven Development (TDD) Strategy & Results for SafetyMind DAS
---

# 🧪 TDD: Estrategia y Resultados de Pruebas (V4.3)

> Última ejecución: 2026-05-07 — **21/21 tests PASSED** ✅

## 1. Suite de Tests

**Ubicación:** `agent/tests/test_das_pipeline.py`
**Ejecución:** `cd agent && python3 -m pytest tests/ -v`

### Grupo 1: Database Layer (8 tests)
| Test | Validación |
|------|-----------|
| `test_init_db_creates_table` | La tabla `reports` se crea correctamente |
| `test_save_report_inserts_data` | Los datos se persisten con estado PENDING |
| `test_approve_report_changes_status` | Estado cambia a APPROVED |
| `test_reject_report_changes_status` | Estado cambia a REJECTED |
| `test_set_report_status_adjustments` | Estado cambia a ADJUSTMENTS_REQUIRED |
| `test_get_report_by_id_not_found` | Retorna None para IDs inexistentes |
| `test_infrastructure_json_roundtrip` | Datos JSON de infra sobreviven persistencia |
| `test_camera_scores_json_roundtrip` | Scores de cámaras sobreviven persistencia |

### Grupo 2: LangGraph State (3 tests)
| Test | Validación |
|------|-----------|
| `test_diagnostic_state_has_camera_risks` | El campo `camera_risks` existe en el estado |
| `test_diagnostic_state_fields_complete` | Todos los 16 campos requeridos están presentes |
| `test_report_uses_dynamic_date` | NO hay fechas hardcodeadas (BUG-2 fix) |

### Grupo 3: Report Template (2 tests)
| Test | Validación |
|------|-----------|
| `test_template_renders_without_error` | Jinja2 renderiza con datos VERDE |
| `test_template_handles_rojo_verdict` | Jinja2 renderiza con datos ROJO |

### Grupo 4: BDD Scenarios (8 tests)
| Test | Escenario BDD |
|------|--------------|
| `test_minimum_5_cameras_required` | 3 cámaras → NO permite envío |
| `test_5_cameras_allows_submission` | 5 cámaras → SÍ permite envío |
| `test_verdict_semaphore_verde` | Score 92 → VERDE |
| `test_verdict_semaphore_amarillo` | Score 72 → AMARILLO |
| `test_verdict_semaphore_rojo` | Score 45 → ROJO |
| `test_hitl_approve_flow` | Admin aprueba → APPROVED |
| `test_hitl_reject_flow` | Admin rechaza → REJECTED |
| `test_hitl_adjust_flow` | Admin ajusta → ADJUSTMENTS_REQUIRED |

## 2. Bugs Resueltos por Tests

| Bug | Test que lo valida | Estado |
|-----|-------------------|--------|
| BUG-1: `recipient` duplicada | Revisión manual + refactor | ✅ Corregido |
| BUG-2: Fecha hardcodeada | `test_report_uses_dynamic_date` | ✅ Corregido |
| BUG-3: Índices de cámaras | Refactor en frontend (`handleSubmit`) | ✅ Corregido |

## 3. Pipeline de Calidad Pre-Deploy

```bash
# 1. Ejecutar tests
cd agent && python3 -m pytest tests/ -v

# 2. Verificar linting
python3 -m flake8 main.py langgraph_agent.py database.py --max-line-length=200

# 3. Sync y deploy
rsync -avz agent/ arturo@100.74.53.2:/home/arturo/diagnostic-automation-suite/agent/
ssh arturo@100.74.53.2 "cd /home/arturo/diagnostic-automation-suite && docker compose restart agent-service"
```

## 4. Tests Pendientes (Roadmap)

| Test | Tipo | Prioridad |
|------|------|-----------|
| E2E Wizard Navigation | Playwright | 🟡 Media |
| SMTP ACK Integration | Mock SMTP | 🟡 Media |
| API `/analyze` full flow | FastAPI TestClient | 🔴 Alta |
| Frontend form validation | React Testing Library | 🟡 Media |

## 5. Frontend Test Specs (Vitest + React Testing Library)

**Ubicación propuesta:** `frontend/src/**/*.test.ts`
**Ejecución:** `cd frontend && npx vitest run`

### Grupo 5: Helpers (`lib/helpers.ts`) — 13 tests
| Test | Validación |
|------|-----------|
| `getValidCameras: filtra solo cámaras con file, brand y model` | 5 completas + 2 incompletas → 5 |
| `getValidCameras: cámara sin file no cuenta` | brand+model sin file → excluida |
| `getValidCameras: cámara sin brand no cuenta` | file+model sin brand → excluida |
| `getValidCameras: cámara sin model no cuenta` | file+brand sin model → excluida |
| `isValidInventory: >= 5 retorna true` | 6 válidas → true |
| `isValidInventory: < 5 retorna false` | 4 válidas → false |
| `getVerdictColor: VERDE` | `"VERDE"` → variable sm-green |
| `getVerdictColor: AMARILLO` | `"AMARILLO"` → variable sm-yellow |
| `getVerdictColor: ROJO` | `"ROJO"` → variable sm-red |
| `getVerdictColor: default` | `"DESCONOCIDO"` → text-secondary |
| `isTerminalStatus: APPROVED/REJECTED/ADJUSTMENTS_REQUIRED` | 3 terminales → true |
| `isTerminalStatus: PENDING` | No terminal → false |
| `isTerminalStatus: DRAFT` | No terminal → false |

### Grupo 6: Hooks — 12 tests
| Test | Validación |
|------|-----------|
| `useTheme: tema inicial dark` | `theme === "dark"` |
| `useTheme: toggleTheme dark→light` | dark → light |
| `useTheme: toggleTheme light→dark` | light → dark |
| `useTheme: persiste en localStorage` | key `sm-theme` guardada |
| `useTheme: sincroniza data-theme en <html>` | atributo correcto |
| `useSubmit: < 5 cámaras no envía` | errorMsg de validación |
| `useSubmit: construye FormData con client_name` | campo presente |
| `useSubmit: construye camera_N_risks como JSON` | array serializado |
| `useSubmit: VPN="Otra" usa vpnOther` | vpn_client = vpnOther |
| `useSubmit: éxito setea success=true` | setSuccess(true) |
| `useSubmit: error de red setea errorMsg` | mensaje de conexión |
| `useSubmit: reset limpia estados` | submitting=false, success=false, errorMsg="" |

### Grupo 7: Componentes Atom — 10 tests
| Test | Componente |
|------|-----------|
| ProgressBar con 50% → width 50% | `atoms/ProgressBar` |
| ProgressBar con 0% | `atoms/ProgressBar` |
| ProgressBar con 100% | `atoms/ProgressBar` |
| NotificationToast muestra mensaje | `atoms/NotificationToast` |
| NotificationToast ícono según tipo | `atoms/NotificationToast` |
| NotificationToast dismiss | `atoms/NotificationToast` |
| RiskIcons EPP renderiza | `atoms/RiskIcon` |
| RiskIcons ManMachine renderiza | `atoms/RiskIcon` |
| RiskIcons DangerZone renderiza | `atoms/RiskIcon` |
| RiskIcons Critical renderiza | `atoms/RiskIcon` |

### Grupo 8: Componentes Molecule — 10 tests
| Test | Componente |
|------|-----------|
| CameraCard muestra índice correcto | `molecules/CameraCard` |
| CameraCard placeholder sin preview | `molecules/CameraCard` |
| CameraCard imagen con preview | `molecules/CameraCard` |
| CameraCard input file accept image/* | `molecules/CameraCard` |
| CameraCard campos brand y model | `molecules/CameraCard` |
| CameraCard select isFixed 2 opciones | `molecules/CameraCard` |
| CameraCard select adminBy 4 opciones | `molecules/CameraCard` |
| CameraCard 6 botones de riesgo | `molecules/CameraCard` |
| CameraCard riesgo activo highlight | `molecules/CameraCard` |
| CameraCard riesgo inactivo opacity 40 | `molecules/CameraCard` |

### Grupo 9: Componentes Organism — 14 tests
| Test | Componente |
|------|-----------|
| StepIdentification: todos los campos existen | `organisms/StepIdentification` |
| StepIdentification: siguiente deshabilitado si vacío | `organisms/StepIdentification` |
| StepIdentification: campo "¿Cuál?" con VPN="Otra" | `organisms/StepIdentification` |
| StepInventory: renderiza 7 CameraCard | `organisms/StepInventory` |
| StepInventory: contador X/7 | `organisms/StepInventory` |
| StepInventory: validar deshabilitado < 5 | `organisms/StepInventory` |
| StepInventory: validar habilitado >= 5 | `organisms/StepInventory` |
| StepValidation: estado inicial "Confirmar Envío" | `organisms/StepValidation` |
| StepValidation: SLA "Respuesta en 1 Día" | `organisms/StepValidation` |
| StepValidation: "Recibido" en success | `organisms/StepValidation` |
| StepValidation: errorMsg visible | `organisms/StepValidation` |
| WizardNav: título "SafetyMind DAS" | `organisms/WizardNav` |
| WizardNav: botones Llenar/Simular | `organisms/WizardNav` |
| LoginPortal: access code + entradas | `organisms/LoginPortal` |

### Grupo 10: Páginas (Integración) — 8 tests
| Test | Validación |
|------|-----------|
| DiagnosticWizard: step 1 inicial | StepIdentification visible |
| DiagnosticWizard: avance paso 2 | StepInventory visible |
| DiagnosticWizard: avance paso 3 | StepValidation visible |
| DiagnosticWizard: simulación llena datos | Campos poblados |
| TechnicalReview: login screen sin sesión | LoginPortal visible |
| TechnicalReview: login exitoso DAS2026 | Panel visible |
| TechnicalReview: login fallido | Mensaje error |
| TechnicalReview: approve cambia estado | Badge + toast |

### Grupo 11: E2E (Playwright) — 4 escenarios
| Escenario | Pasos |
|-----------|-------|
| Flujo completo wizard | Llenar paso 1 → 5+ cámaras → validar → enviar |
| Validación mínima | 3 cámaras → botón Validar deshabilitado |
| Admin HITL completo | Login → seleccionar → approve → confirmar toast |
| Error de red | Desconectar backend → errorMsg visible |

---
© 2026 SafetyMind Engineering.
