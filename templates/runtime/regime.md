# Validation Regime — <project-name>
# What validation gates apply to this project.
# Written by the developer (not CI/CD). Updated when the approach changes.
# When you change this file, add an entry to runtime/decisions.md explaining why.
#
# Read by the agent at session bootstrap alongside runtime/latest.json.
# The agent uses this to understand what "passing" means for this specific project.

---

## Commit Gates
# These must pass before any commit is pushed.

- [ ] Unit tests pass (`<command>`)
- [ ] Linter / type checker passes (`<command>`)
- [ ] No hardcoded secrets (`<tool or manual>`)

---

## Merge / PR Gates
# These must pass before merging to main.

- [ ] Integration tests pass (`<command>`)
- [ ] Test coverage >= <XX>% (`<command>`)
- [ ] PR reviewed by [developer / second agent pass]

---

## Deploy Gates
# These must pass before promoting to the next environment.

- [ ] Smoke test passes on staging (`<endpoint or script>`)
- [ ] Health check returns 200 within <N>s of deploy (`<url>`)
- [ ] No open P0 or P1 issues at deploy time

---

## Runtime Monitoring
# What infrastructure-level health signals exist for this project.

- Health check URL: [e.g. https://api.project.com/health — or N/A for non-deployed]
- Alert channel: [e.g. Slack #alerts, email, or N/A]
- Expected uptime SLA: [e.g. 99.9% in prod, best-effort in dev]
- On-call: [N/A for solo projects]

---

## Environment Map

| Environment | What it is | Deployed at |
|---|---|---|
| dev | Local development | localhost |
| staging | Pre-prod validation | [URL or N/A] |
| prod | Live product | [URL or N/A] |

---

## Exceptions and Special Cases
# Document project-specific constraints that override workspace defaults.

[e.g. "Integration tests require a live database — do not mock."]
[e.g. "Smoke tests are skipped for POC phases 1-2; add before Phase 3 deploy."]
