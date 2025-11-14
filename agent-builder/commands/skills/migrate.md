---
description: Migrate skill schema (e.g., remove invalid model field)
allowed-tools: Read, Bash
argument-hint: '[skill-name or --dry-run|--apply]'
model: claude-haiku-4-5
---

# Migrate Skill Schema

Migrate skill(s) to current schema: **$1**

## Your Task

Run the skill migration tool to automatically update skill schemas.

## Arguments

- `$1` - Skill name, `--dry-run` (preview all), or `--apply` (apply to all)
- `$2` - (optional) `--apply` flag for single skill migration

## Critical Migration

**MOST IMPORTANT**: Remove model field from skills

Skills do NOT support the `model` field. Only agents can specify models.
If a skill has a model field, it must be removed immediately.

```yaml
# INVALID (causes errors)
---
name: my-skill
model: haiku  # ❌ Skills don't support this!
---

# VALID (corrected)
---
name: my-skill
# No model field - skills don't specify models
---
```

## Other Migrations

1. **Gerund Form Check** (recommendation)
   - Suggests gerund form for skill names
   - Manual rename required if desired

2. **Auto-Invocation Triggers** (recommendation)
   - Checks if description states WHEN to invoke
   - Manual improvement required

## Workflow

### Preview All Skills
```bash
python3 {baseDir}/../scripts/migrate-skill.py --dry-run
```

Shows what would change without modifying files.

### Apply to All Skills
```bash
python3 {baseDir}/../scripts/migrate-skill.py --apply
```

Applies migrations interactively with confirmation for each skill.

### Migrate Single Skill (Preview)
```bash
python3 {baseDir}/../scripts/migrate-skill.py $1
```

### Migrate Single Skill (Apply)
```bash
python3 {baseDir}/../scripts/migrate-skill.py $1 --apply
```

## Example Usage

```
# Preview what needs migration
/agent-builder:skills:migrate --dry-run

# Apply to specific skill
/agent-builder:skills:migrate building-commands --apply

# Apply to all skills
/agent-builder:skills:migrate --apply
```

## Script Behavior

- **Preview mode**: Shows changes without applying
- **Apply mode**: Shows diff and asks for confirmation
- **Backup**: Creates SKILL.md.bak before applying
- **Validation**: Recommends running validation after migration

## When to Use

- After upgrading Claude Code version
- When skill fails to load (model field error)
- To standardize skills across repository
- Before committing skills to version control
- When moving skills from one project to another

## Migration Report

Script provides:
- Total skills found
- Number needing migration (critical changes)
- Number with recommendations (manual changes)
- Specific changes for each skill

## Why Skills Don't Support Model Field

Skills are "always-on" expertise that Claude automatically invokes.
They use the conversation's model context. Only agents (which have
dedicated invocations with isolated context) support model specification.

## If Script Not Found

Script path: `agent-builder/skills/building-skills/scripts/migrate-skill.py`
