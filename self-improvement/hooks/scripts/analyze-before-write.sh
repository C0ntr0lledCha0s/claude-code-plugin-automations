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
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$SCRIPT_DIR")")}"
LOG_DIR="${HOME}/.claude/self-improvement"
DEBUG_LOG="${LOG_DIR}/pre-write-debug.log"
WARNING_TRACKER="${LOG_DIR}/warning-tracker.json"
USER_CONFIG="${LOG_DIR}/config.json"
DEFAULT_CONFIG="${PLUGIN_ROOT}/config/default-config.json"

# Create directories
mkdir -p "${LOG_DIR}"

# Initialize warning tracker if it doesn't exist
if [[ ! -f "${WARNING_TRACKER}" ]]; then
    echo '{"warnings": [], "stats": {"total_issued": 0, "total_addressed": 0, "total_ignored": 0}}' > "${WARNING_TRACKER}"
fi

# Use user config if exists, otherwise use default
CONFIG_FILE="${USER_CONFIG}"
if [[ ! -f "${USER_CONFIG}" && -f "${DEFAULT_CONFIG}" ]]; then
    CONFIG_FILE="${DEFAULT_CONFIG}"
fi

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
python3 - "$payload" "$SCRIPT_DIR" "$WARNING_TRACKER" "$CONFIG_FILE" <<'EOF'
import json
import sys
import os
import re
from datetime import datetime
from pathlib import Path

payload_str = sys.argv[1]
script_dir = sys.argv[2]
warning_tracker_path = sys.argv[3] if len(sys.argv) > 3 else ""
config_path = sys.argv[4] if len(sys.argv) > 4 else ""

def load_config():
    """Load configuration."""
    default_config = {
        "enforcement": {
            "critical_issues": "warn",
            "important_issues": "warn",
            "repeated_ignores": "warn",
            "require_confirmation_after": 3
        }
    }
    if not config_path or not Path(config_path).exists():
        return default_config
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except:
        return default_config

def load_warning_tracker():
    """Load warning tracker data."""
    if not warning_tracker_path or not Path(warning_tracker_path).exists():
        return {"warnings": [], "stats": {"total_issued": 0, "total_addressed": 0, "total_ignored": 0}}
    try:
        with open(warning_tracker_path, 'r') as f:
            return json.load(f)
    except:
        return {"warnings": [], "stats": {"total_issued": 0, "total_addressed": 0, "total_ignored": 0}}

def save_warning_tracker(data):
    """Save warning tracker data."""
    if not warning_tracker_path:
        return
    try:
        with open(warning_tracker_path, 'w') as f:
            json.dump(data, f, indent=2)
    except:
        pass

def check_previous_warnings(file_path, current_issues):
    """Check if previous warnings for this file were addressed."""
    tracker = load_warning_tracker()
    addressed = []
    ignored = []

    # Find warnings for this file that haven't been resolved
    remaining_warnings = []
    for warning in tracker.get("warnings", []):
        if warning.get("file_path") == file_path and warning.get("status") == "active":
            # Check if this issue is still present
            issue_type = warning.get("issue_type", "")
            if issue_type in current_issues:
                # Issue still present - mark as ignored
                warning["status"] = "ignored"
                tracker["stats"]["total_ignored"] += 1
                ignored.append(issue_type)
            else:
                # Issue was fixed - mark as addressed
                warning["status"] = "addressed"
                tracker["stats"]["total_addressed"] += 1
                addressed.append(issue_type)
        else:
            remaining_warnings.append(warning)

    # Keep only last 50 warnings
    tracker["warnings"] = remaining_warnings[-50:]
    save_warning_tracker(tracker)

    return addressed, ignored

def record_warnings(file_path, issues):
    """Record new warnings for tracking."""
    if not issues:
        return

    tracker = load_warning_tracker()
    timestamp = datetime.now().isoformat()

    for issue in issues:
        tracker["warnings"].append({
            "file_path": file_path,
            "issue_type": issue,
            "timestamp": timestamp,
            "status": "active"
        })
        tracker["stats"]["total_issued"] += 1

    # Keep only last 50 warnings
    tracker["warnings"] = tracker["warnings"][-50:]
    save_warning_tracker(tracker)

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
issue_types = []  # Short identifiers for tracking
suggestions = []

# Check critical patterns
for pattern, message in CRITICAL_PATTERNS:
    if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
        issues.append(message)
        # Extract short type from message
        issue_type = message.split()[0].lower().rstrip('()')
        issue_types.append(issue_type)

# Check important patterns
for pattern, message in IMPORTANT_PATTERNS:
    if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
        suggestions.append(message)

# Check if previous warnings were addressed
addressed, ignored = check_previous_warnings(file_path, issue_types)

# Load config for enforcement policy
config = load_config()
enforcement = config.get("enforcement", {})
critical_policy = enforcement.get("critical_issues", "warn")
repeated_threshold = enforcement.get("require_confirmation_after", 3)

# Build response
if issues:
    # Record new warnings for tracking
    record_warnings(file_path, issue_types)

    # Check if we should block
    should_block = False
    block_reason = ""

    if critical_policy == "block":
        should_block = True
        block_reason = "Critical security issues detected"
    elif len(ignored) >= repeated_threshold:
        # Too many repeated ignores
        repeated_policy = enforcement.get("repeated_ignores", "warn")
        if repeated_policy == "block":
            should_block = True
            block_reason = f"Warning ignored {len(ignored)}+ times"

    if should_block:
        # Block the operation
        block_message = f"🚫 **Blocked: {block_reason}**\n\n"
        block_message += "The following critical issues must be addressed:\n"
        for issue in issues[:3]:
            block_message += f"- {issue}\n"
        block_message += "\nFix these issues before proceeding."

        result = {
            "decision": "block",
            "reason": block_message
        }
        print(json.dumps(result))
    else:
        # Warn but approve
        warning_message = "⚠️ **Security Review Needed**\n\n"

        # Note if previous warnings were ignored
        if ignored:
            warning_message += f"🔴 **Previous warnings ignored**: {', '.join(ignored)}\n\n"

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

elif addressed:
    # Previous warnings were addressed - positive feedback
    success_message = "✅ **Previous issues addressed**\n\n"
    success_message += f"Fixed: {', '.join(addressed)}\n"
    success_message += "\nGreat job addressing the warnings!"

    result = {
        "decision": "approve",
        "hookSpecificOutput": {
            "message": success_message
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
