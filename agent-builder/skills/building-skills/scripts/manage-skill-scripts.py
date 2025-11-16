#!/usr/bin/env python3
"""
Manage Skill Scripts - Script file manager with permission enforcement
Part of the agent-builder plugin for Claude Code

Manage scripts in a skill's scripts/ directory with automatic chmod +x.
"""

import sys
import os
import re
import stat
import subprocess
from pathlib import Path
from typing import Optional, List

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

def ensure_scripts_dir(skill_dir: Path) -> Path:
    """Ensure scripts/ directory exists."""
    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir(exist_ok=True)
    return scripts_dir

def is_executable(file_path: Path) -> bool:
    """Check if file has executable permission."""
    return os.access(file_path, os.X_OK)

def make_executable(file_path: Path):
    """Make file executable (chmod +x)."""
    current_permissions = file_path.stat().st_mode
    file_path.chmod(current_permissions | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

def list_scripts(skill_dir: Path):
    """List all scripts with permission status."""
    scripts_dir = skill_dir / "scripts"

    print("\n" + "="*70)
    print(f"Scripts for '{skill_dir.name}'")
    print("="*70)

    if not scripts_dir.exists():
        print(f"\n⚠️  No scripts/ directory found")
        print(f"\nCreate with: mkdir {scripts_dir}")
        return

    script_files = sorted(scripts_dir.glob("*.py")) + sorted(scripts_dir.glob("*.sh"))

    if not script_files:
        print(f"\n📁 scripts/ directory is empty")
        print("\nAdd a script with:")
        print(f"  /agent-builder:skills:update-scripts {skill_dir.name} add <filename.py>")
        return

    print(f"\nFound {len(script_files)} script file(s):\n")

    non_executable = []

    for script_file in script_files:
        executable = is_executable(script_file)
        status = "✅" if executable else "❌"

        print(f"  {status} {script_file.name}")

        if not executable:
            non_executable.append(script_file)

            # Try to read shebang
            try:
                first_line = script_file.read_text().split('\n')[0]
                if first_line.startswith('#!'):
                    print(f"     Shebang: {first_line}")
                else:
                    print(f"     ⚠️  Missing shebang")
            except:
                pass

    if non_executable:
        print(f"\n⚠️  {len(non_executable)} script(s) not executable")
        print(f"\nFix with:")
        print(f"  /agent-builder:skills:update-scripts {skill_dir.name} fix-permissions")

    print()

def add_script(skill_dir: Path, filename: str):
    """Add a new script with proper shebang and permissions."""
    scripts_dir = ensure_scripts_dir(skill_dir)

    # Validate filename
    if not filename.endswith(('.py', '.sh')):
        print("\n❌ Invalid filename. Use .py or .sh extension")
        sys.exit(1)

    if not re.match(r'^[a-z0-9-]+\.(py|sh)$', filename):
        print("\n❌ Invalid filename. Use lowercase-hyphens only (e.g., 'my-script.py')")
        sys.exit(1)

    script_file = scripts_dir / filename

    if script_file.exists():
        print(f"\n❌ File already exists: {filename}")
        print(f"\nUse 'update' action to modify existing file:")
        print(f"  /agent-builder:skills:update-scripts {skill_dir.name} update {filename}")
        sys.exit(1)

    # Prompt for description
    description = input("\nScript description: ").strip()
    if not description:
        description = "Script for " + skill_dir.name

    ext = Path(filename).suffix

    # Create appropriate template
    if ext == '.py':
        content = f'''#!/usr/bin/env python3
"""
{description}

Part of the {skill_dir.name} skill for Claude Code
"""

import sys
import re
from pathlib import Path
from typing import Optional

def main():
    """
    Usage:
        python3 {filename} <arguments>
    """
    if len(sys.argv) < 2:
        print("Usage: python3 {filename} <arguments>")
        sys.exit(1)

    # TODO: Implement functionality
    print("Script executed successfully")

if __name__ == '__main__':
    main()
'''

    elif ext == '.sh':
        content = f'''#!/bin/bash
#
# {description}
# Part of the {skill_dir.name} skill for Claude Code
#

set -euo pipefail

# Usage: {filename} <arguments>

if [ $# -lt 1 ]; then
    echo "Usage: {filename} <arguments>"
    exit 1
fi

# TODO: Implement functionality
echo "Script executed successfully"
'''

    # Write file
    script_file.write_text(content)

    # Make executable (CRITICAL)
    make_executable(script_file)

    executable_status = "✅ Executable" if is_executable(script_file) else "❌ Not executable"

    print(f"\n✅ Created: {filename}")
    print(f"   Location: {script_file}")
    print(f"   Permissions: {executable_status}")
    print(f"\n💡 Next steps:")
    print(f"   1. Edit the file: {script_file}")
    print(f"   2. Document in SKILL.md:")
    print(f"      python3 {{{{baseDir}}}}/scripts/{filename} <args>")
    print()

def remove_script(skill_dir: Path, filename: str):
    """Remove a script file."""
    scripts_dir = skill_dir / "scripts"

    if not scripts_dir.exists():
        print(f"\n❌ No scripts/ directory found")
        sys.exit(1)

    script_file = scripts_dir / filename

    if not script_file.exists():
        print(f"\n❌ File not found: {filename}")
        list_scripts(skill_dir)
        sys.exit(1)

    # Confirm deletion
    print(f"\n⚠️  About to delete: {filename}")
    print(f"   Location: {script_file}")

    confirm = input("\nType 'yes' to confirm deletion: ").strip().lower()

    if confirm != 'yes':
        print("\n❌ Deletion cancelled")
        sys.exit(0)

    # Delete file
    script_file.unlink()

    print(f"\n✅ Deleted: {filename}")
    print(f"\n💡 Remember to remove references to this script from SKILL.md")
    print()

def update_script(skill_dir: Path, filename: str):
    """Update an existing script file."""
    scripts_dir = skill_dir / "scripts"

    if not scripts_dir.exists():
        print(f"\n❌ No scripts/ directory found")
        sys.exit(1)

    script_file = scripts_dir / filename

    if not script_file.exists():
        print(f"\n❌ File not found: {filename}")
        list_scripts(skill_dir)
        sys.exit(1)

    # Check permissions
    if not is_executable(script_file):
        print(f"\n⚠️  Script is not executable")
        print(f"   Making executable with chmod +x...")
        make_executable(script_file)
        print(f"   ✅ Fixed")

    print(f"\n📝 Edit this file: {script_file}")
    print(f"\nUse your preferred editor to make changes.")
    print()

def fix_permissions(skill_dir: Path):
    """Fix executable permissions on all scripts."""
    scripts_dir = skill_dir / "scripts"

    if not scripts_dir.exists():
        print(f"\n⚠️  No scripts/ directory found")
        return

    script_files = list(scripts_dir.glob("*.py")) + list(scripts_dir.glob("*.sh"))

    if not script_files:
        print("\n⚠️  No script files found")
        return

    print("\n" + "="*70)
    print("Fixing Script Permissions")
    print("="*70 + "\n")

    fixed_count = 0
    already_executable = 0

    for script_file in sorted(script_files):
        if is_executable(script_file):
            print(f"  ✅ {script_file.name} (already executable)")
            already_executable += 1
        else:
            print(f"  🔧 {script_file.name} (fixing...)")
            make_executable(script_file)

            if is_executable(script_file):
                print(f"     ✅ Fixed")
                fixed_count += 1
            else:
                print(f"     ❌ Failed to fix permissions")

    print(f"\nSummary:")
    print(f"  ✅ Already executable: {already_executable}")
    print(f"  🔧 Fixed: {fixed_count}")
    print(f"  📊 Total: {len(script_files)}")
    print()

def validate_scripts(skill_dir: Path):
    """Validate script files."""
    scripts_dir = skill_dir / "scripts"

    if not scripts_dir.exists():
        print(f"\n⚠️  No scripts/ directory found")
        return

    script_files = list(scripts_dir.glob("*.py")) + list(scripts_dir.glob("*.sh"))

    if not script_files:
        print("\n⚠️  No script files to validate")
        return

    print("\n" + "="*70)
    print("Validating Script Files")
    print("="*70 + "\n")

    issues_found = False

    for script_file in sorted(script_files):
        print(f"📄 {script_file.name}")

        # Check executable
        if not is_executable(script_file):
            print(f"   ❌ Not executable (run fix-permissions)")
            issues_found = True

        # Check shebang
        try:
            content = script_file.read_text()
            lines = content.split('\n')

            if not lines[0].startswith('#!'):
                print(f"   ❌ Missing shebang")
                issues_found = True
            else:
                shebang = lines[0]
                expected = {
                    '.py': '#!/usr/bin/env python3',
                    '.sh': '#!/bin/bash'
                }
                ext = script_file.suffix
                if ext in expected and shebang != expected[ext]:
                    print(f"   ⚠️  Unexpected shebang: {shebang}")
                    print(f"      Expected: {expected[ext]}")
                else:
                    print(f"   ✅ Valid shebang: {shebang}")

            # Check for input validation patterns (Python)
            if script_file.suffix == '.py':
                has_validation = any([
                    'sys.argv' in content and 'len(sys.argv)' in content,
                    're.match' in content,
                    'argparse' in content,
                ])

                if not has_validation:
                    print(f"   💡 Consider adding input validation (sys.argv, re.match)")

            # Try syntax check
            if script_file.suffix == '.py':
                result = subprocess.run(
                    ['python3', '-m', 'py_compile', str(script_file)],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    print(f"   ❌ Python syntax error")
                    issues_found = True

            elif script_file.suffix == '.sh':
                result = subprocess.run(
                    ['bash', '-n', str(script_file)],
                    capture_output=True,
                    text=True
                )
                if result.returncode != 0:
                    print(f"   ❌ Bash syntax error")
                    issues_found = True

        except Exception as e:
            print(f"   ❌ Error validating: {e}")
            issues_found = True

        print()

    if not issues_found:
        print("✅ All scripts are valid\n")
    else:
        print("⚠️  Some issues found - review above\n")

def main():
    """
    Usage:
        python3 manage-skill-scripts.py <skill-name> [action] [filename]

    Actions:
        list             - List all scripts with permission status (default)
        add <file>       - Add new script with +x permission
        remove <file>    - Remove script file
        update <file>    - Update existing script file
        fix-permissions  - Bulk chmod +x on all scripts
        validate         - Validate all scripts
    """
    if len(sys.argv) < 2:
        print("Usage: python3 manage-skill-scripts.py <skill-name> [action] [filename]")
        print("\nActions: list, add, remove, update, fix-permissions, validate")
        print("\nExamples:")
        print("  python3 manage-skill-scripts.py building-agents list")
        print("  python3 manage-skill-scripts.py building-agents add my-script.py")
        print("  python3 manage-skill-scripts.py building-agents fix-permissions")
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
        list_scripts(skill_dir)

    elif action == 'add':
        if len(sys.argv) < 4:
            print("\n❌ Missing filename argument")
            print("Usage: ... add <filename.py|sh>")
            sys.exit(1)
        filename = sys.argv[3]
        add_script(skill_dir, filename)

    elif action == 'remove':
        if len(sys.argv) < 4:
            print("\n❌ Missing filename argument")
            print("Usage: ... remove <filename.py|sh>")
            sys.exit(1)
        filename = sys.argv[3]
        remove_script(skill_dir, filename)

    elif action == 'update':
        if len(sys.argv) < 4:
            print("\n❌ Missing filename argument")
            print("Usage: ... update <filename.py|sh>")
            sys.exit(1)
        filename = sys.argv[3]
        update_script(skill_dir, filename)

    elif action == 'fix-permissions':
        fix_permissions(skill_dir)

    elif action == 'validate':
        validate_scripts(skill_dir)

    else:
        print(f"\n❌ Unknown action: {action}")
        print("Valid actions: list, add, remove, update, fix-permissions, validate")
        sys.exit(1)

if __name__ == '__main__':
    main()
