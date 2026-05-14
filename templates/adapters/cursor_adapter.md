# .cursorrules — Cursor Adapter for TCode
# Template for use with the Cursor editor (cursor.sh).
# Rename this file to .cursorrules and place it at the workspace root.
# Read FRAMEWORK.md for all SDLC standards — only developer choices live here.

---

## Framework

This workspace uses the TCode SDLC framework. Read `FRAMEWORK.md` before starting
any task. The full quality standards, project structure, and memory protocol are there.

## Prompt Zero

Before creating any new project, generate a Prompt Zero document first.
Use `tools/prompt-zero/` (web UI) or fill `templates/PROMPT_ZERO.md` by hand.
Save to `promptZero/<app-slug>/promptZero.md` and paste into the agent.
Full protocol: `FRAMEWORK.md § Prompt Zero`.

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

## Multi-Agent Protocol

When acting as an **orchestrator** spawning sub-agents, prepend this block to every
sub-agent prompt. Full spec: `FRAMEWORK.md §Multi-Agent Protocol`.

```
## TCode Bootstrap (read before doing anything)
1. Read FRAMEWORK.md — §Session Bootstrap, §Multi-Agent Protocol, §Memory System
2. Read memory/MEMORY.md — stable workspace facts (read-only)
3. Read memory/task_plan.md — cross-project goals (read-only)
4. Read projects/<name>/memory/MEMORY.md and task_plan.md
5. If the project has runtime/regime.md and runtime/latest.json, read them and
   surface any contradiction with memory claims before starting work

## TCode Session End (before returning your result)
1. Append a summary to projects/<name>/memory/sessions/YYYY-MM-DD.md
2. Update projects/<name>/memory/task_plan.md — mark completed items, add blockers
3. Update projects/<name>/memory/MEMORY.md if new stable facts were established
4. Do NOT write to workspace-level memory/ — include what you did in your return message
5. Do NOT commit or push — the orchestrator handles version control
```

After sub-agents return: reconcile summaries into workspace memory, then commit and push.

## Execution Layer

Cursor does not currently have a hook/command harness equivalent to Claude Code's `.claude/`.
The execution layer for this workspace is implemented in Claude Code (`.claude/`).
See `FRAMEWORK.md §Execution Layer` for the full three-layer model and placement rules.
When Cursor ships a comparable harness, build the Cursor execution rail using that spec.

## Commit Format

Conventional Commits with `Coding-Agent:` and `Model:` trailers.
Example: `feat: add receipt OCR pipeline\n\nCoding-Agent: Cursor\nModel: claude-4-sonnet`
