# TCode — How to Use

## The Two-Level Hierarchy

```
TCode/
├── FRAMEWORK.md         ← Canonical SDLC spec. Read this first.
├── <agent-adapter>      ← e.g. CLAUDE.md for Claude Code
│
├── prompts/             ← Shared prompt fragments (all projects)
│   ├── shared/
│   └── system/
│
├── memory/              ← Workspace-level persistent context
│   ├── MEMORY.md
│   ├── USER.md
│   ├── task_plan.md
│   └── sessions/
│
├── templates/
│   ├── adapters/        ← Agent adapter templates
│   └── ...
│
└── projects/
    └── <app-name>/
        ├── <adapter>    ← Project-level adapter (inherits workspace)
        ├── STACK.md
        ├── REQUIREMENTS.md
        ├── prompts/
        └── memory/
```

**How inheritance works:** Your coding agent reads the workspace-level adapter
(e.g. `CLAUDE.md`) and the project-level adapter. The project adapter inherits all
workspace rules and only records overrides and additions.

**Framework vs adapter:** `FRAMEWORK.md` is agent-agnostic. Switching coding agents
means copying a different adapter template — the framework, memory, and devops systems
stay unchanged.

---

## Setting Up for the First Time

### Step 1 — Choose your coding agent and configure the adapter

```bash
ls templates/adapters/
# claude_adapter.md    → CLAUDE.md           (Claude Code)
# cursor_adapter.md    → .cursorrules         (Cursor)
# copilot_adapter.md   → .github/copilot-instructions.md  (GitHub Copilot)
```

Copy the appropriate template to the workspace root and fill in:
- Developer identity and goals
- Technology defaults for this workspace
- Any workspace-wide do-nots

### Step 2 — Configure the DevOps system

```bash
cp devops/config.example.yaml devops/config.yaml
# Edit devops/config.yaml — add your git host tokens and remote URLs
```

### Step 3 — Create your first project (see below)

---

## Creating a New Project

### Fast path — wizard

```bash
python new_project.py
```

Walks through all 8 sections, creates the project folder under `projects/`, and
prints (or launches) the bootstrap prompt for your coding agent.

---

### Manual path

#### 1 — Name and type

| Suffix | Meaning |
|---|---|
| `-poc` | Proof of concept |
| `-mvp` | Minimal viable product |
| `-prod` | Production |

#### 2 — Fill in the spec

```bash
cp templates/APP_TEMPLATE.md projects/<app-name>/APP_SPEC.md
# Edit APP_SPEC.md — fill in all fields
```

#### 3 — Bootstrap with your coding agent

Open your coding agent inside the new project folder and send:

```
Read APP_SPEC.md and FRAMEWORK.md (one level up), plus the workspace adapter.
Generate REQUIREMENTS.md and the project-level adapter for this project.
Include a session bootstrap section and a prompt registry section.
Do not write any application code yet.
```

#### 4 — Review before building

Read the generated files. Adjust the project adapter if anything is wrong
before any code is written.

#### 5 — Build

```
Implement phase 1 from REQUIREMENTS.md
```

#### 6 — Register

Add a row to the Projects table in your workspace adapter (e.g. `CLAUDE.md`).

---

## File Reference

| File | Written by | Purpose |
|---|---|---|
| `FRAMEWORK.md` | Developer | Canonical SDLC spec — agent-agnostic |
| `CLAUDE.md` / adapter | Developer | Agent-specific instructions + tech choices |
| `AGENTS.md` | Developer | Entry point for AGENTS.md-compatible agents |
| `prompts/` (root) | Developer / Agent | Shared prompt fragments |
| `memory/MEMORY.md` (root) | Agent | Stable workspace facts |
| `memory/task_plan.md` (root) | Agent | Cross-project goals |
| `memory/sessions/` (root) | Agent | Session logs |
| `<adapter>` (project) | Agent | Project brief — inherits workspace adapter |
| `STACK.md` | Agent | Live tech ledger |
| `REQUIREMENTS.md` | Agent | Phased feature list with acceptance criteria |
| `APP_SPEC.md` | Developer | Input form — fill to spin up a project |
| `.env.example` | Agent | Env var reference (never commit `.env`) |
| `prompts/` (project) | Developer / Agent | Project-specific prompts |
| `memory/` (project) | Agent | Project-level persistent context |
| `memory/decisions.md` | Agent | Architecture decision records |

---

## Keeping Things Up to Date

**After adding a library:**
```
> Update STACK.md with what you just added and why
```

**After a requirement changes:**
```
> Update REQUIREMENTS.md phase 2 to reflect: <new constraint>
```

**After an architectural decision:**
```
> Record this decision in memory/decisions.md
```

---

## Prompt Discipline

The adapter files carry context so you don't repeat yourself in chat.

**Good:**
```
> Implement the report ingestion endpoint from phase 1
```

**Avoid:**
```
> Build me a patient health app that reads reports and uses AI to summarise them...
```

That belongs in `APP_SPEC.md` and the project adapter, not in the chat.
