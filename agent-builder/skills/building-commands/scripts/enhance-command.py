#!/usr/bin/env python3
"""
Enhance Command Script - Deep analysis and improvement suggestions
Part of the agent-builder plugin for Claude Code
"""

import sys
import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional

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

        command_file = search_path / f"{command_name}.md"
        if command_file.exists():
            return command_file

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

def analyze_schema(frontmatter: Dict, command_name: str) -> Tuple[int, List[str]]:
    """Analyze schema compliance. Returns (score, issues)."""
    score = 0
    issues = []

    # Validate command name
    if not re.match(r'^[a-z0-9-]+$', command_name):
        issues.append("⚠️  Command filename doesn't follow lowercase-hyphen convention")
    if len(command_name) > 64:
        issues.append("⚠️  Command name exceeds 64 character limit")
    else:
        score += 2

    # Check if name is action-oriented
    common_verbs = [
        'add', 'build', 'check', 'clean', 'commit', 'create', 'delete', 'deploy',
        'generate', 'get', 'install', 'list', 'make', 'new', 'push', 'remove',
        'review', 'run', 'search', 'show', 'test', 'update', 'validate'
    ]
    if any(command_name.startswith(verb) for verb in common_verbs):
        score += 2
    else:
        issues.append("⚠️  Command name should start with a verb (e.g., 'create-', 'run-', 'check-')")

    # Required field: description
    if 'description' in frontmatter:
        score += 3
        desc = frontmatter['description']
        if len(desc) < 10:
            issues.append("⚠️  Description too short, should explain what command does")
        elif len(desc) > 200:
            issues.append("⚠️  Description too long, should be a clear one-liner")
        else:
            score += 1
    else:
        issues.append("❌ Missing required 'description' field")

    # Optional but recommended: allowed-tools
    if 'allowed-tools' in frontmatter:
        score += 2
    else:
        issues.append("💡 Consider adding 'allowed-tools' for pre-approved permissions")

    return min(score, 10), issues

def analyze_model_field(frontmatter: Dict) -> Tuple[int, List[str]]:
    """Analyze model field configuration. Returns (score, findings)."""
    score = 10
    findings = []

    if 'model' not in frontmatter:
        findings.append("✅ Using inherited model (recommended)")
        return score, findings

    model = frontmatter['model']

    # CRITICAL: Check for short aliases (don't work in commands)
    if model in ['haiku', 'sonnet', 'opus', 'inherit']:
        score = 0
        findings.append(
            f"❌ CRITICAL: Commands cannot use short alias '{model}'. "
            f"Use version alias like 'claude-haiku-4-5' or full ID like 'claude-haiku-4-5-20251001'"
        )
        return score, findings

    # Check format
    if not model.startswith('claude-'):
        score -= 3
        findings.append(
            f"⚠️  Model '{model}' doesn't start with 'claude-', may cause API errors"
        )
    else:
        findings.append(f"✅ Valid model format: {model}")

    # Check if using version alias (recommended) vs full ID
    if re.match(r'^claude-(haiku|sonnet|opus)-\d+-\d+$', model):
        findings.append("✅ Using version alias (auto-updates with minor versions)")
    elif re.match(r'^claude-(haiku|sonnet|opus)-\d+-\d+-\d+$', model):
        findings.append("💡 Using full model ID (locked to specific version)")

    return score, findings

def analyze_arguments(frontmatter: Dict, body: str) -> Tuple[int, List[str]]:
    """Analyze argument handling. Returns (score, findings)."""
    score = 10
    findings = []

    # Check if command uses arguments
    uses_positional = bool(re.search(r'\$\d+', body))
    uses_all_args = '$ARGUMENTS' in body

    if uses_positional or uses_all_args:
        # Has arguments
        if 'argument-hint' not in frontmatter:
            score -= 3
            findings.append("❌ Uses arguments but missing 'argument-hint' field")
        else:
            hint = frontmatter['argument-hint']
            # Handle YAML parsing list or string
            if isinstance(hint, list):
                hint = ' '.join(str(item) for item in hint)
            elif not isinstance(hint, str):
                hint = str(hint)

            if not hint.startswith('['):
                score -= 1
                findings.append(f"⚠️  argument-hint should use brackets: '{hint}' → '[{hint}]'")
            else:
                findings.append(f"✅ Has clear argument-hint: {hint}")

        # Check for argument documentation
        if '## Arguments' not in body and '## Parameters' not in body:
            score -= 2
            findings.append("⚠️  Missing '## Arguments' section to document parameters")
        else:
            findings.append("✅ Documents arguments in body")

        # List what arguments are used
        if uses_positional:
            args_found = sorted(set(re.findall(r'\$(\d+)', body)))
            findings.append(f"💡 Uses positional arguments: ${', $'.join(args_found)}")
        if uses_all_args:
            findings.append("💡 Uses $ARGUMENTS variable")

    else:
        # No arguments
        if 'argument-hint' in frontmatter:
            score -= 1
            findings.append("⚠️  Has 'argument-hint' but doesn't use arguments in body")
        else:
            findings.append("✅ No arguments (simple command)")

    return max(score, 0), findings

def analyze_security(frontmatter: Dict, body: str) -> Tuple[int, List[str]]:
    """Analyze security. Returns (score, findings)."""
    score = 10
    findings = []

    tools = frontmatter.get('allowed-tools', '')

    # Check for Bash access
    if 'Bash' in tools:
        score -= 2
        findings.append("⚠️  Has Bash access - requires careful input validation")

        # Check for validation documentation
        if 'validation' not in body.lower() and 'sanitize' not in body.lower():
            score -= 3
            findings.append("❌ Has Bash access without input validation documentation")

        # Check for dangerous patterns
        dangerous_patterns = [
            (r'\$\w+\s*(?:&&|\||;|`)', "⚠️  Potential command injection with unsanitized arguments"),
            (r'rm\s+-rf\s+\$', "❌ Dangerous rm -rf with variable - add validation"),
            (r'eval\s+\$', "❌ Using eval with arguments is extremely dangerous"),
            (r'\$ARGUMENTS.*(?:&&|\||;)', "⚠️  $ARGUMENTS used in command chain - validate first"),
        ]

        for pattern, warning in dangerous_patterns:
            if re.search(pattern, body):
                score -= 2
                findings.append(warning)

    # Check for hardcoded secrets
    secret_patterns = [
        r'api[_-]?key',
        r'password',
        r'secret',
        r'token',
        r'credential',
    ]

    for pattern in secret_patterns:
        if re.search(pattern, body, re.IGNORECASE):
            # Check if it's in a documentation context
            if not re.search(f'{pattern}.*example|{pattern}.*placeholder', body, re.IGNORECASE):
                score -= 3
                findings.append(f"❌ Possible hardcoded secret: '{pattern}' found in body")
                break

    # Tool minimalism
    if tools:
        tool_count = len([t.strip() for t in tools.split(',')])
        if tool_count > 6:
            score -= 1
            findings.append("⚠️  Many tools pre-approved - consider minimizing permissions")

    if not [f for f in findings if f.startswith('⚠️') or f.startswith('❌')]:
        findings.append("✅ No security issues detected")

    return max(score, 0), findings

def analyze_content_quality(body: str) -> Tuple[int, List[str]]:
    """Analyze content quality. Returns (score, findings)."""
    score = 0
    findings = []

    # Check for key sections
    sections = {
        'workflow': r'##\s*(?:workflow|steps?|process)',
        'usage/examples': r'##\s*(?:example|usage)',
        'arguments': r'##\s*(?:arguments|parameters)',
    }

    for section_name, pattern in sections.items():
        if re.search(pattern, body, re.IGNORECASE):
            score += 2
            findings.append(f"✅ Has '{section_name}' section")
        else:
            findings.append(f"⚠️  Missing '{section_name}' section")

    # Check for examples count
    example_count = len(re.findall(r'##\s*example', body, re.IGNORECASE))
    if example_count >= 2:
        score += 2
        findings.append(f"✅ Has {example_count} examples")
    elif example_count == 1:
        score += 1
        findings.append("💡 Has 1 example, consider adding more use cases")
    else:
        findings.append("❌ No examples - add 1-2 concrete usage examples")

    # Check word count
    word_count = len(body.split())
    if word_count < 50:
        findings.append("⚠️  Very brief content - add workflow and examples")
    elif word_count > 1000:
        findings.append("⚠️  Very lengthy - commands should be focused workflows")
    else:
        score += 2

    return min(score, 10), findings

def analyze_maintainability(body: str) -> Tuple[int, List[str]]:
    """Analyze maintainability. Returns (score, findings)."""
    score = 0
    findings = []

    # Check for clear headings
    heading_count = len(re.findall(r'^#{1,3}\s+\w+', body, re.MULTILINE))
    if heading_count >= 3:
        score += 3
    elif heading_count >= 2:
        score += 2
        findings.append("💡 Could use more section headings")
    else:
        score += 1
        findings.append("⚠️  Add section headings (## Workflow, ## Examples, etc.)")

    # Check for lists and structure
    if re.search(r'^\s*[-*]\s+', body, re.MULTILINE):
        score += 2
    else:
        findings.append("⚠️  Use lists for step-by-step instructions")

    # Check for code blocks
    code_block_count = body.count('```')
    if code_block_count >= 2:
        score += 2
    else:
        findings.append("⚠️  Add code blocks for examples")

    # Check for clear formatting
    if re.search(r'\*\*.*?\*\*', body):  # Bold text
        score += 1
    if re.search(r'`.*?`', body):  # Inline code
        score += 1

    # Check line length (readability)
    long_lines = [line for line in body.split('\n') if len(line) > 120]
    if len(long_lines) > body.count('\n') * 0.2:  # More than 20% long lines
        findings.append("⚠️  Many long lines - break up for readability")

    if not [f for f in findings if f.startswith('⚠️')]:
        findings.append("✅ Well-formatted and maintainable")

    return min(score, 10), findings

def generate_recommendations(frontmatter: Dict, body: str, all_scores: Dict) -> List[str]:
    """Generate prioritized recommendations."""
    recommendations = []

    # Critical issues
    if all_scores['model'] < 5:
        recommendations.append("🔴 CRITICAL: Fix model field (use version alias, not short alias)")

    if all_scores['schema'] < 5:
        recommendations.append("🔴 CRITICAL: Fix schema issues (description, naming)")

    if all_scores['security'] < 5:
        recommendations.append("🔴 CRITICAL: Address security vulnerabilities")

    # High priority
    if all_scores['arguments'] < 7:
        recommendations.append("🟡 HIGH: Improve argument handling (add argument-hint, document parameters)")

    if 'Bash' in frontmatter.get('allowed-tools', ''):
        recommendations.append("🟡 HIGH: Document input validation for Bash commands")

    # Medium priority
    if all_scores['quality'] < 7:
        recommendations.append("🟢 MEDIUM: Add examples and usage documentation")

    if all_scores['maintainability'] < 7:
        recommendations.append("🟢 MEDIUM: Improve structure with headings and code blocks")

    # Model optimization
    model = frontmatter.get('model', 'inherit')
    if model != 'inherit' and 'claude-opus' in model:
        if 'simple' in frontmatter.get('description', '').lower() or 'quick' in frontmatter.get('description', '').lower():
            recommendations.append("🟢 LOW: Consider claude-haiku-4-5 for simple commands (faster, cheaper)")

    if not recommendations:
        recommendations.append("✅ Excellent command! No improvements needed.")

    return recommendations

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 enhance-command.py <command-name>")
        print("\nExample: python3 enhance-command.py new-agent")
        sys.exit(1)

    command_name = sys.argv[1].replace('.md', '')

    # Find command
    print(f"Analyzing command: {command_name}...\n")
    command_path = find_command(command_name)

    if not command_path:
        print(f"❌ Command not found: {command_name}")
        sys.exit(1)

    # Parse command
    try:
        frontmatter, body = parse_command(command_path)
    except Exception as e:
        print(f"❌ Failed to parse command: {e}")
        sys.exit(1)

    # Run analyses
    print("="*60)
    print(f"Enhancement Analysis: {command_name}")
    print("="*60)
    print(f"Location: {command_path}\n")

    schema_score, schema_issues = analyze_schema(frontmatter, command_name)
    model_score, model_findings = analyze_model_field(frontmatter)
    arguments_score, arguments_findings = analyze_arguments(frontmatter, body)
    security_score, security_findings = analyze_security(frontmatter, body)
    quality_score, quality_findings = analyze_content_quality(body)
    maintainability_score, maintainability_findings = analyze_maintainability(body)

    overall_score = (schema_score + model_score + arguments_score + security_score + quality_score + maintainability_score) / 6

    print(f"Overall Score: {overall_score:.1f}/10\n")

    # Display scores
    print("Detailed Scores:")
    print(f"  Schema Compliance:  {schema_score}/10")
    print(f"  Model Configuration: {model_score}/10")
    print(f"  Argument Handling:  {arguments_score}/10")
    print(f"  Security:           {security_score}/10")
    print(f"  Content Quality:    {quality_score}/10")
    print(f"  Maintainability:    {maintainability_score}/10")
    print()

    # Display findings
    if schema_issues:
        print("Schema & Structure:")
        for issue in schema_issues:
            print(f"  {issue}")
        print()

    print("Model Configuration:")
    for finding in model_findings:
        print(f"  {finding}")
    print()

    print("Argument Handling:")
    for finding in arguments_findings:
        print(f"  {finding}")
    print()

    print("Security Analysis:")
    for finding in security_findings:
        print(f"  {finding}")
    print()

    print("Content Quality:")
    for finding in quality_findings:
        print(f"  {finding}")
    print()

    print("Maintainability:")
    for finding in maintainability_findings:
        print(f"  {finding}")
    print()

    # Generate recommendations
    all_scores = {
        'schema': schema_score,
        'model': model_score,
        'arguments': arguments_score,
        'security': security_score,
        'quality': quality_score,
        'maintainability': maintainability_score,
    }

    recommendations = generate_recommendations(frontmatter, body, all_scores)

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
    print(f"2. Run: python3 update-command.py {command_name}")
    print("3. Apply improvements interactively")
    print(f"4. Re-run: python3 enhance-command.py {command_name}")
    print("5. Verify score improved")
    print()

    # Exit with status
    if overall_score >= 8:
        print("✅ Excellent command! Only minor improvements possible.")
        sys.exit(0)
    elif overall_score >= 6:
        print("✅ Good command. Some improvements recommended.")
        sys.exit(0)
    else:
        print("⚠️  Command needs improvement. Please address findings above.")
        sys.exit(1)

if __name__ == '__main__':
    main()
