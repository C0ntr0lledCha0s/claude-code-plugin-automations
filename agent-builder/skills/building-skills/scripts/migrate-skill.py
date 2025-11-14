#!/usr/bin/env python3
"""
Migrate Skill Script - Automated schema migration for skills
Part of the agent-builder plugin for Claude Code

Handles migrations like:
- Removing invalid model field (CRITICAL - skills don't support it)
- Field renames and updates
- Directory structure standardization
"""

import sys
import re
import yaml
import difflib
from pathlib import Path
from typing import Dict, Tuple, List

def find_all_skills(directory: Path = None) -> List[Path]:
    """Find all skill directories in tree."""
    if directory is None:
        directory = Path(".")

    skill_dirs = []

    # Search common locations
    search_paths = [
        directory / ".claude" / "skills",
        directory / "skills",
    ]

    # Also search plugin directories
    for plugin_dir in directory.glob("*/skills"):
        search_paths.append(plugin_dir)

    for search_path in search_paths:
        if search_path.exists():
            for skill_dir in search_path.iterdir():
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                    skill_dirs.append(skill_dir)

    return sorted(set(skill_dirs))

def parse_skill(skill_path: Path) -> Tuple[Dict, str]:
    """Parse SKILL.md file into frontmatter and body."""
    skill_md = skill_path / "SKILL.md"
    content = skill_md.read_text()

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        raise ValueError("Invalid SKILL.md: missing YAML frontmatter")

    frontmatter_text, body = match.groups()
    frontmatter = yaml.safe_load(frontmatter_text)

    return frontmatter, body

def migrate_remove_model_field(frontmatter: Dict) -> Tuple[Dict, List[str]]:
    """
    Remove model field if present (CRITICAL - skills don't support it).

    This is the most important migration for skills.
    """
    changes = []

    if 'model' in frontmatter:
        old_value = frontmatter['model']
        del frontmatter['model']
        changes.append(f"CRITICAL: Removed 'model' field with value '{old_value}' (skills don't support model specification)")

    return frontmatter, changes

def migrate_gerund_form_recommendation(frontmatter: Dict, skill_path: Path) -> Tuple[Dict, List[str]]:
    """
    Check if skill name follows gerund form convention.
    This is a recommendation, not an automatic change.
    """
    changes = []

    name = frontmatter.get('name', skill_path.name)

    if not name.endswith('ing') and not any(word in name for word in ['-ing-', 'analyzing', 'building', 'creating']):
        changes.append(f"RECOMMENDATION: Consider gerund form for skill name '{name}' (e.g., 'building-{name}', '{name}ing')")

    return frontmatter, changes

def migrate_description_triggers(frontmatter: Dict) -> Tuple[Dict, List[str]]:
    """
    Check if description includes auto-invocation triggers.
    This is a recommendation for manual improvement.
    """
    changes = []

    description = frontmatter.get('description', '')

    trigger_keywords = ['use when', 'when', 'auto-invokes when', 'whenever']
    if description and not any(keyword in description.lower() for keyword in trigger_keywords):
        changes.append("RECOMMENDATION: Description should state WHEN Claude should auto-invoke (add 'Auto-invokes when...' or 'Use when...')")

    return frontmatter, changes

def apply_all_migrations(frontmatter: Dict, skill_path: Path) -> Tuple[Dict, List[str]]:
    """Apply all available migrations."""
    all_changes = []

    # Migration 1: Remove model field (CRITICAL)
    frontmatter, changes = migrate_remove_model_field(frontmatter)
    all_changes.extend(changes)

    # Migration 2: Check gerund form (RECOMMENDATION)
    frontmatter, changes = migrate_gerund_form_recommendation(frontmatter, skill_path)
    all_changes.extend(changes)

    # Migration 3: Check description triggers (RECOMMENDATION)
    frontmatter, changes = migrate_description_triggers(frontmatter)
    all_changes.extend(changes)

    return frontmatter, all_changes

def reconstruct_skill(frontmatter: Dict, body: str) -> str:
    """Reconstruct SKILL.md file from frontmatter and body."""
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

def migrate_single_skill(skill_path: Path, dry_run: bool = True) -> Tuple[bool, List[str]]:
    """
    Migrate a single skill directory.

    Returns:
        (needs_migration, changes_list)
    """
    try:
        frontmatter, body = parse_skill(skill_path)
        skill_md = skill_path / "SKILL.md"
        original_content = skill_md.read_text()
    except Exception as e:
        print(f"❌ Failed to parse {skill_path.name}: {e}")
        return False, []

    # Apply migrations
    new_frontmatter, changes = apply_all_migrations(frontmatter, skill_path)

    if not changes:
        return False, []

    # Separate critical changes from recommendations
    critical_changes = [c for c in changes if c.startswith('CRITICAL')]
    recommendations = [c for c in changes if c.startswith('RECOMMENDATION')]

    print(f"\n{'='*60}")
    print(f"Migration: {skill_path.name}")
    print(f"{'='*60}")
    print(f"Location: {skill_path}")

    if critical_changes:
        print(f"\nCritical Changes:")
        for change in critical_changes:
            print(f"  • {change}")

    if recommendations:
        print(f"\nRecommendations (manual):")
        for rec in recommendations:
            print(f"  • {rec}")

    # Only apply if there are critical changes
    if not critical_changes:
        print("\n(only recommendations, no automatic changes)")
        return False, changes

    if not dry_run:
        # Reconstruct file
        new_content = reconstruct_skill(new_frontmatter, body)

        # Show diff
        show_diff(original_content, new_content, skill_md)

        # Confirm
        confirm = input("\nApply migration? (y/n): ").strip().lower()

        if confirm == 'y':
            # Backup original
            backup_path = skill_md.with_suffix('.md.bak')
            skill_md.rename(backup_path)

            # Write new content
            skill_md.write_text(new_content)

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
        python3 migrate-skill.py --dry-run              # Preview all migrations
        python3 migrate-skill.py --apply                 # Apply all migrations
        python3 migrate-skill.py <skill-name>            # Migrate single skill
        python3 migrate-skill.py <skill-name> --apply    # Apply single migration
    """
    if len(sys.argv) < 2:
        print("Skill Migration Tool")
        print("="*60)
        print("\nUsage:")
        print("  python3 migrate-skill.py --dry-run              # Preview all")
        print("  python3 migrate-skill.py --apply                 # Apply all")
        print("  python3 migrate-skill.py <skill-name>            # Preview one")
        print("  python3 migrate-skill.py <skill-name> --apply    # Apply one")
        print("\nMigrations:")
        print("  • Remove 'model' field (CRITICAL - skills don't support it)")
        print("  • Check gerund form naming (recommendation)")
        print("  • Check auto-invocation triggers (recommendation)")
        sys.exit(1)

    arg1 = sys.argv[1]
    dry_run = True
    specific_skill = None

    # Parse arguments
    if arg1 == '--dry-run':
        dry_run = True
    elif arg1 == '--apply':
        dry_run = False
    else:
        # Specific skill
        specific_skill = arg1
        if len(sys.argv) > 2 and sys.argv[2] == '--apply':
            dry_run = False

    print("="*60)
    print("Skill Migration Tool")
    print("="*60)
    print(f"Mode: {'Dry-run (preview only)' if dry_run else 'Apply changes'}\n")

    # Single skill migration
    if specific_skill:
        from pathlib import Path

        # Find skill
        skill_path = None
        search_paths = [
            Path(".claude/skills"),
            Path.home() / ".claude" / "skills",
            Path("."),
        ]

        for search_path in search_paths:
            if not search_path.exists():
                continue

            candidate = search_path / specific_skill
            if candidate.exists() and candidate.is_dir() and (candidate / "SKILL.md").exists():
                skill_path = candidate
                break

            for candidate in search_path.rglob(specific_skill):
                if candidate.is_dir() and (candidate / "SKILL.md").exists():
                    skill_path = candidate
                    break

        if not skill_path:
            print(f"❌ Skill not found: {specific_skill}")
            sys.exit(1)

        needs_migration, changes = migrate_single_skill(skill_path, dry_run)

        if not needs_migration:
            print(f"\n✅ Skill '{specific_skill}' is already up-to-date!")
        elif dry_run:
            print(f"\n💡 Run with --apply to apply these migrations")

        sys.exit(0)

    # Bulk migration
    skill_dirs = find_all_skills()

    if not skill_dirs:
        print("No skill directories found")
        sys.exit(0)

    print(f"Found {len(skill_dirs)} skill directories\n")

    migrated_count = 0
    skipped_count = 0

    for skill_dir in skill_dirs:
        needs_migration, changes = migrate_single_skill(skill_dir, dry_run=True)

        if needs_migration:
            migrated_count += 1
            if not dry_run:
                # Apply migration interactively
                migrate_single_skill(skill_dir, dry_run=False)
        else:
            skipped_count += 1

    # Summary
    print("\n" + "="*60)
    print("Migration Summary")
    print("="*60)
    print(f"Total skills: {len(skill_dirs)}")
    print(f"Need migration: {migrated_count}")
    print(f"Already up-to-date: {skipped_count}")

    if dry_run and migrated_count > 0:
        print(f"\n💡 Run with --apply to apply migrations")

if __name__ == '__main__':
    main()
