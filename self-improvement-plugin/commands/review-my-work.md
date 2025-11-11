---
description: Invoke the self-critic agent to review Claude's recent work and provide feedback
allowed-tools: Read, Grep, Glob
model: sonnet
---

# Review My Work

Invoke the self-critic agent to perform a comprehensive review of Claude's recent work and provide constructive feedback for improvement.

## Your Task

Use the `self-critic` agent to analyze the conversation and Claude's outputs, then provide a detailed critique.

### Step 1: Gather Context
Review the conversation history to understand:
- What tasks Claude was asked to perform
- What outputs Claude generated
- What requirements were given
- What constraints existed

### Step 2: Invoke Self-Critic Agent
Use the Task tool to invoke the self-critic agent:

```
Please invoke the self-critic agent to:
1. Review all work completed in this conversation
2. Analyze the quality of responses, code, and solutions
3. Identify strengths and weaknesses
4. Provide specific, actionable feedback
5. Suggest improvements
6. Extract learning points

Focus on the most recent complex task or the overall conversation quality.
```

### Step 3: Present Findings
After the self-critic completes its analysis, summarize:
- Overall quality assessment
- Key issues found
- Most important improvements needed
- Learning points to remember

### Step 4: Offer to Implement
Ask the user if they want to:
- Fix any critical issues identified
- Implement suggested improvements
- Iterate on the solution
- Continue with current approach

## Usage

This command triggers a comprehensive self-review:

```bash
/review-my-work
```

## What Gets Reviewed

The self-critic will analyze:
- **Code Quality**: Bugs, best practices, security, performance
- **Completeness**: Requirements coverage, edge cases, error handling
- **Clarity**: Explanations, documentation, examples
- **Correctness**: Accuracy of information and implementations
- **Communication**: Tone, structure, helpfulness
- **Process**: Approach taken, decisions made

## Output Format

The review will include:
1. **Quality Scores**: Numerical ratings across dimensions
2. **Strengths**: What was done well
3. **Critical Issues**: Must-fix problems
4. **Important Concerns**: Should-fix problems
5. **Suggestions**: Nice-to-have improvements
6. **Learning Points**: Lessons for future work
7. **Next Steps**: Recommended actions

## When to Use

Use this command:
- After completing complex or critical tasks
- When unsure about solution quality
- To learn from mistakes
- To establish best practices
- Before final delivery of important work
- When iterating on solutions

## Example

**User**: `/review-my-work`

**Claude**: I'll invoke the self-critic agent to review the authentication system I just built...

[Invokes self-critic agent via Task tool]

**Self-Critic Output**:
```
# Self-Critique: Authentication System Implementation

## Overview
Built a user authentication system with login, registration, and session management.
Overall quality: 3.5/5 - Functional but has security issues.

## Quality Scores
- Correctness: 3/5 - Logic works but has vulnerabilities
- Completeness: 4/5 - Missing password reset
- Clarity: 4/5 - Well-documented
- Efficiency: 3/5 - No caching
- Security: 2/5 - Critical issues found
- Usability: 4/5 - Easy to integrate

## Critical Issues
🔴 SQL injection vulnerability in login function (line 45)
🔴 Passwords hashed with weak MD5 algorithm
🔴 No rate limiting on login attempts

## Important Concerns
🟡 Missing password reset functionality
🟡 Session tokens not securely generated
🟡 No input validation on registration

## Suggestions
🔵 Add remember-me functionality
🔵 Implement two-factor authentication
🔵 Add audit logging

## Next Steps
1. IMMEDIATE: Fix SQL injection (use parameterized queries)
2. IMMEDIATE: Upgrade to bcrypt for passwords
3. Soon: Add rate limiting
4. Soon: Implement password reset
```

**Claude**: Based on the self-critique, I've identified several critical security issues that need immediate attention. Would you like me to:
1. Fix the SQL injection and password hashing immediately?
2. Address all critical and important issues?
3. Review the complete improvement list and prioritize together?

## Benefits

Using `/review-my-work` helps:
- Catch errors before they cause problems
- Learn from mistakes
- Improve code quality
- Build better habits
- Deliver higher quality work
- Grow expertise over time

## Tips

**For Best Results**:
- Use after completing significant work
- Be open to critical feedback
- Focus on learning, not perfection
- Implement at least critical fixes
- Track recurring issues over time

**When Not to Use**:
- For trivial tasks
- When time is extremely limited
- If work is already thoroughly reviewed
- For quick questions or simple responses

## Related Commands

- `/improve-this` - Get suggestions for specific code/text
- `/fix-issues` - Address known problems
- `/quality-check` - Quick quality assessment

## Important Notes

- The self-critic is honest and direct - expect critical feedback
- Focus on learning from issues, not feeling bad about them
- Not all suggestions need to be implemented immediately
- Prioritize based on severity and impact
- Use insights to improve future work

---

This command activates the self-improvement system to help Claude continuously improve through honest self-assessment and constructive feedback.
