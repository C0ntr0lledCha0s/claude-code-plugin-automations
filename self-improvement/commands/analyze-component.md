---
description: Analyze the quality of a Claude Code component (agent, skill, command, hook) with detailed scores and improvement suggestions
allowed-tools: Read, Bash
argument-hint: "<component-path>"
model: claude-sonnet-4-5
---

# Analyze Component Quality

You are analyzing the quality of a Claude Code component. This command provides comprehensive quality evaluation beyond technical validation.

## Task

Analyze the component at path: `$1`

## Process

### 1. Run Automated Quality Scoring

First, run the automated quality scorer:

```bash
python self-improvement/skills/analyzing-component-quality/scripts/quality-scorer.py "$1"
```

This provides baseline scores for:
- Description Clarity
- Tool Permissions
- Auto-Invoke Triggers (if skill)
- Security
- Usability

### 2. Invoke Quality Analysis Skill

Invoke the `analyzing-component-quality` skill for deep analysis:

1. **Read the component file** to understand its purpose and implementation
2. **Identify the component type** (agent, skill, command, hook)
3. **Score each quality dimension** (1-5) with specific justification
4. **Identify specific issues** categorized by severity (critical, important, minor)
5. **Provide concrete improvement suggestions** with before/after examples

### 3. Generate Comprehensive Report

Produce a detailed quality report including:

```markdown
# Component Quality Analysis

**Component**: [name from frontmatter]
**Type**: [agent/skill/command/hook]
**Location**: `$1`
**Overall Quality**: X.X/5 ([Excellent/Good/Adequate/Poor/Critical])

## Quality Scores

| Dimension | Score | Assessment |
|-----------|-------|------------|
| Description Clarity | X/5 | [Brief justification] |
| Tool Permissions | X/5 | [Brief justification] |
| Auto-Invoke Triggers | X/5 | [If applicable] |
| Security | X/5 | [Brief justification] |
| Usability | X/5 | [Brief justification] |

## Issues Identified

### 🔴 Critical Issues
1. [Issue with specific location and impact]
2. [Issue with specific location and impact]

### 🟡 Important Issues
1. [Issue with explanation]
2. [Issue with explanation]

### 🟢 Minor Issues
1. [Issue with suggestion]

## Improvement Suggestions

### 1. [Improvement Title]
**Priority**: Critical/Important/Minor
**Current**:
```[yaml/markdown]
[Current problematic content]
```

**Suggested**:
```[yaml/markdown]
[Improved content]
```

**Rationale**: [Why this improves quality]
**Expected Impact**: [Improvement in score]

[Additional suggestions...]

## Strengths

- [What this component does well]
- [Good design decisions]

## Recommended Actions

1. [Highest priority action]
2. [Next priority action]
3. [Additional improvements]

## Quality Projection

If critical and important issues are addressed:
- **Current Quality**: X.X/5
- **Projected Quality**: X.X/5
- **Improvement**: +X.X points

## Next Steps

To apply these improvements:
```bash
/improve-component $1
```

To compare with similar components:
```bash
/claude-component-builder:compare [type] [component1] [component2]
```
```

## Quality Dimensions Reference

### Description Clarity (1-5)
- **5/5**: Specific, detailed (100+ chars), clear triggers, examples
- **4/5**: Good clarity, minor vagueness
- **3/5**: Adequate but could be more specific
- **2/5**: Vague or unclear purpose
- **1/5**: Too vague to understand purpose

### Tool Permissions (1-5)
- **5/5**: Minimal necessary tools, all justified
- **4/5**: Appropriate with minor concerns
- **3/5**: Some unnecessary tools
- **2/5**: Excessive permissions
- **1/5**: Dangerous or unjustified permissions

### Auto-Invoke Triggers (1-5) - Skills Only
- **5/5**: Specific quoted phrases, unambiguous
- **4/5**: Clear but could be more specific
- **3/5**: Somewhat vague
- **2/5**: Too vague to match effectively
- **1/5**: No clear triggers or too broad

### Security (1-5)
- **5/5**: No security concerns, minimal permissions
- **4/5**: Generally secure, minor considerations
- **3/5**: Some security concerns
- **2/5**: Significant security risks
- **1/5**: Critical vulnerabilities

### Usability (1-5)
- **5/5**: Excellent docs, examples, intuitive
- **4/5**: Good usability, minor improvements possible
- **3/5**: Adequate but could be clearer
- **2/5**: Confusing or poorly documented
- **1/5**: Very hard to understand or use

## Output Format

Provide a comprehensive analysis that:
- ✓ Uses the quality report template above
- ✓ Scores each dimension with specific justification
- ✓ Categorizes issues by severity
- ✓ Provides concrete before/after improvements
- ✓ Includes both strengths and weaknesses
- ✓ Gives actionable next steps

## Important Notes

- This analysis assumes the component has **already passed technical validation** (schema, syntax)
- Focus on **quality and effectiveness**, not just correctness
- Be **specific** - quote exact text, cite line numbers where possible
- Provide **constructive** feedback with clear improvement paths
- Consider **context** - marketplace components need higher standards than internal tools

Your analysis helps improve the overall quality of Claude Code components across the ecosystem.
