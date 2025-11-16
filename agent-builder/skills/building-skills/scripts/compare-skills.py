#!/usr/bin/env python3
"""
Compare Skills Script - Side-by-side comparison tool
Part of the agent-builder plugin for Claude Code

Compare two skill directories to see differences in configuration, structure, and content.
"""

import sys
import re
import yaml
import difflib
from pathlib import Path
from typing import Dict, Tuple, Optional, List

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

        # Direct match
        skill_dir = search_path / skill_name
        if skill_dir.exists() and skill_dir.is_dir():
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                return skill_dir

        # Search in subdirectories (plugin skills)
        for skill_dir in search_path.rglob(skill_name):
            if skill_dir.is_dir() and skill_dir.parent.name == "skills":
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    return skill_dir

    return None

def parse_skill(skill_dir: Path) -> Tuple[Dict, str]:
    """Parse SKILL.md file into frontmatter and body."""
    skill_md = skill_dir / "SKILL.md"
    content = skill_md.read_text()

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        raise ValueError("Invalid SKILL.md: missing YAML frontmatter")

    frontmatter_text, body = match.groups()
    frontmatter = yaml.safe_load(frontmatter_text)

    return frontmatter, body

def analyze_directory_structure(skill_dir: Path) -> Dict:
    """Analyze the directory structure of a skill."""
    structure = {
        'has_scripts': (skill_dir / "scripts").exists(),
        'has_references': (skill_dir / "references").exists(),
        'has_templates': (skill_dir / "templates").exists(),
        'has_assets': (skill_dir / "assets").exists(),
        'script_count': 0,
        'reference_count': 0,
        'template_count': 0,
        'asset_count': 0,
    }

    if structure['has_scripts']:
        scripts_dir = skill_dir / "scripts"
        structure['script_count'] = len(list(scripts_dir.glob("*")))

    if structure['has_references']:
        references_dir = skill_dir / "references"
        structure['reference_count'] = len(list(references_dir.glob("*.md")))

    if structure['has_templates']:
        templates_dir = skill_dir / "templates"
        structure['template_count'] = len(list(templates_dir.glob("*")))

    if structure['has_assets']:
        assets_dir = skill_dir / "assets"
        structure['asset_count'] = len(list(assets_dir.glob("*")))

    return structure

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

    # Highlight critical field: model
    if 'model' in fm1 or 'model' in fm2:
        print("\n❌ CRITICAL: One or both skills have 'model' field (not supported)")

def compare_directory_structure(struct1: Dict, struct2: Dict, name1: str, name2: str):
    """Compare directory structures."""
    print(f"\n{'='*70}")
    print("DIRECTORY STRUCTURE COMPARISON")
    print(f"{'='*70}\n")

    print(f"{name1}:")
    print(f"  ✓ SKILL.md")
    print(f"  {'✓' if struct1['has_scripts'] else '✗'} scripts/ ({struct1['script_count']} files)")
    print(f"  {'✓' if struct1['has_references'] else '✗'} references/ ({struct1['reference_count']} files)")
    print(f"  {'✓' if struct1['has_templates'] else '✗'} templates/ ({struct1['template_count']} files)")
    print(f"  {'✓' if struct1['has_assets'] else '✗'} assets/ ({struct1['asset_count']} files)")

    print(f"\n{name2}:")
    print(f"  ✓ SKILL.md")
    print(f"  {'✓' if struct2['has_scripts'] else '✗'} scripts/ ({struct2['script_count']} files)")
    print(f"  {'✓' if struct2['has_references'] else '✗'} references/ ({struct2['reference_count']} files)")
    print(f"  {'✓' if struct2['has_templates'] else '✗'} templates/ ({struct2['template_count']} files)")
    print(f"  {'✓' if struct2['has_assets'] else '✗'} assets/ ({struct2['asset_count']} files)")

def compare_resources(struct1: Dict, struct2: Dict, name1: str, name2: str):
    """Compare resource counts."""
    print(f"\n{'='*70}")
    print("RESOURCE COMPARISON")
    print(f"{'='*70}\n")

    print(f"{'Resource Type':<20} {name1:<15} {name2:<15} {'Difference':<15}")
    print("-" * 70)

    def format_diff(count1: int, count2: int) -> str:
        diff = count2 - count1
        if diff > 0:
            return f"+{diff}"
        elif diff < 0:
            return str(diff)
        else:
            return "same"

    print(f"{'Scripts':<20} {struct1['script_count']:<15} {struct2['script_count']:<15} {format_diff(struct1['script_count'], struct2['script_count']):<15}")
    print(f"{'References':<20} {struct1['reference_count']:<15} {struct2['reference_count']:<15} {format_diff(struct1['reference_count'], struct2['reference_count']):<15}")
    print(f"{'Templates':<20} {struct1['template_count']:<15} {struct2['template_count']:<15} {format_diff(struct1['template_count'], struct2['template_count']):<15}")
    print(f"{'Assets':<20} {struct1['asset_count']:<15} {struct2['asset_count']:<15} {format_diff(struct1['asset_count'], struct2['asset_count']):<15}")

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

def calculate_metrics(body: str) -> Dict:
    """Calculate content metrics."""
    return {
        'word_count': len(body.split()),
        'heading_count': len(re.findall(r'^#{1,3}\s+', body, re.MULTILINE)),
        'code_blocks': len(re.findall(r'```', body)) // 2,
        'list_items': len(re.findall(r'^\s*[-*]\s+', body, re.MULTILINE)),
    }

def compare_metrics(metrics1: Dict, metrics2: Dict, name1: str, name2: str):
    """Compare content metrics."""
    print(f"\n{'='*70}")
    print("METRICS COMPARISON")
    print(f"{'='*70}\n")

    print(f"{'Metric':<20} {name1:<15} {name2:<15} {'Difference':<15}")
    print("-" * 70)

    for key in ['word_count', 'heading_count', 'code_blocks', 'list_items']:
        val1 = metrics1[key]
        val2 = metrics2[key]
        diff = val2 - val1

        if diff > 0:
            diff_str = f"+{diff}"
        elif diff < 0:
            diff_str = str(diff)
        else:
            diff_str = "same"

        print(f"{key:<20} {val1:<15} {val2:<15} {diff_str:<15}")

def compare_auto_invocation(fm1: Dict, fm2: Dict, name1: str, name2: str):
    """Compare auto-invocation triggers in descriptions."""
    print(f"\n{'='*70}")
    print("AUTO-INVOCATION TRIGGERS")
    print(f"{'='*70}\n")

    desc1 = fm1.get('description', '')
    desc2 = fm2.get('description', '')

    # Extract trigger phrases
    trigger_patterns = [
        r'auto-invokes? when ([^.]+)',
        r'use when ([^.]+)',
        r'when (?:the user|user) ([^.]+)',
    ]

    triggers1 = []
    triggers2 = []

    for pattern in trigger_patterns:
        triggers1.extend(re.findall(pattern, desc1, re.IGNORECASE))
        triggers2.extend(re.findall(pattern, desc2, re.IGNORECASE))

    print(f"{name1} triggers:")
    if triggers1:
        for trigger in triggers1:
            print(f"  • {trigger.strip()}")
    else:
        print("  (no explicit triggers found)")

    print(f"\n{name2} triggers:")
    if triggers2:
        for trigger in triggers2:
            print(f"  • {trigger.strip()}")
    else:
        print("  (no explicit triggers found)")

def compare_content(body1: str, body2: str, name1: str, name2: str):
    """Compare content with unified diff."""
    print(f"\n{'='*70}")
    print("CONTENT DIFF")
    print(f"{'='*70}\n")

    lines1 = body1.splitlines()
    lines2 = body2.splitlines()

    diff = list(difflib.unified_diff(
        lines1,
        lines2,
        fromfile=name1,
        tofile=name2,
        lineterm='',
        n=2  # Context lines
    ))

    if not diff:
        print("✅ Content is identical\n")
        return

    print(f"Showing first 50 lines of diff:\n")

    # Print diff with color indicators
    for i, line in enumerate(diff[:50]):
        if line.startswith('---') or line.startswith('+++'):
            print(f"\033[36m{line}\033[0m")  # Cyan for file markers
        elif line.startswith('-'):
            print(f"\033[31m{line}\033[0m")  # Red for deletions
        elif line.startswith('+'):
            print(f"\033[32m{line}\033[0m")  # Green for additions
        elif line.startswith('@@'):
            print(f"\033[34m{line}\033[0m")  # Blue for position markers
        else:
            print(line)

    if len(diff) > 50:
        print(f"\n... ({len(diff) - 50} more lines)")

    print()

def print_summary(fm1: Dict, fm2: Dict, struct1: Dict, struct2: Dict, body1: str, body2: str):
    """Print comparison summary."""
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}\n")

    # Frontmatter status
    frontmatter_same = fm1 == fm2
    print(f"Frontmatter:         {'✅ Identical' if frontmatter_same else '⚠️  Different'}")

    # Structure status
    structure_same = (
        struct1['has_scripts'] == struct2['has_scripts'] and
        struct1['has_references'] == struct2['has_references'] and
        struct1['has_templates'] == struct2['has_templates'] and
        struct1['has_assets'] == struct2['has_assets']
    )
    print(f"Directory Structure: {'✅ Same' if structure_same else '⚠️  Different'}")

    # Content similarity
    lines1 = body1.splitlines()
    lines2 = body2.splitlines()

    if lines1 and lines2:
        matcher = difflib.SequenceMatcher(None, body1, body2)
        similarity = matcher.ratio() * 100
        print(f"Content Similarity:  {similarity:.1f}%")
    else:
        print(f"Content Similarity:  N/A")

    # Recommendations
    print("\nRecommendations:")
    if not frontmatter_same:
        print("  • Review frontmatter differences to ensure consistency")
    if not structure_same:
        print("  • Consider standardizing directory structure")
    if 'model' in fm1 or 'model' in fm2:
        print("  • CRITICAL: Remove 'model' field from skills")

    print()

def main():
    """
    Usage:
        python3 compare-skills.py <skill1> <skill2>
    """
    if len(sys.argv) < 3:
        print("Usage: python3 compare-skills.py <skill1-name> <skill2-name>")
        print("\nExample:")
        print("  python3 compare-skills.py building-agents building-skills")
        sys.exit(1)

    skill1_name = sys.argv[1]
    skill2_name = sys.argv[2]

    print("="*70)
    print(f"Skill Comparison Tool")
    print("="*70)
    print(f"\nComparing: {skill1_name} vs {skill2_name}\n")

    # Find skills
    skill1_dir = find_skill(skill1_name)
    skill2_dir = find_skill(skill2_name)

    if not skill1_dir:
        print(f"\n❌ Skill not found: {skill1_name}")
        sys.exit(1)

    if not skill2_dir:
        print(f"\n❌ Skill not found: {skill2_name}")
        sys.exit(1)

    # Parse skills
    try:
        fm1, body1 = parse_skill(skill1_dir)
        fm2, body2 = parse_skill(skill2_dir)
    except Exception as e:
        print(f"\n❌ Error parsing skills: {e}")
        sys.exit(1)

    # Analyze structures
    struct1 = analyze_directory_structure(skill1_dir)
    struct2 = analyze_directory_structure(skill2_dir)

    # Calculate metrics
    metrics1 = calculate_metrics(body1)
    metrics2 = calculate_metrics(body2)

    # Run comparisons
    compare_frontmatter(fm1, fm2, skill1_name, skill2_name)
    compare_directory_structure(struct1, struct2, skill1_name, skill2_name)
    compare_resources(struct1, struct2, skill1_name, skill2_name)
    compare_structure(body1, body2, skill1_name, skill2_name)
    compare_metrics(metrics1, metrics2, skill1_name, skill2_name)
    compare_auto_invocation(fm1, fm2, skill1_name, skill2_name)
    compare_content(body1, body2, skill1_name, skill2_name)
    print_summary(fm1, fm2, struct1, struct2, body1, body2)

if __name__ == '__main__':
    main()
