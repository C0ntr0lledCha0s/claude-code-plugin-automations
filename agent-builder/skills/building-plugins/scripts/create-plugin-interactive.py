#!/usr/bin/env python3
"""
Interactive plugin creator script.
Creates a complete plugin structure with user-guided configuration.
This script can be called by the /agent-builder:plugins:new command
or run directly for manual plugin creation.
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional


def print_header(title: str):
    """Print a formatted header."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}\n")


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'-' * 60}")
    print(f"  {title}")
    print(f"{'-' * 60}\n")


def validate_plugin_name(name: str) -> tuple[bool, Optional[str]]:
    """
    Validate plugin name follows conventions.

    Returns:
        (is_valid, error_message)
    """
    if not name:
        return False, "Plugin name cannot be empty"

    if len(name) > 64:
        return False, f"Plugin name too long ({len(name)} chars, max 64)"

    if not re.match(r'^[a-z0-9-]+$', name):
        return False, "Plugin name must be lowercase letters, numbers, and hyphens only"

    if '_' in name:
        return False, "Plugin name cannot contain underscores (use hyphens instead)"

    if name != name.lower():
        return False, "Plugin name must be lowercase"

    if name.startswith('-') or name.endswith('-'):
        return False, "Plugin name cannot start or end with a hyphen"

    if '--' in name:
        return False, "Plugin name cannot contain consecutive hyphens"

    return True, None


def get_plugin_name() -> str:
    """Interactively get and validate plugin name."""
    print_section("Plugin Name")
    print("Plugin name must be:")
    print("  - lowercase-hyphens only (e.g., 'my-plugin')")
    print("  - max 64 characters")
    print("  - descriptive and unique")
    print("\nExamples: code-review-suite, data-analysis-tools, git-workflow-automation\n")

    while True:
        name = input("Plugin name: ").strip()
        is_valid, error = validate_plugin_name(name)

        if is_valid:
            return name
        else:
            print(f"❌ Invalid name: {error}")
            print("Please try again.\n")


def get_plugin_description() -> str:
    """Get plugin description."""
    print_section("Plugin Description")
    print("Brief description of what your plugin does (20-1024 chars)\n")

    while True:
        description = input("Description: ").strip()

        if len(description) < 20:
            print(f"❌ Description too short ({len(description)} chars, min 20)")
            continue

        if len(description) > 1024:
            print(f"❌ Description too long ({len(description)} chars, max 1024)")
            continue

        return description


def get_author_info() -> Dict[str, str]:
    """Get author information."""
    print_section("Author Information")

    name = input("Author name: ").strip()
    email = input("Author email (optional): ").strip()
    url = input("Author URL (e.g., GitHub profile): ").strip()

    author = {"name": name}
    if email:
        author["email"] = email
    if url:
        author["url"] = url

    return author


def get_keywords() -> List[str]:
    """Get plugin keywords."""
    print_section("Keywords")
    print("Enter 3-10 keywords for better discoverability")
    print("(comma-separated, e.g., 'automation, productivity, workflow')\n")

    while True:
        keywords_str = input("Keywords: ").strip()
        keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]

        if len(keywords) < 3:
            print(f"❌ Please provide at least 3 keywords (you provided {len(keywords)})")
            continue

        if len(keywords) > 10:
            print(f"⚠️  You provided {len(keywords)} keywords. Consider using 3-10 for best results.")
            confirm = input("Continue anyway? (y/n): ").strip().lower()
            if confirm != 'y':
                continue

        return keywords


def select_category() -> str:
    """Select plugin category."""
    print_section("Plugin Category")
    categories = {
        "1": ("development-tools", "Code generation, testing, linting, formatting"),
        "2": ("automation", "Workflow automation, task automation"),
        "3": ("integration", "External service integrations, APIs"),
        "4": ("productivity", "General productivity enhancements"),
        "5": ("security", "Security scanning, vulnerability detection"),
        "6": ("data", "Data analysis, processing, visualization"),
        "7": ("documentation", "Documentation generation, maintenance"),
    }

    print("Select the category that best describes your plugin:\n")
    for key, (cat, desc) in categories.items():
        print(f"  {key}. {cat}")
        print(f"     {desc}")

    while True:
        choice = input("\nCategory (1-7): ").strip()
        if choice in categories:
            return categories[choice][0]
        print("❌ Invalid choice. Please select 1-7.")


def select_components() -> Dict[str, bool]:
    """Select which components to include."""
    print_section("Plugin Components")
    print("Which components should this plugin include?\n")

    components = {}

    # Agents
    print("1. Agents - Specialized subagents for complex tasks")
    choice = input("   Include agents? (y/n): ").strip().lower()
    components['agents'] = choice == 'y'

    # Skills
    print("\n2. Skills - Auto-invoked expertise modules")
    choice = input("   Include skills? (y/n): ").strip().lower()
    components['skills'] = choice == 'y'

    # Commands
    print("\n3. Commands - User-triggered slash commands")
    choice = input("   Include commands? (y/n): ").strip().lower()
    components['commands'] = choice == 'y'

    # Hooks
    print("\n4. Hooks - Event-driven automation")
    choice = input("   Include hooks? (y/n): ").strip().lower()
    components['hooks'] = choice == 'y'

    if not any(components.values()):
        print("\n⚠️  Warning: You didn't select any components!")
        print("A plugin should have at least one component.")
        confirm = input("Continue anyway? (y/n): ").strip().lower()
        if confirm != 'y':
            return select_components()

    return components


def create_plugin_structure(plugin_name: str, components: Dict[str, bool]) -> Path:
    """Create plugin directory structure."""
    plugin_dir = Path(plugin_name)

    if plugin_dir.exists():
        print(f"\n⚠️  Directory '{plugin_name}' already exists!")
        choice = input("Overwrite? (y/n): ").strip().lower()
        if choice != 'y':
            print("Aborting.")
            sys.exit(0)
        print("Removing existing directory...")
        import shutil
        shutil.rmtree(plugin_dir)

    print(f"\nCreating plugin structure in '{plugin_name}/'...")

    # Create base structure
    (plugin_dir / ".claude-plugin").mkdir(parents=True)

    # Create component directories based on selection
    if components.get('agents'):
        (plugin_dir / "agents").mkdir()
        print("  ✓ Created agents/")

    if components.get('skills'):
        (plugin_dir / "skills").mkdir()
        print("  ✓ Created skills/")

    if components.get('commands'):
        (plugin_dir / "commands").mkdir()
        print("  ✓ Created commands/")

    if components.get('hooks'):
        (plugin_dir / "hooks").mkdir()
        print("  ✓ Created hooks/")

    # Always create scripts directory
    (plugin_dir / "scripts").mkdir()
    print("  ✓ Created scripts/")

    return plugin_dir


def create_plugin_json(
    plugin_dir: Path,
    plugin_name: str,
    description: str,
    author: Dict[str, str],
    keywords: List[str],
    category: str,
    components: Dict[str, bool]
) -> None:
    """Create plugin.json manifest."""
    manifest = {
        "name": plugin_name,
        "version": "1.0.0",
        "description": description,
        "author": author,
        "license": "MIT",
        "keywords": keywords,
    }

    # Add repository URLs if author has URL
    if "url" in author:
        base_url = author["url"].rstrip('/')
        manifest["homepage"] = f"{base_url}/{plugin_name}"
        manifest["repository"] = f"{base_url}/{plugin_name}"

    # Add component references
    if components.get('agents'):
        manifest["agents"] = "./agents/"

    if components.get('skills'):
        manifest["skills"] = "./skills/"

    if components.get('commands'):
        manifest["commands"] = "./commands/"

    if components.get('hooks'):
        manifest["hooks"] = ["./hooks/hooks.json"]

    # Write plugin.json
    plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"
    with open(plugin_json_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"\n  ✓ Created .claude-plugin/plugin.json")


def create_readme(
    plugin_dir: Path,
    plugin_name: str,
    description: str,
    author: Dict[str, str],
    components: Dict[str, bool]
) -> None:
    """Create README.md."""
    readme_content = f"""# {plugin_name}

{description}

## Features

- (Add key features here)

## Installation

### Manual Installation

1. Clone or download this plugin
2. Symlink to Claude's plugin directory:
   ```bash
   ln -s $(pwd)/{plugin_name} ~/.claude/plugins/{plugin_name}
   ```
3. Restart Claude Code

## Components
"""

    if components.get('agents'):
        readme_content += "\n### Agents\n\n- (List agents here)\n"

    if components.get('skills'):
        readme_content += "\n### Skills\n\n- (List skills here)\n"

    if components.get('commands'):
        readme_content += "\n### Commands\n\n- (List commands here)\n"

    if components.get('hooks'):
        readme_content += "\n### Hooks\n\n- (List hooks here)\n"

    readme_content += f"""
## Usage

(Add usage examples here)

## Requirements

- Claude Code v1.0.0 or higher

## License

MIT License

## Author

**{author.get('name', 'Unknown')}**
"""

    if author.get('email'):
        readme_content += f"- Email: {author['email']}\n"

    if author.get('url'):
        readme_content += f"- GitHub: {author['url']}\n"

    readme_path = plugin_dir / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)

    print(f"  ✓ Created README.md")


def print_summary(
    plugin_name: str,
    plugin_dir: Path,
    components: Dict[str, bool]
) -> None:
    """Print creation summary and next steps."""
    print_header("Plugin Created Successfully!")

    print(f"📦 Plugin: {plugin_name}")
    print(f"📁 Location: {plugin_dir.absolute()}\n")

    print("📂 Structure:")
    print(f"  {plugin_name}/")
    print(f"  ├── .claude-plugin/")
    print(f"  │   └── plugin.json")

    if components.get('agents'):
        print(f"  ├── agents/")
    if components.get('skills'):
        print(f"  ├── skills/")
    if components.get('commands'):
        print(f"  ├── commands/")
    if components.get('hooks'):
        print(f"  ├── hooks/")

    print(f"  ├── scripts/")
    print(f"  └── README.md")

    print("\n📝 Next Steps:\n")

    step = 1

    if components.get('agents'):
        print(f"{step}. Create agents:")
        print(f"   cd {plugin_name}/agents")
        print(f"   # Use /agent-builder:agents:new <agent-name>")
        step += 1

    if components.get('skills'):
        print(f"\n{step}. Create skills:")
        print(f"   cd {plugin_name}/skills")
        print(f"   # Use /agent-builder:skills:new <skill-name>")
        step += 1

    if components.get('commands'):
        print(f"\n{step}. Create commands:")
        print(f"   cd {plugin_name}/commands")
        print(f"   # Use /agent-builder:commands:new <command-name>")
        step += 1

    if components.get('hooks'):
        print(f"\n{step}. Create hooks:")
        print(f"   cd {plugin_name}/hooks")
        print(f"   # Use /agent-builder:hooks:new <hook-name>")
        step += 1

    print(f"\n{step}. Test the plugin:")
    print(f"   ln -s $(pwd)/{plugin_name} ~/.claude/plugins/{plugin_name}")
    print(f"   # Restart Claude Code")
    step += 1

    print(f"\n{step}. Validate:")
    print(f"   python3 agent-builder/skills/building-plugins/scripts/validate-plugin.py {plugin_name}/")
    step += 1

    print(f"\n{step}. Update README.md with:")
    print(f"   - Component descriptions")
    print(f"   - Usage examples")
    print(f"   - Configuration options")

    print("\n" + "=" * 60)


def main():
    """Main interactive plugin creation flow."""
    print_header("Claude Code Plugin Creator")
    print("This tool will guide you through creating a new plugin.\n")

    # Gather information
    plugin_name = get_plugin_name()
    description = get_plugin_description()
    author = get_author_info()
    keywords = get_keywords()
    category = select_category()
    components = select_components()

    # Confirm before creating
    print_section("Confirmation")
    print(f"Plugin name: {plugin_name}")
    print(f"Description: {description}")
    print(f"Author: {author['name']}")
    print(f"Category: {category}")
    print(f"Keywords: {', '.join(keywords)}")
    print(f"\nComponents:")
    for comp, enabled in components.items():
        status = "✓" if enabled else "✗"
        print(f"  {status} {comp}")

    confirm = input("\nCreate plugin? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Aborting.")
        sys.exit(0)

    # Create plugin
    plugin_dir = create_plugin_structure(plugin_name, components)
    create_plugin_json(plugin_dir, plugin_name, description, author, keywords, category, components)
    create_readme(plugin_dir, plugin_name, description, author, components)

    # Print summary
    print_summary(plugin_name, plugin_dir, components)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAborted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
