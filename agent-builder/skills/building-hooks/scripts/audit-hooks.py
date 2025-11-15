#!/usr/bin/env python3
"""
Bulk hooks auditor for Claude Code repositories.

Finds and validates all hooks.json files with security focus.
"""

import json
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple

# ANSI colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"


def find_hooks_files(root_dir: Path) -> List[Path]:
    """Find all hooks.json files in directory tree."""
    hooks_files = []

    # Common locations
    patterns = [
        "*/hooks/hooks.json",
        "**/hooks.json",
        ".claude/hooks.json",
    ]

    for pattern in patterns:
        hooks_files.extend(root_dir.glob(pattern))

    # Remove duplicates
    return list(set(hooks_files))


def run_validation(hooks_file: Path, validator_script: Path) -> Tuple[bool, str]:
    """Run validation script on hooks file."""
    try:
        result = subprocess.run(
            ["python3", str(validator_script), str(hooks_file)],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Validation timed out"
    except Exception as e:
        return False, f"Validation failed: {e}"


def count_security_issues(output: str) -> Tuple[int, int]:
    """Count critical and warning security issues from output."""
    critical = output.count("❌ CRITICAL:")
    critical += output.count("CRITICAL:")
    warnings = output.count("⚠️")
    warnings += output.count("WARNING:")
    return critical, warnings


def main():
    verbose = "--verbose" in sys.argv

    # Find root directory
    if len(sys.argv) > 1 and not sys.argv[1].startswith('--'):
        root_dir = Path(sys.argv[1])
    else:
        root_dir = Path.cwd()

    print(f"\n{BOLD}🔍 HOOKS AUDIT{RESET}")
    print(f"{BOLD}Directory:{RESET} {root_dir}\n")

    # Find validator script
    validator_script = Path(__file__).parent / "validate-hooks.py"
    if not validator_script.exists():
        # Try alternate location
        validator_script = root_dir / "agent-builder/skills/building-hooks/scripts/validate-hooks.py"

    if not validator_script.exists():
        print(f"{YELLOW}⚠️  Validator script not found, using basic validation{RESET}\n")
        validator_script = None

    # Find all hooks files
    hooks_files = find_hooks_files(root_dir)

    if not hooks_files:
        print(f"{YELLOW}⚠️  No hooks.json files found{RESET}")
        sys.exit(0)

    print(f"Found {len(hooks_files)} hooks.json file(s)\n")
    print("=" * 60)

    # Audit each file
    results = {
        'valid': [],
        'warnings': [],
        'errors': [],
        'parse_errors': []
    }

    for hooks_file in sorted(hooks_files):
        rel_path = hooks_file.relative_to(root_dir) if hooks_file.is_relative_to(root_dir) else hooks_file
        print(f"\n{BOLD}{rel_path}{RESET}")

        # Try to load JSON
        try:
            content = hooks_file.read_text()
            config = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"{RED}❌ JSON Parse Error: {e}{RESET}")
            results['parse_errors'].append((rel_path, str(e)))
            continue
        except Exception as e:
            print(f"{RED}❌ Read Error: {e}{RESET}")
            results['parse_errors'].append((rel_path, str(e)))
            continue

        # Run validation if available
        if validator_script:
            is_valid, output = run_validation(hooks_file, validator_script)

            if is_valid:
                print(f"{GREEN}✓ Valid{RESET}")
                results['valid'].append(rel_path)
            else:
                # Count issues
                critical, warnings = count_security_issues(output)

                if critical > 0:
                    print(f"{RED}❌ {critical} critical error(s){RESET}")
                    results['errors'].append((rel_path, critical, warnings))
                elif warnings > 0:
                    print(f"{YELLOW}⚠️  {warnings} warning(s){RESET}")
                    results['warnings'].append((rel_path, warnings))

                if verbose:
                    print(output)

        else:
            # Basic validation
            if 'hooks' in config and isinstance(config['hooks'], dict):
                hooks_count = sum(
                    len(hook_config.get('hooks', []))
                    for event_hooks in config['hooks'].values()
                    for hook_config in event_hooks
                )
                print(f"{GREEN}✓ Valid JSON structure ({hooks_count} hooks){RESET}")
                results['valid'].append(rel_path)
            else:
                print(f"{RED}❌ Invalid structure{RESET}")
                results['errors'].append((rel_path, 1, 0))

    # Summary
    print("\n" + "=" * 60)
    print(f"\n{BOLD}📊 AUDIT SUMMARY{RESET}\n")

    print(f"{GREEN}Valid:{RESET} {len(results['valid'])}")
    print(f"{YELLOW}Warnings:{RESET} {len(results['warnings'])}")
    print(f"{RED}Errors:{RESET} {len(results['errors'])}")
    print(f"{RED}Parse Errors:{RESET} {len(results['parse_errors'])}")

    # Details
    if results['errors']:
        print(f"\n{BOLD}Files with errors:{RESET}")
        for path, critical, warnings in results['errors']:
            print(f"  {RED}❌{RESET} {path} ({critical} critical, {warnings} warnings)")

    if results['warnings']:
        print(f"\n{BOLD}Files with warnings:{RESET}")
        for path, warnings in results['warnings']:
            print(f"  {YELLOW}⚠️ {RESET} {path} ({warnings} warnings)")

    if results['parse_errors']:
        print(f"\n{BOLD}Files with parse errors:{RESET}")
        for path, error in results['parse_errors']:
            print(f"  {RED}❌{RESET} {path}: {error}")

    # Exit code
    has_errors = len(results['errors']) > 0 or len(results['parse_errors']) > 0

    if has_errors:
        print(f"\n{RED}❌ Audit completed with errors{RESET}")
        sys.exit(1)
    elif results['warnings']:
        print(f"\n{YELLOW}⚠️  Audit completed with warnings{RESET}")
        sys.exit(0)
    else:
        print(f"\n{GREEN}✓ All hooks are valid!{RESET}")
        sys.exit(0)


if __name__ == '__main__':
    main()
