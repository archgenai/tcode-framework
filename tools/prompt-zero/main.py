"""
Prompt Zero web UI — TCode Framework tool.

Generates a filled promptZero.md from a product idea form and saves it to
promptZero/<app-slug>/promptZero.md relative to the TCode workspace root.

Usage:
    cd tools/prompt-zero
    pip install -r requirements.txt
    uvicorn main:app --reload
    # open http://localhost:7999
"""

import re
from pathlib import Path

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="TCode Prompt Zero")

WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
PROMPT_ZERO_DIR = WORKSPACE_ROOT / "promptZero"


def slugify(name: str) -> str:
    name = name.lower().strip()
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"[\s_]+", "-", name)
    name = re.sub(r"-+", "-", name).strip("-")
    return name


def generate_document(
    app_name: str,
    description: str,
    users: str,
    problem: str,
    mvp_capabilities: str,
    llm_requirements: str,
    rag_requirements: str,
    cloud_target: str,
    stack: str,
    safety_requirements: str,
) -> str:
    slug = slugify(app_name)
    return f"""You are Claude Code operating inside the TCode Framework.

Repository/framework source:
https://github.com/archgenai/tcode-framework

Your job is to convert my product idea, {app_name}, into a TCode-governed implementation plan and then prepare the project for phased implementation.

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

Can {app_name} be successfully developed, tested, and deployed using the current TCode Framework as-is?

You must classify the answer as one of:

1. TCODE_READY
   The current framework is sufficient. Build {app_name} strictly using existing TCode templates, memory conventions, session protocol, DevOps process, prompts, and project structure.

2. TCODE_READY_WITH_MINOR_ADDITIONS
   The current framework is mostly sufficient, but {app_name} needs small project-local additions such as deployment docs, OCI scripts, Docker files, or app-specific safety prompts. Do not modify the framework itself unless absolutely necessary.

3. TCODE_FRAMEWORK_EXTENSION_REQUIRED
   {app_name} exposes missing framework-level capabilities. In this case, do not hack around them only inside the app. Propose a TCode next-version extension and add the missing framework pieces in a clean, reusable way.

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
{app_name}

One-line description:
{description}

Primary users:
{users}

Core problem:
{problem}

MVP capabilities:
{mvp_capabilities}

AI/LLM requirements:
{llm_requirements}

RAG requirements:
{rag_requirements}

Cloud deployment target:
{cloud_target}

Preferred stack:
{stack}

Safety/compliance requirements:
{safety_requirements}

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

4. {app_name} implementation plan
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
   - projects/{slug}/REQUIREMENTS.md
   - projects/{slug}/STACK.md
   - projects/{slug}/memory/MEMORY.md
   - projects/{slug}/memory/decisions.md
   - projects/{slug}/memory/task_plan.md
   - projects/{slug}/memory/sessions/[date].md
   - projects/{slug}/CLAUDE.md or AGENTS.md
   - projects/{slug}/docs/architecture.md
   - projects/{slug}/docs/deployment.md
   - projects/{slug}/docs/security.md

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
"""


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TCode — Prompt Zero</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg: #0d1117;
    --surface: #161b22;
    --border: #30363d;
    --accent: #58a6ff;
    --accent-dim: #1f6feb33;
    --text: #e6edf3;
    --muted: #8b949e;
    --success: #3fb950;
    --radius: 6px;
    --font-mono: "JetBrains Mono", "Fira Code", "Cascadia Code", monospace;
  }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    font-size: 14px;
    line-height: 1.6;
    min-height: 100vh;
  }

  header {
    border-bottom: 1px solid var(--border);
    padding: 16px 32px;
    display: flex;
    align-items: center;
    gap: 12px;
  }

  header .logo {
    font-family: var(--font-mono);
    font-size: 13px;
    color: var(--muted);
  }

  header .logo span { color: var(--accent); font-weight: 600; }

  header h1 {
    font-size: 16px;
    font-weight: 600;
    color: var(--text);
  }

  header .step-badge {
    background: var(--accent-dim);
    color: var(--accent);
    border: 1px solid var(--accent);
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    padding: 2px 10px;
    font-family: var(--font-mono);
    letter-spacing: 0.5px;
  }

  .container {
    max-width: 860px;
    margin: 0 auto;
    padding: 32px 24px 80px;
  }

  .intro {
    color: var(--muted);
    margin-bottom: 32px;
    font-size: 13px;
    line-height: 1.7;
  }

  .intro code {
    font-family: var(--font-mono);
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 3px;
    padding: 1px 5px;
    font-size: 12px;
    color: var(--text);
  }

  .section-label {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--muted);
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
  }

  .field-group {
    margin-bottom: 28px;
  }

  label {
    display: block;
    font-size: 13px;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 6px;
  }

  label .hint {
    font-weight: 400;
    color: var(--muted);
    font-size: 12px;
    margin-left: 6px;
  }

  input[type="text"],
  textarea {
    width: 100%;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    color: var(--text);
    font-family: inherit;
    font-size: 13px;
    padding: 10px 12px;
    resize: vertical;
    transition: border-color 0.15s;
    outline: none;
  }

  input[type="text"]:focus,
  textarea:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 3px var(--accent-dim);
  }

  textarea { min-height: 100px; }
  textarea.tall { min-height: 140px; }

  .actions {
    display: flex;
    gap: 10px;
    margin-top: 32px;
    align-items: center;
  }

  button {
    font-family: inherit;
    font-size: 13px;
    font-weight: 600;
    border: none;
    border-radius: var(--radius);
    padding: 10px 20px;
    cursor: pointer;
    transition: opacity 0.15s, background 0.15s;
  }

  .btn-primary {
    background: var(--accent);
    color: #0d1117;
  }

  .btn-primary:hover { opacity: 0.88; }
  .btn-primary:disabled { opacity: 0.4; cursor: not-allowed; }

  .btn-secondary {
    background: var(--surface);
    color: var(--text);
    border: 1px solid var(--border);
  }

  .btn-secondary:hover { border-color: var(--accent); color: var(--accent); }

  .status {
    font-size: 12px;
    color: var(--muted);
    font-family: var(--font-mono);
  }

  .status.ok { color: var(--success); }
  .status.err { color: #f85149; }

  #result-section {
    margin-top: 48px;
    display: none;
  }

  .result-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
  }

  .result-header h2 {
    font-size: 14px;
    font-weight: 600;
  }

  .result-actions { display: flex; gap: 8px; }

  .saved-path {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--success);
    margin-bottom: 12px;
  }

  pre {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px;
    overflow-x: auto;
    font-family: var(--font-mono);
    font-size: 12px;
    line-height: 1.7;
    white-space: pre-wrap;
    word-break: break-word;
    color: var(--text);
    max-height: 600px;
    overflow-y: auto;
  }

  .two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }

  @media (max-width: 600px) {
    .two-col { grid-template-columns: 1fr; }
    header { padding: 12px 16px; }
    .container { padding: 20px 16px 60px; }
  }
</style>
</head>
<body>

<header>
  <span class="logo"><span>TCode</span> Framework</span>
  <h1>Prompt Zero</h1>
  <span class="step-badge">Step 0</span>
</header>

<div class="container">
  <p class="intro">
    Prompt Zero is the planning step that happens <strong>before any project is created</strong>.
    Fill in your product idea below. The tool will generate a structured prompt that instructs
    your coding agent to classify the project against the TCode Framework and produce a full
    implementation plan — without writing any application code yet.<br><br>
    The result is saved to <code>promptZero/&lt;app-slug&gt;/promptZero.md</code> and ready to paste
    into Claude Code, Cursor, Codex, or Copilot.
  </p>

  <form id="pz-form">

    <div class="section-label">Project Identity</div>

    <div class="field-group">
      <label for="app_name">Application name <span class="hint">exact name used throughout the prompt</span></label>
      <input type="text" id="app_name" name="app_name" placeholder="e.g. CareNav Mini" required>
    </div>

    <div class="field-group">
      <label for="description">One-line description <span class="hint">what it does in one sentence</span></label>
      <input type="text" id="description" name="description" placeholder="e.g. A RAG-powered medical report assistant that navigates patients to nearby care." required>
    </div>

    <div class="two-col">
      <div class="field-group">
        <label for="users">Primary users</label>
        <textarea id="users" name="users" placeholder="Who uses this app and in what context?"></textarea>
      </div>
      <div class="field-group">
        <label for="cloud_target">Cloud deployment target</label>
        <textarea id="cloud_target" name="cloud_target" placeholder="e.g. Oracle Cloud Infrastructure — Compute VM + OCI Object Storage"></textarea>
      </div>
    </div>

    <div class="section-label">Problem & Scope</div>

    <div class="field-group">
      <label for="problem">Core problem</label>
      <textarea id="problem" name="problem" class="tall" placeholder="What specific pain does this solve? Be concrete."></textarea>
    </div>

    <div class="field-group">
      <label for="mvp_capabilities">MVP capabilities <span class="hint">numbered list of what the MVP must do</span></label>
      <textarea id="mvp_capabilities" name="mvp_capabilities" class="tall" placeholder="1. Upload a PDF report&#10;2. Ask questions over it via RAG&#10;3. Get a care-navigation category&#10;..."></textarea>
    </div>

    <div class="section-label">AI & Technical</div>

    <div class="two-col">
      <div class="field-group">
        <label for="llm_requirements">AI / LLM requirements</label>
        <textarea id="llm_requirements" name="llm_requirements" class="tall" placeholder="What should the LLM do? Which providers? Any guardrails?"></textarea>
      </div>
      <div class="field-group">
        <label for="rag_requirements">RAG requirements</label>
        <textarea id="rag_requirements" name="rag_requirements" class="tall" placeholder="Document types, chunk strategy, vector store choice, retrieval flow..."></textarea>
      </div>
    </div>

    <div class="field-group">
      <label for="stack">Preferred stack</label>
      <textarea id="stack" name="stack" placeholder="Backend: FastAPI&#10;Frontend: Streamlit (MVP)&#10;DB: SQLite (local) / PostgreSQL (prod)&#10;Vector store: ChromaDB&#10;Testing: pytest"></textarea>
    </div>

    <div class="field-group">
      <label for="safety_requirements">Safety / compliance requirements</label>
      <textarea id="safety_requirements" name="safety_requirements" class="tall" placeholder="Disclaimers required? Sensitive data handling? PII rules? Emergency escalation? Regulatory constraints?"></textarea>
    </div>

    <div class="actions">
      <button type="submit" class="btn-primary" id="generate-btn">Generate Prompt Zero</button>
      <span class="status" id="status-msg"></span>
    </div>

  </form>

  <div id="result-section">
    <div class="result-header">
      <h2>Generated promptZero.md</h2>
      <div class="result-actions">
        <button class="btn-secondary" onclick="copyResult()">Copy</button>
        <button class="btn-secondary" onclick="downloadResult()">Download</button>
      </div>
    </div>
    <div class="saved-path" id="saved-path"></div>
    <pre id="result-content"></pre>
  </div>
</div>

<script>
  let generatedContent = "";
  let generatedSlug = "";

  document.getElementById("pz-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const btn = document.getElementById("generate-btn");
    const status = document.getElementById("status-msg");

    btn.disabled = true;
    status.className = "status";
    status.textContent = "Generating…";

    const form = e.target;
    const data = new URLSearchParams(new FormData(form));

    try {
      const res = await fetch("/generate", { method: "POST", body: data });
      const json = await res.json();

      if (!res.ok) {
        status.className = "status err";
        status.textContent = json.detail || "Error generating document.";
        return;
      }

      generatedContent = json.content;
      generatedSlug = json.slug;

      document.getElementById("result-content").textContent = generatedContent;
      document.getElementById("saved-path").textContent =
        "Saved → " + json.path;
      document.getElementById("result-section").style.display = "block";
      document.getElementById("result-section").scrollIntoView({ behavior: "smooth" });

      status.className = "status ok";
      status.textContent = "✓ Saved to promptZero/" + generatedSlug + "/promptZero.md";
    } catch (err) {
      status.className = "status err";
      status.textContent = "Request failed: " + err.message;
    } finally {
      btn.disabled = false;
    }
  });

  function copyResult() {
    navigator.clipboard.writeText(generatedContent).then(() => {
      const btn = event.target;
      const orig = btn.textContent;
      btn.textContent = "Copied!";
      setTimeout(() => { btn.textContent = orig; }, 1500);
    });
  }

  function downloadResult() {
    const blob = new Blob([generatedContent], { type: "text/markdown" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = generatedSlug + "-promptZero.md";
    a.click();
    URL.revokeObjectURL(a.href);
  }
</script>

</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML


@app.post("/generate")
async def generate(
    app_name: str = Form(...),
    description: str = Form(...),
    users: str = Form(default=""),
    problem: str = Form(default=""),
    mvp_capabilities: str = Form(default=""),
    llm_requirements: str = Form(default=""),
    rag_requirements: str = Form(default=""),
    cloud_target: str = Form(default=""),
    stack: str = Form(default=""),
    safety_requirements: str = Form(default=""),
):
    slug = slugify(app_name)
    if not slug:
        return JSONResponse(status_code=400, content={"detail": "App name produced an empty slug."})

    content = generate_document(
        app_name=app_name,
        description=description,
        users=users,
        problem=problem,
        mvp_capabilities=mvp_capabilities,
        llm_requirements=llm_requirements,
        rag_requirements=rag_requirements,
        cloud_target=cloud_target,
        stack=stack,
        safety_requirements=safety_requirements,
    )

    output_dir = PROMPT_ZERO_DIR / slug
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "promptZero.md"
    output_file.write_text(content, encoding="utf-8")

    relative_path = output_file.relative_to(WORKSPACE_ROOT)

    return {"slug": slug, "path": str(relative_path), "content": content}
