---
description: Display tracked learning points from automated conversation analysis
allowed-tools: Bash
model: haiku
---

# Show Learnings

Display all learning points that have been automatically tracked by the self-improvement system.

## Your Task

Execute the view-learnings script to show tracked learnings.

```bash
bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/view-learnings.sh
```

## What This Shows

The system automatically tracks learning points when specific topics or issues come up in conversations:

**Learning Categories:**
- **Security**: SQL injection, XSS, authentication, etc.
- **Best Practices**: Testing, validation, error handling
- **Code Quality**: Structure, maintainability, performance
- **Communication**: Clarity, completeness, user focus

**Learning Information:**
- **Key**: Learning identifier
- **Text**: The actual learning point
- **Learned at**: When first tracked
- **Reinforced count**: How many times it came up again
- **Last reinforced**: Most recent mention

## Example Output

```
🔥 sql_injection_discussed
   SQL injection topic came up - ensure parameterized queries used
   Learned: 2025-01-10T09:00:00
   Reinforced: 5 times (last: 2025-01-20T15:30:00)

⭐ missing_validation_pattern
   Input validation missing - add validation before business logic
   Learned: 2025-01-12T11:20:00
   Reinforced: 2 times (last: 2025-01-19T14:10:00)

💡 test_coverage_low
   Tests not provided with code - always include test examples
   Learned: 2025-01-18T16:45:00
```

## Learning Indicators

- **🔥 Highly Reinforced** (3+ times): Critical learning that keeps coming up
- **⭐ Reinforced** (1+ times): Important learning mentioned multiple times
- **💡 New** (0 times): Recently learned, not yet reinforced

## Usage

```bash
/show-learnings
```

## Applying Learnings

When you see highly reinforced learnings:

1. **Internalize the pattern**: Make it automatic
2. **Proactive application**: Use it before issues arise
3. **Create checks**: Add to mental checklist
4. **Reduce count**: Goal is to never trigger the learning again

**Example Application:**
```
Learning: "SQL injection - use parameterized queries"
→ Before writing ANY database query:
  ✓ Check if parameterized
  ✓ Never concatenate user input
  ✓ Use ORM or prepared statements
```

## Reinforcement Tracking

**Why track reinforcement?**
- Shows if learning is being applied
- High reinforcement = pattern not internalized yet
- Low reinforcement = successfully learning
- Zero reinforcement after learning = mastery!

**Goal**: Every highly-reinforced learning should eventually stop being reinforced because you've internalized it and stopped making that mistake.

## Related Commands

- `/show-patterns` - View tracked patterns
- `/show-metrics` - View conversation statistics
- `/review-my-work` - Trigger manual review
- `/quality-check` - Quick quality assessment

---

Learnings are automatically tracked when specific topics arise to build a knowledge base for continuous improvement.
