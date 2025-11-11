#!/usr/bin/env bash
#
# Load Learnings Script
# Triggers on SessionStart event
# Loads accumulated learnings and patterns to inform the current session
#

set -euo pipefail

# Configuration
LOG_DIR="${HOME}/.claude/self-improvement"
PATTERNS_DB="${LOG_DIR}/patterns.json"
LEARNINGS_DB="${LOG_DIR}/learnings.json"
METRICS_DB="${LOG_DIR}/metrics.json"

# Create directory if it doesn't exist
mkdir -p "${LOG_DIR}"

# Function to load and display learnings
load_learnings() {
    if [[ ! -f "${LEARNINGS_DB}" || ! -f "${PATTERNS_DB}" ]]; then
        # First run, no learnings yet
        echo '{"decision": "allow", "suppressOutput": true}'
        exit 0
    fi

    python3 - <<'EOF'
import json
import sys
from datetime import datetime, timedelta

learnings_file = "${LEARNINGS_DB}"
patterns_file = "${PATTERNS_DB}"

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

# Filter to most important learnings and patterns
critical_patterns = [p for p in patterns if p.get('severity') == 'critical' and p.get('count', 0) >= 2]
important_patterns = [p for p in patterns if p.get('severity') == 'important' and p.get('count', 0) >= 3]
recent_learnings = learnings[-10:]  # Last 10 learnings

# Build context message
if critical_patterns or important_patterns or recent_learnings:
    context_parts = []

    if critical_patterns:
        context_parts.append("⚠️ Critical patterns to watch:")
        for pattern in critical_patterns[:3]:
            context_parts.append(f"  • {pattern['type']}: {pattern['description']} (seen {pattern['count']}x)")

    if important_patterns:
        context_parts.append("\n📋 Important patterns to remember:")
        for pattern in important_patterns[:3]:
            context_parts.append(f"  • {pattern['type']}: {pattern['description']} (seen {pattern['count']}x)")

    if recent_learnings:
        context_parts.append("\n💡 Recent learning points:")
        for learning in recent_learnings[-5:]:
            context_parts.append(f"  • {learning['text']}")

    context_message = "\n".join(context_parts)

    # Output for Claude to see
    result = {
        "decision": "allow",
        "hookSpecificOutput": {
            "additionalContext": f"""
🔄 Self-Improvement Context Loaded

{context_message}

Apply these learnings proactively in this session to avoid repeating past issues.
"""
        }
    }
    print(json.dumps(result))
else:
    # No significant learnings yet, suppress output
    print('{"decision": "allow", "suppressOutput": true}')

EOF
}

# Main execution
load_learnings
exit 0
