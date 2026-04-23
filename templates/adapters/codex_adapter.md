# OpenAI Codex Adapter for TCode
#
# OpenAI Codex CLI reads AGENTS.md files at the repo root and in parent directories.
# It also reads ~/.codex/instructions.md for user-level global instructions.
#
# Usage:
#   Workspace level : place content in AGENTS.md at TCode root
#   Project level   : place content in projects/<name>/AGENTS.md
#   User level      : place content in ~/.codex/instructions.md (Codex-only, not versioned)
#
# TCode already ships an AGENTS.md that Codex can read. Use this template if you want
# a Codex-optimised version that replaces or extends the default AGENTS.md.
# ─────────────────────────────────────────────────────────────────────────────

# AGENTS.md — TCode Workspace (Codex-optimised)

## Framework

This workspace uses the TCode SDLC framework.
Read `FRAMEWORK.md` before starting any task — it contains all quality standards,
project structure rules, the memory protocol, and the devops reference.

## Workspace Layout

```
TCode/
├── FRAMEWORK.md        ← Canonical SDLC spec (READ THIS FIRST)
├── AGENTS.md           ← This file — Codex entry point
├── CLAUDE.md           ← Claude Code adapter (if also using Claude Code)
├── devops/             ← Provider-agnostic VCS / CI tooling
├── memory/             ← Workspace persistent context
│   ├── MEMORY.md       ← Stable facts (read every session)
│   ├── task_plan.md    ← In-flight work (read every session)
│   └── sessions/       ← Session logs YYYY-MM-DD.md
├── prompts/            ← Shared LLM prompt fragments
│   ├── shared/
│   └── system/
├── templates/
│   └── adapters/       ← Agent adapter templates
└── projects/
    └── <app-name>/
        ├── AGENTS.md   ← Project-level Codex context
        ├── REQUIREMENTS.md
        ├── STACK.md
        ├── prompts/
        └── memory/
```

## Session Protocol

**Start of every session:**
1. Read `FRAMEWORK.md`
2. Read `memory/MEMORY.md` — stable workspace facts
3. Read `memory/task_plan.md` — current goals and in-flight work
4. If working inside a project: also read `projects/<name>/memory/MEMORY.md`
   and `projects/<name>/memory/task_plan.md`
5. If resuming interrupted work: read the most recent `memory/sessions/YYYY-MM-DD.md`

**End of every session:**
1. Append a summary to `memory/sessions/YYYY-MM-DD.md` (create if needed)
2. Update `memory/task_plan.md` — mark completed items, add new tasks
3. Update `memory/MEMORY.md` if new stable facts were established
4. Apply the same writes at the project level if you worked inside a project

## Non-Negotiable Rules

These come from `FRAMEWORK.md` and cannot be overridden at project level:

- Load all LLM prompts from `.txt` files — never inline prompt strings in code
- No hardcoded credentials — environment variables only; never commit `.env`
- Always provide `.env.example` documenting every required variable
- No dead code, no commented-out blocks in committed files
- No features outside the current phase scope (no gold-plating)
- Eager-load all ORM relationships — no lazy loading
- Parse and validate all LLM responses before storing or returning them
- `tests/unit/` and `tests/integration/` must pass before any push

## Developer Stack

- **Language:** [Python / TypeScript / Go / …]
- **API framework:** [FastAPI / Express / …]
- **Database:** [SQLite / PostgreSQL / …]
- **LLM provider:** [Anthropic / OpenAI / …]
- **Testing:** [pytest / jest / …]

## Projects

| Folder | Type | Description |
|---|---|---|
| | | |

> Add a row here for each project.

## Commit Format

Conventional Commits with agent trailers:

```
feat: short description

Optional body.

Coding-Agent: OpenAI Codex
Model: codex-1
```

---

# ~/.codex/instructions.md — User-Level Global Instructions (optional)
#
# The block below is a template for ~/.codex/instructions.md.
# Copy it there to apply TCode preferences globally across ALL your repos,
# not just this workspace. Do NOT version-control this file — it is personal.
#
# ─────────────────────────────────────────────────────────────────────────────
#
# I follow the TCode SDLC framework in all my projects.
#
# Universal rules that apply everywhere:
# - Always read AGENTS.md and FRAMEWORK.md (if present) at session start
# - Read memory/MEMORY.md and memory/task_plan.md before starting work
# - Update memory files at session end
# - Conventional Commits with Coding-Agent: and Model: trailers
# - No hardcoded secrets; no committed .env files
# - No gold-plating; build only what is in scope
# - Tests must pass before pushing
#
# My preferred stack:
# - Language: [Python / TypeScript]
# - Framework: [FastAPI / Express]
# - Testing: [pytest / jest]
# ─────────────────────────────────────────────────────────────────────────────
