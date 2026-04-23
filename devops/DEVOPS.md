# TCode DevOps System
# Design document, agent workflow protocol, and operating guide.
# See SOURCES.md for the full bibliography of every decision below.

---

## Design Philosophy

The DevOps system is built around one central constraint: **the git repository
is the single source of truth, and every other service is optional and swappable.**

This means:
- Standard `git push / pull / branch / worktree` is the core workflow.
  It works identically on Gogs, GitHub, GitLab, Gitea, Forgejo, Bitbucket.
- Provider-specific features (PR creation, webhooks, issue tracking) are handled
  by a thin abstraction layer (`remotes.py`) that speaks each provider's API.
- You can run zero providers (pure local git), one provider, or several simultaneously.
- Switching or adding a provider is a config change, not a code change.

Source for this philosophy: git-workflow-skill (netresearch), trunkbaseddevelopment.com,
and the observation that all major AI coding agents (Devin, OpenHands, Claude Code)
use standard git CLI — never provider-specific SDKs for core operations.

---

## Architecture

```
TCode workspace
│
├── devops/
│   ├── config.yaml            ← Active multi-provider configuration (gitignored)
│   ├── config.example.yaml    ← Template — copy and fill in
│   ├── remotes.py             ← Provider-agnostic Python client
│   ├── scripts/
│   │   ├── push-all.sh        ← Push current branch to all active remotes
│   │   ├── create-pr.py       ← Open a PR/MR on the configured primary provider
│   │   └── install-hooks.sh   ← Install git hooks into any project folder
│   ├── hooks/
│   │   ├── commit-msg         ← Enforces Conventional Commits format
│   │   └── pre-push           ← Runs test suite before any push
│   └── ci/
│       ├── webhook-handler.py ← Lightweight local CI server (listens for pushes)
│       └── pipeline-template.yaml ← CI pipeline definition for new projects
│
└── .pre-commit-config.yaml    ← Pre-commit hooks (formatting, linting, secrets)
```

---

## Supported Providers

| Provider type | PR/MR API | Webhooks API | Notes |
|---|---|---|---|
| `github` | Full | Full | api.github.com or GitHub Enterprise |
| `gitlab` | Full (MRs) | Full | gitlab.com or self-hosted |
| `gitea` | Full | Full | Recommended self-hosted option |
| `forgejo` | Full | Full | Gitea-compatible fork |
| `gogs` | **None** (Issue #5871) | Full | Push works; PRs require web UI |
| `bitbucket` | Full | Full | bitbucket.org or Bitbucket Server |

**Gogs PR limitation**: Gogs has never implemented `POST /api/v1/repos/{owner}/{repo}/pulls`.
See: https://github.com/gogs/gogs/issues/5871 (open since 2017, unresolved).
`create-pr.py` handles this by printing the direct URL to open a PR in the Gogs web UI
and optionally opening the browser automatically.

**Recommendation**: If you need full API coverage locally, replace Gogs with Gitea
or Forgejo. They are drop-in compatible (same data format, superset of Gogs API).

---

## Multi-Remote Strategy

You can configure multiple remotes with different roles:

| Role | Meaning | Behavior |
|---|---|---|
| `primary` | Canonical source of truth | PRs/MRs created here; CI triggers here |
| `mirror` | Secondary copy | Pushed to on every `push-all.sh` call |
| `backup` | Offline/archival copy | Pushed to on explicit `push-all.sh --include-backup` |

Example: Gogs as `primary` (local, private), GitHub as `mirror` (cloud backup),
a second GitHub org as `backup` (disaster recovery). All three stay in sync
automatically after every completed task.

---

## Agent Workflow Protocol

This is the standard loop Claude (or any coding agent) follows for every task.
It is based on trunk-based development + git worktrees for parallel execution.

Source: DEV Community "Agentic Git Workflow" (Igor Grieder),
Nx Blog "Git Worktrees Changed My AI Agent Workflow", trunkbaseddevelopment.com.

### Step 1 — Session start

```bash
# Load context
cat memory/MEMORY.md
cat memory/task_plan.md
# Read most recent session log if resuming
ls memory/sessions/ | tail -1 | xargs cat
```

### Step 2 — Create a task branch

Branch naming convention: `<type>/<issue-or-short-description>`

```bash
# Examples:
git checkout -b feat/receipt-ocr-pipeline
git checkout -b fix/telegram-webhook-timeout
git checkout -b chore/update-dependencies
```

For parallel tasks (multiple Claude instances): use git worktrees.
Each worktree is an independent working directory sharing one git history.

```bash
git worktree add ../tcode-task-a -b feat/feature-a
git worktree add ../tcode-task-b -b fix/bug-b
# Each instance works in its own directory — no file conflicts
git worktree remove ../tcode-task-a   # clean up when done
```

Source: Cursor 2.0 uses this pattern for up to 8 parallel agents.

### Step 3 — Implement, test, commit

Run tests after every logical unit of work. Never commit failing tests.

```bash
pytest tests/ -q
git add <specific files>   # never `git add -A` — avoids accidental .env commits
git commit -m "feat(ocr): extract vendor and amount from receipt image

intent(ocr): replace manual receipt entry with automated extraction
decision(ocr): use Claude vision API — handles varied formats natively
rejected(ocr): regex parsing — too brittle for unstructured receipts
constraint(api): image bytes only, no PII in prompt

Coding-Agent: Claude Code
Model: claude-sonnet-4-6"
```

### Step 4 — Push and open PR

```bash
# Push to all configured remotes
bash devops/scripts/push-all.sh

# Create PR on primary provider
python3 devops/scripts/create-pr.py \
  --title "feat(ocr): receipt extraction pipeline" \
  --body "Implements Phase 1 OCR. All tests pass." \
  --head feat/receipt-ocr-pipeline \
  --base main
```

### Step 5 — Session end

```bash
# Update memory before closing
# Append to memory/sessions/YYYY-MM-DD.md
# Update memory/task_plan.md
# Update memory/MEMORY.md if new stable facts were established
```

---

## Commit Message Convention

TCode uses **Conventional Commits 1.0.0** with two extensions.

Source: https://www.conventionalcommits.org/en/v1.0.0/

### Standard format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`
Breaking change: append `!` → `feat!: ...` or add `BREAKING CHANGE:` footer.

### Extension 1 — Contextual Commits (for agent decision audit trail)

Source: https://github.com/berserkdisruptors/contextual-commits

Embed decision traces in the commit body using action lines:

```
intent(<scope>): what the user/agent was trying to achieve
decision(<scope>): what was chosen and why
rejected(<scope>): alternatives that were discarded and why
constraint(<scope>): hard limits that shaped the implementation
learned(<scope>): discovered facts or gotchas
```

These are queryable via git: `git log --all --grep='rejected(auth'`

### Extension 2 — Agent attribution trailer

Source: https://fabiorehm.com/blog/2026/03/02/our-coding-agent-commits-deserve-better-than-co-authored-by/

Use `Coding-Agent:` and `Model:` trailers instead of `Co-Authored-By:` (which is
semantically wrong — it was designed for human collaborators who exchanged drafts).

```
Coding-Agent: Claude Code
Model: claude-sonnet-4-6
```

---

## CI Pipeline

The local CI pipeline uses a lightweight Python webhook handler that:
1. Listens on a configured port (default: 9000)
2. Validates the provider's HMAC signature (X-Gogs-Signature, X-Hub-Signature-256, X-Gitlab-Token)
3. On `push` to `main` or a PR branch: runs `pytest`, `flake8`, and checks for secrets
4. Logs results to `devops/ci/logs/YYYY-MM-DD.log`

Start the CI server:
```bash
python3 devops/ci/webhook-handler.py --port 9000 --config devops/config.yaml
```

Register the webhook on your provider:
- Gogs: Settings → Webhooks → Add → URL: `http://localhost:9000/hook`
- GitHub: Settings → Webhooks → Payload URL: `https://your-host:9000/hook`
- GitLab: Settings → Webhooks → URL: `https://your-host:9000/hook`

For cloud providers (GitHub/GitLab), you need the webhook URL to be publicly reachable.
Options: ngrok (`ngrok http 9000`), Cloudflare Tunnel, or a VPS reverse proxy.

---

## Pre-commit Hooks

Install with: `pip install pre-commit && pre-commit install`

Hooks run automatically on every `git commit`. They check:
- `black` — Python auto-formatting
- `flake8` — PEP 8 linting
- `bandit` — Security vulnerability scanning for Python code
- `detect-secrets` — Blocks accidental credential commits

Source: GitGuardian "Automated Guardrails for Vibe Coding",
Helio Medeiros "Quality Gates in the Age of Agentic Coding"

---

## Setting Up a New Project

1. Copy `devops/config.example.yaml` to `devops/config.yaml` and fill in tokens
2. Create the repo on your provider(s) using `remotes.py`:
   ```bash
   python3 devops/remotes.py create-repo --name my-project-poc --private
   ```
3. Initialize git and push:
   ```bash
   cd projects/my-project-poc
   git init && git add . && git commit -m "chore: initial scaffold"
   bash ../../devops/scripts/push-all.sh
   ```
4. Install git hooks:
   ```bash
   bash ../../devops/scripts/install-hooks.sh
   ```
5. Register the webhook on your primary provider (see CI Pipeline section above)
