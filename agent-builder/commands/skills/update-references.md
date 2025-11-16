---
description: Manage reference documentation files in a skill's references/ directory
allowed-tools: Read, Write, Edit, Bash
argument-hint: '<skill-name> [action]'
model: claude-haiku-4-5
---

# Update Skill References

Manage reference documentation in **$1** skill's `references/` directory.

## Your Task

Help the user manage reference documentation files for a skill.

## Arguments

- `$1` - Skill name (required)
- `$2` - Action: `list`, `add`, `remove`, `update` (optional, defaults to `list`)
- `$3+` - Additional arguments depending on action

## Workflow

1. **Run Management Script**:
   ```bash
   python3 {baseDir}/../scripts/manage-skill-references.py $ARGUMENTS
   ```

2. **Script Actions**:
   - **list**: Show all reference files
   - **add**: Create new reference document
   - **remove**: Delete a reference file
   - **update**: Edit existing reference
   - **validate**: Check markdown formatting

3. **Update SKILL.md**: Ensure references are documented

## Actions

### List References
```bash
/agent-builder:skills:update-references building-agents list
```
Shows all files in `references/` directory with descriptions.

### Add Reference
```bash
/agent-builder:skills:update-references building-agents add <filename.md>
```
Creates a new reference document interactively.

### Remove Reference
```bash
/agent-builder:skills:update-references building-agents remove <filename.md>
```
Removes a reference file after confirmation.

### Update Reference
```bash
/agent-builder:skills:update-references building-agents update <filename.md>
```
Opens reference for editing.

## Reference File Conventions

**Naming**:
- Use lowercase-hyphens: `agent-update-patterns.md`
- Use `.md` extension
- Descriptive names

**Content**:
- Start with `# Title` heading
- Include clear sections
- Provide examples
- Link to related resources

**{baseDir} Usage**:
When referencing in SKILL.md:
```markdown
See [{baseDir}/references/guide.md]
```

## Common Reference Types

1. **Patterns**: Common scenarios and solutions
   - `agent-update-patterns.md`
   - `migration-patterns.md`

2. **Guides**: Step-by-step instructions
   - `agent-migration-guide.md`
   - `troubleshooting-guide.md`

3. **Checklists**: Quality checks
   - `agent-checklist.md`
   - `security-checklist.md`

4. **Examples**: Sample implementations
   - `example-agent.md`
   - `example-workflow.md`

## Validation

The script checks:
- Valid markdown formatting
- Proper heading structure
- No broken internal links
- Consistent style

## Integration with SKILL.md

After adding references, update SKILL.md to document them:

```markdown
## References

- [{baseDir}/references/guide.md] - Implementation guide
- [{baseDir}/references/patterns.md] - Common patterns
```

## If Script Not Found

Script path: `agent-builder/skills/building-skills/scripts/manage-skill-references.py`

## Related Commands

- `/agent-builder:skills:update-templates <name>` - Manage templates
- `/agent-builder:skills:update-scripts <name>` - Manage scripts
- `/agent-builder:skills:update <name>` - Update skill configuration
