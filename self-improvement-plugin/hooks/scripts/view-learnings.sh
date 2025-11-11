#!/usr/bin/env bash
#
# View Learnings Script
# Display all tracked learning points
#

set -euo pipefail

LOG_DIR="${HOME}/.claude/self-improvement"
LEARNINGS_DB="${LOG_DIR}/learnings.json"

if [[ ! -f "${LEARNINGS_DB}" ]]; then
    echo "No learnings tracked yet. The system will start tracking after conversations end."
    exit 0
fi

python3 - <<'EOF'
import json

learnings_file = "${LEARNINGS_DB}"

with open(learnings_file, 'r') as f:
    data = json.load(f)

learnings = data.get('learnings', [])

if not learnings:
    print("No learnings tracked yet.")
    exit(0)

# Sort by reinforcement count
sorted_learnings = sorted(
    learnings,
    key=lambda x: x.get('reinforced_count', 0),
    reverse=True
)

print("=" * 80)
print("📚 TRACKED LEARNINGS - Self-Improvement System")
print("=" * 80)
print()

for learning in sorted_learnings:
    reinforced = learning.get('reinforced_count', 0)
    status_emoji = "🔥" if reinforced >= 3 else "⭐" if reinforced >= 1 else "💡"

    print(f"{status_emoji} {learning['key']}")
    print(f"   {learning['text']}")
    print(f"   Learned: {learning.get('learned_at', 'N/A')}")

    if reinforced > 0:
        print(f"   Reinforced: {reinforced} times (last: {learning.get('last_reinforced', 'N/A')})")
    print()

print("=" * 80)
print(f"Total learnings: {len(learnings)}")
print(f"Highly reinforced (3+): {sum(1 for l in learnings if l.get('reinforced_count', 0) >= 3)}")
print(f"Reinforced (1+): {sum(1 for l in learnings if l.get('reinforced_count', 0) >= 1)}")
print(f"New (0): {sum(1 for l in learnings if l.get('reinforced_count', 0) == 0)}")
print("=" * 80)
EOF
