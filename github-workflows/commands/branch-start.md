---
description: Start a new branch following the configured branching strategy flow
allowed-tools: Bash, Read, Grep, Glob
argument-hint: "<type> <name> [--issue N]"
---

# Branch Start

Create a new branch following the configured branching strategy (gitflow, github-flow, etc.).

## Usage

```bash
/branch-start feature auth               # Create feature/auth from develop
/branch-start bugfix validation-error    # Create bugfix/validation-error
/branch-start feature user-dashboard --issue 42  # With issue link
```

## Arguments

- **First argument** (required): Branch type
  - `feature`: New feature development
  - `bugfix`: Bug fix (non-urgent)
  - `hotfix`: Emergency production fix
  - `release`: Release preparation
  - `docs`: Documentation changes
  - `refactor`: Code refactoring

- **Second argument** (required): Branch name/description
  - Will be formatted according to naming conventions
  - Spaces converted to hyphens
  - Made lowercase

- **--issue N** (optional): Related issue number
  - Creates branch as `feature/issue-42-name`
  - Automatically links to the issue

**Input validation**: Branch type must match configured flow types. Name must follow naming conventions (lowercase, hyphens, max 64 chars).

## Workflow

When this command is invoked:

1. **Validate arguments**:
   - Check branch type is valid for configured strategy
   - Validate name follows conventions
   - Check issue exists if provided

2. **Load configuration**: Read branching-config.json for flow settings

3. **Invoke managing-branches skill**: Get branching expertise

4. **Determine base branch**:
   - Gitflow: features from develop, hotfixes from main
   - GitHub Flow: all branches from main
   - Per configured flows

5. **Generate branch name**:
   - Apply prefix based on type
   - Include issue reference if provided
   - Enforce naming conventions

6. **Create the branch**:
   - Switch to base branch
   - Pull latest from origin
   - Create new branch
   - Optionally push to origin

7. **Link to issue** (if provided):
   - Add branch label to issue
   - Update issue tracking

8. **Show next steps**:
   - Recommended commit format
   - Issue references to use
   - How to finish the branch

## Examples

**Simple feature branch**:
```bash
/branch-start feature user-authentication

# Creates: feature/user-authentication from develop
```

**With issue link**:
```bash
/branch-start feature auth --issue 42

# Creates: feature/issue-42-auth from develop
# Links to issue #42
```

**Hotfix branch**:
```bash
/branch-start hotfix security-patch

# Creates: hotfix/security-patch from main
# May create worktree automatically
```

**Release branch**:
```bash
/branch-start release 2.0.0

# Creates: release/2.0.0 from develop
```

## Strategy-Specific Behavior

### Gitflow
- Features branch from `develop`
- Hotfixes branch from `main`
- Releases branch from `develop`

### GitHub Flow
- All branches from `main`
- No release branches (continuous deployment)

### Trunk-Based
- Short-lived branches from `main`
- Warning if branch open > 2 days

## Type-Specific Guidance

### Hotfix Branches

**When to use hotfix type:**
- Security vulnerabilities
- Critical production bugs
- Data corruption issues
- Service outages

**Do NOT use hotfix for:**
- Normal bug fixes (use `bugfix` type instead)
- New features
- Non-urgent improvements

**Best practices:**
1. Keep it minimal - fix only the critical issue
2. Test thoroughly even in emergencies
3. Document the fix with clear commit messages
4. Notify team about the emergency

**Workflow notes:**
- Hotfixes branch from `main`, not `develop`
- May create worktree automatically for isolation
- Merges to both `main` AND `develop` when finished
- Creates a version tag automatically

### Release Branches

**When to use release type:**
- Feature freeze for new version
- Preparing for production deployment
- Version bump and changelog updates

**Release preparation checklist:**
- [ ] Bump version in package files
- [ ] Update CHANGELOG.md
- [ ] Update documentation
- [ ] Final testing
- [ ] Fix any last-minute bugs (no new features!)

**Workflow notes:**
- Release branches from `develop`
- Only bug fixes allowed after branch creation
- Merges to both `main` AND `develop` when finished
- Creates tag matching the version number

## Output Example

```
Starting feature branch: feature/issue-42-auth
Base branch: develop

Switching to develop...
Updating develop from origin...
Creating branch: feature/issue-42-auth

✅ Branch created: feature/issue-42-auth
✅ Based on: develop (up to date)
✅ Linked to: #42

Next steps:
1. Make your changes
2. Commit with: feat(auth): description
3. Reference issue: Refs #42
4. When done: /branch-finish
```

## Error Handling

If arguments are invalid:
1. Display specific error (unknown type, invalid name)
2. Show available branch types
3. Show naming convention requirements

If base branch doesn't exist:
1. Offer to create it
2. Suggest alternative base

If network errors:
1. Create branch locally
2. Warn about not being up to date

## Important Notes

- Branch names are automatically formatted (lowercase, hyphens)
- Issue links update GitHub automatically
- Worktrees may be auto-created for hotfixes
- Configuration determines all flow behavior

Use this to start branches that follow your team's conventions!
