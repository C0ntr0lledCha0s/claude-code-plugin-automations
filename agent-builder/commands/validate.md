---
description: Validate a Claude Code component or plugin for schema compliance
allowed-tools: Read, Grep, Glob, Bash
argument-hint: "[path]"
model: claude-haiku-4-5
---

# Validate Component

Validate a Claude Code component or plugin for schema compliance and best practices.

**Arguments:**
- `$1` (required): Path to component file or plugin directory

**Full arguments:** $ARGUMENTS

## Workflow

1. **Detect Component Type**
   - Agent: `*/agents/*.md`
   - Skill: `*/skills/*/SKILL.md`
   - Command: `*/commands/*.md`
   - Hook: `*/hooks.json` or `*/hooks/hooks.json`
   - Plugin: Directory with `.claude-plugin/plugin.json`

2. **Run Appropriate Validator**
   - Use validation scripts from building-* skills
   - Check schema compliance
   - Verify best practices

3. **Report Results**
   - Pass/fail status
   - Specific issues found
   - Recommendations

## Validation Scripts

| Type | Script |
|------|--------|
| Agent | `validate-agent.py` |
| Skill | `validate-skill.py` |
| Command | `validate-command.py` |
| Hook | `validate-hooks.py` |
| Plugin | `validate-plugin.py` |

## Examples

### Validate an Agent
```
/agent-builder:validate .claude/agents/code-reviewer.md
```

### Validate a Skill
```
/agent-builder:validate .claude/skills/analyzing-code/
```

### Validate a Command
```
/agent-builder:validate .claude/commands/run-tests.md
```

### Validate Hooks
```
/agent-builder:validate .claude/hooks.json
```

### Validate a Plugin
```
/agent-builder:validate my-plugin/
```

## Validation Checks

### All Components
- ✅ Valid YAML/JSON syntax
- ✅ Required fields present
- ✅ Naming conventions (lowercase-hyphens)
- ✅ Max length (64 chars)

### Agents
- ✅ Valid frontmatter
- ✅ name and description present
- ✅ Valid tools list (if specified)
- ✅ Valid model (if specified)

### Skills
- ✅ SKILL.md exists
- ✅ **No model field** (critical)
- ✅ Directory structure valid
- ✅ {baseDir} references valid

### Commands
- ✅ description present
- ✅ **Model format correct** (version alias)
- ✅ Arguments documented
- ✅ Bash security (if used)

### Hooks
- ✅ Valid JSON schema
- ✅ Valid event types
- ✅ Matcher patterns valid
- ✅ Scripts exist (if referenced)
- ✅ Security assessment

### Plugins
- ✅ plugin.json valid
- ✅ All referenced paths exist
- ✅ Components valid
- ✅ README.md exists

## Output Format

### Success
```
✅ VALIDATION PASSED: [path]

Component: [type]
Schema: Valid
Best Practices: Followed

Recommendations:
- [Optional improvements]
```

### Failure
```
❌ VALIDATION FAILED: [path]

Component: [type]

Critical Issues:
1. [Issue 1]
2. [Issue 2]

Warnings:
1. [Warning 1]

How to Fix:
1. [Fix for issue 1]
2. [Fix for issue 2]
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All validations passed |
| 1 | Critical errors found |
| 2 | Warnings only |

## Execution

When invoked:
1. Parse path from $1
2. Detect component type from path pattern
3. Run appropriate validation script
4. Return detailed validation results
