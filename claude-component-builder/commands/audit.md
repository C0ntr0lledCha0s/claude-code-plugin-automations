---
description: Audit Claude Code components for quality, security, and compliance
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
argument-hint: "[type|--all|--deep path]"
model: claude-sonnet-4-5
---

# Audit Components

Audit Claude Code components for quality, security, and schema compliance.

**Arguments:**
- `$1` (optional): Component type OR `--all` OR `--deep`
  - Types: `agent`, `skill`, `command`, `hook` - audit all of that type
  - `--all`: Audit all component types (default if omitted)
  - `--deep`: Deep single-component analysis with scoring and recommendations
- `$2` (required for --deep): Path to specific component

**Full arguments:** $ARGUMENTS

## Workflow

### Single Type Audit
```
/claude-component-builder:audit agent
    ↓
Task → agent-builder
    ↓
Audit all agents in project
```

### Full Audit (--all)
```
/claude-component-builder:audit --all
    ↓
Parallel Task invocations
    ↓
├─ agent-builder: Audit agents
├─ skill-builder: Audit skills
├─ command-builder: Audit commands
└─ hook-builder: Audit hooks
    ↓
Consolidated report
```

### Deep Single-Component Analysis (--deep)
```
/claude-component-builder:audit --deep agents/code-reviewer.md
    ↓
Detect type → agent
    ↓
Task → agent-builder: "Deep quality analysis"
    ↓
Detailed scoring + recommendations
```

## Audit Categories

### Agents
- Schema compliance
- Naming conventions
- Tool permissions
- Model selection
- Content quality

### Skills
- Directory structure
- No model field (critical)
- {baseDir} usage
- Auto-invoke triggers
- Resource organization

### Commands
- Model format (version alias, not short)
- Argument documentation
- Security (Bash validation)
- Description clarity

### Hooks
- Security (7 categories)
- Matcher specificity
- JSON schema
- Script validation

## Examples

### Audit All Components
```
/claude-component-builder:audit --all
```

### Audit Only Agents
```
/claude-component-builder:audit agent
```

### Audit Only Skills
```
/claude-component-builder:audit skill
```

### Audit Only Commands
```
/claude-component-builder:audit command
```

### Audit Only Hooks
```
/claude-component-builder:audit hook
```

### Deep Analysis of Single Component
```
/claude-component-builder:audit --deep agents/code-reviewer.md
/claude-component-builder:audit --deep skills/building-agents/
/claude-component-builder:audit --deep commands/validate.md
```

## Report Format

```markdown
## Audit Report: my-plugin

### Summary
| Type | Count | Pass | Warn | Fail |
|------|-------|------|------|------|
| Agents | 5 | 4 | 1 | 0 |
| Skills | 3 | 2 | 0 | 1 |
| Commands | 8 | 7 | 1 | 0 |
| Hooks | 2 | 2 | 0 | 0 |
| **Total** | **18** | **15** | **2** | **1** |

### Critical Issues (1)
1. **skills/analyzing-data/SKILL.md**: Has `model: sonnet` field - skills cannot have model field
   - Fix: Remove the model field entirely from SKILL.md frontmatter
   - Impact: Skill will fail to load in Claude Code

### Warnings (2)
1. **agents/data-processor.md**: Uses Bash tool without input validation guidance
   - Recommendation: Add Input Validation section or remove Bash from tools
2. **commands/export-data.md**: Missing argument-hint field
   - Recommendation: Add `argument-hint: "[format] [output-path]"`

### Passing Components (15)
- agents/analyzer.md ✅
- agents/reporter.md ✅
- agents/validator.md ✅
- agents/transformer.md ✅
- skills/processing-data/ ✅
- skills/generating-reports/ ✅
- commands/analyze.md ✅
- commands/validate.md ✅
- commands/transform.md ✅
- commands/report.md ✅
- commands/import.md ✅
- commands/status.md ✅
- commands/config.md ✅
- hooks/hooks.json ✅ (2 hooks)

### Recommendations (Prioritized)
1. 🔴 **Fix skill model field** - Critical, blocks skill loading
2. 🟡 **Add Bash validation guidance** - Important for security
3. 🟢 **Add argument hints** - Improves user experience
```

## Deep Analysis Output Format

```markdown
## Deep Analysis: code-reviewer

**Overall Score**: 32/40 (80%)

### Detailed Scores
| Dimension | Score | Status |
|-----------|-------|--------|
| Schema | 10/10 | ✅ |
| Security | 7/10 | ⚠️ |
| Quality | 8/10 | ✅ |
| Maintainability | 7/10 | ⚠️ |

### Findings

#### ✅ Strengths
- Valid YAML frontmatter with all required fields
- Clear, action-oriented naming convention
- Well-structured workflow documentation

#### ⚠️ Areas for Improvement
- Missing color field for terminal identification
- No capabilities array defined
- Examples section could be more comprehensive

### Recommendations (Prioritized)
1. 🔴 HIGH: Add input validation for Bash commands
2. 🟡 MEDIUM: Add capabilities array
3. 🟢 LOW: Expand examples section

### Next Steps
1. Apply fixes manually or ask Claude to update
2. Re-validate: `python3 validate-agent.py code-reviewer.md`
3. Test the updated component
```

## Execution

When invoked:
1. Parse audit scope from $1
2. If `--deep`: detect component type, delegate deep analysis to builder
3. If type specified: delegate to single builder
4. If `--all`: parallel Task invocations to all builders
5. Aggregate and return report
