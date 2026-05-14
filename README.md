# ⚙️ TCode Framework

**A portable SDLC framework for AI-assisted software development.**

*Stop re-briefing your agent every session. Give it a framework it can actually live in.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/framework-agent--agnostic-blue.svg)]()
[![Agents](https://img.shields.io/badge/agents-Claude%20%7C%20Cursor%20%7C%20Copilot%20%7C%20Codex-purple.svg)]()
[![Execution](https://img.shields.io/badge/execution-hooks%20%7C%20commands%20%7C%20plugins-teal.svg)]()
[![DevOps](https://img.shields.io/badge/devops-GitHub%20%7C%20GitLab%20%7C%20Gitea%20%7C%20Gogs-orange.svg)]()
[![Commits](https://img.shields.io/badge/commits-Conventional%20%2B%20AI%20trailers-green.svg)]()

---

## 🧠 The Core Idea

Most developers hand an AI agent a task and hope for the best. TCode flips this: the agent reads the framework, inherits your standards, and works within a defined structure — across every session, every project, every sprint.

TCode defines **three layers** at every level of the workspace:

```
FRAMEWORK.md          ← Spec layer        — agent-agnostic canonical rules
CLAUDE.md             ← Declarative layer  — agent-specific context and instructions
.claude/              ← Execution layer    — hooks, commands, plugin system (Claude Code rail)
```

> **Switching agents = swapping the declarative layer.** The spec, memory, DevOps, and validation layers stay unchanged. Each agent gets its own execution rail when its harness supports one.

---

## ✨ What You Get

| | Feature | What it does |
|---|---|---|
| 🔁 | **Session bootstrap protocol** | Agent reads memory, task plan, and runtime signals at every session start — zero re-briefing |
| 🧠 | **Persistent memory system** | Workspace and project-level memory files the agent maintains automatically |
| 📋 | **Architecture Decision Records** | Decisions tracked in `memory/decisions.md`, consulted by agent before re-solving known problems |
| ✅ | **Validation ecosystem** | `runtime/` per project — schema-conforming CI signals the agent reconciles against memory at every session boundary |
| 🔌 | **Execution layer** | Hooks, slash commands, and a plugin system that automate what rules can only ask for — tests run, reviews fire, sessions close properly |
| 🤝 | **Multi-agent protocol** | Formal orchestrator/sub-agent role split with defined write-scope rules — workspace memory stays consistent across parallel agents |
| 🚀 | **Provider-agnostic DevOps** | One script pushes to Gogs, GitHub, GitLab, or Gitea simultaneously |
| 🏷️ | **Conventional Commits + AI trailers** | `Coding-Agent:` and `Model:` trailers — proper AI attribution on every commit |
| 🤖 | **Multi-agent adapter templates** | Ready-made adapter files for Claude, Cursor, Copilot, and Codex |
| 🏗️ | **Project scaffolding wizard** | `python new_project.py` — nine questions, full project scaffold including validation regime |
| 📝 | **Prompt discipline** | Prompts live in `.txt` files loaded by path — never inline strings in code |
| 🔒 | **Pre-commit guardrails** | Hooks enforce commit format, block secrets, and gate pushes on test passage |

---

## 🗂️ Workspace Layout

```
your-workspace/
├── FRAMEWORK.md              ← canonical spec — read this first
├── CLAUDE.md                 ← your agent adapter (fill in once)
├── AGENTS.md                 ← entry point for AGENTS.md-compatible agents
│
├── .claude/                  ← Claude Code execution layer
│   ├── settings.json         ← hooks, permissions, MCP config
│   └── commands/             ← slash command plugin system (one .md per command)
│       ├── review.md         ← /review      — framework compliance + test suite report
│       ├── session-end.md    ← /session-end — TCode session-end protocol
│       └── prompt-zero.md    ← /prompt-zero — new project planning workflow
│
├── validation/               ← framework-level validation conventions
│   ├── VALIDATION.md
│   └── schema/
│       ├── runtime.schema.json
│       └── event.schema.json
│
├── devops/                   ← push-all, CI hooks, PR creation scripts
│   ├── config.example.yaml
│   ├── hooks/
│   └── scripts/
│
├── memory/
│   ├── MEMORY.md             ← stable workspace facts (agent-maintained)
│   ├── task_plan.md          ← cross-project goals (agent-maintained)
│   └── sessions/             ← YYYY-MM-DD.md session logs
│
├── templates/
│   ├── adapters/             ← claude / cursor / copilot / codex
│   ├── commands/             ← command/plugin authoring template
│   ├── runtime/              ← validation scaffold templates
│   └── PROMPT_ZERO.md        ← master Prompt Zero template
│
└── projects/
    └── my-app/
        ├── REQUIREMENTS.md
        ├── STACK.md
        ├── .claude/          ← project-level execution layer (overrides workspace)
        │   └── commands/
        ├── memory/
        │   ├── MEMORY.md
        │   ├── task_plan.md
        │   └── sessions/
        └── runtime/
            ├── regime.md
            ├── latest.json
            ├── decisions.md
            └── events/
```

---

## 🚀 Getting Started

### 1 — Clone and pick your agent

```bash
git clone https://github.com/archgenai/tcode-framework your-workspace
cd your-workspace
ls templates/adapters/
# claude_adapter.md    → CLAUDE.md                              (Claude Code)
# cursor_adapter.md    → .cursorrules                           (Cursor)
# copilot_adapter.md   → .github/copilot-instructions.md       (GitHub Copilot)
# codex_adapter.md     → AGENTS.md                             (OpenAI Codex)
```

Copy the adapter for your agent to the workspace root and fill in three sections: developer identity, technology defaults, and your projects table.

### 2 — Set up DevOps

```bash
cp devops/config.example.yaml devops/config.yaml
# Add your git host URLs and token env var names
bash devops/scripts/install-hooks.sh
```

### 3 — Scaffold your first project

```bash
python new_project.py
# → walks through 9 questions (last one sets up the validation regime)
# → creates projects/my-app/ with all required files including runtime/
# → prints the bootstrap prompt to paste into your agent
```

### 4 — Bootstrap your agent

Paste the generated prompt into your coding agent. It will read `FRAMEWORK.md`, your adapter, and the project files — then generate `REQUIREMENTS.md` and the project-level adapter **before writing a single line of code**.

### 5 — Wire CI/CD to the validation schema

Point your CI/CD pipeline at `projects/my-app/runtime/latest.json`. On every build and deploy, write the result conforming to `validation/schema/runtime.schema.json`. The agent reconciles it against memory at the next session start.

---

## 🔌 The Execution Layer

TCode's three-layer model separates *what is correct* from *what triggers automatically*:

| Layer | Files | Nature | Traditional equivalent |
|---|---|---|---|
| **Spec** | `FRAMEWORK.md` | Agent-agnostic canonical rules | Engineering standards, architecture docs |
| **Declarative** | `CLAUDE.md`, `.cursorrules`, etc. | Agent-specific context and instructions | Team onboarding docs, project READMEs |
| **Execution** | `.claude/` | Agent-specific harness automation | CI/CD pipelines, pre-commit hooks, branch protection |

> **Rules govern what is correct. Execution automates what is repetitive.**

The spec and declarative layers always existed. The execution layer closes the gap that traditional SDLC filled with CI/CD: enforcement that runs automatically, regardless of agent state or context length.

### The plugin system — `.claude/commands/`

Each `.md` file in `.claude/commands/` is one slash command. TCode ships three standard workspace commands:

| Command | What it does |
|---|---|
| `/review` | Framework compliance scan (inline prompts, secrets, dead code, raw LLM storage, lazy loading, function size) + linting + tests + git hygiene. Structured PASS/FAIL report. |
| `/session-end` | Full TCode session-end protocol with explicit orchestrator vs sub-agent branching — memory writes, task plan, validation reconciliation, commit and push. |
| `/prompt-zero` | Gather idea → generate planning document → classify against TCode Framework → produce phased implementation plan. |

Drop a new `.md` file into `.claude/commands/` and the agent has a new capability immediately. No code changes. The plugin system is a directory.

Use `templates/commands/command_template.md` to author new commands.

### Hooks

Workspace-level hooks in `.claude/settings.json` run on harness events:

| Hook | Trigger | Standard use |
|---|---|---|
| `Stop` | Agent finishes a turn | Run tests if `tests/` exists |
| `PostToolUse:Bash` | After any Bash call | Log tool activity to session log |
| `PreToolUse:Bash` | Before any Bash call | Gate or warn on destructive commands |

**Claude Code is the reference implementation** of the execution layer. When another agent ships a comparable harness, it gets its own rail built on the same spec and declarative foundation — no framework changes required.

---

## 🤝 Multi-Agent Protocol

TCode has a formal protocol for orchestrator sessions that spawn sub-agents (ADR-W009).

### Role split

| Role | Writes | Does not write |
|---|---|---|
| **Orchestrator** | Workspace `memory/`, all git commits and pushes | Sub-agent project files |
| **Sub-agent** | Its assigned `projects/<name>/memory/` only | Workspace `memory/`, git |

Two agents writing to the same file concurrently produce corrupt state. Centralising workspace writes in the orchestrator eliminates that failure without file locks or coordination protocols.

### Sub-agent bootstrap block

The orchestrator prepends this to every sub-agent prompt:

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

After all sub-agents return, the orchestrator reconciles their summaries into workspace memory and performs the session-end commit and push.

Full spec: [`FRAMEWORK.md §Multi-Agent Protocol`](FRAMEWORK.md)

---

## ✅ The Validation System

TCode's memory system tells the agent what it *believes* to be true. The validation system tells it what is *actually* true in the running environment. At every session boundary, the agent compares the two.

### Four layers per project

| Layer | File | Written by | Contains |
|---|---|---|---|
| **Regime** | `runtime/regime.md` | Developer | What gates apply — commit / merge / deploy |
| **State** | `runtime/latest.json` | CI / CD | Most recent build, test, and deploy state |
| **Events** | `runtime/events/YYYY-MM-DD.jsonl` | CI / CD | Per-run event log |
| **Decisions** | `runtime/decisions.md` | Agent + Developer | Changes to the validation regime |

### The reconciliation ritual

- **Session start:** read `runtime/regime.md` + `runtime/latest.json` after memory. Surface contradictions before starting work.
- **Session end:** compare memory claims against `runtime/latest.json`. Record discrepancies in the session log. If the same failure recurs 2+ sessions, append to `runtime/decisions.md`.

Full spec: [`validation/VALIDATION.md`](validation/VALIDATION.md)

---

## 🤖 Agent Support

| Agent | Adapter file | Execution rail |
|---|---|---|
| ![Claude](https://img.shields.io/badge/Claude_Code-black?logo=anthropic&logoColor=white) | `CLAUDE.md` | ✅ Reference implementation — hooks, commands, plugin system |
| ![Cursor](https://img.shields.io/badge/Cursor-black?logo=cursor&logoColor=white) | `.cursorrules` | 🔜 When harness supports hooks/commands |
| ![Copilot](https://img.shields.io/badge/GitHub_Copilot-black?logo=github&logoColor=white) | `.github/copilot-instructions.md` | 🔜 When harness supports hooks/commands |
| ![Codex](https://img.shields.io/badge/OpenAI_Codex-black?logo=openai&logoColor=white) | `AGENTS.md` | 🔜 When harness supports hooks/commands |

All adapter templates include the multi-agent bootstrap block and execution layer section.

---

## 🔒 Non-Negotiable Rules

These apply regardless of agent or project.

- 📄 Prompts are `.txt` files loaded by path — never inline strings in code
- 🔑 No hardcoded secrets — `.env` files only, never committed
- 🚫 No dead code, no commented-out blocks in committed code
- 🎯 No gold-plating — build only what is in scope for the current phase
- ✅ Tests must pass before pushing
- 📋 Every architectural decision goes into `memory/decisions.md`
- 🗒️ Every session ends with updated memory files, a session log, and a push to all remotes
- 🔍 A phase is not complete unless `runtime/latest.json` confirms it

---

## 🔀 DevOps: Multi-Remote Push

```bash
bash devops/scripts/push-all.sh
python devops/scripts/create-pr.py
```

Supported providers: `gogs` · `gitea` · `forgejo` · `github` · `gitlab` · `bitbucket`

---

## 📝 Commit Format

```
feat(scope): short description

Body explaining the why, not the what.

Coding-Agent: Claude Code
Model: claude-sonnet-4-6
```

Conventional Commits + `Coding-Agent:` / `Model:` trailers — proper AI attribution, not the semantically wrong `Co-Authored-By`.

---

## 📚 Read Next

| File | What it covers |
|---|---|
| [`FRAMEWORK.md`](FRAMEWORK.md) | Full spec — memory, validation, session protocol, execution layer, multi-agent protocol, quality gates |
| [`validation/VALIDATION.md`](validation/VALIDATION.md) | Validation system — schema, taxonomy, reconciliation ritual |
| [`HOW_TO_USE.md`](HOW_TO_USE.md) | Step-by-step setup and project creation walkthrough |
| [`AGENTS.md`](AGENTS.md) | Quick-start for AGENTS.md-compatible coding agents |
| [`devops/DEVOPS.md`](devops/DEVOPS.md) | Full DevOps system documentation |
| [`templates/commands/command_template.md`](templates/commands/command_template.md) | How to author a new plugin command |

---

## 📄 License

MIT — free to use, fork, and build on. See [`LICENSE`](LICENSE) for the full terms.
