# GitHub Conventions Guide

This document defines conventions for project status management, label usage, issue naming, and hierarchical work organization.

## Table of Contents

1. [Project Board Status Transitions](#project-board-status-transitions)
2. [Label Conventions](#label-conventions)
3. [Issue Naming Guidelines](#issue-naming-guidelines)
4. [Phase and Epic Structure](#phase-and-epic-structure)
5. [Feature Branch Tracking](#feature-branch-tracking)

---

## Project Board Status Transitions

### Available Statuses

| Status | Description | Entry Criteria | Exit Criteria |
|--------|-------------|----------------|---------------|
| **Backlog** | Unscheduled, unrefined work | Issue created | Refined and ready to schedule |
| **Todo** | Ready to start, hasn't been started | Refined, requirements clear | Work begins |
| **In Progress** | Actively being worked on | Developer assigned and working | Work complete or paused |
| **On Hold** | Paused, not being actively progressed | Intentionally paused (deprioritized, waiting for decision) | Decision made, work resumes |
| **Blocked** | Cannot proceed due to internal dependency | Blocked by another issue/PR in this repo | Blocker resolved |
| **Pending** | Awaiting external factor | Waiting on external team, third-party, or user input | External factor resolved |
| **In Review** | Awaiting internal review | PR created or review requested | Review approved or changes requested |
| **Done** | Completed | Merged/closed and verified | - |
| **Cancelled** | Will not be done | Decision to not proceed | - |

### Status Transition Rules

```
                                    ┌──────────┐
                                    │ Cancelled│
                                    └────▲─────┘
                                         │ won't do
┌─────────┐    refine     ┌──────┐  start  ┌─────────────┐
│ Backlog │ ─────────────►│ Todo │ ───────►│ In Progress │
└─────────┘               └──┬───┘         └──────┬──────┘
                             │                    │
                    ┌────────┼────────┬───────────┼──────────┐
                    │        │        │           │          │
                    ▼        ▼        ▼           ▼          ▼
              ┌─────────┐ ┌───────┐ ┌─────────┐ ┌─────────┐ ┌──────┐
              │ On Hold │ │Blocked│ │ Pending │ │In Review│ │ Done │
              └────┬────┘ └───┬───┘ └────┬────┘ └────┬────┘ └──────┘
                   │          │          │           │
                   └──────────┴──────────┴───────────┘
                              │ resolved
                              ▼
                    ┌─────────────────┐
                    │  Todo or        │
                    │  In Progress    │
                    └─────────────────┘
```

### When to Update Status

#### Backlog → Todo
- **Trigger**: Issue is refined and ready to be worked on
- **Requirements**:
  - Clear acceptance criteria defined
  - No known blocking dependencies
  - Priority label assigned
- **Action**: Move issue to Todo column in project board

#### Todo → In Progress
- **Trigger**: Developer starts working on issue
- **Requirements**:
  - Assignee set
  - Branch created (if code change)
- **Action**: Move issue to In Progress column in project board

#### In Progress → In Review
- **Trigger**: Work complete, ready for peer review
- **Requirements**:
  - PR created and linked
  - All tests passing
  - Self-review complete
- **Action**: Move issue to In Review column in project board

#### In Review → Done
- **Trigger**: Review approved and merged
- **Requirements**:
  - All review comments addressed
  - CI/CD passing
  - Merged to main (or closed as resolved)
- **Action**: Move issue to Done column in project board

#### Any → Blocked
- **Trigger**: Cannot proceed due to internal dependency (another issue/PR in this repo)
- **Requirements**:
  - Document blocking reason in comment
  - Link to blocking issue/PR
- **Action**: Move issue to Blocked column in project board
- **Return**: When blocker is resolved, return to previous status (usually Todo or In Progress)

#### Any → Pending
- **Trigger**: Awaiting external factor (external team, third-party service, user input)
- **Requirements**:
  - Document what external factor is needed
  - Set reminder or follow-up date if possible
- **Action**: Move issue to Pending column in project board
- **Return**: When external factor resolved, return to previous status

#### Any → On Hold
- **Trigger**: Work intentionally paused (not blocked, just deprioritized)
- **Requirements**:
  - Document reason for hold
  - Note conditions for resumption
- **Action**: Move issue to On Hold column in project board
- **Return**: When ready to resume, return to Todo

#### Any → Cancelled
- **Trigger**: Decision made to not complete this work
- **Requirements**:
  - Document reason for cancellation
  - Close the issue
- **Action**: Move issue to Cancelled column in project board

---

## Label Conventions

### Core Principles

1. **Labels describe categories, not titles** - Don't repeat label information in the issue title
2. **One label per dimension** - Use one type, one priority, etc.
3. **Labels are searchable** - Use for filtering and automation
4. **Titles are readable** - Use for human understanding

### Label Categories

#### Type Labels (What is it?) - REQUIRED
| Label | Use When |
|-------|----------|
| `bug` | Something isn't working as expected |
| `enhancement` | Improving existing functionality |
| `feature` | Adding new functionality |
| `documentation` | Documentation changes only |
| `refactor` | Code improvement without behavior change |
| `chore` | Maintenance tasks (dependencies, CI, etc.) |

#### Priority Labels (How urgent?) - REQUIRED for open issues
| Label | Use When |
|-------|----------|
| `priority:high` | Critical path, blocking others, security issue |
| `priority:medium` | Important but not blocking, should do this sprint |
| `priority:low` | Nice to have, can defer |

#### Scope Labels (What area?)
| Label | Use When |
|-------|----------|
| `plugin` | Plugin-specific functionality |
| `plugin:agent-builder` | Agent-builder plugin specific |
| `plugin:self-improvement` | Self-improvement plugin specific |
| `plugin:github-workflows` | GitHub-workflows plugin specific |
| `plugin:testing-expert` | Testing-expert plugin specific |

#### Feature Branch Labels (What branch?)

Use branch labels to track which issues relate to specific feature branches. Create labels as needed for active branches.

**Format**: `branch:<branch-name>`

**Examples**:
| Label | Use When |
|-------|----------|
| `branch:feature/auth` | Work for feature/auth branch |
| `branch:release/v2.0` | Work for release/v2.0 branch |
| `branch:hotfix/login` | Work for hotfix/login branch |

**Creating branch labels**:
```bash
# Format: branch:<branch-name>
gh label create "branch:<branch-name>" --color "c5def5" --description "Work for <branch-name> branch"
```

### Anti-Patterns to Avoid

#### DON'T: Repeat labels in titles
```
❌ [BUG] Login button doesn't work
   Labels: bug

✅ Login button doesn't work
   Labels: bug, priority:high, scope:frontend
```

#### DON'T: Use type prefixes in titles
```
❌ [ENHANCEMENT] Add dark mode support
❌ [FEATURE] Implement user authentication
❌ [DOCS] Update README with examples

✅ Add dark mode support
   Labels: enhancement, priority:medium

✅ Implement user authentication
   Labels: feature, priority:high

✅ Update README with examples
   Labels: documentation, priority:low
```

#### DON'T: Use multiple type labels
```
❌ Labels: bug, enhancement
✅ Labels: bug (pick the primary type)
```

---

## Issue Naming Guidelines

### Title Format

```
<Concise description of the work>
```

**Characteristics of good titles:**
- Describes the **what**, not the **type**
- Uses imperative mood (like a command)
- 50-72 characters when possible
- No prefixes like [BUG], [FEATURE], [ENHANCEMENT]

### Examples

#### For Bugs
```
❌ [BUG] Validator rejects valid SessionStart hooks
❌ Bug: validation fails for hooks
❌ ISSUE: SessionStart hook format not recognized

✅ Validator incorrectly rejects valid SessionStart hooks
✅ Fix SessionStart hook validation to accept matchers
```

#### For Features
```
❌ [FEATURE] Add environment variable validation
❌ New Feature: env var checking for hooks
❌ ENHANCEMENT - validate environment variables

✅ Add environment variable validation for hook commands
✅ Validate environment variables in hook commands
```

#### For Documentation
```
❌ [DOCS] Skills reference non-existent scripts
❌ Documentation Issue: missing script references
❌ DOC FIX: update skill documentation

✅ Remove references to non-existent validation scripts
✅ Update skill documentation to reflect actual scripts
```

#### For Enhancements
```
❌ [ENHANCEMENT] Add prompt hook best practices
❌ Improve: hook prompt validation
❌ ENH: better prompt hooks

✅ Add prompt hook best practices validation
✅ Improve prompt hook validation with best practices
```

### Title Patterns by Type

| Type | Title Pattern | Example |
|------|--------------|---------|
| Bug | `Fix <problem>` or `<Problem description>` | `Fix race condition in concurrent file writes` |
| Feature | `Add <capability>` or `Implement <feature>` | `Add dark mode support` |
| Enhancement | `Improve <aspect>` or `Enhance <component>` | `Improve error messages for validation failures` |
| Documentation | `Update <doc>` or `Document <topic>` | `Update API reference with new endpoints` |
| Refactor | `Refactor <component>` or `Simplify <process>` | `Refactor validation logic into separate module` |

---

## Phase and Epic Structure

### Use Milestones for Phases

GitHub's built-in **milestones** are the recommended way to group related work:
- Automatic progress tracking (X of Y issues completed)
- Due dates for time-boxing
- Description field for goals and scope
- Built-in filtering in issue lists and project boards

### When to Use Milestones

Use milestones when:
- Work has multiple related issues
- Work has a target completion date
- Need to track aggregate progress
- Want to group a release, sprint, or feature phase

### Creating Milestones

```bash
# Create a milestone
gh api repos/:owner/:repo/milestones -f title="Phase: Hooks Validation" \
  -f due_on="2024-03-31T00:00:00Z" \
  -f description="Enhance hooks validation system to catch more errors"

# Or via GitHub UI: Settings → Milestones → New milestone
```

### Milestone Naming Conventions

| Type | Format | Example |
|------|--------|---------|
| Feature phase | `Phase: <Feature Name>` | `Phase: Hooks Validation` |
| Release | `v<version>` | `v2.0.0` |
| Sprint | `Sprint <number>` | `Sprint 5` |
| Quarter | `Q<number> <year>` | `Q1 2024` |

### Assigning Issues to Milestones

```bash
# Assign single issue
gh issue edit 42 --milestone "Phase: Hooks Validation"

# Bulk assign
gh issue list --label "plugin:agent-builder" --json number -q '.[].number' | \
  xargs -I {} gh issue edit {} --milestone "Phase: Hooks Validation"
```

### Example Milestone Structure

**Milestone**: `Phase: Hooks Validation`
- **Due date**: 2024-03-31
- **Description**: Enhance hooks validation system to catch more errors and provide better feedback

**Issues in milestone**:
- #101 Add tool name validation for hook matchers
- #102 Add environment variable validation for hook commands
- #103 Add prompt hook best practices validation
- #104 Update validator to support SessionStart matchers

Each issue has its own:
- Type label (enhancement, bug, etc.)
- Priority label
- Scope label if applicable
- Branch label if applicable

### Tracking Progress

```bash
# View milestone progress
gh api repos/:owner/:repo/milestones --jq '.[] | "\(.title): \(.open_issues) open, \(.closed_issues) closed"'

# List issues in milestone
gh issue list --milestone "Phase: Hooks Validation"
```

### Closing Milestones

When all issues are complete:
```bash
# Close milestone
gh api repos/:owner/:repo/milestones/<number> -X PATCH -f state="closed"
```

---

## Feature Branch Tracking

### Purpose

Track which issues relate to which feature branch to:
- See all work for a feature at a glance
- Coordinate merges
- Plan releases
- Identify work that must complete before branch merge

### Creating Branch Labels

Create labels as needed for active feature branches:

```bash
# Format: branch:<branch-name>
gh label create "branch:<branch-name>" --color "c5def5" --description "Work for <branch-name> branch"

# Examples:
gh label create "branch:feature/user-auth" --color "c5def5" --description "Work for feature/user-auth branch"
gh label create "branch:release/v2.0" --color "c5def5" --description "Work for release/v2.0 branch"
```

### Usage

1. When creating an issue for work on a specific branch, add the branch label
2. When working on a PR that addresses the issue, include the branch label
3. Query all work for a branch: `gh issue list --label "branch:<branch-name>"`

### When to Use

- **Always** for issues created while working on a feature branch
- **Always** for issues that should be addressed before merging branch
- **Optional** for issues that apply to multiple branches

### Cleanup

When a branch is merged or deleted, consider:
- Archive or delete the branch label
- Or keep it for historical tracking

---

## Quick Reference

### Creating a New Issue Checklist

1. [ ] Write clear, descriptive title (no type prefixes)
2. [ ] Add type label (bug, feature, enhancement, documentation)
3. [ ] Add priority label (high, medium, low)
4. [ ] Add scope label if applicable
5. [ ] Add branch label if related to specific feature branch
6. [ ] Assign to milestone if part of a phase/release
7. [ ] Include acceptance criteria in body

### Updating Issue Status Checklist

1. [ ] Move issue to appropriate project board column
2. [ ] Add blocking/pending reason in comment if applicable
3. [ ] Link to blocking issue/PR if blocked
4. [ ] Link PRs when work begins

### Label Application Summary

| Dimension | Always Required? | Example |
|-----------|-----------------|---------|
| Type | Yes | `bug` |
| Priority | Yes (for open) | `priority:medium` |
| Scope | If applicable | `plugin:agent-builder` |
| Branch | If feature work | `branch:feature/auth` |

**Notes**:
- Status is managed through project board columns, not labels
- Phases/epics are managed through milestones, not labels
