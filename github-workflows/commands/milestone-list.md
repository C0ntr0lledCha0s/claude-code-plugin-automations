---
description: List all milestones with progress tracking
allowed-tools: Bash
argument-hint: "[state: open|closed|all]"
---

# List Milestones

Display all milestones with their progress (open/closed issues count).

## Usage

```bash
/milestone-list              # List open milestones
/milestone-list open         # List open milestones
/milestone-list closed       # List closed milestones
/milestone-list all          # List all milestones
```

## Arguments

- **First argument** (optional): Filter by state - `open` (default), `closed`, or `all`

## What This Does

1. Fetches milestones from GitHub API
2. Calculates progress percentage for each
3. Shows due dates and days remaining
4. Sorts by due date (soonest first)

## Output Format

For each milestone, display:
- Title
- Progress: X/Y issues (Z%)
- Due date and days remaining (or overdue)
- State (open/closed)

## Example Output

```
## Open Milestones

### Phase: Hooks Validation
- Progress: 2/4 issues (50%)
- Due: 2024-03-31 (15 days remaining)
- State: Open

### v2.0.0
- Progress: 8/12 issues (67%)
- Due: 2024-04-15 (30 days remaining)
- State: Open

### Sprint 5
- Progress: 5/8 issues (63%)
- Due: 2024-03-20 (4 days remaining)
- State: Open
```

## Implementation

Use `gh api` to fetch milestones:

```bash
gh api repos/:owner/:repo/milestones?state=STATE --jq '.[] | {title, open_issues, closed_issues, due_on, state}'
```

Calculate progress and format output clearly.
