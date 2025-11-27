---
description: Clean up worktrees for merged branches and prune stale references
allowed-tools: Bash, Read, Grep, Glob
argument-hint: "[--dry-run]"
---

# Worktree Clean

Remove worktrees for branches that have been merged and prune stale references.

## Usage

```bash
/worktree-clean                          # Clean merged worktrees
/worktree-clean --dry-run                # Preview what would be cleaned
```

## Arguments

- **--dry-run** (optional): Show what would be cleaned without removing

## Workflow

When this command is invoked:

1. **Get merged branches**: Find branches merged to main

2. **Find worktrees**: Identify worktrees with merged branches

3. **Invoke managing-branches skill**: Get cleanup expertise

4. **Show cleanup plan**: List worktrees to remove

5. **Confirm action**: Ask for user confirmation

6. **Remove worktrees**: Delete each merged worktree

7. **Delete branches**: Remove merged branches

8. **Prune references**: Clean up stale git refs

## Example Output

```
Checking for merged branches...

Found 2 worktree(s) with merged branches:

1. /home/user/worktrees/old-feature
   Branch: feature/old-feature
   Merged to: main

2. /home/user/worktrees/bugfix
   Branch: bugfix/validation-error
   Merged to: main

Remove these worktrees? [y/N] y

Removing worktrees...
✅ Removed: /home/user/worktrees/old-feature
✅ Deleted branch: feature/old-feature
✅ Removed: /home/user/worktrees/bugfix
✅ Deleted branch: bugfix/validation-error

Pruning stale references...
✅ Pruned

Cleanup complete!
```

## Dry Run

Preview without making changes:

```bash
/worktree-clean --dry-run

# Output:
Found 2 worktree(s) with merged branches:
  - /home/user/worktrees/old-feature (feature/old-feature)
  - /home/user/worktrees/bugfix (bugfix/validation-error)

Dry run - no worktrees removed
```

## What Gets Cleaned

1. **Worktrees for merged branches**: Branches merged to main
2. **Local branches**: Deleted after worktree removal
3. **Stale references**: Orphaned git refs

## What's Preserved

- Main/primary worktree
- Worktrees with uncommitted changes (unless forced)
- Branches not yet merged
- Remote tracking branches

## Important Notes

- Only cleans branches merged to main
- Asks for confirmation before deletion
- Use --dry-run to preview safely
- Uncommitted changes prevent removal

Use this regularly to keep your worktree space clean!
