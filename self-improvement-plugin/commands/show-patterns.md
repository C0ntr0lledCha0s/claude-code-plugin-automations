---
description: Display tracked patterns from automated conversation analysis
allowed-tools: Bash
model: haiku
---

# Show Patterns

Display all patterns that have been automatically tracked by the self-improvement system.

## Your Task

Execute the view-patterns script to show tracked patterns.

```bash
bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/view-patterns.sh
```

## What This Shows

The system automatically tracks patterns across all conversations, including:

**Pattern Types:**
- `high_bug_discussion` - Conversations with many bug mentions
- `security_focus` - Security-related topics
- `missing_tests` - Code without tests
- `missing_validation` - Code without input validation
- `high_error_rate` - Multiple errors encountered
- `negative_user_experience` - User frustration
- `unclear_communication` - User confusion

**Pattern Information:**
- **Type**: Pattern identifier
- **Description**: What the pattern represents
- **Severity**: Critical (🔴), Important (🟡), Minor (🟢)
- **Occurrences**: How many times seen
- **First/Last seen**: When the pattern was detected

## Example Output

```
🔴 CRITICAL: high_error_rate
   Description: Multiple errors encountered in conversation
   Occurrences: 5
   First seen: 2025-01-15T10:30:00
   Last seen: 2025-01-20T14:20:00

🟡 IMPORTANT: missing_tests
   Description: Code provided but no tests mentioned
   Occurrences: 12
   First seen: 2025-01-10T09:15:00
   Last seen: 2025-01-20T16:45:00
```

## Usage

```bash
/show-patterns
```

## Interpreting Results

**Critical Patterns (🔴):**
- Require immediate attention
- Indicate serious recurring issues
- Should be addressed proactively in every conversation

**Important Patterns (🟡):**
- Should be improved
- Common issues that affect quality
- Worth consciously avoiding

**Minor Patterns (🟢):**
- Nice to improve
- Low-impact issues
- Track for trends

## Taking Action

Based on patterns shown:
1. **Acknowledge the pattern**: Be aware it's recurring
2. **Understand why**: What causes this pattern?
3. **Create prevention**: How to avoid it next time?
4. **Apply proactively**: Use the learning in future work

## Related Commands

- `/show-learnings` - View learning points
- `/show-metrics` - View conversation statistics
- `/review-my-work` - Trigger manual review
- `/quality-check` - Quick quality assessment

---

Patterns are automatically tracked at the end of each conversation to enable continuous improvement.
