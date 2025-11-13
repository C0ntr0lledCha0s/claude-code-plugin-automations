#!/usr/bin/env python3
"""
Compare Commands Script - Side-by-side comparison tool
Part of the agent-builder plugin for Claude Code

Compare two command files to see differences in configuration and content.
"""

import sys
import re
import yaml
import difflib
from pathlib import Path
from typing import Dict, Tuple, Optional

def find_command(command_name: str) -> Optional[Path]:
    """Find command file in common locations."""
    search_paths = [
        Path(".claude/commands"),
        Path.home() / ".claude" / "commands",
        Path("."),
    ]

    for search_path in search_paths:
        if not search_path.exists():
            continue

        # Direct match
        command_file = search_path / f"{command_name}.md"
        if command_file.exists():
            return command_file

        # Search in subdirectories
        for command_file in search_path.rglob(f"{command_name}.md"):
            if command_file.parent.name == "commands":
                return command_file

    return None

def parse_command(file_path: Path) -> Tuple[Dict, str]:
    """Parse command file into frontmatter and body."""
    content = file_path.read_text()

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        raise ValueError("Invalid command file: missing YAML frontmatter")

    frontmatter_text, body = match.groups()
    frontmatter = yaml.safe_load(frontmatter_text)

    return frontmatter, body

def compare_frontmatter(fm1: Dict, fm2: Dict, name1: str, name2: str):
    """Compare frontmatter fields."""
    print(f"\n{'='*70}")
    print("FRONTMATTER COMPARISON")
    print(f"{'='*70}\n")

    # Collect all keys
    all_keys = set(fm1.keys()) | set(fm2.keys())

    print(f"{'Field':<20} {name1:<25} {name2:<25}")
    print("-" * 70)

    for key in sorted(all_keys):
        val1 = fm1.get(key, '(not set)')
        val2 = fm2.get(key, '(not set)')

        # Truncate long values
        val1_str = str(val1)[:23] if val1 != '(not set)' else val1
        val2_str = str(val2)[:23] if val2 != '(not set)' else val2

        # Highlight differences
        if val1 != val2:
            marker = "⚠️ "
        else:
            marker = "✓ "

        print(f"{marker}{key:<18} {val1_str:<25} {val2_str:<25}")

def compare_structure(body1: str, body2: str, name1: str, name2: str):
    """Compare document structure (headings)."""
    print(f"\n{'='*70}")
    print("STRUCTURE COMPARISON (Headings)")
    print(f"{'='*70}\n")

    # Extract headings
    headings1 = re.findall(r'^(#{1,3})\s+(.+)$', body1, re.MULTILINE)
    headings2 = re.findall(r'^(#{1,3})\s+(.+)$', body2, re.MULTILINE)

    print(f"{name1}:")
    if headings1:
        for level, heading in headings1:
            indent = "  " * (len(level) - 1)
            print(f"  {indent}• {heading}")
    else:
        print("  (no headings)")

    print(f"\n{name2}:")
    if headings2:
        for level, heading in headings2:
            indent = "  " * (len(level) - 1)
            print(f"  {indent}• {heading}")
    else:
        print("  (no headings)")

def compare_content(body1: str, body2: str, name1: str, name2: str):
    """Show unified diff of content."""
    print(f"\n{'='*70}")
    print("CONTENT DIFF")
    print(f"{'='*70}\n")

    diff = difflib.unified_diff(
        body1.splitlines(keepends=True),
        body2.splitlines(keepends=True),
        fromfile=name1,
        tofile=name2,
        lineterm=''
    )

    has_diff = False
    line_count = 0
    for line in diff:
        has_diff = True
        line_count += 1

        # Limit output for very large diffs
        if line_count > 100:
            print("\n... (diff truncated, too many lines) ...")
            break

        if line.startswith('+') and not line.startswith('+++'):
            print(f"\033[92m{line}\033[0m", end='')  # Green
        elif line.startswith('-') and not line.startswith('---'):
            print(f"\033[91m{line}\033[0m", end='')  # Red
        elif line.startswith('@@'):
            print(f"\033[94m{line}\033[0m", end='')  # Blue
        else:
            print(line, end='')

    if not has_diff:
        print("✅ Content is identical")

def compare_metrics(body1: str, body2: str, name1: str, name2: str):
    """Compare basic metrics."""
    print(f"\n{'='*70}")
    print("METRICS COMPARISON")
    print(f"{'='*70}\n")

    metrics1 = {
        'word_count': len(body1.split()),
        'line_count': body1.count('\n'),
        'heading_count': len(re.findall(r'^#{1,3}\s+', body1, re.MULTILINE)),
        'code_blocks': body1.count('```') // 2,
        'list_items': len(re.findall(r'^\s*[-*]\s+', body1, re.MULTILINE)),
    }

    metrics2 = {
        'word_count': len(body2.split()),
        'line_count': body2.count('\n'),
        'heading_count': len(re.findall(r'^#{1,3}\s+', body2, re.MULTILINE)),
        'code_blocks': body2.count('```') // 2,
        'list_items': len(re.findall(r'^\s*[-*]\s+', body2, re.MULTILINE)),
    }

    print(f"{'Metric':<20} {name1:<15} {name2:<15} {'Difference':<15}")
    print("-" * 70)

    for metric in metrics1.keys():
        val1 = metrics1[metric]
        val2 = metrics2[metric]
        diff = val2 - val1

        diff_str = f"{diff:+d}" if diff != 0 else "same"
        marker = "  " if diff == 0 else "⚠️ "

        print(f"{marker}{metric:<18} {val1:<15} {val2:<15} {diff_str:<15}")

def main():
    """
    Usage:
        python3 compare-commands.py <command1> <command2>

    Example:
        python3 compare-commands.py new-agent create-agent
    """
    if len(sys.argv) < 3:
        print("Command Comparison Tool")
        print("="*70)
        print("\nUsage:")
        print("  python3 compare-commands.py <command1> <command2>")
        print("\nExample:")
        print("  python3 compare-commands.py new-agent create-agent")
        print("\nCompares:")
        print("  • Frontmatter fields")
        print("  • Document structure")
        print("  • Content differences")
        print("  • Metrics (word count, headings, etc.)")
        sys.exit(1)

    command1_name = sys.argv[1].replace('.md', '')
    command2_name = sys.argv[2].replace('.md', '')

    # Find commands
    print(f"Searching for commands...")

    command1_path = find_command(command1_name)
    if not command1_path:
        print(f"❌ Command not found: {command1_name}")
        sys.exit(1)

    command2_path = find_command(command2_name)
    if not command2_path:
        print(f"❌ Command not found: {command2_name}")
        sys.exit(1)

    print(f"✓ Found: {command1_path}")
    print(f"✓ Found: {command2_path}")

    # Parse commands
    try:
        fm1, body1 = parse_command(command1_path)
        fm2, body2 = parse_command(command2_path)
    except Exception as e:
        print(f"❌ Failed to parse commands: {e}")
        sys.exit(1)

    # Header
    print(f"\n{'='*70}")
    print("COMMAND COMPARISON")
    print(f"{'='*70}")
    print(f"\nCommand 1: {command1_name}")
    print(f"  Location: {command1_path}")
    print(f"\nCommand 2: {command2_name}")
    print(f"  Location: {command2_path}")

    # Compare
    compare_frontmatter(fm1, fm2, command1_name, command2_name)
    compare_structure(body1, body2, command1_name, command2_name)
    compare_metrics(body1, body2, command1_name, command2_name)
    compare_content(body1, body2, command1_name, command2_name)

    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}\n")

    # Check if commands are similar
    fm_diff = set(fm1.keys()) ^ set(fm2.keys())  # Symmetric difference
    if not fm_diff and all(fm1.get(k) == fm2.get(k) for k in fm1.keys()):
        print("✅ Frontmatter: Identical")
    else:
        print("⚠️  Frontmatter: Different")

    if body1 == body2:
        print("✅ Content: Identical")
    else:
        similarity = difflib.SequenceMatcher(None, body1, body2).ratio()
        print(f"⚠️  Content: {similarity*100:.1f}% similar")

    print()

if __name__ == '__main__':
    main()
