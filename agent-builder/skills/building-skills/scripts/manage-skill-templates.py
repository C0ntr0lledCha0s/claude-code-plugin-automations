#!/usr/bin/env python3
"""
Manage Skill Templates Script - Template file manager
Part of the agent-builder plugin for Claude Code

Manage template files in a skill's templates/ or assets/ directory.
"""

import sys
import re
import json
import yaml
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

def get_templates_dir(skill_dir: Path) -> Path:
    """Get templates or assets directory (prefer templates)."""
    templates_dir = skill_dir / "templates"
    assets_dir = skill_dir / "assets"

    if templates_dir.exists():
        return templates_dir
    elif assets_dir.exists():
        return assets_dir
    else:
        # Default to templates/
        return templates_dir

def ensure_templates_dir(skill_dir: Path) -> Path:
    """Ensure templates/ directory exists."""
    templates_dir = get_templates_dir(skill_dir)
    templates_dir.mkdir(exist_ok=True)
    return templates_dir

def list_templates(skill_dir: Path):
    """List all template files."""
    templates_dir = get_templates_dir(skill_dir)
    dir_name = templates_dir.name

    print("\n" + "="*70)
    print(f"Template Files for '{skill_dir.name}'")
    print("="*70)

    if not templates_dir.exists():
        print(f"\n⚠️  No {dir_name}/ directory found")
        print(f"\nCreate with: mkdir {templates_dir}")
        return

    template_files = sorted(templates_dir.glob("*"))

    if not template_files:
        print(f"\n📁 {dir_name}/ directory is empty")
        print("\nAdd a template with:")
        print(f"  /agent-builder:skills:update-templates {skill_dir.name} add <filename>")
        return

    print(f"\nFound {len(template_files)} template file(s) in {dir_name}/:\n")

    # Group by extension
    by_extension = {}
    for template_file in template_files:
        if template_file.is_file():
            ext = template_file.suffix or '(no extension)'
            if ext not in by_extension:
                by_extension[ext] = []
            by_extension[ext].append(template_file)

    for ext in sorted(by_extension.keys()):
        files = by_extension[ext]
        print(f"  {ext}:")
        for template_file in files:
            print(f"    📄 {template_file.name}")
        print()

    print(f"\nTo use in SKILL.md:")
    print(f"  {{{{baseDir}}}}/{dir_name}/{template_files[0].name}")
    print()

def add_template(skill_dir: Path, filename: str):
    """Add a new template file."""
    templates_dir = ensure_templates_dir(skill_dir)
    dir_name = templates_dir.name

    # Validate filename
    if not re.match(r'^[a-z0-9-]+\.[a-z0-9]+$', filename):
        print("\n❌ Invalid filename. Use lowercase-hyphens with extension (e.g., 'my-template.md')")
        sys.exit(1)

    template_file = templates_dir / filename

    if template_file.exists():
        print(f"\n❌ File already exists: {filename}")
        print(f"\nUse 'update' action to modify existing file:")
        print(f"  /agent-builder:skills:update-templates {skill_dir.name} update {filename}")
        sys.exit(1)

    # Determine template type from extension
    ext = Path(filename).suffix.lower()

    # Prompt for description
    description = input("\nTemplate description: ").strip()
    if not description:
        description = "Template file"

    # Create appropriate template content
    if ext == '.md':
        content = f"""---
name: {{{{NAME}}}}
description: {{{{DESCRIPTION}}}}
version: {{{{VERSION}}}}
---

# {{{{TITLE}}}}

Template created for {skill_dir.name} skill.

## Usage

[Instructions for using this template]

## Variables

Replace these placeholders:
- `{{{{NAME}}}}` - Component name
- `{{{{DESCRIPTION}}}}` - Component description
- `{{{{VERSION}}}}` - Version number
- `{{{{TITLE}}}}` - Display title
"""

    elif ext == '.json':
        content = '''{
  "name": "{{NAME}}",
  "description": "{{DESCRIPTION}}",
  "version": "{{VERSION}}"
}
'''

    elif ext in ['.yaml', '.yml']:
        content = '''---
name: {{NAME}}
description: {{DESCRIPTION}}
version: {{VERSION}}
'''

    elif ext == '.py':
        content = '''#!/usr/bin/env python3
"""
{{DESCRIPTION}}

Part of the {{SKILL_NAME}} skill
"""

def main():
    """Main function."""
    # TODO: Implement functionality
    pass

if __name__ == '__main__':
    main()
'''

    elif ext == '.sh':
        content = '''#!/bin/bash
#
# {{DESCRIPTION}}
# Part of the {{SKILL_NAME}} skill
#

set -euo pipefail

# TODO: Implement functionality
'''

    else:
        # Generic template
        content = f"""# {description}

Template file for {skill_dir.name} skill.

Replace variables as needed:
- {{{{VAR_NAME}}}}
"""

    # Write file
    template_file.write_text(content)

    print(f"\n✅ Created: {filename}")
    print(f"   Location: {template_file}")
    print(f"\n💡 Next steps:")
    print(f"   1. Edit the file: {template_file}")
    print(f"   2. Document in SKILL.md:")
    print(f"      Use template: `{{{{baseDir}}}}/{dir_name}/{filename}`")
    print()

def remove_template(skill_dir: Path, filename: str):
    """Remove a template file."""
    templates_dir = get_templates_dir(skill_dir)

    if not templates_dir.exists():
        print(f"\n❌ No {templates_dir.name}/ directory found")
        sys.exit(1)

    template_file = templates_dir / filename

    if not template_file.exists():
        print(f"\n❌ File not found: {filename}")
        list_templates(skill_dir)
        sys.exit(1)

    # Confirm deletion
    print(f"\n⚠️  About to delete: {filename}")
    print(f"   Location: {template_file}")

    confirm = input("\nType 'yes' to confirm deletion: ").strip().lower()

    if confirm != 'yes':
        print("\n❌ Deletion cancelled")
        sys.exit(0)

    # Delete file
    template_file.unlink()

    print(f"\n✅ Deleted: {filename}")
    print(f"\n💡 Remember to remove references to this file from SKILL.md")
    print()

def update_template(skill_dir: Path, filename: str):
    """Update an existing template file."""
    templates_dir = get_templates_dir(skill_dir)

    if not templates_dir.exists():
        print(f"\n❌ No {templates_dir.name}/ directory found")
        sys.exit(1)

    template_file = templates_dir / filename

    if not template_file.exists():
        print(f"\n❌ File not found: {filename}")
        list_templates(skill_dir)
        sys.exit(1)

    print(f"\n📝 Edit this file: {template_file}")
    print(f"\nUse your preferred editor to make changes.")
    print()

def validate_templates(skill_dir: Path):
    """Validate template files."""
    templates_dir = get_templates_dir(skill_dir)

    if not templates_dir.exists():
        print(f"\n⚠️  No {templates_dir.name}/ directory found")
        return

    template_files = list(templates_dir.glob("*"))

    if not template_files:
        print("\n⚠️  No template files to validate")
        return

    print("\n" + "="*70)
    print("Validating Template Files")
    print("="*70 + "\n")

    issues_found = False

    for template_file in sorted(template_files):
        if not template_file.is_file():
            continue

        print(f"📄 {template_file.name}")

        # Check file is readable
        try:
            content = template_file.read_text()
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")
            issues_found = True
            continue

        ext = template_file.suffix.lower()

        # Validate based on file type
        if ext == '.json':
            try:
                # Allow {{VAR}} style variables
                test_content = re.sub(r'\{\{[A-Z_]+\}\}', '"test"', content)
                json.loads(test_content)
                print(f"   ✅ Valid JSON syntax")
            except json.JSONDecodeError as e:
                print(f"   ❌ Invalid JSON: {e}")
                issues_found = True

        elif ext in ['.yaml', '.yml']:
            try:
                # Allow {{VAR}} style variables
                test_content = re.sub(r'\{\{[A-Z_]+\}\}', 'test', content)
                yaml.safe_load(test_content)
                print(f"   ✅ Valid YAML syntax")
            except yaml.YAMLError as e:
                print(f"   ❌ Invalid YAML: {e}")
                issues_found = True

        # Check for variable placeholders
        variables = re.findall(r'\{\{([A-Z_]+)\}\}', content)
        if variables:
            print(f"   💡 Variables found: {', '.join(set(variables))}")

        # Check filename format
        if not re.match(r'^[a-z0-9-]+\.[a-z0-9]+$', template_file.name):
            print(f"   ⚠️  Filename should use lowercase-hyphens")
            issues_found = True

        if not issues_found:
            print(f"   ✅ Valid")

        print()

    if not issues_found:
        print("✅ All template files are valid\n")
    else:
        print("⚠️  Some issues found - review above\n")

def main():
    """
    Usage:
        python3 manage-skill-templates.py <skill-name> [action] [filename]

    Actions:
        list           - List all template files (default)
        add <file>     - Add new template file
        remove <file>  - Remove template file
        update <file>  - Update existing template file
        validate       - Validate all templates
    """
    if len(sys.argv) < 2:
        print("Usage: python3 manage-skill-templates.py <skill-name> [action] [filename]")
        print("\nActions: list, add, remove, update, validate")
        print("\nExamples:")
        print("  python3 manage-skill-templates.py building-agents list")
        print("  python3 manage-skill-templates.py building-agents add my-template.md")
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
        list_templates(skill_dir)

    elif action == 'add':
        if len(sys.argv) < 4:
            print("\n❌ Missing filename argument")
            print("Usage: ... add <filename.ext>")
            sys.exit(1)
        filename = sys.argv[3]
        add_template(skill_dir, filename)

    elif action == 'remove':
        if len(sys.argv) < 4:
            print("\n❌ Missing filename argument")
            print("Usage: ... remove <filename.ext>")
            sys.exit(1)
        filename = sys.argv[3]
        remove_template(skill_dir, filename)

    elif action == 'update':
        if len(sys.argv) < 4:
            print("\n❌ Missing filename argument")
            print("Usage: ... update <filename.ext>")
            sys.exit(1)
        filename = sys.argv[3]
        update_template(skill_dir, filename)

    elif action == 'validate':
        validate_templates(skill_dir)

    else:
        print(f"\n❌ Unknown action: {action}")
        print("Valid actions: list, add, remove, update, validate")
        sys.exit(1)

if __name__ == '__main__':
    main()
