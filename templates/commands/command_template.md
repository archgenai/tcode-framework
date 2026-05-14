# /command-name
# TCode Command Template
# Copy to .claude/commands/<command-name>.md and fill in the sections below.
# The filename (without .md) is the slash command the agent will expose.

---

## Purpose

One sentence: what this command does and when to invoke it.

---

## When to use

- Condition 1 — e.g. "after implementing a new feature"
- Condition 2 — e.g. "before opening a PR"

## When NOT to use

- Condition 1 — e.g. "mid-implementation while changes are incomplete"

---

## Steps

The agent executes these steps in order when this command is invoked.

1. **Step name** — what to do. Be specific: file paths, tool calls, expected outputs.
2. **Step name** — ...
3. **Step name** — ...

---

## Output

Describe what the agent should produce or report at the end. Example:
- A summary table of findings
- A commit with a specific message format
- A file written to a specific path

---

## Scope

| Scope | Value |
|---|---|
| Level | workspace / project (delete one) |
| Reads | list of files or directories this command reads |
| Writes | list of files or directories this command writes |
| Side effects | any external actions (git commit, push, API call) |

---

## Notes

Any non-obvious constraints, edge cases, or links to ADRs that inform this command's design.
