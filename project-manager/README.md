# Project Manager Plugin

**Strategic project coordination and planning plugin** for Claude Code that orchestrates multi-agent workflows, manages sprints and roadmaps, coordinates tasks across projects, and delegates execution to specialized agents.

## Overview

The project-manager plugin provides a comprehensive project management layer that sits above tactical execution plugins. It handles strategic planning, coordinates work across multiple projects, intelligently delegates tasks to specialized agents, and maintains project context throughout development lifecycles.

### Key Concept

**Orchestrate, Don't Execute**: This plugin focuses on planning and coordination, delegating tactical execution to specialized plugins:
- **github-workflows**: For GitHub operations (issues, PRs, boards, commits)
- **research-agent**: For codebase research and best practices
- **self-improvement**: For quality validation and critique
- **agent-builder**: For creating custom automation

## Components

### 1 Agent: `project-coordinator`

Strategic planning and orchestration agent that manages project lifecycles and delegates to specialized agents.

**Invoke directly**:
```bash
# Use Task tool in conversations
Task → project-coordinator: "Plan our Q2 roadmap and create sprint boards"
```

**Capabilities**:
- Sprint planning and backlog management
- Multi-project coordination
- Task delegation and routing
- Roadmap creation and strategic planning
- Progress tracking and reporting
- Dependency management

### 2 Skills

#### `planning-sprints`
Auto-activates for sprint planning, backlog refinement, and iteration management.

**Triggers**: sprint planning, backlog, velocity, story points, iteration
**Provides**: RICE/MoSCoW prioritization, capacity planning, velocity tracking

#### `coordinating-projects`
Auto-activates for multi-project coordination, strategic planning, and portfolio management.

**Triggers**: multi-project, roadmap, OKRs, resource allocation, portfolio
**Provides**: Roadmap frameworks, dependency mapping, resource optimization

### 5 Commands

#### `/project-manager:plan-sprint [sprint-name]`
Interactive sprint planning workflow.
```bash
# Plan next sprint
/project-manager:plan-sprint

# Plan specific sprint
/project-manager:plan-sprint Sprint-6
```

**What it does**:
- Analyzes backlog and prioritizes issues
- Calculates team capacity
- Creates sprint plan document
- Sets up GitHub Project board
- Delegates board creation to workflow-orchestrator

#### `/project-manager:prioritize-backlog [framework]`
Analyzes and prioritizes entire backlog.
```bash
# Use RICE framework (default)
/project-manager:prioritize-backlog

# Use MoSCoW method
/project-manager:prioritize-backlog moscow

# Interactive selection
/project-manager:prioritize-backlog interactive
```

**What it does**:
- Applies prioritization framework (RICE, MoSCoW, WSJF, Value-Effort)
- Updates GitHub labels
- Reorganizes project boards
- Identifies issues ready for sprint

#### `/project-manager:project-status [project-name]`
Comprehensive project health check.
```bash
# Check current project
/project-manager:project-status

# Check specific repository
/project-manager:project-status my-org/api-service
```

**What it does**:
- Analyzes sprint progress
- Tracks velocity and trends
- Identifies blockers and risks
- Provides data-driven recommendations

#### `/project-manager:delegate-task [task-description]`
Intelligently routes tasks to appropriate agents.
```bash
# Route PR review
/project-manager:delegate-task Review PR #123 for quality

# Route research
/project-manager:delegate-task Research best authentication patterns

# Route triage
/project-manager:delegate-task Triage all open issues
```

**What it does**:
- Analyzes task type
- Selects best agent (workflow-orchestrator, investigator, self-critic, meta-architect)
- Delegates via Task tool
- Reports results

#### `/project-manager:roadmap-create [timeframe] [name]`
Creates strategic roadmaps.
```bash
# Quarterly roadmap
/project-manager:roadmap-create 2025-q2

# Annual roadmap
/project-manager:roadmap-create 2025 "2025 Product Vision"

# Custom timeframe
/project-manager:roadmap-create 6-months
```

**What it does**:
- Gathers strategic goals and OKRs
- Prioritizes initiatives
- Maps dependencies and risks
- Creates roadmap documents
- Sets up GitHub milestones

### 1 Hook

**project-planning-awareness** (PostToolUse):
Triggers when project planning files are modified (sprint plans, roadmaps, backlog docs), suggesting coordination actions.

## Installation

```bash
# Install from marketplace (when published)
claude plugin install project-manager

# Or install from local directory
ln -s $(pwd)/project-manager ~/.claude/plugins/project-manager
```

### Prerequisites

**Required**:
- GitHub CLI (`gh`) installed and authenticated
- Git repository context

**Recommended Plugins** (for full functionality):
- `github-workflows` - For GitHub operations
- `research-agent` - For research and investigation
- `self-improvement` - For quality checks
- `agent-builder` - For custom automation

## Quick Start

### 1. Plan Your First Sprint

```bash
/project-manager:plan-sprint Sprint-1
```

This will:
1. Prompt for team capacity and sprint goal
2. Analyze your backlog
3. Recommend issues based on priority
4. Create sprint plan document
5. Set up GitHub Project board

### 2. Check Project Status

```bash
/project-manager:project-status
```

This provides:
- Sprint progress metrics
- Issue and PR status
- Blocker analysis
- Velocity trends
- Recommendations

### 3. Delegate a Task

```bash
/project-manager:delegate-task Review PR #42 for security
```

The coordinator will:
1. Determine task needs pr-reviewer
2. Delegate to github-workflows plugin
3. Report review results

## Usage Examples

### Sprint Planning Workflow

```bash
# 1. Check current status
/project-manager:project-status

# 2. Prioritize backlog (if needed)
/project-manager:prioritize-backlog

# 3. Plan next sprint
/project-manager:plan-sprint

# 4. During sprint: monitor progress
/project-manager:project-status
```

### Quarterly Planning Workflow

```bash
# 1. Create quarterly roadmap
/project-manager:roadmap-create 2025-q2

# 2. Break down into sprints
/project-manager:plan-sprint Sprint-6
/project-manager:plan-sprint Sprint-7
/project-manager:plan-sprint Sprint-8

# 3. Track progress
/project-manager:project-status
```

### Task Delegation Examples

```bash
# GitHub operations
/project-manager:delegate-task Create project board for microservices migration

# Research tasks
/project-manager:delegate-task How does our authentication system work?

# Quality tasks
/project-manager:delegate-task Validate this sprint plan for completeness

# Automation tasks
/project-manager:delegate-task Create command for deployment automation
```

## Integration with Other Plugins

### github-workflows Integration

The project-manager coordinates with github-workflows for tactical GitHub operations:

```bash
# Project-manager plans, github-workflows executes
/project-manager:plan-sprint Sprint-5
  → Delegates to /github-workflows:project-create
  → Delegates to /github-workflows:project-sync

/project-manager:prioritize-backlog
  → Delegates to /github-workflows:issue-triage
  → Delegates to /github-workflows:label-sync
```

### research-agent Integration

The project-manager delegates research to investigator:

```bash
/project-manager:delegate-task Research GraphQL vs REST for our API
  → Delegates to investigator (research-agent)
  → Returns research findings
```

### self-improvement Integration

The project-manager uses self-critic for quality validation:

```bash
/project-manager:roadmap-create 2025-q3
  → Creates roadmap
  → Delegates to self-critic for quality check
  → Returns validated roadmap
```

## Advanced Workflows

### Multi-Project Coordination

Coordinate releases across multiple projects:

```bash
/project-manager:delegate-task Coordinate deployment of API, Web, and Mobile apps
```

The coordinator will:
1. Analyze dependencies between projects
2. Create release sequence plan
3. Delegate individual deployments to workflow-orchestrator
4. Track progress across all projects

### Strategic Initiative Planning

Plan and track large initiatives:

```bash
# 1. Research best approach
/project-manager:delegate-task Research microservices architecture patterns

# 2. Create roadmap
/project-manager:roadmap-create 2025 "Microservices Migration"

# 3. Break into sprints
/project-manager:plan-sprint Microservices-Sprint-1

# 4. Track progress
/project-manager:project-status
```

### Resource Allocation

Optimize team allocation:

```bash
# Check current status across all projects
/project-manager:project-status all

# Delegate resource reallocation decision
/project-manager:delegate-task Recommend resource allocation for 2 new engineers
```

## Configuration

### Sprint Planning Defaults

Customize sprint planning behavior in sprint plans:

```markdown
# Default sprint duration
sprint_duration: 10 days  # 2-week sprint

# Default capacity buffer
capacity_buffer: 20%  # Reserve 20% for unknowns

# Default sprint composition
sprint_composition:
  features: 65%
  bugs: 20%
  tech_debt: 15%
```

### Prioritization Framework

Choose default prioritization method:

```bash
# Use RICE (default)
/project-manager:prioritize-backlog rice

# Use MoSCoW
/project-manager:prioritize-backlog moscow

# Use WSJF (for SAFe)
/project-manager:prioritize-backlog wsjf
```

## Best Practices

### Sprint Planning
1. **Groom backlog first**: Run `/project-manager:prioritize-backlog` before sprint planning
2. **Don't overcommit**: Use 80% of calculated capacity, not 100%
3. **Define clear sprint goals**: One focused objective per sprint
4. **Review velocity**: Check past sprints for realistic planning

### Backlog Management
1. **Prioritize regularly**: Weekly backlog reviews
2. **Keep items ready**: Top 20 issues should be well-defined
3. **Remove stale items**: Archive issues >6 months old
4. **Use frameworks consistently**: Pick one prioritization method and stick with it

### Roadmap Planning
1. **Align with business goals**: Every initiative supports clear objectives
2. **Balance portfolio**: Mix quick wins, strategic bets, and technical foundation
3. **Review quarterly**: Adjust roadmap based on learnings
4. **Track dependencies proactively**: Don't discover them mid-sprint

### Task Delegation
1. **Be specific**: Clear task descriptions get better results
2. **Trust specialized agents**: They know their domains
3. **Chain when needed**: Complex tasks may need multiple agents
4. **Review results**: Always validate delegated work

## Troubleshooting

### Sprint Planning Issues

**Problem**: No issues in backlog
```
Solution: Create issues first, then run /project-manager:plan-sprint
```

**Problem**: Can't calculate velocity
```
Solution: Normal for first sprint. Estimate conservatively (5-6 hours/person/day)
```

### Delegation Issues

**Problem**: Agent not available
```
Solution: Install required plugin (github-workflows, research-agent, etc.)
```

**Problem**: Task routing unclear
```
Solution: Be more specific in task description or use direct agent invocation
```

### GitHub Integration Issues

**Problem**: Can't create boards/issues
```
Solution: Ensure `gh` CLI is installed and authenticated
Run: gh auth login
```

## File Structure

```
project-manager/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── agents/
│   └── project-coordinator.md # Strategic coordination agent
├── skills/
│   ├── planning-sprints/     # Sprint planning expertise
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   ├── references/
│   │   └── templates/
│   └── coordinating-projects/ # Multi-project coordination
│       ├── SKILL.md
│       ├── scripts/
│       ├── references/
│       └── templates/
├── commands/
│   ├── plan-sprint.md        # Sprint planning command
│   ├── prioritize-backlog.md # Backlog prioritization command
│   ├── project-status.md     # Health check command
│   ├── delegate-task.md      # Task routing command
│   └── roadmap-create.md     # Roadmap creation command
├── hooks/
│   └── hooks.json           # Project file awareness hook
└── README.md               # This file
```

## Artifacts Created

When you use this plugin, it creates structured artifacts:

```
.claude-project/
├── sprints/
│   ├── Sprint-1-plan.md      # Sprint plan documents
│   ├── Sprint-2-plan.md
│   └── Sprint-3/
│       ├── daily-notes.md
│       ├── blockers.md
│       └── retrospective.md
├── roadmaps/
│   ├── 2025-q1-roadmap.md    # Quarterly roadmaps
│   ├── 2025-q2-roadmap.md
│   ├── 2025-roadmap.md       # Annual roadmap
│   └── 2025-q2-initiatives/  # Initiative details
│       ├── initiative-1.md
│       └── initiative-2.md
├── backlog-analysis-2025-03-15.md  # Prioritization reports
└── status-reports/
    ├── status-2025-03-10.md  # Health check reports
    └── status-2025-03-17.md
```

## Metrics & Success Criteria

The project-manager plugin helps you achieve:

- ✅ **Predictable velocity**: 90%+ sprint completion rate
- ✅ **Clear priorities**: Backlog always organized by value
- ✅ **Strategic alignment**: All work tied to roadmap goals
- ✅ **Efficient coordination**: Tasks routed to right agents
- ✅ **Visibility**: Clear status at all times
- ✅ **Proactive planning**: Blockers identified early

## Contributing

This plugin is part of the claude-code-plugin-automations repository.

To contribute:
1. Fork the repository
2. Create feature branch
3. Make changes
4. Run validation: `bash validate-all.sh`
5. Submit pull request

## License

MIT License - See repository root for details

## Support

- Issues: https://github.com/anthropics/claude-code-plugin-automations/issues
- Discussions: https://github.com/anthropics/claude-code-plugin-automations/discussions
- Documentation: https://code.claude.com/docs

## Version History

### 1.0.0 (Initial Release)
- project-coordinator agent for strategic planning
- planning-sprints skill for sprint management
- coordinating-projects skill for multi-project coordination
- 5 commands: plan-sprint, prioritize-backlog, project-status, delegate-task, roadmap-create
- project-planning-awareness hook
- Full integration with github-workflows, research-agent, self-improvement, agent-builder

---

**Made with Claude Code** - Building tools for Claude, by Claude.
