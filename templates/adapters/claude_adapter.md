# CLAUDE.md — Claude Code Adapter
# Template for use with Claude Code (claude.ai/claude-code).
# Place this file at the workspace root (or project root for project-level adapters).
# Read FRAMEWORK.md first — it contains all SDLC standards.
# Only record developer-specific choices and Claude-specific instructions here.

---

## Read First

Before doing anything else, read:
1. `FRAMEWORK.md` — canonical SDLC spec
2. `memory/MEMORY.md` — stable workspace facts
3. `memory/task_plan.md` — current goals

---

## Developer Identity & Goals

- **Role:** [solo developer / team lead / researcher / …]
- **Primary domains:** [healthcare / fintech / internal tooling / …]
- **Typical project stage:** [POC / MVP / production]

---

## Technology Defaults

Override per project in its own CLAUDE.md.

| Concern | Default | Notes |
|---|---|---|
| Backend language | Python | FastAPI preferred for APIs |
| Frontend | None (API-first) | Add only when spec requires it |
| Database | SQLite (dev) / PostgreSQL (prod) | |
| LLM integration | [Your preferred provider] | |
| Testing | pytest | |
| Dependency management | pip + requirements.txt | |

---

## Projects in This Workspace

| Folder | Type | Description |
|---|---|---|
| | | |

> Add a row here for each project you create.

---

## DevOps

Provider-agnostic tooling in `devops/`.
Config: `devops/config.yaml` — never commit.
Commit format: Conventional Commits + `Coding-Agent:` / `Model:` trailers.

---

## Session Bootstrap Protocol (Claude Code)

At **session start**, read:
1. `FRAMEWORK.md`
2. `memory/MEMORY.md` and `memory/task_plan.md`
3. Most recent `memory/sessions/YYYY-MM-DD.md` if resuming
4. If working inside a project, also read:
   - `projects/<name>/memory/MEMORY.md` and `task_plan.md`
   - `projects/<name>/runtime/regime.md` — validation gates (if exists)
   - `projects/<name>/runtime/latest.json` — most recent CI/deploy state (if exists)
   - **Before starting any work:** note contradictions between memory claims and runtime
     state and surface them explicitly.

At **session end**, write:
1. Append summary to `memory/sessions/YYYY-MM-DD.md`
2. Update `memory/task_plan.md`
3. Update `memory/MEMORY.md` if new stable facts were established
4. If project has `runtime/`:
   - Compare memory claims against `runtime/latest.json`
   - Add `## Validation Reconciliation` to session log if discrepancies exist
   - If same failure recurs 2+ sessions: append entry to `runtime/decisions.md`

Full validation protocol: `validation/VALIDATION.md`.
