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
3. **Find Project Board**: Auto-detect most recent active project board
4. **Get Current Milestone**: Find active milestone/sprint
5. **Analyze Project Scopes**: Suggest scope labels based on project structure
6. **Label Stocktake**: Check and report missing standard labels
7. **Detect Branch**: Get current branch and detect related issues and scope
8. **Sync Issues**: Fetch issues (defaults to all issues)
9. **Set Preferences**: Configure defaults (project type, issue filter, default project)
10. **Create Setup Status**: Track which setup steps are complete
11. **Save Environment**: Save context to `.claude/github-workflows/env.json`
12. **Show Summary**: Display workflow status, label stocktake, and setup recommendations

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
    "relatedIssues": [42],
    "detectedScope": "auth",
    "scopeLabel": "scope:auth"
  },
  "issueCache": {
    "count": 5,
    "lastSync": "2025-01-15T10:30:00Z"
  },
  "labels": {
    "existing": 15,
    "missing": ["priority:high", "priority:medium"],
    "recommended": ["bug", "feature", "enhancement"],
    "suggestedScopes": ["agent-builder", "self-improvement", "github-workflows"]
  },
  "setup": {
    "labelsComplete": false,
    "projectBoardExists": true,
    "milestonesExist": true
  },
  "preferences": {
    "projectType": "personal",
    "defaultIssueFilter": "all",
    "defaultProject": null
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

3. **Find project board** (automated):
   - Query user's project boards: `gh project list --owner @me --format json`
   - Auto-select the most recent (first) project board
   - If no user projects, try organization projects
   - Store in `projectBoard` section of `env.json`
   - Store project number in `preferences.defaultProject`

4. **Set preferences** (automated defaults):
   - **projectType**: Set to `"personal"` (single contributor default)
   - **defaultIssueFilter**: Set to `"all"` (fetch all open issues)
   - **defaultProject**: Set to detected project board number (or null)

   These defaults can be manually adjusted in `env.json` if needed:
   - For team projects: Set `projectType` to `"team"` and `defaultIssueFilter` to `"assigned"`

5. **Label stocktake**:
   ```bash
   # Get existing labels
   gh label list --json name,color,description

   # Compare with standard labels (from label-presets.json)
   STANDARD_LABELS=(
     # Type labels (no prefix)
     "bug"
     "feature"
     "enhancement"
     "docs"
     "refactor"
     "test"
     # Priority labels
     "priority:critical"
     "priority:high"
     "priority:medium"
     "priority:low"
     # Scope labels
     "scope:frontend"
     "scope:backend"
     "scope:docs"
   )

   # Identify missing labels
   for label in "${STANDARD_LABELS[@]}"; do
     if ! gh label list --json name | jq -e ".[] | select(.name == \"$label\")" > /dev/null; then
       echo "Missing: $label"
     fi
   done
   ```

6. **Analyze project scopes**:
   ```bash
   # Check for configured scopes in git-conventional-commits.json
   if [[ -f "git-conventional-commits.json" ]]; then
     SCOPES=$(jq -r '.convention.commitScopes[]?' git-conventional-commits.json)
   fi

   # If no configured scopes, analyze project structure
   if [[ -z "$SCOPES" ]]; then
     # Detect plugin directories
     PLUGIN_DIRS=$(find . -maxdepth 2 -name "plugin.json" -exec dirname {} \; | xargs -n1 basename)

     # Or use top-level directories (excluding common non-scopes)
     if [[ -z "$PLUGIN_DIRS" ]]; then
       SCOPES=$(ls -d */ 2>/dev/null | sed 's/\///' | grep -v -E '^(node_modules|dist|build|coverage|\.git)$')
     else
       SCOPES="$PLUGIN_DIRS"
     fi
   fi

   echo "Suggested scopes: $SCOPES"
   ```

7. **Sync issues** (using preference):
   ```bash
   # Use defaultIssueFilter from preferences (defaults to "assigned" for backward compatibility)
   FILTER=$(jq -r '.preferences.defaultIssueFilter // "assigned"' .claude/github-workflows/env.json 2>/dev/null || echo "assigned")
   python {baseDir}/scripts/issue-tracker.py sync $FILTER
   ```

8. **Detect branch context**:
   - Get current branch name
   - Extract issue number if present
   - Match to cached issues

9. **Write environment file**:
   - Save all context to `.claude/github-workflows/env.json`
   - This file is read by other commands

10. **Display summary**:
   ```
   ✅ GitHub Workflow Environment Initialized

   Repository: owner/repo
   User: username
   Project Board: Sprint 5 (#1)
   Current Milestone: Sprint 5 (due Jan 31)
   Current Branch: feature/issue-42 → Issues #42
     Detected scope: auth (scope:auth)

   📋 Label Stocktake:
     Existing: 15 labels
     Missing: 3 standard labels
       - priority:high
       - priority:medium
       - scope:frontend

   🏷️ Suggested Scope Labels (from project analysis):
     scope:agent-builder
     scope:self-improvement
     scope:github-workflows
     Run /label-suggest --create to add these

   📝 Tracked Issues: 5 assigned to you
     #42: Implement user authentication [High Priority]
     #56: Fix login validation [High Priority]
     #78: Add password reset [Normal]

   🔧 Setup Recommendations:
     ⚠️ Missing labels - run /label-sync standard to create
     ✅ Project board exists
     ✅ Active milestone found

   💡 Tips:
   - Use /commit-smart to commit with auto issue refs
   - Use /workflow-status to see full workflow state
   - Use /issue-track to refresh issue cache
   - Use /label-sync to create missing labels
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

📋 Label Stocktake:
  Existing: 12 labels
  Missing: 5 standard labels
    - bug
    - priority:high
    - priority:medium
    - scope:frontend
    - scope:backend

📝 Tracked Issues: 8 assigned to you
  HIGH PRIORITY:
    #142: Security vulnerability in auth
    #156: Performance regression in API

  NORMAL:
    #167: Add dark mode support
    #189: Update documentation

🔧 Setup Recommendations:
  ⚠️ Missing 5 labels - run /label-sync standard
  ✅ Project board exists
  ✅ Active milestone found

💡 Run /workflow-status for detailed view
   Run /label-sync standard to create missing labels
```

## Environment Variables Available

After initialization, these are available in `env.json`:

| Variable | Description | Example |
|----------|-------------|---------|
| `repository.fullName` | Full repo identifier | `owner/repo` |
| `user.login` | GitHub username | `developer` |
| `projectBoard.number` | Active project ID | `5` |
| `milestone.title` | Current milestone | `Sprint 5` |
| `branch.relatedIssues` | Issues selected for current branch | `[42, 43]` |
| `branch.detectedScope` | Scope detected from branch name | `"auth"` |
| `branch.scopeLabel` | Label matching detected scope | `"scope:auth"` |
| `labels.existing` | Count of existing labels | `15` |
| `labels.missing` | List of missing standard labels | `["priority:high"]` |
| `labels.suggestedScopes` | Scope labels suggested from project analysis | `["agent-builder"]` |
| `setup.labelsComplete` | Whether all standard labels exist | `false` |
| `preferences.projectType` | Personal or team project | `"personal"` |
| `preferences.defaultIssueFilter` | Default filter for issue-track | `"all"` |
| `preferences.defaultProject` | Default project board number | `3` |

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
