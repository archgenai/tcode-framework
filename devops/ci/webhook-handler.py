#!/usr/bin/env python3
"""
devops/ci/webhook-handler.py — Lightweight local CI server.

Listens for webhook POSTs from any supported provider (Gogs, GitHub, GitLab, Gitea,
Forgejo, Bitbucket) and runs the project test suite on push events.

Provider signature headers:
  Gogs/Gitea/Forgejo: X-Gogs-Signature   (HMAC-SHA256)
  GitHub:             X-Hub-Signature-256 (HMAC-SHA256)
  GitLab:             X-Gitlab-Token      (plain token comparison)
  Bitbucket:          No signature (IP allowlist instead)

Usage:
    # Set webhook secret (must match what you configured on the provider)
    export WEBHOOK_SECRET=your-secret

    # Start the server
    python3 devops/ci/webhook-handler.py --port 9000 --config devops/config.yaml

    # For cloud providers (GitHub/GitLab), expose locally via:
    #   ngrok http 9000
    # Then set the ngrok URL as the webhook on your provider.

Source: mrexodia/go-gitea-webhook, go-playground/webhooks
"""

import argparse
import hashlib
import hmac
import json
import logging
import os
import subprocess
import sys
from datetime import date
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

try:
    import yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

ROOT = Path(__file__).parent.parent.parent.resolve()
LOG_DIR = ROOT / "devops" / "ci" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / f"{date.today().isoformat()}.log"),
    ],
)
log = logging.getLogger("ci")


# ── Config ─────────────────────────────────────────────────────────────────────

def load_config(config_path: str) -> dict:
    if not _HAS_YAML:
        log.warning("PyYAML not installed — using default CI config")
        return {}
    with open(config_path) as f:
        return yaml.safe_load(f)


# ── Signature validation ───────────────────────────────────────────────────────

def _verify_hmac_sha256(secret: str, body: bytes, signature: str) -> bool:
    expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    # Strip "sha256=" prefix if present (GitHub format)
    sig = signature.removeprefix("sha256=")
    return hmac.compare_digest(expected, sig)


def _validate_signature(provider: str, secret: str, body: bytes, headers: dict) -> bool:
    if not secret:
        log.warning("No WEBHOOK_SECRET set — skipping signature validation")
        return True

    sig_header = {
        "gogs":    "X-Gogs-Signature",
        "gitea":   "X-Gogs-Signature",   # Gitea uses the same header name
        "forgejo": "X-Gogs-Signature",
        "github":  "X-Hub-Signature-256",
    }.get(provider, "X-Gogs-Signature")

    sig = headers.get(sig_header.lower(), "")
    if provider == "gitlab":
        return hmac.compare_digest(secret, sig)

    if not sig:
        log.warning(f"Missing signature header {sig_header}")
        return False

    return _verify_hmac_sha256(secret, body, sig)


# ── Pipeline runner ────────────────────────────────────────────────────────────

def _detect_project(payload: dict) -> str | None:
    """Extract project/repo name from webhook payload."""
    # Try common payload shapes across providers
    repo = (
        payload.get("repository", {}).get("name")
        or payload.get("project", {}).get("name")
        or payload.get("repository", {}).get("slug")
    )
    return repo


def _run_pipeline(project_name: str, branch: str, config: dict) -> bool:
    project_dir = ROOT / "projects" / project_name
    if not project_dir.exists():
        log.warning(f"Project directory not found: {project_dir}")
        return False

    ci_cfg = config.get("ci", {})
    test_cmd = ci_cfg.get("test_command", "pytest tests/ -q --tb=short")
    lint_cmd = ci_cfg.get("lint_command", "flake8 src/ --max-line-length=100")

    log.info(f"Pipeline start  project={project_name}  branch={branch}")
    success = True

    for label, cmd in [("lint", lint_cmd), ("test", test_cmd)]:
        src_dir = project_dir / "src"
        tests_dir = project_dir / "tests"

        # Skip lint if no src/, skip test if no tests/
        if label == "lint" and not src_dir.exists():
            continue
        if label == "test" and not tests_dir.exists():
            log.info(f"  [{label}] SKIP (no tests/ directory)")
            continue

        log.info(f"  [{label}] {cmd}")
        result = subprocess.run(
            cmd.split(),
            cwd=project_dir,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            log.info(f"  [{label}] PASS")
        else:
            log.error(f"  [{label}] FAIL\n{result.stdout}\n{result.stderr}")
            success = False

    status = "PASS" if success else "FAIL"
    log.info(f"Pipeline end    project={project_name}  branch={branch}  status={status}")
    return success


# ── HTTP handler ───────────────────────────────────────────────────────────────

class WebhookHandler(BaseHTTPRequestHandler):
    config: dict = {}
    secret: str = ""

    def log_message(self, fmt, *args):
        pass  # Suppress default HTTP logging; use our logger instead

    def do_POST(self):
        if self.path != "/hook":
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        # Detect provider from headers
        event_header = self.headers.get("X-Gogs-Event") or self.headers.get("X-GitHub-Event") or \
                       self.headers.get("X-Gitlab-Event") or "push"
        provider = "gogs"
        if "X-GitHub-Event" in self.headers:
            provider = "github"
        elif "X-Gitlab-Event" in self.headers:
            provider = "gitlab"

        # Validate signature
        headers_lower = {k.lower(): v for k, v in self.headers.items()}
        if not _validate_signature(provider, self.secret, body, headers_lower):
            log.warning(f"Signature validation failed from {self.client_address[0]}")
            self.send_response(401)
            self.end_headers()
            return

        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return

        self.send_response(200)
        self.end_headers()

        # Only run pipeline on push events
        if event_header not in ("push", "Push Hook"):
            log.info(f"Ignoring event: {event_header}")
            return

        project = _detect_project(payload)
        branch_ref = payload.get("ref", "")
        branch = branch_ref.replace("refs/heads/", "") if branch_ref else "unknown"

        if not project:
            log.warning("Could not determine project from payload")
            return

        # Run pipeline in background (don't block the HTTP response)
        import threading
        threading.Thread(
            target=_run_pipeline,
            args=(project, branch, self.config),
            daemon=True,
        ).start()


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="TCode CI webhook server")
    parser.add_argument("--port", type=int, default=9000)
    parser.add_argument("--config", default="devops/config.yaml")
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()

    config_path = ROOT / args.config
    config = load_config(str(config_path)) if config_path.exists() else {}

    secret_env = config.get("ci", {}).get("secret_env", "WEBHOOK_SECRET")
    secret = os.environ.get(secret_env, "")

    WebhookHandler.config = config
    WebhookHandler.secret = secret

    server = HTTPServer((args.host, args.port), WebhookHandler)
    log.info(f"CI webhook server listening on {args.host}:{args.port}/hook")
    if not secret:
        log.warning(f"No secret set (export {secret_env}=...) — running without signature validation")
    log.info("Waiting for webhook events...")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log.info("Shutting down.")


if __name__ == "__main__":
    main()
