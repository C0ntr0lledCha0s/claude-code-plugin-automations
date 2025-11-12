#!/usr/bin/env python3
"""
Command Generator Script
Creates a new Claude Code slash command with interactive prompts
"""

import sys
import re
from pathlib import Path


def validate_name(name):
    """Validate command name follows conventions"""
    if not re.match(r'^[a-z0-9-]+$', name):
        return False, "Name must be lowercase letters, numbers, and hyphens only"
    if '_' in name:
        return False, "Use hyphens instead of underscores"

    # Recommend action-oriented names
    common_verbs = ['add', 'build', 'check', 'create', 'delete', 'deploy', 'generate',
                    'get', 'list', 'make', 'remove', 'review', 'run', 'show', 'test', 'update']
    if not any(name.startswith(verb) for verb in common_verbs):
        print(f"💡 Tip: Command names are typically action-oriented (start with a verb)")
        print(f"   Examples: run-{name}, create-{name}, show-{name}")

    return True, "Valid"


def prompt_user(question, default=None, required=True):
    """Prompt user for input"""
    if default:
        prompt = f"{question} [{default}]: "
    else:
        prompt = f"{question}: "

    while True:
        response = input(prompt).strip()
        if not response and default:
            return default
        if not response and not required:
            return ""
        if response or not required:
            return response
        print("This field is required. Please provide a value.")


def generate_command(name, description, tools, argument_hint, has_args, workflow):
    """Generate command markdown content"""

    # Build frontmatter
    frontmatter = [
        "---",
        f"description: {description}"
    ]

    if tools:
        frontmatter.append(f"allowed-tools: {tools}")

    if argument_hint:
        frontmatter.append(f"argument-hint: {argument_hint}")

    # Note: Commands do not support the 'model' field - only agents do

    frontmatter.append("---")

    # Build body
    command_name_title = ' '.join(word.capitalize() for word in name.split('-'))

    # Build arguments section
    args_section = ""
    if has_args:
        args_section = """
## Arguments

- **`$1`**: [Description of first argument]
- **`$2`**: [Description of second argument] (optional)
- **`$ARGUMENTS`**: Use this to capture all arguments as a single string

Note: Use the variables in your workflow below.
"""

    body = f"""
# {command_name_title}

[Brief description of what this command does and when to use it]

{args_section}

## Your Task

{workflow}

## Workflow

When this command is invoked:

1. **Validate**: Check that required arguments are provided
2. **Process**: Execute the main logic
3. **Output**: Provide clear results to the user

## Examples

### Example Usage
```
/{name} [example arguments]
```

Expected behavior:
1. [What happens]
2. [What happens]
3. [Result]

## Important Notes

- [Note about usage]
- [Note about requirements]
- [Note about side effects]

## Error Handling

If arguments are missing or invalid:
- Display clear error message
- Show usage example
- Provide guidance for correction
"""

    return '\n'.join(frontmatter) + body


def main():
    print("=" * 70)
    print("⚡ CLAUDE CODE COMMAND GENERATOR")
    print("=" * 70)
    print()

    # Get command name
    while True:
        name = prompt_user("Command name (lowercase-hyphens, e.g., 'run-tests')")
        valid, message = validate_name(name)
        if valid:
            break
        print(f"❌ {message}")

    # Get description
    print("\n📝 Description")
    print("Brief one-line description of what this command does.")
    description = prompt_user("Description")

    # Get tools
    print("\n🔧 Allowed Tools")
    print("Common: Read, Grep, Bash (for executing commands)")
    print("        Read, Write, Edit, Grep, Glob (for file operations)")
    tools = prompt_user("Allowed tools", "Read, Grep, Bash")

    # Note: Commands do not support model specification - they inherit from parent context

    # Check if command needs arguments
    has_args = prompt_user("Does this command take arguments? (y/n)", "y").lower() == 'y'

    argument_hint = ""
    if has_args:
        print("\n📋 Arguments")
        print("Describe arguments for users (e.g., '[filename]', '[source] [dest]')")
        argument_hint = prompt_user("Argument hint")

    # Get workflow
    print("\n🔄 Command Workflow")
    print("Describe what the command should do when invoked.")
    workflow = prompt_user("Workflow description")

    # Generate command content
    content = generate_command(name, description, tools, argument_hint, has_args, workflow)

    # Determine output path
    output_dir = Path.cwd() / '.claude' / 'commands'
    if not output_dir.exists():
        output_dir = Path.cwd() / 'commands'

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{name}.md"

    # Preview
    print("\n" + "=" * 70)
    print("📄 GENERATED COMMAND PREVIEW")
    print("=" * 70)
    print(content[:400] + "..." if len(content) > 400 else content)
    print("=" * 70)

    # Confirm
    save = prompt_user(f"\n💾 Save to {output_file}? (y/n)", "y")

    if save.lower() == 'y':
        output_file.write_text(content)
        print(f"\n✅ Command created: {output_file}")
        print(f"\n📝 Next steps:")
        print(f"   1. Edit {output_file} and customize the workflow")
        print(f"   2. Add detailed examples and error handling")
        print(f"   3. Validate: python validate-command.py {output_file}")
        print(f"   4. Test: /{name} [arguments]")
    else:
        print("\n❌ Cancelled. Command not saved.")

    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
