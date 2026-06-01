---
name: "STM32 Audit Loop"
description: "Iterative simplicity audit loop for STM32 firmware. Keeps auditing and fixing until no more findings remain."
mode: agent
---

You are running a **convergence loop** audit on an STM32 firmware project. Your goal is to iterate until the codebase has **zero remaining simplicity or correctness findings**.

## Loop Protocol

Repeat the following cycle until the exit condition is met:

### Step 1 — Read
Read ALL user-code sections of every `.cpp` and `.c` file in `Core/Src/` and every `.hpp` / `.h` in `Core/Inc/`. Do not skip HAL-generated files (they are read-only — skip them).

### Step 2 — Audit
Apply the **full simplicity checklist** from Section 16.3 of the stm32-expert instructions:

1. Unused `#include`
2. `#define` / `typedef` used < 2 times → inline
3. Globals written but never read, or read from only one place
4. Functions reachable from 0 call sites (dead functions)
5. Functions reachable from exactly 1 call site → consider inline
6. Switch `case` entries that are no-ops (only `break` or a comment)
7. Null guards on pointers that cannot be null at that point
8. Comments that say *what* the code does (not *why*)
9. Stale or incorrect docblocks
10. Unreachable `#if` / `#else` branches
11. Dead variables (written but never read after the write)
12. Duplicate log calls that can be merged
13. Redundant `memset` / `memcpy` of already-zeroed data
14. `new`/`delete` for objects with static lifetime

Also apply the **correctness checklist**:
- Unchecked HAL return values
- `volatile` missing on ISR-shared variables
- `HAL_Delay()` inside ISR or main loop (use `HAL_GetTick()` delta instead)
- Buffer size mismatches

### Step 3 — Report
Output a numbered table of ALL findings:

| # | File | Line/Function | Severity | Description |
|---|------|--------------|----------|-------------|

Severity: `CRITICAL` / `WARNING` / `SIMPLICITY`

**If the table is empty → print "✅ No findings. Audit complete." and stop.**

### Step 4 — Fix
Apply ALL findings from Step 3 in a single `multi_replace_string_in_file` call per file.

### Step 5 — Compile
Run the syntax-only compile check:

```powershell
$gcc = "C:\ST\STM32CubeIDE_1.19.0\STM32CubeIDE\plugins\com.st.stm32cube.ide.mcu.externaltools.gnu-tools-for-stm32.13.3.rel1.win32_1.0.0.202411081344\tools\bin\arm-none-eabi-g++.exe"
$p = "firmware\projects\gateway-2lora"
Set-Location "c:\Users\artur\development\products\leaky-feeder\fw-gateway2Lora"
& $gcc "$p\Core\Src\main.cpp" -mcpu=cortex-m4 -std=gnu++14 -DDEBUG -DUSE_HAL_DRIVER -DSTM32G474xx -fno-exceptions -fno-rtti -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -fsyntax-only "-I$p\Core\Inc" "-I$p\Drivers\STM32G4xx_HAL_Driver\Inc" "-I$p\Drivers\CMSIS\Device\ST\STM32G4xx\Include" "-I$p\Drivers\CMSIS\Include" 2>&1 | Out-File C:\Temp\audit_loop.txt
$rc = $LASTEXITCODE
if ($rc -eq 0) { "CLEAN" } else { Get-Content C:\Temp\audit_loop.txt }
"EXIT:$rc"
```

**If RC ≠ 0**: fix all compiler errors before continuing. Do not proceed to Step 6 with errors.

### Step 6 — Commit
```
git add <changed files>
git commit -m "refactor: simplicity audit loop — iteration N

<bullet list of what was removed/simplified>"
git push origin main
```

### Step 7 — Loop
Go back to **Step 1** and audit again.

## Exit Condition

The loop ends when **Step 2 produces zero findings** AND the compile is clean (RC=0).

Print the final summary:
```
## Audit Loop Complete

Iterations: N
Total findings fixed: X
Net lines removed: Y
Final commit: <hash>
```

## Rules

- Never invent functionality. Only remove or simplify existing code.
- Never change hardware pin assignments, baud rates, or interrupt priorities unless that is explicitly the finding.
- Never change `.ioc` files or HAL-generated MX_ functions.
- If a finding requires understanding context (e.g., "is this function called from anywhere?"), use `grep_search` before removing it.
- If unsure whether a removal is safe, mark it `[SKIP — needs confirmation]` and continue with the rest.
