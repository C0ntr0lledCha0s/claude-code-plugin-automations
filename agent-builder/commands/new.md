---
description: Create a new Claude Code component (agent, skill, command, hook, or plugin)
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
argument-hint: "[type] [name]"
model: claude-sonnet-4-5
---

# Create New Component

Create a new Claude Code component using the orchestrator pattern.

**Arguments:**
- `$1` (required): Component type - `agent`, `skill`, `command`, `hook`, or `plugin`
- `$2` (required): Component name (lowercase-hyphens, max 64 chars)

**Full arguments:** $ARGUMENTS

## Workflow

1. **Validate Arguments**
   - Ensure type is one of: agent, skill, command, hook, plugin
   - Validate name follows conventions (lowercase-hyphens)

2. **Delegate to Orchestrator**
   - Use Task tool to invoke meta-architect agent
   - meta-architect will delegate to appropriate specialized builder

3. **Report Results**
   - Show created files/directories
   - Validation status
   - Next steps

## Delegation Pattern

```
/agent-builder:new agent code-reviewer
    ↓
meta-architect (orchestrator)
    ↓
agent-builder (specialized)
    ↓
Created: .claude/agents/code-reviewer.md
```

## Examples

### Create an Agent
```
/agent-builder:new agent code-reviewer
```

### Create a Skill
```
/agent-builder:new skill analyzing-code
```

### Create a Command
```
/agent-builder:new command run-tests
```

### Create a Hook
```
/agent-builder:new hook validate-write
```

### Create a Plugin
```
/agent-builder:new plugin code-review-suite
```

## Type-Specific Notes

| Type | Builder | Key Consideration |
|------|---------|-------------------|
| agent | agent-builder | Action-oriented naming |
| skill | skill-builder | Gerund naming, no model field |
| command | command-builder | Version alias for model |
| hook | hook-builder | Security review required |
| plugin | meta-architect | Multi-component orchestration |

## Error Handling

### Invalid Type
```
❌ Invalid type: "$1"

Valid types: agent, skill, command, hook, plugin
```

### Invalid Name
```
❌ Invalid name: "$2"

Names must be:
- Lowercase letters, numbers, and hyphens only
- Maximum 64 characters
- No underscores or special characters
```

## Execution

When invoked:
1. Parse $1 as type, $2 as name
2. Validate both arguments
3. Delegate to meta-architect with full context
4. Return comprehensive results from orchestration
