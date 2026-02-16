#!/usr/bin/env bash
#
# Session End: Project Planning File Check
# Checks if project planning files were modified during the session
# and suggests coordination actions if needed.
#

set -uo pipefail

# Check for git
if ! command -v git &> /dev/null; then
    echo '{"decision": "approve", "suppressOutput": true}'
    exit 0
fi

# Check if we're in a git repo
if ! git rev-parse --is-inside-work-tree &> /dev/null 2>&1; then
    echo '{"decision": "approve", "suppressOutput": true}'
    exit 0
fi

# Get files modified during this session
PLANNING_PATTERNS="sprint.*\.md|roadmap.*\.md|backlog.*\.md|\.claude-project/(sprints|roadmaps|projects)"

CHANGED_FILES=$(git diff --name-only HEAD 2>/dev/null || true)
STAGED_FILES=$(git diff --cached --name-only 2>/dev/null || true)
ALL_CHANGED=$(printf '%s\n%s' "$CHANGED_FILES" "$STAGED_FILES" | sort -u | grep -v '^$' || true)

PLANNING_COUNT=$(echo "$ALL_CHANGED" | grep -E "$PLANNING_PATTERNS" | grep -c '[^[:space:]]' 2>/dev/null || echo 0)

# Only suggest coordination if planning files were modified
if [[ "$PLANNING_COUNT" -ge 1 ]]; then
    echo '{"decision": "approve", "systemMessage": "Project planning files were modified. Consider running /project-manager:project-status to check coordination needs."}'
else
    echo '{"decision": "approve", "suppressOutput": true}'
fi

exit 0
