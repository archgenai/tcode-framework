#!/usr/bin/env python3
"""
TCode — New Project Wizard  [LEGACY — terminal fallback only]

DEPRECATED as the primary interface. Use the /new-project slash command in
Claude Code instead — it runs the full Prompt Zero → approval gate → scaffold
→ register flow in a single agent session.

This script is kept as a terminal-only fallback for environments without a
Claude Code session (e.g. running in a plain terminal with no agent present).
Do NOT invoke this script from within a Claude Code session or from the
/new-project slash command.

  Primary interface:  /new-project  (in Claude Code)
  Terminal fallback:  python new_project.py

Run from the TCode root:

    python new_project.py

Collects project inputs across 8 sections, creates the project folder under
projects/, writes APP_SPEC.md, STACK.md stub, and .env.example, then hands
off directly to Claude Code to generate CLAUDE.md and REQUIREMENTS.md.
"""

import os
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT         = Path(__file__).parent.resolve()
PROJECTS_DIR = ROOT / "projects"

# ── ANSI colours (disabled automatically for non-TTY output) ─────────────────

_COLOR = sys.stdout.isatty()

def _e(code: str) -> str:
    return code if _COLOR else ""

RST  = _e("\033[0m")
BOLD = _e("\033[1m")
DIM  = _e("\033[2m")
CYAN = _e("\033[36m")
GRN  = _e("\033[32m")
YLW  = _e("\033[33m")
RED  = _e("\033[31m")

def s(text: str, *codes: str) -> str:
    """Wrap text in ANSI codes, appending reset."""
    if not _COLOR:
        return text
    return "".join(codes) + text + RST


# ── UI primitives ─────────────────────────────────────────────────────────────

def banner() -> None:
    lines = [
        "╔══════════════════════════════════════════════════════════╗",
        "║              TCode — New Project Wizard                  ║",
        "║   Answer the prompts below to scaffold a new project.    ║",
        "║   All fields marked * are required.                      ║",
        "║   9 sections — last one sets up the validation regime.   ║",
        "╚══════════════════════════════════════════════════════════╝",
    ]
    print()
    for line in lines:
        print(s(line, BOLD + CYAN))
    print()


def section(number: str, title: str, subtitle: str = "") -> None:
    print()
    print(s("━" * 60, CYAN))
    print(s(f"  {number}  {title}", BOLD + CYAN))
    if subtitle:
        print(s(f"  {subtitle}", DIM))
    print(s("━" * 60, CYAN))
    print()


def hint(text: str) -> None:
    print(s(f"  ↳ {text}", DIM))


def ask(
    label: str,
    default: str | None = None,
    required: bool = True,
    tip: str | None = None,
) -> str:
    """Single-line text prompt with optional default."""
    if tip:
        hint(tip)
    marker = s(" *", RED) if required and default is None else ""
    default_tag = s(f"  [{default}]", DIM) if default is not None else ""
    while True:
        raw = input(s(f"  {label}{marker}{default_tag}: ", BOLD)).strip()
        if not raw and default is not None:
            return default
        if not raw and required:
            print(s("  ⚠  This field is required.", RED))
            continue
        return raw


def ask_choice(
    label: str,
    options: list[str],
    default: str | None = None,
    tip: str | None = None,
) -> str:
    """Numbered-choice prompt."""
    if tip:
        hint(tip)
    print(s(f"  {label}", BOLD))
    for i, opt in enumerate(options, 1):
        flag = s("  ← default", DIM) if opt == default else ""
        print(f"    {s(str(i), CYAN + BOLD)}.  {opt}{flag}")
    default_num = options.index(default) + 1 if default in options else None
    prompt_tag  = f"  Choice [{default_num}]" if default_num else f"  Choice [1-{len(options)}]"
    while True:
        raw = input(s(prompt_tag + ": ", BOLD)).strip()
        if not raw and default_num:
            return default
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        print(s(f"  ⚠  Enter a number between 1 and {len(options)}.", RED))


def ask_list(
    label: str,
    tip: str | None = None,
    min_items: int = 0,
) -> list[str]:
    """Collect a variable-length bullet list. Blank line to finish."""
    if tip:
        hint(tip)
    print(s(f"  {label}", BOLD))
    print(s("  (One item per line. Blank line when done.)", DIM))
    items, idx = [], 1
    while True:
        raw = input(s(f"    {idx}. ", CYAN)).strip()
        if not raw:
            if len(items) < min_items:
                print(s(f"  ⚠  Please add at least {min_items} item(s).", RED))
                continue
            break
        items.append(raw)
        idx += 1
    return items


def ask_features() -> list[tuple[str, str]]:
    """Collect features with MVP / Future tagging."""
    print(s("  List your core features in priority order (3–7 recommended).", BOLD))
    print(s("  Leave the description blank when you are done.", DIM))
    features, idx = [], 1
    while True:
        print()
        name = input(s(f"  Feature {idx} — description (or blank to finish): ", BOLD)).strip()
        if not name:
            if not features:
                print(s("  ⚠  Add at least one feature.", RED))
                continue
            break
        scope = ask_choice("  Scope for this feature", ["MVP", "Future"], default="MVP")
        features.append((name, scope))
        idx += 1
    return features


def ask_integrations() -> list[tuple[str, str, str]]:
    """Collect LLM, auth, and any other external service integrations."""
    integrations: list[tuple[str, str, str]] = []

    llm = ask_choice(
        "LLM / AI provider",
        ["Claude (Anthropic)", "OpenAI", "Other LLM provider", "None"],
        default="Claude (Anthropic)",
        tip="The root CLAUDE.md defaults to Claude — override here only if different.",
    )
    if llm != "None":
        purpose = ask("  Purpose of the LLM integration", default="AI-assisted analysis")
        integrations.append((llm, purpose, "Required"))

    use_auth = input(s("  Auth provider needed? [y/N]: ", BOLD)).strip().lower()
    if use_auth in ("y", "yes"):
        provider = ask("  Auth provider name", tip="e.g. Auth0, Firebase Auth, custom JWT")
        integrations.append((provider, "User authentication", "Required"))

    while True:
        more = input(s("  Add another external API or service? [y/N]: ", BOLD)).strip().lower()
        if more not in ("y", "yes"):
            break
        name    = ask("  Integration name")
        purpose = ask("  Purpose")
        req     = ask_choice("  Required or optional?", ["Required", "Optional"], default="Optional")
        integrations.append((name, purpose, req))

    return integrations


def ask_success_criteria() -> list[tuple[str, str, str]]:
    """Collect 2–3 Given / When / Then acceptance tests."""
    print(s("  Define 2–3 acceptance tests (Given / When / Then).", BOLD))
    criteria: list[tuple[str, str, str]] = []
    for i in range(1, 4):
        label = f"\n  Criterion {i}" + (s("  (optional — blank Given to skip)", DIM) if i > 2 else s("  *", RED))
        print(label)
        given = input(s("    Given: ", BOLD)).strip()
        if not given:
            if i > 2:
                break
            print(s("  ⚠  Required.", RED))
            given = input(s("    Given: ", BOLD)).strip()
        when = input(s("    When:  ", BOLD)).strip()
        then = input(s("    Then:  ", BOLD)).strip()
        criteria.append((given, when, then))
    return criteria


def confirm(msg: str, default: bool = True) -> bool:
    hint_str = "[Y/n]" if default else "[y/N]"
    raw = input(s(f"  {msg} {hint_str}: ", YLW + BOLD)).strip().lower()
    if not raw:
        return default
    return raw in ("y", "yes")


# ── Slug / folder helpers ──────────────────────────────────────────────────────

def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")


_TYPE_SUFFIX = {
    "POC — Proof of Concept":         "poc",
    "MVP — Minimal Viable Product":   "mvp",
    "Production":                     "prod",
}


# ── File generators ───────────────────────────────────────────────────────────

def gen_app_spec(d: dict) -> str:
    features_rows = "\n".join(
        f"| {i+1} | {feat} | {scope} |"
        for i, (feat, scope) in enumerate(d["features"])
    )
    integrations_rows = "\n".join(
        f"| {name} | {purpose} | {req} |"
        for name, purpose, req in d["integrations"]
    ) or "| — | — | — |"
    criteria_block = "\n".join(
        f"{i+1}. Given {g}, when {w}, then {t}."
        for i, (g, w, t) in enumerate(d["success_criteria"])
    ) or "_No criteria specified._"
    oos_block = "\n".join(f"- {item}" for item in d["out_of_scope"]) or "- (none specified)"

    return f"""\
# App Specification — {d["app_name"]}
# Generated: {date.today().isoformat()}
# Review and edit this file before running the Claude bootstrap prompt.

---

## 1. Identity

| Field | Value |
|---|---|
| **App Name** | `{d["folder_name"]}` |
| **Type** | {d["project_type"]} |
| **Short Description** | {d["description"]} |
| **Primary Language** | {d["language"]} |
| **Target Environment** | {d["environment"]} |

---

## 2. Users & Problem

**Who is the primary user?**
> {d["primary_user"]}

**What problem does this solve?**
> {d["problem"]}

**What is the single most important outcome for the user?**
> {d["outcome"]}

---

## 3. Core Features

| # | Feature | MVP / Future |
|---|---|---|
{features_rows}

---

## 4. Data

**Inputs:**
{d["data_inputs"]}

**Outputs:**
{d["data_outputs"]}

**Storage:**
{d["data_storage"]}

---

## 5. External Integrations

| Integration | Purpose | Required / Optional |
|---|---|---|
{integrations_rows}

---

## 6. Constraints & Non-Functional Requirements

| Concern | Requirement |
|---|---|
| **Privacy / compliance** | {d["constraint_privacy"]} |
| **Performance** | {d["constraint_performance"]} |
| **Offline capable?** | {d["constraint_offline"]} |
| **Auth required?** | {d["constraint_auth"]} |
| **Deployment target** | {d["constraint_deployment"]} |

---

## 7. Out of Scope

{oos_block}

---

## 8. Success Criteria

{criteria_block}
"""


def gen_stack_stub(d: dict) -> str:
    return f"""\
# STACK.md — {d["app_name"]}
# Claude maintains this file.
# After every library addition or architecture decision, run:
#   > Update STACK.md with what you just added and why

## Language & Runtime

| Concern | Choice | Version | Notes |
|---|---|---|---|
| Language | {d["language"]} | TBD | — |

## Dependencies

| Package | Purpose | Version |
|---|---|---|
| — | — | — |

## Architecture Decisions

| Date | Decision | Reason |
|---|---|---|
| {date.today().isoformat()} | Initial scaffold | Created via new_project.py wizard |
"""


def gen_agents_md(d: dict) -> str:
    return f"""\
# AGENTS.md — {d["app_name"]}
# Tool-agnostic context (AGENTS.md standard).
# Canonical SDLC spec: ../../FRAMEWORK.md
# Full project brief: CLAUDE.md (or the active agent adapter)

---

## What This Project Is

{d["description"]}

**Type:** {d["project_type"]}

## Key Locations

```
src/
├── api/          # HTTP layer: routes, request/response models
├── core/         # Business logic — no framework imports
├── db/           # Database models and repository classes
├── services/     # Orchestration — calls core + db + external APIs
└── main.py       # Entry point
prompts/          # LLM prompt .txt files, organized by feature
├── system/
│   └── system_prompt.txt
└── <feature>/
memory/           # Agent-authored state (read + written at session boundary)
├── MEMORY.md     # Stable facts about this project
├── task_plan.md  # Current phase tasks and blockers
├── decisions.md  # Architecture decision records
└── sessions/     # Per-session episodic logs (agent-written)
runtime/          # Environment-authored state (written by CI/CD, read by agent)
├── regime.md     # What validation gates apply (developer-maintained)
├── latest.json   # Most recent build/test/deploy state
├── decisions.md  # Validation regime changes (VDR log)
└── events/       # Per-run event log (YYYY-MM-DD.jsonl)
```

## Hard Rules

- Prompts are `.txt` files in `prompts/` — never inline strings in code
- No hardcoded secrets — use `.env`, never commit it
- No gold-plating — build only what is in scope for the current phase

## Session Bootstrap

Start: read `memory/MEMORY.md` + `memory/task_plan.md` + `../../memory/MEMORY.md`
      + `runtime/regime.md` + `runtime/latest.json` (if exists)
      Note any contradictions between memory claims and runtime state before starting work.
End:   update `memory/task_plan.md`, append to `memory/sessions/YYYY-MM-DD.md`
      Compare memory claims against `runtime/latest.json`; record discrepancies under
      ## Validation Reconciliation in the session log.

## Current Phase

Phase 1 — see REQUIREMENTS.md for full breakdown.
"""


def gen_memory_md(d: dict) -> str:
    return f"""\
# {d["app_name"]} — Project Memory
# Type: semantic — stable facts about this project.
# Updated by Claude at session end. Read at every session start.

---

## Project Identity

**Name:** {d["folder_name"]}
**Type:** {d["project_type"]}
**Purpose:** {d["description"]}
**Current Phase:** Phase 1

## Architecture

[To be filled in after CLAUDE.md is generated.]

## Key Constraints

[To be filled in after CLAUDE.md is generated.]

## Prompt Inventory

Prompts live in `prompts/`:

| File | Purpose |
|---|---|
| `prompts/system/system_prompt.txt` | Base system prompt |

## Memory Index

| File | Purpose |
|---|---|
| `memory/MEMORY.md` | This file — stable project facts |
| `memory/task_plan.md` | Current phase tasks and blockers |
| `memory/decisions.md` | Architecture decision records |
| `memory/sessions/` | Per-session episodic logs |
"""


def gen_task_plan(d: dict) -> str:
    return f"""\
# {d["app_name"]} — Task Plan
# Type: working memory — current goals, in-flight work, blockers.
# Updated by Claude at the end of every session.

---

## Current Phase

Phase 1 — [Phase name — fill in after REQUIREMENTS.md is generated]

## Completed

- [x] APP_SPEC.md filled in
- [x] Project folder scaffolded by new_project.py

## In Progress / Next

- [ ] Generate CLAUDE.md and REQUIREMENTS.md (run bootstrap prompt)
- [ ] Review generated files before writing any code
- [ ] Implement Phase 1 features

## Blockers

None currently.
"""


def gen_decisions_md(d: dict) -> str:
    return f"""\
# {d["app_name"]} — Architecture Decision Records
# Updated when a significant technical decision is made or reversed.
# Format: date, decision, reason, alternatives rejected.

---

## {date.today().isoformat()} — Initial scaffold

**Decision:** Project created via new_project.py wizard.
**Reason:** Standard TCode bootstrapping process.
"""


def gen_system_prompt(d: dict) -> str:
    return f"""\
You are a precise, reliable AI assistant integrated into {d["app_name"]}.

Rules that always apply:
- Never invent data. If information is missing, say so explicitly.
- Be concise. Omit filler phrases.
- Respond with valid JSON when the task requires structured output.
- If the task is ambiguous, make the most conservative interpretation and flag it.
"""


def gen_runtime_regime(d: dict) -> str:
    """Generate runtime/regime.md pre-filled from wizard answers."""
    project_type = d["project_type"]
    language     = d["language"]
    has_tests    = d.get("has_tests", True)
    test_cmd     = d.get("test_command", "pytest" if language == "Python" else "npm test")
    lint_cmd     = d.get("lint_command", "ruff check ." if language == "Python" else "npm run lint")
    has_deploy   = d.get("has_deploy", False)
    health_url   = d.get("health_url", "")
    is_poc       = "POC" in project_type

    commit_gates = []
    if has_tests:
        commit_gates.append(f"- [ ] Unit tests pass (`{test_cmd}`)")
    commit_gates.append(f"- [ ] Linter / type checker passes (`{lint_cmd}`)")
    commit_gates.append("- [ ] No hardcoded secrets (manual check or `git diff --staged`)")
    if not is_poc:
        commit_gates.append("- [ ] No dead code — remove before committing")

    merge_gates = ["- [ ] All commit gates pass on a clean run"]
    if has_tests:
        merge_gates.append(f"- [ ] Integration tests pass (`{test_cmd} tests/integration/`)")
    if not is_poc:
        merge_gates.append("- [ ] Test coverage >= 70% (raise per-project as codebase matures)")

    deploy_section = ""
    if has_deploy:
        health_line = f"- [ ] Health check returns 200 (`{health_url}`)" if health_url else \
                      "- [ ] Health check returns 200 (set URL in regime.md when known)"
        deploy_section = f"""
## Deploy Gates

- [ ] Smoke test passes on staging before prod promotion
{health_line}
- [ ] No open P0 or P1 issues at deploy time
"""
    else:
        deploy_section = """
## Deploy Gates

- [ ] N/A — this project is not deployed (update when deployment is added)
"""

    monitoring_url  = health_url or "N/A"
    poc_note        = "\n## POC Exception\n\nThis is a POC project. Integration tests and coverage gates apply\nfrom Phase 3 onward. Commit gates apply from Phase 1.\n" if is_poc else ""

    return f"""\
# Validation Regime — {d["app_name"]}
# What validation gates apply to this project.
# Written by the developer, not CI/CD. Update when the approach changes.
# When you change this file, add an entry to runtime/decisions.md explaining why.
#
# Agent reads this at session bootstrap alongside runtime/latest.json.

---

## Commit Gates

{chr(10).join(commit_gates)}

---

## Merge / PR Gates

{chr(10).join(merge_gates)}
{deploy_section}
---

## Runtime Monitoring

- Health check URL: {monitoring_url}
- Alert channel: N/A (update when alerting is wired)
- On-call: N/A

---

## Environment Map

| Environment | What it is | Deployed at |
|---|---|---|
| dev | Local development | localhost |
| staging | Pre-prod validation | TBD |
| prod | Live product | TBD |
{poc_note}"""


def gen_runtime_latest(d: dict) -> str:
    import json
    return json.dumps({
        "_schema": "../../validation/schema/runtime.schema.json",
        "_note": "Written by CI/CD on every build and deploy. Do not edit manually. Agent reads at session bootstrap.",
        "generated_at": None,
        "project": d["folder_name"],
        "status": "unknown",
        "build":   {"id": None, "triggered_at": None, "duration_s": None, "passed": None},
        "tests":   {"passed": 0, "failed": 0, "skipped": 0, "coverage_pct": None},
        "deploy":  {"environment": None, "version": None, "deployed_at": None, "healthy": None, "url": None},
        "gates":   [],
        "open_issues": [],
        "notes": "",
    }, indent=2)


def gen_runtime_decisions(d: dict) -> str:
    return f"""\
# Validation Decisions — {d["app_name"]}
# Append-only log of changes to this project's validation regime.
# Parallel to memory/decisions.md but scoped to the validation ecosystem.
#
# Write here when:
# - A gate is added or removed from regime.md (record why)
# - A validation failure recurs across 2+ sessions (record the pattern and the response)
# - The CI/CD tooling or deploy pipeline changes
#
# Format mirrors workspace decisions.md ADR format.
# Prefix decisions with VDR-NNN (Validation Decision Record).

---

## VDR-001 — Initial validation regime established ({date.today().isoformat()})

**Decision:** Regime scaffolded by new_project.py wizard.
**Project type:** {d["project_type"]}
**Gates set:** {"Commit + Merge gates" if not d.get("has_deploy") else "Commit + Merge + Deploy gates"}
**Consequences:** Update regime.md and add VDR-002 when CI/CD is wired or gates change.
"""


def gen_env_example(d: dict) -> str:
    lines = [
        "# Environment variables for this project.",
        "# Copy this file to .env and fill in real values. Never commit .env.",
        "",
    ]
    for name, _, _ in d["integrations"]:
        if "claude" in name.lower() or "anthropic" in name.lower():
            lines += ["ANTHROPIC_API_KEY=your-api-key-here", ""]
        elif "openai" in name.lower():
            lines += ["OPENAI_API_KEY=your-api-key-here", ""]
    lines += [
        "# Add project-specific variables below.",
        "# EXAMPLE_VAR=value",
    ]
    return "\n".join(lines)


# ── Project creation ──────────────────────────────────────────────────────────

def create_project(d: dict) -> Path:
    folder = PROJECTS_DIR / d["folder_name"]

    if folder.exists():
        print(s(f"\n  ⚠  Folder already exists: projects/{d['folder_name']}/", RED))
        if not confirm("Overwrite existing files?", default=False):
            print(s("  Aborted. No files were changed.", YLW))
            sys.exit(0)

    folder.mkdir(parents=True, exist_ok=True)

    # ── Core project files ────────────────────────────────────────────────────
    files = {
        "APP_SPEC.md":  gen_app_spec(d),
        "STACK.md":     gen_stack_stub(d),
        ".env.example": gen_env_example(d),
        "AGENTS.md":    gen_agents_md(d),
    }
    for name, content in files.items():
        (folder / name).write_text(content, encoding="utf-8")

    # ── Memory subsystem ──────────────────────────────────────────────────────
    memory_dir = folder / "memory"
    memory_dir.mkdir(exist_ok=True)
    (memory_dir / "sessions").mkdir(exist_ok=True)
    (memory_dir / "sessions" / ".gitkeep").touch()
    (memory_dir / "MEMORY.md").write_text(gen_memory_md(d), encoding="utf-8")
    (memory_dir / "task_plan.md").write_text(gen_task_plan(d), encoding="utf-8")
    (memory_dir / "decisions.md").write_text(gen_decisions_md(d), encoding="utf-8")

    # ── Prompt registry ───────────────────────────────────────────────────────
    prompts_dir = folder / "prompts"
    (prompts_dir / "system").mkdir(parents=True, exist_ok=True)
    (prompts_dir / "system" / "system_prompt.txt").write_text(
        gen_system_prompt(d), encoding="utf-8"
    )

    # ── Validation / runtime subsystem ────────────────────────────────────────
    runtime_dir = folder / "runtime"
    runtime_dir.mkdir(exist_ok=True)
    (runtime_dir / "events").mkdir(exist_ok=True)
    (runtime_dir / "events" / ".gitkeep").touch()
    (runtime_dir / "regime.md").write_text(gen_runtime_regime(d), encoding="utf-8")
    (runtime_dir / "latest.json").write_text(gen_runtime_latest(d), encoding="utf-8")
    (runtime_dir / "decisions.md").write_text(gen_runtime_decisions(d), encoding="utf-8")

    return folder


def print_created(folder: Path, folder_name: str) -> None:
    print()
    print(s("  ✓  Project scaffolded:", GRN + BOLD))
    for f in sorted(folder.iterdir()):
        if f.name.startswith("."):
            continue
        if f.is_dir():
            label = f.name
            if label == "runtime":
                label += s("  ← validation ecosystem (fill regime.md, wire CI to latest.json)", DIM)
            elif label == "memory":
                label += s("  ← agent-authored state", DIM)
            print(s(f"     projects/{folder_name}/{label}/", GRN))
            for child in sorted(f.iterdir()):
                if not child.name.startswith("."):
                    print(s(f"       ├── {child.name}", GRN))
        else:
            print(s(f"     projects/{folder_name}/{f.name}", GRN))


BOOTSTRAP_PROMPT = (
    "Read APP_SPEC.md, then read ../../FRAMEWORK.md (the canonical SDLC spec) and "
    "../../CLAUDE.md (the workspace adapter with tech defaults). "
    "Using all three as your context, generate two files for this project:\n\n"
    "  CLAUDE.md        — project-level adapter that inherits all workspace conventions "
    "and adds project-specific architecture, constraints, and current phase. Include a "
    "session bootstrap section (referencing both memory/ and runtime/) and a prompt "
    "registry section referencing prompts/.\n"
    "  REQUIREMENTS.md  — phased feature plan derived from APP_SPEC.md, with clear "
    "acceptance criteria for each phase.\n\n"
    "Then:\n"
    "  1. Update memory/MEMORY.md with the architecture and key constraints you just defined.\n"
    "  2. Update memory/task_plan.md with the Phase 1 tasks from REQUIREMENTS.md.\n"
    "  3. Review runtime/regime.md — confirm the pre-filled gates are correct for this "
    "project, adjust if needed, and note any changes in runtime/decisions.md.\n\n"
    "Do not write any application code yet. Briefly summarise what you produced "
    "and wait for my next instruction."
)


def _claude_available() -> bool:
    return shutil.which("claude") is not None


def launch_or_print(folder: Path, folder_name: str) -> None:
    """Ask whether to hand off to Claude now. If yes, exec into it; if no, print manual steps."""
    print()
    print(s("━" * 60, CYAN))
    print(s("  Bootstrap with Claude", BOLD + GRN))
    print(s("━" * 60, CYAN))

    if not _claude_available():
        print(s("  ⚠  claude CLI not found in PATH — showing manual steps instead.", YLW))
        _print_manual_steps(folder_name)
        return

    print()
    print(s("  Claude Code will now open inside:", BOLD))
    print(s(f"    projects/{folder_name}/", CYAN))
    print()
    print(s("  It will read your APP_SPEC.md and the root CLAUDE.md, then", DIM))
    print(s("  generate CLAUDE.md and REQUIREMENTS.md for this project.", DIM))
    print()

    if not confirm("Launch Claude now to generate the project files?", default=True):
        _print_manual_steps(folder_name)
        return

    print()
    print(s("  Handing off to Claude Code…", GRN + BOLD))
    print(s("  (Type /exit or Ctrl+C to quit the Claude session when done.)", DIM))
    print()

    # Change into the project directory and exec claude, replacing this process.
    # Claude inherits the full terminal so the interactive session works normally.
    os.chdir(str(folder))
    os.execvp("claude", ["claude", BOOTSTRAP_PROMPT])


def _print_manual_steps(folder_name: str) -> None:
    print()
    print(s("  Manual steps:", BOLD))
    print()
    print(s("  1.  Open Claude Code in the project folder:", BOLD))
    print(s(f"        cd projects/{folder_name} && claude", CYAN))
    print()
    print(s("  2.  Paste this bootstrap prompt:", BOLD))
    print(s("      " + "─" * 52, DIM))
    for line in BOOTSTRAP_PROMPT.splitlines():
        print(s(f"      {line}", CYAN))
    print(s("      " + "─" * 52, DIM))
    print()
    print(s("  3.  Once files look good:", BOLD))
    print(s("        > Implement phase 1 from REQUIREMENTS.md", CYAN))
    print()
    print(s("  4.  Register the project in the root CLAUDE.md", BOLD))
    print(s(f"      Add a row for '{folder_name}' to the Projects table.", DIM))
    print()
    print(s("━" * 60, CYAN))
    print()


# ── Input collection ──────────────────────────────────────────────────────────

def collect() -> dict:
    d: dict = {}

    banner()

    # ── 1 / 8  Identity ───────────────────────────────────────────────────────
    section("1 / 8", "Project Identity", "What are you building?")

    d["app_name"] = ask(
        "App name",
        tip="e.g.  Budget Tracker  |  Patient Health Analyzer  |  Invoice Parser",
    )
    d["project_type"] = ask_choice(
        "Project type",
        list(_TYPE_SUFFIX.keys()),
        default="POC — Proof of Concept",
        tip="POC skips production concerns. Production enforces all root-level quality standards.",
    )
    base_slug      = slugify(d["app_name"])
    suffix         = _TYPE_SUFFIX[d["project_type"]]
    d["folder_name"] = ask(
        "Folder name under projects/",
        default=f"{base_slug}-{suffix}",
        tip="Press Enter to accept the suggested name.",
    )
    d["description"] = ask(
        "One-sentence description",
        tip="What does this app do for the end user?",
    )
    d["language"] = ask_choice(
        "Primary language",
        ["Python", "TypeScript", "JavaScript", "Go", "Other"],
        default="Python",
    )
    d["environment"] = ask_choice(
        "Target environment",
        ["REST API", "CLI tool", "Web app (full-stack)", "Desktop app", "Mobile app", "Other"],
        default="REST API",
    )

    # ── 2 / 8  Users & Problem ────────────────────────────────────────────────
    section("2 / 8", "Users & Problem", "Who is this for and what pain does it solve?")

    d["primary_user"] = ask(
        "Who is the primary user?",
        tip='e.g.  "a hospital clinician reviewing patient histories"',
    )
    d["problem"] = ask(
        "What problem does this solve?",
        tip='e.g.  "manual report correlation is slow and error-prone"',
    )
    d["outcome"] = ask(
        "Single most important outcome for the user?",
        tip='e.g.  "receive a concise health summary in under 10 seconds"',
    )

    # ── 3 / 8  Core Features ──────────────────────────────────────────────────
    section("3 / 8", "Core Features", "List key features in priority order.")
    d["features"] = ask_features()

    # ── 4 / 8  Data ───────────────────────────────────────────────────────────
    section("4 / 8", "Data", "What flows in, out, and where is it stored?")

    d["data_inputs"] = ask(
        "What data comes in?",
        tip="Source, format, volume.  e.g.  'PDF lab reports via form, ~10 per patient'",
    )
    d["data_outputs"] = ask(
        "What does the app produce?",
        tip="e.g.  'JSON health summary via REST API, consumed by a web dashboard'",
    )
    d["data_storage"] = ask_choice(
        "Storage type",
        ["None (stateless)", "SQLite", "PostgreSQL", "File system", "MongoDB / NoSQL", "Other"],
        default="SQLite",
    )

    # ── 5 / 8  External Integrations ─────────────────────────────────────────
    section("5 / 8", "External Integrations", "APIs and services this app will call.")
    d["integrations"] = ask_integrations()

    # ── 6 / 8  Constraints ────────────────────────────────────────────────────
    section("6 / 8", "Constraints", "Non-functional requirements and hard limits.")

    d["constraint_privacy"] = ask(
        "Privacy / compliance requirement",
        default="No sensitive data leaves the local machine",
        required=False,
        tip="Leave blank to accept the default.",
    )
    d["constraint_performance"] = ask(
        "Performance target",
        default="No strict requirement for v1",
        required=False,
        tip='e.g.  "summary returned in < 15 s"',
    )
    d["constraint_offline"] = ask_choice(
        "Offline capable?",
        ["Yes", "No", "Partial"],
        default="No",
    )
    d["constraint_auth"] = ask_choice(
        "Authentication required?",
        ["Yes", "No"],
        default="No",
    )
    d["constraint_deployment"] = ask_choice(
        "Deployment target",
        ["Local / developer machine", "Docker", "Cloud (managed)", "Bare metal server", "Not decided yet"],
        default="Local / developer machine",
    )

    # ── 7 / 8  Out of Scope ───────────────────────────────────────────────────
    section("7 / 8", "Out of Scope", "What are you explicitly NOT building in this version?")
    d["out_of_scope"] = ask_list(
        "List items explicitly excluded from v1",
        tip="Prevents Claude from over-engineering. Leave blank and press Enter to skip.",
    )

    # ── 8 / 9  Success Criteria ───────────────────────────────────────────────
    section("8 / 9", "Success Criteria", "How will you know the app works?")
    d["success_criteria"] = ask_success_criteria()

    # ── 9 / 9  Validation Regime ──────────────────────────────────────────────
    section(
        "9 / 9", "Validation Regime",
        "Sets up runtime/ — the environment-authored side of the harness.",
    )
    hint("Answers pre-fill runtime/regime.md. CI/CD writes runtime/latest.json at each run.")
    hint("You can edit regime.md after scaffolding — this just gives sensible defaults.")
    print()

    d["has_tests"] = confirm("Does this project have automated tests?", default=True)
    if d["has_tests"]:
        default_test_cmd = "pytest" if d["language"] == "Python" else "npm test"
        d["test_command"] = ask(
            "Test command",
            default=default_test_cmd,
            required=False,
            tip="Command that runs the test suite.",
        )
    else:
        d["test_command"] = ""

    default_lint = "ruff check ." if d["language"] == "Python" else "npm run lint"
    d["lint_command"] = ask(
        "Lint / type-check command",
        default=default_lint,
        required=False,
        tip="Leave blank to accept the default.",
    )

    # Infer deployment from earlier answer
    non_local = d["constraint_deployment"] not in (
        "Local / developer machine", "Not decided yet"
    )
    d["has_deploy"] = confirm(
        "Will this project be deployed to a server, container, or cloud?",
        default=non_local,
    )
    if d["has_deploy"]:
        d["health_url"] = ask(
            "Health check URL",
            default="",
            required=False,
            tip="e.g. https://api.example.com/health — leave blank if not yet known.",
        )
    else:
        d["health_url"] = ""

    return d


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    try:
        data = collect()

        # ── Review summary ────────────────────────────────────────────────────
        section("Review", "Summary of your inputs")
        rows = [
            ("App name",      data["app_name"]),
            ("Folder",        f"projects/{data['folder_name']}/"),
            ("Type",          data["project_type"]),
            ("Language",      data["language"]),
            ("Environment",   data["environment"]),
            ("Features",      f"{len(data['features'])} total  "
                              f"({sum(1 for _, sc in data['features'] if sc == 'MVP')} MVP)"),
            ("Integrations",  str(len(data["integrations"]))),
            ("Storage",       data["data_storage"]),
            ("Auth",          data["constraint_auth"]),
            ("Deployment",    data["constraint_deployment"]),
        ]
        col = max(len(k) for k, _ in rows) + 2
        for key, val in rows:
            print(f"  {s(key.ljust(col), BOLD)}  {val}")

        print()
        if not confirm("Create project with these settings?", default=True):
            print(s("\n  Aborted. No files were created.\n", YLW))
            sys.exit(0)

        folder = create_project(data)
        print_created(folder, data["folder_name"])
        launch_or_print(folder, data["folder_name"])

    except KeyboardInterrupt:
        print(s("\n\n  Interrupted. No files were created.\n", YLW))
        sys.exit(0)


if __name__ == "__main__":
    main()
