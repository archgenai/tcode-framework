# TCode Framework
# Version 1.0 — Agent-agnostic SDLC specification.
# This is the canonical document. Read this before any agent-specific adapter file.
# Agent adapters (CLAUDE.md, .cursorrules, copilot-instructions.md, etc.) reference
# this file and add only the agent-specific syntax on top.

---

## What TCode Is

TCode is a portable software development framework for AI-assisted projects. It enforces
SDLC discipline — quality standards, project structure, memory continuity, and version
control — regardless of which coding agent you use.

**The core idea:** separate the *framework* (universal) from the *agent adapter* (your choice).

```
FRAMEWORK.md          ← You are here. Canonical. Agent-agnostic.
CLAUDE.md             ← Claude Code adapter  (this developer's current choice)
.cursorrules          ← Cursor adapter        (if/when you switch)
.github/copilot-...   ← Copilot adapter       (if/when you switch)
```

Changing agents means swapping the adapter, not rewriting the framework.

---

## The Two-Level Hierarchy

Every project lives inside a workspace. Both levels carry the same structure.

```
TCode/                        ← Level 1: Workspace
├── FRAMEWORK.md              ← Canonical framework spec (this file)
├── <agent-adapter>           ← e.g. CLAUDE.md, .cursorrules
├── devops/                   ← Provider-agnostic VCS / CI / CD tooling
├── prompts/                  ← Shared LLM prompt fragments (all projects)
│   ├── shared/               ← Output formats, reasoning templates
│   └── system/               ← Base system prompt fragments
├── memory/                   ← Workspace-level persistent context
│   ├── MEMORY.md             ← Stable workspace facts (agent-maintained)
│   ├── USER.md               ← Developer profile and preferences
│   ├── task_plan.md          ← Cross-project goals (agent-maintained)
│   └── sessions/             ← Per-session logs: YYYY-MM-DD.md
├── templates/                ← Reusable scaffolding templates
│   ├── adapters/             ← Agent-specific adapter templates
│   ├── PROMPT_ZERO.md        ← Master Prompt Zero template
│   └── ...
├── promptZero/               ← Pre-kickoff structured planning prompts
│   └── <app-slug>/           ← One folder per project idea
│       └── promptZero.md     ← Filled template → paste into coding agent
├── tools/                    ← Workspace tooling
│   └── prompt-zero/          ← Web UI: generate Prompt Zero documents
└── projects/
    └── <app-name>/           ← Level 2: Individual project
        ├── <agent-adapter>   ← Project-level adapter (inherits workspace rules)
        ├── FRAMEWORK_REF.md  ← Optional: project-specific SDLC overrides
        ├── APP_SPEC.md       ← Input form (developer fills in)
        ├── REQUIREMENTS.md   ← Phased feature plan (agent-generated)
        ├── STACK.md          ← Live tech ledger (agent-maintained)
        ├── prompts/          ← Project-specific LLM prompts
        └── memory/           ← Project-level persistent context
            ├── MEMORY.md
            ├── task_plan.md
            ├── decisions.md
            └── sessions/
```

**Inheritance:** Workspace-level rules apply to every project. Project-level adapter files
extend or override workspace rules. Projects never need to restate what is already in the
workspace adapter.

---

## Session Bootstrap Protocol

This protocol is agent-agnostic. Each agent adapter translates it into agent-specific
instructions (e.g. Claude reads CLAUDE.md; Cursor reads .cursorrules).

### At session start

1. Read workspace `memory/MEMORY.md` — stable workspace facts
2. Read workspace `memory/task_plan.md` — cross-project goals and in-flight work
3. If resuming interrupted work: read the most recent `memory/sessions/YYYY-MM-DD.md`
4. If working inside a project: also read the project-level equivalents of 1–3
5. **Before solving any non-trivial problem, scan `memory/decisions.md` for an
   established pattern.** If one exists, follow it as the default. Deviation
   requires a new ADR explaining why.

### At session end

1. Append a summary to `memory/sessions/YYYY-MM-DD.md` (create if it doesn't exist)
2. Update `memory/task_plan.md` — mark completed items, add newly surfaced tasks
3. Update `memory/MEMORY.md` if any new stable facts were established
4. **If any non-obvious decision was made, append it to `memory/decisions.md`.**
5. Apply the same writes at the project level if you worked inside a project
6. **Commit and push to all remotes:**
   ```bash
   git add -A && git commit -m "chore: session end <YYYY-MM-DD>"
   bash devops/scripts/push-all.sh
   ```
   This is not optional. Commits that exist only on the local machine are not backed up
   and are invisible to collaborators and the public framework repo.

---

## SDLC Quality Standards

These apply to every project in this workspace. Project-level adapters may tighten
but not remove these standards.

### Code Quality
- Functions stay focused and small (< 40 lines default; refactor when exceeded)
- Clarity over cleverness — code is read far more than it is written
- No dead code, no commented-out blocks in committed files
- Every module has a single, clearly named responsibility

### Testing
- Unit tests for all business logic
- Integration tests for any external I/O (database, API, file system)
- Tests live in `tests/unit/` and `tests/integration/`
- Tests run in CI before any merge

### Security
- No hardcoded credentials — use environment variables and `.env` files
- Never commit `.env` — always provide `.env.example`
- Sanitise all external inputs at system boundaries
- No user or patient data in logs

### Error Handling
- Fail loudly in development; fail gracefully in production
- Structured error responses from all APIs
- Log errors with enough context to reproduce them

### Do-Nots (universal)
- Do not add authentication unless the spec explicitly requires it
- Do not gold-plate — build only what is in scope for the current phase
- Do not use ORM lazy loading — always eager-load related objects
- Do not store raw LLM responses — always parse and validate before saving
- Do not generate UI unless the project explicitly targets a frontend

---

## Style Conventions

### Naming
- Python: `snake_case` for functions and variables, `PascalCase` for classes
- TypeScript / JavaScript: `camelCase` for functions and variables, `PascalCase` for classes
- Descriptive names over abbreviations
- Test files: `test_<module>.py` or `<module>.test.ts`

### Project Layout
Every project follows this base structure (adapt in the project adapter as needed):

```
src/
├── api/          # HTTP layer: routes, request/response models
├── core/         # Business logic — no framework imports
├── db/           # Database models and repository classes
├── prompts/      # LLM prompt templates (plain .txt files, never hardcoded)
├── services/     # Orchestration — calls core + db + external APIs
└── main.py       # Entry point
tests/
├── unit/
└── integration/
```

### LLM Prompt Discipline
- Workspace-shared fragments live in the root `prompts/`
- Project-specific prompts live in `projects/<name>/prompts/`, organised by feature
- Never inline a prompt string in code — always load from a `.txt` file by path
- Always validate and parse LLM responses before using them
- Log each LLM call: model, token counts, latency — never log raw user data

---

## Project Lifecycle

0. **Ideate (Prompt Zero)** — Before creating any project folder, generate a Prompt Zero
   document using `tools/prompt-zero/` (web UI) or by filling `templates/PROMPT_ZERO.md`
   by hand. Save the result to `promptZero/<app-slug>/promptZero.md` and paste its contents
   into your coding agent. The agent will classify the project against the current TCode
   Framework and produce a full implementation plan before any code is written.
   See **§ Prompt Zero** below for the full protocol.
1. **Specify** — Fill in `APP_SPEC.md` from the template. Define features, constraints, out-of-scope.
2. **Scaffold** — Run `python new_project.py` or follow the manual path in `HOW_TO_USE.md`.
3. **Bootstrap** — Ask your coding agent to generate `REQUIREMENTS.md` and the project adapter from `APP_SPEC.md`.
4. **Build** — Work phase by phase. Never implement beyond the current phase.
5. **Iterate** — After each phase: update `STACK.md`, commit, update memory.

---

## Prompt Zero

Prompt Zero is Step 0 of every new project. It converts a product idea into a structured
document that instructs a coding agent to plan and classify the project against the
current TCode Framework — before any application code is written.

### What the agent does with a Prompt Zero document

1. Reads the TCode Framework files before writing any code
2. Classifies the project as one of:
   - `TCODE_READY` — framework is sufficient as-is
   - `TCODE_READY_WITH_MINOR_ADDITIONS` — small project-local additions needed
   - `TCODE_FRAMEWORK_EXTENSION_REQUIRED` — missing framework capabilities must be added first
3. Evaluates the framework against five areas: memory, approvals, telemetry, deploy
   workflows, and coding-agent governance
4. Produces a full implementation plan, the minimum TCode file set, and a first-phase
   task list
5. Returns the exact next prompt the developer should send to begin implementation

### How to generate a Prompt Zero document

**Option A — Web UI (recommended):**
1. Start the web app: `cd tools/prompt-zero && pip install -r requirements.txt && uvicorn main:app --reload --port 7999`
2. Open `http://localhost:7999`
3. Fill in the product idea fields (name, users, problem, MVP, stack, cloud target, safety)
4. Click Generate — the tool fills the template and saves to `promptZero/<app-slug>/promptZero.md`
5. Copy the output and paste it into your coding agent

**Option B — Manual:**
1. Copy `templates/PROMPT_ZERO.md` to `promptZero/<app-slug>/promptZero.md`
2. Fill in all `[INSERT ...]` placeholders
3. Paste into your coding agent

### Storage convention

```
promptZero/
└── <app-slug>/
    └── promptZero.md     ← commit this — it is the planning record for the project
```

One folder per idea. The slug is the lowercased, hyphenated project name.
Commit these files alongside other workspace docs — they are the historical record of how
each project was planned and what TCode classification was assigned.

### Rules

- Do not ask the coding agent to write application code during Prompt Zero — it is a
  planning step only.
- Do not modify `templates/PROMPT_ZERO.md` for a specific project — fill the copy in
  `promptZero/<app-slug>/`.
- If the agent classifies as `TCODE_FRAMEWORK_EXTENSION_REQUIRED`, resolve the framework
  gap before starting implementation — do not hack around it inside the project.

---

## Memory System

The memory system gives coding agents persistent context across sessions.

| File | Updated by | Contents |
|---|---|---|
| `memory/MEMORY.md` | Agent (session end) | Stable facts: architecture, constraints, active projects |
| `memory/USER.md` | Agent / Developer | Developer profile, preferences, working style |
| `memory/task_plan.md` | Agent (session end) | In-flight work, completed items, blockers |
| `memory/sessions/YYYY-MM-DD.md` | Agent (session end) | Episodic log of what was done and what is next |
| `memory/decisions.md` | Agent (when decision made) | Architecture Decision Records — see §Decision Records below |

At project level: same structure under `projects/<name>/memory/`.

**Rule:** Memory files record facts that are not derivable from reading the code or git log.
Do not duplicate what is already in `STACK.md`, `REQUIREMENTS.md`, or git history.

---

## Decision Records

### What they are

A Decision Record (ADR — Architecture Decision Record) is a short document that
captures a non-obvious choice made during development: what was decided, why, and
what it means going forward.

**The critical property: past ADRs are the historically-preferred patterns.**
When a future session encounters a problem that matches an existing ADR, the
recorded decision is the default solution. Do not re-derive the answer from scratch;
apply the established pattern. Only deviate if you have a compelling, documented reason
— which itself becomes a new ADR.

This turns `memory/decisions.md` from a passive archive into an active engineering
guide: the accumulated knowledge of every hard-won decision made in this workspace.

---

### When to write an ADR

Write one whenever:

- A choice was made between two or more plausible alternatives (you rejected something)
- A constraint or environmental quirk drove the design (e.g. no font files in WASM)
- A bug's root cause revealed a non-obvious platform behaviour worth remembering
- A performance, security, or cost trade-off was consciously accepted
- A dependency was added, replaced, or explicitly rejected

**Do not write one for:**

- Bug fixes with an obvious cause (just commit)
- Cosmetic or style choices
- Anything already captured clearly in `STACK.md` or `REQUIREMENTS.md`

---

### ADR format

Every entry follows this structure. All five fields are required.

```markdown
## ADR-NNN — Short title (YYYY-MM-DD)

**Decision:** One or two sentences. The choice that was made.

**Context:** Why this came up. What problem it solves or what constraint forced it.

**Rationale:** Why this option over the alternatives. Name the alternatives you
rejected and why.

**Consequences:** What this means going forward. What is now easier, harder,
or different. What future code must respect.
```

Entries are **append-only**. Never rewrite or delete a past ADR. If a later decision
supersedes it, write a new ADR that references and overrides the old one. This
preserves the full reasoning chain.

---

### Two levels of decisions

| Level | File | Scope |
|---|---|---|
| Workspace | `memory/decisions.md` | Patterns that apply across all projects: testing approach, security conventions, memory protocol, cross-cutting tooling |
| Project | `projects/<name>/memory/decisions.md` | Patterns specific to one product: encoding strategy, API design, UI state model, platform-specific quirks |

Both files are consulted at the appropriate scope. Workspace ADRs take precedence
over project ADRs when they conflict.

---

### The lookup rule

Before implementing any solution that is:

- architectural (affects multiple modules)
- non-trivial (took thought to figure out)
- recurring (could come up again in other projects)

— search `decisions.md` for an established pattern first. If found: apply it.
If you deviate: explain why in a new ADR. If not found: implement, then record.

This loop keeps the decisions log growing as a living engineering guide, not just
a historical log.

---

## Validation System

Full specification: `validation/VALIDATION.md`.

The harness constrains what agents *write*. The validation system tells agents whether
what they wrote *actually works* in the running environment. At the session boundary,
agents compare their memory claims against runtime signals and surface any gap.

### The four-layer taxonomy

Each project that has a deployed artefact (or a test suite) should have a `runtime/` directory:

| File | Lifetime | Written by | Contains |
|---|---|---|---|
| `runtime/regime.md` | Stable | Developer | What gates apply — commit / merge / deploy |
| `runtime/latest.json` | Active | CI / CD | Most recent build, test, and deploy state |
| `runtime/events/YYYY-MM-DD.jsonl` | Episodic | CI / CD | Per-run event log |
| `runtime/decisions.md` | Append-only | Agent + Developer | Changes to the validation regime |

This mirrors the memory taxonomy. An agent already knows how to read memory — it reads
`runtime/` the same way.

### The schema

`runtime/latest.json` must conform to `validation/schema/runtime.schema.json`.
See that file for the full field definitions. Key fields: `status` (passing / failing /
degraded / unknown), `tests`, `deploy`, `gates`, `open_issues`.

### The reconciliation ritual

Enforced at the session boundary in all agent adapters (see §Plugging In a Coding Agent):

**At session start:** After reading memory, read `runtime/regime.md` and `runtime/latest.json`
(if they exist). Before starting any work, note contradictions between memory claims and
runtime state. Surface them explicitly and wait for developer direction.

**At session end:** Before writing the session log, compare memory claims being written
against current `runtime/latest.json`. Record discrepancies under `## Validation Reconciliation`
in the session log. If the same failure recurs across 2+ sessions, append an entry to
`runtime/decisions.md`.

### Setting up a new project

```bash
cp templates/runtime/regime.md     projects/<name>/runtime/regime.md
cp templates/runtime/latest.json   projects/<name>/runtime/latest.json
cp templates/runtime/decisions.md  projects/<name>/runtime/decisions.md
mkdir -p projects/<name>/runtime/events
```

Then fill in `regime.md` and wire CI/CD to write `latest.json` on every build.

### What the framework does not prescribe

Test runners, CI platforms, deployment tools, health check implementations, alerting
systems. Those are project concerns. The framework provides only: schema, taxonomy,
and the reconciliation ritual.

---

## DevOps System

All VCS and CI operations use the provider-agnostic tooling in `devops/`.
Supported: Gogs, Gitea, Forgejo, GitHub, GitLab, Bitbucket — simultaneously.

| Operation | Command |
|---|---|
| Push to all remotes | `bash devops/scripts/push-all.sh` |
| Create PR | `python3 devops/scripts/create-pr.py --repo <name> --title "..."` |
| Install git hooks | `bash devops/scripts/install-hooks.sh projects/<name>` |
| Start local CI | `python3 devops/ci/webhook-handler.py` |

Config: `devops/config.yaml` (copy from `devops/config.example.yaml` — never commit).

Commit format: **Conventional Commits** with `Coding-Agent:` and `Model:` trailers.
Full documentation: `devops/DEVOPS.md`.

---

## Plugging In a Coding Agent

TCode works with any coding agent that can read a context file at session start.

### Step 1 — Choose an adapter template

```
templates/adapters/
├── claude_adapter.md      → CLAUDE.md    (Claude Code)
├── cursor_adapter.md      → .cursorrules  (Cursor)
├── copilot_adapter.md     → .github/copilot-instructions.md  (GitHub Copilot)
└── codex_adapter.md       → AGENTS.md    (OpenAI Codex CLI)
```

### Step 2 — Place the adapter at the workspace root

Copy the template to the correct filename for your agent and fill in the
developer-specific sections (identity, tech defaults, projects registry).

### Step 3 — Do the same for each project

Copy the same adapter template into `projects/<name>/` and adjust it to add
project-specific context. The project adapter **inherits** workspace rules;
only record overrides and additions.

### What goes in an adapter (and what doesn't)

| Belongs in adapter | Belongs in FRAMEWORK.md |
|---|---|
| Developer identity and preferences | SDLC quality standards |
| Tech stack choices (language, DB, etc.) | Project structure conventions |
| Agent-specific syntax or directives | Memory system protocol |
| Projects registry | Commit format rules |
| Session bootstrap (agent-specific phrasing) | Adapter pattern documentation |

---

## Video + Audio Generation

When producing explainer videos, demo recordings, or any video with voice-over narration,
follow the procedure below. The full reference is in the `/video-audio-overlay` skill.

### Core rules

1. **Use Remotion's bundled ffmpeg** for all audio muxing — never the 2018 `@ffmpeg-installer`
   build (it silently corrupts AAC output). Path: `node_modules/@remotion/compositor-linux-x64-gnu/ffmpeg`

2. **One TTS segment per visual scene.** Do not generate one audio blob for the whole video.
   Segment narration matches scene transitions and keeps audio in sync with visuals.

3. **Save the narration script** as `narration_script.txt` alongside the video before generating
   TTS. Include scene labels, word counts, and target durations.

4. **Do not name internal projects** in narration intended for public or external audiences.
   Say "multiple projects across multiple languages and domains" instead.

5. **Verify with silencedetect** after every mux — ffprobe alone is insufficient. A silent AAC
   track passes all codec/duration/bitrate checks. Silencedetect is the real gate:
   ```bash
   ffmpeg -i out.mp4 -af "silencedetect=noise=-30dB:d=0.5" -vn -f null /dev/null 2>&1 | grep silence_start
   ```
   Pass: first `silence_start` > 1.0 s (natural sentence pause). If `silence_start: 0` with
   `silence_end ≈ video_duration`, the track is silent — fix the TTS source and re-mux.

### Narration script word budget

`alloy` (tts-1-hd) speaks at ~158 wpm. Use this to target scene-length segments:

| Scene duration | Target words |
|---|---|
| 10 s | ~26 words |
| 20 s | ~53 words |
| 30 s | ~79 words |
| 60 s | ~158 words |

### Quick reference

```python
# 1. Write narration_script.txt with one segment per scene
# 2. Generate TTS per scene
from openai import OpenAI
client = OpenAI()
for i, text in enumerate(scene_texts, 1):
    data = client.audio.speech.create(model="tts-1-hd", voice="alloy", input=text, response_format="mp3")
    Path(f"scene_{i:02d}.mp3").write_bytes(data.read())

# 3. Concatenate
# ffmpeg -f concat -safe 0 -i concat_list.txt -c:a libmp3lame narration.mp3

# 4. Mux
# ffmpeg -i video.mp4 -i narration.mp3 -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 128k -shortest out.mp4

# 5. Verify (mandatory)
# ffmpeg -i out.mp4 -af "silencedetect=noise=-30dB:d=0.5" -vn -f null /dev/null 2>&1 | grep silence_start
```

---

## Framework File Reference

| File | Maintained by | Purpose |
|---|---|---|
| `FRAMEWORK.md` | Developer | Canonical SDLC spec — this file |
| `CLAUDE.md` (or other adapter) | Developer | Agent-specific instructions and tech choices |
| `AGENTS.md` | Developer | Entry point for agents that read AGENTS.md standard |
| `HOW_TO_USE.md` | Developer | Human-readable guide to using TCode |
| `new_project.py` | Developer | Wizard to scaffold new projects |
| `devops/` | Developer | VCS / CI tooling |
| `prompts/` | Developer / Agent | Shared LLM prompt fragments |
| `memory/` | Agent | Persistent workspace context |
| `templates/` | Developer | Scaffolding templates for new projects and adapters |
