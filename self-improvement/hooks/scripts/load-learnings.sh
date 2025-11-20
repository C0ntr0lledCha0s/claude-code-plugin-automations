#!/usr/bin/env bash
#
# Load Learnings Script
# Triggers on SessionStart event
# Loads accumulated learnings and patterns to inform the current session
#

set -euo pipefail

# Cleanup trap for error handling
cleanup() {
    local exit_code=$?
    if [[ $exit_code -ne 0 ]]; then
        # Log error but don't fail the session start
        echo "ERROR: load-learnings.sh failed with exit code $exit_code" >&2
    fi
}
trap cleanup EXIT

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${HOME}/.claude/self-improvement"
PATTERNS_DB="${LOG_DIR}/patterns.json"
LEARNINGS_DB="${LOG_DIR}/learnings.json"
METRICS_DB="${LOG_DIR}/metrics.json"

# Create directory if it doesn't exist
mkdir -p "${LOG_DIR}"

# Generate session ID
SESSION_ID=$(date +%s)

# Function to load and display learnings
load_learnings() {
    if [[ ! -f "${LEARNINGS_DB}" || ! -f "${PATTERNS_DB}" ]]; then
        # First run, no learnings yet
        echo '{"decision": "approve", "suppressOutput": true}'
        exit 0
    fi

    # Pass variables as arguments to Python script
    python3 - "$LEARNINGS_DB" "$PATTERNS_DB" "$SESSION_ID" "$SCRIPT_DIR" <<'EOF'
import json
import sys
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# Get file paths from arguments
learnings_file = sys.argv[1]
patterns_file = sys.argv[2]
session_id = sys.argv[3] if len(sys.argv) > 3 else str(int(datetime.now().timestamp()))
script_dir = sys.argv[4] if len(sys.argv) > 4 else ""

# Actionable templates for each pattern type
# These provide specific guidance instead of generic warnings
ACTIONABLE_TEMPLATES = {
    "missing_tests": {
        "instruction": "Before writing any function, propose test cases first",
        "template": """When implementing functions, follow this pattern:
1. First, outline test cases:
   ```python
   def test_function_name():
       # Test normal case
       assert function_name(valid_input) == expected
       # Test edge case
       assert function_name(empty_input) == expected
       # Test error case
       with pytest.raises(ValueError):
           function_name(invalid_input)
   ```
2. Then implement the function to pass these tests""",
        "priority": "high"
    },
    "missing_validation": {
        "instruction": "Add input validation at the start of every function that accepts parameters",
        "template": """Always validate inputs:
```python
def process_data(data: list, limit: int):
    # Validate inputs first
    if not isinstance(data, list):
        raise TypeError("data must be a list")
    if limit <= 0:
        raise ValueError("limit must be positive")
    if not data:
        return []
    # ... rest of implementation
```""",
        "priority": "high"
    },
    "high_error_rate": {
        "instruction": "Wrap risky operations in try/except with specific exceptions",
        "template": """Use specific exception handling:
```python
try:
    result = risky_operation()
except FileNotFoundError as e:
    logger.error(f"File not found: {e}")
    raise
except ValueError as e:
    return handle_invalid_value(e)
# Avoid bare except or catching Exception
```""",
        "priority": "critical"
    },
    "security_vulnerabilities": {
        "instruction": "Check all code for OWASP Top 10 vulnerabilities before finalizing",
        "template": """Security checklist:
- [ ] No eval() or exec() with user input
- [ ] Parameterized queries for SQL (use ?, :param, %s)
- [ ] No hardcoded secrets (use env vars)
- [ ] Input sanitization before HTML output
- [ ] subprocess with shell=False""",
        "priority": "critical"
    },
    "sql_injection_discussed": {
        "instruction": "Always use parameterized queries, never string concatenation",
        "template": """Use parameterized queries:
```python
# WRONG - SQL injection risk
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# CORRECT - Parameterized
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```""",
        "priority": "critical"
    },
    "xss_discussed": {
        "instruction": "Sanitize all user input before rendering as HTML",
        "template": """Prevent XSS:
```javascript
// WRONG - XSS risk
element.innerHTML = userInput;

// CORRECT - Use textContent or sanitize
element.textContent = userInput;
// or
element.innerHTML = DOMPurify.sanitize(userInput);
```""",
        "priority": "critical"
    },
    "high_code_complexity": {
        "instruction": "Break down complex functions into smaller, focused functions",
        "template": """When a function exceeds 10 lines or has multiple responsibilities:
1. Extract each responsibility into its own function
2. Keep functions under 20 lines
3. Each function should do one thing well
```python
# Instead of one 50-line function, use:
def process_order(order):
    validated = validate_order(order)
    calculated = calculate_totals(validated)
    return format_response(calculated)
```""",
        "priority": "medium"
    },
    "negative_user_experience": {
        "instruction": "Be more explicit about limitations and ask clarifying questions",
        "template": """When uncertain or when requirements are ambiguous:
1. State what you understand
2. List your assumptions
3. Ask specific questions before proceeding
4. Offer alternatives when blocked""",
        "priority": "high"
    },
    "unclear_communication": {
        "instruction": "Structure responses with clear headings and step-by-step explanations",
        "template": """Use this response structure:
1. **Summary**: One-line answer to the question
2. **Details**: Explanation with code examples
3. **Caveats**: Important limitations or edge cases
4. **Next Steps**: What the user should do next""",
        "priority": "medium"
    },
    "poor_error_handling": {
        "instruction": "Replace bare except clauses with specific exception types",
        "template": """Never use bare except:
```python
# WRONG
try:
    something()
except:
    pass

# CORRECT
try:
    something()
except (ValueError, TypeError) as e:
    logger.warning(f"Expected error: {e}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```""",
        "priority": "high"
    }
}

# Load learnings
learnings = []
try:
    with open(learnings_file, 'r') as f:
        learnings_data = json.load(f)
        learnings = learnings_data.get('learnings', [])
except:
    pass

# Load patterns
patterns = []
try:
    with open(patterns_file, 'r') as f:
        patterns_data = json.load(f)
        patterns = patterns_data.get('patterns', [])
except:
    pass

# Filter to most important patterns (higher thresholds for actionable output)
critical_patterns = [p for p in patterns if p.get('severity') == 'critical' and p.get('count', 0) >= 2]
important_patterns = [p for p in patterns if p.get('severity') == 'important' and p.get('count', 0) >= 3]

# Get learnings that have actionable templates
actionable_learnings = [l for l in learnings if l.get('key') in ACTIONABLE_TEMPLATES]

# Build actionable context message
if critical_patterns or important_patterns or actionable_learnings:
    context_parts = []

    # Session guidance header
    context_parts.append("## Session Guidance Based on Past Patterns\n")

    # Critical actions needed
    if critical_patterns:
        context_parts.append("### Critical Actions Required\n")
        for pattern in critical_patterns[:2]:  # Limit to top 2
            pattern_type = pattern['type']
            if pattern_type in ACTIONABLE_TEMPLATES:
                template = ACTIONABLE_TEMPLATES[pattern_type]
                context_parts.append(f"**{template['instruction']}** (issue seen {pattern['count']}x)\n")
                context_parts.append(template['template'])
                context_parts.append("")  # blank line
            else:
                context_parts.append(f"- Watch for: {pattern['type']} ({pattern['count']}x)")

    # Important actions
    if important_patterns:
        context_parts.append("\n### Important Reminders\n")
        for pattern in important_patterns[:2]:  # Limit to top 2
            pattern_type = pattern['type']
            if pattern_type in ACTIONABLE_TEMPLATES:
                template = ACTIONABLE_TEMPLATES[pattern_type]
                context_parts.append(f"**{template['instruction']}**\n")
            else:
                context_parts.append(f"- Remember: {pattern['type']} ({pattern['count']}x)")

    # Specific learnings with templates
    if actionable_learnings:
        shown_keys = set()  # Avoid duplicates with patterns
        for learning in actionable_learnings[-3:]:
            key = learning.get('key')
            if key and key not in shown_keys and key in ACTIONABLE_TEMPLATES:
                shown_keys.add(key)
                template = ACTIONABLE_TEMPLATES[key]
                if template['priority'] == 'critical' and not any(p['type'] == key for p in critical_patterns):
                    context_parts.append(f"\n**{template['instruction']}**\n")
                    context_parts.append(template['template'])

    context_message = "\n".join(context_parts)

    # Record advice given for compliance tracking
    advice_given = []
    for pattern in critical_patterns + important_patterns:
        advice_given.append(pattern['type'])
    for learning in actionable_learnings[-3:]:
        key = learning.get('key')
        if key and key not in advice_given:
            advice_given.append(key)

    # Call compliance tracker to record advice
    if script_dir and advice_given:
        tracker_path = Path(script_dir) / "compliance-tracker.py"
        if tracker_path.exists():
            try:
                subprocess.run(
                    ["python3", str(tracker_path), "record", session_id, json.dumps(advice_given)],
                    capture_output=True,
                    timeout=5
                )
            except Exception:
                pass  # Don't fail session start if tracking fails

    # Output for Claude to use
    result = {
        "decision": "approve",
        "hookSpecificOutput": {
            "additionalContext": f"""
{context_message}

---
*Apply these patterns proactively. Goal: reduce pattern frequency over time.*
"""
        }
    }
    print(json.dumps(result))
else:
    # No significant learnings yet, suppress output
    print('{"decision": "approve", "suppressOutput": true}')

EOF
}

# Main execution
# Strip Windows CRLF from Python output to ensure clean JSON
load_learnings | tr -d '\r'
exit 0
