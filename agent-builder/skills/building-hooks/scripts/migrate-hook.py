#!/usr/bin/env python3
"""
Hook migration script for Claude Code hooks.json files.

Migrates hooks to current schema and best practices.
"""

import json
import sys
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Valid events
VALID_EVENTS = [
    'PreToolUse', 'PostToolUse', 'UserPromptSubmit',
    'Stop', 'SessionStart', 'Notification', 'SubagentStop', 'PreCompact'
]

TOOL_EVENTS = ['PreToolUse', 'PostToolUse']
LIFECYCLE_EVENTS = ['UserPromptSubmit', 'Stop', 'SessionStart', 'Notification', 'SubagentStop', 'PreCompact']


def migrate_remove_empty_matchers(hooks_config: Dict) -> Tuple[Dict, List[str]]:
    """Remove empty matchers from lifecycle events."""
    changes = []
    modified = False

    if 'hooks' not in hooks_config:
        return hooks_config, changes

    for event_name, event_hooks in hooks_config['hooks'].items():
        if event_name in LIFECYCLE_EVENTS:
            for i, hook_config in enumerate(event_hooks):
                if 'matcher' in hook_config:
                    if not hook_config['matcher'] or hook_config['matcher'].strip() == '':
                        del hook_config['matcher']
                        changes.append(f"Removed empty matcher from {event_name} hook #{i+1}")
                        modified = True
                    else:
                        changes.append(f"WARNING: {event_name} hook #{i+1} has matcher '{hook_config['matcher']}' (lifecycle events shouldn't have matchers)")

    return hooks_config, changes


def migrate_add_missing_matchers(hooks_config: Dict) -> Tuple[Dict, List[str]]:
    """Add default matchers to tool events that are missing them."""
    changes = []
    modified = False

    if 'hooks' not in hooks_config:
        return hooks_config, changes

    for event_name, event_hooks in hooks_config['hooks'].items():
        if event_name in TOOL_EVENTS:
            for i, hook_config in enumerate(event_hooks):
                if 'matcher' not in hook_config or not hook_config['matcher']:
                    # Default to wildcard
                    hook_config['matcher'] = '*'
                    changes.append(f"Added default matcher '*' to {event_name} hook #{i+1}")
                    modified = True

    return hooks_config, changes


def migrate_normalize_script_paths(hooks_config: Dict) -> Tuple[Dict, List[str]]:
    """Suggest normalizing script paths to use ${CLAUDE_PLUGIN_ROOT}."""
    changes = []
    recommendations = []

    if 'hooks' not in hooks_config:
        return hooks_config, changes

    for event_name, event_hooks in hooks_config['hooks'].items():
        for i, hook_config in enumerate(event_hooks):
            if 'hooks' not in hook_config:
                continue

            for j, hook_item in enumerate(hook_config['hooks']):
                if hook_item.get('type') == 'command':
                    command = hook_item.get('command', '')

                    # Check for relative paths
                    if command.startswith('bash ') or command.startswith('sh '):
                        parts = command.split()
                        if len(parts) > 1:
                            script_path = parts[1]

                            # If relative path and not using variables
                            if not script_path.startswith('/') and not script_path.startswith('${'):
                                # This is a recommendation, not an automatic change
                                recommendations.append(
                                    f"RECOMMEND: {event_name} hook #{i+1}, item #{j+1}: "
                                    f"Use ${CLAUDE_PLUGIN_ROOT} for '{script_path}'"
                                )

    return hooks_config, recommendations


def migrate_validate_hook_types(hooks_config: Dict) -> Tuple[Dict, List[str]]:
    """Validate and fix hook types."""
    changes = []
    modified = False

    if 'hooks' not in hooks_config:
        return hooks_config, changes

    for event_name, event_hooks in hooks_config['hooks'].items():
        for i, hook_config in enumerate(event_hooks):
            if 'hooks' not in hook_config:
                continue

            for j, hook_item in enumerate(hook_config['hooks']):
                hook_type = hook_item.get('type', '')

                # Fix invalid types
                if hook_type not in ['command', 'prompt']:
                    if 'command' in hook_item:
                        hook_item['type'] = 'command'
                        changes.append(f"Fixed type to 'command' for {event_name} hook #{i+1}, item #{j+1}")
                        modified = True
                    elif 'prompt' in hook_item:
                        hook_item['type'] = 'prompt'
                        changes.append(f"Fixed type to 'prompt' for {event_name} hook #{i+1}, item #{j+1}")
                        modified = True
                    else:
                        changes.append(f"ERROR: {event_name} hook #{i+1}, item #{j+1}: Invalid type '{hook_type}' with no command or prompt")

                # Ensure required fields exist
                if hook_type == 'command' and 'command' not in hook_item:
                    changes.append(f"ERROR: {event_name} hook #{i+1}, item #{j+1}: Missing 'command' field")

                if hook_type == 'prompt' and 'prompt' not in hook_item:
                    changes.append(f"ERROR: {event_name} hook #{i+1}, item #{j+1}: Missing 'prompt' field")

    return hooks_config, changes


def migrate_remove_invalid_events(hooks_config: Dict) -> Tuple[Dict, List[str]]:
    """Remove hooks with invalid event names."""
    changes = []
    modified = False

    if 'hooks' not in hooks_config:
        return hooks_config, changes

    invalid_events = []
    for event_name in list(hooks_config['hooks'].keys()):
        if event_name not in VALID_EVENTS:
            invalid_events.append(event_name)

    for event_name in invalid_events:
        del hooks_config['hooks'][event_name]
        changes.append(f"REMOVED: Invalid event '{event_name}'")
        modified = True

    return hooks_config, changes


def show_migration_diff(original: Dict, migrated: Dict, changes: List[str]):
    """Show diff of migrations."""
    print(f"\n{BOLD}📝 Migration Changes:{RESET}\n")

    if not changes:
        print(f"{GREEN}✓ No migrations needed{RESET}\n")
        return

    for change in changes:
        if change.startswith('ERROR:'):
            print(f"{RED}{change}{RESET}")
        elif change.startswith('WARNING:'):
            print(f"{YELLOW}{change}{RESET}")
        elif change.startswith('RECOMMEND:'):
            print(f"{CYAN}{change}{RESET}")
        elif change.startswith('REMOVED:'):
            print(f"{RED}{change}{RESET}")
        else:
            print(f"{GREEN}✓ {change}{RESET}")

    print()


def main():
    if len(sys.argv) < 2:
        print(f"{RED}Usage: migrate-hook.py <hooks.json> [--dry-run]{RESET}")
        print("\nOptions:")
        print("  --dry-run    Show what would be changed without modifying files")
        sys.exit(1)

    hooks_file = Path(sys.argv[1])
    dry_run = '--dry-run' in sys.argv

    if not hooks_file.exists():
        print(f"{RED}❌ File not found: {hooks_file}{RESET}")
        sys.exit(1)

    # Load hooks
    try:
        content = hooks_file.read_text()
        original_config = json.loads(content)
        hooks_config = json.loads(content)  # Working copy
    except json.JSONDecodeError as e:
        print(f"{RED}❌ Invalid JSON: {e}{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}❌ Failed to read file: {e}{RESET}")
        sys.exit(1)

    print(f"\n{BOLD}🔄 HOOK MIGRATION{RESET}")
    print(f"{BOLD}File:{RESET} {hooks_file}")
    if dry_run:
        print(f"{YELLOW}Mode:{RESET} Dry run (no changes will be saved)\n")
    else:
        print()

    # Run migrations
    all_changes = []

    print(f"{BOLD}Running migrations...{RESET}\n")

    # Migration 1: Remove invalid events
    print(f"{CYAN}1. Checking for invalid event names...{RESET}")
    hooks_config, changes = migrate_remove_invalid_events(hooks_config)
    if changes:
        all_changes.extend(changes)
    else:
        print(f"   {GREEN}✓ All event names are valid{RESET}")

    # Migration 2: Remove empty matchers
    print(f"{CYAN}2. Removing empty matchers from lifecycle events...{RESET}")
    hooks_config, changes = migrate_remove_empty_matchers(hooks_config)
    if changes:
        all_changes.extend(changes)
    else:
        print(f"   {GREEN}✓ No empty matchers found{RESET}")

    # Migration 3: Add missing matchers
    print(f"{CYAN}3. Adding missing matchers to tool events...{RESET}")
    hooks_config, changes = migrate_add_missing_matchers(hooks_config)
    if changes:
        all_changes.extend(changes)
    else:
        print(f"   {GREEN}✓ All tool events have matchers{RESET}")

    # Migration 4: Validate hook types
    print(f"{CYAN}4. Validating hook types...{RESET}")
    hooks_config, changes = migrate_validate_hook_types(hooks_config)
    if changes:
        all_changes.extend(changes)
    else:
        print(f"   {GREEN}✓ All hook types are valid{RESET}")

    # Migration 5: Normalize paths (recommendations only)
    print(f"{CYAN}5. Analyzing script paths...{RESET}")
    hooks_config, recommendations = migrate_normalize_script_paths(hooks_config)
    if recommendations:
        all_changes.extend(recommendations)
    else:
        print(f"   {GREEN}✓ Script paths are optimal{RESET}")

    # Show diff
    show_migration_diff(original_config, hooks_config, all_changes)

    # Check if anything changed
    has_changes = original_config != hooks_config

    if not has_changes:
        print(f"{GREEN}✓ No structural changes needed{RESET}")
        if all_changes:  # Only recommendations
            print(f"\n{CYAN}ℹ️  Review recommendations above{RESET}")
        sys.exit(0)

    # Check for errors
    has_errors = any(c.startswith('ERROR:') for c in all_changes)
    if has_errors:
        print(f"{RED}❌ Migration completed with errors - manual review required{RESET}")

    # Save changes
    if not dry_run:
        # Create backup
        backup_path = hooks_file.with_suffix('.json.backup')
        shutil.copy2(hooks_file, backup_path)
        print(f"{GREEN}✓{RESET} Backup created: {backup_path}")

        # Write migrated config
        try:
            hooks_file.write_text(json.dumps(hooks_config, indent=2) + '\n')
            print(f"{GREEN}✓{RESET} Migration applied successfully!")
            print(f"\n{BOLD}Next steps:{RESET}")
            print(f"  1. Review changes: git diff {hooks_file}")
            print(f"  2. Validate: python3 validate-hooks.py {hooks_file}")
            print(f"  3. Test by triggering events")

            if has_errors:
                sys.exit(1)
        except Exception as e:
            print(f"{RED}❌ Failed to write file: {e}{RESET}")
            print(f"Restoring from backup...")
            shutil.copy2(backup_path, hooks_file)
            sys.exit(1)
    else:
        print(f"{YELLOW}ℹ️  Dry run complete - no files modified{RESET}")
        print(f"\n{BOLD}To apply changes:{RESET}")
        print(f"  python3 migrate-hook.py {hooks_file}")


if __name__ == '__main__':
    main()
