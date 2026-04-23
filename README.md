<div align="center">

# ⚙️ TCode Framework

**A portable SDLC framework for AI-assisted software development.**

*Stop re-briefing your agent every session. Give it a framework it can actually live in.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Framework](https://img.shields.io/badge/framework-agent--agnostic-blue.svg)]()
[![Agents](https://img.shields.io/badge/agents-Claude%20%7C%20Cursor%20%7C%20Copilot%20%7C%20Codex-purple.svg)]()
[![DevOps](https://img.shields.io/badge/devops-GitHub%20%7C%20GitLab%20%7C%20Gitea%20%7C%20Gogs-orange.svg)]()
[![Commits](https://img.shields.io/badge/commits-Conventional%20%2B%20AI%20trailers-green.svg)]()

</div>

---

## 🧠 The Core Idea

Most developers hand an AI agent a task and hope for the best. TCode flips this: the agent reads the framework, inherits your standards, and works within a defined structure — across every session, every project, every sprint.

```
FRAMEWORK.md      ← canonical SDLC spec, agent-agnostic
CLAUDE.md         ← adapter for Claude Code     ┐
.cursorrules      ← adapter for Cursor          ├─ swap without touching anything else
copilot-...md     ← adapter for GitHub Copilot  ┘
```

> **Switching agents = swapping one file.** The framework, memory, and DevOps system stay unchanged.

---

## ✨ What You Get

| | Feature | What it does |
|---|---|---|
| 🔁 | **Session bootstrap protocol** | Agent reads memory and task plan at every session start — zero re-briefing |
| 🧠 | **Persistent memory system** | Workspace and project-level memory files the agent maintains automatically |
| 📋 | **Architecture Decision Records** | Decisions tracked in `memory/decisions.md`, queryable by agent at any time |
| 🚀 | **Provider-agnostic DevOps** | One script pushes to Gogs, GitHub, GitLab, or Gitea simultaneously |
| 🏷️ | **Conventional Commits + AI trailers** | `Coding-Agent:` and `Model:` trailers — proper AI attribution on every commit |
| 🤖 | **Multi-agent adapter templates** | Ready-made adapter files for Claude, Cursor, Copilot, and Codex |
| 🏗️ | **Project scaffolding wizard** | `python new_project.py` — eight questions, full project scaffold in seconds |
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
├── devops/                   ← push-all, CI hooks, PR creation scripts
│   ├── config.example.yaml   ← copy → config.yaml, fill in tokens
│   ├── hooks/                ← commit-msg + pre-push git hooks
│   └── scripts/              ← push-all.sh, create-pr.py, install-hooks.sh
│
├── prompts/
│   ├── shared/               ← chain-of-thought, output format fragments
│   └── system/               ← base system prompt
│
├── memory/
│   ├── MEMORY.md             ← stable workspace facts (agent-maintained)
│   ├── task_plan.md          ← cross-project goals (agent-maintained)
│   └── sessions/             ← YYYY-MM-DD.md session logs
│
├── templates/
│   ├── APP_TEMPLATE.md       ← fill in to spin up a new project
│   ├── CLAUDE_TEMPLATE.md    ← workspace adapter template
│   ├── MEMORY_TEMPLATE.md    ← project memory template
│   └── adapters/             ← claude / cursor / copilot / codex
│
└── projects/
    └── my-app/               ← each project inherits workspace rules
        ├── REQUIREMENTS.md
        ├── STACK.md
        └── memory/
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
# → walks through 8 questions
# → creates projects/my-app/ with all required files
# → prints the bootstrap prompt to paste into your agent
```

### 4 — Bootstrap your agent

Paste the generated prompt into your coding agent. It will read `FRAMEWORK.md`, your adapter, and the project files — then generate `REQUIREMENTS.md` and the project-level adapter **before writing a single line of code**.

---

## 🤖 Agent Support

| Agent | Adapter file | Template |
|---|---|---|
| ![Claude](https://img.shields.io/badge/Claude_Code-black?logo=anthropic&logoColor=white) | `CLAUDE.md` | `templates/adapters/claude_adapter.md` |
| ![Cursor](https://img.shields.io/badge/Cursor-black?logo=cursor&logoColor=white) | `.cursorrules` | `templates/adapters/cursor_adapter.md` |
| ![Copilot](https://img.shields.io/badge/GitHub_Copilot-black?logo=github&logoColor=white) | `.github/copilot-instructions.md` | `templates/adapters/copilot_adapter.md` |
| ![Codex](https://img.shields.io/badge/OpenAI_Codex-black?logo=openai&logoColor=white) | `AGENTS.md` | `templates/adapters/codex_adapter.md` |

---

## 🔒 Non-Negotiable Rules

These apply regardless of agent or project. The agent inherits and enforces them.

- 📄 Prompts are `.txt` files loaded by path — never inline strings in code
- 🔑 No hardcoded secrets — `.env` files only, never committed
- 🚫 No dead code, no commented-out blocks in committed code
- 🎯 No gold-plating — build only what is in scope for the current phase
- ✅ Tests must pass before pushing
- 📋 Every architectural decision goes into `memory/decisions.md`
- 🗒️ Every session ends with updated memory files and a session log

---

## 🔀 DevOps: Multi-Remote Push

TCode's DevOps system is provider-agnostic. Configure once, push everywhere:

```bash
# Push to all remotes defined in config.yaml
bash devops/scripts/push-all.sh

# Create a PR (works with GitHub, GitLab, Gitea; prints URL for Gogs)
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
| [`FRAMEWORK.md`](FRAMEWORK.md) | Full SDLC spec — memory system, session protocol, quality gates, commit format |
| [`HOW_TO_USE.md`](HOW_TO_USE.md) | Step-by-step setup and project creation walkthrough |
| [`AGENTS.md`](AGENTS.md) | Quick-start reference for AGENTS.md-compatible coding agents |
| [`devops/DEVOPS.md`](devops/DEVOPS.md) | Full DevOps system documentation |

---

## 📄 License

MIT — free to use, fork, and build on. Attribution appreciated but not required.
