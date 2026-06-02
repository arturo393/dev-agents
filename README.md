# dev-agents

Repositorio central de agentes e instrucciones para asistentes de IA (Copilot, Cursor, Claude).

## Estructura

```
dev-agents/
├── uqomm/          # Cliente UQOMM — agentes hardware/firmware/QA específicos
├── safetymind/     # Cliente SafetyMind — infra, Jira, DAS
├── personal/       # Proyectos personales — montecarlo-bot, planner, jira
└── shared/         # Reutilizable cross-proyecto
    ├── experts/    # Agentes especializados: xdd/, cpp, react, python
    ├── skills/     # Skills ejecutables: git-jira-sync, repo_sentinel, ui-audit
    ├── standards/  # Políticas: go, ansible, react, testing, sanitizer
    └── workflows/  # Procedimientos: cleanup, sanitizer, testing-cycle
```

## Convenciones

- Cada proyecto tiene un `context.md` con stack, rutas, comandos de build/test.
- Agentes UQOMM-specific viven en `uqomm/agents/`. Los reutilizables en `shared/experts/`.
- Un agente es útil si contiene rutas, decisiones o convenciones que el LLM no puede adivinar.
- Scripts con credenciales usan variables de entorno (`$SSH_PASSWORD`), nunca valores hardcodeados.

## Agregar un agente nuevo

1. ¿Es específico de un proyecto? → `<proyecto>/agents/`
2. ¿Es reutilizable entre proyectos? → `shared/experts/`
3. ¿Es un script ejecutable? → `shared/skills/<nombre>/scripts/`
4. Máximo ~150 líneas. Sin teoría genérica — solo lo que el LLM no sabe de tu proyecto.
