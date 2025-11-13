#!/usr/bin/env python3
"""
Migrate Command Script - Automated schema migration for commands
Part of the agent-builder plugin for Claude Code

Handles migrations like:
- model: haiku → model: claude-haiku-4-5 (short alias to version alias)
- model: sonnet → model: claude-sonnet-4-5
- model: opus → model: claude-opus-4-5
- Removing invalid short aliases
- Field renames and additions
"""

import sys
import re
import yaml
import difflib
from pathlib import Path
from typing import Dict, Tuple, List

def find_all_commands(directory: Path = None) -> List[Path]:
    """Find all command files in directory tree."""
    if directory is None:
        directory = Path(".")

    command_files = []

    # Search common locations
    search_paths = [
        directory / ".claude" / "commands",
        directory / "commands",
    ]

    # Also search plugin directories
    for plugin_dir in directory.glob("*/commands"):
        search_paths.append(plugin_dir)

    for search_path in search_paths:
        if search_path.exists():
            command_files.extend(search_path.glob("*.md"))
            # Include subdirectories (namespaced commands)
            command_files.extend(search_path.glob("*/*.md"))

    return sorted(set(command_files))

def parse_command(file_path: Path) -> Tuple[Dict, str]:
    """Parse command file into frontmatter and body."""
    content = file_path.read_text()

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        raise ValueError("Invalid command file: missing YAML frontmatter")

    frontmatter_text, body = match.groups()
    frontmatter = yaml.safe_load(frontmatter_text)

    return frontmatter, body

def migrate_short_alias_to_version_alias(frontmatter: Dict) -> Tuple[Dict, List[str]]:
    """
    Migrate short aliases (haiku/sonnet/opus) to version aliases.

    This is the most common migration needed for commands.
    """
    changes = []

    if 'model' not in frontmatter:
        return frontmatter, changes

    model = frontmatter['model']

    # Map short aliases to version aliases
    alias_map = {
        'haiku': 'claude-haiku-4-5',
        'sonnet': 'claude-sonnet-4-5',
        'opus': 'claude-opus-4-5',
    }

    if model in alias_map:
        old_value = model
        new_value = alias_map[model]
        frontmatter['model'] = new_value
        changes.append(f"Migrated model: '{old_value}' → '{new_value}'")

    # Remove 'inherit' value (just delete the field)
    elif model == 'inherit':
        del frontmatter['model']
        changes.append("Removed model: 'inherit' (use field omission instead)")

    return frontmatter, changes

def migrate_argument_hint_format(frontmatter: Dict) -> Tuple[Dict, List[str]]:
    """
    Ensure argument-hint uses bracket notation.
    """
    changes = []

    if 'argument-hint' not in frontmatter:
        return frontmatter, changes

    hint = frontmatter['argument-hint']

    # Handle YAML list (convert to string)
    if isinstance(hint, list):
        hint_str = ' '.join(str(item) for item in hint)
        frontmatter['argument-hint'] = hint_str
        changes.append(f"Converted argument-hint from list to string: {hint_str}")
        hint = hint_str

    # Ensure brackets
    if not str(hint).startswith('['):
        old_value = hint
        new_value = f"[{hint}]"
        frontmatter['argument-hint'] = new_value
        changes.append(f"Added brackets to argument-hint: '{old_value}' → '{new_value}'")

    return frontmatter, changes

def migrate_tools_field_name(frontmatter: Dict) -> Tuple[Dict, List[str]]:
    """
    Migrate old 'tools' field to 'allowed-tools' if needed.
    """
    changes = []

    if 'tools' in frontmatter and 'allowed-tools' not in frontmatter:
        frontmatter['allowed-tools'] = frontmatter['tools']
        del frontmatter['tools']
        changes.append("Renamed field: 'tools' → 'allowed-tools'")

    return frontmatter, changes

def apply_all_migrations(frontmatter: Dict) -> Tuple[Dict, List[str]]:
    """Apply all available migrations."""
    all_changes = []

    # Migration 1: Short alias to version alias (most important)
    frontmatter, changes = migrate_short_alias_to_version_alias(frontmatter)
    all_changes.extend(changes)

    # Migration 2: Argument hint format
    frontmatter, changes = migrate_argument_hint_format(frontmatter)
    all_changes.extend(changes)

    # Migration 3: Tools field rename (if needed in future)
    frontmatter, changes = migrate_tools_field_name(frontmatter)
    all_changes.extend(changes)

    return frontmatter, all_changes

def reconstruct_command(frontmatter: Dict, body: str) -> str:
    """Reconstruct command file from frontmatter and body."""
    yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    return f"---\n{yaml_str}---\n{body}"

def show_diff(original_content: str, new_content: str, file_path: Path):
    """Show diff of changes."""
    print(f"\n{'='*60}")
    print(f"Proposed Changes: {file_path.name}")
    print(f"{'='*60}\n")

    diff = difflib.unified_diff(
        original_content.splitlines(keepends=True),
        new_content.splitlines(keepends=True),
        fromfile=f"{file_path.name} (original)",
        tofile=f"{file_path.name} (migrated)",
        lineterm=''
    )

    has_diff = False
    for line in diff:
        has_diff = True
        if line.startswith('+') and not line.startswith('+++'):
            print(f"\033[92m{line}\033[0m", end='')  # Green
        elif line.startswith('-') and not line.startswith('---'):
            print(f"\033[91m{line}\033[0m", end='')  # Red
        elif line.startswith('@@'):
            print(f"\033[94m{line}\033[0m", end='')  # Blue
        else:
            print(line, end='')

    if not has_diff:
        print("(no changes)")

    print(f"\n{'='*60}\n")

def migrate_single_command(file_path: Path, dry_run: bool = True) -> Tuple[bool, List[str]]:
    """
    Migrate a single command file.

    Returns:
        (needs_migration, changes_list)
    """
    try:
        frontmatter, body = parse_command(file_path)
        original_content = file_path.read_text()
    except Exception as e:
        print(f"❌ Failed to parse {file_path.name}: {e}")
        return False, []

    # Apply migrations
    new_frontmatter, changes = apply_all_migrations(frontmatter)

    if not changes:
        return False, []

    # Reconstruct file
    new_content = reconstruct_command(new_frontmatter, body)

    # Show what would change
    print(f"\n{'='*60}")
    print(f"Migration: {file_path.name}")
    print(f"{'='*60}")
    print(f"Location: {file_path}")
    print(f"\nChanges:")
    for change in changes:
        print(f"  • {change}")

    if not dry_run:
        # Show diff
        show_diff(original_content, new_content, file_path)

        # Confirm
        confirm = input("\nApply migration? (y/n): ").strip().lower()

        if confirm == 'y':
            # Backup original
            backup_path = file_path.with_suffix('.md.bak')
            file_path.rename(backup_path)

            # Write new content
            file_path.write_text(new_content)

            print(f"✅ Migrated successfully!")
            print(f"   Backup: {backup_path}")
            return True, changes
        else:
            print("⏭️  Skipped")
            return False, []
    else:
        print("(dry-run mode, no changes applied)")
        return True, changes

def main():
    """
    Usage:
        python3 migrate-command.py --dry-run              # Preview all migrations
        python3 migrate-command.py --apply                 # Apply all migrations
        python3 migrate-command.py <command-name>          # Migrate single command
        python3 migrate-command.py <command-name> --apply  # Apply single migration
    """
    if len(sys.argv) < 2:
        print("Command Migration Tool")
        print("="*60)
        print("\nUsage:")
        print("  python3 migrate-command.py --dry-run              # Preview all")
        print("  python3 migrate-command.py --apply                 # Apply all")
        print("  python3 migrate-command.py <command-name>          # Preview one")
        print("  python3 migrate-command.py <command-name> --apply  # Apply one")
        print("\nMigrations:")
        print("  • Short aliases (haiku/sonnet/opus) → version aliases")
        print("  • argument-hint format standardization")
        print("  • Field renames and deprecations")
        sys.exit(1)

    arg1 = sys.argv[1]
    dry_run = True
    specific_command = None

    # Parse arguments
    if arg1 == '--dry-run':
        dry_run = True
    elif arg1 == '--apply':
        dry_run = False
    else:
        # Specific command
        specific_command = arg1.replace('.md', '')
        if len(sys.argv) > 2 and sys.argv[2] == '--apply':
            dry_run = False

    print("="*60)
    print("Command Migration Tool")
    print("="*60)
    print(f"Mode: {'Dry-run (preview only)' if dry_run else 'Apply changes'}\n")

    # Single command migration
    if specific_command:
        from pathlib import Path

        # Find command
        command_path = None
        search_paths = [
            Path(".claude/commands"),
            Path.home() / ".claude" / "commands",
            Path("."),
        ]

        for search_path in search_paths:
            if not search_path.exists():
                continue

            candidate = search_path / f"{specific_command}.md"
            if candidate.exists():
                command_path = candidate
                break

            for candidate in search_path.rglob(f"{specific_command}.md"):
                if candidate.parent.name == "commands":
                    command_path = candidate
                    break

        if not command_path:
            print(f"❌ Command not found: {specific_command}")
            sys.exit(1)

        needs_migration, changes = migrate_single_command(command_path, dry_run)

        if not needs_migration:
            print(f"\n✅ Command '{specific_command}' is already up-to-date!")
        elif dry_run:
            print(f"\n💡 Run with --apply to apply these migrations")

        sys.exit(0)

    # Bulk migration
    command_files = find_all_commands()

    if not command_files:
        print("No command files found")
        sys.exit(0)

    print(f"Found {len(command_files)} command files\n")

    migrated_count = 0
    skipped_count = 0

    for command_file in command_files:
        needs_migration, changes = migrate_single_command(command_file, dry_run=True)

        if needs_migration:
            migrated_count += 1
            if not dry_run:
                # Apply migration interactively
                migrate_single_command(command_file, dry_run=False)
        else:
            skipped_count += 1

    # Summary
    print("\n" + "="*60)
    print("Migration Summary")
    print("="*60)
    print(f"Total commands: {len(command_files)}")
    print(f"Need migration: {migrated_count}")
    print(f"Already up-to-date: {skipped_count}")

    if dry_run and migrated_count > 0:
        print(f"\n💡 Run with --apply to apply migrations")

if __name__ == '__main__':
    main()
