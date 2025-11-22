#!/bin/bash
# Check if GitHub workflow environment is initialized

ENV_FILE=".claude/github-workflows/env.json"
MAX_AGE_HOURS=24

if [ ! -f "$ENV_FILE" ]; then
    echo "Tip: Run /github-workflows:init to set up your workflow environment with project context, issue tracking, and environment variables for this session."
    exit 0
fi

# Check file age (in seconds)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    FILE_AGE=$(( $(date +%s) - $(stat -f %m "$ENV_FILE") ))
else
    # Linux
    FILE_AGE=$(( $(date +%s) - $(stat -c %Y "$ENV_FILE") ))
fi

MAX_AGE_SECONDS=$((MAX_AGE_HOURS * 3600))

if [ $FILE_AGE -gt $MAX_AGE_SECONDS ]; then
    echo "Tip: Run /github-workflows:init to refresh your workflow environment (last initialized $(($FILE_AGE / 3600)) hours ago)."
fi
