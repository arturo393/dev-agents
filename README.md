# Dev Agents

Shared agents, workflows, and skills for development projects.

## Structure
```
dev-agents/
├── agents/           # Reusable agent definitions
│   ├── base/        # Base classes and interfaces
│   ├── hunter/      # Sales/lead generation agent
│   ├── product/     # Document intelligence agent
│   └── bidding/     # GovTech bidding agent
├── workflows/        # Pre-built workflow compositions
├── skills/          # Shareable skill modules
├── agents.md        # Agent documentation
├── skills.md        # Skill documentation
└── README.md        # This file
```

## Quick Start
Add as submodule to your project:
```bash
git submodule add https://github.com/arturo393/dev-agents.git .agents
git submodule update --init --recursive
```

## Contributing
1. Create a new branch
2. Add your agent/skill/workflow
3. Update relevant documentation
4. Submit a pull request

## License
MIT
