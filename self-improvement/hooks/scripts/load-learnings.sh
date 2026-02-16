#!/usr/bin/env bash
#
# Load Learnings Script
# Triggers on SessionStart event
# Loads accumulated learnings and patterns to inform the current session
#

set -uo pipefail

# Track whether we've already sent JSON output
OUTPUT_SENT=false

# Cleanup trap for error handling
cleanup() {
    local exit_code=$?
    if [[ $exit_code -ne 0 && "$OUTPUT_SENT" != "true" ]]; then
        # Log error to stderr but don't fail the session start
        echo "ERROR: load-learnings.sh failed with exit code $exit_code" >&2
        # Ensure we always output valid JSON even on error
        printf '{"decision": "approve", "reason": "Hook error - continuing session"}\n' | tr -d '\r'
    fi
}
trap cleanup EXIT

# Configuration
LOG_DIR="${HOME}/.claude/self-improvement"
PATTERNS_DB="${LOG_DIR}/patterns.json"
LEARNINGS_DB="${LOG_DIR}/learnings.json"

# Create directory if it doesn't exist
mkdir -p "${LOG_DIR}"

# Function to load and display learnings
load_learnings() {
    if [[ ! -f "${LEARNINGS_DB}" || ! -f "${PATTERNS_DB}" ]]; then
        # First run, no learnings yet
        echo '{"decision": "approve", "suppressOutput": true}'
        exit 0
    fi

    # Pass variables as arguments to Python script
    # Use a temporary file to capture Python output and extract only JSON
    local temp_output
    temp_output=$(mktemp)
    trap "rm -f '$temp_output'" RETURN

    python3 - "$LEARNINGS_DB" "$PATTERNS_DB" > "$temp_output" 2>/dev/null <<'EOF'
import json
import sys
import warnings

# Suppress all warnings to keep output clean
warnings.filterwarnings('ignore')

# Get file paths from arguments
learnings_file = sys.argv[1]
patterns_file = sys.argv[2]

# Short descriptions for known pattern types
PATTERN_LABELS = {
    "missing_tests": "Propose test cases before writing functions",
    "missing_validation": "Add input validation at function boundaries",
    "high_error_rate": "Use specific exception handling",
    "security_vulnerabilities": "Check for OWASP Top 10 vulnerabilities",
    "sql_injection_discussed": "Use parameterized queries",
    "xss_discussed": "Sanitize user input before HTML rendering",
    "high_code_complexity": "Break complex functions into smaller ones",
    "negative_user_experience": "Ask clarifying questions when uncertain",
    "unclear_communication": "Structure responses with clear headings",
    "poor_error_handling": "Use specific exception types instead of bare except",
    "high_bug_discussion": "Write defensive code with edge case handling",
    "security_focus": "Review code for security vulnerabilities",
}

# Load patterns
patterns = []
try:
    with open(patterns_file, 'r') as f:
        patterns_data = json.load(f)
        patterns = patterns_data.get('patterns', [])
except Exception:
    pass

# Filter to significant patterns
significant = [p for p in patterns
    if (p.get('severity') == 'critical' and p.get('count', 0) >= 2)
    or (p.get('severity') == 'important' and p.get('count', 0) >= 3)]

# Sort by count descending, take top 5
significant.sort(key=lambda p: p.get('count', 0), reverse=True)
significant = significant[:5]

if significant:
    parts = []
    for p in significant:
        label = PATTERN_LABELS.get(p['type'], p['type'].replace('_', ' '))
        parts.append(f"{label} ({p['count']}x)")

    message = "Session reminders: " + " | ".join(parts)

    result = {
        "decision": "approve",
        "systemMessage": message
    }
    print(json.dumps(result))
else:
    print('{"decision": "approve", "suppressOutput": true}')

EOF

    # Extract only valid JSON from the output (last line starting with {)
    local json_output
    json_output=$(grep -E '^\{' "$temp_output" | tail -1 || echo '')

    OUTPUT_SENT=true
    if [[ -n "$json_output" ]]; then
        echo "$json_output"
    else
        # If no valid JSON found, output a default approval
        echo '{"decision": "approve", "reason": "No learnings to load"}'
    fi
}

# Main execution
# Strip Windows CRLF from Python output to ensure clean JSON
load_learnings | tr -d '\r'
exit 0
