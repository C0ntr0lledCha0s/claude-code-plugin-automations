---
description: Quick quality assessment of recent work using the analyzing-response-quality skill
allowed-tools: Read, Grep, Glob
model: haiku
---

# Quality Check

Perform a quick quality assessment of Claude's recent work using the analyzing-response-quality skill.

## Your Task

Activate the `analyzing-response-quality` skill to perform a rapid quality evaluation.

### Step 1: Identify What to Check
Determine what needs assessment:
- Most recent code implementation
- Last complex explanation
- Overall conversation quality
- Specific component if specified by user

### Step 2: Run Quality Analysis
Use the analyzing-response-quality skill framework:

```markdown
## Quick Quality Assessment

### Requirements Check
- [✓/✗] Requirement 1
- [✓/✗] Requirement 2
- [✓/✗] Requirement 3

### Quality Scores (1-5)
- Correctness: X/5
- Completeness: X/5
- Clarity: X/5
- Efficiency: X/5
- Security: X/5
- Usability: X/5

### Issues Found
🔴 Critical: [Any critical issues]
🟡 Important: [Any important issues]
🟢 Minor: [Any minor issues]

### Overall: X/5
```

### Step 3: Report Results
Present a concise summary:
- Overall quality rating
- Top 3 issues (if any)
- Quick recommendation (ship it / needs work / critical fixes required)

## Usage

```bash
/quality-check
```

Or with specific target:

```bash
/quality-check the authentication function
```

## What Gets Checked

- **Correctness**: Are there bugs or errors?
- **Completeness**: Is anything missing?
- **Clarity**: Is it understandable?
- **Efficiency**: Is it optimal?
- **Security**: Are there vulnerabilities?
- **Usability**: Can it be easily used?

## Output Format

```markdown
# Quality Check Results

## Overall Rating: X/5

### Status: [✓ Ready to Ship | ⚠️ Needs Improvement | 🔴 Critical Issues]

### Top Issues:
1. [Most important issue]
2. [Second issue]
3. [Third issue]

### Quick Recommendation:
[Ship it | Fix critical issues first | Needs rework | Iterate further]
```

## Example

**User**: `/quality-check`

**Claude**:
```markdown
# Quality Check Results

## Overall Rating: 4/5

### Status: ⚠️ Needs Improvement

### Quality Breakdown:
- Correctness: 4/5 - Logic is sound
- Completeness: 5/5 - All requirements met
- Clarity: 4/5 - Well explained
- Efficiency: 3/5 - Could be optimized
- Security: 3/5 - Missing input validation
- Usability: 5/5 - Easy to use

### Top Issues:
1. 🟡 No input validation on user_id parameter
2. 🟡 Database query could be cached for better performance
3. 🟢 Function name could be more descriptive

### Quick Recommendation:
Add input validation, then ship. Performance optimization can be done later.
```

## When to Use

Use `/quality-check` for:
- Quick sanity check before delivery
- Checkpoint during long tasks
- Rapid assessment of specific components
- When time is limited but quality matters

Use `/review-my-work` instead for:
- Comprehensive deep-dive review
- Learning and improvement focus
- After completing major work
- When quality is critical

## Benefits

- **Fast**: Takes seconds, not minutes
- **Focused**: Highlights most important issues
- **Actionable**: Clear next steps
- **Lightweight**: Doesn't slow down workflow
- **Preventive**: Catches issues early

## Tips

**For Best Results**:
- Use as checkpoints during work
- Fix critical issues immediately
- Note patterns for later improvement
- Don't let minor issues block progress

**Interpretation Guide**:
- 5/5: Excellent, ship it
- 4/5: Good, minor improvements optional
- 3/5: Okay, important improvements needed
- 2/5: Poor, significant rework required
- 1/5: Critical, must fix before use

## Related Commands

- `/review-my-work` - Comprehensive review with self-critic agent
- `/improve-this` - Get specific improvement suggestions
- `/fix-issues` - Address identified problems

## Important Notes

- This is a **quick check**, not a thorough review
- Critical issues should always be addressed
- Use judgment on whether to fix other issues now or later
- For critical systems, use `/review-my-work` instead

---

Quick quality checks help maintain high standards without slowing down workflow.
