# /new-project
# TCode unified new-project interface.
# Single entry point for creating a new project — from idea to scaffolded, bootstrapped project.
#
# Replaces the dual-method workflow (prompt-zero + new_project.py) with one sequential flow:
#   Step 1  Plan       — gather idea, generate promptZero.md, classify against TCode Framework
#   Step 2  Gate       — present classification + plan, get developer approval before touching files
#   Step 3  Scaffold   — write the full project directory (what new_project.py wrote)
#   Step 4  Bootstrap  — generate project CLAUDE.md + REQUIREMENTS.md
#   Step 5  Register   — update workspace CLAUDE.md projects table + memory files
#   Step 6  Commit     — one clean commit for the new project
#
# Legacy: new_project.py remains as a standalone terminal fallback. It is no longer the
# primary interface. Do not invoke it during this command.

---

## When to use

- Starting any new project in this workspace
- Developer has an idea and wants to go from concept to scaffolded project in one session

## When NOT to use

- The project already has a promptZero.md AND a scaffolded folder — it is past this stage
- Mid-project re-planning (use /prompt-zero for that)

---

## Step 1 — Plan (Prompt Zero)

### 1a. Check for existing work

```bash
ls promptZero/
ls projects/
```

If `promptZero/<slug>/promptZero.md` already exists:
- Read it aloud to the developer as a summary
- Ask: continue from it, or start fresh?

If `projects/<slug>/` already exists: warn the developer and confirm before proceeding.

### 1b. Gather the idea

Collect the following through conversation. Do not present this as a form — ask naturally,
group related questions, infer what you can from context already in the conversation.

**Identity**
- Project name (working title is fine)
- Project type: POC / MVP / Production
- One-sentence description: what does it do for the user?

**Users & Problem**
- Who is the primary user and what is their context?
- What problem does it solve?
- What is the single most important outcome for the user?

**Scope**
- Core features in priority order (3–7; mark each MVP or Future)
- What is explicitly out of scope for v1?

**Data & Stack**
- What data flows in, and in what format?
- What does the app produce?
- Storage: None / SQLite / PostgreSQL / File system / Other
- Primary language (default: Python per workspace CLAUDE.md)
- Target environment: REST API / CLI / Web app / Desktop / Mobile / Other
- LLM/AI provider needed? (default: Claude/Anthropic)
- Auth required? Any other external integrations?

**Constraints**
- Privacy / compliance requirements
- Performance target
- Offline capable?
- Deployment target: local / Docker / cloud / not decided

**Validation**
- Will the project have automated tests? (default: yes)
- Test command (default: pytest / npm test)
- Lint command (default: ruff / eslint)
- Will it be deployed to a server or cloud?
- Health check URL (if known)

**Success criteria** — 2–3 acceptance tests in Given / When / Then form

### 1c. Generate promptZero.md

Derive the folder slug: project name → lowercase → hyphens. Example: "CareNav Mini" → `carenav-mini`.

```bash
mkdir -p promptZero/<slug>
```

Write a complete `promptZero/<slug>/promptZero.md` by filling `templates/PROMPT_ZERO.md`
with the gathered information.

---

## Step 2 — Gate (classify + get approval)

Read `FRAMEWORK.md` in full. Then classify and present to the developer:

### Classification

Choose one:
- `TCODE_READY` — framework covers this project as-is
- `TCODE_READY_WITH_MINOR_ADDITIONS` — small project-local additions needed; name them
- `TCODE_FRAMEWORK_EXTENSION_REQUIRED` — a framework capability is genuinely missing

If `TCODE_FRAMEWORK_EXTENSION_REQUIRED`:
- Name the missing capability precisely
- **STOP.** Do not scaffold. Surface the gap and wait for the developer to resolve it at
  the framework level before proceeding.

### Framework evaluation

Evaluate across five areas and note any concerns:

| Area | Question |
|---|---|
| Memory | Does the memory system cover this project's continuity needs? |
| Approvals | Are there decisions that need human approval gates? |
| Telemetry | Does the project need runtime observability beyond `runtime/latest.json`? |
| Deploy | Does the standard DevOps system cover the deploy target? |
| Agent governance | Are there multi-agent concerns not covered by the protocol? |

### Implementation plan preview

Present a phased plan (Phase 0 scaffold + Phase 1+ features) with deliverables and
test criteria per phase.

### Approval gate

Ask the developer:
> "Classification: [RESULT]. Does this plan look right? Shall I scaffold the project?"

**Do not proceed to Step 3 until the developer explicitly says yes.**

---

## Step 3 — Scaffold

Create the full project directory. Write each file — do not invoke `new_project.py`
(the wizard requires interactive terminal input; the slash command writes files directly).

### Directory structure to create

```
projects/<slug>/
├── APP_SPEC.md          ← filled from gathered inputs
├── STACK.md             ← stub with language + empty tables
├── .env.example         ← env vars implied by integrations
├── AGENTS.md            ← project-level tool-agnostic context
├── memory/
│   ├── MEMORY.md        ← project identity + architecture (stub)
│   ├── task_plan.md     ← Phase 1 tasks (from plan)
│   ├── decisions.md     ← initial scaffold ADR
│   └── sessions/
│       └── .gitkeep
├── prompts/
│   └── system/
│       └── system_prompt.txt   ← base system prompt stub
└── runtime/
    ├── regime.md        ← pre-filled from validation answers
    ├── latest.json      ← starter conforming to validation/schema/runtime.schema.json
    ├── decisions.md     ← VDR-001 initial entry
    └── events/
        └── .gitkeep
```

### File content guidelines

**APP_SPEC.md** — structured markdown with all 8 sections from the gathered inputs:
identity, users & problem, core features table, data (in/out/storage), integrations table,
constraints table, out of scope, success criteria.

**STACK.md** — stub: language, empty dependencies table, one architecture decision row
noting "Initial scaffold via /new-project".

**.env.example** — one variable per integration (ANTHROPIC_API_KEY, OPENAI_API_KEY, etc.)
plus a comment block for project-specific vars.

**AGENTS.md** — project identity, key locations tree, hard rules, session bootstrap
instructions referencing both memory/ and runtime/.

**memory/MEMORY.md** — project identity block (name, type, purpose, current phase).
Architecture and key constraints sections left as stubs to be filled after CLAUDE.md is
generated.

**memory/task_plan.md** — current phase, Phase 1 tasks derived from the plan, blockers: None.

**memory/decisions.md** — ADR-001 recording the initial scaffold and Prompt Zero classification.

**prompts/system/system_prompt.txt** — concise system prompt: role, output format rules,
never invent data.

**runtime/regime.md** — pre-filled from validation answers: commit gates (tests, lint,
secrets check), merge gates, deploy gates (or N/A), environment map. Add POC exception
block if project type is POC.

**runtime/latest.json** — starter JSON conforming to `validation/schema/runtime.schema.json`
with status: "unknown" and all numeric fields null.

**runtime/decisions.md** — VDR-001 recording the initial regime and project type.

---

## Step 4 — Bootstrap

With the scaffold in place, generate the two files that require full FRAMEWORK.md context:

**`projects/<slug>/CLAUDE.md`** — project-level Claude Code adapter:
- Inherits workspace rules (reference ../../CLAUDE.md and ../../FRAMEWORK.md)
- Project-specific tech stack, architecture decisions, prompt registry location
- Session bootstrap: reads memory/ + runtime/ at start; reconciles at end
- Current phase and what is in scope

**`projects/<slug>/REQUIREMENTS.md`** — phased feature plan:
- Phase 0: scaffold (mark complete)
- Phase 1: first feature set with acceptance criteria matching the gathered success criteria
- Phase 2+: future features marked for later

After writing both files, update:
- `memory/MEMORY.md` — fill in Architecture and Key Constraints sections from CLAUDE.md
- `memory/task_plan.md` — replace stub Phase 1 tasks with the actual tasks from REQUIREMENTS.md

---

## Step 5 — Register in workspace

**Root CLAUDE.md projects table** — add a row:
```
| `projects/<slug>` | <type> | <one-sentence description> |
```

**Root `memory/MEMORY.md` active projects table** — add a row:
```
| `<slug>` | <type> | Phase 1 | <brief note> |
```

**Root `memory/task_plan.md`** — add a new section for the project under Open / Next.

---

## Step 6 — Commit

```bash
git add promptZero/<slug>/ projects/<slug>/
git add CLAUDE.md memory/MEMORY.md memory/task_plan.md
git commit -m "feat(<slug>): new project scaffold — Prompt Zero + full TCode structure"
```

---

## Step 7 — Report

Output a clean summary:

```
✓  Project created: projects/<slug>/
   Classification:  <TCODE_READY / TCODE_READY_WITH_MINOR_ADDITIONS>
   promptZero.md:   promptZero/<slug>/promptZero.md
   Phase 1 tasks:   <N> tasks in memory/task_plan.md

Next steps:
  1. Review projects/<slug>/REQUIREMENTS.md — adjust phase boundaries if needed
  2. Review projects/<slug>/runtime/regime.md — confirm validation gates
  3. Open a project session: cd projects/<slug> && claude
  4. Begin implementation: "Implement Phase 1 from REQUIREMENTS.md"
```

---

## Scope

| Scope | Value |
|---|---|
| Level | workspace |
| Reads | `FRAMEWORK.md`, `CLAUDE.md`, `templates/PROMPT_ZERO.md`, `memory/MEMORY.md` |
| Writes | `promptZero/<slug>/`, `projects/<slug>/` (full tree), root `CLAUDE.md`, root `memory/` |
| Side effects | one git commit |

---

## Notes

- **Approval gate is mandatory** — never scaffold before the developer approves the plan.
- **new_project.py is the legacy fallback** — use it only if running outside a Claude session
  (e.g., terminal only, no Claude Code). Do not invoke it from within this command.
- **TCODE_FRAMEWORK_EXTENSION_REQUIRED means stop** — resolve the framework gap first.
- The generated CLAUDE.md and REQUIREMENTS.md are starting points — the developer reviews
  them before any implementation begins.
- If the developer already has detailed notes or a spec document in the conversation, use
  them directly instead of asking questions that are already answered.
