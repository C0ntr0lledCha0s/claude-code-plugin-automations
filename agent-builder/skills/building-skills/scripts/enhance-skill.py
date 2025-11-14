#!/usr/bin/env python3
"""
Enhance Skill Script - Deep analysis and improvement suggestions
Part of the agent-builder plugin for Claude Code

Analyzes skill quality across multiple dimensions with directory-aware checks
"""

import sys
import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional

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

        skill_dir = search_path / skill_name
        if skill_dir.exists() and skill_dir.is_dir():
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                return skill_dir

        for skill_dir in search_path.rglob(skill_name):
            if skill_dir.is_dir() and skill_dir.parent.name == "skills":
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    return skill_dir

    return None

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

def analyze_schema(frontmatter: Dict, skill_name: str, skill_path: Path) -> Tuple[int, List[str]]:
    """Analyze schema compliance. Returns (score, issues)."""
    score = 0
    issues = []

    # Validate skill name
    if not re.match(r'^[a-z0-9-]+$', skill_name):
        issues.append("⚠️  Skill name doesn't follow lowercase-hyphen convention")
    if len(skill_name) > 64:
        issues.append("⚠️  Skill name exceeds 64 character limit")
    else:
        score += 2

    # Check gerund form (recommended for skills)
    if not skill_name.endswith('ing') and not any(word in skill_name for word in ['-ing-', 'analyzing', 'building', 'creating']):
        issues.append("💡 Consider gerund form for skill names (e.g., 'building-x', 'analyzing-y')")
    else:
        score += 1

    # Required field: name
    if 'name' in frontmatter:
        score += 2
        if frontmatter['name'] != skill_path.name:
            issues.append(f"⚠️  Name '{frontmatter['name']}' doesn't match directory '{skill_path.name}'")
    else:
        issues.append("❌ Missing required 'name' field")

    # Required field: description
    if 'description' in frontmatter:
        score += 3
        desc = frontmatter['description']
        if len(desc) < 30:
            issues.append("⚠️  Description too short for skills (< 30 chars)")
        elif len(desc) > 1024:
            issues.append("⚠️  Description exceeds 1024 character limit")
        else:
            score += 1

        # Check for auto-invocation triggers
        trigger_keywords = ['use when', 'when', 'auto-invokes when', 'whenever']
        if not any(keyword in desc.lower() for keyword in trigger_keywords):
            issues.append("⚠️  Description should clearly state WHEN Claude should auto-invoke")
    else:
        issues.append("❌ Missing required 'description' field")

    # Optional but recommended: version
    if 'version' in frontmatter:
        score += 1
        if not re.match(r'^\d+\.\d+\.\d+', str(frontmatter['version'])):
            issues.append("💡 Use semantic versioning (e.g., 1.0.0)")

    # Optional: allowed-tools
    if 'allowed-tools' in frontmatter:
        score += 1

    return min(score, 10), issues

def analyze_model_field(frontmatter: Dict) -> Tuple[int, List[str]]:
    """Analyze model field (CRITICAL: skills cannot have model field). Returns (score, findings)."""
    score = 10
    findings = []

    # CRITICAL: Skills do not support model field
    if 'model' in frontmatter:
        score = 0
        findings.append(
            "❌ CRITICAL: Skills cannot have 'model' field. "
            "Only agents support model specification. "
            "Remove this field immediately."
        )
        return score, findings

    findings.append("✅ No model field (correct - skills don't support it)")
    return score, findings

def analyze_auto_invocation(frontmatter: Dict, body: str) -> Tuple[int, List[str]]:
    """Analyze auto-invocation clarity. Returns (score, findings)."""
    score = 0
    findings = []

    description = frontmatter.get('description', '')

    # Check description for auto-invocation triggers
    trigger_phrases = [
        'auto-invokes when',
        'use when',
        'when the user',
        'when user',
        'whenever'
    ]

    has_triggers = any(phrase in description.lower() for phrase in trigger_phrases)
    if has_triggers:
        score += 3
        findings.append("✅ Description clearly states when to auto-invoke")
    else:
        findings.append("❌ Description doesn't clearly state WHEN to auto-invoke")

    # Check body for "When to Use" section
    if '## when to use' in body.lower():
        score += 3
        findings.append("✅ Has 'When to Use' section")
    else:
        findings.append("⚠️  Missing 'When to Use' section")

    # Check for auto-invocation examples
    if 'auto-invoke' in body.lower() or 'automatically' in body.lower():
        score += 2
        findings.append("✅ Documents auto-invocation behavior")
    else:
        findings.append("💡 Consider documenting auto-invocation behavior")

    # Check if description is specific enough
    vague_words = ['helps', 'assists', 'provides']
    if any(word in description.lower() for word in vague_words) and not has_triggers:
        findings.append("⚠️  Description is vague - be specific about WHEN to invoke")

    return min(score, 10), findings

def analyze_directory_structure(skill_path: Path, body: str) -> Tuple[int, List[str]]:
    """Analyze directory structure and resource usage. Returns (score, findings)."""
    score = 0
    findings = []

    # Check for subdirectories
    subdirs = [d for d in skill_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
    subdir_names = [d.name for d in subdirs]

    valid_subdirs = ['scripts', 'references', 'assets', 'templates']

    # Check for standard subdirectories
    if 'scripts' in subdir_names:
        score += 2
        findings.append("✅ Has scripts/ directory")

        # Check {baseDir} usage
        if '{baseDir}' in body:
            score += 1
            findings.append("✅ Uses {baseDir} to reference scripts")
        else:
            findings.append("⚠️  Has scripts/ but doesn't use {baseDir} variable")

    if 'references' in subdir_names:
        score += 2
        findings.append("✅ Has references/ directory")

    if 'templates' in subdir_names or 'assets' in subdir_names:
        score += 1
        findings.append("✅ Has templates/ or assets/ directory")

    # Check for invalid subdirectories
    invalid_subdirs = [d for d in subdir_names if d not in valid_subdirs]
    if invalid_subdirs:
        findings.append(f"⚠️  Unexpected subdirectories: {', '.join(invalid_subdirs)}")

    # Check script executability
    scripts_dir = skill_path / 'scripts'
    if scripts_dir.exists():
        scripts = list(scripts_dir.glob('*.py')) + list(scripts_dir.glob('*.sh'))
        non_executable = [s for s in scripts if not s.stat().st_mode & 0o111]
        if non_executable:
            findings.append(f"⚠️  {len(non_executable)} script(s) not executable")

    # Minimal structure (just SKILL.md) is okay
    if not subdirs:
        score += 3
        findings.append("✅ Minimal structure (SKILL.md only) - valid approach")

    return min(score, 10), findings

def analyze_security(frontmatter: Dict, body: str) -> Tuple[int, List[str]]:
    """Analyze security. Returns (score, findings)."""
    score = 10
    findings = []

    tools = frontmatter.get('allowed-tools', '')

    # Check for Bash access
    if 'Bash' in tools:
        score -= 2
        if 'validation' not in body.lower() and 'sanitize' not in body.lower():
            score -= 2
            findings.append("❌ Has Bash access without input validation documentation")
        else:
            findings.append("⚠️  Has Bash access - ensure validation is thorough")

    # Check for Write/Edit access
    if 'Write' in tools or 'Edit' in tools:
        if not any(word in body.lower() for word in ['validate', 'check', 'verify']):
            score -= 1
            findings.append("⚠️  Has write access - consider adding validation checks")

    # Tool minimalism
    if tools:
        tool_count = len([t.strip() for t in tools.split(',')])
        if tool_count > 6:
            score -= 1
            findings.append("⚠️  Many tools pre-approved - consider minimizing")

    if not [f for f in findings if f.startswith('⚠️') or f.startswith('❌')]:
        findings.append("✅ No security issues detected")

    return max(score, 0), findings

def analyze_content_quality(body: str) -> Tuple[int, List[str]]:
    """Analyze content quality. Returns (score, findings)."""
    score = 0
    findings = []

    # Check for key sections
    sections = {
        'when to use': r'##\s*when to use',
        'capabilities': r'##\s*capabilit(?:y|ies)',
        'examples': r'##\s*example',
        'workflow': r'##\s*(?:workflow|how it works)',
    }

    for section_name, pattern in sections.items():
        if re.search(pattern, body, re.IGNORECASE):
            score += 2
            findings.append(f"✅ Has '{section_name}' section")
        else:
            findings.append(f"⚠️  Missing '{section_name}' section")

    # Check word count
    word_count = len(body.split())
    if word_count < 200:
        findings.append("⚠️  Very brief content (< 200 words) - add more detail")
    elif word_count > 3000:
        findings.append("⚠️  Very lengthy content (> 3000 words) - consider condensing")
    else:
        score += 2

    return min(score, 10), findings

def analyze_maintainability(body: str, skill_path: Path) -> Tuple[int, List[str]]:
    """Analyze maintainability. Returns (score, findings)."""
    score = 0
    findings = []

    # Check for clear headings
    heading_count = len(re.findall(r'^#{1,3}\s+\w+', body, re.MULTILINE))
    if heading_count >= 5:
        score += 3
    elif heading_count >= 3:
        score += 2
        findings.append("💡 Could use more section headings")
    else:
        score += 1
        findings.append("⚠️  Add more headings to organize content")

    # Check for lists
    if re.search(r'^\s*[-*]\s+', body, re.MULTILINE):
        score += 2
    else:
        findings.append("💡 Use lists for better readability")

    # Check for code blocks
    if '```' in body:
        score += 2
    else:
        findings.append("💡 Add code examples in code blocks")

    # Check for formatting
    if re.search(r'\*\*.*?\*\*', body):
        score += 1
    if re.search(r'`.*?`', body):
        score += 1

    # Check for documentation files
    refs_dir = skill_path / 'references'
    if refs_dir.exists() and any(refs_dir.iterdir()):
        score += 1
        findings.append("✅ Has reference documentation")

    if not [f for f in findings if f.startswith('⚠️')]:
        findings.append("✅ Well-formatted and maintainable")

    return min(score, 10), findings

def generate_recommendations(frontmatter: Dict, body: str, all_scores: Dict, skill_path: Path) -> List[str]:
    """Generate prioritized recommendations."""
    recommendations = []

    # Critical issues
    if all_scores['model_field'] < 5:
        recommendations.append("🔴 CRITICAL: Remove 'model' field (skills don't support it)")

    if all_scores['schema'] < 5:
        recommendations.append("🔴 CRITICAL: Fix schema issues (name, description)")

    if all_scores['auto_invocation'] < 5:
        recommendations.append("🔴 CRITICAL: Clarify when Claude should auto-invoke this skill")

    # High priority
    if all_scores['security'] < 5:
        recommendations.append("🟡 HIGH: Address security vulnerabilities")

    if 'Bash' in frontmatter.get('allowed-tools', ''):
        recommendations.append("🟡 HIGH: Document input validation for Bash commands")

    # Medium priority
    if all_scores['content'] < 7:
        recommendations.append("🟢 MEDIUM: Add missing sections (when to use, examples, capabilities)")

    if all_scores['directory'] < 7:
        recommendations.append("🟢 MEDIUM: Consider using {baseDir} for resource references")

    if all_scores['maintainability'] < 7:
        recommendations.append("🟢 MEDIUM: Improve structure with headings and examples")

    if not recommendations:
        recommendations.append("✅ Excellent skill! No major improvements needed.")

    return recommendations

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 enhance-skill.py <skill-name>")
        print("\nExample: python3 enhance-skill.py building-commands")
        sys.exit(1)

    skill_name = sys.argv[1]

    # Find skill
    print(f"Analyzing skill: {skill_name}...\n")
    skill_path = find_skill(skill_name)

    if not skill_path:
        print(f"❌ Skill not found: {skill_name}")
        sys.exit(1)

    # Parse skill
    try:
        frontmatter, body = parse_skill(skill_path)
    except Exception as e:
        print(f"❌ Failed to parse skill: {e}")
        sys.exit(1)

    # Run analyses
    print("="*60)
    print(f"Enhancement Analysis: {skill_name}")
    print("="*60)
    print(f"Location: {skill_path}\n")

    schema_score, schema_issues = analyze_schema(frontmatter, skill_name, skill_path)
    model_score, model_findings = analyze_model_field(frontmatter)
    auto_inv_score, auto_inv_findings = analyze_auto_invocation(frontmatter, body)
    dir_score, dir_findings = analyze_directory_structure(skill_path, body)
    security_score, security_findings = analyze_security(frontmatter, body)
    content_score, content_findings = analyze_content_quality(body)
    maint_score, maint_findings = analyze_maintainability(body, skill_path)

    overall_score = (schema_score + model_score + auto_inv_score + dir_score +
                     security_score + content_score + maint_score) / 7

    print(f"Overall Score: {overall_score:.1f}/10\n")

    # Display scores
    print("Detailed Scores:")
    print(f"  Schema Compliance:   {schema_score}/10")
    print(f"  Model Field Check:   {model_score}/10")
    print(f"  Auto-Invocation:     {auto_inv_score}/10")
    print(f"  Directory Structure: {dir_score}/10")
    print(f"  Security:            {security_score}/10")
    print(f"  Content Quality:     {content_score}/10")
    print(f"  Maintainability:     {maint_score}/10")
    print()

    # Display findings
    if schema_issues:
        print("Schema & Structure:")
        for issue in schema_issues:
            print(f"  {issue}")
        print()

    print("Model Field Check:")
    for finding in model_findings:
        print(f"  {finding}")
    print()

    print("Auto-Invocation Clarity:")
    for finding in auto_inv_findings:
        print(f"  {finding}")
    print()

    print("Directory Structure:")
    for finding in dir_findings:
        print(f"  {finding}")
    print()

    print("Security Analysis:")
    for finding in security_findings:
        print(f"  {finding}")
    print()

    print("Content Quality:")
    for finding in content_findings:
        print(f"  {finding}")
    print()

    print("Maintainability:")
    for finding in maint_findings:
        print(f"  {finding}")
    print()

    # Generate recommendations
    all_scores = {
        'schema': schema_score,
        'model_field': model_score,
        'auto_invocation': auto_inv_score,
        'directory': dir_score,
        'security': security_score,
        'content': content_score,
        'maintainability': maint_score,
    }

    recommendations = generate_recommendations(frontmatter, body, all_scores, skill_path)

    print("="*60)
    print("Recommendations (Prioritized)")
    print("="*60)
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")
    print()

    # Next steps
    print("="*60)
    print("Next Steps")
    print("="*60)
    print("1. Review recommendations above")
    print(f"2. Run: python3 update-skill.py {skill_name}")
    print("3. Apply improvements interactively")
    print(f"4. Re-run: python3 enhance-skill.py {skill_name}")
    print("5. Verify score improved")
    print()

    # Exit with status
    if overall_score >= 8:
        print("✅ Excellent skill! Only minor improvements possible.")
        sys.exit(0)
    elif overall_score >= 6:
        print("✅ Good skill. Some improvements recommended.")
        sys.exit(0)
    else:
        print("⚠️  Skill needs improvement. Please address findings above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
