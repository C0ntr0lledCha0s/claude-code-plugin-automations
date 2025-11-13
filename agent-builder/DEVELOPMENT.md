# Agent Builder Plugin - Development Guide

Quick reference for developing and validating agent-builder plugin components.

## Validation Commands

### Validate All Components
```bash
# From repository root
bash validate-all.sh
```

### Validate Individual Components

**Agents:**
```bash
python3 agent-builder/skills/building-agents/scripts/validate-agent.py agent-builder/agents/meta-architect.md
```

**Skills:**
```bash
python3 agent-builder/skills/building-skills/scripts/validate-skill.py agent-builder/skills/building-agents/
python3 agent-builder/skills/building-skills/scripts/validate-skill.py agent-builder/skills/building-skills/
python3 agent-builder/skills/building-skills/scripts/validate-skill.py agent-builder/skills/building-commands/
python3 agent-builder/skills/building-skills/scripts/validate-skill.py agent-builder/skills/building-hooks/
```

**Commands:**
```bash
for cmd in agent-builder/commands/*.md; do
  python3 agent-builder/skills/building-commands/scripts/validate-command.py "$cmd"
done
```

**Plugin Manifest:**
```bash
python3 -m json.tool agent-builder/.claude-plugin/plugin.json
```

## Component Locations

- **Agents**: `agent-builder/agents/*.md`
- **Skills**: `agent-builder/skills/*/SKILL.md`
- **Commands**: `agent-builder/commands/*.md`
- **Hooks**: N/A (this plugin has no hooks)
- **Validation Scripts**: `agent-builder/skills/*/scripts/validate-*.py`
- **Templates**: `agent-builder/skills/*/templates/`
- **References**: `agent-builder/skills/*/references/`

## Before Committing

1. Run `bash validate-all.sh` from repository root
2. Fix all critical errors
3. Verify the pre-commit hook is enabled (`.git/hooks/pre-commit`)
4. Test modified components manually

## Creating New Components

Use the agent-builder tools:
- `/agent-builder:new-agent <name>` - Create new agent
- `/agent-builder:new-skill <name>` - Create new skill
- `/agent-builder:new-command <name>` - Create new command
- `/agent-builder:new-hook <name>` - Create new hook

Or invoke the skills by mentioning keywords like "create agent", "modify skill", etc.
