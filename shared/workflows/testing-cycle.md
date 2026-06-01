---
name: Testing Cycle Orchestrator
description: Testing Cycle Orchestrator - Guía + Código + Auditoría (V1.0)
---

# 🔄 Testing Cycle Orchestrator

Orquestador del ciclo completo de desarrollo guiado por metodologías XDD.

## 🎯 Propósito

Une `workflows/driven-development.md` (la guía) con `workflows/testing-auditor.md` (el inspector) en un flujo único y coherente.

## 🚀 Ciclo Completo

```
┌──────────────────────────────────────────────────┐
│  1. ELEGIR METODOLOGÍA                           │
│     → workflows/driven-development.md            │
│     → Matriz de selección rápida                 │
└──────────────────┬───────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────┐
│  2. DESARROLLAR                                  │
│     → Código siguiendo el flujo XDD elegido      │
│     → CDD: componente → variantes → test         │
│     → TDD: test fail → code → test pass          │
│     → BDD: story → scenario → integración        │
│     → ...                                        │
└──────────────────┬───────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────┐
│  3. AUDITAR                                      │
│     → workflows/testing-auditor.md               │
│     → El auditor lee la guía para saber qué      │
│       metodología se usó                         │
│     → Reporte con scores y P1/P2/P3              │
└──────────────────┬───────────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────┐
│  4. ¿APROBADO?                                   │
│     → Sí:  continuar a commit/deploy             │
│     → No:  volver al paso 2 con las              │
│            recomendaciones del reporte           │
└──────────────────────────────────────────────────┘
```

## 🧠 Pasos de Ejecución

### Paso 1: Diagnosticar y Elegir
1. Lee `workflows/driven-development.md` — catálogo + matriz de selección
2. Pregunta al usuario (o infiere del contexto):
   - ¿Qué estás construyendo? (UI, lógica, API, dominio, seguridad)
   - ¿Hay criterios de aceptación definidos?
3. Selecciona la metodología XDD de la matriz
4. Comunica al usuario: "Usaremos [metodología] para este cambio"
5. Opcional: dejar nota en el commit message (ej: `feat(xdd:cdd+tdd): new sensor component`)

### Paso 2: Desarrollar
- El usuario codifica siguiendo el flujo de la metodología elegida
- Este agente puede asistir con ejemplos o templates si se le pide

### Paso 3: Auditar
1. Invoca `workflows/testing-auditor.md`
2. El auditor leerá la misma guía para saber qué metodología auditar
3. Genera reporte con scores

### Paso 4: Decidir
- **Score ≥ target**: ✅ Listo para commit → invocar `git-ops.md`
- **Score < target**: ❌ Volver a paso 2 con las recomendaciones del reporte

## 📋 Comandos Rápidos

```bash
# Ciclo completo interactivo
@testing-cycle

# Solo elegir metodología
@driven-development --diagnose "estoy creando un nuevo dashboard"

# Solo auditar (si ya desarrollaste)
@testing-auditor --methodology=cdd+tdd
```

## 📦 Dependencias

- `workflows/driven-development.md` — guía metodológica (lectura obligatoria en paso 1)
- `workflows/testing-auditor.md` — auditoría post-código (invocación en paso 3)
- `../TESTING_GUIDELINES.md` — referencia base de testing pragmático
- `git-ops.md` — commit al aprobar

## ⚠️ Reglas

- No saltarse la auditoría en cambios críticos (API, lógica core, seguridad)
- Si el usuario se salta la elección, usar default TDD+BDD+SDD
- El reporte de auditoría es sugerencia, no bloqueante — el usuario decide si deploya
