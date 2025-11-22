---
description: Sync and display active GitHub issues as trackable tasks with local caching for commit integration
allowed-tools: Bash, Read, Grep, Glob
argument-hint: "[filter: assigned|labeled|milestone|all] [value]"
---

# Issue Track

Synchronize GitHub issues to a local cache and display them as trackable tasks. This enables automatic issue references in commits.

## Usage

```bash
/issue-track                    # Show cached issues (or sync if empty)
/issue-track sync               # Force sync from GitHub
/issue-track assigned           # Sync issues assigned to you
/issue-track labeled priority:high  # Sync issues with specific label
/issue-track milestone "Sprint 5"   # Sync issues in milestone
/issue-track all                # Sync all open issues
/issue-track clear              # Clear the local cache
```

## Arguments

- **First argument** (optional): Filter type or action
  - `sync`: Force resync from GitHub
  - `assigned`: Issues assigned to current user
  - `labeled`: Issues with specific label (requires second arg)
  - `milestone`: Issues in specific milestone (requires second arg)
  - `all`: All open issues in repository
  - `clear`: Clear the local cache
  - (empty): Show cached issues

- **Second argument** (optional): Filter value for `labeled` or `milestone`

**Input validation**: Only accepts predefined filters. Invalid inputs are rejected.

## What This Does

1. **Sync Issues**: Fetches issues from GitHub based on filter
2. **Cache Locally**: Stores in `.claude/github-workflows/active-issues.json`
3. **Display as Tasks**: Shows issues with status, priority, and progress
4. **Enable Commit Integration**: Makes issues available for auto-referencing

## Cache File Location

Issues are cached in `.claude/github-workflows/active-issues.json`:

```json
{
  "lastSync": "2025-01-15T10:30:00Z",
  "repository": "owner/repo",
  "filter": "assigned",
  "issues": [
    {
      "number": 42,
      "title": "Implement user authentication",
      "state": "open",
      "labels": ["feature", "priority:high"],
      "assignees": ["username"],
      "milestone": "Sprint 5",
      "created_at": "2025-01-10T08:00:00Z",
      "updated_at": "2025-01-14T15:30:00Z",
      "url": "https://github.com/owner/repo/issues/42",
      "body_preview": "First 200 characters of issue body..."
    }
  ]
}
```

## Workflow

When this command is invoked:

1. **Validate arguments** (CRITICAL - prevents command injection):
   - Only accept predefined filters from allowlist
   - Reject invalid input immediately
   - DO NOT pass user input directly to shell

2. **Check cache status**:
   - If no argument and cache exists: display cached issues
   - If no argument and no cache: run default sync (assigned)
   - If `sync` or filter: fetch fresh data from GitHub

3. **Fetch from GitHub** (if syncing):
   ```bash
   # Assigned to user
   gh issue list --assignee @me --state open --json number,title,state,labels,assignees,milestone,createdAt,updatedAt,url,body

   # With label
   gh issue list --label "priority:high" --state open --json ...

   # In milestone
   gh issue list --milestone "Sprint 5" --state open --json ...

   # All open
   gh issue list --state open --json ...
   ```

4. **Process and cache**:
   - Parse JSON response
   - Extract relevant fields
   - Truncate body to preview
   - Write to `.github-workflows/active-issues.json`

5. **Display as task list**:
   ```
   📋 Active Issues (synced 5 minutes ago)
   Repository: owner/repo
   Filter: assigned to @me

   HIGH PRIORITY:
   ┌─ #42 Implement user authentication
   │  Labels: feature, priority:high, scope:backend
   │  Milestone: Sprint 5
   │  Status: In Progress (branch: feature/auth)
   └─ Use: Closes #42 or Refs #42

   ┌─ #56 Fix login validation error
   │  Labels: bug, priority:high
   │  Status: Open
   └─ Use: Closes #56 or Refs #56

   NORMAL PRIORITY:
   ┌─ #78 Add password reset feature
   │  Labels: feature
   │  Milestone: Sprint 6
   └─ Use: Closes #78 or Refs #78

   💡 Tip: Use /commit-smart to auto-suggest these in commits
   ```

## Integration with Commits

The cached issues enable automatic commit integration:

1. **Branch name detection**: `feature/issue-42` → suggests #42
2. **Keyword matching**: Changed files match issue keywords
3. **Automatic suggestions**: `/commit-smart` reads cache and suggests references

### Commit Footer Options

- `Closes #N`: Closes issue when PR merges
- `Fixes #N`: Same as Closes (for bugs)
- `Refs #N`: References without closing
- `Progresses #N`: Indicates partial progress

## Examples

**Show cached issues**:
```bash
/issue-track
```

**Sync assigned issues**:
```bash
/issue-track assigned
```

**Sync high-priority issues**:
```bash
/issue-track labeled priority:high
```

**Sync current sprint**:
```bash
/issue-track milestone "Sprint 5"
```

**Force resync**:
```bash
/issue-track sync
```

## Branch-Issue Detection

The command also detects if current branch relates to an issue:

```bash
# On branch feature/issue-42 or feature/42-auth
Current branch appears related to issue #42
```

This information is used by `/commit-smart` to prioritize that issue.

## Error Handling

If the filter is invalid:
1. Display error: "Invalid filter: '{value}'. Must be one of: sync, assigned, labeled, milestone, all, clear"
2. Show usage example
3. Stop execution

If GitHub CLI fails:
1. Display the error message
2. Check if `gh` is installed and authenticated
3. Suggest: `gh auth login`

If no issues found:
1. Display: "No issues found matching filter"
2. Suggest alternative filters

## Important Notes

- Cache is stored per-project in `.claude/github-workflows/`
- Cache expires after 1 hour (shows warning)
- `/commit-smart` automatically reads the cache
- `/workflow-status` displays cached issues in summary
- The `.claude/` directory is already typically gitignored

## Security

- All arguments are validated against allowlists
- Label/milestone values are shell-escaped before use
- No user input passed directly to commands
