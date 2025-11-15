#!/usr/bin/env python3
"""
Compare two hooks.json files side-by-side.

Shows differences in structure, hooks, and configuration.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# ANSI colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


def load_hooks(file_path: Path) -> Tuple[Dict, str]:
    """Load hooks.json file."""
    try:
        content = file_path.read_text()
        config = json.loads(content)
        return config, ""
    except json.JSONDecodeError as e:
        return {}, f"Invalid JSON: {e}"
    except Exception as e:
        return {}, f"Read error: {e}"


def count_hooks(config: Dict) -> Dict[str, int]:
    """Count hooks by event type."""
    counts = {}

    if 'hooks' not in config:
        return counts

    for event_name, event_hooks in config['hooks'].items():
        count = sum(
            len(hook_config.get('hooks', []))
            for hook_config in event_hooks
        )
        counts[event_name] = count

    return counts


def get_hook_summary(config: Dict) -> Dict:
    """Get summary statistics."""
    summary = {
        'total_events': 0,
        'total_hooks': 0,
        'command_hooks': 0,
        'prompt_hooks': 0,
        'events': []
    }

    if 'hooks' not in config:
        return summary

    summary['total_events'] = len(config['hooks'])

    for event_name, event_hooks in config['hooks'].items():
        summary['events'].append(event_name)

        for hook_config in event_hooks:
            if 'hooks' not in hook_config:
                continue

            for hook_item in hook_config['hooks']:
                summary['total_hooks'] += 1

                if hook_item.get('type') == 'command':
                    summary['command_hooks'] += 1
                elif hook_item.get('type') == 'prompt':
                    summary['prompt_hooks'] += 1

    return summary


def compare_structures(config1: Dict, config2: Dict) -> List[str]:
    """Compare overall structures."""
    diffs = []

    summary1 = get_hook_summary(config1)
    summary2 = get_hook_summary(config2)

    # Compare events
    events1 = set(summary1['events'])
    events2 = set(summary2['events'])

    only_in_1 = events1 - events2
    only_in_2 = events2 - events1
    common = events1 & events2

    if only_in_1:
        diffs.append(f"{RED}Events only in file 1: {', '.join(sorted(only_in_1))}{RESET}")

    if only_in_2:
        diffs.append(f"{GREEN}Events only in file 2: {', '.join(sorted(only_in_2))}{RESET}")

    if common:
        diffs.append(f"Common events: {', '.join(sorted(common))}")

    # Compare counts
    if summary1['total_hooks'] != summary2['total_hooks']:
        diffs.append(
            f"Total hooks: {RED}{summary1['total_hooks']}{RESET} vs {GREEN}{summary2['total_hooks']}{RESET}"
        )

    if summary1['command_hooks'] != summary2['command_hooks']:
        diffs.append(
            f"Command hooks: {RED}{summary1['command_hooks']}{RESET} vs {GREEN}{summary2['command_hooks']}{RESET}"
        )

    if summary1['prompt_hooks'] != summary2['prompt_hooks']:
        diffs.append(
            f"Prompt hooks: {RED}{summary1['prompt_hooks']}{RESET} vs {GREEN}{summary2['prompt_hooks']}{RESET}"
        )

    return diffs


def compare_events(config1: Dict, config2: Dict) -> List[str]:
    """Compare event-by-event."""
    diffs = []

    if 'hooks' not in config1 and 'hooks' not in config2:
        return ["Both files have no hooks"]

    hooks1 = config1.get('hooks', {})
    hooks2 = config2.get('hooks', {})

    all_events = sorted(set(hooks1.keys()) | set(hooks2.keys()))

    for event in all_events:
        event_hooks1 = hooks1.get(event, [])
        event_hooks2 = hooks2.get(event, [])

        count1 = sum(len(hc.get('hooks', [])) for hc in event_hooks1)
        count2 = sum(len(hc.get('hooks', [])) for hc in event_hooks2)

        if count1 != count2:
            diffs.append(
                f"{BOLD}{event}:{RESET} {RED}{count1}{RESET} vs {GREEN}{count2}{RESET} hooks"
            )
        else:
            diffs.append(f"{BOLD}{event}:{RESET} {count1} hooks (same)")

    return diffs


def show_detailed_diff(config1: Dict, config2: Dict):
    """Show detailed unified diff."""
    print(f"\n{BOLD}📝 Detailed Differences:{RESET}\n")

    json1 = json.dumps(config1, indent=2, sort_keys=True)
    json2 = json.dumps(config2, indent=2, sort_keys=True)

    lines1 = json1.splitlines()
    lines2 = json2.splitlines()

    # Simple line-by-line comparison
    max_lines = max(len(lines1), len(lines2))

    for i in range(max_lines):
        line1 = lines1[i] if i < len(lines1) else ""
        line2 = lines2[i] if i < len(lines2) else ""

        if line1 != line2:
            if line1:
                print(f"{RED}- {line1}{RESET}")
            if line2:
                print(f"{GREEN}+ {line2}{RESET}")
        else:
            # Show context (first 10 and last 10 matching lines)
            if i < 10 or i > max_lines - 10:
                print(f"  {line1}")


def main():
    if len(sys.argv) < 3:
        print(f"{RED}Usage: compare-hooks.py <hooks1.json> <hooks2.json>{RESET}")
        sys.exit(1)

    file1 = Path(sys.argv[1])
    file2 = Path(sys.argv[2])

    # Load files
    config1, error1 = load_hooks(file1)
    if error1:
        print(f"{RED}❌ File 1 error: {error1}{RESET}")
        sys.exit(1)

    config2, error2 = load_hooks(file2)
    if error2:
        print(f"{RED}❌ File 2 error: {error2}{RESET}")
        sys.exit(1)

    # Display comparison
    print(f"\n{BOLD}⚖️  HOOKS COMPARISON{RESET}\n")
    print(f"{CYAN}File 1:{RESET} {file1}")
    print(f"{CYAN}File 2:{RESET} {file2}\n")
    print("=" * 60)

    # Structure comparison
    print(f"\n{BOLD}📊 Structure Comparison:{RESET}\n")
    struct_diffs = compare_structures(config1, config2)
    for diff in struct_diffs:
        print(f"  {diff}")

    # Event comparison
    print(f"\n{BOLD}📋 Event-by-Event Comparison:{RESET}\n")
    event_diffs = compare_events(config1, config2)
    for diff in event_diffs:
        print(f"  {diff}")

    # Detailed diff
    if '--verbose' in sys.argv or '-v' in sys.argv:
        show_detailed_diff(config1, config2)

    # Similarity score
    json1 = json.dumps(config1, sort_keys=True)
    json2 = json.dumps(config2, sort_keys=True)

    if json1 == json2:
        print(f"\n{GREEN}✓ Files are identical{RESET}")
        similarity = 100.0
    else:
        # Simple similarity based on common lines
        lines1 = set(json.dumps(config1, indent=2, sort_keys=True).splitlines())
        lines2 = set(json.dumps(config2, indent=2, sort_keys=True).splitlines())

        common_lines = lines1 & lines2
        total_lines = lines1 | lines2

        similarity = (len(common_lines) / len(total_lines) * 100) if total_lines else 0

        print(f"\n{BOLD}Similarity:{RESET} {similarity:.1f}%")

    print()


if __name__ == '__main__':
    main()
