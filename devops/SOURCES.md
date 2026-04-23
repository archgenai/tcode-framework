# TCode DevOps — Sources Bibliography
# Every decision in DEVOPS.md traces back to a source listed here.
# Format: [Topic] Title — URL — Key finding used
# Last updated: 2026-03-16

---

## Topic 1: DevOps Cycle for AI Coding Agents

- **Pulumi Blog: AI Predictions for 2026 — A DevOps Engineer's Guide**
  https://www.pulumi.com/blog/ai-predictions-2026-devops-guide/
  → "Define → Orchestrate → Validate" as the new DevOps loop; humans validate diffs not write code

- **IBM Think: Beyond Shift Left — AI Agents in DevOps**
  https://www.ibm.com/think/insights/ai-in-devops
  → Two-phase transition: automation (deterministic) → autonomy (agents deciding); role of human oversight

- **XenonStack: AI Agents and Agentic Workflow for DevOps**
  https://www.xenonstack.com/blog/ai-agents-devops
  → Seven-stage agentic DevOps lifecycle: Planning → Dev → CI → CD → Monitoring → Incident → Feedback

- **GitHub Blog: Automate Repository Tasks with GitHub Agentic Workflows**
  https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/
  → "Pull requests are never merged automatically; humans must always review and approve"

- **GitHub Changelog: Agentic Workflows Technical Preview (Feb 13 2026)**
  https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/
  → Agents have read-only access by default; write operations require "safe outputs" declarations

- **OpenHands Software Agent SDK (arXiv 2511.03690)**
  https://arxiv.org/html/2511.03690v1
  → Three-tier testing: mocked LLM tests (seconds), real LLM tests ($0.5–$3/run), benchmarks ($100–1000/run)

- **Cognition: Devin 2025 Performance Review**
  https://cognition.ai/blog/devin-annual-performance-review-2025
  → Merge rate improved 34%→67% through better test verification before PR submission

- **Cognition: Devin 101 — Automatic PR Reviews with the Devin API**
  https://cognition.ai/blog/devin-101-automatic-pr-reviews-with-the-devin-api
  → Published GitHub Actions YAML for automated PR review pipeline structure

- **InfoQ: DevOps Modernization — AI Agents, Intelligent Observability**
  https://www.infoq.com/presentations/devops-modernization-ai-agents/
  → AI agents shift DevOps from reactive to predictive operations

---

## Topic 2: Git Workflow for AI Agents

- **DEV Community: Agentic Git Workflow (Igor Grieder)**
  https://dev.to/igor_grieder/agentic-git-workflow-hig
  → Trunk-based development recommended for agent workflows; short-lived branches (<2 days)

- **Nx Blog: Git Worktrees Changed My AI Agent Workflow**
  https://nx.dev/blog/git-worktrees-ai-agents
  → Git worktrees for parallel agent execution — each agent in its own worktree, shared history
  → Cursor 2.0 runs up to 8 parallel agents using this pattern

- **trunkbaseddevelopment.com: Short-Lived Feature Branches**
  https://trunkbaseddevelopment.com/short-lived-feature-branches/
  → Branches less than 2 days prevent merge conflicts from accumulating

- **trunkbaseddevelopment.com: Feature Flags**
  https://trunkbaseddevelopment.com/feature-flags/
  → Feature flags allow merging incomplete work to trunk without activating it

- **netresearch/git-workflow-skill (Claude Code compatible)**
  https://github.com/netresearch/git-workflow-skill
  → Git workflow skill for Claude Code: PR best practices, merge strategies, conventional commit enforcement

- **GitGuardian: Automated Guardrails for Vibe Coding**
  https://blog.gitguardian.com/automated-guard-rails-for-vibe-coding/
  → Published .pre-commit-config.yaml stack: ggshield + black + flake8 + coverage gate
  → "AI generates code probabilistically; automated guardrails provide deterministic, binary assurances"

- **Helio Medeiros: Quality Gates in the Age of Agentic Coding**
  https://blog.heliomedeiros.com/posts/2025-07-18-quality-gates-agentic-coding/
  → Two-layer defense: pre-commit (fast, local) + CI (comprehensive, centralized)

- **DEV Community: Tests Are Everything in Agentic AI**
  https://dev.to/htekdev/tests-are-everything-in-agentic-ai-building-devops-guardrails-for-ai-powered-development-2onl
  → Coverage ratcheting via PreToolUse hook; blocks git push until tests pass

- **Claude Code Hooks Guide (Anthropic)**
  https://code.claude.com/docs/en/hooks-guide
  → Full hook event taxonomy (21 events); Stop hook for test verification; PostToolUse http hook for audit logs
  → PreToolUse hook can intercept and block git commands

---

## Topic 3: Git Provider APIs

- **Gogs API Reference (official, current)**
  https://gogs.io/api-reference
  → Official API docs (redirected from archived docs-api repo as of Feb 7 2026)

- **gogs/docs-api (archived Feb 7 2026)**
  https://github.com/gogs/docs-api
  → Webhook creation: POST /api/v1/repos/{owner}/{repo}/hooks; HMAC-SHA256 signature

- **gogs/gogs Issue #5871: API for creating pull request**
  https://github.com/gogs/gogs/issues/5871
  → **Critical**: Gogs has no PR creation API endpoint. Open since 2017, unresolved.
  → Workaround: use git push + web UI, or migrate to Gitea/Forgejo

- **gogs/gogs Issue #2253: APIs for pull requests**
  https://github.com/gogs/gogs/issues/2253
  → Secondary confirmation of missing PR API; user migrated to GitLab

- **xa1.at: Create Gogs Repository via Script**
  https://xa1.at/create-gogs-repo-script/
  → POST /api/v1/admin/users/{username}/repos with token auth

- **Gitea API Usage Documentation**
  https://docs.gitea.com/development/api-usage
  → Full PR creation API; Gitea is a superset of Gogs API

- **Gitea API 1.20 Reference (Swagger)**
  https://docs.gitea.com/api/1.20/
  → POST /api/v1/repos/{owner}/{repo}/pulls — creates pull request

- **GitHub REST API: Pull Requests**
  https://docs.github.com/en/rest/pulls/pulls
  → POST /repos/{owner}/{repo}/pulls

- **GitLab API: Merge Requests**
  https://docs.gitlab.com/ee/api/merge_requests.html
  → POST /projects/{id}/merge_requests

- **Bitbucket Cloud API: Pull Requests**
  https://developer.atlassian.com/cloud/bitbucket/rest/api-group-pullrequests/
  → POST /repositories/{workspace}/{repo_slug}/pullrequests

- **go-playground/webhooks (Go library)**
  https://github.com/go-playground/webhooks
  → Handles GitHub, GitLab, Bitbucket, Gogs webhook signatures

---

## Topic 4: Lightweight Self-Hosted CI

- **cgebe/gogs-drone-ci**
  https://github.com/cgebe/gogs-drone-ci
  → Complete nginx + Gogs + Drone + Docker Registry on one machine
  → Webhook URL must be changed from external HTTPS to internal Docker network address

- **WebhookRelay: Simple Self-Hosted CI/CD with Drone**
  https://webhookrelay.com/blog/using-drone-for-simple-selfhosted-ci-cd/
  → Drone CI + Gogs Docker Compose setup; ~15 MB RAM idle

- **DEV Community: Self-Hosted CI/CD with Gitea and Drone CI**
  https://dev.to/ruanbekker/self-hosted-cicd-with-gitea-and-drone-ci-200l
  → Step-by-step Drone + Gitea integration

- **Woodpecker CI: Your First Pipeline**
  https://woodpecker-ci.org/docs/usage/intro
  → .woodpecker.yaml pipeline format; ~130 MB RAM idle

- **Woodpecker CI Issue #1894: Reconsider Gogs Support**
  https://github.com/woodpecker-ci/woodpecker/issues/1894
  → **Critical**: Woodpecker dropped Gogs support — no OAuth2, zero bug reports from Gogs users
  → Alternative: use Forgejo (Gitea-compatible, full Woodpecker support)

- **xyquadrat.ch: Simple Self-Hosted CI with Woodpecker**
  https://xyquadrat.ch/blog/simple-ci-with-woodpecker/
  → Minimal Woodpecker setup on a single machine

- **nektos/act: Run GitHub Actions Locally**
  https://github.com/nektos/act
  → Runs GitHub Actions workflows locally in Docker; no CI server required

- **mrexodia/go-gitea-webhook**
  https://github.com/mrexodia/go-gitea-webhook
  → Go webhook handler for Gogs/Gitea; port 3344; validates secrets; executes shell commands

- **jenkinsci/gogs-webhook-plugin**
  https://github.com/jenkinsci/gogs-webhook-plugin
  → Jenkins native Gogs webhook plugin

---

## Topic 5: Commit Hygiene and Audit Trails

- **Conventional Commits 1.0.0 Specification**
  https://www.conventionalcommits.org/en/v1.0.0/
  → Authoritative commit format standard; types: feat/fix/docs/style/refactor/perf/test/build/ci/chore
  → Breaking changes: `!` suffix or `BREAKING CHANGE:` footer; maps to SemVer

- **berserkdisruptors/contextual-commits**
  https://github.com/berserkdisruptors/contextual-commits
  → Extends Conventional Commits with decision traces: intent/decision/rejected/constraint/learned
  → Zero infrastructure (pure git); agent-parseable via `git log --grep='rejected(scope'`

- **git-ai-project/git-ai**
  https://github.com/git-ai-project/git-ai
  → Attaches structured JSON to commits via Git Notes; tracks additions/deletions/accepted/overridden
  → Attribution preserved across rebases, squashes, cherry-picks

- **fabiorehm.com: Our Coding Agent Commits Deserve Better Than Co-Authored-By (March 2 2026)**
  https://fabiorehm.com/blog/2026/03/02/our-coding-agent-commits-deserve-better-than-co-authored-by/
  → Use `Coding-Agent:` and `Model:` trailers instead of `Co-Authored-By:` (semantically wrong for AI)
  → `Co-Authored-By` designed for human collaborators who exchanged drafts

- **Bence Ferdinandy: Don't Abuse Co-authored-by for AI Assistance**
  https://bence.ferdinandy.com/2025/12/29/dont-abuse-co-authored-by-for-marking-ai-assistance/
  → GitHub once attributed commits to random users who registered noreply@anthropic.com

- **DeployHQ: How to Use Git with Claude Code — Co-Authored-By Attribution**
  https://www.deployhq.com/blog/how-to-use-git-with-claude-code-understanding-the-co-authored-by-attribution
  → Context on current Claude Code default behavior and its drawbacks

- **pre-commit.com**
  https://pre-commit.com/
  → Framework for managing pre-commit hooks across languages

- **SWE-agent (NeurIPS 2024)**
  https://github.com/SWE-agent/SWE-agent
  → Agent-Computer Interface design; how agents interact with file systems and git

- **OpenHands GitHub Repository**
  https://github.com/OpenHands/OpenHands
  → Open-source Devin alternative; standard git CLI usage pattern for agents
