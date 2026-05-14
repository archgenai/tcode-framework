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

## Prompt Zero

Before creating any new project, generate a Prompt Zero document first.
Use the web UI at `tools/prompt-zero/` or fill `templates/PROMPT_ZERO.md` by hand.
Save the result to `promptZero/<app-slug>/promptZero.md` and paste it into the agent.
Full protocol: `FRAMEWORK.md § Prompt Zero`.

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

---

## Multi-Agent Orchestrator Protocol (Claude Code)

When this session acts as an **orchestrator** spawning sub-agents via the `Agent` tool,
the following rules apply. Full spec: `FRAMEWORK.md §Multi-Agent Protocol`.

**Before spawning any sub-agent**, include this block verbatim at the top of the agent prompt:

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

**After all sub-agents return**, the orchestrator must:
1. Reconcile their summaries into workspace `memory/task_plan.md` and `memory/sessions/YYYY-MM-DD.md`
2. Update workspace `memory/MEMORY.md` if cross-project stable facts changed
3. Perform the session-end commit and push

---

## Execution Layer (Claude Code)

Claude Code is the reference implementation of TCode's execution layer. The execution
layer sits in `.claude/` and automates what the declarative layer instructs.
Full spec: `FRAMEWORK.md §Execution Layer`.

**Standard workspace commands** (invoke as slash commands):

| Command | File | Purpose |
|---|---|---|
| `/review` | `.claude/commands/review.md` | Framework compliance + linting + test suite report |
| `/session-end` | `.claude/commands/session-end.md` | Full TCode session-end protocol |
| `/prompt-zero` | `.claude/commands/prompt-zero.md` | Prompt Zero planning workflow for a new project |

**Hooks** in `.claude/settings.json`:
- `Stop` — runs the test suite if `tests/` exists
- `PostToolUse:Bash` — logs tool activity to the session log

Add project-specific commands to `projects/<name>/.claude/commands/`.
Command template: `templates/commands/command_template.md`.
