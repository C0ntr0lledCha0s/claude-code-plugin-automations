# Self-Improvement Plugin - Development Guide

Quick reference for developing and validating self-improvement plugin components.

## Validation Commands

### Validate All Components
```bash
# From repository root
bash validate-all.sh
```

### Validate Individual Components

**Agents:**
```bash
python3 agent-builder/skills/building-agents/scripts/validate-agent.py self-improvement/agents/self-critic.md
```

**Skills:**
```bash
python3 agent-builder/skills/building-skills/scripts/validate-skill.py self-improvement/skills/analyzing-response-quality/
python3 agent-builder/skills/building-skills/scripts/validate-skill.py self-improvement/skills/suggesting-improvements/
python3 agent-builder/skills/building-skills/scripts/validate-skill.py self-improvement/skills/creating-feedback-loops/
```

**Commands:**
```bash
for cmd in self-improvement/commands/*.md; do
  python3 agent-builder/skills/building-commands/scripts/validate-command.py "$cmd"
done
```

**Hooks:**
```bash
python3 agent-builder/skills/building-hooks/scripts/validate-hooks.py self-improvement/hooks/hooks.json
```

**Plugin Manifest:**
```bash
python3 -m json.tool self-improvement/.claude-plugin/plugin.json
```

## Component Locations

- **Agents**: `self-improvement/agents/*.md`
- **Skills**: `self-improvement/skills/*/SKILL.md`
- **Commands**: `self-improvement/commands/*.md`
- **Hooks**: `self-improvement/hooks/hooks.json`

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

## Testing

- **Skills**: Trigger auto-invocation by mentioning "response quality", "improvements", or "feedback loops"
- **Commands**: Use `/self-improvement:quality-check`, `/self-improvement:review-my-work`, etc.
- **Hooks**: Monitored automatically during conversations
