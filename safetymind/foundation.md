# SafetyMind Foundation

Contenido específico del proyecto SafetyMind (Diagnostic Automation Suite).

---

## Architecture

- **Frontend:** Next.js 14 (App Router) + Tailwind CSS 4.0
- **Orchestration:** n8n V2 (Self-hosted) for workflow management and HITL
- **AI Agent:** LangGraph (Python 3.11) as state-machine orchestrator
- **LLM Engine:** Gemini 2.0 Flash (Vision) & Gemini 2.5 Pro (Reasoning)
- **Communication:** Multipart/FormData via HTTP Webhooks

---

## Design Tokens (OKLCH)

| Token | OKLCH Value | HEX Fallback |
|-------|-------------|--------------|
| `--primary` | `oklch(0.92 0.20 95)` | `#ffed01` |
| `--background` | `oklch(0 0 0)` | `#000000` |
| `--card` | `oklch(0.05 0 0)` | `#0a0a0a` |
| `--status-green` | `oklch(0.75 0.25 150)` | `#00ff88` |
| `--status-red` | `oklch(0.60 0.25 25)` | `#ff3b3b` |

---

## UI Standards

- **Bento Grid:** Modular grids for technical reports
- **Industrial Grid & Scanline:** Background effects for "Mission Critical" aesthetic
- **Industrial SVGs:** Traffic-sign style icons for risk factors
- **WCAG AAA:** 7:1 contrast ratios, >48px touch targets (Glove-Touch)
- **Glassmorphism:** `backdrop-filter: blur(8px)` with 10% opacity

---

## Coding Patterns

### Python (Agent)
- Use `TypedDict` for LangGraph state and `Optional` for API results
- Strict `.env` management, no hardcoded keys
- Print meaningful node transitions for debugging

### React (Frontend)
- Logic in custom hooks
- Mandatory `aria-label` for all interactive elements
- Atomic UI: `atoms` → `molecules` → `organisms`

---

## Design Patterns

- **State Machine:** Use `StateGraph` in LangGraph for AI transitions
- **Fallback Engine:** `try-except` blocks with technical fallbacks for 99.9% availability
- **Context Preservation:** All diagnostic data persists in LangGraph state until report generation

---

## Project Management (Jira)

- Issue naming: `DAS-[ID]` (e.g., DAS-9)
- Every significant change must include worklog update
- Keep `JIRA_SYNC_STATUS.md` and `JIRA_ROADMAP.md` updated

---

## Infrastructure

- Server: `192.168.1.149` (on-premise)
- Ports: 8000 (API), 8501 (Portal), 3000 (Grafana), 9090 (Prometheus)
- Docker Compose for all services
