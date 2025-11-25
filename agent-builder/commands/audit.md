---
description: Audit Claude Code components for quality, security, and compliance
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
argument-hint: "[type|--all]"
model: claude-sonnet-4-5
---

# Audit Components

Audit Claude Code components for quality, security, and schema compliance.

**Arguments:**
- `$1` (optional): Component type to audit OR `--all` for all types
  - Types: `agent`, `skill`, `command`, `hook`
  - Default: `--all` if not specified

**Full arguments:** $ARGUMENTS

## Workflow

### Single Type Audit
```
/agent-builder:audit agent
    ↓
meta-architect → agent-builder
    ↓
Audit all agents in project
```

### Full Audit (--all)
```
/agent-builder:audit --all
    ↓
meta-architect (orchestrator)
    ↓ (parallel)
├─ agent-builder: Audit agents
├─ skill-builder: Audit skills
├─ command-builder: Audit commands
└─ hook-builder: Audit hooks
    ↓
Consolidated report
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
/agent-builder:audit --all
```

### Audit Only Agents
```
/agent-builder:audit agent
```

### Audit Only Skills
```
/agent-builder:audit skill
```

### Audit Only Commands
```
/agent-builder:audit command
```

### Audit Only Hooks
```
/agent-builder:audit hook
```

## Report Format

```markdown
## Audit Report

### Summary
| Type | Count | Pass | Warn | Fail |
|------|-------|------|------|------|
| Agents | 5 | 4 | 1 | 0 |
| Skills | 3 | 2 | 0 | 1 |
| Commands | 8 | 7 | 1 | 0 |
| Hooks | 2 | 2 | 0 | 0 |

### Critical Issues
- [List of critical issues requiring immediate attention]

### Warnings
- [List of warnings for improvement]

### Recommendations
1. [Prioritized recommendations]
```

## Execution

When invoked:
1. Parse audit scope from $1
2. Delegate to meta-architect
3. For --all: parallel delegation to all builders
4. Aggregate and return consolidated report
