#!/usr/bin/env bash
#
# Session End: Best Practices Review Suggestion
# Checks if substantial source code was written during the session
# and suggests a best practices review if warranted.
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

# Get files modified during this session (unstaged + staged changes)
# Filter to source code files only
SOURCE_EXTENSIONS="js|ts|jsx|tsx|py|go|rs|java|rb|php|c|cpp|h|hpp|cs|swift|kt"
CHANGED_FILES=$(git diff --name-only HEAD 2>/dev/null | grep -iE "\.(${SOURCE_EXTENSIONS})$" || true)
STAGED_FILES=$(git diff --cached --name-only 2>/dev/null | grep -iE "\.(${SOURCE_EXTENSIONS})$" || true)
ALL_CHANGED=$(printf '%s\n%s' "$CHANGED_FILES" "$STAGED_FILES" | sort -u | grep -v '^$' || true)

FILE_COUNT=$(echo "$ALL_CHANGED" | grep -c '[^[:space:]]' 2>/dev/null || echo 0)

# Only suggest review if 3+ source files were modified
if [[ "$FILE_COUNT" -ge 3 ]]; then
    echo '{"decision": "approve", "systemMessage": "Session summary: '"$FILE_COUNT"' source files were modified. Consider running /research-agent:best-practice for a review."}'
else
    echo '{"decision": "approve", "suppressOutput": true}'
fi

exit 0
