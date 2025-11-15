#!/usr/bin/env python3
"""
Interactive hook updater for Claude Code hooks.json files.

Updates hook configurations with validation and security checks.
"""

import json
import sys
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Valid event names
VALID_EVENTS = [
    'PreToolUse',
    'PostToolUse',
    'UserPromptSubmit',
    'Stop',
    'SessionStart',
    'Notification',
    'SubagentStop',
    'PreCompact'
]

# Events that require matchers
TOOL_EVENTS = ['PreToolUse', 'PostToolUse']

# Events that should NOT have matchers
LIFECYCLE_EVENTS = [
    'UserPromptSubmit',
    'Stop',
    'SessionStart',
    'Notification',
    'SubagentStop',
    'PreCompact'
]


def load_hooks_json(file_path: Path) -> Tuple[Dict, str]:
    """Load hooks.json and return (data, error)."""
    try:
        content = file_path.read_text()
        data = json.loads(content)
        return data, ""
    except json.JSONDecodeError as e:
        return {}, f"Invalid JSON: {e}"
    except Exception as e:
        return {}, f"Failed to read file: {e}"


def list_all_hooks(hooks_config: Dict) -> List[Tuple[str, int, int, Dict]]:
    """
    List all hooks in the configuration.

    Returns list of tuples: (event_name, hook_config_index, hook_item_index, hook_data)
    """
    all_hooks = []

    if 'hooks' not in hooks_config:
        return all_hooks

    for event_name, event_hooks in hooks_config['hooks'].items():
        for i, hook_config in enumerate(event_hooks):
            if 'hooks' in hook_config:
                for j, hook_item in enumerate(hook_config['hooks']):
                    all_hooks.append((event_name, i, j, {
                        'event': event_name,
                        'matcher': hook_config.get('matcher', 'N/A'),
                        'type': hook_item.get('type', 'unknown'),
                        'command': hook_item.get('command', ''),
                        'prompt': hook_item.get('prompt', ''),
                        'hook_config': hook_config,
                        'hook_item': hook_item
                    }))

    return all_hooks


def print_hooks_list(hooks: List[Tuple[str, int, int, Dict]]):
    """Print formatted list of hooks."""
    print(f"\n{BOLD}📋 Available Hooks:{RESET}\n")

    for idx, (event, cfg_idx, item_idx, data) in enumerate(hooks, 1):
        hook_type = data['type']
        matcher = data['matcher']

        print(f"{CYAN}{idx}.{RESET} {BOLD}Event:{RESET} {event}")
        if matcher != 'N/A':
            print(f"   {BOLD}Matcher:{RESET} {matcher}")
        print(f"   {BOLD}Type:{RESET} {hook_type}")

        if hook_type == 'command':
            cmd = data['command'][:60] + '...' if len(data['command']) > 60 else data['command']
            print(f"   {BOLD}Command:{RESET} {cmd}")
        elif hook_type == 'prompt':
            prompt = data['prompt'][:60] + '...' if len(data['prompt']) > 60 else data['prompt']
            print(f"   {BOLD}Prompt:{RESET} {prompt}")

        print()


def validate_matcher(matcher: str) -> Tuple[bool, str]:
    """Validate matcher pattern."""
    if not matcher:
        return False, "Empty matcher (use '*' for all tools)"

    # Try to compile as regex
    try:
        re.compile(matcher)
        return True, ""
    except re.error as e:
        return False, f"Invalid regex: {e}"


def validate_event_name(event: str) -> Tuple[bool, str]:
    """Validate event name."""
    if event not in VALID_EVENTS:
        return False, f"Invalid event. Valid: {', '.join(VALID_EVENTS)}"
    return True, ""


def check_script_security(command: str) -> List[str]:
    """Check command for security issues."""
    warnings = []

    # Check for dangerous patterns
    dangerous_patterns = [
        (r'\$\(.*\)', 'Command substitution detected'),
        (r'`.*`', 'Backtick command execution detected'),
        (r'eval\s+', 'eval command detected (dangerous)'),
        (r'rm\s+-rf\s+/', 'Dangerous rm -rf command detected'),
        (r'>\s*/dev/', 'Writing to device files'),
    ]

    for pattern, message in dangerous_patterns:
        if re.search(pattern, command):
            warnings.append(message)

    return warnings


def update_event_type(current_event: str) -> str:
    """Interactive event type updater."""
    print(f"\n{BOLD}Update Event Type{RESET}")
    print(f"Current: {YELLOW}{current_event}{RESET}\n")

    print("Available events:")
    for i, event in enumerate(VALID_EVENTS, 1):
        marker = "✓ " if event == current_event else "  "
        print(f"{marker}{i}. {event}")

    print(f"\n{len(VALID_EVENTS) + 1}. Keep current")

    choice = input(f"\n{BOLD}Select event [1-{len(VALID_EVENTS) + 1}]:{RESET} ").strip()

    try:
        idx = int(choice)
        if 1 <= idx <= len(VALID_EVENTS):
            return VALID_EVENTS[idx - 1]
    except ValueError:
        pass

    return current_event


def update_matcher(current_matcher: str, event: str) -> str:
    """Interactive matcher updater."""
    if event in LIFECYCLE_EVENTS:
        if current_matcher and current_matcher != 'N/A':
            print(f"\n{YELLOW}⚠️  Lifecycle events should not have matchers.{RESET}")
            print("   Matcher will be removed.")
        return ''

    print(f"\n{BOLD}Update Matcher Pattern{RESET}")
    print(f"Current: {YELLOW}{current_matcher if current_matcher != 'N/A' else '(none)'}{RESET}\n")

    print("Examples:")
    print("  1. Specific tool:     Write")
    print("  2. Multiple tools:    Write|Edit")
    print("  3. All tools:         *")
    print("  4. Pattern:           Bash.*")
    print(f"\n  5. Keep current: {current_matcher if current_matcher != 'N/A' else '(none)'}")

    choice = input(f"\n{BOLD}Enter matcher (or 5 to keep):{RESET} ").strip()

    if choice == '5' or not choice:
        return current_matcher if current_matcher != 'N/A' else ''

    # Validate
    is_valid, error = validate_matcher(choice)
    if not is_valid:
        print(f"\n{RED}❌ {error}{RESET}")
        print("Keeping current matcher.")
        return current_matcher if current_matcher != 'N/A' else ''

    return choice


def update_hook_type(current_type: str) -> str:
    """Interactive hook type updater."""
    print(f"\n{BOLD}Update Hook Type{RESET}")
    print(f"Current: {YELLOW}{current_type}{RESET}\n")

    print("1. command - Execute bash command")
    print("2. prompt  - LLM-based evaluation")
    print("3. Keep current")

    choice = input(f"\n{BOLD}Select type [1-3]:{RESET} ").strip()

    if choice == '1':
        return 'command'
    elif choice == '2':
        return 'prompt'

    return current_type


def update_command(current_command: str) -> str:
    """Interactive command updater."""
    print(f"\n{BOLD}Update Command{RESET}")
    print(f"Current: {YELLOW}{current_command}{RESET}\n")

    print("Examples:")
    print("  bash /path/to/script.sh")
    print("  bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/validate.sh")

    new_command = input(f"\n{BOLD}Enter command (or press Enter to keep):{RESET} ").strip()

    if not new_command:
        return current_command

    # Security check
    warnings = check_script_security(new_command)
    if warnings:
        print(f"\n{YELLOW}⚠️  Security warnings:{RESET}")
        for warning in warnings:
            print(f"   - {warning}")

        confirm = input(f"\n{BOLD}Continue anyway? [y/N]:{RESET} ").strip().lower()
        if confirm != 'y':
            print("Keeping current command.")
            return current_command

    return new_command


def update_prompt(current_prompt: str) -> str:
    """Interactive prompt updater."""
    print(f"\n{BOLD}Update Prompt{RESET}")
    print(f"Current: {YELLOW}{current_prompt[:100]}{'...' if len(current_prompt) > 100 else ''}{RESET}\n")

    print("Enter new prompt (or press Enter to keep current):")
    new_prompt = input().strip()

    if not new_prompt:
        return current_prompt

    return new_prompt


def show_diff(old_hook: Dict, new_hook: Dict, event: str, matcher: str):
    """Show colored diff of changes."""
    print(f"\n{BOLD}📝 Changes Preview:{RESET}\n")

    print(f"{BOLD}Event:{RESET}")
    if old_hook.get('event') != event:
        print(f"{RED}- {old_hook.get('event')}{RESET}")
        print(f"{GREEN}+ {event}{RESET}")
    else:
        print(f"  {event} (unchanged)")

    if event in TOOL_EVENTS:
        print(f"\n{BOLD}Matcher:{RESET}")
        old_matcher = old_hook.get('matcher', 'N/A')
        if old_matcher != matcher:
            print(f"{RED}- {old_matcher}{RESET}")
            print(f"{GREEN}+ {matcher}{RESET}")
        else:
            print(f"  {matcher} (unchanged)")

    print(f"\n{BOLD}Type:{RESET}")
    if old_hook.get('type') != new_hook.get('type'):
        print(f"{RED}- {old_hook.get('type')}{RESET}")
        print(f"{GREEN}+ {new_hook.get('type')}{RESET}")
    else:
        print(f"  {new_hook.get('type')} (unchanged)")

    if new_hook.get('type') == 'command':
        print(f"\n{BOLD}Command:{RESET}")
        if old_hook.get('command') != new_hook.get('command'):
            print(f"{RED}- {old_hook.get('command', '')}{RESET}")
            print(f"{GREEN}+ {new_hook.get('command', '')}{RESET}")
        else:
            print(f"  {new_hook.get('command', '')} (unchanged)")

    if new_hook.get('type') == 'prompt':
        print(f"\n{BOLD}Prompt:{RESET}")
        old_prompt = old_hook.get('prompt', '')
        new_prompt = new_hook.get('prompt', '')
        if old_prompt != new_prompt:
            print(f"{RED}- {old_prompt[:60]}{'...' if len(old_prompt) > 60 else ''}{RESET}")
            print(f"{GREEN}+ {new_prompt[:60]}{'...' if len(new_prompt) > 60 else ''}{RESET}")
        else:
            print(f"  {new_prompt[:60]}{'...' if len(new_prompt) > 60 else ''} (unchanged)")


def main():
    if len(sys.argv) < 2:
        print(f"{RED}Usage: update-hook.py <hooks.json>{RESET}")
        sys.exit(1)

    hooks_file = Path(sys.argv[1])

    if not hooks_file.exists():
        print(f"{RED}❌ File not found: {hooks_file}{RESET}")
        sys.exit(1)

    # Load hooks.json
    hooks_config, error = load_hooks_json(hooks_file)
    if error:
        print(f"{RED}❌ {error}{RESET}")
        sys.exit(1)

    # List all hooks
    all_hooks = list_all_hooks(hooks_config)

    if not all_hooks:
        print(f"{YELLOW}⚠️  No hooks found in {hooks_file}{RESET}")
        sys.exit(0)

    # Display hooks
    print_hooks_list(all_hooks)

    # Select hook
    choice = input(f"{BOLD}Select hook to update [1-{len(all_hooks)}]:{RESET} ").strip()

    try:
        idx = int(choice) - 1
        if not (0 <= idx < len(all_hooks)):
            print(f"{RED}❌ Invalid selection{RESET}")
            sys.exit(1)
    except ValueError:
        print(f"{RED}❌ Invalid input{RESET}")
        sys.exit(1)

    event_name, cfg_idx, item_idx, hook_data = all_hooks[idx]

    # Interactive updates
    new_event = update_event_type(event_name)

    # Validate event change
    is_valid, error = validate_event_name(new_event)
    if not is_valid:
        print(f"{RED}❌ {error}{RESET}")
        sys.exit(1)

    # Update matcher if applicable
    new_matcher = update_matcher(hook_data['matcher'], new_event)

    # Update hook type
    new_type = update_hook_type(hook_data['type'])

    # Update command or prompt based on type
    new_hook_item = {'type': new_type}

    if new_type == 'command':
        new_hook_item['command'] = update_command(hook_data.get('command', ''))
    elif new_type == 'prompt':
        new_hook_item['prompt'] = update_prompt(hook_data.get('prompt', ''))

    # Show diff
    show_diff(hook_data, new_hook_item, new_event, new_matcher)

    # Confirm
    confirm = input(f"\n{BOLD}Apply changes? [y/N]:{RESET} ").strip().lower()
    if confirm != 'y':
        print(f"{YELLOW}❌ Changes cancelled{RESET}")
        sys.exit(0)

    # Create backup
    backup_path = hooks_file.with_suffix('.json.backup')
    shutil.copy2(hooks_file, backup_path)
    print(f"\n{GREEN}✓{RESET} Backup created: {backup_path}")

    # Apply changes
    # This is complex because we need to handle event changes
    if new_event != event_name:
        # Remove from old event
        old_event_hooks = hooks_config['hooks'][event_name]
        hook_config = old_event_hooks[cfg_idx]
        hook_config['hooks'].pop(item_idx)

        # Clean up if no more hooks
        if not hook_config['hooks']:
            old_event_hooks.pop(cfg_idx)
        if not old_event_hooks:
            del hooks_config['hooks'][event_name]

        # Add to new event
        if new_event not in hooks_config['hooks']:
            hooks_config['hooks'][new_event] = []

        new_hook_config = {}
        if new_event in TOOL_EVENTS and new_matcher:
            new_hook_config['matcher'] = new_matcher
        new_hook_config['hooks'] = [new_hook_item]

        hooks_config['hooks'][new_event].append(new_hook_config)
    else:
        # Update in place
        hook_config = hooks_config['hooks'][event_name][cfg_idx]
        if new_event in TOOL_EVENTS and new_matcher:
            hook_config['matcher'] = new_matcher
        elif new_event in LIFECYCLE_EVENTS and 'matcher' in hook_config:
            del hook_config['matcher']

        hook_config['hooks'][item_idx] = new_hook_item

    # Write back
    try:
        hooks_file.write_text(json.dumps(hooks_config, indent=2) + '\n')
        print(f"{GREEN}✓{RESET} Hook updated successfully!")
        print(f"\n{BOLD}Next steps:{RESET}")
        print(f"  1. Review changes: git diff {hooks_file}")
        print(f"  2. Validate: python3 validate-hooks.py {hooks_file}")
        print(f"  3. Test by triggering the event")
    except Exception as e:
        print(f"{RED}❌ Failed to write file: {e}{RESET}")
        print(f"Restoring from backup...")
        shutil.copy2(backup_path, hooks_file)
        sys.exit(1)


if __name__ == '__main__':
    main()
