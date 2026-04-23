# App Specification Template
# Fill in every field below, then ask Claude to generate CLAUDE.md + REQUIREMENTS.md from this file.

---

## 1. Identity

| Field | Value |
|---|---|
| **App Name** | `<your-app-name>` |
| **Short Description** | One sentence: what does this app do for the end user? |
| **Primary Language** | e.g. Python / TypeScript / Go |
| **Target Environment** | e.g. local CLI / web app / REST API / desktop / kaggle-notebook |

---

## 2. Users & Problem

**Who is the primary user?**
> (e.g. "a hospital clinician reviewing patient histories")

**What problem does this solve?**
> (e.g. "manually correlating dozens of lab reports is time-consuming and error-prone")

**What is the single most important outcome for the user?**
> (e.g. "get a concise, actionable health summary in under 10 seconds")

---

## 3. Core Features

List 3–7 features in priority order. Mark each as MVP or Future.

| # | Feature | MVP / Future |
|---|---|---|
| 1 | | MVP |
| 2 | | MVP |
| 3 | | Future |

---

## 4. Data

**Inputs:**
- What data comes in? (files, database, API, user form, …)
- Format? (PDF, CSV, JSON, FHIR, …)
- Volume? (one record at a time / batch / stream)

**Outputs:**
- What does the app produce? (report, dashboard, API response, …)
- Who consumes it?

**Storage:**
- Does data need to persist? If yes, what kind of store? (SQL, NoSQL, file system, …)

---

## 5. External Integrations

| Integration | Purpose | Required / Optional |
|---|---|---|
| LLM API (e.g. Claude) | | |
| Auth provider | | |
| Other APIs | | |

---

## 6. Constraints & Non-Functional Requirements

| Concern | Requirement |
|---|---|
| **Privacy / compliance** | e.g. "no patient data leaves the local machine" |
| **Performance** | e.g. "summary generated in < 15 s" |
| **Offline capable?** | Yes / No |
| **Auth required?** | Yes / No |
| **Deployment target** | e.g. Docker, bare metal, cloud |

---

## 7. Out of Scope (for now)

List things that are explicitly NOT being built in this version so Claude doesn't gold-plate the solution.

-
-

---

## 8. Success Criteria

How will you know the app works? Define 2–3 concrete acceptance tests.

1. Given _____, when _____, then _____.
2. Given _____, when _____, then _____.
