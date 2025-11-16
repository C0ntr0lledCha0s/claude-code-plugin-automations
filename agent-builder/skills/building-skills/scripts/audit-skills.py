#!/usr/bin/env python3
"""
Audit Skills Script - Bulk validation and reporting
Part of the agent-builder plugin for Claude Code

Runs validation across all skills and generates comprehensive report.
"""

import sys
import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional

def find_all_skills(directory: Path = None) -> List[Path]:
    """Find all skill directories in directory tree."""
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
            # Find directories containing SKILL.md
            for skill_dir in search_path.iterdir():
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                    skill_dirs.append(skill_dir)

    return sorted(set(skill_dirs))

def parse_skill(skill_dir: Path) -> Tuple[Optional[Dict], Optional[str], Optional[str]]:
    """
    Parse skill SKILL.md into frontmatter and body.

    Returns:
        (frontmatter, body, error) - error is None if successful
    """
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return None, None, "SKILL.md not found"

    try:
        content = skill_md.read_text()
    except Exception as e:
        return None, None, f"Failed to read SKILL.md: {e}"

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return None, None, "Missing YAML frontmatter"

    frontmatter_text, body = match.groups()

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        return None, None, f"Invalid YAML: {e}"

    return frontmatter, body, None

def validate_skill(skill_dir: Path) -> Tuple[str, List[str], List[str], List[str]]:
    """
    Validate a single skill.

    Returns:
        (status, critical_errors, warnings, recommendations)
        status: 'valid', 'warnings', 'errors', 'parse_error'
    """
    critical_errors = []
    warnings = []
    recommendations = []

    skill_name = skill_dir.name

    # Parse
    frontmatter, body, parse_error = parse_skill(skill_dir)

    if parse_error:
        return 'parse_error', [parse_error], [], []

    # Validate directory name
    if not re.match(r'^[a-z0-9-]+$', skill_name):
        critical_errors.append(f"Invalid directory name: must be lowercase-hyphens only")

    if '_' in skill_name:
        critical_errors.append(f"Underscores not allowed in directory name")

    if len(skill_name) > 64:
        critical_errors.append(f"Directory name exceeds 64 characters")

    # Check gerund form (recommended for skills)
    if not skill_name.endswith('ing') and not any(word in skill_name for word in ['-ing-', 'analyzing', 'building', 'creating']):
        recommendations.append("Consider gerund form for skill names (e.g., 'building-x', 'analyzing-y')")

    # Validate required fields
    if 'name' not in frontmatter:
        critical_errors.append("Missing required 'name' field")
    else:
        if frontmatter['name'] != skill_name:
            warnings.append(f"Name '{frontmatter['name']}' doesn't match directory '{skill_name}'")

    if 'description' not in frontmatter:
        critical_errors.append("Missing required 'description' field")
    else:
        desc = frontmatter['description']
        if len(desc) < 30:
            warnings.append("Description too short for skills (< 30 chars)")
        elif len(desc) > 1024:
            critical_errors.append("Description exceeds 1024 character limit")

        # Check for auto-invocation triggers
        trigger_keywords = ['use when', 'when', 'auto-invokes when', 'whenever', 'automatically activated']
        if not any(keyword in desc.lower() for keyword in trigger_keywords):
            warnings.append("Description should clearly state WHEN Claude should auto-invoke")

    # CRITICAL: Check for model field (skills don't support it)
    if 'model' in frontmatter:
        critical_errors.append(
            "CRITICAL: Skills cannot have 'model' field. "
            "Only agents support model specification. "
            "Run: /agent-builder:skills:migrate " + skill_name + " --apply"
        )

    # Validate version field
    if 'version' in frontmatter:
        if not re.match(r'^\d+\.\d+\.\d+', str(frontmatter['version'])):
            warnings.append("Use semantic versioning (e.g., 1.0.0)")

    # Validate tools
    if 'allowed-tools' in frontmatter:
        tools = frontmatter['allowed-tools']
        valid_tools = [
            'Read', 'Write', 'Edit', 'Grep', 'Glob', 'Bash',
            'WebFetch', 'WebSearch', 'NotebookEdit', 'Task',
            'TodoWrite', 'BashOutput', 'KillShell'
        ]

        if isinstance(tools, str):
            tool_list = [t.strip() for t in tools.split(',')]
            for tool in tool_list:
                if tool not in valid_tools:
                    warnings.append(f"Unknown tool: '{tool}'")

            # Security check: Bash without validation
            if 'Bash' in tools:
                if body and 'validation' not in body.lower() and 'sanitize' not in body.lower():
                    warnings.append("Has Bash access - ensure input validation is documented")

    # Check directory structure
    has_scripts = (skill_dir / "scripts").exists()
    has_references = (skill_dir / "references").exists()
    has_assets = (skill_dir / "assets").exists() or (skill_dir / "templates").exists()

    # Check for {baseDir} usage if resources exist
    if body and (has_scripts or has_references or has_assets):
        if '{baseDir}' not in body:
            warnings.append("Has resource directories but doesn't use {baseDir} variable")

    # Check script permissions
    if has_scripts:
        script_dir = skill_dir / "scripts"
        for script_file in script_dir.glob("*.py"):
            if not os.access(script_file, os.X_OK):
                warnings.append(f"Script not executable: {script_file.name} (run chmod +x)")
        for script_file in script_dir.glob("*.sh"):
            if not os.access(script_file, os.X_OK):
                warnings.append(f"Script not executable: {script_file.name} (run chmod +x)")

    # Check for SKILL.md content structure
    if body:
        if '## ' not in body:
            recommendations.append("Add section headings (##) to structure the skill content")

        # Look for key sections
        recommended_sections = ['When to Use', 'Capabilities', 'Examples', 'How to Use']
        missing_sections = []
        for section in recommended_sections:
            if section not in body:
                missing_sections.append(section)

        if missing_sections:
            recommendations.append(f"Consider adding sections: {', '.join(missing_sections)}")

    # Determine status
    if critical_errors:
        status = 'errors'
    elif warnings:
        status = 'warnings'
    else:
        status = 'valid'

    return status, critical_errors, warnings, recommendations

def print_report(results: Dict, verbose: bool = False):
    """Print audit report."""
    print("\n" + "="*70)
    print("SKILL AUDIT REPORT")
    print("="*70)

    # Count statuses
    status_counts = {
        'valid': 0,
        'warnings': 0,
        'errors': 0,
        'parse_error': 0,
    }

    for skill_dir, (status, _, _, _) in results.items():
        status_counts[status] += 1

    total = len(results)

    print(f"\nTotal Skills: {total}")
    print(f"  ✅ Valid:        {status_counts['valid']}")
    print(f"  ⚠️  Warnings:     {status_counts['warnings']}")
    print(f"  ❌ Errors:       {status_counts['errors']}")
    print(f"  💥 Parse Errors: {status_counts['parse_error']}")

    # Show errors first
    errors_found = False
    for skill_dir, (status, critical_errors, warnings, recommendations) in sorted(results.items()):
        if status in ['errors', 'parse_error']:
            if not errors_found:
                print("\n" + "="*70)
                print("SKILLS WITH ERRORS")
                print("="*70)
                errors_found = True

            print(f"\n❌ {skill_dir.name}")
            print(f"   Location: {skill_dir}")

            for error in critical_errors:
                print(f"   • {error}")

    # Show warnings
    warnings_found = False
    if verbose:
        for skill_dir, (status, critical_errors, warnings, recommendations) in sorted(results.items()):
            if status == 'warnings':
                if not warnings_found:
                    print("\n" + "="*70)
                    print("SKILLS WITH WARNINGS")
                    print("="*70)
                    warnings_found = True

                print(f"\n⚠️  {skill_dir.name}")
                print(f"   Location: {skill_dir}")

                for warning in warnings:
                    print(f"   • {warning}")

                if recommendations:
                    for rec in recommendations:
                        print(f"   💡 {rec}")

    # Summary recommendations
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)

    if status_counts['errors'] > 0 or status_counts['parse_error'] > 0:
        print("\n🔴 Action Required:")
        print("   Fix critical errors before committing.")
        print(f"   Run: /agent-builder:skills:update <skill-name>")
        print(f"   Or: /agent-builder:skills:migrate <skill-name> --apply")

    if status_counts['warnings'] > 0:
        print("\n🟡 Improvements Available:")
        print("   Review warnings and consider fixes.")
        print(f"   Run with --verbose to see all warnings")
        print(f"   Run: /agent-builder:skills:enhance <skill-name>")

    if status_counts['valid'] == total:
        print("\n✅ All skills are valid!")
        print("   No critical issues found.")

    print()

def main():
    """
    Usage:
        python3 audit-skills.py              # Audit all skills
        python3 audit-skills.py --verbose    # Show warnings and recommendations
        python3 audit-skills.py --directory <path>  # Audit specific directory
    """
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    # Check for custom directory
    directory = None
    if '--directory' in sys.argv:
        idx = sys.argv.index('--directory')
        if idx + 1 < len(sys.argv):
            directory = Path(sys.argv[idx + 1])

    print("="*70)
    print("Skill Audit Tool")
    print("="*70)

    # Find all skills
    skill_dirs = find_all_skills(directory)

    if not skill_dirs:
        print("\n❌ No skill directories found")
        print("\nSearched in:")
        print("  - .claude/skills/")
        print("  - Plugin skills/ directories")
        sys.exit(0)

    print(f"\nScanning {len(skill_dirs)} skill directories...")

    # Validate each skill
    results = {}
    for skill_dir in skill_dirs:
        status, critical_errors, warnings, recommendations = validate_skill(skill_dir)
        results[skill_dir] = (status, critical_errors, warnings, recommendations)

    # Print report
    print_report(results, verbose)

    # Exit with appropriate code
    has_errors = any(status in ['errors', 'parse_error'] for status, _, _, _ in results.values())
    sys.exit(1 if has_errors else 0)

if __name__ == '__main__':
    main()
