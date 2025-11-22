---
description: Show detailed progress report for a milestone
allowed-tools: Bash
argument-hint: "[milestone-title]"
---

# Milestone Progress Report

Display detailed progress report for a specific milestone.

## Usage

```bash
/milestone-progress "Phase: Hooks Validation"
/milestone-progress "v2.0.0"
/milestone-progress "Sprint 5"
```

## Arguments

- **First argument** (required): Milestone title (exact match)

## What This Does

1. Fetches milestone details
2. Lists all issues in milestone grouped by state
3. Shows progress by label/type
4. Calculates completion rate and velocity
5. Estimates completion date if applicable

## Output Format

```
## Milestone: Phase: Hooks Validation

### Overview
- **Progress**: 2/4 issues (50%)
- **Due date**: 2024-03-31
- **Days remaining**: 15
- **Status**: On track

### Issues by State

**Closed (2)**:
- #101 Add tool name validation ✓
- #102 Add environment variable validation ✓

**Open (2)**:
- #103 Add prompt hook best practices
- #104 Update validator for SessionStart

### Progress by Type
- enhancement: 2/3 (67%)
- bug: 0/1 (0%)

### Velocity
- Closed this week: 2
- Average: 1.5 issues/week
- Estimated completion: 2024-03-25 (6 days ahead of schedule)
```

## Implementation

1. Get milestone details:
   ```bash
   gh api repos/:owner/:repo/milestones --jq '.[] | select(.title == "MILESTONE")'
   ```

2. Get issues in milestone:
   ```bash
   gh issue list --milestone "MILESTONE" --state all --json number,title,state,labels
   ```

3. Calculate statistics and format report.
