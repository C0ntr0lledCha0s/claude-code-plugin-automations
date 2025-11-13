#!/usr/bin/env python3
"""
Migrate Agent Script - Automated schema and best practice migration
Part of the agent-builder plugin for Claude Code
"""

import sys
import os
import re
import yaml
import difflib
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

def find_agent(agent_name: str) -> Optional[Path]:
    """Find agent file in common locations."""
    search_paths = [
        Path(".claude/agents"),
        Path.home() / ".claude" / "agents",
        Path("."),
    ]

    for search_path in search_paths:
        if not search_path.exists():
            continue

        agent_file = search_path / f"{agent_name}.md"
        if agent_file.exists():
            return agent_file

        for agent_file in search_path.rglob(f"{agent_name}.md"):
            if agent_file.parent.name == "agents":
                return agent_file

    return None

def detect_schema_version(content: str) -> str:
    """Detect schema version from file structure."""
    if not content.startswith('---'):
        return 'pre-1.0'

    try:
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return 'invalid'

        frontmatter = yaml.safe_load(match.group(1))

        if not frontmatter:
            return '0.x (empty frontmatter)'

        if 'name' not in frontmatter or 'description' not in frontmatter:
            return '0.x (missing required fields)'

        return '1.0 (current)'

    except Exception:
        return 'invalid'

def parse_agent(content: str) -> Tuple[Optional[Dict], str]:
    """Parse agent file into frontmatter and body."""
    if not content.startswith('---'):
        return None, content

    try:
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
        if not match:
            return None, content

        frontmatter_text, body = match.groups()
        frontmatter = yaml.safe_load(frontmatter_text)

        return frontmatter, body

    except Exception:
        return None, content

def extract_name_from_heading(body: str) -> str:
    """Extract agent name from markdown heading."""
    match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
    if match:
        name = match.group(1).strip()
        # Convert to lowercase-hyphens
        name = name.lower()
        name = re.sub(r'[^a-z0-9-]', '-', name)
        name = re.sub(r'-+', '-', name)
        name = name.strip('-')
        return name[:64]  # Max 64 chars

    return 'untitled-agent'

def extract_description(body: str) -> str:
    """Extract description from agent body."""
    # Try to find "You are..." statement
    match = re.search(r'You are (.*?)(?:[.!]|\n\n)', body, re.IGNORECASE | re.DOTALL)
    if match:
        desc = match.group(1).strip()
        return desc[:1024]  # Max 1024 chars

    # Try first paragraph
    paragraphs = [p.strip() for p in body.split('\n\n') if p.strip()]
    for para in paragraphs:
        # Skip headings
        if para.startswith('#'):
            continue
        if len(para) > 20:
            return para[:1024]

    return "Agent description needed"

def fix_agent_name(name: str) -> str:
    """Fix agent name to follow conventions."""
    name = name.lower()
    name = re.sub(r'[^a-z0-9-]', '-', name)
    name = re.sub(r'-+', '-', name)
    name = name.strip('-')
    return name[:64]

def migrate_pre_10_to_10(content: str) -> Tuple[str, List[str]]:
    """Migrate pre-1.0 agent to 1.0 schema."""
    changes = []

    # Extract name from heading
    name = extract_name_from_heading(content)
    changes.append(f"Extracted name: {name}")

    # Extract description
    description = extract_description(content)
    changes.append(f"Extracted description (first {min(len(description), 50)} chars)")

    # Create frontmatter
    frontmatter = {
        'name': name,
        'description': description,
        'tools': 'Read, Grep, Glob',
        'model': 'sonnet'
    }

    # Reconstruct
    yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    new_content = f"---\n{yaml_str}---\n{content}"

    changes.append("Added YAML frontmatter with default tools and model")

    return new_content, changes

def migrate_incomplete_to_complete(frontmatter: Dict, body: str) -> Tuple[Dict, str, List[str]]:
    """Migrate incomplete 1.0 agent to complete current standards."""
    changes = []
    new_frontmatter = frontmatter.copy()
    new_body = body

    # Fix name if needed
    if 'name' in new_frontmatter:
        original_name = new_frontmatter['name']
        fixed_name = fix_agent_name(original_name)
        if fixed_name != original_name:
            new_frontmatter['name'] = fixed_name
            changes.append(f"Fixed name: {original_name} → {fixed_name}")

    # Add description if missing
    if 'description' not in new_frontmatter or not new_frontmatter['description']:
        description = extract_description(body)
        new_frontmatter['description'] = description
        changes.append("Added description field")

    # Optimize tools if over-permissioned
    if 'tools' in new_frontmatter:
        tools = new_frontmatter['tools']
        if 'Bash' in tools and 'validation' not in body.lower():
            # Remove Bash if no validation docs
            new_tools = ', '.join([t.strip() for t in tools.split(',') if t.strip() != 'Bash'])
            new_frontmatter['tools'] = new_tools
            changes.append("Removed Bash (no validation documented)")

        if 'Write' in tools and 'Edit' in tools:
            # Remove Write if both present (Edit is more specific)
            new_tools = ', '.join([t.strip() for t in tools.split(',') if t.strip() != 'Write'])
            new_frontmatter['tools'] = new_tools
            changes.append("Removed Write (Edit already present)")

    # Update model to alias if specific version
    if 'model' in new_frontmatter:
        model = new_frontmatter['model']
        if 'claude-sonnet' in model:
            new_frontmatter['model'] = 'sonnet'
            changes.append(f"Updated model: {model} → sonnet (version alias)")
        elif 'claude-opus' in model:
            new_frontmatter['model'] = 'opus'
            changes.append(f"Updated model: {model} → opus (version alias)")
        elif 'claude-haiku' in model:
            new_frontmatter['model'] = 'haiku'
            changes.append(f"Updated model: {model} → haiku (version alias)")

    # Add missing content sections
    sections_to_add = []

    if '## Your Capabilities' not in new_body and '## Capabilities' not in new_body:
        sections_to_add.append("Capabilities")

    if '## Your Workflow' not in new_body and '## Workflow' not in new_body:
        sections_to_add.append("Workflow")

    if '## Example' not in new_body:
        sections_to_add.append("Examples")

    if sections_to_add:
        # Add template sections
        additions = []

        if "Capabilities" in sections_to_add:
            additions.append("""
## Your Capabilities

1. [Capability 1 - describe what you can do]
2. [Capability 2 - describe what you can do]
3. [Capability 3 - describe what you can do]
""")

        if "Workflow" in sections_to_add:
            additions.append("""
## Your Workflow

When invoked, follow these steps:

1. **Step 1**: [Action and rationale]
2. **Step 2**: [Action and rationale]
3. **Step 3**: [Action and rationale]
""")

        if "Examples" in sections_to_add:
            additions.append("""
## Examples

### Example 1: [Scenario Name]

**Task**: [What user asks for]
**Process**: [How you approach it]
**Output**: [What you deliver]

### Example 2: [Scenario Name]

**Task**: [What user asks for]
**Process**: [How you approach it]
**Output**: [What you deliver]
""")

        # Append to body
        new_body = body.rstrip() + '\n\n' + '\n'.join(additions)
        changes.append(f"Added template sections: {', '.join(sections_to_add)}")

    return new_frontmatter, new_body, changes

def reconstruct_agent(frontmatter: Dict, body: str) -> str:
    """Reconstruct agent file from frontmatter and body."""
    yaml_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
    return f"---\n{yaml_str}---\n{body}"

def show_diff(original: str, migrated: str, file_name: str):
    """Show diff of changes."""
    print(f"\n{'='*60}")
    print(f"Migration Diff: {file_name}")
    print(f"{'='*60}\n")

    diff = difflib.unified_diff(
        original.splitlines(keepends=True),
        migrated.splitlines(keepends=True),
        fromfile=f"{file_name} (original)",
        tofile=f"{file_name} (migrated)",
        lineterm=''
    )

    for line in diff:
        if line.startswith('+') and not line.startswith('+++'):
            print(f"\033[92m{line}\033[0m", end='')
        elif line.startswith('-') and not line.startswith('---'):
            print(f"\033[91m{line}\033[0m", end='')
        elif line.startswith('@@'):
            print(f"\033[94m{line}\033[0m", end='')
        else:
            print(line, end='')

    print(f"\n{'='*60}\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 migrate-agent.py <agent-name>")
        print("\nExample: python3 migrate-agent.py code-reviewer")
        sys.exit(1)

    agent_name = sys.argv[1].replace('.md', '')

    # Find agent
    print(f"Searching for agent: {agent_name}...")
    agent_path = find_agent(agent_name)

    if not agent_path:
        print(f"❌ Agent not found: {agent_name}")
        sys.exit(1)

    print(f"✓ Found: {agent_path}\n")

    # Read original
    original_content = agent_path.read_text()

    # Detect version
    version = detect_schema_version(original_content)
    print(f"Detected schema version: {version}\n")

    # Determine migration path
    all_changes = []
    migrated_content = original_content

    if version == 'pre-1.0':
        print("Migration path: pre-1.0 → 1.0")
        print("  1. Add YAML frontmatter")
        print("  2. Extract name and description")
        print("  3. Add default tools and model\n")

        migrated_content, changes = migrate_pre_10_to_10(original_content)
        all_changes.extend(changes)

    elif version.startswith('0.x') or version.startswith('1.0'):
        print("Migration path: Complete to current standards")
        print("  1. Fix schema issues")
        print("  2. Optimize tool permissions")
        print("  3. Update model to alias")
        print("  4. Add missing content sections\n")

        frontmatter, body = parse_agent(original_content)
        if frontmatter:
            new_frontmatter, new_body, changes = migrate_incomplete_to_complete(frontmatter, body)
            migrated_content = reconstruct_agent(new_frontmatter, new_body)
            all_changes.extend(changes)
        else:
            print("❌ Failed to parse agent")
            sys.exit(1)

    elif version == 'invalid':
        print("❌ Invalid agent format - cannot migrate automatically")
        print("Please fix syntax errors first")
        sys.exit(1)

    else:
        print("✓ Agent is already at current version")
        print("No migration needed")
        sys.exit(0)

    # Show changes
    print("="*60)
    print("Changes to Apply")
    print("="*60)
    for i, change in enumerate(all_changes, 1):
        print(f"{i}. {change}")
    print()

    # Show diff
    show_diff(original_content, migrated_content, agent_path.name)

    # Confirm
    confirm = input("Apply migration? (y/n): ").strip().lower()

    if confirm == 'y':
        # Backup
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = agent_path.with_suffix(f'.md.pre-migration-{timestamp}')
        backup_path.write_text(original_content)

        # Write migrated
        agent_path.write_text(migrated_content)

        print(f"\n✅ Migration complete!")
        print(f"   Backup: {backup_path}")
        print(f"   Updated: {agent_path}")

        # Run validation
        print("\n" + "="*60)
        print("Validation")
        print("="*60)
        validate_script = Path(__file__).parent / 'validate-agent.py'
        if validate_script.exists():
            os.system(f"python3 {validate_script} {agent_path}")

        # Run enhancement
        print("\n" + "="*60)
        print("Enhancement Score")
        print("="*60)
        enhance_script = Path(__file__).parent / 'enhance-agent.py'
        if enhance_script.exists():
            os.system(f"python3 {enhance_script} {agent_name}")

        print("\n" + "="*60)
        print("Next Steps")
        print("="*60)
        print("1. Review the migrated agent")
        print("2. Test agent functionality")
        print("3. Fill in template placeholders (marked with [])")
        print(f"4. Commit: git add {agent_path} && git commit")
        print(f"\nRollback: mv {backup_path} {agent_path}")

    else:
        print("\n✓ Migration cancelled")

if __name__ == '__main__':
    main()
