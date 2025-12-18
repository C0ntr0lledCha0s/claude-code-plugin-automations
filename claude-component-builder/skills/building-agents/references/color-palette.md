# Agent Color Palette Reference

This reference provides color recommendations for Claude Code agents organized by domain and plugin.

## Color Format

Claude Code accepts the following **named colors** (case-insensitive):

| Color | Name |
|-------|------|
| 🔴 | `red` |
| 🔵 | `blue` |
| 🟢 | `green` |
| 🟡 | `yellow` |
| 🟣 | `purple` |
| 🟠 | `orange` |
| 🩷 | `pink` |
| 🩵 | `cyan` |

**YAML format**: No quotes required for color names
```yaml
color: blue
```

## Domain Color Recommendations

### Meta/Building → Purple
For meta-programming, agent builders, and tools that create other tools.

```yaml
# claude-component-builder agents
agent-builder:     purple
skill-builder:     purple
command-builder:   purple
hook-builder:      purple
plugin-builder:    purple
skill-reviewer:    purple
```

### GitHub/Git → Blue
For version control, GitHub workflows, and collaboration tools.

```yaml
# github-workflows agents
workflow-orchestrator: blue
issue-manager:         blue
pr-reviewer:           blue
release-manager:       blue
```

### Testing/QA → Red
For test execution, quality assurance, and validation tools.

```yaml
# testing-expert agents
test-reviewer: red
```

### Documentation → Green
For documentation generation, README creation, and guides.

```yaml
doc-generator:    green
readme-writer:    green
changelog-writer: green
```

### Security → Orange
For security analysis, vulnerability scanning, and compliance tools.

```yaml
security-auditor:     orange
vulnerability-scanner: orange
compliance-checker:   orange
```

### Performance → Cyan
For optimization, profiling, and performance analysis tools.

```yaml
optimizer:        cyan
profiler:         cyan
bundle-analyzer:  cyan
```

### Research/Exploration → Purple
For research agents, codebase exploration, and investigation tools.

```yaml
# research-agent agents
investigator: purple
```

### Self-Improvement → Pink
For self-critique, quality analysis, and feedback tools.

```yaml
# self-improvement agents
self-critic: pink
```

### Project Management → Yellow
For project coordination, planning, and task management.

```yaml
# project-manager agents
project-coordinator: yellow
```

### Knowledge/Expertise → Cyan
For domain-specific expertise and knowledge tools.

```yaml
# logseq-expert agents
logseq-db-expert: cyan
```

## Color Selection Best Practices

### 1. Plugin Consistency
Use the same color for all agents within a plugin.

```yaml
# Good - consistent color for github-workflows
workflow-orchestrator: blue
issue-manager:         blue
pr-reviewer:           blue

# Avoid - inconsistent colors within same plugin
workflow-orchestrator: blue
issue-manager:         red
pr-reviewer:           green
```

### 2. Domain Matching
Choose colors that intuitively match the agent's purpose:

| Color | Domain Association |
|-------|-------------------|
| `red` | Testing, errors, warnings |
| `blue` | Workflows, processes, git |
| `green` | Documentation, success, creation |
| `yellow` | Caution, validation, planning |
| `purple` | Meta, building, creation |
| `orange` | Security, alerts |
| `pink` | Self-improvement, feedback |
| `cyan` | Performance, knowledge, data |

### 3. Terminal Visibility
All named colors are designed for good visibility on both light and dark terminal backgrounds.

### 4. Accessibility
Named colors are chosen to be distinguishable for most users, but don't rely solely on color to convey critical information.

## Quick Reference by Plugin

| Plugin | Recommended Color |
|--------|------------------|
| claude-component-builder | `purple` |
| github-workflows | `blue` |
| testing-expert | `red` |
| self-improvement | `pink` |
| research-agent | `purple` |
| project-manager | `yellow` |
| logseq-expert | `cyan` |
