#!/usr/bin/env python3
"""
Update Command Script - Interactive command updater with diff preview
Part of the agent-builder plugin for Claude Code
"""

import sys
import os
import re
import yaml
import difflib
from pathlib import Path
from typing import Dict, List, Optional, Tuple

def find_command(command_name: str) -> Optional[Path]:
    """Find command file in common locations."""
    search_paths = [
        Path(".claude/commands"),
        Path.home() / ".claude" / "commands",
        Path("."),  # Search in current directory and subdirs
    ]

    for search_path in search_paths:
        if not search_path.exists():
            continue

        # Direct match
        command_file = search_path / f"{command_name}.md"
        if command_file.exists():
            return command_file

        # Search in subdirectories
        for command_file in search_path.rglob(f"{command_name}.md"):
            if command_file.parent.name == "commands":
                return command_file

    return None

def parse_command(file_path: Path) -> Tuple[Dict, str]:
    """Parse command file into frontmatter and body."""
    content = file_path.read_text()

    # Extract YAML frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        raise ValueError("Invalid command file: missing YAML frontmatter")

    frontmatter_text, body = match.groups()
    frontmatter = yaml.safe_load(frontmatter_text)

    return frontmatter, body

def validate_command_name(name: str) -> bool:
    """Validate command name follows conventions."""
    if not name:
        return False
    if len(name) > 64:
        return False
    if not re.match(r'^[a-z0-9-]+$', name):
        return False
    return True

def show_current_config(command_name: str, frontmatter: Dict, file_path: Path):
    """Display current command configuration."""
    print(f"\n{'='*60}")
    print(f"Current Configuration: {command_name}")
    print(f"{'='*60}")
    print(f"Location: {file_path}")
    print(f"Description: {frontmatter.get('description', 'N/A')}")
    print(f"Tools: {frontmatter.get('allowed-tools', 'inherit (all tools)')}")
    print(f"Model: {frontmatter.get('model', 'inherit')}")
    print(f"Argument Hint: {frontmatter.get('argument-hint', 'N/A')}")
    print(f"{'='*60}\n")

def interactive_menu() -> List[int]:
    """Show interactive update menu and get user choices."""
    print("What would you like to update?\n")
    options = [
        "Description (what the command does)",
        "Allowed Tools (pre-approved tool permissions)",
        "Model (version alias or full ID, e.g., claude-haiku-4-5)",
        "Argument Hint (parameter guide for users)",
        "Run validation and show recommendations",
        "Cancel (no changes)"
    ]

    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    print("\nEnter numbers (comma-separated) or 'all':")
    choice = input("> ").strip().lower()

    if choice == 'all':
        return list(range(1, len(options)))
    elif choice == str(len(options)) or choice == 'cancel':
        return []

    try:
        choices = [int(c.strip()) for c in choice.split(',')]
        return [c for c in choices if 1 <= c < len(options)]
    except ValueError:
        print("Invalid input. Please enter numbers separated by commas.")
        return []

def update_description(frontmatter: Dict) -> Dict:
    """Update command description."""
    print(f"\nCurrent description: {frontmatter.get('description', 'N/A')}")
    print("\nEnter new description (clear one-liner, max 200 chars):")
    new_desc = input("> ").strip()

    if len(new_desc) > 200:
        print("⚠️  Description too long, truncating to 200 characters")
        new_desc = new_desc[:200]

    if new_desc:
        frontmatter['description'] = new_desc
        print("✓ Description updated")

    return frontmatter

def update_allowed_tools(frontmatter: Dict) -> Dict:
    """Update command tool permissions."""
    current_tools = frontmatter.get('allowed-tools', 'inherit (all tools)')
    print(f"\nCurrent allowed-tools: {current_tools}")

    print("\nCommon tool presets:")
    print("1. Read, Grep, Glob (read-only, safest)")
    print("2. Read, Write, Edit, Grep, Glob (file modification)")
    print("3. Read, Write, Edit, Grep, Glob, Bash (full access)")
    print("4. Read, Grep, Glob, WebFetch, WebSearch (web access)")
    print("5. Custom (enter your own)")
    print("6. Inherit (remove allowed-tools field, use all)")

    choice = input("Select preset (1-6): ").strip()

    tool_presets = {
        '1': 'Read, Grep, Glob',
        '2': 'Read, Write, Edit, Grep, Glob',
        '3': 'Read, Write, Edit, Grep, Glob, Bash',
        '4': 'Read, Grep, Glob, WebFetch, WebSearch',
    }

    if choice in tool_presets:
        frontmatter['allowed-tools'] = tool_presets[choice]
        print(f"✓ Tools updated to: {tool_presets[choice]}")
    elif choice == '5':
        custom = input("Enter tools (comma-separated): ").strip()
        if custom:
            frontmatter['allowed-tools'] = custom
            print(f"✓ Tools updated to: {custom}")
    elif choice == '6':
        if 'allowed-tools' in frontmatter:
            del frontmatter['allowed-tools']
        print("✓ Tools set to inherit (all tools)")

    # Security warning
    if 'allowed-tools' in frontmatter and 'Bash' in frontmatter['allowed-tools']:
        print("⚠️  Security Warning: Bash access requires input validation!")

    return frontmatter

def update_model(frontmatter: Dict) -> Dict:
    """Update command model selection."""
    current_model = frontmatter.get('model', 'inherit')
    print(f"\nCurrent model: {current_model}")

    print("\n⚠️  IMPORTANT: Commands require VERSION ALIASES or FULL IDs (NOT short aliases)")
    print("\nModel options:")
    print("1. claude-haiku-4-5 (fastest, cheapest, simple tasks)")
    print("2. claude-sonnet-4-5 (balanced, default for most tasks)")
    print("3. claude-opus-4-5 (most capable, complex reasoning)")
    print("4. Custom version alias or full ID (e.g., claude-haiku-4-5-20251001)")
    print("5. inherit (remove model field, use parent conversation's model)")

    choice = input("Select model (1-5): ").strip()

    models = {
        '1': 'claude-haiku-4-5',
        '2': 'claude-sonnet-4-5',
        '3': 'claude-opus-4-5',
    }

    if choice in models:
        frontmatter['model'] = models[choice]
        print(f"✓ Model updated to: {models[choice]}")
    elif choice == '4':
        custom_model = input("Enter version alias or full model ID: ").strip()
        if custom_model:
            # Validate format
            if custom_model in ['haiku', 'sonnet', 'opus', 'inherit']:
                print("❌ ERROR: Commands cannot use short aliases!")
                print("   Use version aliases like 'claude-haiku-4-5' or full IDs like 'claude-haiku-4-5-20251001'")
            elif not custom_model.startswith('claude-'):
                print("⚠️  Warning: Model doesn't start with 'claude-', this may cause errors")
                confirm = input("Continue anyway? (y/n): ").strip().lower()
                if confirm == 'y':
                    frontmatter['model'] = custom_model
                    print(f"✓ Model updated to: {custom_model}")
            else:
                frontmatter['model'] = custom_model
                print(f"✓ Model updated to: {custom_model}")
    elif choice == '5':
        if 'model' in frontmatter:
            del frontmatter['model']
        print("✓ Model set to inherit")

    return frontmatter

def update_argument_hint(frontmatter: Dict, body: str) -> Dict:
    """Update command argument hint."""
    current_hint = frontmatter.get('argument-hint', 'N/A')
    print(f"\nCurrent argument-hint: {current_hint}")

    # Check if command uses arguments
    uses_positional = bool(re.search(r'\$\d+', body))
    uses_all_args = '$ARGUMENTS' in body

    if uses_positional or uses_all_args:
        print("\n✓ This command uses arguments:")
        if uses_positional:
            args_found = re.findall(r'\$(\d+)', body)
            print(f"  - Positional: ${', $'.join(sorted(set(args_found)))}")
        if uses_all_args:
            print("  - All arguments: $ARGUMENTS")
        print("\nRecommendation: Provide clear argument-hint in brackets")
        print("Example: [filename] [options]")
    else:
        print("\n⚠️  This command doesn't appear to use arguments")
        print("   argument-hint is optional for commands without parameters")

    print("\nEnter new argument-hint (or leave empty to keep current):")
    new_hint = input("> ").strip()

    if new_hint:
        # Ensure brackets
        if not new_hint.startswith('['):
            new_hint = f"[{new_hint}]"
        frontmatter['argument-hint'] = new_hint
        print(f"✓ Argument hint updated to: {new_hint}")
    elif new_hint == '' and current_hint == 'N/A':
        # User pressed enter with no current hint
        remove = input("Remove argument-hint field? (y/n): ").strip().lower()
        if remove == 'y':
            if 'argument-hint' in frontmatter:
                del frontmatter['argument-hint']
            print("✓ Argument hint removed")

    return frontmatter

def show_diff(original_content: str, new_content: str, file_path: Path):
    """Show diff of changes."""
    print(f"\n{'='*60}")
    print(f"Proposed Changes to {file_path.name}")
    print(f"{'='*60}\n")

    diff = difflib.unified_diff(
        original_content.splitlines(keepends=True),
        new_content.splitlines(keepends=True),
        fromfile=f"{file_path.name} (original)",
        tofile=f"{file_path.name} (updated)",
        lineterm=''
    )

    for line in diff:
        if line.startswith('+') and not line.startswith('+++'):
            print(f"\033[92m{line}\033[0m", end='')  # Green
        elif line.startswith('-') and not line.startswith('---'):
            print(f"\033[91m{line}\033[0m", end='')  # Red
        elif line.startswith('@@'):
            print(f"\033[94m{line}\033[0m", end='')  # Blue
        else:
            print(line, end='')

    print(f"\n{'='*60}\n")

def reconstruct_command(frontmatter: Dict, body: str) -> str:
    """Reconstruct command file from frontmatter and body."""
    yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    return f"---\n{yaml_str}---\n{body}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 update-command.py <command-name>")
        print("\nExample: python3 update-command.py new-agent")
        sys.exit(1)

    command_name = sys.argv[1].replace('.md', '')

    # Find command
    print(f"Searching for command: {command_name}...")
    command_path = find_command(command_name)

    if not command_path:
        print(f"❌ Command not found: {command_name}")
        print("\nSearched in:")
        print("  - .claude/commands/")
        print("  - ~/.claude/commands/")
        print("  - Plugin directories")
        sys.exit(1)

    print(f"✓ Found: {command_path}")

    # Parse command
    try:
        frontmatter, body = parse_command(command_path)
        original_content = command_path.read_text()
    except Exception as e:
        print(f"❌ Failed to parse command: {e}")
        sys.exit(1)

    # Show current config
    show_current_config(command_name, frontmatter, command_path)

    # Interactive menu
    choices = interactive_menu()

    if not choices:
        print("\n✓ No changes made")
        sys.exit(0)

    # Apply updates
    print("\n" + "="*60)
    print("Applying Updates")
    print("="*60)

    for choice in choices:
        if choice == 1:
            frontmatter = update_description(frontmatter)
        elif choice == 2:
            frontmatter = update_allowed_tools(frontmatter)
        elif choice == 3:
            frontmatter = update_model(frontmatter)
        elif choice == 4:
            frontmatter = update_argument_hint(frontmatter, body)
        elif choice == 5:
            # Run validation
            print("\nRunning validation...")
            os.system(f"python3 {Path(__file__).parent / 'validate-command.py'} {command_path}")

    # Reconstruct file
    new_content = reconstruct_command(frontmatter, body)

    # Show diff
    show_diff(original_content, new_content, command_path)

    # Confirm
    confirm = input("Apply these changes? (y/n): ").strip().lower()

    if confirm == 'y':
        # Backup original
        backup_path = command_path.with_suffix('.md.bak')
        command_path.rename(backup_path)

        # Write new content
        command_path.write_text(new_content)

        print(f"\n✅ Command updated successfully!")
        print(f"   Original backed up to: {backup_path}")
        print(f"   Updated file: {command_path}")

        # Run validation
        print("\n" + "="*60)
        print("Validation")
        print("="*60)
        os.system(f"python3 {Path(__file__).parent / 'validate-command.py'} {command_path}")
    else:
        print("\n✓ Changes cancelled")

if __name__ == '__main__':
    main()
