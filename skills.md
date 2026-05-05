# Skills Documentation

## Overview
Skills are modular capabilities that can be used by agents or directly by users. They follow the pattern established in the original `.agents/skills/` directories.

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

## SKILL.md Format
```markdown
# Skill Name

## Description
Brief description of what the skill does.

## Use Cases
- Use case 1
- Use case 2

## Usage
```bash
# Example command
```

## Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| param1    | string | Yes | Description |

## Examples
Example usage scenarios.
```

## Available Skills
- **capacity**: Azure OpenAI model capacity discovery
- **customize**: Custom model deployment
- **deploy-model**: Unified deployment skill
- **microsoft-foundry**: Foundry agent management
- **preset**: Quick deployment to optimal regions

## Adding a New Skill
1. Create a new directory under `skills/`
2. Create `SKILL.md` with the required format
3. Add any supporting scripts or configs
4. Update this `skills.md` with the new skill
5. Test the skill in a project

## Using Skills
Skills can be referenced by agents or used directly:
```python
# In an agent
from skills.capacity import check_capacity

# Direct usage via tool
# Use the skill tool with name="capacity"
```

## Migration from Old .agents/skills/
If migrating from project-specific `.agents/skills/`:
1. Copy the skill directory to `skills/`
2. Ensure SKILL.md follows the standard format
3. Remove from original project after testing
