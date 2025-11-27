---
description: List all active git worktrees with their branches and status
allowed-tools: Bash, Read, Grep, Glob
argument-hint: ""
---

# Worktree List

Display all active git worktrees with their branches, paths, and status.

## Usage

```bash
/worktree-list
```

## Workflow

When this command is invoked:

1. **Get worktree list**: Query git for all worktrees

2. **Invoke managing-branches skill**: Format output nicely

3. **Show for each worktree**:
   - Path
   - Branch name
   - Commit hash
   - Working directory status (clean/dirty)

4. **Highlight current**: Mark which worktree you're in

5. **Show summary**: Total count and recommendations

## Example Output

```
Active Worktrees
============================================================

1. /home/user/project
   Branch: main (primary)
   Commit: abc1234
   Status: clean

2. /home/user/worktrees/auth
   Branch: feature/auth
   Commit: def5678
   Status: 3 uncommitted changes

3. /home/user/worktrees/hotfix
   Branch: hotfix/security-patch
   Commit: ghi9012
   Status: clean

Total: 3 worktree(s)

Recommendations:
- Worktree #2 has uncommitted changes
- Consider /worktree-clean to remove merged worktrees
```

## Status Indicators

- **clean**: No uncommitted changes
- **N uncommitted changes**: Modified files
- **detached**: Not on a branch
- **(primary)**: The main worktree

## Quick Navigation

To switch to a worktree:
```bash
cd /home/user/worktrees/auth
```

Or use shell navigation:
```bash
pushd ../worktrees/auth
# work...
popd  # return to previous
```

## Important Notes

- Lists all worktrees for the repository
- Shows status of each working directory
- Identifies the current worktree
- Suggests cleanup for merged branches

Use this to see all your parallel development environments!
