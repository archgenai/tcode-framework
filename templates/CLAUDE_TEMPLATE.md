# CLAUDE.md — [App Name]
# Claude Code project-level adapter.
# Inherits all rules from the workspace FRAMEWORK.md and root CLAUDE.md.
# Only record here what is different from or additional to those defaults.

---

## Read First

At session start, read in order:
1. `../../FRAMEWORK.md` — canonical SDLC spec
2. `../../memory/MEMORY.md` and `../../memory/task_plan.md` — workspace context
3. `memory/MEMORY.md` and `memory/task_plan.md` — this project's context
4. Most recent `memory/sessions/YYYY-MM-DD.md` if resuming interrupted work

---

## Project Purpose

[One short paragraph: what the app does, for whom, and why it matters.]

---

## Architecture Overview

[Describe the high-level shape of the system: major components, how data flows, what calls what.]

```
[ASCII diagram or bullet list]
```

---

## Language & Framework Decisions

> Only list overrides from root CLAUDE.md defaults. If a choice matches the root default, omit it.

| Concern | Choice | Override Reason |
|---|---|---|
| Language | | |
| Web framework | | |
| Database | | |
| LLM integration | | |
| Testing | | |

Full stack details are in `STACK.md`.

---

## Project-Specific Conventions

> Only conventions specific to THIS project — not already in FRAMEWORK.md or root CLAUDE.md.

- [e.g. "All patient data is anonymised before being sent to any external API"]
- [e.g. "Report parsing logic lives in `core/parsers/`, one file per report type"]

---

## File Layout

```
src/
├── api/          # HTTP layer (routes, request/response models)
├── core/         # Business logic (no framework imports here)
├── db/           # Database models and repository classes
├── prompts/      # LLM prompt templates (plain .txt files)
├── services/     # Orchestration — calls core + db + external APIs
└── main.py       # Entry point
tests/
├── unit/
└── integration/
```

---

## What NOT to Do (Project-Specific)

> Project-specific prohibitions only. Universal ones are in FRAMEWORK.md.

- [e.g. "Do not add authentication — explicitly out of scope for v1"]

---

## Current Phase

Phase [N] — [Phase name]
See `REQUIREMENTS.md` for full phase breakdown.

---

## Open Decisions

| Decision | Options | Status |
|---|---|---|
| | | |

---

## Prompt Registry

All LLM prompts for this project live in `prompts/`, organised by feature:

```
prompts/
├── system/
│   └── system_prompt.txt
└── <feature>/
    └── <task>.txt
```

Workspace-wide shared fragments are in `../../prompts/shared/`.

---

## Session End Protocol

1. Append summary to `memory/sessions/YYYY-MM-DD.md`
2. Update `memory/task_plan.md` — completed items and next tasks
3. Update `memory/MEMORY.md` if new stable facts were established
