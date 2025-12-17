---
description: Create a new Claude Code component (agent, skill, command, or hook). For plugins, use `/agent-builder:plugin create` instead.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
argument-hint: "[type] [name]"
model: claude-sonnet-4-5
---

# Create New Component

Create a new Claude Code component by delegating to the appropriate specialized builder agent.

**Arguments:**
- `$1` (required): Component type - `agent`, `skill`, `command`, `hook`
- `$2` (required): Component name (lowercase-hyphens, max 64 chars)

**Full arguments:** $ARGUMENTS

## Important: Plugin Creation

For creating **plugins** (multi-component packages), use the dedicated plugin command:
```
/agent-builder:plugin create my-plugin
```

The plugin command provides full orchestration including:
- Research of existing patterns
- Template selection
- Parallel component creation
- Validation and finalization

## Workflow

### Step 1: Validate Arguments

1. Ensure type is one of: `agent`, `skill`, `command`, `hook`
2. If type is `plugin`, redirect user to `/agent-builder:plugin create`
3. Validate name follows conventions:
   - Lowercase letters, numbers, and hyphens only
   - Maximum 64 characters
   - No underscores or special characters

### Step 2: Delegate to Specialized Builder

Use the Task tool to invoke the appropriate builder agent:

| Type | Builder Agent | Example Prompt |
|------|---------------|----------------|
| agent | `agent-builder` | "Create agent 'code-reviewer' for [purpose]" |
| skill | `skill-builder` | "Create skill 'analyzing-code' for [purpose]" |
| command | `command-builder` | "Create command 'run-tests' for [purpose]" |
| hook | `hook-builder` | "Create hook 'validate-write' for [purpose]" |

### Step 3: Report Results

Show:
- Created files/directories
- Validation status
- Next steps for testing

## Delegation Pattern

```
/agent-builder:new agent code-reviewer
    ↓
Validate: type=agent, name=code-reviewer ✓
    ↓
Task → agent-builder
Prompt: "Create agent 'code-reviewer' for reviewing code quality"
    ↓
Created: .claude/agents/code-reviewer.md
```

## Examples

### Create an Agent
```
/agent-builder:new agent code-reviewer
```
Delegates to `agent-builder` agent.

### Create a Skill
```
/agent-builder:new skill analyzing-code
```
Delegates to `skill-builder` agent.

### Create a Command
```
/agent-builder:new command run-tests
```
Delegates to `command-builder` agent.

### Create a Hook
```
/agent-builder:new hook validate-write
```
Delegates to `hook-builder` agent.

## Type-Specific Notes

| Type | Builder | Key Consideration |
|------|---------|-------------------|
| agent | agent-builder | Action-oriented naming (e.g., code-reviewer) |
| skill | skill-builder | Gerund naming (e.g., analyzing-code), NO model field |
| command | command-builder | Model must use version alias (e.g., claude-sonnet-4-5) |
| hook | hook-builder | Security review required for all hooks |

## Error Handling

### Plugin Type Requested
```
ℹ️ For plugins, use the dedicated plugin command:

/agent-builder:plugin create $2

This provides full orchestration including template selection,
parallel component creation, and marketplace registration.
```

### Invalid Type
```
❌ Invalid type: "$1"

Valid types: agent, skill, command, hook

For plugins, use: /agent-builder:plugin create [name]
```

### Invalid Name
```
❌ Invalid name: "$2"

Names must be:
- Lowercase letters, numbers, and hyphens only
- Maximum 64 characters
- No underscores or special characters

Examples: code-reviewer, analyzing-code, run-tests
```

### Builder Agent Failed
```
⚠️ Component creation failed

Error from $1-builder: [error details]

Options:
1. Fix the issue and retry
2. Check validation: /agent-builder:validate [path]
```

## Execution

When invoked:
1. Parse `$1` as type, `$2` as name
2. If type is "plugin", inform user to use `/agent-builder:plugin create`
3. Validate type is one of: agent, skill, command, hook
4. Validate name follows conventions
5. Invoke appropriate builder agent via Task tool
6. Return results from builder
