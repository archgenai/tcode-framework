# GitHub Copilot Instructions — TCode Adapter
# Template for use with GitHub Copilot.
# Rename to .github/copilot-instructions.md and place at the workspace root.
# Read FRAMEWORK.md for all SDLC standards — only developer choices live here.

## Framework Context

This workspace uses the TCode SDLC framework. Full standards are in `FRAMEWORK.md`.
Before any task: read `FRAMEWORK.md`, `memory/MEMORY.md`, and `memory/task_plan.md`.

## Session Protocol

Start: read `memory/MEMORY.md` + `memory/task_plan.md`. If in a project, read the
project-level equivalents too.

End: update `memory/task_plan.md`, append `memory/sessions/YYYY-MM-DD.md`, update
`memory/MEMORY.md` if new stable facts emerged.

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

## Commit Convention

Conventional Commits + trailers:
```
feat: short description

Body (optional).

Coding-Agent: GitHub Copilot
Model: gpt-4o
```
