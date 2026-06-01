---
description: 'Python conventions for DRS installer orchestrator and validation scripts'
applyTo: 'sw-drsmonitoring/**/*.py'
---

# Python Conventions for DRS Installer

## Scope

Use these rules for Python code related to installer orchestration, offline upgrades, prechecks, verification, reporting, and test tooling in `sw-drsmonitoring`.

## Core Principles

- Keep flows deterministic and restart-safe
- Prefer explicit errors over silent fallbacks
- Make operations idempotent whenever possible
- Preserve backwards compatibility for manifests and state files
- Fail fast on invalid inputs before side effects start

## CLI and Inputs

- Build CLIs with `argparse` and explicit defaults
- Validate required parameters in precheck stage
- Use clear, actionable error messages that include field names
- Keep option names consistent across scripts (for example `--manifest`, `--state-file`, `--dry-run`)

## State and File Safety

- Treat state writes as critical operations
- Write JSON state atomically: write temp file first, then replace
- Never partially update state after a failed step
- Include step name, timestamp, result, and error context in state transitions
- Use UTF-8 text encoding explicitly when reading and writing files

## Error Handling and Exit Codes

- Use typed exceptions for validation vs runtime failures
- Convert known failures into stable, documented exit codes
- Avoid broad `except Exception` unless re-raising with context
- Ensure dry-run and verify-only modes still report full validation failures

## Logging and Evidence

- Log by stage: precheck, pre-apply, backup, apply, verify, close
- Every failed stage must emit enough context to reproduce the issue
- Do not log secrets, credentials, or full tokens
- Keep logs machine-readable where practical (stable keys/messages)

## Integrity and Compatibility

- Validate manifest schema and compatibility before apply
- Verify artifact existence and checksum before any destructive step
- Reject unsupported version jumps with explicit guidance
- Keep compatibility matrix checks centralized in one module/function

## Testing

- Add unit tests for each new validation rule and failure path
- Cover positive and negative scenarios for CLI modes
- Preserve deterministic tests (no external network dependencies)
- Use temporary directories and fixtures instead of fixed host paths

## Code Style

- Prefer small functions with single responsibility
- Use type hints on public functions and key internal helpers
- Keep imports explicit and remove unused ones
- Use descriptive names for stages and transition helpers
