# AGENTS.md

## What This Repo Is

Knowledge base for AI assistants. Not a code repo — no build, no tests, no CI. Reference it from other projects via `opencode.json` `references`.

## Structure

```
.opencode/instructions/   ← Load these as system instructions
  software-foundation.md  ← Code Review, XDD, Fault Tolerance, Hardware Resilience
  firmware-foundation.md  ← MISRA-C, C++20, Testing Tiers, Layered Architecture

shared/brands/            ← Brand tokens (reference via opencode.json)
  uqomm.md
  safetymind.md

_archived/                ← Old project-specific content (ignore)
launch/                   ← Old project-specific workflows (ignore)
```

## Conventions

- **English only** in all instruction files
- **No project-specific content** — each project owns its own `agents.md`
- **Max ~150 lines** per file — patterns only, no theory
- Brand guidelines are the exception to the "no project-specific" rule (they document specific brands)

## How Other Projects Reference This

```json
{
  "references": {
    "dev-agents": {
      "path": "/path/to/dev-agents",
      "description": "General SE, firmware, and brand foundations"
    }
  }
}
```

## When Editing Instructions

- Keep patterns actionable, not educational
- Remove anything a competent engineer would already know
- Prefer tables and checklists over prose
- If it's project-specific, it doesn't belong here
