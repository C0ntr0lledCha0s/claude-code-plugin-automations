---
description: Create a git worktree for parallel development on multiple branches
allowed-tools: Bash, Read, Grep, Glob
argument-hint: "<branch> [--path PATH]"
---

# Worktree Add

Create a new git worktree to work on multiple branches simultaneously.

## Usage

```bash
/worktree-add feature/auth               # Auto-generate path
/worktree-add hotfix/urgent --path ../hotfix  # Custom path
```

## Arguments

- **First argument** (required): Branch name
  - Existing branch or new branch to create
  - Will be checked out in the worktree

- **--path PATH** (optional): Custom worktree path
  - If omitted, auto-generates from branch name
  - Relative to configured base directory

## Workflow

When this command is invoked:

1. **Validate branch**: Check if branch exists or can be created

2. **Determine path**: Auto-generate or use provided path

3. **Invoke managing-branches skill**: Get worktree expertise

4. **Check prerequisites**:
   - Branch not already checked out elsewhere
   - Path doesn't already exist

5. **Create worktree**:
   - For existing branch: `git worktree add <path> <branch>`
   - For new branch: `git worktree add -b <branch> <path> <base>`

6. **Show navigation**: How to switch to worktree

## Example Output

```
Creating worktree for feature/auth...

Branch: feature/auth
Path: ../worktrees/auth

Creating worktree:
  git worktree add ../worktrees/auth feature/auth

✅ Worktree created: ../worktrees/auth

To work in this worktree:
  cd ../worktrees/auth

Current worktrees:
  1. /home/user/project (main)
  2. /home/user/worktrees/auth (feature/auth) ← NEW
```

## Use Cases

### Parallel Feature Development
```bash
/worktree-add feature/dashboard
# Continue main work while building dashboard
```

### PR Review
```bash
/worktree-add pr-123
# Review PR without disrupting current work
```

### Emergency Hotfix
```bash
/worktree-add hotfix/critical
# Fix production while keeping feature work
```

### Release Preparation
```bash
/worktree-add release/2.0.0
# Prepare release while features continue
```

## Path Configuration

Worktree paths are determined by:

1. **Custom path**: If `--path` provided
2. **Auto-generate**: Based on branch name and config

Default base directory: `../worktrees`

Configure in `.claude/github-workflows/branching-config.json`:
```json
{
  "worktrees": {
    "baseDir": "../worktrees"
  }
}
```

## Important Notes

- Each branch can only be in ONE worktree
- Worktrees share the same git history
- Commits in any worktree are visible in all
- Use `/worktree-clean` to remove merged worktrees

Use this to work on multiple branches without stashing or context switching!
