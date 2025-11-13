---
description: Comprehensive issue triage with duplicate detection, labeling, and relationship mapping
allowed-tools: Bash, Read, Grep
argument-hint: "[issue-number]"
---

# Triage Issue

Perform comprehensive triage on a GitHub issue.

## Usage

```bash
/issue-triage 42
/issue-triage all
```

## Arguments

- **First argument** (required): Issue number or "all" for batch triage

## What This Does

1. **Classify**: Determine type, priority, scope
2. **Check duplicates**: Search for similar issues
3. **Validate quality**: Check completeness
4. **Map relationships**: Find dependencies
5. **Apply labels**: Add appropriate labels
6. **Add to board**: Include in project tracking
7. **Assign**: Route to team if high priority
