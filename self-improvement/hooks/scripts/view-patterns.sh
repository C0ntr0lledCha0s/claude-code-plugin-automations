#!/usr/bin/env bash
#
# View Patterns Script
# Display all tracked patterns and their statistics
#

set -euo pipefail

LOG_DIR="${HOME}/.claude/self-improvement"
PATTERNS_DB="${LOG_DIR}/patterns.json"

if [[ ! -f "${PATTERNS_DB}" ]]; then
    echo "No patterns tracked yet. The system will start tracking after conversations end."
    exit 0
fi

python3 - <<'EOF'
import json
from datetime import datetime

patterns_file = "${PATTERNS_DB}"

with open(patterns_file, 'r') as f:
    data = json.load(f)

patterns = data.get('patterns', [])

if not patterns:
    print("No patterns tracked yet.")
    exit(0)

# Sort by severity and count
severity_order = {'critical': 0, 'important': 1, 'minor': 2}
sorted_patterns = sorted(
    patterns,
    key=lambda x: (severity_order.get(x.get('severity', 'minor'), 3), -x.get('count', 0))
)

print("=" * 80)
print("📊 TRACKED PATTERNS - Self-Improvement System")
print("=" * 80)
print()

for pattern in sorted_patterns:
    severity = pattern.get('severity', 'minor')
    severity_emoji = {'critical': '🔴', 'important': '🟡', 'minor': '🟢'}.get(severity, '⚪')

    print(f"{severity_emoji} {severity.upper()}: {pattern['type']}")
    print(f"   Description: {pattern['description']}")
    print(f"   Occurrences: {pattern.get('count', 0)}")
    print(f"   First seen: {pattern.get('first_seen', 'N/A')}")
    print(f"   Last seen: {pattern.get('last_seen', 'N/A')}")
    print()

print("=" * 80)
print(f"Total patterns tracked: {len(patterns)}")
print(f"Critical: {sum(1 for p in patterns if p.get('severity') == 'critical')}")
print(f"Important: {sum(1 for p in patterns if p.get('severity') == 'important')}")
print(f"Minor: {sum(1 for p in patterns if p.get('severity') == 'minor')}")
print("=" * 80)
EOF
