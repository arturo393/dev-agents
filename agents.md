# Agents Documentation

## UQOMM (`uqomm/agents/`)
- **uqomm-qa-master** — Orquestador QA multi-fase (security, unit, integration, HWIT)
- **uqomm-hwit-auditor** — Auditoría Hardware-in-the-Loop (SCPI, USB-TMC, sentinels)
- **uqomm-qt-designer-auditor** — Auditoría UI Qt/C++ (P1-P12, QSS, brand tokens)
- **uqomm-gui-web-auditor** — Auditoría UI web (Playwright, WCAG AAA, brand tokens)
- **uqomm-board-tools** — Board tools, protocolo UART, build FPGA
- **uqomm-tui-architect** — TUI con FTXUI
- **uqomm-audit-loop** — Orquestador de auditorías iterativas
- **uqomm-docs-expert** — Documentación arc42, ADR, C4
- **fw-ulad** — Firmware ULAD (ADC map, pines, protocolo)
- **stm32-expert** — STM32 (MISRA, HAL, init sequence, build/flash)
- **rdss-deploy** — Deploy RDSS (IPs, Docker, secrets, gotchas)

## SafetyMind (`safetymind/`)
- **infrastructure-monitoring/** — Guardian Prime, codebase auditor, deploy, DWService
- **jira-automation/** — PMO automation, Jira sync
- **diagnostic-automation-suite/** — BDD/TDD/SDD para DAS
  - **DAS Validation Agent** — Webhook health, agent health, container status, and n8n configuration validation
  - **DAS Responsive Agent** — Playwright-based viewport responsiveness audit across mobile, tablet, and desktop viewports

## Personal (`personal/`)
- **montecarlo-bot/** — Bot trading C++ (auditor, reviewer, DB, backtest, sanitizer, concurrency)
- **weekly-planner.agent.md** — Planificador semanal Jira (JQL de Arturo)
- **jira-sync-universal.agent.md** — Sync Git↔Jira universal

## Shared Experts (`shared/experts/`)
- **xdd/** — atdd, bdd, tdd, ddt, pbt (con ejemplos VLAD/UQOMM)
- **cpp-engineer** — C++ cross-proyecto (proyectos, build, convenciones)
- **react-engineer** — React/Next.js con brand tokens UQOMM/SafetyMind
- **python-monitor** — Python monitor service (paths, funciones, test patterns)

## Shared Skills (`shared/skills/`)
- **git-jira-sync** — Workflow commit+push+sync Jira
- **jira-sync** — Jira CLI básico vía mcp-atlassian
- **repo_sentinel** — CI hook + pre-commit
- **ui-audit** — Auditoría visual Playwright
- **infra-monitoring** — Scripts SSH de monitoreo
- **trading_bot_ops** — Audit completo del bot en producción

## Shared Standards/Workflows (`shared/standards/`, `shared/workflows/`)
Ver archivos individuales — políticas (standards) y procedimientos paso a paso (workflows).
