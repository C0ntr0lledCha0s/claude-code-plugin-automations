---
description: Finish a branch by merging it following the configured flow rules
allowed-tools: Bash, Read, Grep, Glob
argument-hint: "[branch-name]"
---

# Branch Finish

Complete a branch by merging it to the appropriate target(s) following the configured flow.

## Usage

```bash
/branch-finish                           # Finish current branch
/branch-finish feature/auth              # Finish specific branch
```

## Arguments

- **First argument** (optional): Branch name to finish
  - If omitted, finishes the current branch
  - Must be a valid flow branch (feature/, bugfix/, etc.)

## Workflow

When this command is invoked:

1. **Identify branch**: Determine which branch to finish (current or specified)

2. **Validate branch type**: Ensure it's a recognized flow branch

3. **Load configuration**: Get flow rules for this branch type

4. **Invoke managing-branches skill**: Get branching expertise

5. **Check preconditions**:
   - Working directory is clean
   - Branch is up to date
   - All tests pass (if CI integration)

6. **Determine targets**: Get merge target(s) from flow config
   - Single target: feature → develop
   - Multiple targets: hotfix → main AND develop

7. **Execute merges**: For each target branch:
   - Switch to target
   - Pull latest from origin
   - Merge the branch (with or without squash per config)
   - Push to origin

8. **Create tag** (if configured): For releases/hotfixes

9. **Clean up**:
   - Delete local branch
   - Delete remote branch
   - Remove worktree if exists

10. **Update tracking**:
    - Close linked issues (via commit message)
    - Update project board

## Examples

**Finish current feature branch**:
```bash
/branch-finish

# Merges to develop, deletes branch
```

**Finish specific branch**:
```bash
/branch-finish feature/issue-42-auth

# Merges to develop, deletes branch
```

**Finish hotfix** (multiple targets):
```bash
/branch-finish hotfix/security-patch

# Merges to main AND develop
# Creates tag v1.0.1
# Deletes branch
```

**Finish release**:
```bash
/branch-finish release/2.0.0

# Merges to main AND develop
# Creates tag v2.0.0
# Deletes branch
```

## Output Example

```
Finishing feature branch: feature/issue-42-auth
Target(s): develop

Checking working directory... clean
Updating develop from origin... done

Merging to develop...
✅ Merged to develop

Pushing develop to origin...
✅ Pushed

Deleting branch: feature/issue-42-auth
✅ Deleted local branch
✅ Deleted remote branch

✅ Branch feature/issue-42-auth completed!
```

## Flow-Specific Behavior

### Feature Branches
- Merge to `develop`
- No tag created
- Delete after merge

### Bugfix Branches
- Merge to `develop`
- No tag created
- Delete after merge

### Hotfix Branches
- Merge to `main` AND `develop`
- Create version tag (e.g., v1.0.1)
- Delete after merge

### Release Branches
- Merge to `main` AND `develop`
- Create version tag (e.g., v2.0.0)
- Delete after merge

## Merge Strategies

Configured per branch type:

- **No fast-forward** (`--no-ff`): Preserves branch history (default)
- **Squash merge**: Condenses commits into one
- **Rebase merge**: Linear history

## Version Tagging (Hotfix/Release)

For hotfix and release branches, version is determined by:

1. **Branch name**: If includes version (e.g., `release/2.0.0` or `hotfix/1.0.1`)
2. **Latest tag**: Increment appropriately (PATCH for hotfix, based on changes for release)
3. **User prompt**: Ask for version number if not determinable

Follows semantic versioning: `MAJOR.MINOR.PATCH`
- Hotfixes typically increment PATCH
- Releases use the version in the branch name

## Prerequisites

Before finishing a branch:

1. **Working directory must be clean**
   - Commit or stash all changes

2. **Branch should be pushed**
   - Remote tracking established

3. **Code should be reviewed**
   - PR approved (if required by policy)

## Error Handling

If working directory is dirty:
1. Show uncommitted changes
2. Suggest: commit, stash, or discard

If merge conflicts:
1. Stop and show conflicting files
2. Guide through conflict resolution
3. Offer to abort or continue

If branch not recognized:
1. Show error with branch name
2. List valid branch types
3. Suggest using different command

If target branch doesn't exist:
1. Offer to create it
2. Suggest alternative target

## Important Notes

- Always uses `--no-ff` by default to preserve history
- Hotfixes/releases merge to multiple branches
- Tags follow semantic versioning
- Remote branches are automatically cleaned up
- Linked issues close via `Closes #N` in merge commits

Use this to properly complete branches following your team's workflow!
