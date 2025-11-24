---
description: Prepare a release by analyzing commits, determining version, and generating changelog
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
argument-hint: "[version-type: major|minor|patch|auto]"
---

# Prepare Release

Analyzes commits since the last release and prepares all release artifacts.

## Usage

```bash
/release-prepare auto       # Auto-detect version from commits
/release-prepare minor      # Force minor version bump
/release-prepare major      # Force major version bump
/release-prepare patch      # Force patch version bump
```

## What This Does

1. **Analyze Commits**: Get all commits since last release tag
2. **Determine Version**: Calculate version bump based on commit types
3. **Generate Changelog**: Create changelog entries grouped by type
4. **Create Release Notes**: Generate comprehensive release notes
5. **Prepare Files**: Show what version files need updating

## Workflow

### Step 1: Get Last Release

Find the most recent release tag and analyze commits since then:

```bash
# Get last release tag
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
echo "Last release: ${LAST_TAG:-'No previous release'}"

# Count commits since last release
if [ -n "$LAST_TAG" ]; then
  COMMIT_COUNT=$(git rev-list --count $LAST_TAG..HEAD)
else
  COMMIT_COUNT=$(git rev-list --count HEAD)
fi
echo "Commits since last release: $COMMIT_COUNT"
```

### Step 2: Analyze Commit Types

Parse commits using conventional commit format:

```bash
# Get commits since last tag
if [ -n "$LAST_TAG" ]; then
  COMMITS=$(git log $LAST_TAG..HEAD --pretty=format:"%s")
else
  COMMITS=$(git log --pretty=format:"%s")
fi

# Count by type
FEAT_COUNT=$(echo "$COMMITS" | grep -c "^feat" || echo "0")
FIX_COUNT=$(echo "$COMMITS" | grep -c "^fix" || echo "0")
BREAKING_COUNT=$(echo "$COMMITS" | grep -c "!" || echo "0")
BREAKING_FOOTER=$(echo "$COMMITS" | grep -c "BREAKING CHANGE" || echo "0")

echo "Features: $FEAT_COUNT"
echo "Fixes: $FIX_COUNT"
echo "Breaking changes: $((BREAKING_COUNT + BREAKING_FOOTER))"
```

### Step 3: Determine Version Bump

Based on argument or auto-detection:

**Auto-detection logic**:
- Any breaking changes (`!` or `BREAKING CHANGE`) → MAJOR
- Any features (`feat:`) → MINOR
- Only fixes/docs/chores → PATCH

### Step 4: Generate Changelog

Group commits by type for the changelog:

```markdown
## [VERSION] - DATE

### ⚠️ Breaking Changes
- Breaking change commits

### ✨ Features
- feat: commits

### 🐛 Bug Fixes
- fix: commits

### 📚 Documentation
- docs: commits

### 🔧 Maintenance
- chore:, refactor:, ci: commits
```

### Step 5: Create Release Notes

Generate user-friendly release notes:

```markdown
# Release vVERSION

## Highlights

Summary of the key changes in this release.

## ⚠️ Breaking Changes

Details on breaking changes with migration instructions.

## ✨ New Features

Description of new features.

## 🐛 Bug Fixes

List of bug fixes.

## 📦 Upgrade

Instructions for upgrading.
```

### Step 6: Show Files to Update

Identify version files that need updating:

- `package.json` (if exists)
- `.claude-plugin/plugin.json` (if exists)
- `CHANGELOG.md`
- Any other version constants

## Arguments

- **version-type** (optional):
  - `auto` (default): Auto-detect from commits
  - `major`: Force major version bump
  - `minor`: Force minor version bump
  - `patch`: Force patch version bump

## Output

The command outputs:
1. Commit analysis summary
2. Determined version number
3. Generated changelog section
4. Draft release notes
5. List of files to update

## Example Output

```markdown
## Release Preparation: v1.6.0

### Commit Analysis

Analyzed 15 commits since v1.5.0:
- 2 features (feat:)
- 5 fixes (fix:)
- 3 documentation (docs:)
- 5 maintenance (chore:, refactor:)

**Version Bump**: MINOR (1.5.0 → 1.6.0)
Reason: New features added, no breaking changes

### Changelog Entry

## [1.6.0] - 2025-01-15

### ✨ Features
- Add issue tracking command (#42)
- Add release preparation workflow (#45)

### 🐛 Bug Fixes
- Fix validation error in hooks (#55)
- Fix duplicate detection (#58)
...

### Files to Update

- [ ] .claude-plugin/plugin.json: 1.5.0 → 1.6.0
- [ ] CHANGELOG.md: Add new section

Ready to proceed?
```

## Integration

This command works with:
- **release-manager agent**: Full release workflow
- **managing-commits skill**: Commit analysis
- **milestone-close command**: Close release milestone

## Notes

- Uses conventional commits format for parsing
- Follows semantic versioning (SemVer)
- Generates Keep a Changelog format
- Does NOT automatically update files (presents plan first)
