#!/usr/bin/env python3
"""
create-pr.py — Create a pull request (or MR) on the primary configured provider.

Usage:
    python3 devops/scripts/create-pr.py \
        --repo budget-tracker-poc \
        --title "feat(ocr): receipt extraction pipeline" \
        --head feat/receipt-ocr \
        --base main

    # Read body from file:
    python3 devops/scripts/create-pr.py \
        --repo budget-tracker-poc \
        --title "feat(ocr): receipt extraction pipeline" \
        --head feat/receipt-ocr \
        --body-file /tmp/pr-body.md

The body can use Markdown. For best results, include:
  - What this PR does (one paragraph)
  - Test plan (bulleted checklist)
  - Any breaking changes

For Gogs: opens the compare URL in your browser (no PR API available).
For GitHub/GitLab/Gitea: creates the PR/MR via API and prints the URL.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import argparse
from devops.remotes import RemoteManager


def main() -> None:
    parser = argparse.ArgumentParser(description="Create PR on primary provider")
    parser.add_argument("--repo", required=True, help="Repository name")
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", default="", help="PR body text (Markdown)")
    parser.add_argument("--body-file", help="Read PR body from this file")
    parser.add_argument("--head", required=True, help="Source branch")
    parser.add_argument("--base", default="main", help="Target branch")
    args = parser.parse_args()

    body = args.body
    if args.body_file:
        body = Path(args.body_file).read_text()

    mgr = RemoteManager()
    mgr.create_pr(args.repo, args.title, body, args.head, args.base)


if __name__ == "__main__":
    main()
