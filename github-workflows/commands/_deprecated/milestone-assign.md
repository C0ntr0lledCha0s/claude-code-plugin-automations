---
description: Bulk assign issues to a milestone based on filter
allowed-tools: Bash
argument-hint: "[milestone] [filter]"
---

# Assign Issues to Milestone

Bulk assign issues to a milestone using a filter query.

## Usage

```bash
/milestone-assign "Phase: Hooks Validation" "label:plugin:agent-builder"
/milestone-assign "v2.0.0" "label:feature"
/milestone-assign "Sprint 5" "is:open no:milestone"
```

## Arguments

- **First argument** (required): Milestone title (exact match)
- **Second argument** (required): GitHub issue filter query

## Common Filters

| Filter | Description |
|--------|-------------|
| `label:bug` | Issues with bug label |
| `label:plugin:agent-builder` | Issues for specific plugin |
| `is:open no:milestone` | Open issues without milestone |
| `is:open label:priority:high` | High priority open issues |

## What This Does

1. Validates milestone exists
2. Searches for issues matching filter
3. Shows preview of issues to be assigned
4. Assigns all matching issues to milestone
5. Reports count of assigned issues

## Output Format

```
## Assigning to Milestone: Phase: Hooks Validation

Found 4 issues matching filter "label:plugin:agent-builder is:open":

- #55 Add tool name validation for hook matchers
- #56 Add environment variable validation for hook commands
- #57 Add prompt hook best practices validation
- #58 Investigate SessionStart hook format

Assigning... Done!

Assigned 4 issues to "Phase: Hooks Validation"
Milestone progress: 0/4 issues (0%)
```

## Implementation

1. Verify milestone exists:
   ```bash
   gh api repos/:owner/:repo/milestones --jq '.[] | select(.title == "MILESTONE")'
   ```

2. Find matching issues:
   ```bash
   gh issue list --search "FILTER" --json number,title
   ```

3. Assign each issue:
   ```bash
   gh issue edit NUMBER --milestone "MILESTONE"
   ```
