---
description: Update an existing Claude Code component with interactive workflow
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
argument-hint: "[type] [name]"
model: claude-sonnet-4-5
---

# Update Component

Update an existing Claude Code component using the orchestrator pattern.

**Arguments:**
- `$1` (required): Component type - `agent`, `skill`, `command`, `hook`
- `$2` (required): Component name to update

**Full arguments:** $ARGUMENTS

## Workflow

1. **Validate Arguments**
   - Ensure type is valid
   - Verify component exists

2. **Delegate to Builder**
   - Route via Task to appropriate builder
   - Builder provides interactive update workflow

3. **Report Results**
   - Show diff of changes
   - Validation status
   - Recommendations

## Update Capabilities

| Aspect | Supported |
|--------|-----------|
| Description | ✅ |
| Tools/Permissions | ✅ |
| Model (agents/commands) | ✅ |
| Body content | ✅ |
| Resources (skills) | ✅ |

## Examples

### Update an Agent
```
/agent-builder:update agent code-reviewer
```

### Update a Skill
```
/agent-builder:update skill analyzing-code
```

### Update a Command
```
/agent-builder:update command run-tests
```

### Update a Hook
```
/agent-builder:update hook validate-write
```

## Type-Specific Behavior

| Type | Builder | Special Handling |
|------|---------|------------------|
| agent | agent-builder | Tools, model, description |
| skill | skill-builder | Resources, {baseDir} refs |
| command | command-builder | Model format validation |
| hook | hook-builder | Security re-assessment |

## Error Handling

### Component Not Found
```
❌ Component not found: "$2"

Searched locations:
- .claude/agents/$2.md
- plugin-dir/agents/$2.md

Use /agent-builder:new to create it.
```

## Execution

When invoked:
1. Parse type and name from arguments
2. Locate existing component
3. Delegate via Task to appropriate builder
4. Return update results with diff
