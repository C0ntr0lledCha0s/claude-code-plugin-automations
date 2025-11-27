---
description: Show current branch status, flow information, and related branches
allowed-tools: Bash, Read, Grep, Glob
argument-hint: ""
---

# Branch Status

Show comprehensive information about the current branch, its flow configuration, and related branches.

## Usage

```bash
/branch-status
```

## Workflow

When this command is invoked:

1. **Invoke managing-branches skill**: Activate the branching expertise

2. **Load configuration**: Read `.claude/github-workflows/branching-config.json` for flow settings

3. **Get current branch info**:
   - Branch name
   - Branch type (feature, bugfix, hotfix, release)
   - Base branch and target branch per flow

4. **Check working directory status**:
   - Uncommitted changes
   - Staged files
   - Untracked files

5. **Show commit history**:
   - Recent commits on this branch
   - Commits ahead/behind base branch

6. **List related branches**:
   - Other branches of the same type
   - Active feature/bugfix branches
   - Any release or hotfix branches

7. **Show flow information**:
   - Current strategy (gitflow, github-flow, etc.)
   - Expected merge target
   - Whether PR is required

## What This Shows

```
Branch Status
========================================
Current branch: feature/issue-42-auth
Strategy: gitflow
Branch type: feature
Base: develop
Target: develop

Working directory:
  3 files modified
  1 file staged

Recent commits (since develop):
  abc1234 feat(auth): add login form
  def5678 feat(auth): add validation

Active branches by type:
  feature: 3
    - feature/issue-42-auth (current)
    - feature/dashboard
    - feature/api-refactor
  hotfix: 1
    - hotfix/security-patch

Next steps:
  - Commit remaining changes
  - Create PR to develop when ready
```

## Integration

This command invokes the `managing-branches` skill which provides:

- Branch flow awareness
- Configuration interpretation
- Next step recommendations

It also integrates with:
- `managing-commits` skill for commit analysis
- Issue tracking for related issues

## Important Notes

- Shows flow-aware recommendations
- Identifies blocked or stale branches
- Suggests cleanup for merged branches
- Works with all configured strategies

Use this to understand your current branch context and next actions!
