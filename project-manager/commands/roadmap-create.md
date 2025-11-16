---
description: Creates strategic roadmaps (quarterly or annual) by analyzing goals, prioritizing initiatives, mapping dependencies, and generating comprehensive roadmap documents
allowed-tools: Bash, Read, Write, Grep, Glob, Task
argument-hint: "[timeframe] [roadmap-name]"
---

# Create Roadmap Command

Facilitates strategic roadmap creation for quarters or years by gathering strategic goals, analyzing projects, prioritizing initiatives, mapping dependencies, allocating resources, and generating comprehensive roadmap documentation.

## Arguments

- **`$1`**: Timeframe (required)
  - `q1`, `q2`, `q3`, `q4` - Quarterly roadmaps
  - `2025-q1`, `2025-q2` - Specific quarter with year
  - `annual`, `2025`, `2026` - Annual roadmaps
  - `6-months`, `12-months` - Custom timeframes

- **`$2`**: Roadmap name (optional, auto-generated if not provided)
  - Custom name for the roadmap
  - Default: auto-generated from timeframe

## Workflow

When this command is invoked with `/project-manager:roadmap-create [timeframe] [name]`:

### Phase 1: Context Gathering

1. **Invoke coordinating-projects Skill**:
   - Automatically activates for strategic roadmap planning
   - Provides roadmap frameworks and best practices

2. **Determine Roadmap Scope**:
   - Parse timeframe from `$1`
   - Calculate start and end dates
   - Determine planning horizon

3. **Gather Strategic Context**:
   - Prompt user for:
     - Company/team goals for period
     - OKRs (Objectives and Key Results)
     - Strategic priorities
     - Known constraints

4. **Discover Active Projects**:
   ```bash
   # List all repositories if multi-project
   gh repo list [org] --limit 100 --json name,description,url

   # Or analyze current repository
   gh repo view --json name,description,topics

   # List all open issues and epics
   gh issue list --limit 500 --json number,title,labels,milestone
   ```

5. **Review Existing Roadmaps** (if any):
   ```bash
   # Check for previous roadmaps
   ls .claude-project/roadmaps/

   # Read most recent for context
   cat .claude-project/roadmaps/[previous]-roadmap.md
   ```

### Phase 2: Strategic Analysis

6. **Identify Themes & Initiatives**:
   - Group work into strategic themes
   - Examples:
     - Developer Experience
     - Performance & Scale
     - Security & Compliance
     - Technical Debt
     - New Features

7. **Map Goals to Projects**:
   - For each strategic goal/OKR:
     - Identify projects that support it
     - Estimate effort and timeline
     - Assess strategic value

8. **Prioritize Initiatives**:
   - Apply strategic prioritization (delegate to coordinating-projects skill)
   - Consider:
     - Strategic alignment (supports OKRs?)
     - Business value (revenue, retention, acquisition)
     - Dependencies (what must come first?)
     - Resource availability
     - Risk vs opportunity

9. **Research Unknowns**:
   - For initiatives with unclear complexity:
     ```markdown
     Delegate to investigator:
     "Research [technology/approach] for [initiative] to estimate complexity and identify risks"
     ```

### Phase 3: Resource Allocation

10. **Calculate Available Capacity**:
    - Team size and composition
    - Timeframe duration
    - Account for:
      - Maintenance/support (15-25%)
      - Technical debt (10-20%)
      - Unplanned work buffer (10-15%)
      - PTO, holidays, training

11. **Allocate Resources to Themes**:
    - Percentage-based allocation
    - Example for Q2:
      - Developer Experience: 40%
      - Performance: 25%
      - Security: 20%
      - Tech Debt: 15%

12. **Balance Portfolio**:
    - Quick wins vs long-term investments
    - Innovation vs optimization
    - Customer-facing vs internal
    - Risk distribution

### Phase 4: Timeline & Milestones

13. **Create Monthly/Quarterly Milestones**:
    - Break timeframe into periods
    - Assign initiatives to periods
    - Identify dependencies and sequence

14. **Map Critical Path**:
    - Identify longest chain of dependencies
    - Calculate minimum timeline
    - Identify opportunities for parallelization

15. **Define Success Metrics**:
    - For each initiative:
      - Clear deliverables
      - Success criteria
      - Measurable outcomes

### Phase 5: Dependency & Risk Analysis

16. **Map Dependencies**:
    - Technical dependencies (A needs B's API)
    - Resource dependencies (same engineer needed)
    - External dependencies (vendor, partner, approval)

17. **Identify Risks**:
    - Technical risks (unknowns, complexity)
    - Resource risks (hiring, retention)
    - Dependency risks (external blockers)
    - Market risks (competition, timing)

18. **Create Mitigation Plans**:
    - For each high-impact risk:
      - Mitigation strategy
      - Contingency plan
      - Owner and timeline

### Phase 6: Documentation & Artifacts

19. **Generate Roadmap Document**:
    - Use template from coordinating-projects skill:
      ```bash
      cp coordinating-projects/templates/[quarterly|annual]-roadmap-template.md .claude-project/roadmaps/$1-roadmap.md
      ```

    - Fill in comprehensive roadmap:
      - Executive summary
      - Strategic goals and OKRs
      - Themes and initiatives
      - Timeline and milestones
      - Resource allocation
      - Dependencies and risks
      - Success metrics

20. **Create Supporting Artifacts**:
    ```bash
    # Dependency map
    cp coordinating-projects/templates/dependency-map-template.md .claude-project/roadmaps/$1-dependencies.md

    # Initiative briefs (for each major initiative)
    mkdir -p .claude-project/roadmaps/$1-initiatives/
    ```

21. **Create GitHub Artifacts** (optional):
    - Delegate to workflow-orchestrator:
      ```markdown
      "Create milestones for roadmap periods"
      "Create project boards for each theme"
      "Create epic issues for initiatives"
      ```

### Phase 7: Validation & Finalization

22. **Quality Check**:
    - Optionally delegate to self-critic:
      ```markdown
      "Review this roadmap for:
      - Strategic alignment
      - Realistic scope
      - Clear priorities
      - Risk coverage
      - Completeness"
      ```

23. **Generate Summary Report**:
    - Timeframe and dates
    - Number of themes/initiatives
    - Resource allocation breakdown
    - Key milestones
    - Top risks identified
    - Links to all artifacts

## Examples

### Example Usage 1: Quarterly Roadmap
```
/project-manager:roadmap-create 2025-q2
```

Expected behavior:
1. Prompts for Q2 2025 goals and OKRs
2. Analyzes all projects and issues
3. Groups into strategic themes
4. Prioritizes initiatives
5. Creates monthly milestones
6. Maps dependencies
7. Generates comprehensive Q2 roadmap
8. Creates GitHub milestones

Output:
```markdown
✅ Q2 2025 Roadmap Created!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 Timeframe: Q2 2025 (Apr 1 - Jun 30)
🎯 Strategic Objective: Expand enterprise segment

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 THEMES & ALLOCATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Enterprise Readiness (40%)
   - Multi-tenancy support
   - SSO integration
   - Audit logging
   - Admin dashboard

2. Developer Experience (35%)
   - CLI tool redesign
   - Documentation platform
   - Onboarding automation

3. Technical Foundation (25%)
   - Microservices migration
   - Observability platform
   - Performance optimization

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 MILESTONES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

April 2025:
- ✓ Multi-tenancy Phase 1 (50% complete)
- ✓ CLI redesign complete
- ✓ SSO integration complete

May 2025:
- □ Multi-tenancy Phase 2 complete
- □ Documentation platform Beta
- □ Observability platform setup

June 2025:
- □ Audit logging complete
- □ Admin dashboard v1
- □ Performance optimization done

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Initiatives: 9 total
- Large (>8 weeks): 3
- Medium (4-8 weeks): 4
- Small (<4 weeks): 2

Resource Allocation:
- Engineering: 12 people
- Design: 2 people
- Product: 2 people

Expected Outcomes:
- 10 enterprise customers onboarded
- Developer satisfaction: 4.5+ / 5
- System uptime: 99.9%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  KEY RISKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Multi-tenancy migration complexity
   Mitigation: Phase approach, extensive testing

2. Resource constraint (Design team)
   Mitigation: Hire 1 contractor for Q2

3. SSO vendor integration delays
   Mitigation: Start early, have fallback plan

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 ARTIFACTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Roadmap Document: .claude-project/roadmaps/2025-q2-roadmap.md
Dependencies: .claude-project/roadmaps/2025-q2-dependencies.md
Initiative Briefs: .claude-project/roadmaps/2025-q2-initiatives/

GitHub Artifacts:
- Milestones: April, May, June 2025
- Project Boards: 3 theme boards created
- Epic Issues: 9 epics created

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Review roadmap with leadership team
2. Socialize with all engineering teams
3. Begin April sprint planning from roadmap
4. Set up tracking dashboards
5. Schedule monthly roadmap check-ins

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Roadmap creation completed!
```

### Example Usage 2: Annual Roadmap
```
/project-manager:roadmap-create 2025 "2025 Product Vision"
```

Expected behavior:
1. Prompts for 2025 annual goals
2. Creates high-level yearly themes
3. Breaks into quarterly phases
4. Maps major initiatives
5. Generates annual roadmap document

Output:
```markdown
✅ 2025 Annual Roadmap Created!

📅 Timeframe: 2025 (Jan - Dec)
📋 Name: "2025 Product Vision"

Quarterly Breakdown:

Q1 2025: Foundation
- Core platform stability
- Technical debt reduction
- Team growth

Q2 2025: Enterprise Features
- Multi-tenancy
- Advanced security
- Admin capabilities

Q3 2025: Scale & Performance
- Infrastructure optimization
- Global deployment
- Performance improvements

Q4 2025: Innovation & Growth
- AI/ML features
- Mobile experience
- Partner ecosystem

Full roadmap: .claude-project/roadmaps/2025-roadmap.md
```

### Example Usage 3: Custom Timeframe
```
/project-manager:roadmap-create 6-months "H1 2025 Roadmap"
```

Expected behavior:
1. Creates 6-month roadmap (next 6 months from today)
2. Uses custom name "H1 2025 Roadmap"
3. Generates artifacts accordingly

## Important Notes

### Prerequisites
- Clear understanding of strategic goals (will prompt if not available)
- Visibility into all active projects
- Recommended: Past roadmap for context

### Delegation Points
This command delegates to:
- **coordinating-projects skill**: Auto-invokes for roadmap expertise
- **investigator**: (Optional) For researching unknowns
- **workflow-orchestrator**: For creating GitHub artifacts
- **self-critic**: (Optional) For roadmap quality validation

### State Changes
- Creates roadmap documents in `.claude-project/roadmaps/`
- May create GitHub milestones (via delegation)
- May create project boards (via delegation)
- May create epic issues (via delegation)

### Roadmap Types

**Quarterly (Recommended)**:
- Detailed and actionable
- Monthly milestones
- Specific initiatives with owners
- Best for tactical planning

**Annual**:
- High-level strategic themes
- Quarterly phases
- Major initiatives only
- Best for strategic direction

**Custom (6-12 months)**:
- Flexible timeframe
- Mix of strategic and tactical
- Useful for specific initiatives

### Collaborative Process
This command is designed to be interactive:
- Prompts for strategic input
- Asks for prioritization decisions
- Requests resource information
- Validates assumptions

## Interactive Prompts

### Strategic Goals
```
"Roadmap Creation - Strategic Goals

What are the primary strategic goals for [timeframe]?

Examples:
- Expand into enterprise market
- Improve developer experience
- Achieve 99.99% uptime
- Launch mobile app

Enter goals (one per line, blank line to finish):
> [User input]
> [User input]
> [User input]
>
"
```

### OKR Definition (Optional)
```
"Would you like to define OKRs (Objectives & Key Results)? [y/n]

If yes, for each goal:
Objective: [User input]

Key Results:
1. [User input]
2. [User input]
3. [User input]
"
```

### Resource Allocation
```
"Resource Allocation for [timeframe]

Total Team Capacity:
- Engineering: [X] people
- Design: [Y] people
- Product: [Z] people

How should capacity be allocated across themes?

Theme 1: [Name] - [%]
Theme 2: [Name] - [%]
Theme 3: [Name] - [%]
Theme 4: [Name] - [%]

(Should total 100%)
"
```

### Milestone Definition
```
"Milestone Planning

For [Month 1]:
- What should be completed by end of month?
- [User input]

For [Month 2]:
- What should be completed by end of month?
- [User input]

For [Month 3]:
- What should be completed by end of month?
- [User input]
"
```

## Error Handling

### Invalid Timeframe
```
❌ Error: Invalid timeframe "$1"

Valid timeframes:
- Quarterly: q1, q2, q3, q4, 2025-q2
- Annual: 2025, 2026, annual
- Custom: 6-months, 12-months

Usage: /project-manager:roadmap-create [timeframe] [optional-name]
Examples:
- /project-manager:roadmap-create 2025-q3
- /project-manager:roadmap-create 2025 "Annual Vision"
```

### No Strategic Context
```
⚠️  No Strategic Goals Provided

Creating a roadmap requires clear strategic goals.

Options:
1. Enter goals interactively now
2. Read goals from existing document (provide path)
3. Use template goals (generic, will need customization)

Without goals, roadmap will be tactical only (not strategic).

Proceed? [1/2/3/cancel]
```

### Conflicting Existing Roadmap
```
⚠️  Existing Roadmap Found

A roadmap for [timeframe] already exists:
.claude-project/roadmaps/[existing]-roadmap.md

Options:
1. Update existing roadmap (merge new input)
2. Create new version (archive old one)
3. Cancel and review existing first

Choice: [1/2/3]
```

## Output Format

```markdown
✅ Roadmap Created Successfully!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 ROADMAP OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Timeframe: [Timeframe]
Name: [Roadmap Name]
Created: [Date]
Planning Horizon: [X] months/weeks

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 STRATEGIC OBJECTIVES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. [Goal 1]
   Key Results:
   - [KR 1.1]
   - [KR 1.2]

2. [Goal 2]
   Key Results:
   - [KR 2.1]
   - [KR 2.2]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 STRATEGIC THEMES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Theme 1: [Name] ([X]% capacity)
- [Initiative 1.1] ([timeline])
- [Initiative 1.2] ([timeline])

Theme 2: [Name] ([Y]% capacity)
- [Initiative 2.1] ([timeline])

[...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 TIMELINE & MILESTONES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Period 1]:
✓ [Milestone 1.1]
✓ [Milestone 1.2]

[Period 2]:
□ [Milestone 2.1]
□ [Milestone 2.2]

[Period 3]:
□ [Milestone 3.1]
□ [Milestone 3.2]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 RESOURCE ALLOCATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Capacity: [X] person-months

By Theme:
- [Theme 1]: [X]% ([Y] person-months)
- [Theme 2]: [X]% ([Y] person-months)
- [...]

By Type:
- Strategic Projects: [X]%
- Maintenance: [Y]%
- Tech Debt: [Z]%
- Buffer: [W]%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 DEPENDENCIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Critical Path: [Initiative A] → [Initiative B] → [Initiative C]
Timeline: [X] months

Dependency Highlights:
- [Initiative X] blocks [Initiative Y]
- [Initiative Z] requires external vendor

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  RISKS & MITIGATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

High Priority Risks:
1. [Risk description]
   Impact: [description]
   Mitigation: [strategy]
   Owner: [person/team]

2. [Risk description]
   Impact: [description]
   Mitigation: [strategy]
   Owner: [person/team]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SUCCESS METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Completion Targets:
- [X]% of initiatives delivered on time
- [Y]% of OKR key results achieved
- [Z] customer/user impact metrics hit

Quality Metrics:
- System uptime: [target]
- Developer satisfaction: [target]
- Performance: [target]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 ARTIFACTS & LINKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Documents:
- 📄 Roadmap: .claude-project/roadmaps/[name]-roadmap.md
- 📄 Dependencies: .claude-project/roadmaps/[name]-dependencies.md
- 📁 Initiatives: .claude-project/roadmaps/[name]-initiatives/

GitHub:
- 📌 Milestones: [X] created
- 📊 Project Boards: [Y] created
- 📋 Epic Issues: [Z] created

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Immediate:
1. Review roadmap with stakeholders
2. Validate resource allocations
3. Confirm milestones and dates

Next Week:
1. Socialize with all teams
2. Begin breaking down initiatives
3. Start first sprint planning

Ongoing:
1. Monthly roadmap reviews
2. Quarterly roadmap updates
3. Track progress against metrics

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎉 Roadmap creation completed successfully!

Use /project-manager:project-status to track progress.
Use /project-manager:plan-sprint to execute initiatives.
```

## Advanced Features

### Roadmap Comparison
- Compare to previous roadmaps
- Identify scope changes
- Track strategic shifts

### Impact Analysis
- Estimate customer/user impact for each initiative
- Prioritize based on impact
- Track actual vs projected impact

### Capacity Modeling
- What-if scenarios for resource changes
- Adjust roadmap based on hiring plans
- Model team growth impact

### Integration with Sprint Planning
- Link roadmap initiatives to sprints
- Track sprint contributions to roadmap
- Ensure tactical work aligns with strategy

### Version Control
- Roadmaps are versioned documents
- Track changes over time
- Understand evolution of strategy
