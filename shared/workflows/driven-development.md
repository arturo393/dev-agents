---
name: Driven Development (XDD)
description: Multi-Paradigm Driven Development Methodologies
---

# XDD - Multi-Paradigm Driven Development

This agent selects and applies the appropriate Driven Development methodology based on change context, maximizing flexibility without sacrificing quality.

## Guiding Principle

> Pragmatism over dogma. Each methodology is a tool, not a religion.

## XDD Methodology Catalog

### 1. CDD (Component-Driven Development)
- **When**: New UI components in React/Next.js
- **Flow**: Story or mock → Component → Visual test
- **Output**: Atomic component with variants and states (loading, empty, error, success)
- **Tools**: Storybook, Vitest + Testing Library

### 2. TDD (Test-Driven Development)
- **When**: Pure logic, hooks, utilities, data conversions
- **Flow**: Red (test fails) → Green (test passes) → Refactor
- **Output**: Unit test + minimal implementation
- **Tools**: Vitest, Jest

### 3. BDD (Behavior-Driven Development)
- **When**: User flows, pages, integrations
- **Flow**: User Story → Scenario → Integration test → Code
- **Output**: Business-readable integration test
- **Tools**: Vitest with descriptive describe/it (no Gherkin)

### 4. DDD (Domain-Driven Design)
- **When**: Complex business logic, microservices, data models
- **Flow**: Locate bounded context → Model entities/aggregates → Implement
- **Output**: Code reflecting ubiquitous domain language
- **Resources**: Shared types

### 5. ATDD (Acceptance Test-Driven Development)
- **When**: Acceptance criteria given by client/PM
- **Flow**: Criterion → Acceptance test → Feature → Validation
- **Output**: Complete feature validated against expectations

### 6. SDD (Schema-Driven Development)
- **When**: API contracts, shared types, serialization
- **Flow**: Schema → Types → Runtime validation
- **Output**: Zod schemas / TypeScript interfaces defining the contract
- **Tools**: Zod, TypeScript strict, ts-reset

### 7. STDD (Security-Test Driven Development)
- **When**: Sensitive endpoints, authentication, plant data
- **Flow**: Identify vector → Write security test → Mitigate → Verify
- **Output**: Tests for injection, XSS, data exposure

## Quick Selection Matrix

| Scenario | Methodology | Priority |
|----------|-------------|----------|
| New UI component | CDD + TDD (logic) | High |
| New hook or utility | TDD | High |
| Feature with defined criteria | BDD / ATDD | Medium |
| New API or integration | SDD + TDD | High |
| Refactor existing logic | TDD (before) | Medium |
| Critical bug | TDD (reproduce bug) | High |
| Module with complex domain logic | DDD + TDD | High |
| Feature with sensitive data | STDD | Risk-based |

## Recommended Workflow

1. **Diagnose**: Identify change type (UI, logic, API, domain, security)
2. **Select methodology**: Use quick selection matrix
3. **Execute cycle**: Follow chosen methodology flow
4. **Self-audit**: Run test suite before commit
5. **Can combine**: New component can use CDD + TDD + SDD simultaneously

## Anti-patterns

- ❌ Force TDD on pure UI components (use CDD)
- ❌ Write BDD tests with heavy Gherkin/Cucumber (descriptive vitest suffices)
- ❌ Apply DDD where a simple type suffices
- ❌ Write trivial tests just to meet metrics
- ❌ STDD without real risk analysis

## Ecosystem Integration

- `../software-foundation.md`: Code Review, Testing, Security
- `../TESTING_GUIDELINES.md`: Base reference for pragmatic testing
