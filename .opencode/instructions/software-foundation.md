# Software Engineering Foundation

Reusable knowledge for any software project.

---

## Code Review Pillars

| Pillar | Checks |
|--------|--------|
| **Maintainability** | Complexity >50 lines/4 levels, dead code, redundancy, naming |
| **Resilience** | Idempotency, `except: pass`, timeouts, inconsistent state |
| **Security** | Credentials, input validation, least privilege |
| **Observability** | `print()` in prod, exit codes, actionable messages, CI/CD |
| **Code UX** | Does the code invite use or rewriting? (see below) |

### Security by Context

Don't apply generic checklists. Ask:

1. **Isolated network or internet?**
   - Isolated → rate limiting + input validation + Docker segmentation
   - Internet → HTTPS + auth + RBAC + WAF
2. **Who can damage hardware with wrong commands?**
   - RF commands → mandatory rate limiting
   - Flashable firmware → serial/JTAG access control
3. **Sensitive data?** (locations, frequencies, power levels)
   - Yes → minimal logging, don't expose in public dashboards
   - No → prioritize observability

Rule: **3 well-applied controls > 10 generic checklist items.**

### Security Audit (Static)

| Language | Detectors |
|----------|-----------|
| PHP | `eval`, `unserialize`, `$_GET/POST/REQUEST` |
| JS/TS | `.innerHTML`, `eval`, `document.write` |
| Python | `subprocess`, `except Exception: pass`, `eval` |
| Shell | `rm $VAR`, `curl \| bash`, `chmod 777` |

Critical/High block progress. Medium → fix + continue. Low → log.

---

## Testing Methodology (XDD)

> Pragmatism over dogma. Each methodology is a tool, not a religion.

### Methodology Catalog

| # | Methodology | When | Flow | Output |
|---|-------------|------|------|--------|
| 1 | **CDD** (Component-Driven) | New UI components | Story/mock → Component → Visual test | Atomic component with variants |
| 2 | **TDD** (Test-Driven) | Pure logic, hooks, utilities | Red → Green → Refactor | Unit test + minimal implementation |
| 3 | **BDD** (Behavior-Driven) | User flows, pages, integrations | Story → Scenario → Integration test → Code | Business-readable integration test |
| 4 | **DDD** (Domain-Driven) | Complex business logic, microservices | Bounded context → Entities/aggregates → Implement | Code reflecting ubiquitous language |
| 5 | **ATDD** (Acceptance Test-Driven) | Client/PM acceptance criteria | Criterion → Acceptance test → Feature → Validation | Feature validated against expectations |
| 6 | **SDD** (Schema-Driven) | API contracts, shared types | Schema → Types → Runtime validation | Zod/TypeScript defining the contract |
| 7 | **STDD** (Security-Test-Driven) | Sensitive endpoints, auth | Identify vector → Security test → Mitigate → Verify | Tests for injection, XSS, exposure |
| 8 | **PBT** (Property-Based) | Edge cases, fuzzing | Properties + random inputs → Failures | Discovered edge cases |
| 9 | **DDT** (Data-Driven) | Multiple devices/configurations | Test matrix → Execute per config | Coverage across variants |

### Quick Selection Matrix

| Scenario | Methodology | Priority |
|----------|-------------|----------|
| New UI component | CDD + TDD (logic) | High |
| New hook or utility | TDD | High |
| Feature with defined criteria | BDD / ATDD | Medium |
| New API or integration | SDD + TDD | High |
| Refactor existing logic | TDD (before) | Medium |
| Critical bug | TDD (reproduce bug) | High |
| Complex domain module | DDD + TDD | High |
| Feature with sensitive data | STDD | Risk-based |

**Golden rule:** No test, no production change. Every fix includes its test.

---

## Code UX Principles

### 3-Second Scan
Every file must have a 3-line header: what it does, how to use it, what it DOESN'T do.

### API by Usage Flow
Methods organized by usage order, not by type:
1. Construct → create instance
2. Configure → prepare
3. Control → execute
4. Execute step → use in loop
5. Query → check state
6. Utilities → helpers

### Verb Names
| Bad (says HOW) | Good (says WHAT) |
|----------------|------------------|
| `apply_current_config()` | `start_scan()` |
| `handle_received_data()` | `on_data()` |
| `check_scan_timeout()` | `advance_or_stop()` |
| `get_detection_count()` | `detection_count()` |

### Universal Checklist
| # | Rule |
|---|------|
| 1 | 3-line header at the top of every file |
| 2 | API ordered by usage flow |
| 3 | Names are verbs without `get_`/`set_` prefix |
| 4 | No inline logic in headers (signatures only) |
| 5 | Files < 500 lines |
| 6 | Max 4 parameters per function |

---

## Documentation Principles

| Pattern | Rule |
|---------|------|
| Lead with answer | Decision or action first, context after |
| Progressive disclosure | Happy path → details → edge cases |
| Chunking | Small sections, short lists |
| Signposting | Headings, labels, callouts |
| Recognition over recall | Tables, checklists, templates |

### Rules
- Every document answers a real question
- No generic READMEs
- Don't document for documentation's sake
- ADR only for decisions with >30 min discussion

---

## Resilience & Fault Tolerance

### 1. Circuit Breaker
Service fails repeatedly → open circuit → friendly fallback → automatic recovery.

**Example:** Payments fail → "Payment unavailable, try later" → service recovers in background.

### 2. Bulkhead (Failure Isolation)
Each critical module runs isolated in its own "compartment".

**Example:** If reports fail, authentication and sales keep working.

### 3. Observability
- **Structured logs** (JSON): request traceability across services
- **Metrics**: latency, error rate, memory usage
- **Alerts**: notify when error rate > 0.1%

### 4. Eventual Consistency
Accept that data between services may be temporarily misaligned.

**Example:** User updates profile → other services see it 2-5 seconds later.

### 5. Saga Pattern (Compensating Transactions)
Multi-step operation fails → automatic compensating action.

**Example:** Charge successful + reservation failed → emit automatic refund.

### 6. Feature Flags
Deploy features "off" behind a switch.

**Benefit:** Serious bug → turn off flag without full redeploy.

### 7. Chaos Engineering
Inject controlled failures in production to verify resilience.

**Tool:** Netflix Chaos Monkey.

### 8. Fuzz Testing
Send massive random data to find vulnerabilities.

**Goal:** Find holes before an attacker does.

---

## Technical Debt & Dead Code

### Philosophy

> "Code that doesn't run is not an asset, it's a liability."

Dead code in the binary:
- Increases compile time
- Increases binary size
- Confuses new developers
- Hides real bugs (is that error from live or dead code?)

### Rules

| Rule | Description |
|------|-------------|
| **D1** | Dead code = code that doesn't affect the outcome |
| **D2** | If it exists in production but isn't used → delete it (recover from git if needed) |
| **D3** | Backup before modifying build system |

### Priority

| Priority | Category | When |
|----------|----------|------|
| P0 | Dead binary (unused compiled files) | Immediately |
| P1 | Commented-out code blocks | During refactor |
| P2 | Unused dependencies in build files | Sprint planning |
| P3 | Old backup files (>30 days) | Monthly cleanup |
| P4 | Rotational logs (>7 days) | Automate with logrotate |

### Anti-patterns

- ❌ "I'll leave it just in case" — Dead code isn't safe, it's noise
- ❌ "I deleted the file but not from the build" — Worse, now you get link errors
- ❌ "It's commented but I'll need it later" — That's what git is for

---

## Hardware Resilience Patterns

For projects interacting with physical instruments or lab infrastructure.

### 1. Simulation Mode Fallback

Instrument controllers (USB-TMC, Serial, TCP) must load native drivers dynamically. If the driver doesn't exist (CI without hardware), enter Simulation Mode transparently — never abort.

```python
try:
    driver = load_native_driver(device)
except DriverNotFoundError:
    driver = SimulationDriver(device)
```

### 2. Tolerant Tests

Don't assert fixed ideal states. `"degraded"` is a valid controlled state.

```python
# Correct
assert response["status"] in {"ok", "degraded"}

# Incorrect
assert response["status"] == "ok"
```

### 3. LD_PRELOAD for Binary Incompatibilities

Vendor SDKs compiled against deprecated libraries require injecting the compatible library via `ENV LD_PRELOAD` in the Dockerfile.

```dockerfile
ENV LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libudev.so.1
```

### 4. Hostname Offline-First

Format: `<client>-<role>-<location>-<mac-last4>`

```
# Correct
myapp-testbench-lab-657a
monitor-prod-8f2c

# Incorrect (causes collisions, doesn't work offline)
testbench-1
testbench-2
```

---

## Audit Loop (Convergence)

When asked to audit until convergence (zero findings):

1. **Detect type**: Web/Qt/TUI based on files
2. **Loop** (max 10 rounds):
   - Apply standard, list findings with severity, apply fix
   - Stop condition: `findings_total == 0` or `fixes_applied == 0`
   - Same finding 3 rounds without fix → mark "blocked"
3. **Final report**: rounds executed, findings per round, blocked issues
