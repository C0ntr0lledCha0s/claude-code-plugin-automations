---
description: Complete a hotfix by merging to main and develop with version tag
allowed-tools: Bash, Read, Grep, Glob
argument-hint: "<name>"
---

# Hotfix Finish

Complete a hotfix by merging to both main and develop, creating a version tag.

## Usage

```bash
/hotfix-finish security-patch            # Finish hotfix/security-patch
/hotfix-finish critical-login-fix        # Finish hotfix/critical-login-fix
```

## Arguments

- **First argument** (required): Hotfix name
  - The name used when starting the hotfix
  - Branch must exist as `hotfix/<name>`

## Workflow

When this command is invoked:

1. **Identify hotfix branch**: Find `hotfix/<name>`

2. **Validate state**:
   - Branch exists
   - Working directory is clean
   - Branch has commits

3. **Invoke managing-branches skill**: Get branching expertise

4. **Determine version**: Extract or prompt for version number

5. **Merge to main**:
   - Switch to main
   - Pull latest
   - Merge hotfix with `--no-ff`
   - Push

6. **Create version tag**:
   - Tag the merge commit
   - Push tag to origin

7. **Merge to develop**:
   - Switch to develop
   - Merge hotfix
   - Push

8. **Clean up**:
   - Delete hotfix branch (local and remote)
   - Remove worktree if exists
   - Prune references

9. **Trigger release** (optional):
   - Create GitHub release
   - Deploy if CI/CD configured

## Example Output

```
Finishing hotfix: hotfix/security-patch

Checking working directory... clean

Merging to main...
  git checkout main
  git merge --no-ff hotfix/security-patch
  git push origin main
✅ Merged to main

Creating tag: v1.0.1
  git tag -a v1.0.1 -m "Hotfix 1.0.1"
  git push origin v1.0.1
✅ Created tag: v1.0.1

Merging to develop...
  git checkout develop
  git merge --no-ff hotfix/security-patch
  git push origin develop
✅ Merged to develop

Cleaning up...
  git branch -d hotfix/security-patch
  git push origin --delete hotfix/security-patch
  git worktree remove ../worktrees/hotfix
✅ Deleted branch and worktree

✅ Hotfix v1.0.1 completed!

Release published: https://github.com/user/repo/releases/tag/v1.0.1
```

## Version Determination

The version is determined by:

1. **Branch name**: If includes version (e.g., `hotfix/1.0.1`)
2. **Latest tag**: Increment patch version
3. **User prompt**: Ask for version number

Follows semantic versioning: `MAJOR.MINOR.PATCH`
- Hotfixes typically increment PATCH

## Error Handling

If branch doesn't exist:
1. Show error
2. List available hotfix branches

If merge conflicts:
1. Stop and show conflicts
2. Guide through resolution
3. Option to abort

If worktree has changes:
1. Warn about uncommitted work
2. Require commit or stash

## Important Notes

- Hotfixes MUST merge to both main and develop
- Tag is created on main after merge
- Worktree is automatically cleaned up
- Consider creating GitHub release for visibility

Use this to complete emergency fixes and get them into production!
