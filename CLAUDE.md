# CLAUDE.md — Claude Code Adapter
# This is the Claude Code adapter for the TCode framework.
# Read FRAMEWORK.md first — it contains all SDLC standards and conventions.
# This file adds only what is Claude Code-specific plus this developer's choices.
# Project-level CLAUDE.md files extend and override these defaults.

---

## Read First

Before doing anything else, read:
1. `FRAMEWORK.md` — the canonical framework spec (SDLC standards, project structure, memory system)
2. `memory/MEMORY.md` — stable workspace facts
3. `memory/task_plan.md` — current cross-project goals

---

## Developer Identity & Goals

- **Role:** [e.g. solo developer, product-focused engineer, researcher]
- **Primary domains:** [e.g. healthcare, fintech, internal tooling]
- **Typical project stage:** [e.g. POC to production, rapid prototyping, enterprise-grade]

---

## Technology Defaults (This Developer's Choices)

Override these per project in its own CLAUDE.md if the project needs something different.

| Concern | Default | Notes |
|---|---|---|
| Backend language | Python | FastAPI preferred for APIs |
| Frontend | None (API-first) | Add only when explicitly required |
| Database | SQLite (dev) / PostgreSQL (prod) | |
| LLM integration | Anthropic Claude API | Use `anthropic` Python SDK |
| LLM provider fallback | OpenAI | Use `openai` Python SDK |
| Testing | pytest | |
| Dependency management | pip + requirements.txt | |
| Containerisation | Docker + docker-compose | Optional for POCs |

> Customise the table above to reflect your own stack preferences.

---

## Projects in This Workspace

| Folder | Type | Description |
|---|---|---|
| `projects/my-first-app` | POC | Example — replace with your own projects |

> Add new projects here as they are created. See `new_project.py` to scaffold one.

---

## DevOps

All git and repository operations use the provider-agnostic system in `devops/`.
Config: `devops/config.yaml` (copy from `devops/config.example.yaml`, never commit).

Commit format: Conventional Commits + `Coding-Agent:` / `Model:` trailers.
Full docs: `devops/DEVOPS.md`.

---

## Session Bootstrap Protocol (Claude Code)

At the **start of every session**, read in this order:
1. `FRAMEWORK.md`
2. `memory/MEMORY.md`
3. `memory/task_plan.md`
4. Most recent `memory/sessions/YYYY-MM-DD.md` if resuming interrupted work

At the **end of every session**, write:
1. Append a session summary to `memory/sessions/YYYY-MM-DD.md` (create if needed)
2. Update `memory/task_plan.md` — mark completed items, add newly surfaced tasks
3. Update `memory/MEMORY.md` if any new stable facts were established

When working inside a project, apply the same protocol at the project `memory/` level.
