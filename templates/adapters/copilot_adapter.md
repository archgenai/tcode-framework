# GitHub Copilot Instructions — TCode Adapter
# Template for use with GitHub Copilot.
# Rename to .github/copilot-instructions.md and place at the workspace root.
# Read FRAMEWORK.md for all SDLC standards — only developer choices live here.

## Framework Context

This workspace uses the TCode SDLC framework. Full standards are in `FRAMEWORK.md`.
Before any task: read `FRAMEWORK.md`, `memory/MEMORY.md`, and `memory/task_plan.md`.

## Prompt Zero

Before creating any new project, generate a Prompt Zero document first.
Use `tools/prompt-zero/` (web UI) or fill `templates/PROMPT_ZERO.md` by hand.
Save to `promptZero/<app-slug>/promptZero.md` and paste into the agent.
Full protocol: `FRAMEWORK.md § Prompt Zero`.

## Session Protocol

**Start:** Read `memory/MEMORY.md` + `memory/task_plan.md`. If in a project, also read
project-level `memory/` equivalents, plus `runtime/regime.md` and `runtime/latest.json`
(if they exist). Before starting any work, note contradictions between memory claims
and runtime state and surface them explicitly.

**End:** Update `memory/task_plan.md`, append `memory/sessions/YYYY-MM-DD.md`, update
`memory/MEMORY.md` if new stable facts emerged. If project has `runtime/`, compare memory
claims against `runtime/latest.json` and record discrepancies in the session log under
`## Validation Reconciliation`. If the same failure recurs 2+ sessions, append to
`runtime/decisions.md`.

Full validation protocol: `validation/VALIDATION.md`.

## Developer Stack

- Language: [Python / TypeScript / Go / …]
- API framework: [FastAPI / Express / …]
- Database: [SQLite / PostgreSQL / …]
- Testing: [pytest / jest / …]
- LLM provider: [Anthropic / OpenAI / …]

## Non-Negotiable Rules

From `FRAMEWORK.md` — these cannot be overridden at project level:

1. Load all LLM prompts from `.txt` files — never inline them
2. No hardcoded credentials — environment variables only
3. No committed `.env` files — always provide `.env.example`
4. No dead code or commented-out blocks in committed files
5. No features outside the current phase scope
6. Eager-load all ORM relationships
7. Tests (`tests/unit/` + `tests/integration/`) must pass before pushing

## Workspace Projects

| Folder | Type | Description |
|---|---|---|
| | | |

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

GitHub Copilot does not currently have a hook/command harness equivalent to Claude Code's
`.claude/`. The execution layer for this workspace is implemented in Claude Code (`.claude/`).
See `FRAMEWORK.md §Execution Layer` for the full three-layer model and placement rules.
When Copilot ships a comparable harness, build the Copilot execution rail using that spec.

## Commit Convention

Conventional Commits + trailers:
```
feat: short description

Body (optional).

Coding-Agent: GitHub Copilot
Model: gpt-4o
```
