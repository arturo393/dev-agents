# Agents Documentation

## UQOMM (`uqomm/agents/`)
- **uqomm-qa-master** — Orquestador QA multi-fase (security, unit, integration, HWIT)
- **uqomm-hwit-auditor** — Auditoría Hardware-in-the-Loop (SCPI, USB-TMC, sentinels)
- **uqomm-board-tools** — Board tools, protocolo UART, build FPGA, sw-vlad-dac-tools
- **uqomm-backend-expert** — Python/Go backends, serial monitor, frame codecs, polling
- **uqomm-software-design-standards** — Estándares UI (paleta, keyboard-first, WCAG AAA)
- **drs-hwit-auditor** — Auditoría HWIT específica DRS (CAT1-6, CGI HTTP, firmware gating)
- **uqomm-docs-expert** — Documentación arc42, ADR, C4
- **stm32-expert** — STM32 (MISRA, HAL, init sequence, build/flash)

## SafetyMind (`safetymind/`)
- **infrastructure-monitoring/** — Guardian Prime, codebase auditor, deploy, DWService
- **jira-automation/** — PMO automation (usar git-jira-sync skill o jira-sync-universal agent)
- **diagnostic-automation-suite/** — BDD/TDD/SDD para DAS
  - **DAS Validation Agent** — Webhook health, agent health, container status, n8n validation
  - **DAS Responsive Agent** — Playwright viewport responsiveness audit

## Personal (`personal/`)
- **montecarlo-bot/** — Bot trading C++ (master-integrator + context.md + monthly-reconcile.md)
- **weekly-planner.agent.md** — Planificador semanal Jira (JQL de Arturo)
- **jira-sync-universal.agent.md** — Sync Git↔Jira universal (canónico, ~150 líneas)

## Shared Experts (`shared/experts/`)
- **uqomm-frontend-expert** — Frontend UQOMM: React (legacy), Rust/Tauri (nuevos)
- **xdd/** — atdd, bdd, tdd, ddt, pbt *[pendiente crear]*
- **cpp-engineer** — C++ cross-proyecto *[pendiente crear]*
- **react-engineer** — React/Next.js con brand tokens *[pendiente crear]*
- **python-monitor** — Python monitor service *[pendiente crear]*

## Shared Skills (`shared/skills/`)
- **git-jira-sync** — Workflow commit+push+sync Jira
- **repo_sentinel** — CI hook + pre-commit
- **ui-audit** — Auditoría visual Playwright
- **infra-monitoring** — Scripts SSH de monitoreo
- **trading_bot_ops** — Audit completo del bot en producción (consolida MonteCarlo sub-agents archivados)

## Shared Standards/Workflows (`shared/standards/`, `shared/workflows/`)
Ver archivos individuales — políticas (standards) y procedimientos paso a paso (workflows).
