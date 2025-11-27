---
description: Create a release branch for preparing a new version release
allowed-tools: Bash, Read, Grep, Glob
argument-hint: "<version>"
---

# Release Branch

Create a release branch from develop for version preparation.

## Usage

```bash
/release-branch 2.0.0                    # Create release/2.0.0
/release-branch 1.5.0                    # Create release/1.5.0
```

## Arguments

- **First argument** (required): Version number
  - Semantic version format: MAJOR.MINOR.PATCH
  - Creates branch as `release/<version>`

**Input validation**: Version must follow semantic versioning (e.g., 1.0.0, 2.1.0).

## Workflow

When this command is invoked:

1. **Validate version**: Check semantic version format

2. **Check for conflicts**:
   - No existing release branch
   - Version not already tagged

3. **Invoke managing-branches skill**: Get branching expertise

4. **Create release branch**:
   - Switch to develop
   - Pull latest from origin
   - Create release branch

5. **Initialize release**:
   - Bump version in package files
   - Initialize changelog section

6. **Create worktree** (if configured):
   - Isolate release prep
   - Continue feature development

7. **Show release checklist**:
   - Version updates
   - Changelog
   - Documentation
   - Testing

## Example Output

```
Creating release branch for v2.0.0...

Checking prerequisites...
  ✅ No existing release branch
  ✅ Version not yet tagged

Creating release branch:
  git checkout develop
  git pull origin develop
  git checkout -b release/2.0.0
✅ Branch: release/2.0.0

Creating worktree:
  git worktree add ../worktrees/release-2.0.0 release/2.0.0
✅ Worktree: ../worktrees/release-2.0.0

Release preparation checklist:
☐ Bump version in package.json
☐ Update CHANGELOG.md
☐ Update documentation
☐ Final testing
☐ Fix any last-minute bugs

When ready: /release-finish 2.0.0 or /branch-finish release/2.0.0
```

## Release Preparation Tasks

On the release branch, you should:

1. **Bump versions**: Update version in all package files
2. **Update changelog**: Document all changes since last release
3. **Update docs**: Ensure documentation matches release
4. **Final fixes**: Bug fixes only, no new features
5. **Test**: Full regression testing

## Version Bumping

The command can help bump versions:

```bash
# package.json
"version": "2.0.0"

# Other common files:
# - VERSION
# - setup.py
# - Cargo.toml
```

## Finishing the Release

When ready to ship:

```bash
/branch-finish release/2.0.0
```

This will:
- Merge to main AND develop
- Create tag v2.0.0
- Delete release branch
- Optionally publish release

## Multiple Release Branches

While not recommended, gitflow supports parallel releases:

```bash
/release-branch 2.0.0    # New major version
/release-branch 1.5.1    # Patch for older version (use support branch)
```

## Strategy Considerations

### Gitflow
- Release branches from develop
- Allow only bug fixes
- Merge to main and develop

### GitHub Flow
- No release branches
- Use tags on main instead
- Deploy continuously

### GitLab Flow
- Release branches optional
- Use environment branches
- Promote through environments

## Error Handling

If version already exists:
1. Show existing tag
2. Suggest incrementing version

If release branch exists:
1. Show existing branch
2. Suggest finishing or deleting it

If not on develop:
1. Offer to switch
2. Warn about potential issues

## Important Notes

- Only bug fixes allowed on release branches
- No new features after release branch cut
- Merge to BOTH main and develop when done
- Tag follows the version number

Use this when you're ready to freeze features and prepare for release!
