# .cursorrules — Cursor Adapter for TCode
# Template for use with the Cursor editor (cursor.sh).
# Rename this file to .cursorrules and place it at the workspace root.
# Read FRAMEWORK.md for all SDLC standards — only developer choices live here.

---

## Framework

This workspace uses the TCode SDLC framework. Read `FRAMEWORK.md` before starting
any task. The full quality standards, project structure, and memory protocol are there.

## Memory + Validation Protocol

At session start:
- Read `memory/MEMORY.md` (stable facts) and `memory/task_plan.md` (current goals)
- If inside a project: also read `projects/<name>/memory/MEMORY.md` and `task_plan.md`
- If project has `runtime/`: read `runtime/regime.md` and `runtime/latest.json`
- Before starting work: note any contradictions between memory claims and runtime state

At session end:
- Append a summary to `memory/sessions/YYYY-MM-DD.md`
- Update `memory/task_plan.md` and `memory/MEMORY.md` as needed
- If project has `runtime/`: compare memory claims against `runtime/latest.json`
  and add `## Validation Reconciliation` to session log if discrepancies exist
- If same validation failure recurs 2+ sessions: append to `runtime/decisions.md`

Full validation protocol: `validation/VALIDATION.md`.

## Developer Preferences

- **Language:** [Python / TypeScript / Go / …]
- **Framework:** [FastAPI / Express / …]
- **Database:** [SQLite / PostgreSQL / …]
- **Testing:** [pytest / jest / …]

## Hard Rules (from FRAMEWORK.md — do not override)

- Prompts are `.txt` files — never inline strings in code
- No hardcoded secrets — `.env` files only, never committed
- No dead code in committed files
- No gold-plating — current phase scope only
- Tests must pass before committing

## Projects

| Folder | Description |
|---|---|
| | |

## Commit Format

Conventional Commits with `Coding-Agent:` and `Model:` trailers.
Example: `feat: add receipt OCR pipeline\n\nCoding-Agent: Cursor\nModel: claude-4-sonnet`
