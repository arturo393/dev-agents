# Pragmatic Testing Guidelines (TDD/BDD/SDD)

Base guidelines for testing in SafetyMind Infrastructure Monitoring. **Not strict rules** – use as reference, adapt as needed.

## Core Differences
| Approach | Focus | Cycle | Use Case |
|----------|-------|-------|----------|
| TDD | Internal logic, pure functions | Test → Fail → Code → Pass | Metric conversions, API logic |
| BDD | User-visible behavior | User story → Scenario → Test → Code | Page flows, UI interactions |
| SDD | Formal contracts, schemas | Spec → Contract → Validation | API responses, data types |

## Hybrid Approach (Recommended)
- **TDD**: Unit tests for critical logic (metrics, API handlers)
- **BDD**: Integration tests for user flows (service selection, navigation)
- **SDD**: TypeScript types + Zod schemas for API contracts

## Do's ✅
- Use TDD for pure logic (e.g., `Number(cpuLoad)` conversion)
- Use BDD-style tests for UI behavior (e.g., toggle service activation)
- Use SDD via TypeScript interfaces for API contracts
- Keep tests minimal, focus on critical paths
- Use Vitest/Jest without heavy BDD frameworks

## Don'ts ❌
- Don't install heavy BDD frameworks (Cucumber/Gherkin) – plain test syntax is enough
- Don't write TDD tests for trivial UI components
- Don't enforce strict specs for every helper function
- Don't sacrifice flexibility for dogmatic adherence

## Project Structure Reference
```
portal/src/
├── types/          # SDD: Contracts (telemetry.ts, etc.)
├── app/api/        # TDD: API logic tests
└── test/           # BDD: User flow tests (services-page.test.tsx)
```

## Agent Note
When writing tests, follow this guideline as a base. Adjust based on task needs – no need to strictly adhere to all points. Prioritize practicality over dogma.
