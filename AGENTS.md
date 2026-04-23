# AGENTS.md — TCode Workspace
# Entry point for coding agents that follow the AGENTS.md standard.
# (Cursor, GitHub Copilot, Devin, Aider, and others read this file.)
#
# TCode uses a framework + adapter pattern.
# FRAMEWORK.md is the canonical spec — read it first.
# The agent-specific adapter (CLAUDE.md, .cursorrules, etc.) adds syntax on top.

---

## What This Workspace Is

TCode is a portable SDLC framework for AI-assisted development.
Each project under `projects/` inherits workspace conventions and adds its own
architecture, constraints, and phase plan.

**Canonical spec:** `FRAMEWORK.md`
**Current agent adapter:** `CLAUDE.md` (Claude Code)

---

## Quick-Start (any agent)

1. Read `FRAMEWORK.md` — SDLC standards, project structure, memory protocol
2. Read `memory/MEMORY.md` — stable workspace facts
3. Read `memory/task_plan.md` — current goals and in-flight work
4. If working inside a project: also read `projects/<name>/memory/MEMORY.md`
   and `projects/<name>/memory/task_plan.md`

At session end: update the task plan, append a session log, update MEMORY.md
with any new stable facts.

---

## Non-Negotiable Rules

These apply regardless of agent or project. Full rationale is in `FRAMEWORK.md`.

- Prompts are `.txt` files loaded by path — never inline strings in code
- No hardcoded secrets — use `.env` files, never commit them
- No dead code, no commented-out blocks in committed code
- No gold-plating — build only what is in scope for the current phase
- No ORM lazy loading — always eager-load related objects
- No raw LLM responses stored — always parse and validate before saving
- Tests must pass before pushing: `tests/unit/` and `tests/integration/`

---

## Workspace Layout

```
TCode/
├── FRAMEWORK.md        ← Canonical SDLC spec (read this)
├── CLAUDE.md           ← Claude Code adapter
├── AGENTS.md           ← This file
├── devops/             ← Provider-agnostic VCS / CI tooling
├── prompts/            ← Shared LLM prompt fragments
├── memory/             ← Workspace-level persistent context
├── templates/
│   ├── adapters/       ← Adapter templates for Claude, Cursor, Copilot
│   └── ...
└── projects/
    └── <app-name>/
        ├── <adapter>   ← Project-level agent adapter
        ├── REQUIREMENTS.md
        ├── STACK.md
        ├── prompts/
        └── memory/
```

---

## Using a Different Agent

Adapter templates for other coding agents live in `templates/adapters/`:

| Agent | Template | Output filename |
|---|---|---|
| Claude Code | `templates/adapters/claude_adapter.md` | `CLAUDE.md` |
| Cursor | `templates/adapters/cursor_adapter.md` | `.cursorrules` |
| GitHub Copilot | `templates/adapters/copilot_adapter.md` | `.github/copilot-instructions.md` |
| OpenAI Codex | `templates/adapters/codex_adapter.md` | `AGENTS.md` |

Copy the relevant template, fill in developer-specific sections, place at workspace root.
The framework itself (`FRAMEWORK.md`, `devops/`, `memory/`, `templates/`) needs no changes.
