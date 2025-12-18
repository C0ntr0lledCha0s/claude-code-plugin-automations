---
description: Comprehensive documentation audit with quality scoring and recommendations
allowed-tools:
  - Read
  - Glob
  - Grep
  - Task
argument-hint: "[directory]"
---

# Documentation Audit

Perform a comprehensive documentation audit of the specified directory (or entire codebase).

**Target:** $ARGUMENTS (defaults to current directory if empty)

## Audit Scope

This audit evaluates:
1. **Documentation Coverage** - What percentage of code is documented
2. **Documentation Quality** - How good is the existing documentation
3. **Documentation Structure** - How well organized is the documentation
4. **Documentation Currency** - Is documentation up to date

## Audit Process

### Phase 1: Discovery
1. Identify all source files
2. Locate all documentation files (README, docs/, etc.)
3. Detect documentation tools in use (JSDoc, Sphinx, etc.)
4. Map the documentation landscape

### Phase 2: Coverage Analysis
1. Count documentable items (functions, classes, modules)
2. Count documented items
3. Calculate coverage by category
4. Identify critical gaps

### Phase 3: Quality Assessment

Score each dimension (0-10):

**Completeness**
- All public APIs documented
- Parameters and returns described
- Error conditions explained

**Accuracy**
- Documentation matches code
- Examples are correct
- Types are accurate

**Clarity**
- Clear language
- Good organization
- Consistent style

**Usefulness**
- Practical examples
- Common use cases
- Helpful links

### Phase 4: Structure Review
1. Evaluate README.md completeness
2. Check documentation directory organization
3. Assess navigation and discoverability
4. Review cross-linking between docs

### Phase 5: Currency Check
1. Compare documentation dates to code changes
2. Identify potentially outdated docs
3. Check for deprecated content
4. Flag stale examples

## Output Report

Generate a comprehensive markdown report:

```markdown
# Documentation Audit Report

## Executive Summary
- Overall Health Score: X/10
- Coverage: XX%
- Critical Issues: X

## Coverage Analysis
[Table with coverage by category]

## Quality Scores
| Dimension | Score | Issues |
|-----------|-------|--------|
| Completeness | X/10 | ... |
| Accuracy | X/10 | ... |
| Clarity | X/10 | ... |
| Usefulness | X/10 | ... |

## Critical Issues
[Prioritized list of issues to fix]

## Recommendations
[Actionable improvement suggestions]

## Detailed Findings
[File-by-file breakdown]
```

## Priority Classification

- **Critical**: Public APIs without documentation
- **High**: Missing parameter/return documentation
- **Medium**: Outdated examples or descriptions
- **Low**: Style inconsistencies, minor improvements

Use the docs-analyzer agent for complex audits requiring deep analysis.
