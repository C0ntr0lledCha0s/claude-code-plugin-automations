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

1. **Current Branch**: Name, ahead/behind main, related issues, detected scope
2. **Tracked Issues**: Issues from local cache, grouped by context:
   - **Branch Issues**: Issues selected for current branch (from `relatedIssues`)
   - **Scope-Relevant**: Issues matching branch's detected scope label
   - **Project Issues**: Other issues in default project board
   - **All Other**: Remaining cached issues
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
  Detected scope: auth (scope:auth)
  Selected issues: #42, #43

📋 BRANCH ISSUES (selected for this branch):
  #42: Implement JWT authentication [In Progress]
       Labels: feature, priority:high, scope:auth
  #43: Add JWT validation [Open]
       Labels: feature, scope:auth

📋 SCOPE-RELEVANT (matching scope:auth):
  #56: Fix login validation error [Open]
       Labels: bug, priority:high, scope:auth

📋 PROJECT ISSUES (in Agent Plugin Development):
  #78: Add password reset feature [Open]
       Labels: feature, scope:api

📋 OTHER CACHED ISSUES:
  #89: Update documentation [Open]
       Labels: docs

Recent Commits on Branch:
  abc1234 feat(auth): add JWT validation (Refs #42)
  def5678 feat(auth): add token service (Refs #42)
  ghi9012 test(auth): add JWT tests

Open PRs:
  #123: feat(auth): add JWT authentication (ready to merge)
        Closes #42, Closes #43

Project Boards:
  Sprint 5: 3 issues assigned to you
    - #42: In Progress
    - #43: Todo
    - #45: Todo

Pending Reviews:
  #124: fix(api): resolve validation (awaiting your review)

Next Actions:
  1. Merge PR #123 (all checks passed) - will close #42, #43
  2. Review PR #124
  3. Start work on issue #56 (scope-relevant, high priority)
  4. Sync issues: /issue-track sync (cache is 10 min old)
```

## Workflow

When this command is invoked:

1. **Load environment**: Read `.claude/github-workflows/env.json` for context
2. **Check issue cache**: Read `.claude/github-workflows/active-issues.json`
3. **Detect branch context**: Get `relatedIssues`, `detectedScope`, and `scopeLabel`
4. **Group issues by context**:
   - Branch issues: Those in `relatedIssues` array
   - Scope-relevant: Those with matching scope label
   - Project issues: Those in default project board
   - Other: All remaining cached issues
5. **Get git status**: Current branch, commits, ahead/behind
6. **Parse commits**: Extract issue references from recent commits
7. **Get GitHub state**: PRs, boards, pending reviews
8. **Generate actions**: Suggest next steps prioritizing branch and scope-relevant issues

## Issue Cache Integration

The command reads from the local issue cache and environment to:

- Show tracked issues grouped by relevance (branch → scope → project → other)
- Display all selected issues for the current branch
- Show detected scope and matching scope-relevant issues
- Track which issues have been referenced in commits
- Suggest which issues to work on next (prioritizing branch and scope issues)
- Warn when cache is stale (> 60 minutes)

If no cache exists, it suggests running `/issue-track sync`.
If no issues are selected for the branch, it suggests running `/issue-track select`.

Helps you understand where you are in the workflow and what to do next.
