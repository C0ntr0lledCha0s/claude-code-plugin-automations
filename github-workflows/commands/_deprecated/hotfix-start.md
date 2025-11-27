---
description: Start an emergency hotfix branch from main for critical production fixes
allowed-tools: Bash, Read, Grep, Glob
argument-hint: "<name>"
---

# Hotfix Start

Create a hotfix branch from main for emergency production fixes.

## Usage

```bash
/hotfix-start security-patch             # Create hotfix/security-patch
/hotfix-start critical-login-fix         # Create hotfix/critical-login-fix
```

## Arguments

- **First argument** (required): Hotfix name/description
  - Describes the fix being made
  - Will be formatted as `hotfix/<name>`

**Input validation**: Name must follow conventions (lowercase, hyphens, max 64 chars).

## Workflow

When this command is invoked:

1. **Validate argument**: Check name follows conventions

2. **Load configuration**: Get hotfix flow settings

3. **Invoke managing-branches skill**: Get branching expertise

4. **Check current state**: Warn about uncommitted changes

5. **Create hotfix branch**:
   - Switch to main branch
   - Pull latest from origin
   - Create hotfix branch

6. **Create worktree** (if configured):
   - Isolate hotfix work
   - Keep current work untouched

7. **Show emergency workflow**:
   - Fast-track process
   - Direct merge path
   - Tag creation

## Example Output

```
🚨 Starting emergency hotfix workflow...

Creating hotfix branch from main:
  git checkout main
  git pull origin main
  git checkout -b hotfix/security-patch

✅ Branch: hotfix/security-patch

Creating isolated worktree...
  git worktree add ../worktrees/hotfix hotfix/security-patch

✅ Worktree: ../worktrees/hotfix

FAST TRACK WORKFLOW:
1. Fix the issue in ../worktrees/hotfix
2. Commit: fix(security): patch vulnerability
3. Run: /hotfix-finish security-patch

This will:
- Merge to main AND develop
- Create tag vX.Y.Z
- Delete hotfix branch
```

## Hotfix Best Practices

1. **Keep it minimal**: Fix only the critical issue
2. **Test thoroughly**: Even in emergencies
3. **Document the fix**: Clear commit messages
4. **Notify team**: Communicate the emergency

## When to Use

Use `/hotfix-start` for:
- Security vulnerabilities
- Critical production bugs
- Data corruption issues
- Service outages

Do NOT use for:
- Normal bug fixes (use `/branch-start bugfix`)
- New features
- Non-urgent improvements

## Important Notes

- Hotfixes branch from `main`, not `develop`
- Creates worktree automatically for isolation
- Merges to both `main` AND `develop`
- Creates a version tag automatically

Use this for emergency fixes that can't wait for the normal release cycle!
