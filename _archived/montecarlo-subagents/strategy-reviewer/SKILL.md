---
name: Quant-Auditor-4D
description: 4-pillar quantitative strategy auditor (Antifragility, Microstructure, Financial AI, Moneyball) + filter throughput + regime alignment.
---

# Quant-Auditor-4D — Strategy Auditor

Combina el pipeline de filtros original con los 4 pilares Quant-Auditor-4D.

## Pilares

| # | Pilar | Enfoque |
|---|-------|---------|
| 1 | Antifragility (Taleb) | Payoff convexity, liquidity-aware SL, graceful failure, retry resilience |
| 2 | Microstructure | Price discreteness, tick/LOB, slippage modeling |
| 3 | Financial AI (López de Prado) | Fractional differentiation, Triple-Barrier, Meta-Labeling, Purged CV |
| 4 | Moneyball Metrics | Profit Factor, DD duration, regime PnL, hidden alpha variables |
| + | Filter Throughput | % bloqueado por cada gate (learner, convexity, squeeze, funding) |
| + | Regime Weights | Alineación weights ↔ PnL real por régimen |
| + | Risk Safety | Kelly normalization, small-account protection, drawdown circuit |

## Ejecución

```bash
cd /Users/arturo/development/dev-agents
python3 projects/montecarlo-bot/strategy-reviewer/agent.py
```
