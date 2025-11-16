---
description: Manage template files in a skill's templates/ or assets/ directory
allowed-tools: Read, Write, Edit, Bash
argument-hint: '<skill-name> [action]'
model: claude-haiku-4-5
---

# Update Skill Templates

Manage template files in **$1** skill's `templates/` or `assets/` directory.

## Your Task

Help the user manage template files for a skill.

## Arguments

- `$1` - Skill name (required)
- `$2` - Action: `list`, `add`, `remove`, `update` (optional, defaults to `list`)
- `$3+` - Additional arguments depending on action

## Workflow

1. **Run Management Script**:
   ```bash
   python3 {baseDir}/../scripts/manage-skill-templates.py $ARGUMENTS
   ```

2. **Script Actions**:
   - **list**: Show all template files
   - **add**: Create new template file
   - **remove**: Delete a template file
   - **update**: Edit existing template
   - **validate**: Check template syntax

3. **Update SKILL.md**: Ensure templates are documented

## Actions

### List Templates
```bash
/agent-builder:skills:update-templates building-agents list
```
Shows all files in `templates/` or `assets/` directory.

### Add Template
```bash
/agent-builder:skills:update-templates building-agents add <filename>
```
Creates a new template file interactively.

### Remove Template
```bash
/agent-builder:skills:update-templates building-agents remove <filename>
```
Removes a template file after confirmation.

### Update Template
```bash
/agent-builder:skills:update-templates building-agents update <filename>
```
Opens template for editing.

## Template File Conventions

**Naming**:
- Use lowercase-hyphens: `agent-template.md`
- Use appropriate extension: `.md`, `.json`, `.yaml`, `.sh`, `.py`
- Descriptive names

**Content**:
- Include variable placeholders: `{{NAME}}`, `{{DESCRIPTION}}`
- Add clear comments
- Provide usage instructions in header

**{baseDir} Usage**:
When referencing in SKILL.md:
```markdown
Use template: `{{baseDir}}/templates/agent-template.md`
```

## Common Template Types

1. **Markdown Templates**: Component blueprints
   - `agent-template.md`
   - `skill-template.md`

2. **JSON Templates**: Configuration files
   - `plugin-template.json`
   - `config-template.json`

3. **YAML Templates**: Frontmatter examples
   - `frontmatter-template.yaml`

4. **Script Templates**: Automation boilerplate
   - `script-template.py`
   - `script-template.sh`

## Template Variables

Use consistent variable syntax:
```markdown
---
name: {{NAME}}
description: {{DESCRIPTION}}
version: {{VERSION}}
---

# {{TITLE}}

{{CONTENT}}
```

## Validation

The script checks:
- Valid file extension
- Syntax validation (JSON, YAML)
- Variable placeholder consistency
- No hardcoded values

## Integration with SKILL.md

After adding templates, document them in SKILL.md:

```markdown
## Templates

Use these templates to get started:

\`\`\`bash
# Copy agent template
cp {{baseDir}}/templates/agent-template.md my-agent.md

# Replace variables
sed -i 's/{{NAME}}/my-agent/g' my-agent.md
\`\`\`
```

## If Script Not Found

Script path: `agent-builder/skills/building-skills/scripts/manage-skill-templates.py`

## Related Commands

- `/agent-builder:skills:update-references <name>` - Manage references
- `/agent-builder:skills:update-scripts <name>` - Manage scripts
- `/agent-builder:skills:update <name>` - Update skill configuration
