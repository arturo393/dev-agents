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

### Test polarity: a test that documents a defect is not a test that prevents it

A test written to **prove a bug exists** passes *because* the bug exists. When someone fixes the
bug, that test fails — and the natural reaction is to think the fix is wrong.

Both forms are legitimate, but they must be labeled:

| Form | Asserts | When the bug is fixed |
|---|---|---|
| `CHECK_DIES(...)` / `assert(crashes)` | the defect is present | **fails** — must be inverted |
| `CHECK(survives)` / `assert(bounded)` | the protection works | keeps passing |

**Rule:** when you fix a defect that had a documenting test, invert the test in the same commit.
Leaving it certifies the defect forever.

### Negative control: the only proof that a test tests something

A test that passes with the defect **present and absent** proves nothing.

**Rule:** after writing or fixing a test, revert the fix, confirm the test fails, restore. If it
does not fail, the test is decorative.

Evidence: a firmware review found **six** tests written with `CHECK_DIES` that certified bugs. Only
the negative control distinguished the real fixes from the no-ops.

### A test file that is not in the build list is zero coverage, silently

Evidence: a new contract test was written, the suite ran green, and the test **never executed** — the
harness listed its targets explicitly instead of globbing, so an unregistered file is simply absent.
It was caught only by looking for its own line in the output and not finding it.

**Rule:** after adding a test, confirm **its name appears in the run output**. A green suite is not
evidence that your test ran.

### The tests must compile the artifact that ships

Green tests over code that is not deployed measure nothing about production.

**Rule:** verify which target the test harness builds. If it is not the one in the field, that is a
coverage gap of 100 %, not a detail.

Evidence: a repo had 61 passing tests that compiled a variant, while the deployed firmware had
**zero** host coverage — and extending the harness found a wrong assumption on the first run.

---

## Verification Integrity

> The highest-yield question when reviewing any system:
> **does this confirmation look at the effect, or at the intention?**

Not a single rule of MISRA, the C++20 checklist or the Review Pillars catches this class. It was
found seven times in one week, across firmware, a server, a CLI tool and a build system:

| Symptom | What it reported | What it did |
|---|---|---|
| Log then write | «will not save» | saved |
| Readback after a write | the requested value | never applied it to the hardware |
| Function returning `bool` | success or failure | the only `return false` was commented out |
| `if (call() == OK) { }` | checks the status | empty body: discards it |
| Tool reporting `success: true` | the update happened | the HTTP call was missing |
| Version string in a binary | the commit it was built from | that commit cannot produce that binary |
| Test asserting a crash | the code is protected | it certified the bug |
| Fixture with a hardcoded date | the device is `healthy` | it asserted health for 157 days of silence |
| Schema test over hand-written examples | producer and contract agree | the examples used the types the schema already knew |

### How to detect it

| Ask | Red flag |
|---|---|
| What does the confirmation **read**? | the same variable that was just written |
| Can this function ever return failure? | the only failure path is commented out or unreachable |
| Does the `if` on the status **do** anything? | empty body, or only logs at debug level |
| Does the success path verify the **side effect**? | it verifies the request, not the result |
| Can the reported provenance regenerate the artifact? | build metadata taken from HEAD, ignoring a dirty tree |
| Does the fixture age? | a fixed date in a test about freshness stops being valid the day after it was written |
| Does the conformance test read the **producer**, or an example? | an example written next to the schema can only confirm the schema agrees with itself |

### Invert the direction of a conformance test

A test that validates *examples* against a schema proves the examples match. It cannot see a
producer that emits something the contract never declared, because the producer is not in the loop.

**Rule:** read the literals the producer actually emits — from its source — and require the contract
to declare them. Then verify the test can fail: remove one value from the contract and confirm it
turns red.

Evidence: three alert types were emitted by a consumer since the day it was written, and no contract
declared any of them. Every schema test passed. In the lab the amplifier had reported the condition
57 times. A test reading the producer's literals found it in one run.

**Rule:** a confirmation that cannot fail is worse than no confirmation, because it manufactures
confidence. Either make it able to fail, or remove it and say plainly that the operation is
unverified.

---

## Method Before Diagnosis

### Read what already exists before deriving it again

**Rule:** before diagnosing, list and skim `docs/`, `CHANGELOG`, and prior audits **of the repo you
are in**. Cross-reference every finding against them before calling it new.

Evidence: two critical defects were re-derived from scratch, one of them with an hour of hardware
debugging — both were already written in the same repository, with the same mechanism identified.

**Corollary on symbols in audit documents:** verify what a mark means before trusting it. In one
audit `✅` meant *confidence level* («verified by reading the code»), not *fixed*. Ten criticals
looked closed and were open.

### Never trust a `grep` count without looking at the matches

**Rule:** a count only answers «how many lines match», not «does the defect exist». Read the
matches. Comments describing a bug match the same pattern as the bug.

### Say «verified» only for what was executed

**Rule:** separate what was *measured* from what was *inferred*. When a conclusion depends on an
assumption — a compiler flag, a buffer size, a call order — verify the assumption explicitly and
say so. If it cannot be verified, state the conclusion as conditional.

Evidence: an entire causal chain about a crash depended on `-fno-exceptions` being set. It was, but
nobody had checked until it was written down as a dependency.

---

## Build Provenance

Firmware and any artifact deployed to a device must be **reproducible from what it reports**.

| Rule | Why |
|---|---|
| The version must include the commit **and** a dirty marker | a build over uncommitted changes is not reproducible from any commit |
| Generated-code config must agree with the source of truth | regenerating from the IDE can silently ship different behavior |
| A compile-time assertion should protect timing invariants | a bricked device in the field becomes a build error |

Evidence: a fleet reported `2.1.0+<sha>` where that commit did not contain the code running on it —
it had been built with uncommitted changes, and the very command added to identify a unit returned
an answer that could not rebuild it.

---

## Cross-Repo Contracts

When several products share a framing, a bus or a library, the contract lives **between** repos and
nothing enforces it.

| Rule | Why |
|---|---|
| One source of truth per opcode, encoding and constant | the same byte meaning two things is a permanent trap |
| Same transport ≠ same command space | one device may route the same code to different handlers by port |
| A shared fix goes upstream **before** being declared done | a local fix leaves the other consumers broken and is lost on the next update |
| A device must reject what is not addressed to it | otherwise a tool for another product can brick it |

### A sentinel means what the *consumer* decides, not what the producer intended

`0xFFFF` for «not measurable» is honest only if the reader treats it as absent. A decoder that
**clamps to a range** turns that same sentinel into the *most favourable reading in the range*.

Evidence: a firmware used `0xFFFF` for «conversion failed», correctly, across its own commands. The
legacy consumer in another repo clamped ADC-to-dBm, so `0xFFFF` decoded to **0 dBm — perfect output**.
Three unmeasurable fields would have made a device with a disconnected detector look *healthy*. They
had to be sent at the *minimum* of the range instead, which decodes to an alarm.

### A chain wired at both ends and empty in the middle raises nothing

A queue with a consumer and no producer is not an error in any layer. The consumer waits, the
endpoint returns blanks, the collection stays empty, the subscriber never fires — and all of it
looks exactly like "nothing happened yet".

Evidence: `gateway_status` had a consumer, a collection, an HTTP endpoint and a WebSocket event, and
the frontend subscribed to it. Nobody ever published. It went unnoticed because the panel showed the
result from the **synchronous HTTP response** of the same operation, so the visible path worked. The
producer had even been designed — the publisher's own signature accepted the non-durable flag and
its docstring named that queue.

**Rule:** when auditing a chain, enumerate producers and consumers **separately** and diff the two
sets. Do not follow the path from one end: a hop with nobody on the other side answers the same as
one that simply has no traffic yet.

**Rule:** before choosing a sentinel for a cross-repo format, read the consumer's decoder. If it
cannot express absence, pick the value that **raises an alarm**, not the one that reassures — a false
warning gets investigated, a false healthy kills equipment. And state the choice where it is made.

Evidence: a command marked destructive in one repo's docs was harmless there and destructive under
a different code; fixes to a shared submodule lived on a single machine while two other products
kept the same bugs.

---

## Irreversible Operations

Deleting infrastructure, releasing an address, dropping data. The class where being right afterwards
is worthless.

| Rule | Why |
|---|---|
| Snapshot **before** deleting, and verify the snapshot is `READY` with non-zero size | a restore point you intended is not a restore point you have |
| Delete the **name** before the **address** | a DNS record left pointing at a released IP is a subdomain takeover, and the window is real |
| Deleting a parent does not delete its children | a disk with `autoDelete=false` outlives its VM and keeps billing, invisibly |
| Order the work by **increasing risk**, not decreasing cost | the cheapest safe action first buys information for the expensive one |
| Waking a dormant system can act **outward** | queued jobs fire on boot; cut the outbound path *before* starting, not after |

### Identify by effect, not by name

Names are opinion; routing is fact. Before touching anything, resolve the chain end to end: what does
the public record point to, what is that address attached to, what is actually running, and what does
it serve when you bypass the name entirely.

Evidence: the production website ran on a VM called `...-test-...`, while the instance named like the
official one had been off for months. Anyone reading the inventory would have concluded the opposite.

### A backup that exists is not a backup that works

Same failure class as **Verification Integrity**: the existence of a backup is the intention, its
restorability is the effect. Compare its size against the source before trusting it.

Evidence: a machine image of a 300 GB disk weighed **0.2 GB**; a fresh snapshot of the same disk
weighed **26.9 GB**. That "backup" had been empty for years and nobody knew.

### A protection flag is a human signal, not an obstacle

When a resource carries a deliberate lock (deletion protection, immutability, a branch rule), stopping
and asking is the correct behaviour. Removing it is a decision that belongs to whoever set it.

Evidence: the locks in one project turned out to mark exactly the real services, while every
unprotected resource was an experiment. The flag encoded knowledge no inventory did.

---

## State With No Age

> A stored value can be **true and expired at the same time**. Verification Integrity asks whether
> a confirmation looks at the effect; this asks whether the effect it looked at is **still true**.

A field written only when new data arrives keeps its last value forever. Nothing is corrupted,
nothing errors, and every layer that renders it repeats a statement that stopped being true.

Evidence: `devices.status` was written only on measurement arrival. A device that lost power kept
`healthy` **in the table and green on the map**, while a separate watchdog was already raising a
silence alert for it. Three views of the same equipment, two of them lying. The only clue was a
`last_seen` in absolute format, which makes the reader do the arithmetic.

| Rule | Why |
|---|---|
| Present derived state **with its age**, never alone | the age is what turns a value into a claim about *now* |
| Show elapsed time, not a timestamp, when the question is freshness | "3 min ago" answers it; "13/08/2026, 20:35:11" delegates it to the reader |
| Past the threshold, show the **staleness**, not the stored value | keep the reported value visible, but as history: in a tooltip, dated |
| The UI threshold must be the **same one** the alarm uses, read from the same place | otherwise the screen and the alert tell different stories about the same device |
| A value that never arrived is not the same as one that expired | "never" and "stale" have different causes and different fixes |

### The same entity, keyed differently in the same store

A reader that assumes one identifier field silently drops whole families — an empty id is not an
error anywhere, it is a row that quietly stops existing.

Evidence: `devices` held `device_id`, `vlad_id` and `amplifier_id_str` for three families. A new
watchdog read only `device_id`; two of the three families disappeared from supervision **without a
single error**, and the one device on the bench would never have alerted.

**Rule:** when several producers write to one collection, enumerate the identity fields before
reading it, and make the reader fail loudly on an unrecognised shape rather than skipping it.

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

### A decision written as a pending item invites its own reversal

"Not configurable **yet**", "still pending" and "TODO" describe a gap. If what is really there is a
**decision**, that wording asks the next reader — or the next agent — to undo it.

**Rule:** write the decision, its reason, and the observation that would change it. "It stays a
constant because this family is going to be replaced; if it starts needing adjustment often, that is
the signal that the decision changed."

Evidence: a comment saying a family's alert config "does not exist yet" was written by the same
person who had just decided it never would.

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

### Duplication guarded by a comment is not a mechanism

`@mirror-of ... keep in sync` is a wish. It has no enforcement and no failure mode: the copies drift
and nothing reports it.

Evidence, all found the same day: one mirror's label table named five alert types its device never
emitted and none of the six it did; two modals kept their labels in a language the product had
migrated away from; and the `@mirror-of` pointers themselves referenced a directory deleted hours
earlier. **The mirror could not keep its own pointer current.**

**Rule:** if two files must stay identical, make them one file with a parameter. If they must differ,
delete the comment and say what differs and why — a promise nobody can keep is worse than none,
because it stops the next reader from looking.

### Before proposing a removal, check the thing is actually duplicated

Surface similarity is not sameness. Three files of the same length and shape can be three different
problems.

Evidence: three dashboards looked like triplets and a single list with a filter was proposed. Their
columns were 8, 15 and 8 **and disjoint**: the merged table would have had ~25 columns with each row
filling 4 to 8. What was duplicated was the scaffolding — search, pagination, export, empty state —
not the columns, which are the part that *must* differ.

**Rule:** compare what the files *say*, not how they look. Diff the data they render before
concluding one of them is redundant.

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
