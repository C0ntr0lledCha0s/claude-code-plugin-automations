---
description: Intelligently routes tasks to appropriate specialized agents (github-workflows, research-agent, self-improvement, agent-builder) based on task type and requirements
allowed-tools: Bash, Read, Grep, Glob, Task
argument-hint: "[task-description]"
---

# Delegate Task Command

Smart task routing system that analyzes task descriptions, determines the most appropriate specialized agent to handle the work, delegates via the Task tool, monitors completion, and reports results.

## Arguments

- **`$ARGUMENTS`**: Complete task description (all arguments combined)
  - Natural language description of what needs to be done
  - Can be detailed or high-level
  - Examples:
    - "Review PR #123 for code quality"
    - "Research best practices for API authentication"
    - "Create a new command for deployment automation"
    - "Triage all open issues"

## Workflow

When this command is invoked with `/project-manager:delegate-task [task-description]`:

### Phase 1: Task Analysis

1. **Parse Task Description**:
   - Extract key information:
     - Task type (code review, research, planning, automation, etc.)
     - Specific references (#PRs, #issues, file paths, etc.)
     - Complexity level
     - Required expertise domain

2. **Categorize Task Type**:
   ```markdown
   GitHub Operations:
   - PR review, merge, creation
   - Issue triage, labeling, organization
   - Project board operations
   - Commit operations
   - Release management

   Research & Analysis:
   - Codebase investigation
   - Best practice research
   - Architecture analysis
   - Technology comparison
   - Pattern identification

   Quality & Improvement:
   - Code quality review
   - Work critique
   - Plan validation
   - Improvement suggestions

   Automation & Tooling:
   - Agent creation
   - Skill development
   - Command creation
   - Hook setup
   - Plugin development

   Planning & Coordination:
   - Sprint planning
   - Backlog prioritization
   - Roadmap creation
   - Multi-project coordination
   ```

### Phase 2: Agent Selection

3. **Apply Delegation Decision Tree**:
   ```markdown
   Task Type → Best Agent

   GitHub Operations:
   - PRs, issues, boards, commits → workflow-orchestrator
   - Specifically PR reviews → pr-reviewer
   - Project coordination → workflow-orchestrator

   Research Tasks:
   - "How does X work?" → investigator
   - "Best practices for Y" → investigator
   - "Compare A vs B" → investigator
   - Codebase exploration → investigator

   Quality Tasks:
   - "Review my work" → self-critic
   - "Check quality of X" → self-critic
   - "Validate this plan" → self-critic

   Automation Tasks:
   - "Create agent/skill/command/hook" → agent-builder commands
   - "Build automation for X" → agent-builder commands
   - "Need custom workflow" → agent-builder commands

   Planning Tasks:
   - "Plan sprint" → project-coordinator (self)
   - "Multi-project coordination" → project-coordinator (self)
   - "Strategic planning" → project-coordinator (self)
   ```

4. **Determine if Multiple Agents Needed**:
   - Complex tasks may require sequential delegation
   - Example: "Implement feature X" might need:
     1. investigator (research best approach)
     2. workflow-orchestrator (create issues/board)
     3. self-critic (review plan)

### Phase 3: Delegation Execution

5. **Prepare Delegation Context**:
   - Extract all relevant information from task description
   - Gather additional context:
     ```bash
     # If task mentions PR/issue numbers, fetch details
     gh pr view #123 --json title,body,state

     # If task involves files, check their existence
     test -f path/to/file.ts && echo "exists"

     # If task is about current project, gather repo info
     gh repo view --json name,description
     ```

6. **Delegate to Selected Agent**:
   ```markdown
   Use Task tool to invoke the appropriate agent:

   Task tool:
   - subagent_type: [selected-agent]
   - description: [5-word summary]
   - prompt: [detailed instructions with full context]
   ```

7. **Monitor Delegation**:
   - Wait for agent response
   - Track progress (if long-running)
   - Handle any errors or clarification requests

### Phase 4: Result Processing

8. **Receive and Validate Results**:
   - Get response from delegated agent
   - Verify task was completed
   - Check for any issues or blockers

9. **Optionally Chain to Next Agent**:
   - If task requires multiple steps
   - Delegate next phase based on results

### Phase 5: Reporting

10. **Generate Summary Report**:
    - What was delegated
    - Which agent handled it
    - What was accomplished
    - Any follow-up actions needed
    - Relevant links/artifacts created

## Examples

### Example Usage 1: PR Review
```
/project-manager:delegate-task Review PR #123 for security and code quality
```

Expected behavior:
1. Analyzes task: "PR review" → delegate to pr-reviewer
2. Fetches PR #123 details
3. Delegates to pr-reviewer agent:
   ```markdown
   Task → pr-reviewer:
   "Perform comprehensive security and code quality review of PR #123.
   Focus on: security vulnerabilities, code quality, test coverage, documentation."
   ```
4. Receives review results
5. Reports summary with review findings

Output:
```markdown
✅ Task Delegated & Completed

Task: Review PR #123 for security and code quality
Delegated To: pr-reviewer (github-workflows plugin)

Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━
PR #123: Add OAuth authentication

Quality Score: 4.2 / 5.0

Findings:
✅ Security: No critical issues
⚠️  Code Quality: 2 minor improvements suggested
✅ Tests: Good coverage (87%)
⚠️  Docs: Missing API documentation

Detailed Review: [link to review comments]

Recommendation: Approve after minor fixes
━━━━━━━━━━━━━━━━━━━━━━━━━━

Next Steps:
- Address documentation gaps
- Apply suggested code improvements
- Re-request review after fixes
```

### Example Usage 2: Research Task
```
/project-manager:delegate-task Research best authentication patterns for our API
```

Expected behavior:
1. Analyzes task: "Research best practices" → delegate to investigator
2. Delegates to investigator agent:
   ```markdown
   Task → investigator:
   "Research industry best practices for API authentication.
   Focus on: security, developer experience, scalability.
   Provide recommendations for our use case."
   ```
3. Receives research findings
4. Reports summary

Output:
```markdown
✅ Task Delegated & Completed

Task: Research best authentication patterns for our API
Delegated To: investigator (research-agent plugin)

Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Authentication Patterns Research

Recommended Approach: OAuth 2.0 + JWT

Findings:
1. OAuth 2.0 (Industry Standard)
   - Pros: Secure, flexible, widely adopted
   - Cons: Complex setup
   - Use Cases: Third-party integrations

2. JWT Tokens (Recommended for APIs)
   - Pros: Stateless, scalable, fast
   - Cons: Token revocation complexity
   - Use Cases: First-party mobile/web apps

3. API Keys (Simple but Limited)
   - Pros: Easy to implement
   - Cons: Less secure, limited control
   - Use Cases: Internal services only

Recommendation:
- Primary: OAuth 2.0 for external clients
- Secondary: JWT for first-party apps
- API Keys: Internal service-to-service only

Implementation Guide: [link to research document]
━━━━━━━━━━━━━━━━━━━━━━━━━━

Next Steps:
- Review recommendations with team
- Prototype OAuth + JWT implementation
- Plan migration strategy
```

### Example Usage 3: Complex Multi-Step Task
```
/project-manager:delegate-task Implement user notification system
```

Expected behavior:
1. Analyzes task: Complex implementation → needs research + planning
2. Breaks into steps:
   - Step 1: Research (delegate to investigator)
   - Step 2: Planning (handle self as project-coordinator)
   - Step 3: Execution tracking (delegate to workflow-orchestrator)
3. Executes each step sequentially
4. Reports comprehensive results

Output:
```markdown
✅ Multi-Step Task Delegated & Completed

Task: Implement user notification system
Strategy: Sequential delegation (3 phases)

━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 1: Research (investigator)
━━━━━━━━━━━━━━━━━━━━━━━━━━

Researched:
- Notification delivery patterns
- Real-time vs batch notifications
- Technology options (WebSocket, SSE, Push API)

Recommendation: WebSocket for real-time + email for async
Research Doc: .claude-project/research/notifications-2025-03-15.md

━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 2: Planning (project-coordinator)
━━━━━━━━━━━━━━━━━━━━━━━━━━

Created Implementation Plan:
- 5 issues created for notification system
- Estimated: 23 story points total
- Timeline: 2 sprints
- Dependencies mapped

Issues:
- #201: WebSocket server setup (8 pts)
- #202: Notification data model (3 pts)
- #203: Frontend notification UI (5 pts)
- #204: Email notification service (5 pts)
- #205: Testing & documentation (2 pts)

Epic #200 created to track overall initiative

━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase 3: Board Setup (workflow-orchestrator)
━━━━━━━━━━━━━━━━━━━━━━━━━━

Created:
- Project board: "Notification System"
- Added all 5 issues
- Set up dependency tracking
- Configured automation rules

Board: [link to GitHub Project]

━━━━━━━━━━━━━━━━━━━━━━━━━━

Next Steps:
1. Review implementation plan with team
2. Add to next sprint planning
3. Assign issues to team members
4. Begin work on #201 (foundation)
```

### Example Usage 4: Triage All Issues
```
/project-manager:delegate-task Triage all open issues
```

Expected behavior:
1. Analyzes task: "Triage issues" → delegate to workflow-orchestrator
2. Delegates bulk triage operation
3. Reports results

Output:
```markdown
✅ Task Delegated & Completed

Task: Triage all open issues
Delegated To: workflow-orchestrator (github-workflows plugin)

Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Issue Triage Complete

Processed: 67 open issues

Classifications:
- Features: 35 issues
- Bugs: 18 issues (3 critical, 8 high, 7 medium)
- Tech Debt: 10 issues
- Documentation: 4 issues

Duplicates Found: 5 sets (10 issues consolidated)

Relationships Mapped:
- Blocking: 8 dependencies
- Related: 15 clusters

Labels Applied:
- Priority labels: 67 issues
- Type labels: 67 issues
- Component labels: 52 issues

Board Updated: Backlog reorganized by priority

━━━━━━━━━━━━━━━━━━━━━━━━━━

Critical Issues Identified:
- #145: Security vulnerability (requires immediate attention)
- #178: Production bug affecting 1000+ users
- #190: Data corruption risk

Next Steps:
- Address 3 critical bugs immediately
- Review duplicate consolidation
- Plan next sprint from triaged backlog
```

## Important Notes

### Prerequisites
- Access to specialized agents via installed plugins:
  - github-workflows (for workflow-orchestrator, pr-reviewer)
  - research-agent (for investigator)
  - self-improvement (for self-critic)
  - agent-builder (for component creation commands)

### Task Tool Usage
- This command is essentially a router/orchestrator
- Uses Task tool to delegate to specialized agents
- Provides intelligent agent selection

### When to Use
Use this command when:
- ✅ You want smart routing to the right agent
- ✅ You're unsure which agent to use
- ✅ You want a single entry point for delegation
- ✅ You want results summarized consistently

Don't use when:
- ❌ You know exactly which agent you need (invoke directly)
- ❌ Simple tasks you can do yourself
- ❌ Task requires human decision-making

### Delegation Philosophy
- **Right tool for the job**: Routes to most appropriate agent
- **Context preservation**: Passes all relevant information
- **Result synthesis**: Summarizes outcomes clearly
- **Follow-through**: Suggests next steps

## Agent Selection Logic

```markdown
Decision Tree:

1. Parse task description for keywords

2. Match to agent capabilities:

   Keywords: "PR", "pull request", "review PR" → pr-reviewer
   Keywords: "issue", "triage", "label", "board", "project" → workflow-orchestrator
   Keywords: "commit", "release", "deploy" → workflow-orchestrator

   Keywords: "research", "how does", "best practice", "compare" → investigator
   Keywords: "investigate", "analyze pattern", "explore" → investigator

   Keywords: "review my work", "quality check", "critique" → self-critic
   Keywords: "validate", "assess quality" → self-critic

   Keywords: "create agent", "create skill", "create command" → agent-builder commands
   Keywords: "build automation", "create hook" → agent-builder commands

   Keywords: "plan sprint", "roadmap", "multi-project" → project-coordinator (self)

3. If multiple matches → choose most specific

4. If no clear match → ask user to clarify

5. If complex task → break into steps and delegate sequentially
```

## Error Handling

### Ambiguous Task
```
❓ Task Unclear

The task "$ARGUMENTS" could match multiple agents:
1. investigator (research-agent) - for codebase research
2. workflow-orchestrator (github-workflows) - for GitHub operations

Please clarify or rephrase:
- For research: "Research how X works"
- For GitHub ops: "Create board for X"

Or specify agent directly:
- /github-workflows:workflow-orchestrator-invocation
- Use investigator via research-agent commands
```

### Agent Not Available
```
❌ Error: Required agent not available

Task requires: investigator (research-agent plugin)
Status: Plugin not installed

Options:
1. Install research-agent plugin:
   claude plugin install research-agent

2. Handle task manually

3. Use alternative agent (less optimal):
   - Could use workflow-orchestrator for basic analysis
```

### Delegation Failed
```
❌ Delegation Failed

Task: $ARGUMENTS
Attempted Agent: [agent-name]
Error: [error message from agent]

Options:
1. Retry with different approach
2. Delegate to alternative agent
3. Handle task manually
4. Break into smaller sub-tasks

Would you like to retry? [y/n]
```

## Output Format

```markdown
✅ Task Delegated & Completed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Task: [task description]
🤖 Delegated To: [agent-name] ([plugin-name])
⏱️  Completed In: [X] seconds

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Agent-specific results formatted clearly]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 ARTIFACTS CREATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- [Link to PR/Issue/Board/Document]
- [Link to generated files]
- [Link to analysis reports]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [Recommended action 1]
2. [Recommended action 2]
3. [Recommended action 3]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Need additional help? Use /project-manager:delegate-task for more tasks.
```

## Advanced Features

### Learning from Usage
- Tracks which agents work best for which tasks
- Improves routing over time
- Suggests alternatives based on patterns

### Parallel Delegation
- For independent sub-tasks
- Delegates to multiple agents simultaneously
- Combines results

### Context Awareness
- Understands project state
- Routes based on current sprint/phase
- Considers team preferences

### Result Caching
- Avoids re-delegating identical tasks
- Returns cached results when appropriate
- Saves time on repeated requests
