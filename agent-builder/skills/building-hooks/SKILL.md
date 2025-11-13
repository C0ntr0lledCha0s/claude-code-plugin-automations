---
name: building-hooks
description: Expert at creating and modifying Claude Code event hooks for automation and policy enforcement. Auto-invokes when the user wants to create, update, modify, enhance, or validate hooks, needs help with event-driven automation, or wants to understand hook patterns.
version: 1.1.0
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Building Hooks Skill

You are an expert at creating Claude Code event hooks. Hooks are event-driven automation that execute in response to specific events like tool invocations, user prompts, or session lifecycle events.

## When to Create Hooks

**Use HOOKS when:**
- You need event-driven automation
- You want to validate or block tool usage
- You need to enforce policies automatically
- You want to log or audit Claude's actions
- You need pre/post-processing for tool invocations

**Use COMMANDS instead when:**
- The user explicitly triggers an action
- You need manual invocation

**Use AGENTS/SKILLS instead when:**
- You need Claude's reasoning and generation
- The task requires LLM capabilities

## Hook Schema & Structure

### File Location
- **Project-level**: `.claude/hooks.json`
- **Project settings**: `.claude/settings.json` (hooks section)
- **Directory-specific**: `.claude-hooks.json` (in any directory)
- **Plugin-level**: `plugin-dir/hooks/hooks.json`

### File Format
JSON configuration file.

### Schema Structure

```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "bash command to execute"
          }
        ]
      }
    ]
  }
}
```

## Event Types

### Events WITH Matchers (Tool-Specific)

**PreToolUse**: Before a tool runs
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{"type": "command", "command": "bash validate.sh"}]
      }
    ]
  }
}
```

**PostToolUse**: After a tool completes successfully
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{"type": "command", "command": "bash format.sh"}]
      }
    ]
  }
}
```

### Events WITHOUT Matchers (Lifecycle Events)

**UserPromptSubmit**: When user submits a prompt
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [{"type": "command", "command": "bash log-prompt.sh"}]
      }
    ]
  }
}
```

**Stop**: When Claude finishes responding
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [{"type": "command", "command": "bash cleanup.sh"}]
      }
    ]
  }
}
```

**SessionStart**: When session starts
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [{"type": "command", "command": "bash setup.sh"}]
      }
    ]
  }
}
```

**Other Events**:
- **Notification**: When Claude sends an alert
- **SubagentStop**: When a subagent completes
- **PreCompact**: Before transcript compaction

## Matcher Patterns

For `PreToolUse` and `PostToolUse` events:

| Pattern | Matches | Example |
|---------|---------|---------|
| `"Write"` | Exact tool name | Matches only Write tool |
| `"Edit\|Write"` | Regex OR | Matches Edit or Write |
| `"Bash"` | Single tool | Matches Bash tool |
| `"*"` | Wildcard | Matches ALL tools |
| `"Notebook.*"` | Regex pattern | Matches NotebookEdit, etc. |
| `""` | Empty (for non-tool events) | For lifecycle events |

## Hook Types

### Type 1: Command Hook

Execute a bash command:

```json
{
  "type": "command",
  "command": "bash /path/to/script.sh"
}
```

**Use for:**
- Validation scripts
- Formatting tools
- Logging and auditing
- File system operations

### Type 2: Prompt Hook (LLM-based)

Use LLM for evaluation:

```json
{
  "type": "prompt",
  "prompt": "Analyze the tool usage and determine if it's safe"
}
```

**Use for:**
- Complex policy evaluation
- Context-aware decisions
- Natural language analysis

## Hook Return Values

Hooks can return structured JSON to control behavior:

```json
{
  "continue": true,
  "decision": "approve",
  "reason": "Explanation for the decision",
  "suppressOutput": false,
  "systemMessage": "Optional message shown to user",
  "hookSpecificOutput": {
    "permissionDecision": "approve",
    "permissionDecisionReason": "Safe operation",
    "additionalContext": "Extra context for Claude"
  }
}
```

### Key Fields

- **`continue`**: `true` to proceed, `false` to stop
- **`decision`**: `"approve"`, `"block"`, or `"warn"`
- **`reason`**: Explanation for the decision
- **`suppressOutput`**: Hide hook output from transcript
- **`systemMessage`**: Message displayed to user
- **`permissionDecision`**: For tool permission hooks
- **`additionalContext`**: Context added to Claude's knowledge

### Exit Codes

- **`0`**: Success (stdout shown in transcript mode)
- **`2`**: Blocking error (stderr fed to Claude)
- **Other**: Non-blocking error

## Common Hook Patterns

### Pattern 1: Validation Hook (PreToolUse)

Validate tool usage before execution:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/validate-write.sh"
          }
        ]
      }
    ]
  }
}
```

**Example validate-write.sh**:
```bash
#!/bin/bash
# Check if writing to protected directory

FILE_PATH="$1"

if [[ "$FILE_PATH" == /protected/* ]]; then
  echo '{"decision": "block", "reason": "Cannot write to protected directory"}'
  exit 2
fi

echo '{"decision": "approve", "reason": "Path is valid"}'
exit 0
```

### Pattern 2: Formatting Hook (PostToolUse)

Auto-format files after writing:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/format-file.sh"
          }
        ]
      }
    ]
  }
}
```

**Example format-file.sh**:
```bash
#!/bin/bash
FILE_PATH="$1"

if [[ "$FILE_PATH" == *.py ]]; then
  black "$FILE_PATH"
elif [[ "$FILE_PATH" == *.js ]]; then
  prettier --write "$FILE_PATH"
fi

exit 0
```

### Pattern 3: Logging Hook (All Tools)

Log all tool usage:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/log-tool.sh"
          }
        ]
      }
    ]
  }
}
```

### Pattern 4: Security Hook (Bash Commands)

Validate bash commands for security:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/validate-bash.sh"
          }
        ]
      }
    ]
  }
}
```

**Example validate-bash.sh**:
```bash
#!/bin/bash
COMMAND="$1"

# Block dangerous commands
if echo "$COMMAND" | grep -qE "rm -rf /|dd if="; then
  echo '{"decision": "block", "reason": "Dangerous command detected"}'
  exit 2
fi

echo '{"decision": "approve"}'
exit 0
```

### Pattern 5: Session Setup Hook

Initialize environment on session start:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/setup-session.sh"
          }
        ]
      }
    ]
  }
}
```

**Example setup-session.sh**:
```bash
#!/bin/bash
# Load environment, start services, etc.
export PROJECT_ROOT=$(pwd)
echo "Session initialized for project: $PROJECT_ROOT"
exit 0
```

## Creating Hooks

### Step 1: Identify the Need
Ask the user:
1. What event should trigger the hook?
2. What validation or action is needed?
3. Should it block, warn, or just log?
4. What tools or operations need monitoring?

### Step 2: Choose Event and Matcher
- **PreToolUse**: Validate before execution
- **PostToolUse**: Process after execution
- **UserPromptSubmit**: Analyze prompts
- **SessionStart**: Initialize environment
- **Stop**: Cleanup or summary

### Step 3: Design the Hook Logic
- Write bash script for the hook
- Define input parameters
- Plan return JSON structure
- Handle error cases
- Test security

### Step 4: Create hooks.json
```json
{
  "hooks": {
    "EventName": [
      {
        "matcher": "ToolPattern",
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/script.sh"
          }
        ]
      }
    ]
  }
}
```

### Step 5: Implement Hook Script
- Accept appropriate input parameters
- Validate inputs
- Perform check or action
- Return JSON with decision
- Use appropriate exit code

### Step 6: Test the Hook
- Place hooks.json in `.claude/`
- Trigger the event
- Verify hook executes correctly
- Check blocking/approving works
- Test error handling

## Generator Scripts

This skill includes a helper script to streamline hook creation:

### create-hook.py - Interactive Hook Generator

Full-featured interactive script that creates complete hook configuration and bash scripts.

**Usage:**
```bash
python3 {baseDir}/scripts/create-hook.py
```

**Features:**
- Interactive prompts for hook name, event type, matcher, purpose
- Event selection menu (PreToolUse, PostToolUse, UserPromptSubmit, Stop, etc.)
- Matcher pattern configuration for tool events
- Generates complete hooks.json entries
- Creates hook bash scripts with proper structure
- Automatic validation and setup
- Makes scripts executable

**Example Session:**
```
🪝 CLAUDE CODE HOOK GENERATOR
========================================

Hook name: validate-writes

📌 Hook Event Type
  1. PreToolUse   - Before a tool executes (needs matcher)
  2. PostToolUse  - After a tool completes (needs matcher)
  3. UserPromptSubmit - When user submits prompt
  4. Stop - When conversation ends
  5. SessionStart - When session begins
  ...
Select event [1]: 1

🎯 Tool Matcher
  1. Specific tool (e.g., 'Write', 'Bash')
  2. Multiple tools (e.g., 'Write|Edit')
  3. All tools ('*')
Select matcher type [1]: 2
Enter tools separated by | : Write|Edit

Hook purpose: Validate file writes for security

✅ Hook created successfully!

Files created:
  📄 .claude/hooks.json (updated)
  📜 .claude/scripts/validate-writes.sh

Hook configuration:
  Event: PreToolUse
  Matcher: Write|Edit
  Script: .claude/scripts/validate-writes.sh
```

**What It Creates:**

1. **hooks.json Entry** - Adds configuration to hooks.json:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate-writes.sh"
          }
        ]
      }
    ]
  }
}
```

2. **Hook Bash Script** - Complete template with:
   - Proper shebang and error handling (`set -euo pipefail`)
   - Logging function and log file setup
   - Input parameter documentation
   - Example validation functions (approve/block)
   - Placeholder for custom logic
   - Proper JSON return format

**Generated Script Structure:**
```bash
#!/usr/bin/env bash
#
# Hook: validate-writes
# Event: PreToolUse
# Purpose: Validate file writes for security
#

set -euo pipefail

# Configuration
HOOK_NAME="validate-writes"
LOG_FILE="${HOME}/.claude/hooks/validate-writes.log"

# Logging function
log_hook() {
    echo "[$(date -Iseconds)] $*" >> "${LOG_FILE}"
}

log_hook "=== Hook triggered ==="

# Input parameters for Tool events:
#   $1 = Tool name (e.g., "Write", "Bash")
#   $2 = Tool parameters (varies by tool)

TOOL_NAME="$1"
TOOL_PARAM="$2"

log_hook "Event: PreToolUse, Tool: ${TOOL_NAME}"

# TODO: Implement your hook logic here

# Example: Validation that approves operation
validate_operation() {
    # Add your validation logic

    # Return success (approve operation)
    echo '{"decision": "approve", "reason": "Validation passed"}'
    exit 0
}

# Main logic
validate_operation

# Exit successfully
exit 0
```

**When to Use:**
- Creating new event hooks
- Need guided configuration for event types
- Want proper hook structure with logging
- Building validation or policy enforcement

**After Creation:**
1. Edit the generated hook script
2. Implement your custom validation/processing logic
3. Test by triggering the event
4. Check logs in `~/.claude/hooks/{hook-name}.log`
5. Validate with standard validation tools
6. Iterate based on testing

**Event-Specific Behavior:**

The generator customizes the script based on the event:

- **PreToolUse/PostToolUse**: Includes tool name and parameters handling
- **UserPromptSubmit**: Includes prompt text handling
- **Stop/SessionStart**: Includes lifecycle event documentation
- **Others**: Generic event parameter handling

**Directory Structure Created:**
```
.claude/
├── hooks.json              # Updated with new hook entry
└── hooks/
    └── scripts/
        └── validate-writes.sh  # Executable hook script (755)
```

Or if using plugin structure:
```
plugin-dir/
└── hooks/
    ├── hooks.json          # Hook configuration
    └── scripts/
        └── hook-name.sh    # Hook script
```

## Hook Script Best Practices

### Input Parameters

Hooks receive context as arguments:

**PreToolUse / PostToolUse**:
- `$1`: Tool name
- `$2`: Tool parameters (JSON)
- Environment variables with tool details

**UserPromptSubmit**:
- `$1`: User prompt text

**Other events**:
- Event-specific parameters

### Return JSON Format

Always return well-formed JSON:

```bash
#!/bin/bash

# Success
echo '{"decision": "approve", "reason": "Validation passed"}'
exit 0

# Block
echo '{"decision": "block", "reason": "Security violation detected"}'
exit 2

# Warn
echo '{"decision": "warn", "reason": "Unusual pattern detected"}'
exit 0
```

### Error Handling

```bash
#!/bin/bash

if [ $# -lt 1 ]; then
  echo '{"decision": "block", "reason": "Missing required arguments"}' >&2
  exit 2
fi

# Validate input
if ! validate_input "$1"; then
  echo '{"decision": "block", "reason": "Invalid input"}' >&2
  exit 2
fi

# Normal processing
echo '{"decision": "approve"}'
exit 0
```

## Security Considerations

When creating hooks:

1. **Validate All Inputs**: Never trust data from tool parameters
2. **Avoid Command Injection**: Sanitize strings used in shell commands
3. **Check Exit Codes**: Use appropriate codes (0, 2)
4. **Limit Permissions**: Run with minimal necessary privileges
5. **Log Security Events**: Audit sensitive operations
6. **Test Thoroughly**: Try to bypass your own hooks

### Security Anti-Patterns

**Bad** (Command Injection):
```bash
eval "$1"  # NEVER DO THIS
```

**Good** (Safe Validation):
```bash
if [[ "$1" =~ ^[a-zA-Z0-9_/-]+$ ]]; then
  # Process sanitized input
fi
```

## Validation Checklist

Before deploying hooks, verify:

- [ ] hooks.json has valid JSON syntax
- [ ] Event names are correct
- [ ] Matchers are properly escaped (use \| for regex OR)
- [ ] Hook scripts exist and are executable
- [ ] Scripts accept correct input parameters
- [ ] Scripts return valid JSON
- [ ] Exit codes are appropriate (0 or 2)
- [ ] Security validation is thorough
- [ ] Error cases are handled
- [ ] Hooks don't create infinite loops

## Reference Templates

Full templates and examples are available at:
- `{baseDir}/templates/hooks-template.json` - Basic hooks configuration
- `{baseDir}/templates/validation-script.sh` - Validation hook script
- `{baseDir}/templates/formatting-script.sh` - Formatting hook script
- `{baseDir}/references/hook-examples.md` - Real-world examples

## Complete Example: Protected Directories

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
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/auto-format.sh"
          }
        ]
      }
    ]
  }
}
```

**protect-dirs.sh**:
```bash
#!/bin/bash
TOOL_NAME="$1"
FILE_PATH="$2"

PROTECTED_DIRS=("/etc" "/usr" "/sys" "/protected")

for dir in "${PROTECTED_DIRS[@]}"; do
  if [[ "$FILE_PATH" == $dir/* ]]; then
    echo "{\"decision\": \"block\", \"reason\": \"Cannot modify protected directory: $dir\"}"
    exit 2
  fi
done

echo '{"decision": "approve"}'
exit 0
```

**auto-format.sh**:
```bash
#!/bin/bash
FILE_PATH="$2"

if [[ "$FILE_PATH" == *.py ]]; then
  black --quiet "$FILE_PATH" 2>/dev/null
elif [[ "$FILE_PATH" == *.js ]] || [[ "$FILE_PATH" == *.ts ]]; then
  prettier --write "$FILE_PATH" > /dev/null 2>&1
fi

echo '{"decision": "approve", "reason": "File formatted"}'
exit 0
```

## Your Role

When the user asks to create hooks:

1. Understand what behavior needs automation or validation
2. Recommend appropriate event and matcher
3. Design hook logic with security in mind
4. Generate hooks.json configuration
5. Create hook scripts with proper structure
6. Validate JSON syntax and script logic
7. Make scripts executable
8. Provide testing instructions

Be proactive in:
- Identifying security risks
- Recommending appropriate events
- Creating robust validation logic
- Writing defensive hook scripts
- Testing edge cases and error conditions

Your goal is to help users create secure, reliable event hooks that automate workflows and enforce policies effectively.
