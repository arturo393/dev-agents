# AGENTS.md

## What This Repo Is

Knowledge base for AI assistants. Not a code repo — no build, no tests, no CI. Reference it from other projects via `opencode.json` `references`.

## Structure

```
.opencode/instructions/   ← Load these as system instructions
  software-foundation.md  ← Code Review, XDD, Fault Tolerance, Hardware Resilience, tracker hygiene
  firmware-foundation.md  ← MISRA-C, C++20, Testing Tiers, Layered Architecture

.opencode/agents/         ← Agent sources (edit HERE)
  jira.md                 ← git → Jira (worklogs, states, blockers) and the plan the pages read
.claude/agents/           ← GENERATED for Claude Code by scripts/gen-claude-agents.sh
                            (same body, MCP tool names rewritten mcp__jira__*)

shared/brands/            ← Brand tokens (reference via opencode.json)
  uqomm.md
  safetymind.md

_archived/                ← Old project-specific content (ignore)
launch/                   ← Old project-specific workflows (ignore)
```

## Conventions

- **English only** in all instruction files
- **No project-specific content** — each project owns its own `agents.md`. **This applies to
  `.opencode/instructions/` only.** `skills/` *is* allowed to be product- or instrument-specific,
  and in practice all of it is (`openocd-vlad`, `siglent-scope`, `safetymind-jira`, `drift-radar`):
  a skill carries a procedure and the traps that procedure hit, which is inherently about one
  thing. `~/.claude/skills` is a symlink here, so Claude Code and opencode read one copy
- **Max ~150 lines** per file — patterns only, no theory
- Brand guidelines are the exception to the "no project-specific" rule (they document specific brands)
- **Before opening a tracker issue, enumerate the ones that already exist.** List every child of the
  parent (`parent = <key>`, the whole set) and cross-reference the keys already in the git history;
  report the work on the child that covers it, and create only what nothing covers. The principle is
  in `software-foundation.md` → Method Before Diagnosis; the executable step is the `jira`
  agent, which lists before proposing and creates only after the user confirms

## Editing an Agent

The `.opencode/` copy is the source; the `.claude/` one is generated. Edit the source, then:

```bash
scripts/gen-claude-agents.sh            # all of them
scripts/gen-claude-agents.sh jira       # just one
```

Only the tool list lives in the script — Claude Code needs it and opencode does not. The
`description` is read from the source, so it has exactly one copy. A new agent will not show up in
a session already running: the registry is built on connect.

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
