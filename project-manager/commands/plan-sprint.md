---
description: Interactive sprint planning workflow that analyzes backlog, calculates capacity, applies prioritization, and creates a sprint plan with board setup
allowed-tools: Bash, Read, Write, Grep, Glob, Task
argument-hint: "[sprint-name]"
---

# Plan Sprint Command

Facilitates comprehensive sprint planning by analyzing the backlog, calculating team capacity, prioritizing issues, and creating a complete sprint plan with GitHub Project board setup.

## Arguments

- **`$1`**: Sprint name or number (e.g., "Sprint-6", "sprint-15", "2025-03-sprint-01")
  - If not provided, will use auto-incremented sprint number based on existing sprints

## Workflow

When this command is invoked with `/project-manager:plan-sprint [sprint-name]`:

### Phase 1: Preparation & Context Gathering

1. **Determine Sprint Name**:
   - If `$1` provided: Use as sprint name
   - If not: Auto-detect next sprint number from existing sprint plans

2. **Gather Current State**:
   ```bash
   # Check repository status
   gh repo view --json name,description

   # List all open issues
   gh issue list --limit 100 --json number,title,labels,state,body,milestone

   # Check current sprint status if exists
   gh project list
   ```

3. **Calculate Historical Velocity**:
   - Read past sprint plans from `.claude-project/sprints/`
   - Calculate average velocity from last 3-5 sprints
   - Identify velocity trends (improving, stable, declining)

4. **Determine Team Capacity**:
   - Prompt user for:
     - Team size (number of people)
     - Sprint duration (days)
     - Known PTO/holidays
     - Special commitments (on-call, interviews, etc.)
   - Calculate effective capacity in story points

### Phase 2: Backlog Analysis & Prioritization

5. **Invoke planning-sprints Skill**:
   - Skill automatically activates for sprint planning expertise
   - Provides prioritization framework and best practices

6. **Analyze Backlog Items**:
   - For each open issue:
     - Check if it has story point estimate
     - Review labels and priority
     - Identify dependencies (using triaging-issues if needed)
     - Check for blockers

7. **Apply Prioritization**:
   - Use RICE scoring framework (default) or user-specified framework
   - Consider:
     - Strategic alignment with goals
     - Dependencies (must do X before Y)
     - Technical risk vs business value
     - Quick wins vs long-term investments

8. **Estimate Unestimated Items**:
   - For top-priority items without estimates:
     - Delegate research to investigator if complexity unknown
     - Apply relative estimation (compared to known items)
     - Prompt user for estimates if needed

### Phase 3: Sprint Scope Definition

9. **Define Sprint Goal**:
   - Prompt user: "What is the primary objective for this sprint?"
   - Ensure goal is:
     - Clear and focused (one main theme)
     - Achievable within sprint timeframe
     - Aligned with strategic objectives
     - Measurable (has success criteria)

10. **Select Issues for Sprint**:
    - Start with highest priority items
    - Ensure alignment with sprint goal
    - Check dependencies (include blocking work)
    - Add issues until reaching 80% of capacity
    - Reserve 20% buffer for unknowns and emergent work

11. **Balance Sprint Composition**:
    - Features: 60-70%
    - Bugs: 15-25%
    - Technical Debt: 10-15%
    - Testing/QA: 5-10%

### Phase 4: Sprint Board Creation

12. **Delegate Board Setup to workflow-orchestrator**:
    ```markdown
    Use Task tool to invoke workflow-orchestrator agent:

    "Create GitHub Project board for [sprint-name] with the following configuration:
    - Template: sprint
    - Issues: [list of selected issue numbers]
    - Custom fields:
      - Status (To Do, In Progress, In Review, Done)
      - Priority (High, Medium, Low)
      - Story Points
      - Sprint: [sprint-name]
    - Sprint goal: [user-defined goal]
    "
    ```

13. **Organize Board**:
    - Delegate to workflow-orchestrator for:
      - Adding all selected issues to board
      - Setting priority labels
      - Ordering by priority
      - Adding sprint milestone

### Phase 5: Documentation & Finalization

14. **Create Sprint Plan Document**:
    - Use template from planning-sprints skill:
      ```bash
      cp planning-sprints/templates/sprint-plan-template.md .claude-project/sprints/$1-plan.md
      ```
    - Fill in:
      - Sprint name, dates, duration
      - Sprint goal and success criteria
      - Team capacity calculation
      - Historical velocity
      - Complete sprint backlog with estimates
      - Risks and dependencies
      - Sprint ceremony schedule

15. **Create Sprint Tracking Structure**:
    ```bash
    mkdir -p .claude-project/sprints/$1/
    touch .claude-project/sprints/$1/daily-notes.md
    touch .claude-project/sprints/$1/blockers.md
    touch .claude-project/sprints/$1/retrospective.md
    ```

16. **Quality Check**:
    - Optionally delegate to self-critic:
      ```markdown
      "Review this sprint plan for completeness, realistic scope, and quality"
      ```

17. **Generate Summary Report**:
    - Sprint name and dates
    - Sprint goal
    - Number of issues and total story points
    - Capacity utilization percentage
    - Link to GitHub Project board
    - Link to sprint plan document
    - Key risks identified
    - Next steps (kickoff meeting, etc.)

## Examples

### Example Usage 1: With Sprint Name
```
/project-manager:plan-sprint Sprint-6
```

Expected behavior:
1. Uses "Sprint-6" as sprint name
2. Analyzes backlog (fetches all open issues)
3. Prompts for team capacity details
4. Applies RICE prioritization
5. Prompts for sprint goal
6. Recommends issues based on capacity and priority
7. Creates GitHub Project board via workflow-orchestrator
8. Generates sprint plan document at `.claude-project/sprints/Sprint-6-plan.md`
9. Reports comprehensive summary with links

### Example Usage 2: Auto-Increment
```
/project-manager:plan-sprint
```

Expected behavior:
1. Checks existing sprint plans in `.claude-project/sprints/`
2. Finds last sprint was "Sprint-5"
3. Auto-names new sprint "Sprint-6"
4. Proceeds with standard planning workflow
5. Creates all artifacts with Sprint-6 naming

### Example Usage 3: Date-Based Sprint
```
/project-manager:plan-sprint 2025-03-sprint-01
```

Expected behavior:
1. Uses "2025-03-sprint-01" as sprint name
2. Continues with planning workflow
3. All documents and boards use date-based naming

## Important Notes

### Prerequisites
- GitHub CLI (`gh`) must be installed and authenticated
- Repository must have open issues to plan from
- Recommended: Past sprint data for velocity calculation (optional)

### Delegation Points
This command delegates to:
- **planning-sprints skill**: Automatically invokes for sprint planning expertise
- **workflow-orchestrator agent**: For GitHub Project board creation and issue management
- **investigator agent**: (Optional) For researching unknown complexity items
- **self-critic agent**: (Optional) For sprint plan quality validation

### State Changes
- Creates GitHub Project board (via delegation)
- Creates sprint plan documents in `.claude-project/sprints/`
- May add labels to issues (via workflow-orchestrator)
- May create milestone for sprint (via workflow-orchestrator)

### Customization
Users can customize:
- Prioritization framework (RICE, MoSCoW, WSJF, Value vs Effort)
- Sprint duration (default: 2 weeks)
- Capacity buffer percentage (default: 20%)
- Sprint composition ratios (features vs bugs vs tech debt)

### Best Practices
- Run this command 1-2 days before sprint starts
- Ensure backlog is groomed (issues are well-defined)
- Have team available for capacity discussion
- Review generated plan with team before finalizing

## Interactive Prompts

During execution, this command will prompt the user for:

1. **Team Capacity**:
   ```
   "Sprint Planning - Team Capacity

   How many people on the team? [Number]
   Sprint duration in days? [Default: 10 for 2-week sprint]
   Any PTO or holidays during sprint? [List dates or 'none']
   Average hours per person per day? [Default: 5-6]
   "
   ```

2. **Sprint Goal**:
   ```
   "Sprint Planning - Sprint Goal

   What is the ONE primary objective for this sprint?
   (Example: 'Complete user authentication system')

   Sprint Goal: [User input]

   Define 2-3 success criteria:
   1. [User input]
   2. [User input]
   3. [User input]
   "
   ```

3. **Issue Selection Confirmation**:
   ```
   "Recommended Sprint Scope:

   Based on capacity of [X] points, I recommend these [Y] issues:

   [List of issues with titles and points]

   Total: [Z] points ([P]% of capacity)

   Options:
   1. Proceed with this scope
   2. Add more issues (will show next highest priority)
   3. Remove issues (will ask which ones)
   4. Manual selection (interactive selection)

   Choice: [User input]
   "
   ```

## Error Handling

### No Open Issues
```
❌ Error: No open issues found in repository.

Sprint planning requires open issues in the backlog.

Next steps:
1. Create issues for work that needs to be done
2. Ensure issues have clear descriptions and acceptance criteria
3. Run /project-manager:plan-sprint again
```

### GitHub CLI Not Available
```
❌ Error: GitHub CLI (gh) not found or not authenticated.

Please install and authenticate:
1. Install: https://cli.github.com/
2. Authenticate: gh auth login
3. Run /project-manager:plan-sprint again
```

### Invalid Sprint Name
```
❌ Error: Sprint name "$1" contains invalid characters.

Sprint names should:
- Use lowercase-hyphens or numbers
- Examples: "sprint-6", "2025-03-sprint-01", "iteration-15"
- Avoid: Spaces, special characters (except hyphens)

Usage: /project-manager:plan-sprint [valid-sprint-name]
```

### Insufficient Backlog
```
⚠️  Warning: Only [X] story points in backlog, but capacity is [Y] points.

Options:
1. Proceed with available work ([X] points)
2. Create more issues to fill sprint
3. Reduce sprint duration
4. Cancel planning

Recommendation: Create more issues or adjust sprint length.
```

## Output Format

```markdown
✅ Sprint Planned Successfully!

📋 Sprint: [Sprint Name]
📅 Dates: [Start Date] - [End Date]
🎯 Goal: [Sprint Goal]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Sprint Metrics:
- Team Size: [X] people
- Duration: [Y] days
- Capacity: [Z] story points
- Committed: [W] story points ([P]% utilization)

📦 Sprint Scope:
- [N] issues selected
- Features: [X] points ([Y]%)
- Bugs: [X] points ([Y]%)
- Tech Debt: [X] points ([Y]%)

🔗 Resources:
- Project Board: [GitHub Project URL]
- Sprint Plan: .claude-project/sprints/[sprint-name]-plan.md
- Tracking Docs: .claude-project/sprints/[sprint-name]/

⚠️  Identified Risks:
- [Risk 1]
- [Risk 2]

📝 Next Steps:
1. Review sprint plan with team
2. Conduct sprint kickoff meeting
3. Begin work on highest priority items
4. Update board daily

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sprint planning completed in [X] seconds.
```

## Advanced Features

### Integration with Existing Sprints
- Automatically references past sprint data for velocity
- Compares current scope to historical averages
- Warns if capacity utilization is unusual

### Dependency Detection
- Identifies issues that block other issues
- Ensures blocking work is included in sprint
- Recommends sequencing of dependent work

### Smart Recommendations
- Suggests sprint composition based on project phase
- Recommends buffer percentage based on team maturity
- Identifies quick wins for momentum

### Retrospective Integration
- If previous sprint has retrospective notes
- Incorporates action items into current sprint planning
- Tracks improvement over time
