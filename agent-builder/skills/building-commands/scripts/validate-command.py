#!/usr/bin/env python3
"""
Command validation script for Claude Code slash commands.
Validates YAML frontmatter, naming conventions, and schema compliance.
"""

import re
import sys
import yaml
from pathlib import Path


def validate_command(file_path: str) -> tuple[bool, list[str]]:
    """
    Validate a Claude Code slash command file.

    Returns:
        tuple[bool, list[str]]: (is_valid, list_of_errors)
    """
    errors = []
    path = Path(file_path)

    if not path.exists():
        return False, [f"File does not exist: {file_path}"]

    # Get command name from filename
    command_name = path.stem

    # Validate filename
    if not re.match(r'^[a-z0-9-]+$', command_name):
        errors.append(f"Invalid filename '{command_name}.md': must be lowercase letters, numbers, and hyphens only")

    if '_' in command_name:
        errors.append(f"Invalid filename '{command_name}.md': underscores not allowed, use hyphens instead")

    # Check if name is action-oriented (starts with verb)
    common_verbs = [
        'add', 'build', 'check', 'clean', 'commit', 'create', 'delete', 'deploy',
        'generate', 'get', 'install', 'list', 'make', 'push', 'remove', 'review',
        'run', 'search', 'show', 'test', 'update', 'validate'
    ]
    if not any(command_name.startswith(verb) for verb in common_verbs):
        errors.append(f"Recommendation: Command names are typically action-oriented (start with a verb): '{command_name}' → consider 'run-{command_name}', 'create-{command_name}', etc.")

    # Read file
    try:
        content = path.read_text()
    except Exception as e:
        return False, [f"Failed to read file: {e}"]

    # Check for YAML frontmatter
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(frontmatter_pattern, content, re.DOTALL)

    if not match:
        errors.append("Missing YAML frontmatter (must start with --- and end with ---)")
        return False, errors

    frontmatter_text = match.group(1)

    # Parse YAML
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML syntax: {e}")
        return False, errors

    # Check for recommended fields
    if 'description' not in frontmatter:
        errors.append("Recommendation: Add 'description' field to help users understand what the command does")
    else:
        description = frontmatter['description']
        if len(description) < 10:
            errors.append(f"Warning: Description is very short ({len(description)} chars)")

    # Validate optional fields
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
                    errors.append(f"Warning: Unknown tool '{tool}'. Valid tools: {', '.join(valid_tools)}")

    # Commands do not support the 'model' field - only agents support it
    if 'model' in frontmatter:
        errors.append("Invalid field 'model': Commands do not support model specification. Only agents can specify a model. Remove this field.")

    if 'argument-hint' in frontmatter:
        arg_hint = frontmatter['argument-hint']
        if not arg_hint.startswith('['):
            errors.append(f"Warning: argument-hint typically uses brackets: '{arg_hint}' → '[{arg_hint}]'")

    # Check body content
    body = content[match.end():]

    # Check for argument usage
    uses_positional = bool(re.search(r'\$\d+', body))
    uses_all_args = '$ARGUMENTS' in body

    if uses_positional or uses_all_args:
        if 'argument-hint' not in frontmatter:
            errors.append("Recommendation: Add 'argument-hint' field since the command uses arguments ($1, $2, or $ARGUMENTS)")

        # Document the arguments in body
        if uses_positional and '## Arguments' not in body:
            errors.append("Recommendation: Add an '## Arguments' section to document what each positional argument does")

    # Check for workflow documentation
    if '## Workflow' not in body and '## Steps' not in body:
        errors.append("Recommendation: Add a workflow section to document the command's execution steps")

    # Check for examples
    if '## Example' not in body and '## Usage' not in body:
        errors.append("Recommendation: Add usage examples showing how to invoke the command")

    # Security checks
    if 'Bash' in frontmatter.get('allowed-tools', ''):
        # Check for dangerous patterns
        dangerous_patterns = [
            (r'\$\w+\s*(?:&&|\||;|`)', "Potential command injection risk with unsanitized arguments"),
            (r'rm\s+-rf\s+\$', "Dangerous rm -rf with variable - add validation"),
            (r'eval\s+\$', "Using eval with arguments is dangerous"),
        ]

        for pattern, warning in dangerous_patterns:
            if re.search(pattern, body):
                errors.append(f"Security Warning: {warning}")

    return len([e for e in errors if not (e.startswith('Warning:') or e.startswith('Recommendation:'))]) == 0, errors


def main():
    if len(sys.argv) < 2:
        print("Usage: validate-command.py <command-file.md>")
        sys.exit(1)

    command_file = sys.argv[1]
    is_valid, errors = validate_command(command_file)

    if is_valid and not errors:
        print(f"✓ Command '{command_file}' is valid!")
        sys.exit(0)
    else:
        print(f"Validation results for '{command_file}':\n")

        critical_errors = []
        warnings = []
        recommendations = []

        for error in errors:
            if error.startswith("Security Warning:"):
                critical_errors.append(error)
            elif error.startswith("Warning:"):
                warnings.append(error)
            elif error.startswith("Recommendation:"):
                recommendations.append(error)
            else:
                critical_errors.append(error)

        if critical_errors:
            print("❌ Critical Errors:")
            for error in critical_errors:
                print(f"   {error}")
            print()

        if warnings:
            print("⚠️  Warnings:")
            for warning in warnings:
                print(f"   {warning}")
            print()

        if recommendations:
            print("💡 Recommendations:")
            for rec in recommendations:
                print(f"   {rec}")
            print()

        sys.exit(1 if critical_errors else 0)


if __name__ == '__main__':
    main()
