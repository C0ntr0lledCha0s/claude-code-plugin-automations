# Claude Component Builder Plugin - Development Guide

Quick reference for developing and validating claude-component-builder plugin components.

## Validation Commands

### Validate All Components
```bash
# From repository root
bash validate-all.sh
```

### Validate Individual Components

**Agents:**
```bash
python3 claude-component-builder/skills/building-agents/scripts/validate-agent.py claude-component-builder/agents/agent-builder.md
```

**Skills:**
```bash
python3 claude-component-builder/skills/building-skills/scripts/validate-skill.py claude-component-builder/skills/building-agents/
python3 claude-component-builder/skills/building-skills/scripts/validate-skill.py claude-component-builder/skills/building-skills/
python3 claude-component-builder/skills/building-skills/scripts/validate-skill.py claude-component-builder/skills/building-commands/
python3 claude-component-builder/skills/building-skills/scripts/validate-skill.py claude-component-builder/skills/building-hooks/
```

**Commands:**
```bash
for cmd in claude-component-builder/commands/*.md; do
  python3 claude-component-builder/skills/building-commands/scripts/validate-command.py "$cmd"
done
```

**Plugin Manifest:**
```bash
python3 -m json.tool claude-component-builder/.claude-plugin/plugin.json
```

## Component Locations

- **Agents**: `claude-component-builder/agents/*.md`
- **Skills**: `claude-component-builder/skills/*/SKILL.md`
- **Commands**: `claude-component-builder/commands/*.md`
- **Hooks**: N/A (this plugin has no hooks)
- **Validation Scripts**: `claude-component-builder/skills/*/scripts/validate-*.py`
- **Templates**: `claude-component-builder/skills/*/templates/`
- **References**: `claude-component-builder/skills/*/references/`

## Before Committing

1. Run `bash validate-all.sh` from repository root
2. Fix all critical errors
3. Verify the pre-commit hook is enabled (`.git/hooks/pre-commit`)
4. Test modified components manually

## Creating New Components

Use the claude-component-builder tools:
- `/claude-component-builder:new agent <name>` - Create new agent
- `/claude-component-builder:new skill <name>` - Create new skill
- `/claude-component-builder:new command <name>` - Create new command
- `/claude-component-builder:new hook <name>` - Create new hook

Or invoke the skills by mentioning keywords like "create agent", "modify skill", etc.
