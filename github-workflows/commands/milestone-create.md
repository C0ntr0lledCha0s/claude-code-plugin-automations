---
description: Create a milestone with title and due date
allowed-tools: Bash
argument-hint: "[title] [due-date]"
---

# Create Milestone

Create a new milestone for tracking issues.

## Usage

```bash
/milestone-create "v2.0" "2024-03-31"
/milestone-create "Sprint 5" "14"
```

## Arguments

- **First argument** (required): Milestone title
- **Second argument** (optional): Due date (YYYY-MM-DD or days from now)

## What This Does

1. Creates milestone via GitHub API
2. Sets due date if provided
3. Returns milestone number
4. Reports created milestone details
