---
description: Comprehensive project health check providing status metrics, blocker analysis, progress tracking, and recommendations for next steps
allowed-tools: Bash, Read, Grep, Glob, Task
argument-hint: "[project-name]"
---

# Project Status Command

Generates a comprehensive project health report including current status, velocity metrics, blocker analysis, sprint progress, dependency health, and data-driven recommendations.

## Arguments

- **`$1`**: Project name or repository (optional)
  - If provided: Analyzes specific project/repository
  - If not provided: Analyzes current repository
  - Format: "project-name", "org/repo", or "." for current

## Workflow

When this command is invoked with `/project-manager:project-status [project-name]`:

### Phase 1: Project Discovery

1. **Determine Target Project**:
   - If `$1` provided: Use specified project
   - If not: Use current directory's git repository

2. **Gather Project Metadata**:
   ```bash
   # Repository information
   gh repo view --json name,description,url,isPrivate,defaultBranch

   # Project health metrics
   gh repo view --json stargazerCount,forkCount,openIssues,watchers
   ```

### Phase 2: Current State Analysis

3. **Sprint Status** (if active sprint exists):
   ```bash
   # Check current sprint
   gh project list

   # Read sprint plan if exists
   cat .claude-project/sprints/[current-sprint]-plan.md
   ```

   Analyze:
   - Days elapsed vs total
   - Story points completed vs committed
   - Burndown trajectory
   - In-progress vs completed work

4. **Issue Status**:
   ```bash
   # All open issues
   gh issue list --state open --json number,title,labels,state,assignees,createdAt

   # Recent closed issues
   gh issue list --state closed --limit 20 --json number,title,closedAt
   ```

   Metrics:
   - Total open issues
   - Issues by priority (high/medium/low)
   - Issues by type (bug/feature/tech-debt)
   - Average age of open issues
   - Velocity (issues closed per week)

5. **Pull Request Status**:
   ```bash
   # Open PRs
   gh pr list --state open --json number,title,author,createdAt,reviews

   # Recent merged PRs
   gh pr list --state merged --limit 10 --json number,title,mergedAt
   ```

   Metrics:
   - Open PRs count
   - PR age (average time open)
   - Review status
   - Merge rate (PRs per week)

6. **Blocker Analysis**:
   - Issues labeled "blocked"
   - PRs waiting for review >3 days
   - Dependencies not met
   - Stale work in progress

### Phase 3: Velocity & Trends

7. **Calculate Velocity**:
   - Issues closed in last 1/2/4 weeks
   - Story points completed (if tracked)
   - Compare to historical average
   - Identify trends (improving/stable/declining)

8. **Identify Patterns**:
   - Most active contributors
   - Areas with most activity (labels/components)
   - Time to close (bugs vs features)
   - Review turnaround time

### Phase 4: Health Assessment

9. **Overall Health Score** (1-5):
   ```markdown
   Factors:
   - Sprint on track: +1
   - Low blocker count: +1
   - Healthy velocity: +1
   - PRs moving quickly: +1
   - Low bug backlog: +1

   Score: 5 = Excellent, 4 = Good, 3 = Fair, 2 = At Risk, 1 = Critical
   ```

10. **Risk Identification**:
    - Sprint at risk of missing goals
    - Too many blockers
    - Declining velocity
    - Stale PRs piling up
    - Growing bug backlog
    - Key dependencies unresolved

### Phase 5: Recommendations

11. **Generate Actionable Recommendations**:
    Based on health assessment:
    - If sprint behind: "Consider descoping or requesting help"
    - If many blockers: "Schedule blocker resolution session"
    - If stale PRs: "Prioritize code reviews"
    - If declining velocity: "Investigate capacity or complexity issues"

12. **Suggest Next Steps**:
    - Upcoming milestones
    - Issues ready to start
    - PRs ready for review
    - Planning activities needed

### Phase 6: Reporting

13. **Generate Status Report**:
    Create comprehensive dashboard with:
    - Executive summary (health score + key metrics)
    - Sprint progress (if applicable)
    - Issue metrics and trends
    - PR metrics and review status
    - Blocker analysis
    - Velocity trends
    - Risk assessment
    - Recommendations

14. **Optional: Save Report**:
    ```bash
    # Create status report document
    echo "[report]" > .claude-project/status-reports/status-[date].md
    ```

## Examples

### Example Usage 1: Current Repository
```
/project-manager:project-status
```

Expected behavior:
1. Analyzes current git repository
2. Checks active sprint (if exists)
3. Analyzes issues, PRs, and blockers
4. Calculates velocity and trends
5. Generates health score
6. Provides recommendations

Output:
```markdown
📊 Project Status Report: my-project

Overall Health: 🟢 Good (4/5)

━━━━━━━━━━━━━━━━━━━━━━

📅 Sprint 6 Progress:
Status: On Track
Days: 7 / 10 (70%)
Completed: 22 / 38 points (58%)
Burndown: On pace

━━━━━━━━━━━━━━━━━━━━━━

📋 Issues:
Open: 45 total
- High: 8 (ready: 6)
- Medium: 22 (ready: 15)
- Low: 15

Velocity: 12 issues/week
Trend: ↗ Improving (+15% vs last month)

━━━━━━━━━━━━━━━━━━━━━━

🔀 Pull Requests:
Open: 5 PRs
- Ready for review: 2
- In review: 2
- Changes requested: 1

Avg time to merge: 1.5 days

━━━━━━━━━━━━━━━━━━━━━━

⚠️  Blockers: 2
- #134: Waiting on API design (8 days)
- #156: External dependency (3 days)

━━━━━━━━━━━━━━━━━━━━━━

💡 Recommendations:
1. Escalate API design review (blocking #134)
2. Consider moving 1 issue to next sprint for buffer
3. Schedule blocker resolution session

📝 Next Steps:
- Review PRs #145, #147
- Start issues #158, #162 (high priority, ready)
- Prepare for sprint review (Day 10)
```

### Example Usage 2: Specific Repository
```
/project-manager:project-status my-org/api-service
```

Expected behavior:
1. Switches context to specified repository
2. Runs full health check
3. Provides status specific to that project

### Example Usage 3: Multi-Project Dashboard
```
/project-manager:project-status all
```

Expected behavior:
1. Discovers all projects in organization/workspace
2. Generates high-level dashboard for each
3. Provides portfolio-level summary
4. Highlights projects needing attention

## Important Notes

### Prerequisites
- GitHub CLI (`gh`) authenticated
- Git repository context (or specify repository)
- Recommended: Active sprint plan for sprint metrics

### Delegation Points
This command may delegate to:
- **workflow-orchestrator**: For detailed GitHub operations
- **planning-sprints skill**: Auto-invokes for sprint analysis
- **coordinating-projects skill**: For multi-project analysis

### Read-Only Operation
- This command does NOT modify any state
- Purely analytical and reporting
- Safe to run frequently (daily, before standups, etc.)

### Frequency Recommendations
- Daily: During active sprints
- Weekly: For overall project health
- On-demand: Before planning sessions, stakeholder meetings

### Integration with Other Commands
- Follow up unhealthy status with:
  - `/project-manager:plan-sprint` if sprint needed
  - `/project-manager:prioritize-backlog` if backlog messy
  - `/project-manager:delegate-task` to address blockers

## Output Format

```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 PROJECT STATUS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project: [Project Name]
Repository: [org/repo]
Generated: [Date & Time]
Overall Health: [🟢/🟡/🔴] [Rating] ([Score]/5)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 EXECUTIVE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: [On Track / At Risk / Behind]

Key Metrics:
- Sprint Progress: [X]% complete
- Open Issues: [Y]
- Active PRs: [Z]
- Blockers: [W]
- Velocity Trend: [↗/→/↘]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 ACTIVE SPRINT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sprint: [Name]
Goal: [Sprint Goal]
Dates: [Start] - [End]

Progress:
- Days Elapsed: [X] / [Y] ([Z]%)
- Points Completed: [X] / [Y] ([Z]%)
- Issues Done: [X] / [Y]

Status: [Ahead / On Pace / Behind]
Burn Rate: [X] points/day
Projected Completion: [X]% (target: 100%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 ISSUES & BACKLOG
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Open Issues: [Total]

By Priority:
- 🔴 High: [X] issues ([Y] ready)
- 🟡 Medium: [X] issues ([Y] ready)
- ⚪ Low: [X] issues ([Y] ready)

By Type:
- Features: [X]
- Bugs: [Y]
- Tech Debt: [Z]
- Docs: [W]

Velocity:
- Last Week: [X] issues closed
- Last Month: [Y] issues closed
- Average: [Z] issues/week
- Trend: [↗ Improving / → Stable / ↘ Declining]

Avg Age of Open Issues: [X] days

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔀 PULL REQUESTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Open PRs: [X]
- Ready for review: [Y]
- In review: [Z]
- Changes requested: [W]

Avg Time to Merge: [X] days
PRs Merged (last week): [Y]

Oldest PR: #[num] ([X] days old)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  BLOCKERS & RISKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Active Blockers: [X]

Critical:
- #[num]: [Description] ([X] days blocked)
- #[num]: [Description] ([X] days blocked)

Risks Identified:
- [Risk 1]: [Impact & Mitigation]
- [Risk 2]: [Impact & Mitigation]

Stale Work:
- [X] issues in progress >7 days
- [Y] PRs open >14 days

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 VELOCITY TRENDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sprint Velocity (last 5 sprints):
Sprint N-4: [X] points
Sprint N-3: [Y] points
Sprint N-2: [Z] points
Sprint N-1: [W] points
Current:    [V] points (projected)

Average: [X] points/sprint
Trend: [↗ +15% / → Stable / ↘ -10%]

Issue Closure Rate:
Week 1: [X] issues
Week 2: [Y] issues
Week 3: [Z] issues
Week 4: [W] issues (current)

Average: [X] issues/week

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Priority Actions:
1. [Recommendation based on health analysis]
2. [Recommendation based on blockers]
3. [Recommendation based on velocity]

Process Improvements:
- [Suggestion based on patterns]
- [Suggestion based on trends]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Immediate (Today/Tomorrow):
- [ ] [Action item 1]
- [ ] [Action item 2]

This Week:
- [ ] [Action item 3]
- [ ] [Action item 4]

Upcoming Milestones:
- [Milestone 1]: [Date] ([X] days away)
- [Milestone 2]: [Date] ([Y] days away)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Report saved: .claude-project/status-reports/status-[date].md
Run /project-manager:project-status again anytime for updated metrics.
```

## Health Score Calculation

```markdown
Health Score Components (each worth 1 point, max 5):

1. Sprint Progress (if applicable):
   ✅ On pace or ahead: +1
   ❌ Behind by >20%: 0

2. Blocker Count:
   ✅ ≤2 blockers: +1
   ❌ >2 blockers: 0

3. Velocity Trend:
   ✅ Stable or improving: +1
   ❌ Declining >15%: 0

4. PR Flow:
   ✅ Avg merge time <3 days: +1
   ❌ Avg merge time >5 days: 0

5. Issue Health:
   ✅ Bug ratio <20% of total: +1
   ❌ Bug ratio >30%: 0

Rating Scale:
5 = 🟢 Excellent - Project in great shape
4 = 🟢 Good - Minor issues, generally healthy
3 = 🟡 Fair - Some concerns, needs attention
2 = 🟡 At Risk - Significant issues, action needed
1 = 🔴 Critical - Major problems, urgent intervention
```

## Advanced Features

### Trend Analysis
- Tracks metrics over time if run regularly
- Identifies patterns (seasonal velocity changes, recurring blockers)
- Predicts future completion dates based on trends

### Comparative Analysis
- Compares current sprint to past sprints
- Benchmarks against historical averages
- Highlights anomalies

### Automated Alerts
- Flags critical issues automatically
- Provides severity levels for problems
- Suggests escalation when needed

### Export Formats
- Markdown (default, for documentation)
- JSON (for custom dashboards)
- HTML (for sharing with stakeholders)
