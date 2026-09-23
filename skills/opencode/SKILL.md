---
name: opencode
description: Delegar una consulta a otro modelo (OmniRoute razonamiento/codigo/gratis, GPT, Gemini, GLM, Grok, Kimi, Qwen) o a un agente de opencode ejecutando `opencode run` desde Claude Code. Usar cuando el usuario pida: segunda opinión de otro modelo, "preguntale a GPT/Gemini", contrastar un diagnóstico o una spec, delegar una tarea mecánica barata (resumir, extraer de un datasheet) para no gastar el límite de Claude, o correr un auditor de opencode. Solo para Claude Code: dentro de opencode no tiene sentido.
---

# opencode como herramienta

Qué hace: ejecuta `opencode run` sin interfaz y trae la respuesta de otro modelo o agente.
Cómo se usa: plantilla de abajo. **Modelo por defecto para todo: `omniroute/razonamiento`** (gratis).
Qué NO hace: no edita código. La respuesta es una opinión que se verifica, nunca evidencia.

## Plantilla

```bash
cd /tmp && timeout 300 opencode run \
  -m omniroute/razonamiento --agent plan \
  --dir <repo absoluto> --format json "<consulta>" 2>&1 \
| jq -rc 'select(.type=="text" or .type=="error" or .type=="step_finish")
  | if .type=="text" then .part.text
    elif .type=="error" then "ERROR: " + (.error.data.message // .error.name)
    else "[costo US$ \(.part.cost) · razonamiento \(.part.tokens.reasoning) tok]" end'
```

- **Decisión del usuario (23-Sep-2026): `razonamiento` para todo** — mecánico y segundas opiniones.
  Otro modelo solo si el usuario lo nombra ("pregúntale a GPT"); ahí se usa la tabla de Zen, con
  `-m opencode/<modelo> --variant <nivel>`. Si `razonamiento` falla (todos los modelos del combo
  caídos), decirlo y preguntar antes de pasar a uno pago.
- `--dir` fija el repo que ve el modelo. Carga las fundaciones de `dev-agents` (~29k tokens de
  contexto incluso para un "OK"), así que el piso de costo no es cero.
- Con `-f archivo` se adjuntan archivos (un datasheet, un log).
- Para continuar la misma conversación: `-c` (la última) o `-s <sessionID>`.

## Agentes: solo tres modos sirven con `--agent`

| Agente | Modo | Qué puede hacer de verdad |
|---|---|---|
| `plan` | primary | **Por defecto.** Herramienta de edición denegada; **bash sigue permitido** |
| `auditor-arquitectura`, `auditor-resiliencia`, `auditor-ui` | all | Auditan. "No escribe código" lo dice el prompt, **no el permiso**: tienen `*` allow |
| `build` | primary | Edita todo. **No usar** salvo pedido explícito del usuario |

**Trampa medida (23-Sep-2026):** un agente de modo `subagent` (`jira`, `software-foundation`,
`firmware-foundation`, `auditor-cuantitativo`, `auditor-ejecucion-cpp`, `pnl-forensic`, `explore`,
`general`) **o un nombre inexistente** no da error: opencode cae en silencio a `build`, que puede
editar. Por eso:

1. Mirar la primera línea de la salida en formato default: `> <agente> · <modelo>`. Si dice
   `build` y no se pidió, la corrida no fue la que se pensaba.
2. Después de **cualquier** corrida sobre un repo: `git -C <repo> status --short`. Si cambió algo
   que no estaba, reportarlo al usuario y no descartarlo por cuenta propia.
3. Nunca `--auto`: aprueba sola cualquier permiso que no esté denegado.

Un subagente **no se puede invocar directo**. Pedírselo a `plan` en la consulta ("usa el subagente
X para…") **no está verificado**: en la prueba contestó bien pero la salida no mostró ninguna
llamada al subagente, así que pudo haberlo resuelto `plan` solo. Si hace falta el subagente de
verdad, correrlo desde el TUI de opencode.

## OmniRoute: `razonamiento`, `codigo`, `gratis` — gratis, pero no sabes quién contesta

`omniroute/<combo>` pasa por el router local (`omniroute serve`, `localhost:20128`, clave en
`$OMNIROUTE_API_KEY`). Cada combo es una lista de modelos gratuitos con estrategia `auto`: **el
modelo que responde cambia entre llamadas, e incluso entre pasos de una misma corrida**. Costo 0.
`--variant` no aplica (el combo no declara niveles).

| Combo | Qué hay detrás (según `/api/combos`, 23-Sep-2026) |
|---|---|
| `razonamiento` | qwen3.6-27b y gpt-oss-120b (groq), claude-opus-4-6-thinking y gemini-3.7-flash-high (antigravity), nemotron-3-super, big-pickle, mimo, aihorde |
| `codigo` | gpt-oss-120b, qwen3.6-27b, claude-opus-4-6-thinking, gemini-3.1-pro-low, north-mini-code, … |
| `gratis` | gpt-oss-120b/20b, qwen3.6-27b, nemotron, gemini-3.7-flash-high, gemini-3.1-pro-low, … |

**Medido:** una consulta chica por `curl` la contestó `groq/openai/gpt-oss-120b`. La misma vía
`opencode run` (≈37k tokens de contexto por las fundaciones) falló en groq con **413** (demasiado
grande), en big-pickle con **401**, y terminó en `antigravity/gemini-3.7-flash-high`. Una hora
después, otra corrida desde opencode la contestaron `gpt-oss-120b` y `nemotron-3-super` sin
ningún 413. **No hay patrón fijo: siempre leer el log.** El conteo de razonamiento sale en 0 por
este camino aunque el modelo razone: no significa nada.

**Regla:** después de cada corrida por OmniRoute, leer qué modelo contestó y reportarlo:

```bash
curl -s -H "Authorization: Bearer $OMNIROUTE_API_KEY" "localhost:20128/api/usage/call-logs?limit=6" \
| jq -r '.[] | "\(.timestamp[11:19])  \(.status)  \(.provider)/\(.model)"'
```

Para una pregunta sin repo (sin archivos que leer), ir directo al router: menos contexto, más
rápido, y la respuesta trae el modelo en `.model`:

```bash
curl -s -H "Authorization: Bearer $OMNIROUTE_API_KEY" -H 'Content-Type: application/json' \
  localhost:20128/v1/chat/completions \
  -d '{"model":"razonamiento","messages":[{"role":"user","content":"<consulta>"}]}' \
| jq -r '"[\(.model)]", .choices[0].message.content'
```

Es el modelo por defecto para todo. Como el modelo cambia, al presentar una segunda opinión
nombrar el que contestó según el log: «opinó gemini-3.7-flash-high vía razonamiento».

## Modelos de opencode Zen (solo si el usuario nombra uno): listado ≠ accesible

`opencode models` lista 153, pero la cuenta tiene acceso a una parte. Medido el 23-Sep-2026:

| Modelo | Costo in/out (US$/M) | Niveles (`--variant`) | Para qué |
|---|---|---|---|
| `gpt-6-luna` | 0.1 / 0.5 | none, low, medium, high, xhigh, max | Mecánico y barato: resumir, extraer, reformatear |
| `qwen3.8-flash` | 0.15 / 0.47 | low, medium, xhigh | Mecánico, alternativa |
| `gpt-6-sol` | 2 / 10 | none, low, medium, high, xhigh, max | Segunda opinión seria: diagnóstico, spec, diseño |
| `glm-5.3` | 1.4 / 4.4 | low, high, max | Segunda opinión, otra familia |
| `grok-4.7` | 1.4 / 4.2 | low, medium, high, xhigh | Segunda opinión, otra familia |
| `gemini-3.8-flash` | 1.5 / 7.5 | low, medium, high | Contexto largo, documentos |
| `kimi-k3` | 3 / 15 | max | Razonamiento largo; caro para lo trivial |

**Sin acceso** ("Model access is disabled"): `gpt-5.5`, `gpt-5.3-codex`, `gemini-3.1-pro`,
`claude-sonnet-5`, `deepseek-v4-flash`. Un modelo que no está en ninguna de las dos listas: probarlo
con `"Responde: OK"` y `--variant low` antes de usarlo en serio.

Para una segunda opinión conviene **otra familia** que Claude: se equivoca en cosas distintas.

## Nivel de razonamiento

| Tarea | Nivel |
|---|---|
| Extraer, resumir, reformatear | `low` o `none` |
| Revisar código, contrastar una explicación | `medium` o `high` |
| Diagnóstico causal, cálculo, spec, encontrar el hueco en un argumento | `xhigh` o `max` |

**Trampa medida:** un `--variant` que el modelo no tiene (`nope`) **se ignora en silencio** y corre
con el nivel por defecto. Usar solo los nombres de la tabla de arriba. La prueba de que el nivel
se aplicó es el conteo `razonamiento N tok` del `step_finish`: con `xhigh` sobre un problema de
cálculo dio 158; con `high` sobre una multiplicación trivial dio 0, que no prueba nada.

## Cómo presentar lo que vuelve

- Decir **qué modelo, qué nivel y cuánto costó**, siempre.
- Separar dónde coincide con el análisis propio y dónde discrepa. Las discrepancias son lo valioso:
  verificarlas contra el código o el hardware antes de adoptarlas.
- Salida vacía o `ERROR:` es una falla de la corrida, no "el modelo no encontró nada".
- La respuesta de otro modelo no es una fuente: no citarla como verificación de nada
  (`software-foundation.md` → Verification Integrity).
