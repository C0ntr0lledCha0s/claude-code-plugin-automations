---
description: Show current workflow state (branch, commits, PRs, board status) and suggest next actions
allowed-tools: Bash, Read
---

# Workflow Status

Display current GitHub workflow state and suggest next actions.

## Usage

```bash
/workflow-status
```

## What This Shows

1. **Current Branch**: Name, ahead/behind main
2. **Recent Commits**: Last 5 commits on branch
3. **Open PRs**: From this branch or assigned to you
4. **Project Boards**: Issues in boards
5. **Pending Reviews**: PRs awaiting your review
6. **Next Actions**: Suggested next steps

## Example Output

```
Current Branch: feature/auth
  5 commits ahead of main
  Last commit: feat(auth): add JWT validation

Open PRs:
  #123: feat(auth): add JWT authentication (ready to merge)

Project Boards:
  Sprint 5: 3 issues assigned to you
    - #42: In Progress
    - #43: Todo
    - #45: Todo

Pending Reviews:
  #124: fix(api): resolve validation (awaiting your review)

Next Actions:
  1. Merge PR #123 (all checks passed)
  2. Review PR #124
  3. Start work on issue #43
```

Helps you understand where you are in the workflow and what to do next.
