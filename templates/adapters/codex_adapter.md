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
│   ├── adapters/       ← Agent adapter templates
│   └── PROMPT_ZERO.md  ← Master Prompt Zero template
├── promptZero/         ← Pre-kickoff structured planning prompts
│   └── <app-slug>/
│       └── promptZero.md
├── tools/
│   └── prompt-zero/    ← Web UI: generate Prompt Zero documents
└── projects/
    └── <app-name>/
        ├── AGENTS.md   ← Project-level Codex context
        ├── REQUIREMENTS.md
        ├── STACK.md
        ├── prompts/
        └── memory/
```

## Prompt Zero

Before creating any new project, generate a Prompt Zero document first.
Use `tools/prompt-zero/` (web UI) or fill `templates/PROMPT_ZERO.md` by hand.
Save to `promptZero/<app-slug>/promptZero.md` and paste into the agent.
Full protocol: `FRAMEWORK.md § Prompt Zero`.

## Session Protocol

**Start of every session:**
1. Read `FRAMEWORK.md`
2. Read `memory/MEMORY.md` — stable workspace facts
3. Read `memory/task_plan.md` — current goals and in-flight work
4. If resuming interrupted work: read the most recent `memory/sessions/YYYY-MM-DD.md`
5. If working inside a project, also read:
   - `projects/<name>/memory/MEMORY.md` and `task_plan.md`
   - `projects/<name>/runtime/regime.md` — validation gates (if exists)
   - `projects/<name>/runtime/latest.json` — most recent CI/deploy state (if exists)
   - Before starting any work: note contradictions between memory claims and runtime state

**End of every session:**
1. Append a summary to `memory/sessions/YYYY-MM-DD.md` (create if needed)
2. Update `memory/task_plan.md` — mark completed items, add new tasks
3. Update `memory/MEMORY.md` if new stable facts were established
4. Apply the same memory writes at the project level if you worked inside a project
5. If project has `runtime/`:
   - Compare memory claims against `runtime/latest.json`
   - Add `## Validation Reconciliation` to the session log if any discrepancy exists
   - If the same validation failure recurred across 2+ sessions, append an entry to
     `projects/<name>/runtime/decisions.md`

Full validation protocol: `validation/VALIDATION.md`.

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

OpenAI Codex does not currently have a hook/command harness equivalent to Claude Code's
`.claude/`. The execution layer for this workspace is implemented in Claude Code (`.claude/`).
See `FRAMEWORK.md §Execution Layer` for the full three-layer model and placement rules.
When Codex ships a comparable harness, build the Codex execution rail using that spec.

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
