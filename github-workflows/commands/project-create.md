---
description: Create a GitHub Projects v2 board with template (sprint, kanban, or roadmap)
allowed-tools: Bash, Read
argument-hint: "[project-name] [template]"
---

# Create Project Board Command

Create a new GitHub Projects v2 board with a predefined template.

## Usage

```bash
/project-create "Sprint 5" sprint
/project-create "Feature Backlog" kanban
/project-create "Q1 Roadmap" roadmap
```

## Arguments

- `$1` (required): Project title/name
- `$2` (optional): Template type (sprint, kanban, roadmap). Default: kanban

## What This Does

1. **Creates project board** using GitHub CLI
2. **Applies template** if specified (columns, fields, views)
3. **Configures automation** (auto-add, field updates)
4. **Returns project URL** for access

## Templates

### Sprint Template
- **Columns**: Backlog, Sprint, In Progress, Review, Done
- **Fields**: Sprint (iteration), Story Points, Priority
- **Good for**: Scrum teams, sprint planning

### Kanban Template
- **Columns**: Todo, In Progress, Review, Done
- **Fields**: Priority, Size, Assignee
- **Good for**: Continuous flow, individual projects

### Roadmap Template
- **Columns**: Planning, In Progress, Completed, On Hold
- **Fields**: Quarter, Status, Target Date
- **Good for**: Long-term planning, feature roadmaps

## Example Session

```
User: /project-create "Sprint 5" sprint