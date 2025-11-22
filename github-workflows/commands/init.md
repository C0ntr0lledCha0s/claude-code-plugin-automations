---
description: Initialize GitHub workflow environment with project context, issue sync, and environment variables for the current session
allowed-tools: Bash, Read, Grep, Glob
argument-hint: "[--force]"
---

# Initialize Workflow Environment

Set up the GitHub workflow environment for the current session. This command gathers project context, syncs issues, and creates environment variables for use by other commands.

## Usage

```bash
/init                    # Initialize (skip if already done today)
/init --force            # Force re-initialization
```

## Arguments

- **--force** (optional): Re-initialize even if already done today

## What This Does

1. **Detect Repository**: Get owner/repo from git remote
2. **Get User Info**: Current GitHub username
3. **Find Project Board**: Detect active project board for repository
4. **Get Current Milestone**: Find active milestone/sprint
5. **Sync Issues**: Fetch assigned issues to cache
6. **Create Environment**: Save context to `.claude/github-workflows/env.json`
7. **Show Summary**: Display workflow status

## Environment File

Creates `.claude/github-workflows/env.json`:

```json
{
  "initialized": "2025-01-15T10:30:00Z",
  "repository": {
    "owner": "owner",
    "name": "repo",
    "fullName": "owner/repo"
  },
  "user": {
    "login": "username",
    "name": "Full Name"
  },
  "projectBoard": {
    "number": 1,
    "title": "Sprint 5",
    "url": "https://github.com/orgs/owner/projects/1"
  },
  "milestone": {
    "title": "Sprint 5",
    "number": 3,
    "dueOn": "2025-01-31"
  },
  "branch": {
    "name": "feature/issue-42",
    "relatedIssue": 42
  },
  "issueCache": {
    "count": 5,
    "lastSync": "2025-01-15T10:30:00Z"
  }
}
```

## Workflow

When this command is invoked:

1. **Check existing environment**:
   - If `env.json` exists and was created today (and not --force), show current status
   - Otherwise, proceed with initialization

2. **Gather GitHub context**:
   ```bash
   # Repository info
   gh repo view --json owner,name,url

   # Current user
   gh api user --jq '.login,.name'

   # Project boards (find most recent active)
   gh project list --owner @me --format json

   # Current milestone
   gh api repos/{owner}/{repo}/milestones --jq '.[0]'
   ```

3. **Sync issues**:
   ```bash
   python {baseDir}/scripts/issue-tracker.py sync assigned
   ```

4. **Detect branch context**:
   - Get current branch name
   - Extract issue number if present
   - Match to cached issues

5. **Write environment file**:
   - Save all context to `.github-workflows/env.json`
   - This file is read by other commands

6. **Display summary**:
   ```
   ✅ GitHub Workflow Environment Initialized

   Repository: owner/repo
   User: username
   Project Board: Sprint 5 (#1)
   Current Milestone: Sprint 5 (due Jan 31)
   Current Branch: feature/issue-42 → Issue #42

   Tracked Issues: 5 assigned to you
     #42: Implement user authentication [High Priority]
     #56: Fix login validation [High Priority]
     #78: Add password reset [Normal]

   💡 Tips:
   - Use /commit-smart to commit with auto issue refs
   - Use /workflow-status to see full workflow state
   - Use /issue-track to refresh issue cache
   ```

## Integration with Other Commands

The environment file is used by:

- **commit-smart**: Reads project context for better issue detection
- **workflow-status**: Shows project board and milestone info
- **issue-track**: Uses repository info for GitHub API calls
- **pr-review-request**: Knows which project to update

## Auto-Initialization

A UserPromptSubmit hook checks if the environment is initialized:
- If not initialized or stale (> 24 hours), suggests running `/init`
- This ensures fresh context for each working session

## Example Session Start

```bash
# Start of day workflow
/init

# Output:
✅ GitHub Workflow Environment Initialized

Repository: acme/webapp
User: developer
Project Board: Q1 Sprint 3 (#5)
Current Milestone: v2.1.0 (due Feb 15)
Current Branch: main

Tracked Issues: 8 assigned to you
  HIGH PRIORITY:
    #142: Security vulnerability in auth
    #156: Performance regression in API

  NORMAL:
    #167: Add dark mode support
    #189: Update documentation

💡 Run /workflow-status for detailed view
```

## Environment Variables Available

After initialization, these are available in `env.json`:

| Variable | Description | Example |
|----------|-------------|---------|
| `repository.fullName` | Full repo identifier | `owner/repo` |
| `user.login` | GitHub username | `developer` |
| `projectBoard.number` | Active project ID | `5` |
| `milestone.title` | Current milestone | `Sprint 5` |
| `branch.relatedIssue` | Issue for current branch | `42` |

## Error Handling

If GitHub CLI is not authenticated:
1. Display error: "GitHub CLI not authenticated"
2. Suggest: `gh auth login`

If no project board found:
1. Display warning: "No project board detected"
2. Continue with other initialization

If no milestone found:
1. Display info: "No active milestone"
2. Continue normally

## Important Notes

- Run at the start of each working session
- Environment persists in `.claude/github-workflows/env.json`
- The `.claude/` directory is already typically gitignored
- Re-run with `--force` if you switch projects or branches
