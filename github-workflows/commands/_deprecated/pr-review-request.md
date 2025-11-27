---
description: Comprehensive PR review with quality gates and self-improvement integration
allowed-tools: Bash, Read, Grep
argument-hint: "[pr-number]"
---

# Request PR Review

Perform comprehensive pull request review with quality validation.

## Usage

```bash
/pr-review-request 123
/pr-review-request
```

## Arguments

- **First argument** (optional): PR number. If omitted, uses current branch's PR

## What This Does

1. **Fetch PR details**: Changes, commits, files
2. **Run quality gates**:
   - CI/CD status
   - Test coverage
   - Security scan
   - Breaking changes
3. **Invoke self-improvement**: `/quality-check` for deep analysis
4. **Generate review**: Detailed feedback with scores
5. **Make decision**: Approve, request changes, or comment
6. **Post review**: Submit to GitHub

## Quality Gates

- ✅ All CI checks must pass
- ✅ Test coverage >= 80%
- ✅ Security scan passes
- ✅ Quality scores >= thresholds
- ✅ No critical issues

## Decision Criteria

**Approve**: All gates passed, scores >= 4/5
**Request Changes**: Critical issues or scores < 3/5
**Comment**: Minor suggestions only
