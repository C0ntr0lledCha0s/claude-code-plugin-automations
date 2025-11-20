#!/usr/bin/env bash
#
# Automated Conversation Analysis Script
# Triggers on SessionEnd event (when conversation ends)
# Analyzes conversation for quality, patterns, issues, and learning opportunities
#
# Claude Code passes hook payload via stdin with transcript_path field

# Don't use set -e so we can capture errors without exiting
set -uo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$(dirname "$SCRIPT_DIR")")}"
LOG_DIR="${HOME}/.claude/self-improvement"
PATTERNS_DB="${LOG_DIR}/patterns.json"
METRICS_DB="${LOG_DIR}/metrics.json"
LEARNINGS_DB="${LOG_DIR}/learnings.json"
ANALYSIS_LOG="${LOG_DIR}/analysis.log"
DEBUG_LOG="${LOG_DIR}/analyze-debug.log"

# Create directories if they don't exist
mkdir -p "${LOG_DIR}"

# Debug logging function
debug_log() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo "timestamp-unavailable")
    echo "[$timestamp] $1" >> "$DEBUG_LOG" 2>/dev/null || true
}

# Clear previous debug log and start fresh
echo "=== Analyze Conversation Debug Log ===" > "$DEBUG_LOG" 2>/dev/null || true
debug_log "Script started"
debug_log "PID: $$"
debug_log "PWD: $(pwd)"
debug_log "PLUGIN_ROOT: ${PLUGIN_ROOT}"
debug_log "LOG_DIR: ${LOG_DIR}"
debug_log "SCRIPT_DIR: ${SCRIPT_DIR}"

# Cleanup trap for error handling
cleanup() {
    local exit_code=$?
    debug_log "Cleanup called with exit code: $exit_code"
    if [[ $exit_code -ne 0 ]]; then
        log_analysis "ERROR: Script failed with exit code $exit_code"
        debug_log "ERROR: Script failed with exit code $exit_code"
    fi
}
trap cleanup EXIT

# Timestamp for this analysis
TIMESTAMP=$(date -Iseconds 2>/dev/null || date '+%Y-%m-%dT%H:%M:%S')

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
    debug_log "ANALYSIS: $*"
}

# Check for Python availability (jq no longer required - using Python for JSON)
check_python() {
    if ! command -v python3 &> /dev/null; then
        debug_log "ERROR: python3 not found - required for analysis"
        echo '{"decision": "approve", "suppressOutput": true}'
        exit 0
    fi
}

# Parse JSON using Python (replaces jq dependency)
parse_json_field() {
    local json_str="$1"
    local field="$2"
    # Use tr -d '\r' to strip Windows CRLF from Python output
    python3 -c "
import json
import sys
try:
    data = json.loads('''$json_str''')
    value = data.get('$field', '')
    print(value if value else '')
except:
    print('')
" 2>/dev/null | tr -d '\r'
}

debug_log "Initializing databases..."
log_analysis "=== Starting conversation analysis ==="

# Function to analyze conversation transcript
analyze_transcript() {
    local transcript_file="$1"

    if [[ ! -f "${transcript_file}" ]]; then
        log_analysis "Transcript file not found: ${transcript_file}"
        return 1
    fi

    log_analysis "Analyzing transcript: ${transcript_file}"

    # Use parse-jsonl.py to convert JSONL to plain text
    local temp_text="${LOG_DIR}/temp_transcript.txt"
    local summary

    summary=$(python3 "${SCRIPT_DIR}/parse-jsonl.py" "${transcript_file}" "${temp_text}" 2>&1)

    if [[ ! -f "${temp_text}" ]]; then
        log_analysis "Failed to parse JSONL transcript"
        debug_log "parse-jsonl.py failed: ${summary}"
        return 1
    fi

    # Extract statistics from summary
    local total_turns=$(echo "${summary}" | jq -r '.total_turns // 0' 2>/dev/null || echo "0")
    local user_turns=$(echo "${summary}" | jq -r '.user_count // 0' 2>/dev/null || echo "0")
    local assistant_turns=$(echo "${summary}" | jq -r '.assistant_count // 0' 2>/dev/null || echo "0")
    local total_lines=$(wc -l < "${temp_text}" 2>/dev/null || echo "0")

    log_analysis "Statistics: ${total_turns} total turns, ${user_turns} user, ${assistant_turns} assistant, ${total_lines} lines"

    # Analyze the plain text version
    analyze_keywords "${temp_text}"
    analyze_code_quality "${temp_text}"
    analyze_errors "${temp_text}"
    analyze_security "${temp_text}"
    analyze_sentiment "${temp_text}"

    # Run real code analysis if available
    local code_analysis_result=""
    if [[ -f "${SCRIPT_DIR}/analyze-code-quality.py" ]]; then
        code_analysis_result=$(python3 "${SCRIPT_DIR}/analyze-code-quality.py" "${temp_text}" 2>/dev/null || echo "")
        if [[ -n "${code_analysis_result}" ]]; then
            process_code_analysis "${code_analysis_result}"
        fi
    fi

    # Check compliance with session-start advice
    check_compliance

    # Store metrics with quality indicators
    store_session_metrics "${total_turns}" "${user_turns}" "${assistant_turns}" "${total_lines}" "${code_analysis_result}"

    # Clean up temp file
    rm -f "${temp_text}"
}

# Check compliance with advice given at session start
check_compliance() {
    local tracker_script="${SCRIPT_DIR}/compliance-tracker.py"

    if [[ ! -f "${tracker_script}" ]]; then
        return 0
    fi

    # Get patterns found in this session
    local patterns_found
    patterns_found=$(python3 - "$PATTERNS_DB" "$TIMESTAMP" <<'EOF'
import json
import sys

patterns_file = sys.argv[1]
timestamp = sys.argv[2]

try:
    with open(patterns_file, 'r') as f:
        data = json.load(f)

    # Get patterns that were detected today (in this session)
    today = timestamp[:10]
    found = []
    for pattern in data.get('patterns', []):
        if pattern.get('last_seen', '').startswith(today):
            found.append(pattern['type'])

    print(json.dumps(found))
except Exception as e:
    print('[]')
EOF
)

    # Call compliance tracker to check
    local compliance_result
    compliance_result=$(python3 "${tracker_script}" check "${SESSION_ID}" "${patterns_found}" 2>/dev/null || echo '{}')

    # Log compliance result
    local compliance_rate
    compliance_rate=$(echo "${compliance_result}" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('compliance_rate', 'N/A'))" 2>/dev/null || echo "N/A")

    if [[ "${compliance_rate}" != "N/A" ]]; then
        log_analysis "COMPLIANCE: Session compliance rate: ${compliance_rate}"

        # Log details
        local advice_followed
        advice_followed=$(echo "${compliance_result}" | python3 -c "import json,sys; d=json.load(sys.stdin); print(','.join(d.get('advice_followed', [])))" 2>/dev/null || echo "")

        local advice_ignored
        advice_ignored=$(echo "${compliance_result}" | python3 -c "import json,sys; d=json.load(sys.stdin); print(','.join(d.get('advice_ignored', [])))" 2>/dev/null || echo "")

        if [[ -n "${advice_followed}" ]]; then
            log_analysis "COMPLIANCE: Advice followed: ${advice_followed}"
        fi

        if [[ -n "${advice_ignored}" ]]; then
            log_analysis "COMPLIANCE: Advice ignored: ${advice_ignored}"
        fi
    fi
}

# Analyze for important keywords
analyze_keywords() {
    local file="$1"

    debug_log "=== analyze_keywords started ==="
    log_analysis "--- Keyword Analysis ---"

    local bug_count=$(grep -ci "bug\|broken\|failing" "${file}" 2>/dev/null | tr -d '[:space:]' || echo "0")
    local error_count=$(grep -ci "error" "${file}" 2>/dev/null | tr -d '[:space:]' || echo "0")
    local security_count=$(grep -ci "injection\|xss\|csrf\|vulnerability\|security\|exploit\|attack\|malicious" "${file}" 2>/dev/null | tr -d '[:space:]' || echo "0")
    local quality_count=$(grep -ci "quality\|review\|improve\|optimize\|refactor" "${file}" 2>/dev/null | tr -d '[:space:]' || echo "0")
    local help_count=$(grep -ci "how do\|how to\|can you\|please help\|what is\|explain" "${file}" 2>/dev/null | tr -d '[:space:]' || echo "0")

    debug_log "Keyword counts: bugs=${bug_count}, errors=${error_count}, security=${security_count}, quality=${quality_count}, help=${help_count}"
    log_analysis "Keywords: bugs=${bug_count}, errors=${error_count}, security=${security_count}, quality=${quality_count}, help_requests=${help_count}"

    # Check for repeated issues with adjusted thresholds
    local total_issues=$((bug_count + error_count))
    if [[ ${total_issues} -gt 8 ]]; then
        track_pattern "high_bug_discussion" "Conversation had ${total_issues} bug/error mentions (bugs: ${bug_count}, errors: ${error_count})" "important"
    fi

    if [[ ${security_count} -gt 3 ]]; then
        track_pattern "security_focus" "Conversation had ${security_count} security-related mentions" "important"
    fi

    debug_log "=== analyze_keywords completed ==="
}

# Analyze code quality indicators
analyze_code_quality() {
    local file="$1"

    log_analysis "--- Code Quality Analysis ---"

    # Look for code blocks
    local code_blocks=$(grep -c '```' "${file}" 2>/dev/null | tr -d '[:space:]' || echo "0")
    code_blocks=$((code_blocks / 2))  # Divide by 2 since each block has opening and closing

    # Quality indicators
    local test_mentions=$(grep -ci "test\|spec\|unittest\|pytest\|jest" "${file}" 2>/dev/null | tr -d '[:space:]' || echo "0")
    local validation_mentions=$(grep -ci "validat\|sanitiz\|check\|verify" "${file}" 2>/dev/null | tr -d '[:space:]' || echo "0")
    local error_handling=$(grep -ci "try\|catch\|except\|error handling" "${file}" 2>/dev/null | tr -d '[:space:]' || echo "0")

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

    debug_log "=== analyze_errors started ==="
    log_analysis "--- Error Analysis ---"

    local syntax_errors=$(grep -ci "syntax error\|SyntaxError\|parse error\|ParseError\|unexpected token" "${file}" 2>/dev/null | tr -d '[:space:]' || echo "0")
    local runtime_errors=$(grep -ci "runtime error\|RuntimeError\|exception\|traceback\|stack trace" "${file}" 2>/dev/null | tr -d '[:space:]' || echo "0")
    local logic_errors=$(grep -ci "logic error\|incorrect\|not working" "${file}" 2>/dev/null | tr -d '[:space:]' || echo "0")

    debug_log "Error counts: syntax=${syntax_errors}, runtime=${runtime_errors}, logic=${logic_errors}"
    log_analysis "Errors: syntax=${syntax_errors}, runtime=${runtime_errors}, logic=${logic_errors}"

    local total_errors=$((syntax_errors + runtime_errors + logic_errors))
    if [[ ${total_errors} -gt 3 ]]; then
        track_pattern "high_error_rate" "Multiple errors encountered in conversation (${total_errors} total)" "critical"
    fi

    debug_log "=== analyze_errors completed ==="
}

# Process results from real code analysis
process_code_analysis() {
    local analysis_json="$1"

    log_analysis "--- Deep Code Analysis ---"

    # Parse the analysis results using Python
    python3 - "$analysis_json" "$TIMESTAMP" "$PATTERNS_DB" "$LEARNINGS_DB" <<'EOF'
import json
import sys

analysis_json = sys.argv[1]
timestamp = sys.argv[2]
patterns_file = sys.argv[3]
learnings_file = sys.argv[4]

try:
    analysis = json.loads(analysis_json)
except json.JSONDecodeError:
    sys.exit(0)

issues = analysis.get('issues', [])
patterns = analysis.get('patterns', [])
learnings = analysis.get('learnings', [])
metrics = analysis.get('metrics', {})

# Log summary
critical = sum(1 for i in issues if i.get('severity') == 'critical')
important = sum(1 for i in issues if i.get('severity') == 'important')
print(f"Code analysis: {critical} critical, {important} important issues in {metrics.get('total_code_blocks', 0)} blocks")

# Track patterns from analysis
if patterns:
    try:
        with open(patterns_file, 'r+') as f:
            try:
                data = json.load(f)
            except:
                data = {"patterns": []}

            for pattern in patterns:
                pattern_type = pattern.get('type', '')
                if not pattern_type:
                    continue

                # Find existing or create new
                existing = next((p for p in data['patterns'] if p['type'] == pattern_type), None)
                if existing:
                    existing['count'] = existing.get('count', 0) + 1
                    existing['last_seen'] = timestamp
                    existing['severity'] = pattern.get('severity', existing.get('severity', 'minor'))
                    existing['description'] = pattern.get('description', existing.get('description', ''))
                else:
                    data['patterns'].append({
                        'type': pattern_type,
                        'description': pattern.get('description', ''),
                        'severity': pattern.get('severity', 'minor'),
                        'count': 1,
                        'first_seen': timestamp,
                        'last_seen': timestamp
                    })

            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error tracking patterns: {e}", file=sys.stderr)

# Track learnings from analysis
if learnings:
    try:
        with open(learnings_file, 'r+') as f:
            try:
                data = json.load(f)
            except:
                data = {"learnings": []}

            for learning in learnings:
                key = learning.get('key', '')
                text = learning.get('text', '')
                if not key or not text:
                    continue

                # Find existing or create new
                existing = next((l for l in data['learnings'] if l['key'] == key), None)
                if existing:
                    existing['reinforced_count'] = existing.get('reinforced_count', 0) + 1
                    existing['last_reinforced'] = timestamp
                    existing['text'] = text
                else:
                    data['learnings'].append({
                        'key': key,
                        'text': text,
                        'learned_at': timestamp,
                        'reinforced_count': 0
                    })

            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error tracking learnings: {e}", file=sys.stderr)

EOF

    local output
    output=$(python3 - "$analysis_json" 2>&1)
    log_analysis "${output}"
}

# Analyze security considerations
analyze_security() {
    local file="$1"

    log_analysis "--- Security Analysis ---"

    # Security issue indicators
    local sql_injection=$(grep -ci "sql injection\|parameterized query\|prepared statement" "${file}" 2>/dev/null | tr -d '[:space:]' || echo "0")
    local xss=$(grep -ci "xss\|cross-site scripting\|sanitize.*html\|escape.*html" "${file}" 2>/dev/null | tr -d '[:space:]' || echo "0")
    local auth_issues=$(grep -ci "authentication\|authorization\|access control\|permission" "${file}" 2>/dev/null | tr -d '[:space:]' || echo "0")
    local secret_exposure=$(grep -ci "api key\|password\|secret\|credential\|token" "${file}" 2>/dev/null | tr -d '[:space:]' || echo "0")

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

    debug_log "=== analyze_sentiment started ==="
    log_analysis "--- Sentiment Analysis ---"

    local positive=$(grep -ci "thanks\|thank you\|great\|perfect\|excellent\|awesome\|helpful\|works great\|working well" "${file}" 2>/dev/null | tr -d '[:space:]' || echo "0")
    local negative=$(grep -ci "wrong\|incorrect\|not working\|confused\|unclear\|frustrated" "${file}" 2>/dev/null | tr -d '[:space:]' || echo "0")
    local confusion=$(grep -ci "don't understand\|unclear\|confused\|what do you mean\|can you explain\|not sure" "${file}" 2>/dev/null | tr -d '[:space:]' || echo "0")

    debug_log "Sentiment counts: positive=${positive}, negative=${negative}, confusion=${confusion}"
    log_analysis "Sentiment: positive=${positive}, negative=${negative}, confusion=${confusion}"

    # Calculate sentiment score
    local sentiment_score=$((positive - negative))

    if [[ ${sentiment_score} -lt -3 ]]; then
        track_pattern "negative_user_experience" "User expressed frustration or confusion (score: ${sentiment_score})" "critical"
    fi

    if [[ ${confusion} -gt 5 ]]; then
        track_pattern "unclear_communication" "User asked many clarifying questions (${confusion} instances)" "important"
    fi

    debug_log "=== analyze_sentiment completed ==="
}

# Track a pattern in the patterns database
track_pattern() {
    local pattern_type="$1"
    local description="$2"
    local severity="${3:-minor}"

    log_analysis "PATTERN DETECTED: [${severity}] ${pattern_type}: ${description}"

    # Update patterns database using Python
    python3 - "$pattern_type" "$description" "$severity" "$TIMESTAMP" "$PATTERNS_DB" <<'EOF'
import json
import sys

# Get arguments safely
pattern_type = sys.argv[1]
description = sys.argv[2]
severity = sys.argv[3]
timestamp = sys.argv[4]
patterns_file = sys.argv[5]

# Basic validation
if severity not in ['critical', 'important', 'minor']:
    severity = 'minor'

try:
    with open(patterns_file, 'r+') as f:
        try:
            f.seek(0)
            data = json.load(f)
        except (json.JSONDecodeError, ValueError):
            data = {"patterns": []}

        # Find existing pattern or create new
        pattern_found = False
        for pattern in data['patterns']:
            if pattern['type'] == pattern_type:
                pattern['count'] = pattern.get('count', 0) + 1
                pattern['last_seen'] = timestamp
                pattern['severity'] = severity
                pattern['description'] = description
                pattern_found = True
                break

        if not pattern_found:
            data['patterns'].append({
                'type': pattern_type,
                'description': description,
                'severity': severity,
                'count': 1,
                'first_seen': timestamp,
                'last_seen': timestamp
            })

        # Write atomically
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=2)

except Exception as e:
    print(f"Error tracking pattern: {e}", file=sys.stderr)
    sys.exit(1)
EOF
}

# Track a learning point
track_learning() {
    local learning_key="$1"
    local learning_text="$2"

    log_analysis "LEARNING: ${learning_key}: ${learning_text}"

    # Update learnings database using Python
    python3 - "$learning_key" "$learning_text" "$TIMESTAMP" "$LEARNINGS_DB" <<'EOF'
import json
import sys

# Get arguments safely
learning_key = sys.argv[1]
learning_text = sys.argv[2]
timestamp = sys.argv[3]
learnings_file = sys.argv[4]

try:
    with open(learnings_file, 'r+') as f:
        try:
            f.seek(0)
            data = json.load(f)
        except (json.JSONDecodeError, ValueError):
            data = {"learnings": []}

        # Check if learning already exists
        learning_found = False
        for learning in data['learnings']:
            if learning['key'] == learning_key:
                learning['reinforced_count'] = learning.get('reinforced_count', 0) + 1
                learning['last_reinforced'] = timestamp
                learning['text'] = learning_text
                learning_found = True
                break

        if not learning_found:
            data['learnings'].append({
                'key': learning_key,
                'text': learning_text,
                'learned_at': timestamp,
                'reinforced_count': 0
            })

        # Write atomically
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=2)

except Exception as e:
    print(f"Error tracking learning: {e}", file=sys.stderr)
    sys.exit(1)
EOF
}

# Store session metrics with quality indicators
store_session_metrics() {
    local total_turns="$1"
    local user_turns="$2"
    local assistant_turns="$3"
    local total_lines="$4"
    local code_analysis="${5:-}"

    # Update metrics database using Python with quality indicators
    python3 - "$SESSION_ID" "$TIMESTAMP" "$total_turns" "$user_turns" "$assistant_turns" "$total_lines" "$code_analysis" "$METRICS_DB" "$PATTERNS_DB" <<'EOF'
import json
import sys

# Get arguments safely
session_id = sys.argv[1]
timestamp = sys.argv[2]
total_turns = int(sys.argv[3])
user_turns = int(sys.argv[4])
assistant_turns = int(sys.argv[5])
total_lines = int(sys.argv[6])
code_analysis_json = sys.argv[7] if len(sys.argv) > 7 else ""
metrics_file = sys.argv[8]
patterns_file = sys.argv[9]

# Parse code analysis if available
quality_metrics = {
    "code_blocks_analyzed": 0,
    "critical_issues": 0,
    "important_issues": 0,
    "minor_issues": 0,
    "security_issues": 0,
    "quality_score": 100  # Start with perfect, deduct for issues
}

if code_analysis_json:
    try:
        analysis = json.loads(code_analysis_json)
        metrics = analysis.get('metrics', {})
        issues = analysis.get('issues', [])

        quality_metrics["code_blocks_analyzed"] = metrics.get('total_code_blocks', 0)

        for issue in issues:
            severity = issue.get('severity', 'minor')
            issue_type = issue.get('type', '')

            if severity == 'critical':
                quality_metrics["critical_issues"] += 1
                quality_metrics["quality_score"] -= 15
            elif severity == 'important':
                quality_metrics["important_issues"] += 1
                quality_metrics["quality_score"] -= 5
            else:
                quality_metrics["minor_issues"] += 1
                quality_metrics["quality_score"] -= 1

            # Track security-specific issues
            if any(sec in issue_type for sec in ['eval', 'injection', 'xss', 'secret', 'security']):
                quality_metrics["security_issues"] += 1

        # Ensure score doesn't go negative
        quality_metrics["quality_score"] = max(0, quality_metrics["quality_score"])
    except:
        pass

# Count patterns detected in this session
patterns_detected = 0
try:
    with open(patterns_file, 'r') as f:
        patterns_data = json.load(f)
        for pattern in patterns_data.get('patterns', []):
            if pattern.get('last_seen', '').startswith(timestamp[:10]):
                patterns_detected += 1
except:
    pass

try:
    with open(metrics_file, 'r+') as f:
        try:
            f.seek(0)
            data = json.load(f)
        except (json.JSONDecodeError, ValueError):
            data = {"sessions": []}

        # Store comprehensive metrics
        session_data = {
            'session_id': session_id,
            'timestamp': timestamp,
            # Activity metrics (less useful but kept for reference)
            'total_turns': total_turns,
            'user_turns': user_turns,
            'assistant_turns': assistant_turns,
            'total_lines': total_lines,
            # Quality metrics (meaningful indicators)
            'quality_score': quality_metrics["quality_score"],
            'code_blocks_analyzed': quality_metrics["code_blocks_analyzed"],
            'critical_issues': quality_metrics["critical_issues"],
            'important_issues': quality_metrics["important_issues"],
            'minor_issues': quality_metrics["minor_issues"],
            'security_issues': quality_metrics["security_issues"],
            'patterns_detected': patterns_detected
        }

        data['sessions'].append(session_data)

        # Keep only last 100 sessions
        if len(data['sessions']) > 100:
            data['sessions'] = data['sessions'][-100:]

        # Write atomically
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=2)

except Exception as e:
    print(f"Error storing metrics: {e}", file=sys.stderr)
    sys.exit(1)
EOF
}

# Main execution
main() {
    debug_log "=== main() started ==="

    # Check dependencies
    check_python

    # Read hook payload from stdin
    local payload
    payload=$(cat)

    debug_log "Received payload: ${payload}"

    if [[ -z "${payload}" ]]; then
        debug_log "ERROR: Empty payload received"
        log_analysis "ERROR: Empty payload received from hook"
        echo '{"decision": "approve", "suppressOutput": true}'
        exit 0
    fi

    # Extract fields from payload using Python (no jq dependency)
    local transcript_path
    transcript_path=$(parse_json_field "$payload" "transcript_path")

    SESSION_ID=$(parse_json_field "$payload" "session_id")

    if [[ -z "${SESSION_ID}" ]]; then
        SESSION_ID=$(date +%s)
    fi

    debug_log "TRANSCRIPT_PATH: ${transcript_path}"
    debug_log "SESSION_ID: ${SESSION_ID}"

    if [[ -z "${transcript_path}" ]]; then
        debug_log "ERROR: No transcript_path in payload"
        log_analysis "ERROR: No transcript_path in hook payload"
        echo '{"decision": "approve", "suppressOutput": true}'
        exit 0
    fi

    if [[ ! -f "${transcript_path}" ]]; then
        debug_log "ERROR: Transcript file not found: ${transcript_path}"
        log_analysis "ERROR: Transcript file not found: ${transcript_path}"
        echo '{"decision": "approve", "suppressOutput": true}'
        exit 0
    fi

    log_analysis "=== Starting conversation analysis for session ${SESSION_ID} ==="
    debug_log "Starting transcript analysis..."

    # Analyze the transcript
    if analyze_transcript "${transcript_path}"; then
        log_analysis "=== Conversation analysis complete ==="
        debug_log "Analysis complete successfully"
    else
        log_analysis "=== Conversation analysis failed ==="
        debug_log "Analysis failed"
    fi

    # Return success - allow session to end
    echo '{"decision": "approve", "suppressOutput": true}'

    debug_log "=== main() completed ==="
    exit 0
}

debug_log "About to call main()"

# Run main function
main "$@"
