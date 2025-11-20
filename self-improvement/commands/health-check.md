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
echo "📄 Transcript Storage:"

# Check Claude Code's actual transcript storage location
PROJECTS_DIR="${HOME}/.claude/projects"

if [[ -d "${PROJECTS_DIR}" ]]; then
    echo "  ✅ Projects directory exists: ${PROJECTS_DIR}"

    # Count JSONL files
    jsonl_count=$(find "${PROJECTS_DIR}" -name "*.jsonl" 2>/dev/null | wc -l || echo "0")
    echo "  📁 Found ${jsonl_count} conversation transcript(s)"

    # Show most recent
    if [[ ${jsonl_count} -gt 0 ]]; then
        recent=$(find "${PROJECTS_DIR}" -name "*.jsonl" -type f -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -1 | cut -d' ' -f2- || true)
        if [[ -n "${recent}" ]]; then
            echo "  🕐 Most recent: ${recent}"
        fi
    fi

    echo ""
    echo "  ℹ️  Transcripts are provided via hook stdin payload (transcript_path field)"
    echo "     The SessionEnd hook receives the path automatically"
else
    echo "  ⚠️  Projects directory not found: ${PROJECTS_DIR}"
    echo "     This is normal if Claude Code hasn't been used yet"
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
echo "  LOG_DIR: ${LOG_DIR}"
echo "  PROJECTS_DIR: ${PROJECTS_DIR}"

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
echo "  • Transcripts are provided automatically via hook stdin payload"
echo "  • If databases corrupted, delete them and they'll be recreated"
echo "  • If no analysis runs, check SessionEnd hook is properly configured"
echo "  • Check ${LOG_DIR}/analyze-debug.log for detailed debugging info"
echo "  • See: ${LOG_DIR}/analysis.log for analysis history"
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

### Issue: No Analysis Runs After Conversation

**Symptoms**:
```
⚠️ No analysis log found
```

**Possible Causes**:
1. SessionEnd hook not configured
2. Hook script has errors
3. jq or python3 not available

**Fix Options**:
1. **Check hook configuration**:
   - Ensure `hooks/hooks.json` has `SessionEnd` event (not `Stop`)
   - Verify hook command path is correct

2. **Check dependencies**:
   ```bash
   which jq python3
   ```

3. **Check debug log for errors**:
   ```bash
   cat ~/.claude/self-improvement/analyze-debug.log
   ```

4. **Manual analysis only** (alternative):
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

### Issue: Transcript Not Found in Payload

**Symptoms**:
```
ERROR: No transcript_path in hook payload
```

**Possible Causes**:
1. Hook event type is wrong (should be `SessionEnd`)
2. Claude Code version doesn't support `transcript_path`

**Fix**:
```bash
# Check hooks.json configuration
cat ~/.claude/plugins/self-improvement/hooks/hooks.json | jq '.hooks'

# Verify SessionEnd event is configured (not Stop)
# The hook should receive transcript_path automatically

# Check debug log for received payload
cat ~/.claude/self-improvement/analyze-debug.log | grep "Received payload"
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
