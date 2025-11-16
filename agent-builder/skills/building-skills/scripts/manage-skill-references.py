#!/usr/bin/env python3
"""
Manage Skill References Script - Reference documentation manager
Part of the agent-builder plugin for Claude Code

Manage reference files in a skill's references/ directory.
"""

import sys
import re
from pathlib import Path
from typing import Optional

def find_skill(skill_name: str) -> Optional[Path]:
    """Find skill directory in common locations."""
    search_paths = [
        Path(".claude/skills"),
        Path.home() / ".claude" / "skills",
        Path("."),
    ]

    for search_path in search_paths:
        if not search_path.exists():
            continue

        skill_dir = search_path / skill_name
        if skill_dir.exists() and skill_dir.is_dir():
            if (skill_dir / "SKILL.md").exists():
                return skill_dir

        for skill_dir in search_path.rglob(skill_name):
            if skill_dir.is_dir() and skill_dir.parent.name == "skills":
                if (skill_dir / "SKILL.md").exists():
                    return skill_dir

    return None

def ensure_references_dir(skill_dir: Path) -> Path:
    """Ensure references/ directory exists."""
    references_dir = skill_dir / "references"
    references_dir.mkdir(exist_ok=True)
    return references_dir

def list_references(skill_dir: Path):
    """List all reference files."""
    references_dir = skill_dir / "references"

    print("\n" + "="*70)
    print(f"Reference Files for '{skill_dir.name}'")
    print("="*70)

    if not references_dir.exists():
        print("\n⚠️  No references/ directory found")
        print(f"\nCreate with: mkdir {references_dir}")
        return

    reference_files = sorted(references_dir.glob("*.md"))

    if not reference_files:
        print("\n📁 references/ directory is empty")
        print("\nAdd a reference with:")
        print(f"  /agent-builder:skills:update-references {skill_dir.name} add <filename.md>")
        return

    print(f"\nFound {len(reference_files)} reference file(s):\n")

    for ref_file in reference_files:
        # Try to extract title from first heading
        try:
            content = ref_file.read_text()
            title_match = re.match(r'^#\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else "(no title)"
        except:
            title = "(error reading file)"

        print(f"  📄 {ref_file.name}")
        print(f"     {title}")
        print()

    print("\nTo reference in SKILL.md:")
    print(f"  - [{{baseDir}}/references/{reference_files[0].name}]")
    print()

def add_reference(skill_dir: Path, filename: str):
    """Add a new reference file."""
    references_dir = ensure_references_dir(skill_dir)

    # Validate filename
    if not filename.endswith('.md'):
        filename += '.md'

    if not re.match(r'^[a-z0-9-]+\.md$', filename):
        print("\n❌ Invalid filename. Use lowercase-hyphens only (e.g., 'my-guide.md')")
        sys.exit(1)

    ref_file = references_dir / filename

    if ref_file.exists():
        print(f"\n❌ File already exists: {filename}")
        print(f"\nUse 'update' action to modify existing file:")
        print(f"  /agent-builder:skills:update-references {skill_dir.name} update {filename}")
        sys.exit(1)

    # Prompt for title
    title = input("\nReference title: ").strip()
    if not title:
        print("❌ Title cannot be empty")
        sys.exit(1)

    # Create template content
    content = f"""# {title}

Quick reference for {skill_dir.name} skill.

---

## Overview

[Brief description of what this reference covers]

## Content

[Main reference content goes here]

## Examples

[Provide examples if applicable]

## Related

- [Other relevant references]

---

**Note**: This file is referenced in SKILL.md using `{{baseDir}}/references/{filename}`
"""

    # Write file
    ref_file.write_text(content)

    print(f"\n✅ Created: {filename}")
    print(f"   Location: {ref_file}")
    print(f"\n💡 Next steps:")
    print(f"   1. Edit the file: {ref_file}")
    print(f"   2. Add to SKILL.md:")
    print(f"      - [{{baseDir}}/references/{filename}] - {title}")
    print()

def remove_reference(skill_dir: Path, filename: str):
    """Remove a reference file."""
    references_dir = skill_dir / "references"

    if not references_dir.exists():
        print("\n❌ No references/ directory found")
        sys.exit(1)

    if not filename.endswith('.md'):
        filename += '.md'

    ref_file = references_dir / filename

    if not ref_file.exists():
        print(f"\n❌ File not found: {filename}")
        list_references(skill_dir)
        sys.exit(1)

    # Confirm deletion
    print(f"\n⚠️  About to delete: {filename}")
    print(f"   Location: {ref_file}")

    confirm = input("\nType 'yes' to confirm deletion: ").strip().lower()

    if confirm != 'yes':
        print("\n❌ Deletion cancelled")
        sys.exit(0)

    # Delete file
    ref_file.unlink()

    print(f"\n✅ Deleted: {filename}")
    print(f"\n💡 Remember to remove references to this file from SKILL.md")
    print()

def update_reference(skill_dir: Path, filename: str):
    """Update an existing reference file."""
    references_dir = skill_dir / "references"

    if not references_dir.exists():
        print("\n❌ No references/ directory found")
        sys.exit(1)

    if not filename.endswith('.md'):
        filename += '.md'

    ref_file = references_dir / filename

    if not ref_file.exists():
        print(f"\n❌ File not found: {filename}")
        list_references(skill_dir)
        sys.exit(1)

    print(f"\n📝 Edit this file: {ref_file}")
    print(f"\nUse your preferred editor to make changes.")
    print()

def validate_references(skill_dir: Path):
    """Validate reference files."""
    references_dir = skill_dir / "references"

    if not references_dir.exists():
        print("\n⚠️  No references/ directory found")
        return

    reference_files = list(references_dir.glob("*.md"))

    if not reference_files:
        print("\n⚠️  No reference files to validate")
        return

    print("\n" + "="*70)
    print("Validating Reference Files")
    print("="*70 + "\n")

    issues_found = False

    for ref_file in sorted(reference_files):
        print(f"📄 {ref_file.name}")

        # Check file is readable
        try:
            content = ref_file.read_text()
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")
            issues_found = True
            continue

        # Check for title
        if not re.match(r'^#\s+.+', content, re.MULTILINE):
            print(f"   ⚠️  Missing title (# heading)")
            issues_found = True

        # Check for sections
        if not re.search(r'^##\s+', content, re.MULTILINE):
            print(f"   💡 Consider adding sections (## headings)")

        # Check filename format
        if not re.match(r'^[a-z0-9-]+\.md$', ref_file.name):
            print(f"   ⚠️  Filename should use lowercase-hyphens")
            issues_found = True

        if not issues_found:
            print(f"   ✅ Valid")

        print()

    if not issues_found:
        print("✅ All reference files are valid\n")
    else:
        print("⚠️  Some issues found - review above\n")

def main():
    """
    Usage:
        python3 manage-skill-references.py <skill-name> [action] [filename]

    Actions:
        list           - List all reference files (default)
        add <file>     - Add new reference file
        remove <file>  - Remove reference file
        update <file>  - Update existing reference file
        validate       - Validate all references
    """
    if len(sys.argv) < 2:
        print("Usage: python3 manage-skill-references.py <skill-name> [action] [filename]")
        print("\nActions: list, add, remove, update, validate")
        print("\nExamples:")
        print("  python3 manage-skill-references.py building-agents list")
        print("  python3 manage-skill-references.py building-agents add my-guide.md")
        sys.exit(1)

    skill_name = sys.argv[1]
    action = sys.argv[2] if len(sys.argv) > 2 else 'list'

    # Find skill
    skill_dir = find_skill(skill_name)
    if not skill_dir:
        print(f"\n❌ Skill not found: {skill_name}")
        sys.exit(1)

    # Execute action
    if action == 'list':
        list_references(skill_dir)

    elif action == 'add':
        if len(sys.argv) < 4:
            print("\n❌ Missing filename argument")
            print("Usage: ... add <filename.md>")
            sys.exit(1)
        filename = sys.argv[3]
        add_reference(skill_dir, filename)

    elif action == 'remove':
        if len(sys.argv) < 4:
            print("\n❌ Missing filename argument")
            print("Usage: ... remove <filename.md>")
            sys.exit(1)
        filename = sys.argv[3]
        remove_reference(skill_dir, filename)

    elif action == 'update':
        if len(sys.argv) < 4:
            print("\n❌ Missing filename argument")
            print("Usage: ... update <filename.md>")
            sys.exit(1)
        filename = sys.argv[3]
        update_reference(skill_dir, filename)

    elif action == 'validate':
        validate_references(skill_dir)

    else:
        print(f"\n❌ Unknown action: {action}")
        print("Valid actions: list, add, remove, update, validate")
        sys.exit(1)

if __name__ == '__main__':
    main()
