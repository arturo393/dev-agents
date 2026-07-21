# dev-agents

Conocimiento general reutilizable para asistentes de IA (OpenCode, Copilot, Cursor, Claude).

## Propósito

Este repo contiene **fundamentos generales** de software engineering, testing, firmware, hardware, y brand guidelines. Cada proyecto tiene su propio `agents.md` con contexto específico.

## Estructura

```
dev-agents/
├── shared/
│   ├── software-foundation.md   # Code Review, Security, XDD, Fault Tolerance
│   ├── firmware-foundation.md   # MISRA-C, C++20 embedded, Testing Tiers
│   ├── hardware-foundation.md   # Simulation Fallback, Tests tolerantes
│   ├── brands/
│   │   ├── uqomm.md             # Brand tokens UQOMM
│   │   └── safetymind.md        # Brand tokens SafetyMind
│   ├── standards/
│   │   ├── go.instructions.md   # Go idiomatic
│   │   ├── ansible.instructions.md
│   │   ├── sanitizer-standards.md
│   │   └── cleanup-guidelines.md
│   ├── workflows/
│   │   ├── driven-development.md
│   │   └── testing-cycle.md
│   └── skills/
│       ├── SKILL.md             # Decision making framework
│       └── git-jira-sync/
│           └── SKILL.md
└── README.md
```

## Uso

1. **En tu proyecto**: Crea un `agents.md` con el contexto específico de tu proyecto
2. **En OpenCode**: Referencia los foundations de `shared/` para fundamentos generales
3. **En otros proyectos**: Los `shared/` files son reutilizables sin modificación

## Convenciones

- Este repo solo contiene conocimiento **general** y **reutilizable**
- El contexto específico de cada proyecto va en su propio `agents.md`
- Los brand guidelines van en `shared/brands/<marca>.md`
- Máximo ~150 líneas por archivo. Sin teoría genérica — solo lo aplicable
