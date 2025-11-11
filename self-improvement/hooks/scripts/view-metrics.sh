#!/usr/bin/env bash
#
# View Metrics Script
# Display conversation metrics and trends
#

set -euo pipefail

LOG_DIR="${HOME}/.claude/self-improvement"
METRICS_DB="${LOG_DIR}/metrics.json"

if [[ ! -f "${METRICS_DB}" ]]; then
    echo "No metrics tracked yet. The system will start tracking after conversations end."
    exit 0
fi

python3 - <<'EOF'
import json
from datetime import datetime
from statistics import mean, median

metrics_file = "${METRICS_DB}"

with open(metrics_file, 'r') as f:
    data = json.load(f)

sessions = data.get('sessions', [])

if not sessions:
    print("No sessions tracked yet.")
    exit(0)

print("=" * 80)
print("📈 CONVERSATION METRICS - Self-Improvement System")
print("=" * 80)
print()

# Calculate statistics
total_sessions = len(sessions)
total_turns = [s.get('total_turns', 0) for s in sessions if s.get('total_turns', 0) > 0]
total_lines = [s.get('total_lines', 0) for s in sessions if s.get('total_lines', 0) > 0]

if total_turns:
    print("📊 Conversation Statistics:")
    print(f"   Total sessions analyzed: {total_sessions}")
    print(f"   Average turns per conversation: {mean(total_turns):.1f}")
    print(f"   Median turns per conversation: {median(total_turns):.1f}")
    print(f"   Shortest conversation: {min(total_turns)} turns")
    print(f"   Longest conversation: {max(total_turns)} turns")
    print()

if total_lines:
    print("📝 Volume Statistics:")
    print(f"   Average lines per conversation: {mean(total_lines):.1f}")
    print(f"   Median lines per conversation: {median(total_lines):.1f}")
    print()

# Recent sessions
print("🕐 Recent Sessions:")
for session in sessions[-10:]:
    timestamp = session.get('timestamp', 'N/A')
    turns = session.get('total_turns', 0)
    print(f"   {timestamp}: {turns} turns")

print()
print("=" * 80)
EOF
