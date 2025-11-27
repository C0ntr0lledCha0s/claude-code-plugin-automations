---
description: Review commit history for quality, format compliance, and suggest improvements
allowed-tools: Bash, Read
argument-hint: "[branch-name]"
---

# Review Commit History

Analyze commits for quality and conventional commit compliance.

## Usage

```bash
/commit-review
/commit-review feature/auth
```

## Arguments

- **First argument** (optional): Branch name to review. Default: current branch vs main

## What This Does

1. Analyzes commit messages for conventional format
2. Checks commit quality (size, atomicity, clarity)
3. Identifies issues (WIP commits, poor messages)
4. Suggests improvements (squash, reword, split)
5. Offers to fix issues via interactive rebase
