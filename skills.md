# Skills Documentation

## Overview
Skills are modular capabilities that can be used by agents or directly by users. They follow the SKILL.md format with frontmatter (`name` + `description`) for opencode compatibility.

## Skill Structure
Each skill should have:
```
skills/
├── skill-name/
│   ├── SKILL.md          # Main skill documentation (required)
│   ├── scripts/          # Optional scripts
│   ├── config/           # Optional configuration
│   └── examples/         # Optional usage examples
```

## Available Skills

### skills/
- **Decision Maker Evaluator** (`skills/SKILL.md`): Technical and commercial evaluation using hybrid quantitative + qualitative assessment.
- **UI Audit** (`skills/ui-audit/SKILL.md`): Deep technical UI/UX audit for React/Next.js projects with WCAG AAA compliance.
- **Jira Sync** (`skills/jira_sync/SKILL.md`): Syncs project tasks and issues with Jira via CLI.

### workflows/
- **Driven Development (XDD)** (`workflows/driven-development.md`): Multi-paradigm driven development methodology selector.
- **Testing Architecture Auditor** (`workflows/testing-auditor.md`): Audits and enforces pragmatic testing practices.
- **Testing Cycle Orchestrator** (`workflows/testing-cycle.md`): Orchestrates the full testing cycle.
- **Sanitizer Walkthrough** (`workflows/sanitizer-walkthrough.md`): ASan/UBSan/Valgrind audit procedure.
- **Validation Walkthrough** (`workflows/validation-walkthrough.md`): BDD/TDD/ATT/SDD layer selector and procedure.
- **Cleanup Walkthrough** (`workflows/cleanup-walkthrough.md`): Dead code identification and removal procedure.

### projects/montecarlo-bot/
- **Bio-Cognitive Guard** (`projects/montecarlo-bot/bio-cognitive-guard/SKILL.md`): Human factors and cognitive load auditor.
- **Runtime Sanitizer** (`projects/montecarlo-bot/runtime-sanitizer/SKILL.md`): ASan/UBSan/Valgrind memory safety.
- **Validation Agent (BTD/SDD)** (`projects/montecarlo-bot/btd-sdd-validation/SKILL.md`): BDD/TDD/ATT/SDD validation.
- **Cleanup Engine** (`projects/montecarlo-bot/cleanup-engine/SKILL.md`): Dead code removal and repo sanitation.
- **Master Integrator** (`projects/montecarlo-bot/master-integrator/SKILL.md`): Orchestrator that runs all agents.

### shared/
- **Git Operations** (`shared/git-ops.md`): Git commit and branch management with semantic messages.
- **React Development Standard** (`shared/react-standard.md`): SafetyMind React/Next.js development standards.
- **UI/UX Standards (Guardian Prime)** (`shared/ui-standards.md`): Unified UI/UX quality standards.
- **Sanitizer Standards** (`shared/sanitizer-standards.md`): Memory safety rules for C++ trading bots.
- **Testing Standards** (`shared/testing-standards.md`): BDD/TDD/ATT/SDD coverage and format standards.
- **Cleanup Guidelines** (`shared/cleanup-guidelines.md`): Dead code and technical debt policies.

### launch/
- **Launching Expert Agent** (`launch/launching-expert-agent.md`): Pre-production validation and deployment readiness checks.
- **SafetyMind Full Sync** (`launch/full-sync.md`): End-of-session sync for Git + Jira + documentation alignment.

## SKILL.md Format
```markdown
---
name: Skill Name
description: Brief description of what the skill does.
---

# Skill Name

## Description
Brief description...

## Usage
...instructions...
```

## Adding a New Skill
1. Create a new directory under `skills/` or `projects/<name>/`
2. Create `SKILL.md` with frontmatter (name + description)
3. Add any supporting scripts or configs
4. Update this `skills.md` with the new skill
5. Test the skill with opencode

## Using Skills with opencode
Skills are loaded by opencode via the `skill` tool using the skill name. Ensure each SKILL.md has proper `name` and `description` frontmatter for compatibility.
