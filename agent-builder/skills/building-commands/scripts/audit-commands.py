#!/usr/bin/env python3
"""
Audit Commands Script - Bulk validation and reporting
Part of the agent-builder plugin for Claude Code

Runs validation across all commands and generates comprehensive report.
"""

import sys
import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional

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
            command_files.extend(search_path.glob("*/*/*.md"))

    return sorted(set(command_files))

def parse_command(file_path: Path) -> Tuple[Optional[Dict], Optional[str], Optional[str]]:
    """
    Parse command file into frontmatter and body.

    Returns:
        (frontmatter, body, error) - error is None if successful
    """
    try:
        content = file_path.read_text()
    except Exception as e:
        return None, None, f"Failed to read file: {e}"

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return None, None, "Missing YAML frontmatter"

    frontmatter_text, body = match.groups()

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        return None, None, f"Invalid YAML: {e}"

    return frontmatter, body, None

def validate_command(file_path: Path) -> Tuple[str, List[str], List[str], List[str]]:
    """
    Validate a single command.

    Returns:
        (status, critical_errors, warnings, recommendations)
        status: 'valid', 'warnings', 'errors', 'parse_error'
    """
    critical_errors = []
    warnings = []
    recommendations = []

    # Parse
    frontmatter, body, parse_error = parse_command(file_path)

    if parse_error:
        return 'parse_error', [parse_error], [], []

    # Validate filename
    command_name = file_path.stem

    if not re.match(r'^[a-z0-9-]+$', command_name):
        critical_errors.append(f"Invalid filename: must be lowercase-hyphens only")

    if '_' in command_name:
        critical_errors.append(f"Underscores not allowed in filename")

    if len(command_name) > 64:
        critical_errors.append(f"Filename exceeds 64 characters")

    # Check verb-first naming
    common_verbs = [
        'add', 'build', 'check', 'clean', 'commit', 'create', 'delete', 'deploy',
        'generate', 'get', 'install', 'list', 'make', 'new', 'push', 'remove',
        'review', 'run', 'search', 'show', 'test', 'update', 'validate'
    ]
    if not any(command_name.startswith(verb) for verb in common_verbs):
        recommendations.append("Consider verb-first naming (e.g., 'create-', 'run-')")

    # Validate required fields
    if 'description' not in frontmatter:
        critical_errors.append("Missing required 'description' field")
    else:
        desc = frontmatter['description']
        if len(desc) < 10:
            warnings.append("Description too short (< 10 chars)")
        elif len(desc) > 200:
            warnings.append("Description too long (> 200 chars)")

    # Validate model field - CRITICAL for commands
    if 'model' in frontmatter:
        model = frontmatter['model']

        # Check for short aliases (don't work in commands)
        if model in ['haiku', 'sonnet', 'opus', 'inherit']:
            critical_errors.append(
                f"CRITICAL: Commands cannot use short alias '{model}'. "
                f"Use version alias like 'claude-haiku-4-5' or full ID"
            )
        elif not model.startswith('claude-'):
            warnings.append(f"Model '{model}' doesn't start with 'claude-', may cause errors")

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
                    critical_errors.append("Has Bash access without input validation documentation")

    # Validate argument handling
    if body:
        uses_positional = bool(re.search(r'\$\d+', body))
        uses_all_args = '$ARGUMENTS' in body

        if uses_positional or uses_all_args:
            if 'argument-hint' not in frontmatter:
                warnings.append("Uses arguments but missing 'argument-hint' field")

            if '## Arguments' not in body and '## Parameters' not in body:
                recommendations.append("Add '## Arguments' section to document parameters")

        # Security: Check for dangerous patterns
        if 'Bash' in frontmatter.get('allowed-tools', ''):
            dangerous_patterns = [
                (r'\$\w+\s*(?:&&|\||;|`)', "Potential command injection risk"),
                (r'rm\s+-rf\s+\$', "Dangerous rm -rf with variable"),
                (r'eval\s+\$', "Using eval with arguments is dangerous"),
            ]

            for pattern, message in dangerous_patterns:
                if re.search(pattern, body):
                    critical_errors.append(f"SECURITY: {message}")

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
    print("COMMAND AUDIT REPORT")
    print("="*70)

    # Count statuses
    status_counts = {
        'valid': 0,
        'warnings': 0,
        'errors': 0,
        'parse_error': 0,
    }

    for file_path, (status, _, _, _) in results.items():
        status_counts[status] += 1

    total = len(results)

    print(f"\nTotal Commands: {total}")
    print(f"  ✅ Valid:        {status_counts['valid']}")
    print(f"  ⚠️  Warnings:     {status_counts['warnings']}")
    print(f"  ❌ Errors:       {status_counts['errors']}")
    print(f"  💥 Parse Errors: {status_counts['parse_error']}")

    # Show errors first
    errors_found = False
    for file_path, (status, critical_errors, warnings, recommendations) in sorted(results.items()):
        if status in ['errors', 'parse_error']:
            if not errors_found:
                print("\n" + "="*70)
                print("COMMANDS WITH ERRORS")
                print("="*70)
                errors_found = True

            print(f"\n❌ {file_path.name}")
            print(f"   Location: {file_path}")

            for error in critical_errors:
                print(f"   • {error}")

    # Show warnings
    warnings_found = False
    if verbose:
        for file_path, (status, critical_errors, warnings, recommendations) in sorted(results.items()):
            if status == 'warnings':
                if not warnings_found:
                    print("\n" + "="*70)
                    print("COMMANDS WITH WARNINGS")
                    print("="*70)
                    warnings_found = True

                print(f"\n⚠️  {file_path.name}")
                print(f"   Location: {file_path}")

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
        print(f"   Run: python3 update-command.py <command-name>")
        print(f"   Or: python3 migrate-command.py --apply")

    if status_counts['warnings'] > 0:
        print("\n🟡 Improvements Available:")
        print("   Review warnings and consider fixes.")
        print(f"   Run with --verbose to see all warnings")

    if status_counts['valid'] == total:
        print("\n✅ All commands are valid!")
        print("   No critical issues found.")

    print()

def main():
    """
    Usage:
        python3 audit-commands.py              # Audit all commands
        python3 audit-commands.py --verbose    # Show warnings and recommendations
        python3 audit-commands.py --directory <path>  # Audit specific directory
    """
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    # Check for custom directory
    directory = None
    if '--directory' in sys.argv:
        idx = sys.argv.index('--directory')
        if idx + 1 < len(sys.argv):
            directory = Path(sys.argv[idx + 1])

    print("="*70)
    print("Command Audit Tool")
    print("="*70)

    # Find all commands
    command_files = find_all_commands(directory)

    if not command_files:
        print("\n❌ No command files found")
        print("\nSearched in:")
        print("  - .claude/commands/")
        print("  - Plugin commands/ directories")
        sys.exit(0)

    print(f"\nScanning {len(command_files)} command files...")

    # Validate each command
    results = {}
    for command_file in command_files:
        status, critical_errors, warnings, recommendations = validate_command(command_file)
        results[command_file] = (status, critical_errors, warnings, recommendations)

    # Print report
    print_report(results, verbose)

    # Exit with appropriate code
    has_errors = any(status in ['errors', 'parse_error'] for status, _, _, _ in results.values())
    sys.exit(1 if has_errors else 0)

if __name__ == '__main__':
    main()
