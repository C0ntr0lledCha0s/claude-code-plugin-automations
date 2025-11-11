# Automated Conversation Analysis

**Automatic background analysis that runs after every conversation to track patterns, learnings, and quality trends.**

## Overview

The Self-Improvement Plugin v2.0 includes **fully automated conversation analysis** that runs in the background when conversations end. This system:

- ✅ **Runs automatically** - No user action required
- 📊 **Tracks patterns** - Identifies recurring issues
- 📚 **Records learnings** - Builds knowledge base
- 📈 **Measures trends** - Tracks improvement over time
- 🔄 **Loads context** - Applies learnings to new sessions

## How It Works

```
┌───────────────────────────────────────────────────────────┐
│  User finishes conversation                               │
├───────────────────────────────────────────────────────────┤
│  Stop Hook Triggers                                       │
│  └─> analyze-conversation.sh runs in background          │
├───────────────────────────────────────────────────────────┤
│  Conversation Analysis                                    │
│  ├─> Keyword analysis (bugs, security, quality)          │
│  ├─> Code quality indicators (tests, validation)         │
│  ├─> Error pattern detection                             │
│  ├─> Security topic tracking                             │
│  └─> Sentiment analysis                                  │
├───────────────────────────────────────────────────────────┤
│  Pattern Tracking                                         │
│  ├─> Updates patterns.json                               │
│  ├─> Increments occurrence counts                        │
│  └─> Records timestamps                                  │
├───────────────────────────────────────────────────────────┤
│  Learning Reinforcement                                   │
│  ├─> Updates learnings.json                              │
│  ├─> Tracks reinforcement counts                         │
│  └─> Records when topics came up                         │
├───────────────────────────────────────────────────────────┤
│  Metrics Storage                                          │
│  ├─> Updates metrics.json                                │
│  ├─> Stores conversation statistics                      │
│  └─> Tracks trends over time                             │
├───────────────────────────────────────────────────────────┤
│  Next Session Starts                                      │
│  └─> SessionStart Hook loads learnings                   │
│      └─> Claude receives context about patterns          │
│          └─> Proactively applies learnings!              │
└───────────────────────────────────────────────────────────┘
```

## Hook Configuration

The plugin includes two hooks:

### 1. Stop Hook (End of Conversation)

**Trigger**: When conversation ends
**Script**: `analyze-conversation.sh`
**Purpose**: Analyze conversation and track patterns

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/analyze-conversation.sh"
          }
        ]
      }
    ]
  }
}
```

### 2. SessionStart Hook (New Conversation)

**Trigger**: When new session begins
**Script**: `load-learnings.sh`
**Purpose**: Load patterns and learnings into context

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/load-learnings.sh"
          }
        ]
      }
    ]
  }
}
```

## What Gets Analyzed

### Keyword Analysis

Tracks mentions of important topics:

**Bug Keywords**: `bug`, `error`, `issue`, `problem`, `wrong`, `fail`
- Triggers: `high_bug_discussion` pattern if > 5 mentions

**Security Keywords**: `security`, `vulnerability`, `injection`, `xss`, `auth`, `password`
- Triggers: `security_focus` pattern if > 3 mentions

**Quality Keywords**: `quality`, `review`, `improve`, `optimize`, `refactor`
- Tracks quality consciousness

**Help Requests**: `help`, `how to`, `how do`, `can you`, `please`
- Measures support load

### Code Quality Indicators

Analyzes code-related patterns:

**Code Blocks**: Counts ` ``` ` blocks
**Test Mentions**: `test`, `spec`, `unittest`, `pytest`, `jest`
- Triggers: `missing_tests` if code exists but no tests mentioned

**Validation**: `validate`, `sanitize`, `check`, `verify`
- Triggers: `missing_validation` if code exists but no validation

**Error Handling**: `try`, `catch`, `except`, `error handling`
- Tracks error handling awareness

### Error Detection

Identifies error patterns:

**Syntax Errors**: `syntax error`, `syntaxerror`, `parse error`
**Runtime Errors**: `runtime error`, `exception`, `traceback`, `stack trace`
**Logic Errors**: `logic error`, `incorrect`, `doesn't work`, `not working`

- Triggers: `high_error_rate` if total errors > 3

### Security Analysis

Tracks security topic discussions:

**SQL Injection**: Discussion about parameterized queries
- Creates learning: "Use parameterized queries"

**XSS**: Cross-site scripting mentions
- Creates learning: "Sanitize HTML output"

**Authentication**: Auth/authorization discussions
- Tracks security consciousness

**Secrets**: API keys, passwords, credentials mentions
- Monitors credential handling

### Sentiment Analysis

Measures user experience:

**Positive**: `thank`, `thanks`, `great`, `perfect`, `excellent`, `good`, `helpful`
**Negative**: `wrong`, `incorrect`, `doesn't work`, `not working`, `confused`, `unclear`
**Confusion**: Questions, clarifications, misunderstandings

- Triggers: `negative_user_experience` if sentiment < -3
- Triggers: `unclear_communication` if confusion > 5

## Data Storage

All data is stored in `~/.claude/self-improvement/`:

### patterns.json

```json
{
  "patterns": [
    {
      "type": "missing_tests",
      "description": "Code provided but no tests mentioned",
      "severity": "important",
      "count": 12,
      "first_seen": "2025-01-10T09:15:00",
      "last_seen": "2025-01-20T16:45:00"
    }
  ]
}
```

### learnings.json

```json
{
  "learnings": [
    {
      "key": "sql_injection_discussed",
      "text": "SQL injection topic came up - ensure parameterized queries used",
      "learned_at": "2025-01-10T09:00:00",
      "reinforced_count": 5,
      "last_reinforced": "2025-01-20T15:30:00"
    }
  ]
}
```

### metrics.json

```json
{
  "sessions": [
    {
      "session_id": "1234567890",
      "timestamp": "2025-01-20T16:30:00",
      "total_turns": 15,
      "user_turns": 8,
      "assistant_turns": 7,
      "total_lines": 523
    }
  ]
}
```

### analysis.log

Plain text log of all analysis runs:
```
[2025-01-20T16:30:00] === Starting conversation analysis for session 1234567890 ===
[2025-01-20T16:30:00] Statistics: 15 total turns, 8 user, 7 assistant, 523 lines
[2025-01-20T16:30:00] Keywords: bugs=3, security=2, quality=5, help_requests=2
[2025-01-20T16:30:00] Code Quality: 4 code blocks, tests=0, validation=1, error_handling=2
[2025-01-20T16:30:00] PATTERN DETECTED: [important] missing_tests: Code provided but no tests mentioned
...
```

## Viewing Tracked Data

Use the provided commands to view accumulated data:

### View Patterns

```bash
/show-patterns
```

Shows all tracked patterns with:
- Pattern type and description
- Severity (critical/important/minor)
- Occurrence count
- First and last seen timestamps

### View Learnings

```bash
/show-learnings
```

Shows all learning points with:
- Learning key and text
- When first learned
- Reinforcement count
- Last reinforcement timestamp

### View Metrics

```bash
/show-metrics
```

Shows conversation statistics:
- Total sessions analyzed
- Average/median conversation length
- Recent session history
- Trend analysis

## Context Loading

At the start of each new session, the SessionStart hook loads important context:

```
🔄 Self-Improvement Context Loaded

⚠️ Critical patterns to watch:
  • high_error_rate: Multiple errors encountered in conversation (seen 5x)

📋 Important patterns to remember:
  • missing_tests: Code provided but no tests mentioned (seen 12x)
  • missing_validation: Code provided but no input validation mentioned (seen 8x)

💡 Recent learning points:
  • SQL injection topic came up - ensure parameterized queries used
  • Input validation missing - add validation before business logic
  • Tests not provided with code - always include test examples

Apply these learnings proactively in this session to avoid repeating past issues.
```

This context helps Claude:
- **Avoid recurring mistakes** before they happen
- **Proactively apply learnings** without being reminded
- **Focus on known weaknesses** in advance
- **Improve first-time quality** based on past patterns

## Pattern Elimination Workflow

The goal is to eliminate patterns through learning:

```
1. Pattern Detected: "missing_tests" (count: 1)
   └─> Conversation had code but no tests

2. Pattern Reinforced: "missing_tests" (count: 5)
   └─> Still forgetting to include tests

3. Learning Applied: Tests now included proactively
   └─> Pattern stops being triggered

4. Pattern Eliminated: Count stays at 5, no new occurrences
   └─> Success! Behavior improved.
```

**Measuring Success:**
- **Bad**: Pattern count keeps increasing
- **Good**: Pattern count stops growing
- **Excellent**: New patterns don't get created

## Management Scripts

### View All Data

```bash
# View patterns
bash ~/.claude/plugins/self-improvement/hooks/scripts/view-patterns.sh

# View learnings
bash ~/.claude/plugins/self-improvement/hooks/scripts/view-learnings.sh

# View metrics
bash ~/.claude/plugins/self-improvement/hooks/scripts/view-metrics.sh
```

### Reset Data

To clear all tracked data (use with caution):

```bash
bash ~/.claude/plugins/self-improvement/hooks/scripts/reset-data.sh
```

This will:
- Backup existing data
- Clear patterns, learnings, and metrics
- Reset to fresh state
- Keep backups in `~/.claude/self-improvement/backups/`

## Privacy & Data

**What's tracked:**
- Conversation statistics (turns, lines)
- Keyword occurrences (counts only)
- Pattern detections
- Learning reinforcements

**What's NOT tracked:**
- Actual conversation content
- User information
- Code snippets
- Specific details

**All data is stored locally** in your home directory: `~/.claude/self-improvement/`

## Customization

### Adjust Thresholds

Edit `analyze-conversation.sh` to customize:

```bash
# Current thresholds
local bug_count_threshold=5    # Trigger high_bug_discussion
local security_count_threshold=3  # Trigger security_focus
local error_threshold=3          # Trigger high_error_rate
local sentiment_threshold=-3     # Trigger negative_user_experience
local confusion_threshold=5      # Trigger unclear_communication
```

### Add Custom Patterns

Add your own pattern detection:

```bash
analyze_custom_pattern() {
    local file="$1"

    # Count your custom keywords
    local custom_count=$(grep -ci "your-keyword" "${file}" 2>/dev/null || echo "0")

    if [[ ${custom_count} -gt THRESHOLD ]]; then
        track_pattern "custom_pattern" "Your description" "severity"
    fi
}
```

### Add Custom Learnings

Add custom learning triggers:

```bash
if [[ ${custom_topic} -gt 0 ]]; then
    track_learning "custom_learning" "Your learning point text"
fi
```

## Troubleshooting

### Hooks Not Running

**Check hook installation:**
```bash
# Verify hooks.json exists
ls ~/.claude/plugins/self-improvement/hooks/hooks.json

# Verify scripts are executable
ls -l ~/.claude/plugins/self-improvement/hooks/scripts/
```

**Check Claude Code hook support:**
- Ensure your Claude Code version supports hooks
- Check `.claude/settings.json` for hook configuration

### No Data Being Tracked

**Check log file:**
```bash
tail -n 50 ~/.claude/self-improvement/analysis.log
```

**Common issues:**
- Transcript file not found (path may vary)
- Python3 not installed
- Permissions issue with ~/.claude directory

### Data Files Corrupted

**Reset and start fresh:**
```bash
bash ~/.claude/plugins/self-improvement/hooks/scripts/reset-data.sh
```

## Benefits of Automated Analysis

### Passive Learning
- No user action required
- Runs automatically in background
- Builds knowledge base over time

### Pattern Recognition
- Identifies recurring issues automatically
- Quantifies how often mistakes happen
- Tracks improvement (or regression)

### Proactive Improvement
- Context loaded at session start
- Claude knows what to avoid
- First-time quality improves

### Objective Measurement
- Concrete metrics (not just feelings)
- Trend analysis over time
- Evidence-based improvement

### Continuous Feedback Loop
```
Conversation → Analysis → Pattern Detection → Learning →
Context Loading → Better Conversation → Repeat
```

## Example: Pattern Elimination

**Week 1:**
```
Pattern: missing_tests
Count: 8 occurrences
Status: Recurring problem
```

**Week 2:**
```
Context loaded: "Tests not provided with code - always include test examples"
Claude includes tests proactively in 6/7 conversations
Pattern: missing_tests
Count: 9 occurrences (+1, down from +8/week)
Status: Improving!
```

**Week 3:**
```
Context reinforced: Tests are now automatic
Claude includes tests in all conversations
Pattern: missing_tests
Count: 9 occurrences (+0)
Status: Eliminated! 🎉
```

## Advanced: Integration with Manual Review

Combine automated analysis with manual review:

```bash
# End of conversation:
1. Automated analysis runs (Stop hook)
2. Patterns/learnings tracked automatically

# Start of next session:
1. Context loaded automatically (SessionStart hook)
2. Manual review if needed: /review-my-work
3. See both automated patterns and manual critique
```

**Best of both worlds:**
- **Automated**: Catches patterns across conversations
- **Manual**: Deep dive into specific conversation quality
- **Combined**: Comprehensive continuous improvement

## Future Enhancements

Potential future features:
- ML-based pattern detection
- Automatic suggestion generation from patterns
- Integration with code review tools
- Trend visualization dashboard
- Export reports for teams
- Pattern sharing across users (opt-in)

---

**Automated analysis makes self-improvement effortless** - it just happens in the background, continuously learning and improving! 🔄📈
