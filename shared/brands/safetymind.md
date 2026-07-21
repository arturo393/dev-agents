# SafetyMind Brand Guidelines (Guardian Prime V4.0)

## Color Tokens (OKLCH + HEX Fallback)

| Token | OKLCH Value | HEX |
|-------|-------------|-----|
| `--primary` | `oklch(0.92 0.20 95)` | `#ffed01` |
| `--background` | `oklch(0 0 0)` | `#000000` |
| `--card` | `oklch(0.05 0 0)` | `#0a0a0a` |
| `--text-primary` | `oklch(1 0 0)` | `#ffffff` |
| `--text-secondary` | `oklch(0.55 0 0)` | `#888888` |
| `--status-green` | `oklch(0.75 0.25 150)` | `#00ff88` |
| `--status-red` | `oklch(0.60 0.25 25)` | `#ff3b3b` |

## Typography

- **Display & Titles**: `Chakra Petch` (Industrial/Technical vibe)
- **Body & Interface**: `Outfit` or `Inter` (Readability)
- **Technical Data**: `JetBrains Mono` (Zero-ambiguity)

## Layout Standards

- **Bento Grid**: Modular grids for technical reports
- **Industrial Grid & Scanline**: Background effects for "Mission Critical" aesthetic
- **Industrial SVGs**: Traffic-sign style icons for risk factors
- **WCAG AAA**: 7:1 contrast ratios, >48px touch targets (Glove-Touch)
- **Glassmorphism**: `backdrop-filter: blur(8px)` with 10% opacity

## UI Principles

- **Atomic Design**: atoms → molecules → organisms → templates
- **Hooks First**: Toda lógica de negocio en Custom Hooks
- **State Management**: TanStack Query (telemetry) + Zustand (UI state)
