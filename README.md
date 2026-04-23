# TCode Framework

**A portable SDLC framework for AI-assisted software development.**

TCode gives your coding agent — Claude Code, Cursor, GitHub Copilot, or any other — a structured workspace with persistent memory, enforced standards, and provider-agnostic DevOps tooling. Your agent stops being a chat window and starts being a disciplined engineering team member.

---

## The Core Idea

Most developers hand an AI agent a task and hope for the best. TCode flips this: the agent reads the framework, inherits your standards, and works within a defined structure — across every session, every project, every sprint.

```
FRAMEWORK.md      ← canonical SDLC spec, agent-agnostic
CLAUDE.md         ← adapter for Claude Code     ┐
.cursorrules      ← adapter for Cursor          ├─ swap without
copilot-...md     ← adapter for GitHub Copilot  ┘  touching anything else
```

**Switching agents = swapping one file. The framework, memory, and DevOps system stay unchanged.**

---

## What You Get

| Feature | What it does |
|---|---|
| **Session bootstrap protocol** | Agent reads memory and task plan at every session start — zero re-briefing |
| **Persistent memory system** | Workspace and project-level memory files the agent maintains automatically |
| **Architecture Decision Records** | Decisions tracked in `memory/decisions.md`, queryable by agent at any time |
| **Provider-agnostic DevOps** | One script pushes to Gogs, GitHub, GitLab, or Gitea simultaneously |
| **Conventional Commits + AI trailers** | `Coding-Agent:` and `Model:` trailers on every commit — proper AI attribution |
| **Multi-agent adapter templates** | Ready-made adapter files for Claude, Cursor, Copilot, and Codex |
| **Project scaffolding wizard** | `python new_project.py` — eight questions, full project scaffold in seconds |
| **Prompt discipline** | Prompts live in `.txt` files loaded by path — never inline strings in code |
| **Pre-commit guardrails** | Hooks enforce commit format, block secrets, and gate pushes on test passage |

---

## Workspace Layout

```
your-workspace/
├── FRAMEWORK.md              ← canonical spec — read this first
├── CLAUDE.md                 ← your agent adapter (fill in once)
├── AGENTS.md                 ← entry point for AGENTS.md-compatible agents
├── devops/                   ← push-all, CI hooks, PR creation scripts
│   ├── config.example.yaml   ← copy → config.yaml, fill in tokens
│   ├── hooks/                ← commit-msg + pre-push git hooks
│   └── scripts/              ← push-all.sh, create-pr.py, install-hooks.sh
├── prompts/
│   ├── shared/               ← chain-of-thought, output format fragments
│   └── system/               ← base system prompt
├── memory/
│   ├── MEMORY.md             ← stable workspace facts (agent-maintained)
│   ├── task_plan.md          ← cross-project goals (agent-maintained)
│   └── sessions/             ← YYYY-MM-DD.md session logs
├── templates/
│   ├── APP_TEMPLATE.md       ← fill in to spin up a new project
│   ├── CLAUDE_TEMPLATE.md    ← workspace adapter template
│   ├── MEMORY_TEMPLATE.md    ← project memory template
│   └── adapters/             ← claude / cursor / copilot / codex
└── projects/
    └── my-app/               ← each project inherits workspace rules
        ├── REQUIREMENTS.md
        ├── STACK.md
        └── memory/
```

---

## Getting Started

### 1. Clone and pick your agent

```bash
git clone https://github.com/archgenai/tcode-framework your-workspace
cd your-workspace
ls templates/adapters/
# claude_adapter.md    → CLAUDE.md
# cursor_adapter.md    → .cursorrules
# copilot_adapter.md   → .github/copilot-instructions.md
# codex_adapter.md     → AGENTS.md
```

Copy the adapter for your agent to the workspace root and fill in three sections:
- Developer identity and goals
- Technology defaults
- Projects table (add rows as you create projects)

### 2. Set up DevOps

```bash
cp devops/config.example.yaml devops/config.yaml
# Edit config.yaml — add your git host URLs and token env var names
bash devops/scripts/install-hooks.sh
```

### 3. Scaffold your first project

```bash
python new_project.py
# → answers 8 questions
# → creates projects/my-app/ with all required files
# → prints the bootstrap prompt to paste into your agent
```

### 4. Bootstrap your agent

Paste the generated prompt into your coding agent. It will read `FRAMEWORK.md`, your adapter, and the project files — then generate `REQUIREMENTS.md` and the project-level adapter before writing a single line of code.

---

## Agent Support

| Agent | Adapter file | Template |
|---|---|---|
| Claude Code | `CLAUDE.md` | `templates/adapters/claude_adapter.md` |
| Cursor | `.cursorrules` | `templates/adapters/cursor_adapter.md` |
| GitHub Copilot | `.github/copilot-instructions.md` | `templates/adapters/copilot_adapter.md` |
| OpenAI Codex | `AGENTS.md` | `templates/adapters/codex_adapter.md` |

---

## Non-Negotiable Rules (enforced by the framework)

These apply regardless of agent or project. The agent is expected to know and follow them.

- Prompts are `.txt` files loaded by path — never inline strings in code
- No hardcoded secrets — `.env` files only, never committed
- No dead code, no commented-out blocks in committed code
- No gold-plating — build only what is in scope for the current phase
- Tests must pass before pushing
- Every architectural decision goes into `memory/decisions.md`
- Every session ends with updated memory files and a session log

---

## DevOps: Multi-Remote Push

TCode's DevOps system is provider-agnostic. Configure once, push everywhere:

```bash
# Push to all remotes defined in config.yaml
bash devops/scripts/push-all.sh

# Create a PR (works with GitHub, GitLab, Gitea; prints URL for Gogs)
python devops/scripts/create-pr.py
```

Supported providers: `gogs` · `gitea` · `forgejo` · `github` · `gitlab` · `bitbucket`

---

## Commit Format

```
feat(scope): short description

Body explaining the why, not the what.

Coding-Agent: Claude Code
Model: claude-sonnet-4-6
```

Conventional Commits + `Coding-Agent:` / `Model:` trailers — proper AI attribution, not the semantically wrong `Co-Authored-By`.

---

## Read Next

| File | What it covers |
|---|---|
| `FRAMEWORK.md` | Full SDLC spec — memory system, session protocol, quality gates, commit format |
| `HOW_TO_USE.md` | Step-by-step setup and project creation walkthrough |
| `AGENTS.md` | Quick-start reference for AGENTS.md-compatible coding agents |
| `devops/DEVOPS.md` | Full DevOps system documentation |

---

## License

MIT
