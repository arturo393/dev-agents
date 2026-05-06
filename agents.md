# Agents Documentation

## Overview
This repository contains shared agents, workflows, and skills for development projects. Agents follow a consistent interface defined in `agents/base/base_agent.py`.

## Testing Approach (TDD/BDD/SDD)
**Read `.agents/TESTING_GUIDELINES.md` before writing tests.**

This is a **base reference, not strict rules** – adapt as needed for each task.
- **TDD**: Unit tests for pure logic (metrics, API handlers)
- **BDD**: Integration tests for user flows (services page, navigation)  
- **SDD**: TypeScript types + Zod schemas for API contracts

Prioritize practicality over dogma. See the full guidelines file for details.

## Agent Structure
```
agents/
├── base/           # Base classes and interfaces
├── hunter/         # Sales/lead generation agent
├── product/        # Document intelligence agent
└── bidding/        # GovTech bidding agent
```

## Creating a New Agent
1. Create a new directory under `agents/`
2. Inherit from `BaseAgent` (see `agents/base/base_agent.py`)
3. Implement the `run()` method
4. Add configuration in `config.yaml`
5. Document in `README.md`

## Agent Configuration
Each agent should have a `config.yaml`:
```yaml
name: agent_name
version: 1.0.0
description: Agent description
inputs:
  - name: input_field
    type: string
    required: true
outputs:
  - name: output_field
    type: json
dependencies:
  - requests
  - beautifulsoup4
```

## Using Agents in Projects
Add this repo as a submodule:
```bash
cd your-project
git submodule add https://github.com/arturo393/dev-agents.git .agents
```

Then import in your code:
```python
from .agents.agents.hunter import HunterAgent
agent = HunterAgent()
result = await agent.run(input_data)
```

## Versioning
- Major version: Breaking changes to interface
- Minor version: New features, backward compatible
- Patch version: Bug fixes

## Deprecation Policy
Deprecated agents will be moved to `agents/archive/` and supported for 2 minor versions before removal.
