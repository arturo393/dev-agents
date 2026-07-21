# dev-agents

Reusable general knowledge for AI assistants (opencode, Copilot, Cursor, Claude).

## Purpose

This repo contains **general foundations** for software engineering, firmware, and brand guidelines. Optimized for opencode — each project references this repo for shared knowledge.

## Structure

```
dev-agents/
├── opencode.json                          # opencode config
├── .opencode/
│   ├── instructions/
│   │   ├── software-foundation.md         # Code Review, XDD, Fault Tolerance, Hardware Resilience
│   │   └── firmware-foundation.md         # MISRA-C, C++20, Testing Tiers, Layered Architecture
│   └── skills/                            # (reserved for future skills)
├── shared/
│   └── brands/
│       ├── uqomm.md                       # Brand tokens UQOMM
│       └── safetymind.md                  # Brand tokens SafetyMind
└── README.md
```

## Usage

### In opencode

1. Clone this repo or add as submodule
2. Reference from your project's `opencode.json`:
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
3. Or copy the files you need to your project

### In other tools

Copy the files from `.opencode/instructions/` to your project's context.

## Conventions

- This repo contains only **general** and **reusable** knowledge
- Project-specific context goes in each project's own `agents.md`
- Brand guidelines go in `shared/brands/<brand>.md`
- Max ~150 lines per file. No generic theory — only applicable patterns
- All content in English
