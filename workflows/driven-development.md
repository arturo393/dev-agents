---
description: SafetyMind XDD Standards - Multi-Paradigm Driven Development (V1.0)
---

# 🔄 SafetyMind XDD - Multi-Paradigm Driven Development

Este agente selecciona y aplica la metodología Driven Development adecuada según el contexto del cambio, maximizando flexibilidad sin sacrificar calidad.

## 🎯 Principio Rector

> Pragmatismo sobre dogma. Cada metodología es una herramienta, no una religión.

## 📋 Catálogo de Metodologías XDD

### 1. CDD (Component-Driven Development)
- **Cuándo**: Componentes de UI nuevos en React/Next.js
- **Flujo**: Story o mock → Componente → Test visual
- **Output**: Componente atómico con variantes y estados (loading, empty, error, success)
- **Herramientas**: Storybook, Vitest + Testing Library

### 2. TDD (Test-Driven Development)
- **Cuándo**: Lógica pura, hooks, utilidades, conversiones de datos
- **Flujo**: Red (test falla) → Green (test pasa) → Refactor
- **Output**: Test unitario + implementación mínima
- **Herramientas**: Vitest, Jest

### 3. BDD (Behavior-Driven Development)
- **Cuándo**: Flujos de usuario, pages, integraciones
- **Flujo**: User Story → Escenario → Test de integración → Código
- **Output**: Test de integración legible por negocio
- **Herramientas**: Vitest con describe/it descriptivo (sin Gherkin)

### 4. DDD (Domain-Driven Design)
- **Cuándo**: Lógica de negocio compleja, microservicios, modelos de datos
- **Flujo**: Ubicar contexto acotado → Modelar entidades/agregados → Implementar
- **Output**: Código que refleja el lenguaje ubicuo del dominio
- **Recursos**: `SDD_DAS.md`, tipos compartidos

### 5. ATDD (Acceptance Test-Driven Development)
- **Cuándo**: Criterios de aceptación dados por el cliente/PM
- **Flujo**: Criterio → Prueba de aceptación → Feature → Validación
- **Output**: Feature completa validada contra expectativas

### 6. SDD (Schema-Driven Development)
- **Cuándo**: Contratos de API, tipos compartidos, serialización
- **Flujo**: Schema → Types → Validación runtime
- **Output**: Zod schemas / TypeScript interfaces que definen el contrato
- **Herramientas**: Zod, TypeScript strict, ts-reset

### 7. STDD (Security-Test Driven Development)
- **Cuándo**: Endpoints sensibles, autenticación, datos de planta
- **Flujo**: Identificar vector → Escribir test de seguridad → Mitigar → Verificar
- **Output**: Tests que prueban inyección, XSS, exposure de datos

## 🧠 Matriz de Selección Rápida

| Escenario | Metodología | Prioridad |
|-----------|-------------|-----------|
| Nuevo componente UI | CDD + TDD (lógica) | Alta |
| Hook o utilidad nueva | TDD | Alta |
| Feature con criterios definidos | BDD / ATDD | Media |
| API o integración nueva | SDD + TDD | Alta |
| Refactor de lógica existente | TDD (antes) | Media |
| Bug crítico | TDD (reproducir bug) | Alta |
| Módulo con lógica de dominio compleja | DDD + TDD | Alta |
| Feature con datos sensibles | STDD | Según riesgo |

## 🚀 Flujo de Trabajo Recomendado

1. **Diagnóstico**: Identificar el tipo de cambio (UI, lógica, API, dominio, seguridad)
2. **Seleccionar metodología**: Usar la matriz de selección rápida
3. **Ejecutar ciclo**: Seguir el flujo de la metodología elegida
4. **Auto-auditar**: Pasar el test suite antes de commit
5. **Pueden combinarse**: Un componente nuevo puede usar CDD + TDD + SDD simultáneamente

## ⚠️ Anti-patrones

- ❌ Forzar TDD en componentes UI puros (usar CDD)
- ❌ Escribir tests BDD con Gherkin/Cucumber pesado (vitest descriptivo basta)
- ❌ Aplicar DDD donde un simple tipo basta
- ❌ Escribir tests triviales solo por cumplir métricas
- ❌ STDD sin análisis de riesgo real

## 🔧 Integración con el Ecosistema

- `git-ops.md`: Tras pasar tests, commiteaer con mensaje semántico
- `react-development-standard.md`: Seguir CDD con Atomic Design + Hooks-First
- `safetymind-guardian-prime.md`: Validar WCAG AAA y Guardian Prime en componentes UI
- `../TESTING_GUIDELINES.md`: Referencia base de testing pragmático
- `testing-auditor.md`: Auditor post-codificación — validarás contra la metodología elegida aquí
- `testing-cycle.md`: Orquestador — ejecuta el ciclo completo guía → código → auditoría
