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

1. **Current Branch**: Name, ahead/behind main, related issue
2. **Tracked Issues**: Issues from local cache (`.claude/github-workflows/active-issues.json`)
3. **Recent Commits**: Last 5 commits on branch with issue references
4. **Open PRs**: From this branch or assigned to you
5. **Project Boards**: Issues in boards
6. **Pending Reviews**: PRs awaiting your review
7. **Next Actions**: Suggested next steps based on issues and commits

## Example Output

```
Current Branch: feature/auth
  5 commits ahead of main
  Last commit: feat(auth): add JWT validation
  Related issue: #42 "Implement JWT authentication"

Tracked Issues (synced 10 min ago):
  📋 HIGH PRIORITY:
    #42: Implement JWT authentication [In Progress]
         Branch: feature/auth (current)
    #56: Fix login validation error [Open]

  📋 NORMAL:
    #78: Add password reset feature [Open]

Recent Commits on Branch:
  abc1234 feat(auth): add JWT validation (Refs #42)
  def5678 feat(auth): add token service (Refs #42)
  ghi9012 test(auth): add JWT tests

Open PRs:
  #123: feat(auth): add JWT authentication (ready to merge)
        Closes #42

Project Boards:
  Sprint 5: 3 issues assigned to you
    - #42: In Progress
    - #43: Todo
    - #45: Todo

Pending Reviews:
  #124: fix(api): resolve validation (awaiting your review)

Next Actions:
  1. Merge PR #123 (all checks passed) - will close #42
  2. Review PR #124
  3. Start work on issue #56 (high priority)
  4. Sync issues: /issue-track sync (cache is 10 min old)
```

## Workflow

When this command is invoked:

1. **Check issue cache**: Read `.github-workflows/active-issues.json`
2. **Detect branch issue**: Match branch name to tracked issues
3. **Get git status**: Current branch, commits, ahead/behind
4. **Parse commits**: Extract issue references from recent commits
5. **Get GitHub state**: PRs, boards, pending reviews
6. **Generate actions**: Suggest next steps based on all data

## Issue Cache Integration

The command reads from the local issue cache to:

- Show tracked issues with their status
- Highlight which issue the current branch relates to
- Track which issues have been referenced in commits
- Suggest which issues to work on next
- Warn when cache is stale (> 60 minutes)

If no cache exists, it suggests running `/issue-track sync`.

Helps you understand where you are in the workflow and what to do next.
