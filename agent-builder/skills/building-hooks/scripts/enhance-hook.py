#!/usr/bin/env python3
"""
Hook enhancement analyzer for Claude Code hooks.json files.

Analyzes hook quality with security-focused scoring and recommendations.
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple

# ANSI color codes
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Valid events
VALID_EVENTS = [
    'PreToolUse', 'PostToolUse', 'UserPromptSubmit',
    'Stop', 'SessionStart', 'Notification', 'SubagentStop', 'PreCompact'
]

TOOL_EVENTS = ['PreToolUse', 'PostToolUse']
LIFECYCLE_EVENTS = ['UserPromptSubmit', 'Stop', 'SessionStart', 'Notification', 'SubagentStop', 'PreCompact']


def analyze_schema_compliance(hooks_config: Dict) -> Tuple[int, List[str]]:
    """Analyze schema compliance (0-10)."""
    score = 10
    findings = []

    # Check top-level structure
    if 'hooks' not in hooks_config:
        score = 0
        findings.append("❌ CRITICAL: Missing top-level 'hooks' field")
        return score, findings

    if not isinstance(hooks_config['hooks'], dict):
        score = 0
        findings.append("❌ CRITICAL: 'hooks' must be an object")
        return score, findings

    hooks = hooks_config['hooks']

    # Check each event
    for event_name, event_hooks in hooks.items():
        # Validate event name
        if event_name not in VALID_EVENTS:
            score -= 2
            findings.append(f"❌ Invalid event name: '{event_name}'")

        # Check structure
        if not isinstance(event_hooks, list):
            score -= 2
            findings.append(f"❌ Event '{event_name}' must be a list")
            continue

        for i, hook_config in enumerate(event_hooks):
            # Check matcher requirements
            if event_name in TOOL_EVENTS:
                if 'matcher' not in hook_config:
                    score -= 1
                    findings.append(f"⚠️  Event '{event_name}' hook #{i+1}: Missing required 'matcher'")
            elif event_name in LIFECYCLE_EVENTS:
                if 'matcher' in hook_config and hook_config['matcher']:
                    score -= 1
                    findings.append(f"⚠️  Event '{event_name}' hook #{i+1}: Shouldn't have 'matcher'")

            # Check hooks array
            if 'hooks' not in hook_config:
                score -= 2
                findings.append(f"❌ Event '{event_name}' hook #{i+1}: Missing 'hooks' array")
                continue

            if not isinstance(hook_config['hooks'], list):
                score -= 2
                findings.append(f"❌ Event '{event_name}' hook #{i+1}: 'hooks' must be array")

    if score < 0:
        score = 0

    if not findings:
        findings.append("✅ Schema is fully compliant")

    return score, findings


def analyze_security(hooks_config: Dict) -> Tuple[int, List[str]]:
    """Analyze security (0-10) - CRITICAL."""
    score = 10
    findings = []

    if 'hooks' not in hooks_config:
        return 0, ["❌ CRITICAL: Cannot analyze security without hooks"]

    # Security patterns to check
    dangerous_patterns = [
        (r'eval\s+', 'CRITICAL: eval command (arbitrary code execution)', 3),
        (r'rm\s+-rf\s+/', 'CRITICAL: rm -rf / (system destruction)', 3),
        (r'\$\(.*\)', 'Command substitution (injection risk)', 2),
        (r'`.*`', 'Backtick execution (injection risk)', 2),
        (r'>\s*/dev/sd', 'Writing to disk devices (dangerous)', 3),
        (r'dd\s+if=', 'dd command (data destruction risk)', 2),
        (r'mkfs', 'Filesystem formatting (data loss)', 3),
        (r'chmod\s+777', 'Overly permissive permissions', 1),
        (r'wget.*\|.*bash', 'Piping wget to bash (dangerous)', 3),
        (r'curl.*\|.*bash', 'Piping curl to bash (dangerous)', 3),
    ]

    for event_name, event_hooks in hooks_config['hooks'].items():
        for i, hook_config in enumerate(event_hooks):
            if 'hooks' not in hook_config:
                continue

            for j, hook_item in enumerate(hook_config['hooks']):
                if hook_item.get('type') == 'command':
                    command = hook_item.get('command', '')

                    # Check dangerous patterns
                    for pattern, message, penalty in dangerous_patterns:
                        if re.search(pattern, command, re.IGNORECASE):
                            score -= penalty
                            findings.append(f"❌ {event_name} hook #{i+1}, item #{j+1}: {message}")

                    # Check for input validation
                    if '$1' in command or '$2' in command or '$@' in command:
                        if not any(check in command for check in ['[[ ', 'if ', 'case ']):
                            score -= 1
                            findings.append(f"⚠️  {event_name} hook #{i+1}, item #{j+1}: Uses parameters without apparent validation")

                    # Check for error handling
                    if 'set -euo pipefail' not in command and 'bash' in command.lower():
                        score -= 1
                        findings.append(f"⚠️  {event_name} hook #{i+1}, item #{j+1}: Missing set -euo pipefail")

                    # Check for absolute paths vs relative
                    if command.startswith('bash ') and '/' in command:
                        path = command.split()[1] if len(command.split()) > 1 else ''
                        if path and not path.startswith('/') and not path.startswith('${'):
                            score -= 1
                            findings.append(f"⚠️  {event_name} hook #{i+1}, item #{j+1}: Relative path (use absolute or ${CLAUDE_PLUGIN_ROOT})")

    if score < 0:
        score = 0

    if not findings:
        findings.append("✅ No security issues detected")

    return score, findings


def analyze_matcher_validity(hooks_config: Dict) -> Tuple[int, List[str]]:
    """Analyze matcher pattern validity (0-10)."""
    score = 10
    findings = []

    if 'hooks' not in hooks_config:
        return 0, ["❌ CRITICAL: No hooks to analyze"]

    for event_name, event_hooks in hooks_config['hooks'].items():
        for i, hook_config in enumerate(event_hooks):
            if event_name in TOOL_EVENTS:
                matcher = hook_config.get('matcher', '')

                if not matcher:
                    score -= 2
                    findings.append(f"❌ {event_name} hook #{i+1}: Empty matcher")
                    continue

                # Validate regex
                try:
                    re.compile(matcher)
                except re.error as e:
                    score -= 3
                    findings.append(f"❌ {event_name} hook #{i+1}: Invalid regex '{matcher}': {e}")
                    continue

                # Check for common mistakes
                if '\\|' in matcher:
                    score -= 1
                    findings.append(f"⚠️  {event_name} hook #{i+1}: Escaped pipe (\\|) - use plain | for OR")

                # Check for overly broad matchers
                if matcher == '*':
                    findings.append(f"ℹ️  {event_name} hook #{i+1}: Using wildcard matcher (applies to ALL tools)")

    if not findings:
        findings.append("✅ All matchers are valid")

    if score < 0:
        score = 0

    return score, findings


def analyze_script_existence(hooks_config: Dict, hooks_file: Path) -> Tuple[int, List[str]]:
    """Analyze if referenced scripts exist (0-10)."""
    score = 10
    findings = []

    if 'hooks' not in hooks_config:
        return 0, ["❌ CRITICAL: No hooks to analyze"]

    base_dir = hooks_file.parent

    for event_name, event_hooks in hooks_config['hooks'].items():
        for i, hook_config in enumerate(event_hooks):
            if 'hooks' not in hook_config:
                continue

            for j, hook_item in enumerate(hook_config['hooks']):
                if hook_item.get('type') == 'command':
                    command = hook_item.get('command', '')

                    # Extract script path
                    if command.startswith('bash ') or command.startswith('sh '):
                        parts = command.split()
                        if len(parts) > 1:
                            script_path = parts[1]

                            # Skip variable substitutions
                            if script_path.startswith('${'):
                                findings.append(f"ℹ️  {event_name} hook #{i+1}, item #{j+1}: Uses variable '{script_path}' (cannot verify)")
                                continue

                            # Check if file exists
                            if script_path.startswith('/'):
                                script_file = Path(script_path)
                            else:
                                script_file = base_dir / script_path

                            if not script_file.exists():
                                score -= 2
                                findings.append(f"❌ {event_name} hook #{i+1}, item #{j+1}: Script not found: {script_path}")
                            elif not script_file.stat().st_mode & 0o111:
                                score -= 1
                                findings.append(f"⚠️  {event_name} hook #{i+1}, item #{j+1}: Script not executable: {script_path}")

    if not findings:
        findings.append("✅ All scripts exist and are executable")

    if score < 0:
        score = 0

    return score, findings


def analyze_hook_types(hooks_config: Dict) -> Tuple[int, List[str]]:
    """Analyze hook type validity and appropriateness (0-10)."""
    score = 10
    findings = []

    if 'hooks' not in hooks_config:
        return 0, ["❌ CRITICAL: No hooks to analyze"]

    for event_name, event_hooks in hooks_config['hooks'].items():
        for i, hook_config in enumerate(event_hooks):
            if 'hooks' not in hook_config:
                continue

            for j, hook_item in enumerate(hook_config['hooks']):
                hook_type = hook_item.get('type', '')

                if hook_type not in ['command', 'prompt']:
                    score -= 3
                    findings.append(f"❌ {event_name} hook #{i+1}, item #{j+1}: Invalid type '{hook_type}'")
                    continue

                # Validate fields
                if hook_type == 'command':
                    if 'command' not in hook_item:
                        score -= 2
                        findings.append(f"❌ {event_name} hook #{i+1}, item #{j+1}: Missing 'command' field")
                    elif not hook_item['command'].strip():
                        score -= 2
                        findings.append(f"❌ {event_name} hook #{i+1}, item #{j+1}: Empty command")

                elif hook_type == 'prompt':
                    if 'prompt' not in hook_item:
                        score -= 2
                        findings.append(f"❌ {event_name} hook #{i+1}, item #{j+1}: Missing 'prompt' field")
                    elif not hook_item['prompt'].strip():
                        score -= 2
                        findings.append(f"❌ {event_name} hook #{i+1}, item #{j+1}: Empty prompt")

    if not findings:
        findings.append("✅ All hook types are valid")

    if score < 0:
        score = 0

    return score, findings


def analyze_documentation(hooks_config: Dict) -> Tuple[int, List[str]]:
    """Analyze documentation quality (0-10)."""
    score = 10
    findings = []

    if 'hooks' not in hooks_config:
        return 0, ["❌ CRITICAL: No hooks to analyze"]

    hooks = hooks_config['hooks']

    # Check for descriptive comments in hook structure
    if '_comment' in hooks_config or 'description' in hooks_config:
        findings.append("✅ Top-level documentation present")
    else:
        score -= 2
        findings.append("⚠️  No top-level documentation (consider adding '_comment' field)")

    # Check prompt clarity
    for event_name, event_hooks in hooks.items():
        for i, hook_config in enumerate(event_hooks):
            if 'hooks' not in hook_config:
                continue

            for j, hook_item in enumerate(hook_config['hooks']):
                if hook_item.get('type') == 'prompt':
                    prompt = hook_item.get('prompt', '')

                    if len(prompt) < 20:
                        score -= 1
                        findings.append(f"⚠️  {event_name} hook #{i+1}, item #{j+1}: Very short prompt (unclear purpose)")

                    # Check for clear decision guidance
                    decision_keywords = ['approve', 'block', 'warn', 'validate', 'check']
                    if not any(kw in prompt.lower() for kw in decision_keywords):
                        score -= 1
                        findings.append(f"⚠️  {event_name} hook #{i+1}, item #{j+1}: Prompt lacks clear decision keywords")

    if not findings:
        findings.append("✅ Documentation is adequate")

    if score < 0:
        score = 0

    return score, findings


def analyze_maintainability(hooks_config: Dict) -> Tuple[int, List[str]]:
    """Analyze maintainability (0-10)."""
    score = 10
    findings = []

    if 'hooks' not in hooks_config:
        return 0, ["❌ CRITICAL: No hooks to analyze"]

    hooks = hooks_config['hooks']

    # Check number of hooks
    total_hooks = sum(
        len(hook_config.get('hooks', []))
        for event_hooks in hooks.values()
        for hook_config in event_hooks
    )

    if total_hooks > 20:
        score -= 2
        findings.append(f"⚠️  Large number of hooks ({total_hooks}) - consider consolidation")
    elif total_hooks == 0:
        score = 0
        findings.append("❌ No hooks defined")

    # Check for duplicate commands
    commands = []
    for event_name, event_hooks in hooks.items():
        for hook_config in event_hooks:
            if 'hooks' not in hook_config:
                continue
            for hook_item in hook_config['hooks']:
                if hook_item.get('type') == 'command':
                    cmd = hook_item.get('command', '')
                    if cmd in commands:
                        score -= 1
                        findings.append(f"⚠️  Duplicate command found: {cmd[:50]}...")
                    commands.append(cmd)

    # Check for consistent naming in scripts
    script_paths = []
    for event_name, event_hooks in hooks.items():
        for hook_config in event_hooks:
            if 'hooks' not in hook_config:
                continue
            for hook_item in hook_config['hooks']:
                if hook_item.get('type') == 'command':
                    cmd = hook_item.get('command', '')
                    if 'bash' in cmd.lower():
                        parts = cmd.split()
                        if len(parts) > 1:
                            script_paths.append(parts[1])

    # Check naming consistency
    if script_paths:
        has_consistent_prefix = all('${CLAUDE_PLUGIN_ROOT}' in p or p.startswith('/') for p in script_paths)
        if not has_consistent_prefix:
            score -= 1
            findings.append("⚠️  Inconsistent script path styles (mix of absolute and relative)")

    if not findings:
        findings.append("✅ Good maintainability")

    if score < 0:
        score = 0

    return score, findings


def generate_recommendations(all_scores: Dict[str, Tuple[int, List[str]]]) -> List[str]:
    """Generate prioritized recommendations based on analysis."""
    recommendations = []

    # Prioritize by score (lowest first)
    sorted_categories = sorted(all_scores.items(), key=lambda x: x[1][0])

    for category, (score, findings) in sorted_categories:
        if score < 7:
            # Extract actionable items (errors and warnings)
            actionable = [f for f in findings if f.startswith('❌') or f.startswith('⚠️')]
            if actionable:
                recommendations.append(f"\n{BOLD}{category} (Score: {score}/10){RESET}")
                for item in actionable[:3]:  # Top 3 issues
                    recommendations.append(f"  • {item}")

    return recommendations


def main():
    if len(sys.argv) < 2:
        print(f"{RED}Usage: enhance-hook.py <hooks.json>{RESET}")
        sys.exit(1)

    hooks_file = Path(sys.argv[1])

    if not hooks_file.exists():
        print(f"{RED}❌ File not found: {hooks_file}{RESET}")
        sys.exit(1)

    # Load hooks
    try:
        content = hooks_file.read_text()
        hooks_config = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"{RED}❌ Invalid JSON: {e}{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{RED}❌ Failed to read file: {e}{RESET}")
        sys.exit(1)

    print(f"\n{BOLD}🔍 HOOK QUALITY ANALYSIS{RESET}")
    print(f"{BOLD}File:{RESET} {hooks_file}\n")
    print("=" * 60)

    # Run analyses
    analyses = {
        "Schema Compliance": analyze_schema_compliance(hooks_config),
        "Security": analyze_security(hooks_config),
        "Matcher Validity": analyze_matcher_validity(hooks_config),
        "Script Existence": analyze_script_existence(hooks_config, hooks_file),
        "Hook Types": analyze_hook_types(hooks_config),
        "Documentation": analyze_documentation(hooks_config),
        "Maintainability": analyze_maintainability(hooks_config),
    }

    # Display results
    total_score = 0
    max_score = 0

    for category, (score, findings) in analyses.items():
        max_score += 10
        total_score += score

        # Color based on score
        if score >= 8:
            color = GREEN
        elif score >= 5:
            color = YELLOW
        else:
            color = RED

        print(f"\n{BOLD}{category}:{RESET} {color}{score}/10{RESET}")
        for finding in findings:
            print(f"  {finding}")

    # Overall score
    overall_percentage = (total_score / max_score * 100) if max_score > 0 else 0
    print("\n" + "=" * 60)

    if overall_percentage >= 80:
        color = GREEN
        grade = "A"
    elif overall_percentage >= 60:
        color = YELLOW
        grade = "B"
    else:
        color = RED
        grade = "C"

    print(f"{BOLD}Overall Score:{RESET} {color}{total_score}/{max_score} ({overall_percentage:.1f}%) - Grade {grade}{RESET}\n")

    # Recommendations
    recommendations = generate_recommendations(analyses)
    if recommendations:
        print(f"{BOLD}🎯 PRIORITY IMPROVEMENTS:{RESET}")
        for rec in recommendations:
            print(rec)
        print()

    # Next steps
    print(f"{BOLD}📋 Next Steps:{RESET}")
    if total_score < max_score * 0.6:
        print(f"  1. Address critical security issues immediately")
        print(f"  2. Fix schema compliance errors")
        print(f"  3. Validate and test all hooks")
    else:
        print(f"  1. Review warnings and recommendations")
        print(f"  2. Test hooks by triggering events")
        print(f"  3. Update documentation as needed")

    # Exit code based on critical errors
    has_critical = any(
        any('❌ CRITICAL' in f for f in findings)
        for _, findings in analyses.values()
    )

    sys.exit(1 if has_critical else 0)


if __name__ == '__main__':
    main()
