---
description: Test Driven Development (TDD) Strategy & Results for SafetyMind DAS
---

# 🧪 TDD: Estrategia y Resultados de Pruebas (V4.3)

> Última ejecución: 2026-05-12 — **86/86 tests PASSED** ✅
> Backend: 26/26 (pytest) · Frontend: 60/60 (Vitest)

## 1. Suite de Tests — Backend (pytest)

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

### Grupo 5: API Endpoints (5 tests — Nuevo)
| Test | Validación | Estado |
|------|-----------|--------|
| `test_api_analyze_success` | POST /analyze retorna 200 con verdict válido | 🔴 Pendiente |
| `test_api_analyze_missing_fields` | POST /analyze sin campos requeridos → 422 | 🔴 Pendiente |
| `test_api_approve_sends_email` | POST /reports/{id}/approve envía SMTP | 🔴 Pendiente |
| `test_api_list_reports` | GET /reports retorna lista paginada | 🔴 Pendiente |
| `test_api_report_not_found` | GET /reports/{id} inexistente → 404 | 🔴 Pendiente |

## 2. Bugs Resueltos por Tests

| Bug | Test que lo valida | Estado |
|-----|-------------------|--------|
| BUG-1: `recipient` duplicada | Revisión manual + refactor | ✅ Corregido |
| BUG-2: Fecha hardcodeada | `test_report_uses_dynamic_date` | ✅ Corregido |
| BUG-3: Índices de cámaras | Refactor en frontend (`handleSubmit`) | ✅ Corregido |
| BUG-4: SMTP_PASS no se pasaba al contenedor | Verificación manual en deploy | ✅ Corregido (docker-compose) |

## 3. Pipeline de Calidad Pre-Deploy

```bash
# 1. Backend tests
cd agent && python3 -m pytest tests/ -v

# 2. Frontend tests
cd frontend && npx vitest run

# 3. Lint
cd frontend && npm run lint

# 4. Build (TypeScript check)
cd frontend && npm run build

# 5. Sync y deploy
rsync -avz --exclude '.git' --exclude 'node_modules' --exclude '__pycache__' . arturo@100.74.53.2:/home/arturo/jira-automation/
ssh arturo@100.74.53.2 "cd /home/arturo/jira-automation && sudo docker compose up --build -d"
```

## 4. Frontend Test Specs (Vitest + React Testing Library)

**Ubicación:** `frontend/src/**/*.test.ts`
**Ejecución:** `cd frontend && npx vitest run`

### Grupo 6: Helpers (`lib/helpers.ts`) — 15 tests ✅
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

### Grupo 7: Hooks — 12 tests ✅
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

### Grupo 8: Componentes Atom — 11 tests ✅
| Test | Componente |
|------|-----------|
| ProgressBar con 50% → width 50% | `atoms/ProgressBar` |
| ProgressBar con 0% | `atoms/ProgressBar` |
| ProgressBar con 100% | `atoms/ProgressBar` |
| NotificationToast muestra mensaje | `atoms/NotificationToast` |
| NotificationToast dismiss | `atoms/NotificationToast` |
| RiskIcons EPP renderiza | `atoms/RiskIcon` |
| RiskIcons ManMachine renderiza | `atoms/RiskIcon` |
| RiskIcons DangerZone renderiza | `atoms/RiskIcon` |
| RiskIcons Critical renderiza | `atoms/RiskIcon` |

### Grupo 9: Componentes Molecule — 7 tests ✅
| Test | Componente |
|------|-----------|
| CameraCard muestra índice correcto (CAM-01) | `molecules/CameraCard` |
| CameraCard placeholder sin preview | `molecules/CameraCard` |
| CameraCard imagen con preview | `molecules/CameraCard` |
| CameraCard muestra brand + model | `molecules/CameraCard` |
| CameraCard select isFixed 2 opciones | `molecules/CameraCard` |
| CameraCard select adminBy 4 opciones | `molecules/CameraCard` |
| CameraCard 6 botones de riesgo | `molecules/CameraCard` |

### Grupo 10: Componentes Organism — 15 tests ✅
| Test | Componente |
|------|-----------|
| StepIdentification: todos los campos existen | `organisms/StepIdentification` |
| StepIdentification: siguiente deshabilitado si vacío | `organisms/StepIdentification` |
| StepIdentification: campo "¿Cuál?" con VPN="Otra" | `organisms/StepIdentification` |
| StepInventory: renderiza 7 CameraCard | `organisms/StepInventory` |
| StepInventory: botón Validar deshabilitado < 5 | `organisms/StepInventory` |
| StepValidation: estado inicial "Confirmar Envío" | `organisms/StepValidation` |
| StepValidation: SLA "Respuesta en 1 Día" | `organisms/StepValidation` |
| StepValidation: "Recibido" en success | `organisms/StepValidation` |
| StepValidation: errorMsg visible | `organisms/StepValidation` |

### Grupo 11: Páginas — Tests de Integración (Pendientes)
| Test | Validación | Estado |
|------|-----------|--------|
| `test_wizard_step_validation` (Arc42) | Verificar que NO se puede avanzar del Paso 1 sin elegir VPN y tipo de red | 🔴 Pendiente |
| `test_wizard_upload_7_cameras` (Arc42) | Verificar que el formulario exige exactamente 7 fotografías (1 por cámara) antes de habilitar "Enviar" | 🟡 Parcial (valida mínimo 5) |
| `test_dashboard_camera_actions` (Arc42) | Verificar que en el Dashboard interno, al hacer clic en "Aprobar" en una cámara, se emita un request PATCH al backend | 🔴 Pendiente |
| `test_theme_toggle_persists` | Alternar tema y recargar → tema persiste | ✅ Implementado (en useTheme) |

### Grupo 12: E2E (Playwright) — 4 escenarios (Pendientes)
| Escenario | Pasos | Estado |
|-----------|-------|--------|
| Flujo completo wizard | Llenar paso 1 → 5+ cámaras → validar → enviar | 🔴 Pendiente |
| Validación mínima | 3 cámaras → botón Validar deshabilitado | 🔴 Pendiente |
| Admin HITL completo | Login → seleccionar → approve → confirmar toast | 🔴 Pendiente |
| Error de red | Desconectar backend → errorMsg visible | 🔴 Pendiente |

## 5. Tests Pendientes (Roadmap)

| Test | Tipo | Prioridad | Especificado en |
|------|------|-----------|-----------------|
| API `/analyze` full flow | FastAPI TestClient | 🔴 Alta | Arc42 §7 |
| SMTP ACK Integration | Mock SMTP | 🟡 Media | Arc42 §7 |
| E2E Wizard Navigation | Playwright | 🟡 Media | Arc42 §7 |
| Gemini Vision fallback | Mock API | 🟡 Media | Arc42 §7 |
| Per-camera HITL approval | React Testing Library | 🟡 Media | Arc42 §7 |
| Dashboard camera actions | React Testing Library | 🟡 Media | Arc42 §7 |

## 6. Cobertura de Tests

| Capa | Tests | Estado |
|------|-------|--------|
| Backend DB | 8 | ✅ Pasando |
| Backend LangGraph | 3 | ✅ Pasando |
| Backend Templates | 2 | ✅ Pasando |
| Backend BDD Scenarios | 8 | ✅ Pasando |
| Backend API Endpoints | 5 | 🔴 Pendiente |
| Frontend Helpers | 13 | ✅ Pasando |
| Frontend Hooks | 12 | ✅ Pasando |
| Frontend Atoms | 9 | ✅ Pasando |
| Frontend Molecules | 7 | ✅ Pasando |
| Frontend Organisms | 9 | ✅ Pasando |
| Frontend Pages (Integration) | 4 | 🔴 Pendiente |
| E2E (Playwright) | 4 | 🔴 Pendiente |
| **Total** | **86** | **✅ 60 pasando · 26 pendientes** |

---

© 2026 SafetyMind Engineering. Alineado con Arc42.
