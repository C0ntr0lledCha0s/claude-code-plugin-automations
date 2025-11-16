#!/usr/bin/env bash
# Update project board when PR merges
# Called by post-merge hook

set -euo pipefail

PR_NUMBER="${1:-}"

if [ -z "$PR_NUMBER" ]; then
    echo "Usage: $0 <pr-number>"
    exit 1
fi

echo "Updating project board for merged PR #$PR_NUMBER..."

# Get linked issues from PR
LINKED_ISSUES=$(gh pr view "$PR_NUMBER" --json body -q '.body' | grep -oE '#[0-9]+' | tr -d '#' || echo "")

if [ -n "$LINKED_ISSUES" ]; then
    while read -r issue_num; do
        # Check if issue has "Closes #N" syntax (not just "Ref #N")
        if gh pr view "$PR_NUMBER" --json body -q '.body' | grep -qiE "(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+#${issue_num}"; then
            echo "Closing issue #$issue_num (linked to merged PR)"

            # Close the issue with a reference to the PR
            if gh issue close "$issue_num" --comment "Automatically closed by merged PR #$PR_NUMBER" 2>/dev/null; then
                echo "  ✓ Issue #$issue_num closed"
            else
                echo "  ⚠ Could not close issue #$issue_num (may already be closed or insufficient permissions)"
            fi
        else
            echo "Skipping issue #$issue_num (referenced but not closed by PR)"
        fi
    done <<< "$LINKED_ISSUES"

    echo "✓ Processed linked issues for merged PR"
else
    echo "No linked issues found"
fi
