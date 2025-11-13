---
description: Sync issues and PRs to a project board based on labels and filters
allowed-tools: Bash, Read
argument-hint: "[project-number] [filter]"
---

# Sync Project Board

Synchronize issues and pull requests to a project board.

## Usage

```bash
/project-sync 1
/project-sync 1 "label:feature"
/project-sync 1 "is:open milestone:v2.0"
```

## Arguments

- **First argument** (required): Project number
- **Second argument** (optional): Filter query for issues/PRs to add

## What This Does

1. Searches for issues/PRs matching filter
2. Adds them to the specified project board
3. Sets field values based on labels
4. Reports summary of items added
