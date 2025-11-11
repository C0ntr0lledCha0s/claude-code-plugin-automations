---
description: Display conversation metrics and statistics from automated analysis
allowed-tools: Bash
model: haiku
---

# Show Metrics

Display conversation metrics and statistics that have been automatically tracked by the self-improvement system.

## Your Task

Execute the view-metrics script to show conversation statistics.

```bash
bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/view-metrics.sh
```

## What This Shows

The system automatically tracks metrics for every conversation:

**Metrics Tracked:**
- Total sessions analyzed
- Average turns per conversation
- Median turns per conversation
- Shortest/longest conversations
- Average/median lines per conversation
- Recent session history

## Example Output

```
📊 Conversation Statistics:
   Total sessions analyzed: 47
   Average turns per conversation: 12.3
   Median turns per conversation: 8.0
   Shortest conversation: 2 turns
   Longest conversation: 45 turns

📝 Volume Statistics:
   Average lines per conversation: 523.4
   Median lines per conversation: 380.0

🕐 Recent Sessions:
   2025-01-20T16:30:00: 15 turns
   2025-01-20T14:20:00: 8 turns
   2025-01-20T11:15:00: 22 turns
   ...
```

## Usage

```bash
/show-metrics
```

## Interpreting Metrics

**Conversation Length:**
- **Short (< 5 turns)**: Quick questions or simple tasks
- **Medium (5-15 turns)**: Standard conversations
- **Long (15+ turns)**: Complex tasks or iterative refinement
- **Very long (30+ turns)**: Deep dives or troubleshooting

**Trends to Watch:**
- **Increasing average**: More complex tasks or more back-and-forth
- **Decreasing average**: Better first-time quality or simpler tasks
- **High variance**: Wide range of conversation types

**Volume Indicators:**
- **High lines/turn**: Detailed explanations or large code blocks
- **Low lines/turn**: Concise communication or quick exchanges

## Using Metrics for Improvement

**Analyze patterns:**
```
If average turns is increasing:
→ Are initial responses less complete?
→ Do questions need clarification?
→ Is communication unclear?

If conversations are getting longer:
→ More complex tasks (good)
→ Or more confusion (needs improvement)
```

**Set baselines:**
```
Track your metrics over time:
Week 1: 15.2 avg turns
Week 2: 13.8 avg turns (-9%)
Week 3: 12.1 avg turns (-12%)

Improvement! Better first-time responses.
```

## Related Commands

- `/show-patterns` - View tracked patterns
- `/show-learnings` - View learning points
- `/review-my-work` - Trigger manual review
- `/quality-check` - Quick quality assessment

---

Metrics are automatically tracked at the end of each conversation to measure improvement over time.
