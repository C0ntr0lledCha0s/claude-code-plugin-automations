---
description: Create a new Claude Code event hook for automation and validation
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
argument-hint: [hook-name]
model: claude-sonnet-4-5
---

# Create New Hook

Create a new Claude Code event hook named: **$1**

## Your Task

1. **Gather Requirements**: Ask the user about:
   - What event should trigger the hook?
   - What validation or action is needed?
   - Should it block, warn, or just log?
   - What tools or operations need monitoring?
   - Where should the hook be placed? (project-level, directory-specific, plugin)

2. **Choose Event and Matcher**: Based on requirements:
   - **PreToolUse**: Validate before tool execution (needs matcher)
   - **PostToolUse**: Process after tool execution (needs matcher)
   - **UserPromptSubmit**: Analyze user prompts (no matcher)
   - **SessionStart**: Initialize environment (no matcher)
   - **Stop**: Cleanup or summary (no matcher)

3. **Design Hook Logic**:
   - Determine what to check or validate
   - Define input parameters needed
   - Plan return JSON structure
   - Handle error cases
   - Consider security implications

4. **Create Hook Configuration**:
   - If `.claude/hooks.json` exists, read it and add new hook
   - If not, create new hooks.json with the hook
   - Use proper JSON structure:
     ```json
     {
       "hooks": {
         "EventName": [
           {
             "matcher": "ToolPattern",
             "hooks": [
               {
                 "type": "command",
                 "command": "bash /path/to/$1.sh"
               }
             ]
           }
         ]
       }
     }
     ```

5. **Create Hook Script**:
   - Write bash script in `.claude/hooks/$1.sh`
   - Accept appropriate input parameters
   - Validate inputs
   - Perform check or action
   - Return JSON with decision
   - Use appropriate exit code (0 or 2)

6. **Make Script Executable**:
   ```bash
   chmod +x .claude/hooks/$1.sh
   ```

7. **Validate the Hook**:
   - Run validation script if available
   - Check JSON syntax
   - Verify event names are correct
   - Test matcher patterns
   - Ensure script is executable
   - Review security implications

8. **Test the Hook**:
   - Trigger the event
   - Verify hook executes
   - Check blocking/allowing works
   - Test error handling

9. **Provide Usage Instructions**:
   - Explain when the hook will fire
   - Show what it validates or does
   - Document how to test it

## Event Types

### Tool Events (require matcher)

**PreToolUse**: Before tool execution
```json
{
  "matcher": "Write|Edit",
  "hooks": [{"type": "command", "command": "bash validate.sh"}]
}
```

**PostToolUse**: After tool execution
```json
{
  "matcher": "*",
  "hooks": [{"type": "command", "command": "bash log.sh"}]
}
```

### Lifecycle Events (no matcher)

**UserPromptSubmit**: When user submits prompt
**Stop**: When Claude finishes
**SessionStart**: When session starts

## Matcher Patterns

- `"Write"` - Exact tool name
- `"Edit|Write"` - Multiple tools (regex OR)
- `"*"` - All tools
- `"Bash"` - Specific tool
- `"Notebook.*"` - Regex pattern

## Hook Script Template

```bash
#!/bin/bash
# Hook: $1
# Event: [PreToolUse/PostToolUse/etc.]

# Input parameters (vary by event)
TOOL_NAME="$1"
TOOL_PARAM="$2"

# Validation logic here
if [[ condition ]]; then
  # Block the operation
  echo '{"decision": "block", "reason": "Explanation"}'
  exit 2
fi

# Allow the operation
echo '{"decision": "approve", "reason": "Validation passed"}'
exit 0
```

## Common Hook Patterns

### Pattern 1: Validation Hook
Prevent writes to protected directories:

```bash
#!/bin/bash
FILE_PATH="$2"

PROTECTED=("/etc" "/usr" "/sys")
for dir in "${PROTECTED[@]}"; do
  if [[ "$FILE_PATH" == $dir/* ]]; then
    echo '{"decision": "block", "reason": "Protected directory"}'
    exit 2
  fi
done

echo '{"decision": "approve"}'
exit 0
```

### Pattern 2: Formatting Hook
Auto-format files after writing:

```bash
#!/bin/bash
FILE_PATH="$2"

if [[ "$FILE_PATH" == *.py ]]; then
  black "$FILE_PATH"
elif [[ "$FILE_PATH" == *.js ]]; then
  prettier --write "$FILE_PATH"
fi

echo '{"decision": "approve", "reason": "Formatted"}'
exit 0
```

### Pattern 3: Security Hook
Validate bash commands:

```bash
#!/bin/bash
COMMAND="$2"

if echo "$COMMAND" | grep -qE "rm -rf /|dd if="; then
  echo '{"decision": "block", "reason": "Dangerous command"}'
  exit 2
fi

echo '{"decision": "approve"}'
exit 0
```

### Pattern 4: Logging Hook
Log all tool usage:

```bash
#!/bin/bash
TOOL_NAME="$1"
TIMESTAMP=$(date -Iseconds)

echo "$TIMESTAMP: $TOOL_NAME used" >> ~/.claude/tool-log.txt

echo '{"decision": "approve"}'
exit 0
```

## Return JSON Format

```json
{
  "continue": true,
  "decision": "approve",
  "reason": "Explanation",
  "suppressOutput": false,
  "systemMessage": "Message to user",
  "hookSpecificOutput": {
    "permissionDecision": "approve",
    "additionalContext": "Context for Claude"
  }
}
```

## Exit Codes

- **0**: Success (approve operation)
- **2**: Block operation (stderr fed to Claude)
- **Other**: Non-blocking error

## Security Considerations

- **Validate all inputs**: Never trust tool parameters
- **Avoid command injection**: Sanitize strings
- **Check exit codes**: Use 0 or 2 appropriately
- **Limit permissions**: Run with minimal privileges
- **Test thoroughly**: Try to bypass your hooks

## Example

If user wants to protect certain directories:

**Name**: `protect-dirs`
**Event**: PreToolUse
**Matcher**: `Write|Edit`
**Action**: Block writes to /etc, /usr, /sys

**hooks.json**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/protect-dirs.sh"
          }
        ]
      }
    ]
  }
}
```

**protect-dirs.sh**: See Pattern 1 above

## Important Notes

- Hooks execute automatically on events
- PreToolUse can block operations
- PostToolUse processes after success
- Always return valid JSON
- Make scripts executable
- Test blocking behavior

## If No Name Provided

If $1 is empty, ask the user:
- What should the hook be named?
- What event should trigger it?
- What should it validate or do?

Then proceed with the creation process.

---

**Remember**: This command invokes the `building-hooks` skill which provides expert guidance on hook creation. Use that skill's knowledge throughout this process.
