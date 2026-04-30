# CLAUDE.md — Claude Code Adapter
# This is the Claude Code adapter for the TCode framework.
# Read FRAMEWORK.md first — it contains all SDLC standards and conventions.
# This file adds only what is Claude Code-specific plus this developer's choices.
# Project-level CLAUDE.md files extend and override these defaults.

---

## Read First

Before doing anything else, read:
1. `FRAMEWORK.md` — the canonical framework spec (SDLC standards, project structure, memory system)
2. `memory/MEMORY.md` — stable workspace facts
3. `memory/task_plan.md` — current cross-project goals

---

## Developer Identity & Goals

- **Role:** [e.g. solo developer, product-focused engineer, researcher]
- **Primary domains:** [e.g. healthcare, fintech, internal tooling]
- **Typical project stage:** [e.g. POC to production, rapid prototyping, enterprise-grade]

---

## Technology Defaults (This Developer's Choices)

Override these per project in its own CLAUDE.md if the project needs something different.

| Concern | Default | Notes |
|---|---|---|
| Backend language | Python | FastAPI preferred for APIs |
| Frontend | None (API-first) | Add only when explicitly required |
| Database | SQLite (dev) / PostgreSQL (prod) | |
| LLM integration | Anthropic Claude API | Use `anthropic` Python SDK |
| LLM provider fallback | OpenAI | Use `openai` Python SDK |
| Testing | pytest | |
| Dependency management | pip + requirements.txt | |
| Containerisation | Docker + docker-compose | Optional for POCs |

---

## Projects in This Workspace

| Folder | Type | Description |
|---|---|---|
| `projects/patient-health-analyzer` | POC | Reads patient reports from SQLite, calls Claude API, returns structured health summaries |
| `projects/budget-tracker-poc` | POC | Ingests receipts via Telegram, Claude vision OCR, SQLite storage, Matplotlib dashboard |
| `projects/tfs-main-site` | Brand site | TFS (The Final Spell) standalone cricket culture brand website — Next.js 14 + TypeScript + Tailwind, 5 pages, dark/light theme, Vercel-ready. Shopify linked as subdomain merch engine. |
| `projects/tfs-sports-intelligence-engine` | Platform | Local-first cricket intelligence engine — Cricinfo ingest, 15-metric rules-based scoring, canonical JSON artifact, FastAPI, multi-sport plugin architecture. Sprint 1 complete. |
| `projects/amd-rocm-pytorch-bridge` | Learning/Interview | PyTorch custom operator → C++ binding → HIP-style kernel + CPU fallback. Demonstrates framework/backend boundary, ROCm mental model, and compile-time feature gating. |
| `projects/tfs-shrinks` | Digital Product | First member of the Digital Products portfolio. One-click social-media video packager — drop a video, pick platforms, get a zip with correctly-formatted outputs. Next.js + ffmpeg.wasm (web) + Tauri (desktop) + Capacitor (mobile). Lemon Squeezy for billing. Canonical spec: `Project_Kickoffs/Digital_Products/TFS_SHRINKS_v2_addendum.md`. |

> Add new projects here as they are created.

## Digital Products Portfolio

Workspace-level shared standards for paid, distributed consumer products live at
`digital-products/` (FRAMEWORK.md, SECURITY.md, RELEASE_POLICY.md, PRICING_POLICY.md).
Any project in `projects/` that sells to end-users inherits these standards in
addition to the workspace-level rules in `FRAMEWORK.md`. First product in the
portfolio: `tfs-shrinks`.

---

## Prompt Zero

Before starting any new project, run Prompt Zero first — it is Step 0 of the project
lifecycle. Use the web UI (`tools/prompt-zero/`) or fill `templates/PROMPT_ZERO.md` by
hand. Save the output to `promptZero/<app-slug>/promptZero.md` and paste it into the
agent session that will plan the project.

Full protocol (classification rules, storage convention, rules): `FRAMEWORK.md § Prompt Zero`.

---

## DevOps

All git and repository operations use the provider-agnostic system in `devops/`.
Config: `devops/config.yaml` (copy from `devops/config.example.yaml`, never commit).

Commit format: Conventional Commits + `Coding-Agent:` / `Model:` trailers.
Full docs: `devops/DEVOPS.md`.

---

## Session Bootstrap Protocol (Claude Code)

At the **start of every session**, read in this order:
1. `FRAMEWORK.md`
2. `memory/MEMORY.md`
3. `memory/task_plan.md`
4. Most recent `memory/sessions/YYYY-MM-DD.md` if resuming interrupted work
5. If working inside a project, also read:
   - `projects/<name>/memory/MEMORY.md` and `task_plan.md`
   - `projects/<name>/runtime/regime.md` — what validation gates apply (if exists)
   - `projects/<name>/runtime/latest.json` — most recent CI/deploy state (if exists)
   - **Before starting any work:** note contradictions between memory claims and runtime
     state. If task_plan says "Phase N complete" but `latest.json` shows failing tests
     or a degraded deploy, surface this explicitly and ask how to proceed.

At the **end of every session**, write:
1. Append a session summary to `memory/sessions/YYYY-MM-DD.md` (create if needed)
2. Update `memory/task_plan.md` — mark completed items, add newly surfaced tasks
3. Update `memory/MEMORY.md` if any new stable facts were established
4. If project has `runtime/`:
   - Compare memory claims being written against `runtime/latest.json` status
   - If any discrepancy: add a `## Validation Reconciliation` section to the session log
     naming what memory claims vs what runtime shows
   - If the same validation failure appeared in the last 2+ sessions: append an entry
     to `projects/<name>/runtime/decisions.md` — what is recurring and what should change
5. **Commit and push to all remotes** — this is the final mandatory step:
   ```bash
   # Full workspace → Gogs (zaki/TCode) + GitHub (archgenai/TCode private)
   git add -A && git commit -m "chore: session end <YYYY-MM-DD>"
   bash devops/scripts/push-all.sh

   # Framework-only → Gogs (zaki/tcode-framework) + GitHub (archgenai/tcode-framework public)
   # Push commits that touch: FRAMEWORK.md, templates/, validation/, new_project.py,
   # devops/, prompts/, CLAUDE.md, AGENTS.md, HOW_TO_USE.md
   # See devops/scripts/push-framework.sh (or ADR-W008 if script not yet created)
   git push framework main
   ```
   Commits that stay local are not backed up. The tcode-framework public repo
   is only updated when you push to it — it does not auto-sync. See ADR-W008.

Full validation protocol: `validation/VALIDATION.md`.
