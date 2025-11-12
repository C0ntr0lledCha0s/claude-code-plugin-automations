#!/usr/bin/env python3
"""
Hook Generator Script
Creates Claude Code hook configuration and scripts
"""

import sys
import json
from pathlib import Path


def prompt_user(question, default=None, required=True):
    """Prompt user for input"""
    if default:
        prompt = f"{question} [{default}]: "
    else:
        prompt = f"{question}: "

    while True:
        response = input(prompt).strip()
        if not response and default:
            return default
        if not response and not required:
            return ""
        if response or not required:
            return response
        print("This field is required. Please provide a value.")


def select_event():
    """Select hook event type"""
    print("\n📌 Hook Event Type")
    print("  1. PreToolUse   - Before a tool executes (needs matcher)")
    print("  2. PostToolUse  - After a tool completes (needs matcher)")
    print("  3. UserPromptSubmit - When user submits prompt")
    print("  4. Stop - When conversation ends")
    print("  5. SessionStart - When session begins")
    print("  6. Notification - When Claude sends alert")
    print("  7. SubagentStop - When subagent completes")
    print("  8. PreCompact - Before transcript compaction")

    choice = prompt_user("Select event [1]", "1")

    event_map = {
        '1': 'PreToolUse',
        '2': 'PostToolUse',
        '3': 'UserPromptSubmit',
        '4': 'Stop',
        '5': 'SessionStart',
        '6': 'Notification',
        '7': 'SubagentStop',
        '8': 'PreCompact'
    }

    return event_map.get(choice, 'PreToolUse')


def select_matcher(event):
    """Select matcher pattern for tool events"""
    if event not in ['PreToolUse', 'PostToolUse']:
        return None

    print("\n🎯 Tool Matcher")
    print("  1. Specific tool (e.g., 'Write', 'Bash')")
    print("  2. Multiple tools (e.g., 'Write|Edit')")
    print("  3. All tools ('*')")

    choice = prompt_user("Select matcher type [1]", "1")

    if choice == '3':
        return "*"
    elif choice == '2':
        tools = prompt_user("Enter tools separated by | (e.g., 'Write|Edit')")
        return tools
    else:
        tool = prompt_user("Enter tool name (e.g., 'Write', 'Bash')", "Write")
        return tool


def generate_hook_script(hook_name, event, matcher, purpose):
    """Generate hook bash script"""

    if event in ['PreToolUse', 'PostToolUse']:
        input_section = """
# Input parameters for Tool events:
#   $1 = Tool name (e.g., "Write", "Bash")
#   $2 = Tool parameters (varies by tool)

TOOL_NAME="$1"
TOOL_PARAM="$2"

log_hook "Event: ${event}, Tool: ${TOOL_NAME}"
"""
    else:
        input_section = f"""
# Input parameters for {event} event
# (Check Claude Code documentation for specific parameters)

log_hook "Event: {event}"
"""

    return f'''#!/usr/bin/env bash
#
# Hook: {hook_name}
# Event: {event}
# Purpose: {purpose}
#

set -euo pipefail

# Configuration
HOOK_NAME="{hook_name}"
LOG_FILE="${{HOME}}/.claude/hooks/{hook_name}.log"

# Logging function
log_hook() {{
    echo "[$(date -Iseconds)] $*" >> "${{LOG_FILE}}"
}}

log_hook "=== Hook triggered ==="

{input_section}

# TODO: Implement your hook logic here

# Example: Validation that approves operation
validate_operation() {{
    # Add your validation logic

    # Return success (approve operation)
    echo '{{"decision": "approve", "reason": "Validation passed"}}'
    exit 0
}}

# Example: Validation that blocks operation
block_operation() {{
    # Add your blocking logic

    # Return error (block operation)
    echo '{{"decision": "block", "reason": "Validation failed"}}'
    exit 2
}}

# Main logic
# Customize based on your needs
validate_operation

# Exit successfully
exit 0
'''


def main():
    print("=" * 70)
    print("🪝 CLAUDE CODE HOOK GENERATOR")
    print("=" * 70)
    print()

    # Get hook name
    hook_name = prompt_user("Hook name (descriptive, e.g., 'validate-writes')")

    # Get event
    event = select_event()

    # Get matcher if needed
    matcher = select_matcher(event)

    # Get purpose
    purpose = prompt_user("Hook purpose (what does it do?)")

    # Determine directories
    hooks_dir = Path.cwd() / '.claude'
    if not hooks_dir.exists():
        hooks_dir = Path.cwd() / 'hooks'
        hooks_dir.mkdir(parents=True, exist_ok=True)

    scripts_dir = hooks_dir / 'scripts'
    scripts_dir.mkdir(parents=True, exist_ok=True)

    hooks_json = hooks_dir / 'hooks.json'

    # Load or create hooks.json
    if hooks_json.exists():
        with open(hooks_json) as f:
            config = json.load(f)
    else:
        config = {"hooks": {}}

    # Build hook configuration
    if event not in config["hooks"]:
        config["hooks"][event] = []

    hook_entry = {
        "hooks": [
            {
                "type": "command",
                "command": f"bash ${{CLAUDE_PLUGIN_ROOT}}/hooks/scripts/{hook_name}.sh"
            }
        ]
    }

    if matcher:
        hook_entry["matcher"] = matcher

    config["hooks"][event].append(hook_entry)

    # Save hooks.json
    with open(hooks_json, 'w') as f:
        json.dump(config, f, indent=2)

    # Generate hook script
    script_path = scripts_dir / f"{hook_name}.sh"
    script_content = generate_hook_script(hook_name, event, matcher, purpose)
    script_path.write_text(script_content)
    script_path.chmod(0o755)

    print("\n" + "=" * 70)
    print("✅ Hook created successfully!")
    print("=" * 70)
    print(f"\nFiles created:")
    print(f"  📄 {hooks_json} (updated)")
    print(f"  📜 {script_path}")
    print(f"\nHook configuration:")
    print(f"  Event: {event}")
    if matcher:
        print(f"  Matcher: {matcher}")
    print(f"  Script: {script_path}")
    print(f"\n📝 Next steps:")
    print(f"   1. Edit {script_path} and implement your logic")
    print(f"   2. Test the hook by triggering the {event} event")
    print(f"   3. Check logs: ~/.claude/hooks/{hook_name}.log")
    print(f"   4. Validate: python validate-hooks.py {hooks_json}")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
