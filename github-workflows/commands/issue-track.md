---
description: Sync and display active GitHub issues as trackable tasks with local caching for commit integration
allowed-tools: Bash, Read, Grep, Glob
argument-hint: "[filter: assigned|labeled|milestone|project|all] [value]"
---

# Issue Track

Synchronize GitHub issues to a local cache and display them as trackable tasks. This enables automatic issue references in commits.

## Usage

```bash
/issue-track                    # Show cached issues (uses cache if fresh, syncs if stale/empty)
/issue-track sync               # Force sync from GitHub, bypassing cache
/issue-track assigned           # Sync issues assigned to you
/issue-track labeled priority:high  # Sync issues with specific label
/issue-track milestone "Sprint 5"   # Sync issues in milestone
/issue-track project "Agent Plugin Development"  # Sync issues in project board (by title)
/issue-track project 3          # Sync issues in project board (by number)
/issue-track all                # Sync all open issues
/issue-track context            # Show issues filtered by context (project + scope + assignment)
/issue-track scope              # Show issues matching branch scope
/issue-track branch             # Show only issues selected for current branch
/issue-track select 42 43       # Select issues for current branch
/issue-track clear              # Clear the local cache
```

## Arguments

- **First argument** (optional): Filter type or action
  - `sync`: Force sync from GitHub, bypassing cache
  - `assigned`: Issues assigned to current user
  - `labeled`: Issues with specific label (requires second arg)
  - `milestone`: Issues in specific milestone (requires second arg)
  - `project`: Issues in specific project board (requires second arg: title or number)
  - `all`: All open issues in repository
  - `context`: Show issues filtered by combined context (project + scope + assignment)
  - `scope`: Show issues matching the branch's detected scope label
  - `branch`: Show only issues selected for the current branch
  - `select`: Select issues for current branch (requires issue numbers as additional args)
  - `clear`: Clear the local cache
  - (empty): Show cached issues if fresh (< 15 min old), otherwise sync using default filter

- **Second argument** (optional): Filter value for `labeled`, `milestone`, `project`, or `select`
  - For `project`: Can be project title (string) or project number (integer)
  - For `select`: One or more issue numbers (e.g., `select 42 43 44`)

**Input validation**: Only accepts predefined filters. Invalid inputs are rejected.

**Cache behavior**: Cache is considered "fresh" if synced within the last 15 minutes. Fresh cache is displayed without re-fetching from GitHub. Use `sync` to bypass this.

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
      "body_preview": "First 500 characters of issue body for context..."
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
   - If `sync` argument: skip cache and fetch fresh data
   - If no argument and cache exists:
     - Check cache age: `lastSync` timestamp from `active-issues.json`
     - If cache is fresh (< 15 minutes old): display cached issues without fetching
     - If cache is stale (>= 15 minutes old): run default sync using preference
   - If no argument and no cache: run default sync using preference from `env.json`
   - Read default filter: `jq -r '.preferences.defaultIssueFilter // "assigned"' .claude/github-workflows/env.json`
   - Falls back to `assigned` if no preference is set (backward compatible)
   - If specific filter (`assigned`, `all`, etc.): fetch fresh data from GitHub

   ```bash
   # Check cache freshness (15 minute threshold)
   CACHE_FILE=".claude/github-workflows/active-issues.json"
   if [[ -f "$CACHE_FILE" ]]; then
     LAST_SYNC=$(jq -r '.lastSync' "$CACHE_FILE")
     LAST_SYNC_EPOCH=$(date -d "$LAST_SYNC" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%SZ" "$LAST_SYNC" +%s)
     NOW_EPOCH=$(date +%s)
     AGE_MINUTES=$(( (NOW_EPOCH - LAST_SYNC_EPOCH) / 60 ))

     if [[ $AGE_MINUTES -lt 15 ]]; then
       echo "Using cached issues (synced $AGE_MINUTES minutes ago)"
       # Display cached issues
     else
       echo "Cache is stale ($AGE_MINUTES minutes old), syncing..."
       # Fetch fresh data
     fi
   fi
   ```

3. **Fetch from GitHub** (if syncing):
   ```bash
   # Assigned to user
   gh issue list --assignee @me --state open --json number,title,state,labels,assignees,milestone,createdAt,updatedAt,url,body

   # With label
   gh issue list --label "priority:high" --state open --json ...

   # In milestone
   gh issue list --milestone "Sprint 5" --state open --json ...

   # In project board (requires GraphQL)
   # First get project ID, then query items
   gh api graphql -f query='
     query($owner: String!, $number: Int!) {
       user(login: $owner) {
         projectV2(number: $number) {
           items(first: 100) {
             nodes {
               content {
                 ... on Issue {
                   number
                   title
                   state
                   labels(first: 10) { nodes { name } }
                   assignees(first: 5) { nodes { login } }
                   milestone { title }
                   createdAt
                   updatedAt
                   url
                   body
                 }
               }
             }
           }
         }
       }
     }' -f owner="$OWNER" -F number="$PROJECT_NUMBER"

   # All open
   gh issue list --state open --json ...
   ```

4. **Process and cache**:
   - Parse JSON response
   - Extract relevant fields
   - Truncate body to 500 character preview
   - Write to `.claude/github-workflows/active-issues.json`

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

**Sync issues from project board** (by title):
```bash
/issue-track project "Agent Plugin Development"
```

**Sync issues from project board** (by number):
```bash
/issue-track project 3
```

**Show context-filtered issues** (project + scope + assignment):
```bash
/issue-track context
```

**Show issues matching branch scope**:
```bash
/issue-track scope
```

**Show only branch-selected issues**:
```bash
/issue-track branch
```

**Select issues for current branch**:
```bash
/issue-track select 42 43 44
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
1. Display error: "Invalid filter: '{value}'. Must be one of: sync, assigned, labeled, milestone, project, all, context, scope, branch, select, clear"
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
- **Cache freshness**: 15 minutes - fresh cache is used without re-fetching
- **Cache expiry warning**: After 1 hour, shows a warning that cache may be stale
- Use `sync` to bypass cache and fetch fresh data
- `/commit-smart` automatically reads the cache
- `/workflow-status` displays cached issues in summary
- The `.claude/` directory is already typically gitignored
- Default filter is configurable via `/github-workflows:init`:
  - **Personal projects**: defaults to `all` (fetch all open issues)
  - **Team projects**: defaults to `assigned` (fetch only your issues)
  - Preference stored in `.claude/github-workflows/env.json`

## Security

- All arguments are validated against allowlists
- Label/milestone values are shell-escaped before use
- No user input passed directly to commands
