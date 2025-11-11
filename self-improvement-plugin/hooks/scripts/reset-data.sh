#!/usr/bin/env bash
#
# Reset Data Script
# Clear all tracked patterns, learnings, and metrics
# Use with caution!
#

set -euo pipefail

LOG_DIR="${HOME}/.claude/self-improvement"

echo "⚠️  WARNING: This will delete ALL tracked self-improvement data!"
echo "   - Patterns database"
echo "   - Learnings database"
echo "   - Metrics database"
echo "   - Analysis logs"
echo ""
read -p "Are you sure you want to continue? (type 'yes' to confirm): " confirmation

if [[ "${confirmation}" != "yes" ]]; then
    echo "Cancelled. No data was deleted."
    exit 0
fi

# Backup before deleting
BACKUP_DIR="${LOG_DIR}/backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "${BACKUP_DIR}"

if [[ -d "${LOG_DIR}" ]]; then
    echo "Creating backup in ${BACKUP_DIR}..."
    cp -r "${LOG_DIR}"/*.json "${BACKUP_DIR}/" 2>/dev/null || true
    cp -r "${LOG_DIR}"/*.log "${BACKUP_DIR}/" 2>/dev/null || true
    cp -r "${LOG_DIR}"/*.jsonl "${BACKUP_DIR}/" 2>/dev/null || true
fi

# Reset databases
echo '{"patterns": []}' > "${LOG_DIR}/patterns.json"
echo '{"learnings": []}' > "${LOG_DIR}/learnings.json"
echo '{"sessions": []}' > "${LOG_DIR}/metrics.json"

# Clear logs
> "${LOG_DIR}/analysis.log"
> "${LOG_DIR}/conversations.jsonl"

echo "✓ All self-improvement data has been reset."
echo "✓ Backup saved to ${BACKUP_DIR}"
echo ""
echo "The system will start fresh with the next conversation."
