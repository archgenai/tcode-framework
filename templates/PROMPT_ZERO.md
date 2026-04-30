You are Claude Code operating inside the TCode Framework.

Repository/framework source:
https://github.com/archgenai/tcode-framework

Your job is to convert my product idea into a TCode-governed implementation plan and then prepare the project for phased implementation.

Important:
Do NOT start writing application code immediately.

You must first inspect and follow the current TCode Framework conventions, especially:
- FRAMEWORK.md
- CLAUDE.md
- AGENTS.md
- HOW_TO_USE.md
- templates/
- prompts/
- memory/
- devops/
- new_project.py
- any project scaffolding conventions
- any pre-commit, testing, deployment, or DevOps rules

## Core decision rule

Before implementing the app, answer this:

Can this project be successfully developed, tested, and deployed using the current TCode Framework as-is?

You must classify the answer as one of:

1. TCODE_READY
   The current framework is sufficient. Build the project strictly using existing TCode templates, memory conventions, session protocol, DevOps process, prompts, and project structure.

2. TCODE_READY_WITH_MINOR_ADDITIONS
   The current framework is mostly sufficient, but the app needs small project-local additions such as deployment docs, OCI scripts, Docker files, or app-specific safety prompts. Do not modify the framework itself unless absolutely necessary.

3. TCODE_FRAMEWORK_EXTENSION_REQUIRED
   The app exposes missing framework-level capabilities. In this case, do not hack around them only inside the app. Propose a TCode next-version extension and add the missing framework pieces in a clean, reusable way.

## TCode extension areas to evaluate

Evaluate whether the current framework sufficiently supports:

1. Memory
   - Workspace memory
   - Project memory
   - Decision logs
   - Session logs
   - Cross-session continuity

2. Approvals
   - Human approval gates before risky changes
   - Approval before deployment
   - Approval before modifying infrastructure
   - Approval before adding paid services
   - Approval before handling sensitive data

3. Telemetry
   - Agent action logs
   - Build/test/deploy logs
   - Runtime app telemetry
   - LLM/RAG evaluation telemetry
   - Cost/token tracking where relevant
   - Traceability from prompt → code change → test → deployment

4. Deploy workflows
   - Local development
   - Docker Compose
   - Cloud deployment
   - Environment variable management
   - Secrets handling
   - Rollback
   - Release notes
   - Promotion from dev to test/prod

5. Coding-agent governance
   - Agent responsibilities
   - Allowed/disallowed actions
   - Session bootstrap
   - Commit format
   - Test-before-push rules
   - No secrets
   - No dead code
   - No uncontrolled scope expansion

## Product idea

Application name:
[INSERT APP NAME]

One-line description:
[INSERT DESCRIPTION]

Primary users:
[INSERT USERS]

Core problem:
[INSERT PROBLEM]

MVP capabilities:
[INSERT MVP CAPABILITIES]

AI/LLM requirements:
[INSERT LLM REQUIREMENTS]

RAG requirements:
[INSERT RAG REQUIREMENTS]

Cloud deployment target:
[INSERT CLOUD TARGET]

Preferred stack:
[INSERT STACK]

Safety/compliance requirements:
[INSERT SAFETY REQUIREMENTS]

## Required output

Produce the following:

1. TCode capability assessment
   - Classification: TCODE_READY, TCODE_READY_WITH_MINOR_ADDITIONS, or TCODE_FRAMEWORK_EXTENSION_REQUIRED
   - Evidence from existing TCode files
   - Gaps, if any

2. Recommended TCode execution mode
   - Use existing templates only
   - Use existing templates plus project-local additions
   - Extend framework before app implementation

3. If framework extension is required, propose:
   - New files to add under tcode-framework
   - Existing files to modify
   - New templates
   - New memory conventions
   - New approval gates
   - New telemetry conventions
   - New deployment workflow templates
   - Version name suggestion, for example TCode vNext or TCode Teams

4. App implementation plan
   - Product definition
   - MVP scope
   - Out-of-scope list
   - Architecture
   - Repo/project structure under TCode
   - RAG pipeline
   - LLM provider abstraction
   - Safety controls
   - API endpoints
   - Data model
   - Testing plan
   - Local run plan
   - Cloud deployment plan

5. TCode files to create for this project
   Include at minimum:
   - projects/[app-name]/REQUIREMENTS.md
   - projects/[app-name]/STACK.md
   - projects/[app-name]/memory/MEMORY.md
   - projects/[app-name]/memory/decisions.md
   - projects/[app-name]/memory/task_plan.md
   - projects/[app-name]/memory/sessions/[date].md
   - projects/[app-name]/CLAUDE.md or AGENTS.md
   - projects/[app-name]/docs/architecture.md
   - projects/[app-name]/docs/deployment.md
   - projects/[app-name]/docs/security.md

6. First implementation phase
   - Files to create
   - Tests to add
   - Commands to run
   - Definition of done

7. Exact next prompt I should give you after this planning step

Rules:
- Do not write full application code yet.
- Do not ignore TCode conventions.
- Do not invent framework capabilities that do not exist.
- If TCode lacks something, propose it explicitly as a framework extension.
- Keep MVP small.
- Build for successful deployment, not just local demo.
