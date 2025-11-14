#!/usr/bin/env python3
"""
Update Skill Script - Interactive skill updater with diff preview
Part of the agent-builder plugin for Claude Code

Handles directory-aware updates for skills (SKILL.md + subdirectories)
"""

import sys
import os
import re
import yaml
import difflib
from pathlib import Path
from typing import Dict, List, Optional, Tuple

def find_skill(skill_name: str) -> Optional[Path]:
    """Find skill directory in common locations."""
    search_paths = [
        Path(".claude/skills"),
        Path.home() / ".claude" / "skills",
        Path("."),  # Search in current directory and subdirs
    ]

    for search_path in search_paths:
        if not search_path.exists():
            continue

        # Direct match
        skill_dir = search_path / skill_name
        if skill_dir.exists() and skill_dir.is_dir():
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                return skill_dir

        # Search in subdirectories
        for skill_dir in search_path.rglob(skill_name):
            if skill_dir.is_dir() and skill_dir.parent.name == "skills":
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    return skill_dir

    return None

def parse_skill(skill_path: Path) -> Tuple[Dict, str]:
    """Parse SKILL.md file into frontmatter and body."""
    skill_md = skill_path / "SKILL.md"
    content = skill_md.read_text()

    # Extract YAML frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        raise ValueError("Invalid SKILL.md: missing YAML frontmatter")

    frontmatter_text, body = match.groups()
    frontmatter = yaml.safe_load(frontmatter_text)

    return frontmatter, body

def validate_skill_name(name: str) -> bool:
    """Validate skill name follows conventions."""
    if not name:
        return False
    if len(name) > 64:
        return False
    if not re.match(r'^[a-z0-9-]+$', name):
        return False
    return True

def show_current_config(skill_name: str, frontmatter: Dict, skill_path: Path):
    """Display current skill configuration."""
    print(f"\n{'='*60}")
    print(f"Current Configuration: {skill_name}")
    print(f"{'='*60}")
    print(f"Location: {skill_path}")
    print(f"Description: {frontmatter.get('description', 'N/A')}")
    print(f"Version: {frontmatter.get('version', 'N/A')}")
    print(f"Allowed Tools: {frontmatter.get('allowed-tools', 'none specified')}")

    # Show directory structure
    print(f"\nDirectory Structure:")
    subdirs = [d.name for d in skill_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
    if subdirs:
        for subdir in sorted(subdirs):
            count = len(list((skill_path / subdir).iterdir()))
            print(f"  - {subdir}/ ({count} items)")
    else:
        print("  (no subdirectories)")

    print(f"{'='*60}\n")

def interactive_menu() -> List[int]:
    """Show interactive update menu and get user choices."""
    print("What would you like to update?\n")
    options = [
        "Description (WHEN to invoke, purpose)",
        "Allowed Tools (pre-approved tool permissions)",
        "Version (semantic versioning)",
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
    """Update skill description."""
    print(f"\nCurrent description: {frontmatter.get('description', 'N/A')}")
    print("\nImportant: Skills descriptions should clearly state WHEN Claude should auto-invoke.")
    print("Example: 'Expert at X. Auto-invokes when user wants to Y or needs help with Z.'")
    print("\nEnter new description (max 1024 chars):")
    new_desc = input("> ").strip()

    if len(new_desc) > 1024:
        print("⚠️  Description too long, truncating to 1024 characters")
        new_desc = new_desc[:1024]

    if new_desc:
        frontmatter['description'] = new_desc
        print("✓ Description updated")

    return frontmatter

def update_allowed_tools(frontmatter: Dict) -> Dict:
    """Update skill tool permissions."""
    current_tools = frontmatter.get('allowed-tools', 'none specified')
    print(f"\nCurrent allowed-tools: {current_tools}")

    print("\nCommon tool presets:")
    print("1. Read, Grep, Glob (read-only, safest)")
    print("2. Read, Write, Edit, Grep, Glob (file modification)")
    print("3. Read, Write, Edit, Grep, Glob, Bash (full access)")
    print("4. Read, Grep, Glob, WebFetch, WebSearch (web access)")
    print("5. Custom (enter your own)")
    print("6. Remove (no pre-approved tools)")

    choice = input("Select preset (1-6): ").strip()

    tool_presets = {
        '1': 'Read, Grep, Glob',
        '2': 'Read, Write, Edit, Grep, Glob',
        '3': 'Read, Write, Edit, Grep, Glob, Bash',
        '4': 'Read, Grep, Glob, WebFetch, WebSearch',
    }

    if choice in tool_presets:
        frontmatter['allowed-tools'] = tool_presets[choice]
        print(f"✓ Allowed tools updated to: {tool_presets[choice]}")
    elif choice == '5':
        custom = input("Enter tools (comma-separated): ").strip()
        if custom:
            frontmatter['allowed-tools'] = custom
            print(f"✓ Allowed tools updated to: {custom}")
    elif choice == '6':
        if 'allowed-tools' in frontmatter:
            del frontmatter['allowed-tools']
        print("✓ Allowed tools removed (no pre-approval)")

    # Security warning
    if 'allowed-tools' in frontmatter and 'Bash' in frontmatter['allowed-tools']:
        print("⚠️  Security Warning: Bash access requires input validation!")

    return frontmatter

def update_version(frontmatter: Dict) -> Dict:
    """Update skill version."""
    current_version = frontmatter.get('version', 'N/A')
    print(f"\nCurrent version: {current_version}")

    print("\nEnter new version (semantic versioning: MAJOR.MINOR.PATCH):")
    print("Example: 1.2.0")
    new_version = input("> ").strip()

    if new_version:
        # Validate format
        if not re.match(r'^\d+\.\d+\.\d+$', new_version):
            print("⚠️  Warning: Version doesn't follow semantic versioning format (e.g., 1.0.0)")
            confirm = input("Use anyway? (y/n): ").strip().lower()
            if confirm != 'y':
                return frontmatter

        frontmatter['version'] = new_version
        print(f"✓ Version updated to: {new_version}")

    return frontmatter

def show_diff(original_content: str, new_content: str, file_name: str):
    """Show diff of changes."""
    print(f"\n{'='*60}")
    print(f"Proposed Changes to {file_name}")
    print(f"{'='*60}\n")

    diff = difflib.unified_diff(
        original_content.splitlines(keepends=True),
        new_content.splitlines(keepends=True),
        fromfile=f"{file_name} (original)",
        tofile=f"{file_name} (updated)",
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

def reconstruct_skill(frontmatter: Dict, body: str) -> str:
    """Reconstruct SKILL.md file from frontmatter and body."""
    yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    return f"---\n{yaml_str}---\n{body}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 update-skill.py <skill-name>")
        print("\nExample: python3 update-skill.py building-commands")
        sys.exit(1)

    skill_name = sys.argv[1]

    # Find skill
    print(f"Searching for skill: {skill_name}...")
    skill_path = find_skill(skill_name)

    if not skill_path:
        print(f"❌ Skill not found: {skill_name}")
        print("\nSearched in:")
        print("  - .claude/skills/")
        print("  - ~/.claude/skills/")
        print("  - Plugin directories")
        sys.exit(1)

    print(f"✓ Found: {skill_path}")

    # Parse skill
    try:
        frontmatter, body = parse_skill(skill_path)
        skill_md = skill_path / "SKILL.md"
        original_content = skill_md.read_text()
    except Exception as e:
        print(f"❌ Failed to parse skill: {e}")
        sys.exit(1)

    # Show current config
    show_current_config(skill_name, frontmatter, skill_path)

    # Check for model field (CRITICAL ERROR for skills)
    if 'model' in frontmatter:
        print("❌ CRITICAL ERROR: Skills cannot have a 'model' field!")
        print("   Only agents support model specification.")
        print("   This field must be removed before updating.")
        print(f"\n   Run migration script: python3 migrate-skill.py {skill_name}")
        sys.exit(1)

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
            frontmatter = update_version(frontmatter)
        elif choice == 4:
            # Run validation
            print("\nRunning validation...")
            os.system(f"python3 {Path(__file__).parent / 'validate-skill.py'} {skill_path}")

    # Reconstruct file
    new_content = reconstruct_skill(frontmatter, body)

    # Show diff
    show_diff(original_content, new_content, "SKILL.md")

    # Confirm
    confirm = input("Apply these changes? (y/n): ").strip().lower()

    if confirm == 'y':
        # Backup original
        backup_path = skill_md.with_suffix('.md.bak')
        skill_md.rename(backup_path)

        # Write new content
        skill_md.write_text(new_content)

        print(f"\n✅ Skill updated successfully!")
        print(f"   Original backed up to: {backup_path}")
        print(f"   Updated file: {skill_md}")

        # Run validation
        print("\n" + "="*60)
        print("Validation")
        print("="*60)
        os.system(f"python3 {Path(__file__).parent / 'validate-skill.py'} {skill_path}")
    else:
        print("\n✓ Changes cancelled")

if __name__ == '__main__':
    main()
