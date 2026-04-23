# [App Name] — Project Memory
# Type: semantic — stable facts about this project.
# Updated by Claude at session end when new stable facts are established.
# Read at the start of every session alongside the root memory/.

---

## Project Identity

**Name:** [app-name]
**Type:** [POC / MVP / prod]
**Purpose:** [One sentence — what this app does and for whom.]
**Current Phase:** Phase [N] — [Phase name]

## Architecture Decisions

| Decision | Choice | Reason | Date |
|---|---|---|---|
| | | | |

> Record significant choices here. Minor implementation details go in STACK.md.

## Key Constraints

- [e.g. No patient data leaves the local machine]
- [e.g. All routes except /webhook require JWT validation]

## Prompt Inventory

Prompts for this project live in `prompts/`:

| File | Purpose |
|---|---|
| `prompts/system/system_prompt.txt` | Base system prompt |

> Keep this table in sync when prompts are added or renamed.

## Known Gotchas

> Things that tripped up development and are not obvious from the code.

- [e.g. Telegram webhook requires HTTPS even in dev — use ngrok]
