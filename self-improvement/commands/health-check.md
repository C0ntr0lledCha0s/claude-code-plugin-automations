---
description: Diagnose self-improvement plugin health and configuration issues
allowed-tools: Bash, Read
model: claude-haiku-4-5
---

# Health Check

Run comprehensive diagnostics on the self-improvement plugin to identify configuration issues, validate data integrity, and verify automation is working correctly.

> **ℹ️ Command Type**: This command runs actual diagnostic checks using bash scripts.
> It provides actionable troubleshooting information for plugin issues.

## What This Checks

1. **Database Files**: Existence and JSON validity
2. **Transcript Access**: Whether automated analysis can find conversation files
3. **Recent Activity**: Last analysis execution and results
4. **Data Statistics**: Patterns, learnings, and metrics counts
5. **Configuration**: Environment variables and paths

## Running the Health Check

Execute the diagnostic checks:

```bash
# Check database files
LOG_DIR="${HOME}/.claude/self-improvement"

echo "🏥 Self-Improvement Plugin Health Check"
echo "========================================"
echo ""

# Check database files
echo "📊 Database Files:"
for db in patterns.json learnings.json metrics.json; do
    if [[ -f "${LOG_DIR}/${db}" ]]; then
        echo "  ✅ ${db} exists"
        # Validate JSON
        if jq empty "${LOG_DIR}/${db}" 2>/dev/null; then
            echo "     ✅ Valid JSON structure"
            # Show record counts
            case "${db}" in
                patterns.json)
                    count=$(jq '.patterns | length' "${LOG_DIR}/${db}" 2>/dev/null || echo "0")
                    echo "     📈 ${count} patterns tracked"
                    ;;
                learnings.json)
                    count=$(jq '.learnings | length' "${LOG_DIR}/${db}" 2>/dev/null || echo "0")
                    echo "     📚 ${count} learnings stored"
                    ;;
                metrics.json)
                    count=$(jq '.sessions | length' "${LOG_DIR}/${db}" 2>/dev/null || echo "0")
                    echo "     💼 ${count} sessions analyzed"
                    ;;
            esac
        else
            echo "     ❌ CORRUPTED JSON - needs repair"
        fi
    else
        echo "  ⚠️  ${db} not found (not created yet)"
    fi
done

echo ""
echo "📄 Transcript Accessibility:"

# Try to find transcript
transcript_found=false
possible_paths=(
    "${CLAUDE_TRANSCRIPT:-}"
    "${CLAUDE_CONVERSATION_FILE:-}"
    "${HOME}/.claude/transcripts/current.txt"
    "${HOME}/.claude/transcripts/latest.txt"
    "${HOME}/.claude/conversations/current.txt"
    "${HOME}/.claude/conversations/latest.txt"
)

for path in "${possible_paths[@]}"; do
    if [[ -n "${path}" && -f "${path}" ]]; then
        echo "  ✅ Transcript found: ${path}"
        transcript_found=true
        break
    fi
done

if [[ "${transcript_found}" == false ]]; then
    echo "  ❌ Transcript not accessible (automation won't work)"
    echo "     Searched locations:"
    for path in "${possible_paths[@]}"; do
        if [[ -n "${path}" ]]; then
            echo "     - ${path}"
        fi
    done
fi

echo ""
echo "🪝 Hook Execution:"

# Check analysis log
if [[ -f "${LOG_DIR}/analysis.log" ]]; then
    echo "  ✅ Analysis log exists: ${LOG_DIR}/analysis.log"
    echo ""
    echo "  📝 Last 5 analysis runs:"
    tail -n 15 "${LOG_DIR}/analysis.log" | grep -E "\[.*\] ===" | tail -n 5 || echo "     No analysis runs found"
    echo ""
    echo "  🔍 Recent activity (last 10 lines):"
    tail -n 10 "${LOG_DIR}/analysis.log" | sed 's/^/     /'
else
    echo "  ⚠️  No analysis log found"
    echo "     Either hooks haven't run yet, or there's a configuration issue"
fi

echo ""
echo "⚙️  Configuration:"
echo "  CLAUDE_PLUGIN_ROOT: ${CLAUDE_PLUGIN_ROOT:-not set}"
echo "  CLAUDE_TRANSCRIPT: ${CLAUDE_TRANSCRIPT:-not set}"
echo "  CLAUDE_CONVERSATION_FILE: ${CLAUDE_CONVERSATION_FILE:-not set}"
echo "  LOG_DIR: ${LOG_DIR}"

echo ""
echo "📊 Summary Statistics:"

if [[ -f "${LOG_DIR}/patterns.json" ]]; then
    echo ""
    echo "  🔍 Top Patterns:"
    jq -r '.patterns | sort_by(-.count) | .[:5] | .[] | "     \(.severity | ascii_upcase): \(.type) (seen \(.count)x)"' "${LOG_DIR}/patterns.json" 2>/dev/null || echo "     No patterns data"
fi

if [[ -f "${LOG_DIR}/learnings.json" ]]; then
    echo ""
    echo "  📚 Recent Learnings:"
    jq -r '.learnings | .[-5:] | .[] | "     • \(.text)"' "${LOG_DIR}/learnings.json" 2>/dev/null || echo "     No learnings data"
fi

if [[ -f "${LOG_DIR}/metrics.json" ]]; then
    echo ""
    echo "  📈 Metrics:"
    total=$(jq '.sessions | length' "${LOG_DIR}/metrics.json" 2>/dev/null || echo "0")
    avg=$(jq '[.sessions[].total_turns] | add / length | floor' "${LOG_DIR}/metrics.json" 2>/dev/null || echo "0")
    echo "     Total sessions: ${total}"
    echo "     Average conversation length: ${avg} turns"
fi

echo ""
echo "✅ Health check complete!"
echo ""
echo "💡 Troubleshooting Tips:"
echo "  • If transcript not accessible, set CLAUDE_TRANSCRIPT environment variable"
echo "  • If databases corrupted, delete and they'll be recreated"
echo "  • If no analysis runs, check that hooks are properly installed"
echo "  • See: ${LOG_DIR}/analysis.log for detailed logs"
```

## Interpreting Results

### ✅ Healthy Status
All checks pass:
- Database files exist and contain valid JSON
- Transcript is accessible
- Recent analysis runs visible in logs
- Patterns and learnings being tracked

**Action**: No action needed. Plugin is working correctly.

### ⚠️ Warning Signs
Some issues detected:
- Transcript not accessible → Automation won't work
- No recent analysis runs → Hooks may not be executing
- Databases not created yet → Plugin hasn't run

**Action**: Follow troubleshooting tips in output.

### ❌ Critical Issues
Major problems:
- Corrupted JSON databases
- Cannot locate any database files
- Errors in analysis log

**Action**: See repair instructions below.

## Common Issues and Fixes

### Issue: Transcript Not Accessible

**Symptoms**:
```
❌ Transcript not accessible (automation won't work)
```

**Fix Options**:
1. **Set environment variable**:
   ```bash
   export CLAUDE_TRANSCRIPT=/path/to/transcript
   ```

2. **Disable automated analysis** if transcripts unavailable:
   - Remove or disable the Stop hook in `hooks/hooks.json`

3. **Manual analysis only**:
   - Use `/quality-check` and `/review-my-work` commands manually

### Issue: Corrupted JSON Database

**Symptoms**:
```
❌ CORRUPTED JSON - needs repair
```

**Fix**:
```bash
# Backup corrupted file
mv ~/.claude/self-improvement/patterns.json ~/.claude/self-improvement/patterns.json.backup

# File will be recreated on next analysis
# Or manually recreate:
echo '{"patterns": []}' > ~/.claude/self-improvement/patterns.json
```

### Issue: No Analysis Runs

**Symptoms**:
```
⚠️ No analysis log found
```

**Possible Causes**:
1. Hooks not installed correctly
2. Hook execution failing silently
3. Plugin never activated

**Fix**:
```bash
# Check if hooks exist
ls ~/.claude/plugins/self-improvement/hooks/hooks.json

# Check hook syntax
bash -n ~/.claude/plugins/self-improvement/hooks/scripts/analyze-conversation.sh

# Manually trigger analysis (for testing)
bash ~/.claude/plugins/self-improvement/hooks/scripts/analyze-conversation.sh
```

### Issue: Low Data Counts

**Symptoms**:
```
📈 0 patterns tracked
📚 0 learnings stored
```

**Explanation**: This is normal if:
- Plugin just installed
- Not many conversations yet
- Conversations don't trigger pattern thresholds

**Not a problem**: Data will accumulate over time.

## Repair Procedures

### Reset All Data
```bash
# CAUTION: This deletes all tracked patterns, learnings, and metrics
cd ~/.claude/self-improvement

# Backup first
mkdir -p backups
cp patterns.json learnings.json metrics.json backups/ 2>/dev/null || true

# Reset databases
echo '{"patterns": []}' > patterns.json
echo '{"learnings": []}' > learnings.json
echo '{"sessions": []}' > metrics.json

echo "Databases reset. Fresh start!"
```

### View Raw Database Contents
```bash
# Pretty-print patterns
jq '.' ~/.claude/self-improvement/patterns.json

# Pretty-print learnings
jq '.' ~/.claude/self-improvement/learnings.json

# Pretty-print metrics
jq '.' ~/.claude/self-improvement/metrics.json
```

## When to Run Health Check

Run this command when:
- First installing the plugin
- Troubleshooting automation issues
- Verifying fixes after configuration changes
- Suspecting data corruption
- Before reporting bugs

## Related Commands

- `/self-improvement:show-patterns` - View tracked patterns
- `/self-improvement:show-learnings` - View learning points
- `/self-improvement:show-metrics` - View conversation metrics

---

**Diagnostic tool for ensuring the self-improvement plugin is working correctly** 🏥
