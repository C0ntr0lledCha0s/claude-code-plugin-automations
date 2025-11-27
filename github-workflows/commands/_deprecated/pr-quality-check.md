---
description: Run quality gates on PR without full review (quick check)
allowed-tools: Bash
argument-hint: "[pr-number]"
---

# PR Quality Check

Quick quality gate check without detailed review.

## Usage

```bash
/pr-quality-check 123
/pr-quality-check
```

## Arguments

- **First argument** (optional): PR number. If omitted, uses current branch's PR

## What This Does

1. Runs all quality gates
2. Reports pass/fail for each
3. Provides summary
4. No detailed review or comments posted

## Quality Gates Checked

- CI/CD status
- Test coverage
- Security scan
- PR size
- Breaking changes

Faster than full review - use for quick validation.
