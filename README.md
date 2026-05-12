# SafetyMind Dev Agents

Shared agents, workflows, and skills for SafetyMind projects.

## Structure

```
.agents/
├── shared/                        UI/UX standards, React practices, Git conventions
├── projects/
│   ├── diagnostic-automation-suite/   DAS: preventa técnica Seguros Bolívar
│   ├── infrastructure-monitoring/     Monitoreo multi-cliente Edge AI
│   ├── jira-automation/               Automatización Jira Cloud
│   └── montecarlo-bot/                Bot de trading (cripto)
├── launch/                        Deploy, sync, testing auditor
├── backup/                        Agentes deprecados
├── skills/                        Skills modulares transversales
└── agents/                        Base Python para agentes
```

## Uso

Cada proyecto consume este repo como submodule. Para trabajar en uno, ve a `projects/<proyecto>/`. Lo que está en `shared/` aplica a todos.
