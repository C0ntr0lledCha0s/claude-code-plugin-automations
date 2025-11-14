---
description: Interactively update a skill's configuration with diff preview
allowed-tools: Read, Bash
argument-hint: '[skill-name]'
model: claude-haiku-4-5
---

# Update Skill

Update the skill named: **$1**

## Your Task

Run the interactive skill updater script to modify an existing skill's configuration.

## Arguments

- `$1` - The skill name (directory name, e.g., "building-commands")

## Workflow

1. **Invoke Script**: Run the update-skill.py script
   ```bash
   python3 {baseDir}/../scripts/update-skill.py $1
   ```

2. **Script Will**:
   - Find the skill directory
   - Show current configuration (description, version, allowed-tools, directory structure)
   - Check for model field (CRITICAL ERROR if present - skills don't support it)
   - Present interactive menu:
     1. Update description (WHEN to auto-invoke)
     2. Update allowed-tools
     3. Update version
     4. Run validation
   - Show diff preview
   - Confirm before applying changes
   - Create backup (SKILL.md.bak)
   - Run validation after update

3. **Present Results**: Show the user what was changed

## Example Usage

```
/agent-builder:skills:update building-commands
```

## Important Notes

- Changes are previewed before applying
- Original file is backed up
- Validation runs automatically
- **CRITICAL**: Skills cannot have a 'model' field (only agents support it)
- Description should clearly state WHEN Claude should auto-invoke

## Model Field Prohibition

Unlike commands, skills do NOT support the `model` field. If a skill has a model field:
1. The update script will block with an error
2. You must run migration first: `/agent-builder:skills:migrate <skill-name>`
3. This removes the invalid field automatically

## If Script Not Found

Script path: `agent-builder/skills/building-skills/scripts/update-skill.py`
