#!/usr/bin/env bash
# Save current workflow state
# Captures branch, commits, open PRs for session continuity

set -euo pipefail

STATE_FILE=".claude/workflow-state.json"

# Create .claude directory if it doesn't exist
mkdir -p "$(dirname "$STATE_FILE")"

# Initialize with default state in case of errors
DEFAULT_STATE='{
  "timestamp": "'$(date -Iseconds 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%S%z")'",
  "branch": "unknown",
  "commits": [],
  "open_prs": []
}'

# Function to safely write state
write_state() {
    local branch="${1:-unknown}"
    local commits_json="${2:-[]}"
    local prs_json="${3:-[]}"

    cat > "$STATE_FILE" <<EOF
{
  "timestamp": "$(date -Iseconds 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%S%z")",
  "branch": "$branch",
  "commits": $commits_json,
  "open_prs": $prs_json
}
EOF
}

# Get current branch
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")

# Get recent commits as JSON array (without jq dependency)
COMMITS_RAW=$(git log --oneline -5 2>/dev/null || echo "")
COMMITS_JSON="["
if [ -n "$COMMITS_RAW" ]; then
    first=true
    while IFS= read -r line; do
        if [ -n "$line" ]; then
            if [ "$first" = true ]; then
                first=false
            else
                COMMITS_JSON+=","
            fi
            # Escape quotes and backslashes in commit message
            escaped=$(echo "$line" | sed 's/\\/\\\\/g; s/"/\\"/g' 2>/dev/null || echo "$line")
            COMMITS_JSON+="\"$escaped\""
        fi
    done <<< "$COMMITS_RAW"
fi
COMMITS_JSON+="]"

# Get open PRs (if gh available)
if command -v gh &> /dev/null; then
    OPEN_PRS=$(gh pr list --json number,title --limit 5 2>/dev/null || echo "[]")
else
    OPEN_PRS="[]"
fi

# Save state - create file even if empty/default
write_state "$BRANCH" "$COMMITS_JSON" "$OPEN_PRS" || echo "$DEFAULT_STATE" > "$STATE_FILE"

echo "✓ Workflow state saved to $STATE_FILE"
