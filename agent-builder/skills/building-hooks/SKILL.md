---
name: building-hooks
description: Expert at creating and modifying Claude Code event hooks for automation and policy enforcement. Auto-invokes when the user wants to create, update, modify, enhance, validate, or standardize hooks, or when modifying hooks.json configuration, needs help with event-driven automation, or wants to understand hook patterns. Also auto-invokes proactively when Claude is about to write hooks.json files, or implement tasks that involve creating event hook configurations.
version: 1.3.0
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

## Maintaining and Updating Hooks

Once hooks are created, they require ongoing maintenance to ensure security, correctness, and effectiveness. This skill includes comprehensive tools for hook lifecycle management with a strong security focus.

### Maintenance Tools

All maintenance scripts are located in `{baseDir}/scripts/`:

#### 1. update-hook.py - Interactive Hook Updater

Interactive tool for modifying hook configuration with security validation.

**Usage:**
```bash
python3 {baseDir}/scripts/update-hook.py hooks.json
```

**Features:**
- Lists all hooks in hooks.json
- Interactive selection and modification
- Update event types, matchers, hook types, commands/prompts
- Security validation for dangerous patterns
- Regex validation for matchers
- Shows colored diff before applying
- Creates automatic backup

**When to Use:**
- Changing hook event types or matchers
- Updating hook commands or prompts
- Migrating hooks between events
- Security hardening existing hooks

**Security Checks:**
- Command injection patterns (eval, command substitution)
- Dangerous commands (rm -rf, dd, mkfs, etc.)
- Parameter usage without validation
- Relative vs absolute paths

**Slash Command:** `/agent-builder:hooks:update path/to/hooks.json`

#### 2. enhance-hook.py - Security-Focused Quality Analyzer

Comprehensive 7-category analysis with security priority.

**Usage:**
```bash
python3 {baseDir}/scripts/enhance-hook.py hooks.json
```

**Analysis Categories:**
1. **Schema Compliance** (0-10): JSON structure, event names, matcher requirements
2. **Security** (0-10) ⚠️ CRITICAL: Dangerous patterns, injection risks, validation
3. **Matcher Validity** (0-10): Regex patterns, appropriate wildcards
4. **Script Existence** (0-10): Referenced scripts exist and are executable
5. **Hook Types** (0-10): Valid types, required fields present
6. **Documentation** (0-10): Clarity, decision keywords
7. **Maintainability** (0-10): Hook count, duplicates, consistency

**Output:**
- Score for each category (0-10)
- Overall percentage and grade (A/B/C)
- Prioritized recommendations
- Critical security findings highlighted

**Exit Codes:**
- 0: No critical issues
- 1: Critical security issues found

**When to Use:**
- Pre-commit security audits
- Quality gates in PR reviews
- Identifying improvement opportunities
- Learning security best practices

**Slash Command:** `/agent-builder:hooks:enhance path/to/hooks.json`

#### 3. migrate-hook.py - Schema Migration Tool

Automated migrations for schema evolution and fixes.

**Usage:**
```bash
# Preview changes
python3 {baseDir}/scripts/migrate-hook.py hooks.json --dry-run

# Apply migrations
python3 {baseDir}/scripts/migrate-hook.py hooks.json
```

**Migrations:**
1. Remove invalid event names
2. Remove empty matchers from lifecycle events
3. Add missing matchers to tool events (defaults to '*')
4. Validate and fix hook types
5. Recommend ${CLAUDE_PLUGIN_ROOT} for relative paths

**Safety Features:**
- Automatic backup creation
- Dry-run mode for preview
- Error recovery (restores from backup on failure)
- Validation before saving

**When to Use:**
- Upgrading Claude Code versions
- Fixing validation errors
- Cleaning up deprecated patterns
- Preparing hooks for production

**Slash Command:** `/agent-builder:hooks:migrate path/to/hooks.json [--dry-run]`

#### 4. audit-hooks.py - Bulk Security Auditor

Repository-wide security audit of all hooks.json files.

**Usage:**
```bash
# Audit current directory
python3 {baseDir}/scripts/audit-hooks.py .

# Verbose output
python3 {baseDir}/scripts/audit-hooks.py . --verbose
```

**Features:**
- Finds all hooks.json files in directory tree
- Validates each file for security and schema
- Categorizes: Valid, Warnings, Errors, Parse Errors
- Summary report with counts
- Exit code 1 if errors found (CI/CD friendly)

**When to Use:**
- Repository-wide security audits
- CI/CD pipelines
- Pre-commit hooks
- Regular security reviews
- Onboarding inherited codebases

**Slash Command:** `/agent-builder:hooks:audit [directory] [--verbose]`

#### 5. compare-hooks.py - Hook Comparison Tool

Side-by-side comparison of hooks.json files.

**Usage:**
```bash
python3 {baseDir}/scripts/compare-hooks.py hooks1.json hooks2.json

# Detailed diff
python3 {baseDir}/scripts/compare-hooks.py hooks1.json hooks2.json --verbose
```

**Comparison Dimensions:**
- Structure (event counts, hook counts, types)
- Event-by-event hook counts
- Detailed line-by-line diff (verbose mode)
- Similarity percentage

**When to Use:**
- Version comparison (before/after updates)
- Migration validation
- Pull request reviews
- Merge conflict resolution
- Understanding changes between branches

**Slash Command:** `/agent-builder:hooks:compare hooks1.json hooks2.json [--verbose]`

### Common Maintenance Scenarios

#### Scenario 1: Adding Security to Existing Hook

**Context:** Existing Bash hook lacks input validation

**Steps:**
1. Analyze current security:
   ```bash
   python3 {baseDir}/scripts/enhance-hook.py hooks.json
   ```

2. Review security findings, note validation issues

3. Update hook to add validation:
   ```bash
   python3 {baseDir}/scripts/update-hook.py hooks.json
   # Select the hook
   # Update command to include validation script
   ```

4. Verify improvement:
   ```bash
   python3 {baseDir}/scripts/enhance-hook.py hooks.json
   # Security score should increase to ≥8/10
   ```

#### Scenario 2: Migrating Hook to Different Event

**Context:** Move validation from PostToolUse to PreToolUse

**Steps:**
1. Backup current state:
   ```bash
   cp hooks.json hooks.json.before
   ```

2. Update event type interactively:
   ```bash
   python3 {baseDir}/scripts/update-hook.py hooks.json
   # Select hook to migrate
   # Change event to PreToolUse
   # Verify/update matcher
   ```

3. Compare and validate:
   ```bash
   python3 {baseDir}/scripts/compare-hooks.py hooks.json.before hooks.json
   python3 {baseDir}/scripts/enhance-hook.py hooks.json
   ```

4. Test by triggering PreToolUse event

#### Scenario 3: Repository-Wide Security Audit

**Context:** Audit all hooks across multiple plugins

**Steps:**
1. Run bulk audit:
   ```bash
   python3 {baseDir}/scripts/audit-hooks.py . --verbose > audit-report.txt
   ```

2. For each file with errors, analyze:
   ```bash
   python3 {baseDir}/scripts/enhance-hook.py plugin/hooks/hooks.json
   ```

3. Fix critical issues:
   ```bash
   python3 {baseDir}/scripts/update-hook.py plugin/hooks/hooks.json
   # Address each critical finding
   ```

4. Apply automated migrations:
   ```bash
   python3 {baseDir}/scripts/migrate-hook.py plugin/hooks/hooks.json
   ```

5. Re-audit to verify:
   ```bash
   python3 {baseDir}/scripts/audit-hooks.py .
   ```

#### Scenario 4: Preparing for Production

**Context:** Ensure hooks meet production quality standards

**Steps:**
1. Run comprehensive analysis:
   ```bash
   python3 {baseDir}/scripts/enhance-hook.py hooks.json
   ```
   Target: Grade A (≥80%), Security ≥8/10

2. Apply migrations:
   ```bash
   python3 {baseDir}/scripts/migrate-hook.py hooks.json
   ```

3. Fix remaining issues interactively:
   ```bash
   python3 {baseDir}/scripts/update-hook.py hooks.json
   ```

4. Final validation:
   ```bash
   python3 {baseDir}/scripts/enhance-hook.py hooks.json
   python3 {baseDir}/scripts/validate-hooks.py hooks.json
   ```

5. Test all hooks by triggering events

6. Document any special considerations

### Security-First Maintenance

Hooks execute with privileges, making security paramount. Always prioritize security over convenience.

**Critical Security Principles:**

1. **Never Trust Input:** All parameters are potentially malicious
   ```bash
   # WRONG
   eval "$1"

   # RIGHT
   if [[ "$1" =~ ^[a-zA-Z0-9_/-]+$ ]]; then
       # Safe to use
   fi
   ```

2. **Validate Everything:** Check parameters, paths, commands
   ```bash
   set -euo pipefail  # Strict error handling
   [[ ! "$PATH" =~ \.\. ]]  # No directory traversal
   ```

3. **Use Safe Defaults:** Block by default, approve explicitly
   ```bash
   echo '{"decision": "block", "reason": "Validation failed"}' >&2
   exit 2
   ```

4. **Block Dangerous Patterns:**
   - `eval`, command substitution without validation
   - `rm -rf /`, `dd if=`, `mkfs`
   - Piping wget/curl to bash
   - Overly permissive permissions (chmod 777)

**Security Checklist Before Commit:**
- [ ] Run `enhance-hook.py` - no critical errors
- [ ] Security score ≥8/10
- [ ] All scripts exist and are executable
- [ ] Input validation present for all parameters
- [ ] No dangerous command patterns
- [ ] Matchers are valid regex
- [ ] Using ${CLAUDE_PLUGIN_ROOT} for paths
- [ ] Bash scripts use `set -euo pipefail`
- [ ] Tested by triggering events

### Best Practices

1. **Always Backup:** Maintenance tools create backups, but manual backups don't hurt
2. **Test Locally:** Trigger events to test hooks before committing
3. **Use Dry-Run:** Preview migrations before applying
4. **Validate Often:** Run enhance-hook.py frequently during development
5. **Review Diffs:** Always review changes before saving
6. **Security First:** When in doubt, block and investigate
7. **Document Changes:** Note why hooks were modified
8. **Version Control:** Commit hooks.json changes with clear messages
9. **Audit Regularly:** Run repository-wide audits monthly
10. **Update Incrementally:** Make small, tested changes

### Integration with Development Workflow

#### Pre-Commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

for file in $(git diff --cached --name-only | grep 'hooks.json'); do
    python3 agent-builder/skills/building-hooks/scripts/enhance-hook.py "$file"
    if [ $? -ne 0 ]; then
        echo "❌ Hook validation failed for $file"
        exit 1
    fi
done
```

#### CI/CD Pipeline
```yaml
# .github/workflows/validate.yml
- name: Audit Hooks
  run: |
    python3 agent-builder/skills/building-hooks/scripts/audit-hooks.py .
```

### Decision Matrix: Which Tool to Use?

| Goal | Tool | Command |
|------|------|---------|
| Fix specific hook | update-hook.py | `/agent-builder:hooks:update` |
| Security audit | enhance-hook.py | `/agent-builder:hooks:enhance` |
| Automated fixes | migrate-hook.py | `/agent-builder:hooks:migrate` |
| Repository scan | audit-hooks.py | `/agent-builder:hooks:audit` |
| Version comparison | compare-hooks.py | `/agent-builder:hooks:compare` |

### Reference Documentation

- **Maintenance Guide:** `{baseDir}/references/hook-maintenance-guide.md`
  Comprehensive security-focused maintenance guide with scenarios and troubleshooting

- **Security Checklist:** `{baseDir}/references/hook-checklist.md`
  Pre-commit, PR review, and production deployment checklists

### Your Role in Maintenance

When the user asks to maintain or update hooks:

1. **Assess the Need:**
   - What is being changed and why?
   - Are there security implications?
   - Is this a one-time fix or systematic issue?

2. **Choose the Right Tool:**
   - Specific hook: Use update-hook.py
   - Security audit: Use enhance-hook.py
   - Schema issues: Use migrate-hook.py
   - Multiple files: Use audit-hooks.py
   - Comparison: Use compare-hooks.py

3. **Prioritize Security:**
   - Always run security analysis first
   - Fix critical issues before other improvements
   - Validate dangerous patterns
   - Test thoroughly

4. **Validate Changes:**
   - Run enhance-hook.py after modifications
   - Use compare-hooks.py to review changes
   - Test by triggering events
   - Verify security score ≥8/10

5. **Document and Test:**
   - Note why changes were made
   - Test all affected events
   - Update documentation if needed
   - Commit with clear message

Be proactive in:
- Identifying security risks during maintenance
- Recommending security improvements
- Preventing regression in quality scores
- Ensuring hooks remain maintainable
- Educating users on security best practices

Remember: Hooks are security-critical infrastructure. Maintain them with the same rigor as production code.
