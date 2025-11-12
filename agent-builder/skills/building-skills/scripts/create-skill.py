#!/usr/bin/env python3
"""
Skill Generator Script
Creates a new Claude Code skill with complete directory structure
"""

import sys
import os
import re
from pathlib import Path


def validate_name(name):
    """Validate skill name follows conventions"""
    if not re.match(r'^[a-z0-9-]+$', name):
        return False, "Name must be lowercase letters, numbers, and hyphens only"
    if len(name) > 64:
        return False, f"Name too long ({len(name)} chars, max 64)"
    if '_' in name:
        return False, "Use hyphens instead of underscores"

    # Recommend gerund form
    if not name.endswith('ing') and not any(word in name for word in ['analyzing', 'building', 'creating', 'generating', 'processing', 'writing']):
        print(f"💡 Tip: Skill names typically use gerund form (verb + -ing)")
        print(f"   Consider: '{name}' → 'analyzing-{name}', 'generating-{name}', etc.")

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


def select_resources():
    """Select which resource directories to create"""
    print("\n📁 Resource Directories")
    print("Which directories does this skill need?")

    create_scripts = prompt_user("  Create scripts/ directory? (y/n)", "y").lower() == 'y'
    create_references = prompt_user("  Create references/ directory? (y/n)", "y").lower() == 'y'
    create_assets = prompt_user("  Create assets/ directory? (y/n)", "n").lower() == 'y'

    return create_scripts, create_references, create_assets


def generate_skill_md(name, description, version, tools, overview, capabilities, when_to_use, resources_info):
    """Generate SKILL.md content"""

    # Build frontmatter
    frontmatter = [
        "---",
        f"name: {name}",
        f"description: {description}",
        f"version: {version}"
    ]

    if tools:
        frontmatter.append(f"allowed-tools: {tools}")

    # Note: Skills do not support the 'model' field - only agents do

    frontmatter.append("---")

    # Build body
    skill_name_title = ' '.join(word.capitalize() for word in name.split('-'))

    body = f"""
# {skill_name_title} Skill

{overview}

## Your Expertise

You specialize in:
{capabilities}

## When to Use This Skill

Claude should automatically invoke this skill when:
{when_to_use}

## Your Capabilities

Provide detailed description of what this skill can do.

## How to Use This Skill

When this skill is activated:

1. **Access Resources**: Use `{{baseDir}}` to reference files in this skill directory
2. **Progressive Disclosure**: Start with core expertise, discover resources as needed
3. **Provide Context**: Offer relevant information and guidance automatically

{resources_info}

## Examples

### Example 1: [Common Scenario]
When the user [specific action or request]:

1. Automatically recognize the need for this skill
2. [Step-by-step approach]
3. Provide actionable guidance

### Example 2: [Another Scenario]
When encountering [specific situation]:

1. Invoke this skill automatically
2. [Step-by-step approach]
3. Deliver results with context

## Best Practices

- Always [important guideline]
- Prefer [recommended approach]
- Avoid [what to avoid]
- Consider [important considerations]

## Important Notes

- This skill is automatically invoked by Claude when relevant
- Resources are discovered progressively as needed
- Use `{{baseDir}}` variable to reference skill resources
"""

    return '\n'.join(frontmatter) + body


def create_skill_structure(base_dir, name, create_scripts, create_references, create_assets):
    """Create skill directory structure"""

    skill_dir = base_dir / name
    skill_dir.mkdir(parents=True, exist_ok=True)

    # Create resource directories
    if create_scripts:
        (skill_dir / 'scripts').mkdir(exist_ok=True)
        # Create example script
        example_script = skill_dir / 'scripts' / 'example-helper.py'
        example_script.write_text('''#!/usr/bin/env python3
"""
Example helper script for this skill.
Replace with actual functionality.
"""

import sys

def main():
    print("Example helper script")
    print(f"Arguments: {sys.argv[1:]}")

if __name__ == '__main__':
    main()
''')
        example_script.chmod(0o755)

    if create_references:
        (skill_dir / 'references').mkdir(exist_ok=True)
        # Create example reference doc
        readme = skill_dir / 'references' / 'README.md'
        readme.write_text(f'''# {name.replace('-', ' ').title()} Reference

Add reference documentation here:
- API documentation
- Examples
- Best practices guides
- External resources
''')

    if create_assets:
        (skill_dir / 'assets').mkdir(exist_ok=True)
        # Create example template
        template = skill_dir / 'assets' / 'example-template.txt'
        template.write_text('# Example Template\n\nReplace with actual template content.\n')

    return skill_dir


def main():
    print("=" * 70)
    print("🛠️  CLAUDE CODE SKILL GENERATOR")
    print("=" * 70)
    print()

    # Get skill name
    while True:
        name = prompt_user("Skill name (lowercase-hyphens, gerund form, e.g., 'analyzing-data')")
        valid, message = validate_name(name)
        if valid:
            break
        print(f"❌ {message}")

    # Get description
    print("\n📝 Description (max 1024 chars)")
    print("IMPORTANT: Describe WHAT the skill does and WHEN Claude should use it.")
    print("Be specific about auto-invocation triggers!")
    description = prompt_user("Description")

    if len(description) > 1024:
        print(f"⚠️  Description is {len(description)} chars, truncating to 1024...")
        description = description[:1024]

    # Get version
    version = prompt_user("Version", "1.0.0")

    # Get allowed tools
    print("\n🔧 Allowed Tools (pre-approved, no permission prompts)")
    print("Common: Read, Grep, Glob (read-only)")
    print("        Read, Grep, Glob, Bash (with execution)")
    print("        Read, Write, Edit, Grep, Glob (with file modification)")
    tools = prompt_user("Allowed tools", "Read, Grep, Glob")

    # Note: Skills do not support model specification - they inherit from parent context

    # Get overview
    print("\n📋 Skill Overview")
    overview = prompt_user("One-paragraph overview of this skill's expertise")

    # Get capabilities
    print("\n💪 Core Capabilities")
    print("List key capabilities. Enter blank line when done.")
    capabilities_list = []
    count = 1
    while True:
        cap = input(f"  {count}. ").strip()
        if not cap:
            break
        capabilities_list.append(f"- {cap}")
        count += 1
    capabilities = '\n'.join(capabilities_list) if capabilities_list else "- [Describe main capability]"

    # Get auto-invocation triggers
    print("\n🎯 Auto-Invocation Triggers")
    print("When should Claude automatically use this skill?")
    print("Enter triggers, one per line. Blank line when done.")
    triggers_list = []
    count = 1
    while True:
        trigger = input(f"  {count}. ").strip()
        if not trigger:
            break
        triggers_list.append(f"- {trigger}")
        count += 1
    when_to_use = '\n'.join(triggers_list) if triggers_list else "- [When user asks about...]\n- [When task involves...]\n- [When specific patterns detected...]"

    # Select resource directories
    create_scripts, create_references, create_assets = select_resources()

    # Build resources info
    resources_info = "## Resources Available\n\n"
    if create_scripts:
        resources_info += "### Scripts\nLocated in `{baseDir}/scripts/`:\n- **example-helper.py**: [Describe functionality]\n\n"
    if create_references:
        resources_info += "### References\nLocated in `{baseDir}/references/`:\n- **README.md**: Reference documentation\n\n"
    if create_assets:
        resources_info += "### Assets\nLocated in `{baseDir}/assets/`:\n- **example-template.txt**: Template for [use case]\n\n"

    # Determine output directory
    output_dir = Path.cwd() / '.claude' / 'skills'
    if not output_dir.exists():
        output_dir = Path.cwd() / 'skills'

    output_dir.mkdir(parents=True, exist_ok=True)

    # Create skill structure
    skill_dir = create_skill_structure(output_dir, name, create_scripts, create_references, create_assets)

    # Generate SKILL.md
    content = generate_skill_md(name, description, version, tools, overview, capabilities, when_to_use, resources_info)
    skill_md = skill_dir / 'SKILL.md'
    skill_md.write_text(content)

    print("\n" + "=" * 70)
    print(f"✅ Skill created: {skill_dir}")
    print("=" * 70)
    print(f"\nDirectory structure:")
    print(f"  {skill_dir}/")
    print(f"  ├── SKILL.md")
    if create_scripts:
        print(f"  ├── scripts/")
        print(f"  │   └── example-helper.py")
    if create_references:
        print(f"  ├── references/")
        print(f"  │   └── README.md")
    if create_assets:
        print(f"  └── assets/")
        print(f"      └── example-template.txt")

    print(f"\n📝 Next steps:")
    print(f"   1. Edit {skill_md} and customize content")
    print(f"   2. Add actual scripts, references, and templates")
    print(f"   3. Update SKILL.md to reference your resources using {{baseDir}}")
    print(f"   4. Validate: python validate-skill.py {skill_dir}")
    print(f"   5. Test auto-invocation by triggering the skill")
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
