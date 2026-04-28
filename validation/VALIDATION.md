# TCode Validation System
# This document defines how validation signals are structured, surfaced, and
# consumed by agents across all projects in a TCode workspace.
#
# Read this alongside FRAMEWORK.md §Validation System.
# Full context: see the design discussion in memory/decisions.md (ADR-W007).

---

## The Core Principle

TCode's memory system tells the agent what it *believes* to be true.
The validation system tells the agent what is *actually* true in the running environment.

At the session boundary the agent compares the two. The gap between belief and reality
is the most valuable signal in the harness.

The framework does not prescribe test runners, CI tools, or deployment infrastructure.
It prescribes only three things:
1. The **schema** runtime signals must conform to (so any agent can read them)
2. The **taxonomy** of what kind of signal each file represents
3. The **reconciliation ritual** — what the session boundary does with those signals

---

## The Four-Layer Taxonomy

Runtime signals are not one flat thing. They have different lifetimes and different authors.

| Layer | File | Lifetime | Written by | Contains |
|---|---|---|---|---|
| **Regime** | `runtime/regime.md` | Stable | Developer | What gates apply — what must pass before commit / deploy / release |
| **State** | `runtime/latest.json` | Active | CI / CD | Most recent test run, deploy status, health check result |
| **Events** | `runtime/events/YYYY-MM-DD.jsonl` | Episodic | CI / CD | Append-only log of individual build/test/deploy events |
| **Decisions** | `runtime/decisions.md` | Append-only | Agent + Developer | Changes to the validation regime — why a gate was added, removed, or changed |

This mirrors the memory taxonomy exactly:

| Memory layer | Runtime layer |
|---|---|
| `MEMORY.md` (stable facts) | `runtime/regime.md` (stable gates) |
| `task_plan.md` (active goals) | `runtime/latest.json` (active state) |
| `sessions/YYYY-MM-DD.md` (episodic) | `runtime/events/YYYY-MM-DD.jsonl` (episodic) |
| `decisions.md` (ADRs) | `runtime/decisions.md` (validation ADRs) |

An agent already knows how to read the memory taxonomy. Runtime uses the same structure.

---

## Workspace vs Project Scope

`runtime/` lives only at the **project level**. There is no workspace-level `runtime/`
because there is no workspace-level deployment.

```
projects/<name>/
├── memory/               ← agent-authored state
└── runtime/              ← environment-authored state
    ├── regime.md         ← developer-written, stable
    ├── latest.json       ← CI/CD-written, active — conforms to schema below
    ├── events/           ← CI/CD-written, episodic
    │   └── YYYY-MM-DD.jsonl
    └── decisions.md      ← agent+developer-written, append-only
```

**Exception:** if multiple projects share infrastructure (shared database, shared gateway,
monorepo deployment), add `runtime/shared/latest.json` at the workspace level for those
cross-cutting signals only. This should be rare.

---

## The Runtime State Schema

Every `runtime/latest.json` must conform to this shape.
CI/CD tooling writes it. Agents read it. Schema source: `validation/schema/runtime.schema.json`.

```json
{
  "_schema": "<path-to-workspace>/validation/schema/runtime.schema.json",
  "generated_at": "ISO 8601 timestamp",
  "project": "project-folder-name",
  "status": "passing | failing | degraded | unknown",

  "build": {
    "id": "string or null",
    "triggered_at": "ISO 8601 or null",
    "duration_s": "number or null",
    "passed": "boolean or null"
  },

  "tests": {
    "passed": 0,
    "failed": 0,
    "skipped": 0,
    "coverage_pct": "number or null"
  },

  "deploy": {
    "environment": "dev | staging | prod | null",
    "version": "string or null",
    "deployed_at": "ISO 8601 or null",
    "healthy": "boolean or null",
    "url": "string or null"
  },

  "gates": [
    {
      "name": "gate name",
      "passed": "boolean",
      "detail": "string"
    }
  ],

  "open_issues": [
    {
      "severity": "P0 | P1 | P2",
      "description": "string",
      "since": "ISO 8601"
    }
  ],

  "notes": "free-text string"
}
```

**Status rollup rules** (CI/CD must apply these when writing):
- `passing` — all gates passed, no P0/P1 open issues, deploy healthy
- `failing` — one or more gates failed, or tests.failed > 0
- `degraded` — deployed but health check returning non-200, or P0/P1 open issue
- `unknown` — no data yet, or last run > 7 days ago

---

## The Reconciliation Ritual

This is enforced at the session boundary in every agent adapter.

### At session start

After reading the memory layers, if `runtime/latest.json` exists:

1. Read it.
2. Read `runtime/regime.md`.
3. Compare runtime state against memory claims:
   - Does `task_plan.md` say a phase is complete while `runtime/latest.json` shows failing tests?
   - Does `MEMORY.md` claim the app is deployed while `deploy.healthy` is false?
   - Does the test count in `latest.json` suggest a regression since the last session?
4. If a contradiction exists: **surface it before doing any other work**. State explicitly
   what memory claims vs what runtime shows. Let the developer confirm how to proceed.

### At session end

Before writing the session log:

1. Note the current `runtime/latest.json` status.
2. If memory claims (task_plan updates being written) conflict with runtime state: record
   the discrepancy in the session log under a `## Validation Reconciliation` heading.
3. If the same validation failure appears in the last 2 or more sessions: append an entry
   to `runtime/decisions.md` — what changed, what might need to change in the regime,
   or what technical debt is being accumulated.

---

## What the Framework Provides vs What Projects Provide

| Concern | Framework provides | Project provides |
|---|---|---|
| Signal shape | Schema (`validation/schema/runtime.schema.json`) | Actual values written by CI/CD |
| Signal taxonomy | Four-layer model (regime/state/events/decisions) | The actual files populated per layer |
| Reconciliation | Protocol (when and how agents compare memory vs runtime) | The CI/CD tooling that writes runtime/ |
| Regime template | `templates/runtime/regime.md` | Filled-in gates specific to the project |
| Event format | `validation/schema/event.schema.json` | Events appended by each CI run |
| Validation ADR format | Same as `decisions.md` format in FRAMEWORK.md | Project-specific validation decisions |

The framework deliberately does not prescribe: test frameworks, CI platforms, deployment tools,
health check implementations, or alerting systems. Those are project concerns.

---

## Setting Up a New Project

When scaffolding a new project, create the `runtime/` directory from templates:

```bash
cp templates/runtime/regime.md    projects/<name>/runtime/regime.md
cp templates/runtime/latest.json  projects/<name>/runtime/latest.json
cp templates/runtime/decisions.md projects/<name>/runtime/decisions.md
mkdir -p projects/<name>/runtime/events
```

Then:
1. Fill in `runtime/regime.md` — what gates apply to this specific project
2. Wire CI/CD to write `runtime/latest.json` on every build/deploy
3. The agent will begin reading and reconciling these at its next session

---

## Harness Self-Validation

Beyond project-level runtime signals, TCode can validate that the harness itself is
being used correctly. Signs of harness drift (to surface in session logs):

- Session started without reading `MEMORY.md` or `task_plan.md`
- `task_plan.md` was not updated at session end
- A decision was made without checking `decisions.md` first
- A phase was marked complete without `runtime/latest.json` showing passing state

These are not automatically enforced — they rely on agent discipline. Recording them
in the session log when they occur is the mechanism for surfacing and correcting drift.
