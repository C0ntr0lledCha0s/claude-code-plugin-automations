#!/usr/bin/env bash
#
# Automated Conversation Analysis Script
# Triggers on Stop event (when conversation ends)
# Analyzes conversation for quality, patterns, issues, and learning opportunities
#

set -euo pipefail

# Configuration
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-${HOME}/.claude/plugins/self-improvement}"
LOG_DIR="${HOME}/.claude/self-improvement"
CONVERSATION_LOG="${LOG_DIR}/conversations.jsonl"
PATTERNS_DB="${LOG_DIR}/patterns.json"
METRICS_DB="${LOG_DIR}/metrics.json"
LEARNINGS_DB="${LOG_DIR}/learnings.json"
ANALYSIS_LOG="${LOG_DIR}/analysis.log"

# Create directories if they don't exist
mkdir -p "${LOG_DIR}"

# Timestamp for this analysis
TIMESTAMP=$(date -Iseconds)
SESSION_ID="${CLAUDE_SESSION_ID:-$(date +%s)}"

# Initialize databases if they don't exist
if [[ ! -f "${PATTERNS_DB}" ]]; then
    echo '{"patterns": []}' > "${PATTERNS_DB}"
fi

if [[ ! -f "${METRICS_DB}" ]]; then
    echo '{"sessions": []}' > "${METRICS_DB}"
fi

if [[ ! -f "${LEARNINGS_DB}" ]]; then
    echo '{"learnings": []}' > "${LEARNINGS_DB}"
fi

# Function to log analysis results
log_analysis() {
    echo "[${TIMESTAMP}] $*" >> "${ANALYSIS_LOG}"
}

log_analysis "=== Starting conversation analysis for session ${SESSION_ID} ==="

# Function to analyze conversation transcript
analyze_transcript() {
    local transcript_file="$1"

    if [[ ! -f "${transcript_file}" ]]; then
        log_analysis "No transcript file found, skipping analysis"
        return 0
    fi

    log_analysis "Analyzing transcript: ${transcript_file}"

    # Extract conversation statistics
    local total_turns=$(grep -c "User:\|Assistant:" "${transcript_file}" 2>/dev/null || echo "0")
    local user_turns=$(grep -c "^User:" "${transcript_file}" 2>/dev/null || echo "0")
    local assistant_turns=$(grep -c "^Assistant:" "${transcript_file}" 2>/dev/null || echo "0")
    local total_lines=$(wc -l < "${transcript_file}")

    log_analysis "Statistics: ${total_turns} total turns, ${user_turns} user, ${assistant_turns} assistant, ${total_lines} lines"

    # Analyze for keywords and patterns
    analyze_keywords "${transcript_file}"
    analyze_code_quality "${transcript_file}"
    analyze_errors "${transcript_file}"
    analyze_security "${transcript_file}"
    analyze_sentiment "${transcript_file}"

    # Store metrics
    store_session_metrics "${total_turns}" "${user_turns}" "${assistant_turns}" "${total_lines}"
}

# Analyze for important keywords
analyze_keywords() {
    local file="$1"

    log_analysis "--- Keyword Analysis ---"

    # Critical keywords
    local bug_count=$(grep -ci "bug\|error\|issue\|problem\|wrong\|fail" "${file}" 2>/dev/null || echo "0")
    local security_count=$(grep -ci "security\|vulnerability\|injection\|xss\|auth\|password" "${file}" 2>/dev/null || echo "0")
    local quality_count=$(grep -ci "quality\|review\|improve\|optimize\|refactor" "${file}" 2>/dev/null || echo "0")
    local help_count=$(grep -ci "help\|how to\|how do\|can you\|please" "${file}" 2>/dev/null || echo "0")

    log_analysis "Keywords: bugs=${bug_count}, security=${security_count}, quality=${quality_count}, help_requests=${help_count}"

    # Check for repeated issues
    if [[ ${bug_count} -gt 5 ]]; then
        track_pattern "high_bug_discussion" "Conversation had ${bug_count} bug-related mentions" "important"
    fi

    if [[ ${security_count} -gt 3 ]]; then
        track_pattern "security_focus" "Conversation had ${security_count} security-related mentions" "important"
    fi
}

# Analyze code quality indicators
analyze_code_quality() {
    local file="$1"

    log_analysis "--- Code Quality Analysis ---"

    # Look for code blocks
    local code_blocks=$(grep -c '```' "${file}" 2>/dev/null || echo "0")
    code_blocks=$((code_blocks / 2))  # Divide by 2 since each block has opening and closing

    # Quality indicators
    local test_mentions=$(grep -ci "test\|spec\|unittest\|pytest\|jest" "${file}" 2>/dev/null || echo "0")
    local validation_mentions=$(grep -ci "validat\|sanitiz\|check\|verify" "${file}" 2>/dev/null || echo "0")
    local error_handling=$(grep -ci "try\|catch\|except\|error handling" "${file}" 2>/dev/null || echo "0")

    log_analysis "Code Quality: ${code_blocks} code blocks, tests=${test_mentions}, validation=${validation_mentions}, error_handling=${error_handling}"

    # Track patterns
    if [[ ${code_blocks} -gt 0 && ${test_mentions} -eq 0 ]]; then
        track_pattern "missing_tests" "Code provided but no tests mentioned" "important"
    fi

    if [[ ${code_blocks} -gt 0 && ${validation_mentions} -eq 0 ]]; then
        track_pattern "missing_validation" "Code provided but no input validation mentioned" "important"
    fi
}

# Analyze for errors and issues
analyze_errors() {
    local file="$1"

    log_analysis "--- Error Analysis ---"

    # Error indicators
    local syntax_errors=$(grep -ci "syntax error\|syntaxerror\|parse error" "${file}" 2>/dev/null || echo "0")
    local runtime_errors=$(grep -ci "runtime error\|exception\|traceback\|stack trace" "${file}" 2>/dev/null || echo "0")
    local logic_errors=$(grep -ci "logic error\|incorrect\|doesn't work\|not working" "${file}" 2>/dev/null || echo "0")

    log_analysis "Errors: syntax=${syntax_errors}, runtime=${runtime_errors}, logic=${logic_errors}"

    if [[ $((syntax_errors + runtime_errors + logic_errors)) -gt 3 ]]; then
        track_pattern "high_error_rate" "Multiple errors encountered in conversation" "critical"
    fi
}

# Analyze security considerations
analyze_security() {
    local file="$1"

    log_analysis "--- Security Analysis ---"

    # Security issue indicators
    local sql_injection=$(grep -ci "sql injection\|parameterized query\|prepared statement" "${file}" 2>/dev/null || echo "0")
    local xss=$(grep -ci "xss\|cross-site scripting\|sanitize.*html\|escape.*html" "${file}" 2>/dev/null || echo "0")
    local auth_issues=$(grep -ci "authentication\|authorization\|access control\|permission" "${file}" 2>/dev/null || echo "0")
    local secret_exposure=$(grep -ci "api key\|password\|secret\|credential\|token" "${file}" 2>/dev/null || echo "0")

    log_analysis "Security: sql_injection=${sql_injection}, xss=${xss}, auth=${auth_issues}, secrets=${secret_exposure}"

    # Track security patterns
    if [[ ${sql_injection} -gt 0 ]]; then
        track_learning "sql_injection_discussed" "SQL injection topic came up - ensure parameterized queries used"
    fi

    if [[ ${xss} -gt 0 ]]; then
        track_learning "xss_discussed" "XSS topic came up - ensure proper input sanitization"
    fi
}

# Analyze sentiment and user satisfaction
analyze_sentiment() {
    local file="$1"

    log_analysis "--- Sentiment Analysis ---"

    # Positive indicators
    local positive=$(grep -ci "thank\|thanks\|great\|perfect\|excellent\|good\|helpful" "${file}" 2>/dev/null || echo "0")

    # Negative indicators
    local negative=$(grep -ci "wrong\|incorrect\|doesn't work\|not working\|confused\|unclear" "${file}" 2>/dev/null || echo "0")

    # Confusion indicators
    local confusion=$(grep -ci "what\?\|how\?\|why\?\|I don't understand\|unclear\|confusing" "${file}" 2>/dev/null || echo "0")

    log_analysis "Sentiment: positive=${positive}, negative=${negative}, confusion=${confusion}"

    # Calculate sentiment score
    local sentiment_score=$((positive - negative))

    if [[ ${sentiment_score} -lt -3 ]]; then
        track_pattern "negative_user_experience" "User expressed frustration or confusion" "critical"
    fi

    if [[ ${confusion} -gt 5 ]]; then
        track_pattern "unclear_communication" "User asked many clarifying questions" "important"
    fi
}

# Track a pattern in the patterns database
track_pattern() {
    local pattern_type="$1"
    local description="$2"
    local severity="${3:-minor}"

    log_analysis "PATTERN DETECTED: [${severity}] ${pattern_type}: ${description}"

    # Update patterns database
    python3 - <<EOF
import json
import sys
from datetime import datetime

patterns_file = "${PATTERNS_DB}"

try:
    with open(patterns_file, 'r') as f:
        data = json.load(f)
except:
    data = {"patterns": []}

# Find existing pattern or create new
pattern_found = False
for pattern in data['patterns']:
    if pattern['type'] == "${pattern_type}":
        pattern['count'] = pattern.get('count', 0) + 1
        pattern['last_seen'] = "${TIMESTAMP}"
        pattern['severity'] = "${severity}"
        pattern_found = True
        break

if not pattern_found:
    data['patterns'].append({
        'type': "${pattern_type}",
        'description': "${description}",
        'severity': "${severity}",
        'count': 1,
        'first_seen': "${TIMESTAMP}",
        'last_seen': "${TIMESTAMP}"
    })

with open(patterns_file, 'w') as f:
    json.dump(data, f, indent=2)

print(f"Pattern tracked: ${pattern_type}")
EOF
}

# Track a learning point
track_learning() {
    local learning_key="$1"
    local learning_text="$2"

    log_analysis "LEARNING: ${learning_key}: ${learning_text}"

    python3 - <<EOF
import json
from datetime import datetime

learnings_file = "${LEARNINGS_DB}"

try:
    with open(learnings_file, 'r') as f:
        data = json.load(f)
except:
    data = {"learnings": []}

# Check if learning already exists
learning_found = False
for learning in data['learnings']:
    if learning['key'] == "${learning_key}":
        learning['reinforced_count'] = learning.get('reinforced_count', 0) + 1
        learning['last_reinforced'] = "${TIMESTAMP}"
        learning_found = True
        break

if not learning_found:
    data['learnings'].append({
        'key': "${learning_key}",
        'text': "${learning_text}",
        'learned_at': "${TIMESTAMP}",
        'reinforced_count': 0
    })

with open(learnings_file, 'w') as f:
    json.dump(data, f, indent=2)

print(f"Learning tracked: ${learning_key}")
EOF
}

# Store session metrics
store_session_metrics() {
    local total_turns="$1"
    local user_turns="$2"
    local assistant_turns="$3"
    local total_lines="$4"

    python3 - <<EOF
import json

metrics_file = "${METRICS_DB}"

try:
    with open(metrics_file, 'r') as f:
        data = json.load(f)
except:
    data = {"sessions": []}

data['sessions'].append({
    'session_id': "${SESSION_ID}",
    'timestamp': "${TIMESTAMP}",
    'total_turns': ${total_turns},
    'user_turns': ${user_turns},
    'assistant_turns': ${assistant_turns},
    'total_lines': ${total_lines}
})

# Keep only last 100 sessions
if len(data['sessions']) > 100:
    data['sessions'] = data['sessions'][-100:]

with open(metrics_file, 'w') as f:
    json.dump(data, f, indent=2)

print("Session metrics stored")
EOF
}

# Generate summary report
generate_summary() {
    log_analysis "--- Generating Summary ---"

    python3 - <<EOF
import json
from collections import Counter

print("\n=== Self-Improvement Summary ===\n")

# Load patterns
try:
    with open("${PATTERNS_DB}", 'r') as f:
        patterns_data = json.load(f)

    if patterns_data.get('patterns'):
        print("🔍 Recurring Patterns Detected:")
        for pattern in sorted(patterns_data['patterns'], key=lambda x: x.get('count', 0), reverse=True)[:5]:
            severity_emoji = {'critical': '🔴', 'important': '🟡', 'minor': '🟢'}.get(pattern.get('severity'), '⚪')
            print(f"  {severity_emoji} {pattern['type']}: {pattern['description']} (seen {pattern.get('count', 0)} times)")
        print()
except:
    pass

# Load learnings
try:
    with open("${LEARNINGS_DB}", 'r') as f:
        learnings_data = json.load(f)

    if learnings_data.get('learnings'):
        print("📚 Active Learning Points:")
        for learning in learnings_data['learnings'][-5:]:
            reinforced = learning.get('reinforced_count', 0)
            status = f"(reinforced {reinforced}x)" if reinforced > 0 else "(new)"
            print(f"  • {learning['text']} {status}")
        print()
except:
    pass

# Load metrics
try:
    with open("${METRICS_DB}", 'r') as f:
        metrics_data = json.load(f)

    if metrics_data.get('sessions'):
        recent_sessions = metrics_data['sessions'][-10:]
        avg_turns = sum(s.get('total_turns', 0) for s in recent_sessions) / len(recent_sessions)
        print(f"📊 Recent Activity:")
        print(f"  • Average conversation length: {avg_turns:.1f} turns")
        print(f"  • Sessions analyzed: {len(metrics_data['sessions'])}")
        print()
except:
    pass

print("✓ Analysis complete. Data stored for continuous improvement.\n")
EOF
}

# Main execution
main() {
    # Try to find conversation transcript
    # This path may vary depending on Claude Code's transcript storage
    local transcript_path="${CLAUDE_TRANSCRIPT:-}"

    if [[ -z "${transcript_path}" ]]; then
        # Try common locations
        transcript_path="${HOME}/.claude/transcripts/current.txt"
    fi

    if [[ -f "${transcript_path}" ]]; then
        analyze_transcript "${transcript_path}"
    else
        log_analysis "Transcript not found at ${transcript_path}, performing lightweight analysis"
        # Even without transcript, we can track that a session occurred
        store_session_metrics 0 0 0 0
    fi

    # Generate summary
    generate_summary

    log_analysis "=== Conversation analysis complete ==="

    # Return success
    echo '{"decision": "allow", "reason": "Conversation analyzed for continuous improvement"}'
    exit 0
}

# Run main function
main "$@"
