# Agents Documentation

Organized by project to keep concerns separated.

## Structure

- `shared/` — shared standards (UI/UX, React, Git conventions)
- `projects/<name>/` — per-project agents and workflows
- `launch/` — deployment, sync, auditing operations
- `backup/` — deprecated agents (historic reference)
- `skills/` — transversal modular skills
- `agents/` — Python base interfaces

## Convention

Cada proyecto ve solo su carpeta en `projects/`. Los estándares compartidos están en `shared/`. Si un documento mezcla preocupaciones de múltiples proyectos, refactorizarlo.

## Testing

Ver `TESTING_GUIDELINES.md` y `launch/testing-auditor.md`.
