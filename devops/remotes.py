#!/usr/bin/env python3
"""
devops/remotes.py — Provider-agnostic Git remote manager for TCode.

Supports: gogs, gitea, forgejo, github, gitlab, bitbucket.

Usage:
    python3 devops/remotes.py create-repo --name my-app --private
    python3 devops/remotes.py create-pr --title "feat: ..." --head feat/x --base main
    python3 devops/remotes.py add-webhook --url http://localhost:9000/hook
    python3 devops/remotes.py list-remotes
    python3 devops/remotes.py push-all [--include-backup]

Configuration is read from devops/config.yaml (relative to TCode root).
Tokens are read from environment variables named in config (never from config file).
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

# ── Config loading ─────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent.parent.resolve()


def _load_config() -> dict:
    config_path = ROOT / "devops" / "config.yaml"
    if not config_path.exists():
        example = ROOT / "devops" / "config.example.yaml"
        sys.exit(
            f"devops/config.yaml not found.\n"
            f"Copy the template and fill in your values:\n"
            f"  cp {example} {config_path}"
        )
    if not _HAS_YAML:
        sys.exit(
            "PyYAML is required: pip install pyyaml"
        )
    with open(config_path) as f:
        return yaml.safe_load(f)


# ── HTTP helpers ───────────────────────────────────────────────────────────────

def _http(
    method: str,
    url: str,
    token: str,
    token_scheme: str = "token",  # "token" for Gogs/Gitea, "Bearer" for GitHub/GitLab
    body: dict | None = None,
    extra_headers: dict | None = None,
) -> dict:
    data = json.dumps(body).encode() if body else None
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"{token_scheme} {token}",
    }
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        body_text = e.read().decode(errors="replace")
        sys.exit(f"HTTP {e.code} from {url}:\n{body_text}")


# ── Provider base ──────────────────────────────────────────────────────────────

@dataclass
class RemoteConfig:
    id: str
    type: str          # gogs | gitea | forgejo | github | gitlab | bitbucket
    label: str
    url: str           # base URL, no trailing slash
    owner: str
    token_env: str
    role: str          # primary | mirror | backup
    auto_push: bool = True

    @property
    def token(self) -> str:
        t = os.environ.get(self.token_env, "")
        if not t:
            sys.exit(
                f"Token not set for remote '{self.id}'.\n"
                f"Set the environment variable: export {self.token_env}=your-token"
            )
        return t


class BaseProvider:
    def __init__(self, cfg: RemoteConfig):
        self.cfg = cfg

    def create_repo(self, name: str, description: str = "", private: bool = True) -> dict:
        raise NotImplementedError

    def create_pr(self, repo: str, title: str, body: str, head: str, base: str) -> dict:
        raise NotImplementedError

    def add_webhook(self, repo: str, url: str, secret: str, events: list[str] | None = None) -> dict:
        raise NotImplementedError

    def repo_clone_url(self, repo: str) -> str:
        raise NotImplementedError


# ── Gogs provider ─────────────────────────────────────────────────────────────

class GogsProvider(BaseProvider):
    """
    Supports Gogs. Also works for Gitea and Forgejo (superset of Gogs API).
    Critical limitation: Gogs has no PR creation API endpoint.
    See: https://github.com/gogs/gogs/issues/5871
    """

    def _api(self, method: str, path: str, body: dict | None = None) -> dict:
        url = f"{self.cfg.url}/api/v1{path}"
        return _http(method, url, self.cfg.token, token_scheme="token", body=body)

    def create_repo(self, name: str, description: str = "", private: bool = True) -> dict:
        result = self._api("POST", f"/user/repos", {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": False,
        })
        print(f"[{self.cfg.id}] Created repo: {result.get('full_name', name)}")
        return result

    def create_pr(self, repo: str, title: str, body: str, head: str, base: str) -> dict:
        # Gogs has no PR creation API. Print the URL for the user to open manually.
        pr_url = f"{self.cfg.url}/{self.cfg.owner}/{repo}/compare/{base}...{head}"
        print(
            f"\n[{self.cfg.id}] Gogs does not support PR creation via API.\n"
            f"Open this URL in your browser to create the PR:\n\n"
            f"  {pr_url}\n"
        )
        _try_open_browser(pr_url)
        return {"url": pr_url, "note": "manual — Gogs API limitation"}

    def add_webhook(self, repo: str, target_url: str, secret: str, events: list[str] | None = None) -> dict:
        events = events or ["push", "pull_request"]
        result = self._api("POST", f"/repos/{self.cfg.owner}/{repo}/hooks", {
            "type": "gogs",
            "config": {"url": target_url, "content_type": "json", "secret": secret},
            "events": events,
            "active": True,
        })
        print(f"[{self.cfg.id}] Webhook added → {target_url}")
        return result

    def repo_clone_url(self, repo: str) -> str:
        return f"{self.cfg.url}/{self.cfg.owner}/{repo}.git"


# ── Gitea / Forgejo provider ──────────────────────────────────────────────────

class GiteaProvider(GogsProvider):
    """
    Gitea and Forgejo are fully API-compatible supersets of Gogs.
    PR creation works here (unlike Gogs).
    """

    def create_pr(self, repo: str, title: str, body: str, head: str, base: str) -> dict:
        result = self._api("POST", f"/repos/{self.cfg.owner}/{repo}/pulls", {
            "title": title,
            "body": body,
            "head": head,
            "base": base,
        })
        url = result.get("html_url", "")
        print(f"[{self.cfg.id}] PR created: {url}")
        return result


# ── GitHub provider ───────────────────────────────────────────────────────────

class GitHubProvider(BaseProvider):
    """
    Supports github.com and GitHub Enterprise.
    """

    def _api_url(self) -> str:
        if "github.com" in self.cfg.url:
            return "https://api.github.com"
        # GitHub Enterprise: <host>/api/v3
        return f"{self.cfg.url}/api/v3"

    def _api(self, method: str, path: str, body: dict | None = None) -> dict:
        url = f"{self._api_url()}{path}"
        return _http(
            method, url, self.cfg.token, token_scheme="Bearer",
            extra_headers={"X-GitHub-Api-Version": "2022-11-28"},
            body=body,
        )

    def create_repo(self, name: str, description: str = "", private: bool = True) -> dict:
        result = self._api("POST", "/user/repos", {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": False,
        })
        print(f"[{self.cfg.id}] Created repo: {result.get('full_name', name)}")
        return result

    def create_pr(self, repo: str, title: str, body: str, head: str, base: str) -> dict:
        result = self._api("POST", f"/repos/{self.cfg.owner}/{repo}/pulls", {
            "title": title,
            "body": body,
            "head": head,
            "base": base,
        })
        url = result.get("html_url", "")
        print(f"[{self.cfg.id}] PR created: {url}")
        return result

    def add_webhook(self, repo: str, target_url: str, secret: str, events: list[str] | None = None) -> dict:
        events = events or ["push", "pull_request"]
        result = self._api("POST", f"/repos/{self.cfg.owner}/{repo}/hooks", {
            "name": "web",
            "config": {"url": target_url, "content_type": "json", "secret": secret},
            "events": events,
            "active": True,
        })
        print(f"[{self.cfg.id}] Webhook added → {target_url}")
        return result

    def repo_clone_url(self, repo: str) -> str:
        return f"https://github.com/{self.cfg.owner}/{repo}.git"


# ── GitLab provider ───────────────────────────────────────────────────────────

class GitLabProvider(BaseProvider):
    """
    Supports gitlab.com and self-hosted GitLab.
    Note: GitLab calls pull requests "merge requests" (MRs).
    """

    def _api(self, method: str, path: str, body: dict | None = None) -> dict:
        url = f"{self.cfg.url}/api/v4{path}"
        return _http(
            method, url, self.cfg.token, token_scheme="Bearer",
            extra_headers={"PRIVATE-TOKEN": self.cfg.token},
            body=body,
        )

    def _project_path(self, repo: str) -> str:
        return urllib.parse.quote(f"{self.cfg.owner}/{repo}", safe="")

    def create_repo(self, name: str, description: str = "", private: bool = True) -> dict:
        visibility = "private" if private else "public"
        result = self._api("POST", "/projects", {
            "name": name,
            "description": description,
            "visibility": visibility,
            "initialize_with_readme": False,
        })
        print(f"[{self.cfg.id}] Created project: {result.get('path_with_namespace', name)}")
        return result

    def create_pr(self, repo: str, title: str, body: str, head: str, base: str) -> dict:
        result = self._api("POST", f"/projects/{self._project_path(repo)}/merge_requests", {
            "title": title,
            "description": body,
            "source_branch": head,
            "target_branch": base,
        })
        url = result.get("web_url", "")
        print(f"[{self.cfg.id}] MR created: {url}")
        return result

    def add_webhook(self, repo: str, target_url: str, secret: str, events: list[str] | None = None) -> dict:
        result = self._api("POST", f"/projects/{self._project_path(repo)}/hooks", {
            "url": target_url,
            "token": secret,
            "push_events": True,
            "merge_requests_events": True,
            "enable_ssl_verification": False,
        })
        print(f"[{self.cfg.id}] Webhook added → {target_url}")
        return result

    def repo_clone_url(self, repo: str) -> str:
        base = self.cfg.url.rstrip("/")
        return f"{base}/{self.cfg.owner}/{repo}.git"


# ── Bitbucket provider ────────────────────────────────────────────────────────

class BitbucketProvider(BaseProvider):
    """
    Supports Bitbucket Cloud (bitbucket.org).
    Uses App Password authentication (token = app password).
    """

    def _api(self, method: str, path: str, body: dict | None = None) -> dict:
        url = f"https://api.bitbucket.org/2.0{path}"
        # Bitbucket uses Basic auth: username:app-password
        import base64
        cred = base64.b64encode(f"{self.cfg.owner}:{self.cfg.token}".encode()).decode()
        return _http(method, url, cred, token_scheme="Basic", body=body)

    def create_repo(self, name: str, description: str = "", private: bool = True) -> dict:
        result = self._api("POST", f"/repositories/{self.cfg.owner}/{name}", {
            "scm": "git",
            "description": description,
            "is_private": private,
        })
        print(f"[{self.cfg.id}] Created repo: {result.get('full_name', name)}")
        return result

    def create_pr(self, repo: str, title: str, body: str, head: str, base: str) -> dict:
        result = self._api("POST", f"/repositories/{self.cfg.owner}/{repo}/pullrequests", {
            "title": title,
            "description": body,
            "source": {"branch": {"name": head}},
            "destination": {"branch": {"name": base}},
        })
        url = result.get("links", {}).get("html", {}).get("href", "")
        print(f"[{self.cfg.id}] PR created: {url}")
        return result

    def add_webhook(self, repo: str, target_url: str, secret: str, events: list[str] | None = None) -> dict:
        result = self._api("POST", f"/repositories/{self.cfg.owner}/{repo}/hooks", {
            "description": "TCode CI",
            "url": target_url,
            "active": True,
            "events": ["repo:push", "pullrequest:created", "pullrequest:updated"],
        })
        print(f"[{self.cfg.id}] Webhook added → {target_url}")
        return result

    def repo_clone_url(self, repo: str) -> str:
        return f"https://bitbucket.org/{self.cfg.owner}/{repo}.git"


# ── Provider factory ──────────────────────────────────────────────────────────

_PROVIDER_MAP = {
    "gogs":      GogsProvider,
    "gitea":     GiteaProvider,
    "forgejo":   GiteaProvider,   # Forgejo is API-compatible with Gitea
    "github":    GitHubProvider,
    "gitlab":    GitLabProvider,
    "bitbucket": BitbucketProvider,
}


def _make_provider(cfg: RemoteConfig) -> BaseProvider:
    cls = _PROVIDER_MAP.get(cfg.type)
    if not cls:
        sys.exit(f"Unknown provider type '{cfg.type}'. Supported: {list(_PROVIDER_MAP)}")
    return cls(cfg)


# ── Remote manager ────────────────────────────────────────────────────────────

class RemoteManager:
    def __init__(self):
        self._config = _load_config()
        self._remotes: list[RemoteConfig] = []
        self._providers: dict[str, BaseProvider] = {}
        for r in self._config.get("remotes", []):
            rc = RemoteConfig(**{k: v for k, v in r.items() if k in RemoteConfig.__dataclass_fields__})
            self._remotes.append(rc)
            self._providers[rc.id] = _make_provider(rc)

    def primary(self) -> BaseProvider | None:
        for r in self._remotes:
            if r.role == "primary":
                return self._providers[r.id]
        return None

    def auto_push_remotes(self, include_backup: bool = False) -> list[tuple[RemoteConfig, BaseProvider]]:
        result = []
        for r in self._remotes:
            if r.auto_push and (r.role != "backup" or include_backup):
                result.append((r, self._providers[r.id]))
        return result

    def create_repo(self, name: str, description: str = "", private: bool = True) -> None:
        for r, p in self.auto_push_remotes():
            try:
                p.create_repo(name, description, private)
            except SystemExit as e:
                print(f"[{r.id}] Skipped: {e}")

    def create_pr(self, repo: str, title: str, body: str, head: str, base: str) -> None:
        p = self.primary()
        if not p:
            sys.exit("No primary remote configured.")
        p.create_pr(repo, title, body, head, base)

    def add_webhook(self, repo: str, url: str, secret: str) -> None:
        for r, p in self.auto_push_remotes():
            try:
                p.add_webhook(repo, url, secret)
            except SystemExit as e:
                print(f"[{r.id}] Skipped: {e}")

    def list_remotes(self) -> None:
        print(f"\nConfigured remotes ({len(self._remotes)}):\n")
        for r in self._remotes:
            token_set = "✓" if os.environ.get(r.token_env) else "✗ (not set)"
            print(
                f"  {r.id:<16} type={r.type:<12} role={r.role:<8} "
                f"auto_push={str(r.auto_push):<6} token={token_set}"
            )
        print()

    def push_all(self, project_dir: Path, branch: str, include_backup: bool = False) -> None:
        for r, p in self.auto_push_remotes(include_backup):
            clone_url = p.repo_clone_url(project_dir.name)
            # Ensure remote is registered in this repo
            _git_ensure_remote(project_dir, r.id, clone_url, r.token)
            print(f"[{r.id}] Pushing {branch} → {clone_url}")
            result = subprocess.run(
                ["git", "push", r.id, branch],
                cwd=project_dir, capture_output=True, text=True,
            )
            if result.returncode != 0:
                print(f"  ERROR: {result.stderr.strip()}")
            else:
                print(f"  OK")


# ── Git helpers ───────────────────────────────────────────────────────────────

def _git_ensure_remote(project_dir: Path, name: str, url: str, token: str) -> None:
    """Add or update a git remote, embedding the token in the URL."""
    parsed = urllib.parse.urlparse(url)
    auth_url = parsed._replace(
        netloc=f"oauth2:{token}@{parsed.netloc}"
    ).geturl()

    result = subprocess.run(
        ["git", "remote", "get-url", name],
        cwd=project_dir, capture_output=True,
    )
    if result.returncode == 0:
        subprocess.run(["git", "remote", "set-url", name, auth_url], cwd=project_dir, check=True)
    else:
        subprocess.run(["git", "remote", "add", name, auth_url], cwd=project_dir, check=True)


def _try_open_browser(url: str) -> None:
    try:
        import webbrowser
        webbrowser.open(url)
    except Exception:
        pass


# ── CLI ────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="TCode provider-agnostic remote manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # list-remotes
    sub.add_parser("list-remotes", help="Show all configured remotes and token status")

    # create-repo
    p_cr = sub.add_parser("create-repo", help="Create repo on all auto-push remotes")
    p_cr.add_argument("--name", required=True)
    p_cr.add_argument("--description", default="")
    p_cr.add_argument("--public", action="store_true", help="Create as public repo")

    # create-pr
    p_pr = sub.add_parser("create-pr", help="Create PR on primary remote")
    p_pr.add_argument("--repo", required=True, help="Repository name")
    p_pr.add_argument("--title", required=True)
    p_pr.add_argument("--body", default="")
    p_pr.add_argument("--head", required=True, help="Source branch")
    p_pr.add_argument("--base", default="main", help="Target branch")

    # add-webhook
    p_wh = sub.add_parser("add-webhook", help="Register CI webhook on all auto-push remotes")
    p_wh.add_argument("--repo", required=True)
    p_wh.add_argument("--url", required=True, help="Webhook endpoint URL")
    p_wh.add_argument("--secret-env", default="WEBHOOK_SECRET",
                       help="Env var name holding the HMAC secret")

    # push-all
    p_pa = sub.add_parser("push-all", help="Push current branch to all auto-push remotes")
    p_pa.add_argument("--project", help="Project folder name (default: current dir)")
    p_pa.add_argument("--branch", help="Branch to push (default: current branch)")
    p_pa.add_argument("--include-backup", action="store_true")

    args = parser.parse_args()
    mgr = RemoteManager()

    if args.cmd == "list-remotes":
        mgr.list_remotes()

    elif args.cmd == "create-repo":
        mgr.create_repo(args.name, args.description, private=not args.public)

    elif args.cmd == "create-pr":
        mgr.create_pr(args.repo, args.title, args.body, args.head, args.base)

    elif args.cmd == "add-webhook":
        secret = os.environ.get(args.secret_env, "")
        if not secret:
            sys.exit(f"Webhook secret not set. Run: export {args.secret_env}=your-secret")
        mgr.add_webhook(args.repo, args.url, secret)

    elif args.cmd == "push-all":
        if args.project:
            project_dir = ROOT / "projects" / args.project
        else:
            project_dir = Path.cwd()
        if args.branch:
            branch = args.branch
        else:
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=project_dir, text=True
            ).strip()
        mgr.push_all(project_dir, branch, include_backup=args.include_backup)


if __name__ == "__main__":
    main()
