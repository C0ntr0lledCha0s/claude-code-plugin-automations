#!/usr/bin/env bash
#
# Pre-Write Analysis Script
# Triggers on PreToolUse for Write and Edit operations
# Analyzes code for security issues and quality problems BEFORE writing
#
# This provides real-time feedback to prevent mistakes rather than logging them after.

set -uo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${HOME}/.claude/self-improvement"
DEBUG_LOG="${LOG_DIR}/pre-write-debug.log"

# Create directories
mkdir -p "${LOG_DIR}"

# Debug logging
debug_log() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo "unknown")
    echo "[$timestamp] $1" >> "$DEBUG_LOG" 2>/dev/null || true
}

# Initialize debug log
echo "=== Pre-Write Analysis ===" > "$DEBUG_LOG" 2>/dev/null || true
debug_log "Script started"

# Check for Python
if ! command -v python3 &> /dev/null; then
    debug_log "Python3 not found"
    echo '{"decision": "approve"}'
    exit 0
fi

# Read hook payload from stdin
payload=$(cat)
debug_log "Received payload length: ${#payload}"

if [[ -z "${payload}" ]]; then
    debug_log "Empty payload"
    echo '{"decision": "approve"}'
    exit 0
fi

# Analyze the content and provide feedback
python3 - "$payload" "$SCRIPT_DIR" <<'EOF'
import json
import sys
import os
import re

payload_str = sys.argv[1]
script_dir = sys.argv[2]

try:
    payload = json.loads(payload_str)
except json.JSONDecodeError as e:
    print('{"decision": "approve"}')
    sys.exit(0)

# Get tool name and input
tool_name = payload.get("tool_name", "")
tool_input = payload.get("tool_input", {})

# Only analyze Write and Edit operations
if tool_name not in ("Write", "Edit"):
    print('{"decision": "approve"}')
    sys.exit(0)

# Get the content being written
content = ""
if tool_name == "Write":
    content = tool_input.get("content", "")
elif tool_name == "Edit":
    content = tool_input.get("new_string", "")

if not content:
    print('{"decision": "approve"}')
    sys.exit(0)

# Get file path for context
file_path = tool_input.get("file_path", "")
file_ext = os.path.splitext(file_path)[1].lower() if file_path else ""

# Security patterns to check - CRITICAL issues that should warn
CRITICAL_PATTERNS = [
    (r'\beval\s*\(', "eval() detected - can execute arbitrary code"),
    (r'\bexec\s*\(', "exec() detected - can execute arbitrary code"),
    (r'password\s*=\s*["\'][^"\']{5,}["\']', "Potential hardcoded password"),
    (r'api_?key\s*=\s*["\'][^"\']{10,}["\']', "Potential hardcoded API key"),
    (r'secret\s*=\s*["\'][^"\']{5,}["\']', "Potential hardcoded secret"),
    (r'subprocess.*shell\s*=\s*True', "shell=True is dangerous - use shell=False"),
    (r'\.innerHTML\s*=\s*[^"\'`]', "innerHTML with variable - potential XSS"),
    (r'rm\s+-rf?\s+["\']?\$', "rm -rf with variable - dangerous"),
]

# Important patterns - should suggest but not block
IMPORTANT_PATTERNS = [
    (r'except:\s*$', "Bare except clause - specify exception types"),
    (r'except\s+Exception\s*:', "Catching all exceptions - be more specific"),
    (r'SELECT.*FROM.*["\'].*\+', "SQL string concatenation - use parameterized queries"),
    (r'pickle\.load', "pickle can execute arbitrary code - use safe alternatives"),
]

issues = []
suggestions = []

# Check critical patterns
for pattern, message in CRITICAL_PATTERNS:
    if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
        issues.append(message)

# Check important patterns
for pattern, message in IMPORTANT_PATTERNS:
    if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
        suggestions.append(message)

# Build response
if issues:
    # Critical security issues found - warn but approve
    # (blocking would be too disruptive, but we want visibility)
    warning_message = "⚠️ **Security Review Needed**\n\n"
    warning_message += "The following issues were detected:\n"
    for issue in issues[:3]:  # Limit to 3
        warning_message += f"- {issue}\n"

    if suggestions:
        warning_message += "\nAdditional suggestions:\n"
        for suggestion in suggestions[:2]:
            warning_message += f"- {suggestion}\n"

    warning_message += "\nConsider addressing these before finalizing."

    result = {
        "decision": "approve",
        "hookSpecificOutput": {
            "message": warning_message
        }
    }
    print(json.dumps(result))

elif suggestions and len(suggestions) >= 2:
    # Multiple suggestions - worth mentioning
    suggestion_message = "💡 **Code Quality Suggestions**\n\n"
    for suggestion in suggestions[:3]:
        suggestion_message += f"- {suggestion}\n"

    result = {
        "decision": "approve",
        "hookSpecificOutput": {
            "message": suggestion_message
        }
    }
    print(json.dumps(result))

else:
    # No significant issues
    print('{"decision": "approve"}')

EOF

exit 0
