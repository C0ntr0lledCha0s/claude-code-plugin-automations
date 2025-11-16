---
description: Manage scripts in a skill's scripts/ directory with executable permission enforcement
allowed-tools: Read, Write, Edit, Bash
argument-hint: '<skill-name> [action]'
model: claude-haiku-4-5
---

# Update Skill Scripts

Manage scripts in **$1** skill's `scripts/` directory with **automatic executable permission enforcement**.

## Your Task

Help the user manage script files for a skill, ensuring all scripts have proper executable permissions.

## Arguments

- `$1` - Skill name (required)
- `$2` - Action: `list`, `add`, `remove`, `update`, `fix-permissions` (optional, defaults to `list`)
- `$3+` - Additional arguments depending on action

## Workflow

1. **Run Management Script**:
   ```bash
   python3 {baseDir}/../scripts/manage-skill-scripts.py $ARGUMENTS
   ```

2. **Script Actions**:
   - **list**: Show all scripts with permission status
   - **add**: Create new script with +x permission
   - **remove**: Delete a script file
   - **update**: Edit existing script
   - **fix-permissions**: Bulk chmod +x on all scripts
   - **validate**: Check shebangs and permissions

3. **Update SKILL.md**: Ensure scripts are documented

## Actions

### List Scripts
```bash
/agent-builder:skills:update-scripts building-agents list
```
Shows all scripts with executable permission status.

### Add Script
```bash
/agent-builder:skills:update-scripts building-agents add <filename.py>
```
Creates a new script with:
- Proper shebang (`#!/usr/bin/env python3` or `#!/bin/bash`)
- Executable permissions (`chmod +x`)
- Template structure

### Remove Script
```bash
/agent-builder:skills:update-scripts building-agents remove <filename.py>
```
Removes a script file after confirmation.

### Fix Permissions
```bash
/agent-builder:skills:update-scripts building-agents fix-permissions
```
**Automatically sets `chmod +x` on ALL scripts in directory.**

### Validate Scripts
```bash
/agent-builder:skills:update-scripts building-agents validate
```
Checks:
- Shebang presence
- Executable permissions
- Python/Bash syntax errors
- Input validation patterns

## Script File Conventions

**Naming**:
- Use lowercase-hyphens: `validate-agent.py`
- Use appropriate extension: `.py`, `.sh`
- Descriptive, action-oriented names

**Shebang** (REQUIRED):
```python
#!/usr/bin/env python3
```
```bash
#!/bin/bash
```

**Permissions** (ENFORCED):
- All scripts MUST be executable (`chmod +x`)
- Tool automatically fixes permissions
- Validation checks and warns

**Documentation**:
```python
#!/usr/bin/env python3
"""
Script description

Part of the skill-name skill for Claude Code
"""
```

## {baseDir} Usage in SKILL.md

Reference scripts with {baseDir}:
```markdown
## Usage

Run the validation script:
\`\`\`bash
python3 {{baseDir}}/scripts/validate-agent.py agent-name
\`\`\`
```

## Automatic Permission Enforcement

**On Add**: Scripts created with `chmod +x` automatically

**On Fix**: Bulk fix all scripts in directory:
```bash
/agent-builder:skills:update-scripts my-skill fix-permissions
```

**On Validate**: Warns about non-executable scripts

## Common Script Types

1. **Validation Scripts**: Check component validity
   - `validate-agent.py`
   - `validate-command.py`

2. **Creation Scripts**: Generate new components
   - `create-agent.py`
   - `create-command.py`

3. **Maintenance Scripts**: Update existing components
   - `update-agent.py`
   - `migrate-agent.py`

4. **Analysis Scripts**: Quality assessment
   - `enhance-agent.py`
   - `audit-agents.py`

## Security Best Practices

**Input Validation**:
```python
import sys
import re

if len(sys.argv) < 2:
    print("Usage: script.py <name>")
    sys.exit(1)

name = sys.argv[1]

# Validate input
if not re.match(r'^[a-z0-9-]+$', name):
    print("Invalid name: use lowercase-hyphens only")
    sys.exit(1)
```

**Path Safety**:
```python
from pathlib import Path

# Safe path handling
file_path = Path(base_dir) / name
if not file_path.parent.exists():
    print(f"Invalid path: {file_path}")
    sys.exit(1)
```

## Integration with SKILL.md

Document all scripts in SKILL.md:

```markdown
## Scripts

### Validation
\`\`\`bash
python3 {{baseDir}}/scripts/validate-agent.py <agent-name>
\`\`\`

### Creation
\`\`\`bash
python3 {{baseDir}}/scripts/create-agent.py <agent-name>
\`\`\`
```

## If Script Not Found

Script path: `agent-builder/skills/building-skills/scripts/manage-skill-scripts.py`

## Related Commands

- `/agent-builder:skills:update-references <name>` - Manage references
- `/agent-builder:skills:update-templates <name>` - Manage templates
- `/agent-builder:skills:audit` - Check for non-executable scripts
