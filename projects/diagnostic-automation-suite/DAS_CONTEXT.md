# 🛡️ SafetyMind DAS Master Context & Standards
**Project:** Diagnostic Automation Suite (DAS)
**Version:** 1.2.0 (Gemini 2.0 Modernization)

## 🏗️ Architecture & Patterns

### 1. Core Architecture
- **Frontend:** Next.js 14 (App Router) + Tailwind CSS 4.0.
- **Orchestration:** n8n V2 (Self-hosted) for workflow management and HITL.
- **AI Agent:** LangGraph (Python 3.11) as a state-machine orchestrator.
- **LLM Engine:** Gemini 2.0 Flash (Vision) & Gemini 2.5 Pro (Reasoning).
- **Communication:** Multipart/FormData via HTTP Webhooks.

### 2. Design Patterns
- **State Machine:** Use `StateGraph` in LangGraph to manage AI transitions.
- **Fallback Engine:** Always implement `try-except` blocks with technical fallbacks for AI nodes to ensure 99.9% availability.
- **Atomic UI (Lite):** Organized as `atoms` -> `molecules` -> `organisms` in React.
- **Context Preservation:** All diagnostic data must persist in the LangGraph state until report generation.

## 🎨 UI/UX & Brand Identity (Guardian Prime V4.0 - DAS Edition)

### 1. Authority
All UI/UX decisions must follow the **[SAFETYMIND_DAS_AGENT](file:///Users/arturo/development/SafetyMind/.agents/workflows/SAFETYMIND_DAS_AGENT.md)** protocol. This project uses a specialized variant of the Guardian Prime standard optimized for diagnostic workflows.

### 2. Official Palette (OKLCH)
| Token | OKLCH Value | HEX Fallback |
| :--- | :--- | :--- |
| `--primary` | `oklch(0.92 0.20 95)` | `#ffed01` |
| `--background` | `oklch(0 0 0)` | `#000000` |
| `--card` | `oklch(0.05 0 0)` | `#0a0a0a` |
| `--status-green` | `oklch(0.75 0.25 150)` | `#00ff88` |
| `--status-red` | `oklch(0.60 0.25 25)` | `#ff3b3b` |

### 3. Layout Standards
- **Bento Grid:** Use modular grids for technical reports.
- **Industrial Grid & Scanline:** Mandatory background effects for the "Mission Critical" aesthetic.
- **Industrial SVGs:** Use traffic-sign style icons for risk factors.
- **WCAG AAA:** Ensure 7:1 contrast ratios and >48px touch targets (Glove-Touch).

## 🛠️ Coding Best Practices

### Python (Agent)
- **Typing:** Use `TypedDict` for LangGraph state and `Optional` for API results.
- **Environment:** Strict `.env` management, no hardcoded keys.
- **Logging:** Print meaningful node transitions for debugging in production logs.

### React (Frontend)
- **Hooks First:** Logic in custom hooks.
- **Glassmorphism:** Subtle blur (`backdrop-filter: blur(8px)`) with 10% opacity.
- **Accessibility:** Mandatory `aria-label` for all interactive elements.

## 🔄 Project Management (Jira Sync)
- **Issue Naming:** `DAS-[ID]` (e.g., DAS-9).
- **Worklogs:** Every significant change must include a worklog update via script.
- **Sync Status:** Keep `JIRA_SYNC_STATUS.md` and `JIRA_ROADMAP.md` updated as the primary source of truth for stakeholders.

---
*This document is the authoritative source for Antigravity AI when working on the SafetyMind DAS project.*
