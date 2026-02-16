#!/usr/bin/env bash
#
# Session End: Documentation Update Suggestion
# Checks if source code files were modified without corresponding
# documentation updates, and suggests running docs tools.
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
SOURCE_EXTENSIONS="js|ts|jsx|tsx|py|go|rs|java|rb|php|c|cpp|h|hpp|cs|swift|kt"
DOC_EXTENSIONS="md|rst|txt|adoc"

CHANGED_FILES=$(git diff --name-only HEAD 2>/dev/null || true)
STAGED_FILES=$(git diff --cached --name-only 2>/dev/null || true)
ALL_CHANGED=$(printf '%s\n%s' "$CHANGED_FILES" "$STAGED_FILES" | sort -u | grep -v '^$' || true)

SOURCE_COUNT=$(echo "$ALL_CHANGED" | grep -iE "\.(${SOURCE_EXTENSIONS})$" | grep -c '[^[:space:]]' 2>/dev/null || echo 0)
DOC_COUNT=$(echo "$ALL_CHANGED" | grep -iE "\.(${DOC_EXTENSIONS})$" | grep -c '[^[:space:]]' 2>/dev/null || echo 0)

# Suggest docs update if source files changed but no docs were updated
if [[ "$SOURCE_COUNT" -ge 2 && "$DOC_COUNT" -eq 0 ]]; then
    echo '{"decision": "approve", "hookSpecificOutput": {"message": "'"$SOURCE_COUNT"' source files were modified without documentation updates. Consider running /documents-manager:docs-coverage to check."}}'
else
    echo '{"decision": "approve", "suppressOutput": true}'
fi

exit 0
