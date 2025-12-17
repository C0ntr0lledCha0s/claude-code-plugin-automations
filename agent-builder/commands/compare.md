---
description: Compare two components side-by-side to understand differences
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
argument-hint: "[type] [name1] [name2]"
model: claude-sonnet-4-5
---

# Compare Components

Compare two Claude Code components side-by-side to understand differences and trade-offs.

**Arguments:**
- `$1` (required): Component type - `agent`, `skill`, `command`, `hook`
- `$2` (required): First component name
- `$3` (required): Second component name

**Full arguments:** $ARGUMENTS

## Workflow

1. **Locate Components**
   - Find both components by type
   - Read configurations

2. **Delegate Comparison**
   - Route via Task to appropriate builder
   - Builder performs detailed comparison

3. **Return Analysis**
   - Side-by-side differences
   - Trade-off analysis
   - Recommendations

## Comparison Aspects

### Frontmatter
- Name and description
- Tools/permissions
- Model selection
- Optional fields

### Content
- Capabilities/sections
- Workflow steps
- Examples
- Documentation

### Quality
- Schema compliance
- Security posture
- Maintainability

## Examples

### Compare Agents
```
/agent-builder:compare agent code-reviewer security-auditor
```

### Compare Skills
```
/agent-builder:compare skill analyzing-code reviewing-tests
```

### Compare Commands
```
/agent-builder:compare command run-tests test-coverage
```

### Compare Hooks
```
/agent-builder:compare hook validate-write validate-bash
```

## Output Format

```markdown
## Component Comparison

### Overview
| Aspect | [name1] | [name2] |
|--------|---------|---------|
| Type | agent | agent |
| Model | sonnet | haiku |
| Tools | 5 | 3 |

### Frontmatter Diff
```diff
  name: [name1]           | name: [name2]
- model: sonnet           | + model: haiku
  tools: Read, Write...   | tools: Read, Grep...
```

### Capabilities Comparison
| Capability | [name1] | [name2] |
|------------|---------|---------|
| Code review | ✅ | ❌ |
| Security scan | ❌ | ✅ |
| Documentation | ✅ | ✅ |

### Quality Scores
| Dimension | [name1] | [name2] |
|-----------|---------|---------|
| Schema | 10/10 | 10/10 |
| Security | 8/10 | 9/10 |
| Quality | 9/10 | 7/10 |
| **Total** | **27/30** | **26/30** |

### Analysis

#### Similarities
- [What they share]

#### Differences
- [Key differences]

#### Trade-offs
| Choose [name1] when... | Choose [name2] when... |
|------------------------|------------------------|
| [Use case 1] | [Use case 2] |
| [Use case 3] | [Use case 4] |

### Recommendation
[Which to use and why, or when to use each]

### Potential Overlap
⚠️ These components have [X%] overlap.
Consider: [Consolidation recommendation]
```

## Use Cases

### Deciding Between Similar Components
Compare to understand which fits your needs.

### Finding Redundancy
Identify overlapping functionality to consolidate.

### Learning Patterns
See how different implementations approach similar problems.

### Before Refactoring
Understand current state before making changes.

## Execution

When invoked:
1. Parse type and both names from arguments
2. Delegate via Task to appropriate builder
3. Builder performs comprehensive comparison
4. Return detailed analysis with recommendations
