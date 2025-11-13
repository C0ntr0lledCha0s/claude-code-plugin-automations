# GitHub Workflows Plugin - Development Guide

Quick reference for developing and validating github-workflows plugin components.

## Validation Commands

### Validate All Components
```bash
# From repository root
bash validate-all.sh
```

### Validate Individual Components

**Agents:**
```bash
python3 agent-builder/skills/building-agents/scripts/validate-agent.py github-workflows/agents/workflow-orchestrator.md
python3 agent-builder/skills/building-agents/scripts/validate-agent.py github-workflows/agents/pr-reviewer.md
```

**Skills:**
```bash
python3 agent-builder/skills/building-skills/scripts/validate-skill.py github-workflows/skills/managing-commits/
python3 agent-builder/skills/building-skills/scripts/validate-skill.py github-workflows/skills/managing-projects/
python3 agent-builder/skills/building-skills/scripts/validate-skill.py github-workflows/skills/organizing-with-labels/
python3 agent-builder/skills/building-skills/scripts/validate-skill.py github-workflows/skills/triaging-issues/
python3 agent-builder/skills/building-skills/scripts/validate-skill.py github-workflows/skills/reviewing-pull-requests/
```

**Commands:**
```bash
for cmd in github-workflows/commands/*.md; do
  python3 agent-builder/skills/building-commands/scripts/validate-command.py "$cmd"
done
```

**Hooks:**
```bash
python3 agent-builder/skills/building-hooks/scripts/validate-hooks.py github-workflows/hooks/hooks.json
```

**Plugin Manifest:**
```bash
python3 -m json.tool github-workflows/.claude-plugin/plugin.json
```

## Component Locations

- **Agents**: `github-workflows/agents/*.md`
- **Skills**: `github-workflows/skills/*/SKILL.md`
- **Commands**: `github-workflows/commands/*.md`
- **Hooks**: `github-workflows/hooks/hooks.json`
- **Helper Scripts**: `github-workflows/skills/*/scripts/`

## Before Committing

1. Run `bash validate-all.sh` from repository root
2. Fix all critical errors (especially security warnings in commands)
3. Verify the pre-commit hook is enabled (`.git/hooks/pre-commit`)
4. Test modified components manually

## Creating New Components

Use the agent-builder tools:
- `/agent-builder:new-agent <name>` - Create new agent
- `/agent-builder:new-skill <name>` - Create new skill
- `/agent-builder:new-command <name>` - Create new command
- `/agent-builder:new-hook <name>` - Create new hook

Or invoke the skills by mentioning keywords like "create command", "modify skill", etc.

## Testing

- **Skills**: Trigger auto-invocation by mentioning "commits", "projects", "labels", "issues", or "pull requests"
- **Commands**:
  - `/github-workflows:commit-smart` - Smart commit with grouping
  - `/github-workflows:project-create` - Create project board
  - `/github-workflows:pr-review-request` - Request PR review
  - `/github-workflows:issue-triage` - Triage issues
  - `/github-workflows:label-sync` - Sync labels
  - And more...

## Security Notes

- Commands that use Bash MUST validate all user input
- Use allowlists for argument validation
- Never use `$1` followed by backtick in documentation (triggers security validator)
- Use "First argument" instead of "`$1`" in markdown
