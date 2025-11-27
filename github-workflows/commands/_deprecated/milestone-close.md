---
description: Close a completed milestone
allowed-tools: Bash
argument-hint: "[milestone-title]"
---

# Close Milestone

Close a milestone when all work is complete.

## Usage

```bash
/milestone-close "Phase: Hooks Validation"
/milestone-close "v2.0.0"
/milestone-close "Sprint 5"
```

## Arguments

- **First argument** (required): Milestone title (exact match)

## What This Does

1. Validates milestone exists and is open
2. Checks for open issues (warns if any remain)
3. Closes the milestone
4. Reports final statistics

## Output Format

### Success (all issues closed)

```
## Closing Milestone: Phase: Hooks Validation

### Final Statistics
- Total issues: 4
- Completed: 4 (100%)
- Due date: 2024-03-31
- Actual completion: 2024-03-25 (6 days early!)

Closing milestone... Done!

Milestone "Phase: Hooks Validation" is now closed.
```

### Warning (open issues remain)

```
## Closing Milestone: Phase: Hooks Validation

### Warning: Open Issues Remain

2 issues are still open:
- #103 Add prompt hook best practices
- #104 Update validator for SessionStart

### Options
1. Close milestone anyway (issues will remain assigned)
2. Cancel and complete remaining issues first

Do you want to close the milestone with open issues? [y/N]
```

## Implementation

1. Get milestone number:
   ```bash
   gh api repos/:owner/:repo/milestones --jq '.[] | select(.title == "MILESTONE") | .number'
   ```

2. Check for open issues:
   ```bash
   gh issue list --milestone "MILESTONE" --state open
   ```

3. Close milestone:
   ```bash
   gh api repos/:owner/:repo/milestones/NUMBER -X PATCH -f state="closed"
   ```
