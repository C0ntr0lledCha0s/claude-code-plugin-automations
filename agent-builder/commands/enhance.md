---
description: Analyze component quality and get AI-powered improvement suggestions
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
argument-hint: "[type] [name]"
model: claude-sonnet-4-5
---

# Enhance Component

Analyze a Claude Code component's quality and get prioritized improvement suggestions.

**Arguments:**
- `$1` (required): Component type - `agent`, `skill`, `command`, `hook`
- `$2` (required): Component name to analyze

**Full arguments:** $ARGUMENTS

## Workflow

1. **Locate Component**
   - Find component by type and name
   - Read current configuration

2. **Delegate Analysis**
   - meta-architect routes to appropriate builder
   - Builder performs deep quality analysis

3. **Return Recommendations**
   - Detailed scoring across dimensions
   - Prioritized improvement suggestions
   - Actionable next steps

## Scoring Dimensions

### Agents (40 points total)
| Dimension | Points | What's Measured |
|-----------|--------|-----------------|
| Schema | 10 | Required fields, syntax |
| Security | 10 | Tool permissions, validation |
| Quality | 10 | Content, examples, workflow |
| Maintainability | 10 | Organization, documentation |

### Skills (40 points total)
| Dimension | Points | What's Measured |
|-----------|--------|-----------------|
| Schema | 10 | No model field, structure |
| Auto-invoke | 10 | Trigger specificity |
| Resources | 10 | {baseDir} usage, organization |
| Documentation | 10 | Completeness, examples |

### Commands (40 points total)
| Dimension | Points | What's Measured |
|-----------|--------|-----------------|
| Schema | 10 | Model format, fields |
| Arguments | 10 | Documentation, handling |
| Security | 10 | Bash validation |
| Usability | 10 | Examples, clarity |

### Hooks (40 points total)
| Dimension | Points | What's Measured |
|-----------|--------|-----------------|
| Schema | 10 | JSON validity |
| Security | 10 | 7-category analysis |
| Matchers | 10 | Specificity, safety |
| Scripts | 10 | Existence, permissions |

## Examples

### Enhance an Agent
```
/agent-builder:enhance agent code-reviewer
```

### Enhance a Skill
```
/agent-builder:enhance skill analyzing-code
```

### Enhance a Command
```
/agent-builder:enhance command run-tests
```

### Enhance a Hook
```
/agent-builder:enhance hook validate-write
```

## Output Format

```markdown
## Enhancement Analysis: [component-name]

**Overall Score**: X/40 (Y%)

### Detailed Scores
| Dimension | Score | Status |
|-----------|-------|--------|
| Schema | 10/10 | ✅ |
| Security | 8/10 | ⚠️ |
| Quality | 7/10 | ⚠️ |
| Maintainability | 9/10 | ✅ |

### Findings

#### ✅ Strengths
- [What's working well]

#### ⚠️ Areas for Improvement
- [What needs attention]

### Recommendations (Prioritized)

1. 🔴 HIGH: [Critical improvement]
2. 🟡 MEDIUM: [Important improvement]
3. 🟢 LOW: [Nice-to-have improvement]

### Next Steps
1. [Actionable step 1]
2. [Actionable step 2]
```

## Execution

When invoked:
1. Parse type and name from arguments
2. Delegate to meta-architect
3. Builder performs comprehensive analysis
4. Return detailed findings and recommendations
