# Agents Documentation

Organized by project to keep concerns separated.

## Structure

- `shared/` — shared standards (UI/UX, React, Git, Sanitizer, Testing, Cleanup)
- `projects/<name>/` — per-project agents and workflows
- `launch/` — deployment, sync, auditing operations
- `backup/` — deprecated agents (historic reference)
- `skills/` — transversal modular skills
- `workflows/` — methodology walkthroughs (XDD, Sanitizer, Validation, Cleanup)
- `agents/` — Python base interfaces

## Convention

Cada proyecto ve solo su carpeta en `projects/`. Los estándares compartidos están en `shared/`. Si un documento mezcla preocupaciones de múltiples proyectos, refactorizarlo.

## Available Agents

### MonteCarlo Bot (`projects/montecarlo-bot/`)
- **Bot Functional Auditor** — End-to-end technical audit of all bot modules
- **CPP Trading Reviewer v2.0** — Advanced C++ static analysis for trading safety
- **Database Auditor** — SQLite PnL and fee auditing
- **Check Server Logs** — Remote log retrieval from production
- **Backtest Agent** — GA optimization orchestrator
- **Bio-Cognitive Guard** — Human factors, cognitive load, circadian resilience
- **Runtime Sanitizer** — ASan/UBSan/Valgrind memory safety
- **Validation (BTD/SDD)** — BDD/TDD/ATT/SDD multi-layer validation
- **Cleanup Engine** — Dead code removal and repo sanitation
- **Master Integrator** — Orchestrator that runs all agents and consolidates reports

### Walkthroughs (`workflows/`)
- **Driven Development (XDD)** — Methodology selector for CDD/TDD/BDD/DDD/ATDD/SDD/STDD
- **Testing Auditor** — Audits testing practices against chosen XDD methodology
- **Testing Cycle** — Full cycle: guide → code → audit
- **Sanitizer Walkthrough** — ASan/UBSan/Valgrind audit procedure
- **Validation Walkthrough** — BDD/TDD/ATT/SDD layer selector
- **Cleanup Walkthrough** — Dead code identification and removal procedure

### Shared Standards (`shared/`)
- **Git Operations** — Semantic commit management
- **React Development Standard** — SafetyMind React/Next.js standards
- **UI/UX Standards (Guardian Prime)** — WCAG AAA compliance
- **Sanitizer Standards** — Memory safety rules for C++ trading bots
- **Testing Standards** — BDD/TDD/ATT/SDD coverage and format
- **Cleanup Guidelines** — Dead code and technical debt policies

### Launch (`launch/`)
- **Launching Expert Agent** — Pre-production validation
- **Full Sync** — End-of-session Git + Jira + docs alignment

## Testing

Ver `TESTING_GUIDELINES.md` y `workflows/testing-auditor.md`.
