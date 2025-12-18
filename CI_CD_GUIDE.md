# CI/CD Guide

This guide explains the Continuous Integration and Continuous Deployment (CI/CD) pipelines for the Claude Code Plugins repository.

## Overview

Our CI/CD pipeline consists of:

1. **Validation Pipeline** - Validates plugin structure and commit messages
2. **Release Pipeline** - Manages versioning and changelog generation
3. **Automated Changelog** - Updates CHANGELOG.md on commits to main

## Workflows

### 1. Validation Workflow (`.github/workflows/validate.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Manual trigger via workflow dispatch

**Jobs:**

#### validate
Validates all plugin components:
- Runs `validate-plugins.sh` to check all agents, skills, commands, and hooks
- Validates `marketplace.json` structure
- Ensures all JSON files are valid

**Exit codes:**
- `0` - All validations passed
- `1` - Validation errors found (blocks merge)

#### lint-commits (PR only)
Validates commit messages follow conventional commit format:
- Uses `@commitlint/config-conventional`
- Checks all commits in the PR
- Enforces commit message standards

**Commit Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Valid types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style changes
- `refactor` - Code refactoring
- `perf` - Performance improvements
- `test` - Test changes
- `build` - Build system changes
- `ci` - CI/CD changes
- `chore` - Other changes
- `revert` - Revert a commit

**Valid scopes:**
- `claude-component-builder`
- `self-improvement`
- `github-workflows`
- `agents`
- `skills`
- `commands`
- `hooks`
- `marketplace`
- `ci`
- `docs`
- `deps`

### 2. Release Workflow (`.github/workflows/release.yml`)

**Triggers:**
- Manual trigger via workflow dispatch with inputs:
  - `release-type`: major | minor | patch
  - `prerelease`: boolean (optional)

**Jobs:**

#### release
Creates a new release:
1. Validates all plugins
2. Bumps version in `package.json` and `marketplace.json`
3. Generates/updates CHANGELOG.md
4. Creates git tag
5. Pushes changes and tags
6. Creates GitHub release

**Version Bumping:**
- `major` - Breaking changes (1.0.0 → 2.0.0)
- `minor` - New features (1.0.0 → 1.1.0)
- `patch` - Bug fixes (1.0.0 → 1.0.1)
- `prerelease` - Pre-release versions (1.0.0 → 1.0.1-0)

#### update-changelog
Automatically updates CHANGELOG.md on main branch commits:
1. Generates changelog from conventional commits
2. Commits changes with `[skip ci]` to avoid loops
3. Only runs if changes detected

## Local Development

### Installing Dependencies

```bash
npm install
```

### Running Validation Locally

Quick validation:
```bash
npm run validate:quick
# or
bash validate-all.sh
```

Comprehensive validation:
```bash
npm run validate
# or
bash validate-plugins.sh
```

### Generating Changelog

Update CHANGELOG.md with recent commits:
```bash
npm run changelog
```

### Version Management

Bump version and update changelog:
```bash
# Patch version (1.0.0 → 1.0.1)
npm run version:patch

# Minor version (1.0.0 → 1.1.0)
npm run version:minor

# Major version (1.0.0 → 2.0.0)
npm run version:major

# Prerelease
npm run version:prerelease
```

This will:
1. Bump version in `package.json` and `marketplace.json`
2. Update CHANGELOG.md
3. Create a git tag
4. Commit the changes

**Push the release:**
```bash
git push --follow-tags origin main
```

### Commit Message Validation

Validate your commit messages locally:
```bash
# Install commitlint globally (optional)
npm install -g @commitlint/cli @commitlint/config-conventional

# Validate last commit
echo "feat(skills): add new skill" | npx commitlint

# Validate commit message from file
npx commitlint --from HEAD~1
```

## Commit Message Guidelines

### Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Examples

Good commit messages:
```
feat(skills): add building-agents skill with validation
fix(commands): correct argument parsing in new-agent command
docs(readme): update installation instructions
ci(workflows): add automated changelog generation
```

Bad commit messages:
```
update stuff
Fixed bug
WIP
asdf
```

### Rules

1. **Header:**
   - Max 100 characters
   - Lowercase subject
   - No period at the end
   - Imperative mood ("add" not "added")

2. **Body:**
   - Optional
   - Explain what and why, not how
   - Wrap at 100 characters

3. **Footer:**
   - Optional
   - Reference issues: `Closes #123`
   - Note breaking changes: `BREAKING CHANGE: description`

## Release Process

### Creating a Release

1. **Ensure all changes are committed and validated:**
   ```bash
   npm run validate
   ```

2. **Create release via GitHub Actions:**
   - Go to Actions → Release Management
   - Click "Run workflow"
   - Select release type (major/minor/patch)
   - Optionally mark as prerelease
   - Click "Run workflow"

3. **The workflow will:**
   - Validate all plugins
   - Bump version
   - Update changelog
   - Create git tag
   - Push to repository
   - Create GitHub release

### Manual Release (Alternative)

If you prefer to create releases manually:

1. **Bump version and update changelog:**
   ```bash
   npm run version:patch  # or minor/major
   ```

2. **Push changes:**
   ```bash
   git push --follow-tags origin main
   ```

3. **Create GitHub release manually:**
   - Go to Releases → New Release
   - Select the tag created
   - Copy relevant CHANGELOG.md content
   - Publish release

## Troubleshooting

### Validation Failures

**Plugin validation fails:**
1. Run `bash validate-plugins.sh` locally
2. Check error messages for specific issues
3. Fix validation errors in affected files
4. Re-run validation

**Commit message validation fails:**
1. Check commit message format
2. Ensure type and scope are valid
3. Verify header length < 100 chars
4. Use `git commit --amend` to fix

### Release Issues

**Version bump fails:**
1. Ensure working directory is clean
2. Verify you're on the main branch
3. Check that package.json is valid JSON
4. Run `npm run validate` first

**Changelog not updating:**
1. Ensure commits follow conventional format
2. Check that commits are not hidden types (style, chore, test)
3. Verify git history is accessible

### Permission Issues

**GitHub Actions can't push:**
1. Ensure repository has Actions write permissions
2. Check branch protection rules
3. Verify GITHUB_TOKEN has correct scopes

## Configuration Files

- `.commitlintrc.json` - Commit message linting rules
- `.versionrc.json` - Standard-version configuration
- `git-conventional-commits.json` - Conventional commits config
- `.npmrc` - npm configuration
- `scripts/marketplace-version-updater.js` - Custom version updater

## Best Practices

1. **Always validate before committing:**
   ```bash
   npm run validate
   ```

2. **Write meaningful commit messages:**
   - Follow conventional commits
   - Be descriptive but concise
   - Reference issues when applicable

3. **Test locally before pushing:**
   - Run validation scripts
   - Test changed components
   - Verify plugin.json updates

4. **Use semantic versioning:**
   - Patch for bug fixes
   - Minor for new features
   - Major for breaking changes

5. **Keep changelog up to date:**
   - Let automation handle it
   - Review before releases
   - Edit manually if needed

## Continuous Improvement

The CI/CD pipeline is designed to:
- Catch errors early
- Maintain code quality
- Automate repetitive tasks
- Ensure consistency
- Document changes

If you encounter issues or have suggestions, please open an issue or submit a pull request.
