# 🧠 SafetyMind Dev Agents — Plataforma Unificada de Agentes

¡Bienvenido! Este repositorio es tu **biblioteca central de automatización e inteligencia para el desarrollo**. Está diseñado bajo un enfoque **Multi-Tenant (Multinquilino)**, lo que te permite usar esta misma biblioteca tanto para tus proyectos personales (como tu bot de trading C++) como para tu trabajo profesional en Uqomm o futuros clientes.

Para que sea sumamente fácil de entender, usar y mantener, simplificamos y estandarizamos la arquitectura en **dos conceptos muy sencillos**:

---

## 🗺️ La Arquitectura Simplificada

```
dev-agents/ (Repositorio Central)
│
├── shared/                     [1. TU BIBLIOTECA GLOBAL (Transversal y Reutilizable)]
│   ├── personas/                    - Los Cerebros: Perfiles expertos (.agent.md)
│   ├── standards/                   - Guías de "Qué es correcto" (git-ops, react-standard)
│   ├── workflows/                   - Guías procedimentales "Cómo se hace" (testing-cycle)
│   └── skills/                      - Scripts programáticos "Con qué se ejecuta" (sanitizer)
│
└── projects/                   [2. TUS INQUILINOS (Contextos Específicos)]
    ├── uqomm/                       - Cliente: Uqomm Corporation (context.md, stm32, Qt)
    ├── montecarlo-bot/              - Proyecto: Bot de trading C++ (context.md, Bybit)
    └── jira-automation/             - PMO: Automatización Jira Cloud (context.md)
```

---

## 💡 Conceptos Clave para Entender el Sistema

### 1. El Capitán (Brain) vs. El Marinero (Hands)

*   **El Capitán (Personas `.agent.md` en `shared/personas/`):**
    *   **Qué es:** Es un archivo Markdown (`.agent.md`) que define un **perfil o rol experto** en lenguaje natural (ej. *C++ Expert*).
    *   **Cómo se usa:** Lo cargás en tu asistente de IA (como Cursor o Copilot) usando `@nombre-agente`. Le indica a la IA cómo debe comportarse, qué reglas de Uncle Bob seguir, y qué estándares de seguridad de memoria respetar.
*   **El Marinero (Skills programáticos en `shared/skills/`):**
    *   **Qué es:** Es código ejecutable (Python, Bash, C++).
    *   **Cómo se usa:** Es la **herramienta** que el Capitán (la IA) ejecuta de forma automatizada en la terminal para hacer el trabajo sucio (ej: correr sanitizadores, borrar archivos basura `.DS_Store`, auditar base de datos).

### 2. Estándares (`standards/`) vs. Workflows (`workflows/`)

*   **Un Estándar (`shared/standards/`):** Es una **política de calidad** (ej. *nuestros commits de Git deben tener este formato semántico*).
*   **Un Workflow (`shared/workflows/`):** Es una **receta paso a paso** (ej. *para agregar un feature: 1. Crear rama ➔ 2. Escribir test ➔ 3. Programar código ➔ 4. Correr sanitizer ➔ 5. Hacer commit*).

---

## 📋 ¿Cómo se adapta un Agente Global a tu Proyecto? (El archivo `context.md`)

Cada carpeta de proyecto en `projects/<nombre-proyecto>/` posee un único archivo centralizado llamado **`context.md`**. Este archivo es la interfaz que los agentes globales leen al instante para entender dónde están trabajando:

```markdown
# Context: [Nombre del Proyecto]
- **Stack:** [C++17, Qt6, Catch2 | STM32 Firmware, Lora | Python, SQLite]
- **Ruta Local:** [Ubicación absoluta en tu máquina de desarrollo]
- **Comando Build:** [Comando exacto para compilar, ej: cmake --build build]
- **Comando Test:** [Comando exacto para correr pruebas unitarias, ej: ctest]
- **Convenciones:** [Ej: No usar excepciones, solo punteros inteligentes, etc.]
```

Cuando invocás al agente de C++ (por ejemplo, importando `shared/personas/expert-cpp-concurrency-auditor.agent.md` en las Custom Instructions de Cursor, o creando un enlace simbólico desde `shared/personas/` a la carpeta `.github/agents/` de tu espacio de trabajo activo), este lee automáticamente el `context.md` del proyecto abierto y adopta su compilador, comandos y convenciones al instante, garantizando **cero errores de compilación y 100% de compatibilidad**.

---

## 📈 El Flujo de Trabajo Ideal en tu Día a Día

1.  **Abrís tu editor (Cursor/VS Code) en el proyecto en el que vas a trabajar** (ej. el firmware de Uqomm).
2.  **Invocás al Agente de IA** cargando o referenciando el archivo `.agent.md` desde `shared/personas/`.
3.  El agente lee en silencio el archivo `projects/uqomm/context.md` y aprende: *"Ah! Estoy en Uqomm, programando Lora en STM32, no puedo usar malloc y compilo con arm-none-eabi-gcc."*
4.  Le pedís que programe una nueva funcionalidad.
5.  El agente escribe el código respetando las convenciones de Uqomm y **corre los tests automáticamente** usando el comando de compilación del `context.md`.
6.  **¡Todo queda compilado y validado en segundos sin esfuerzo mental de tu parte!**
