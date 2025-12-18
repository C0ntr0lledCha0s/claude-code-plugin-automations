---
description: Migrate component schema to current version and apply best practices
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
argument-hint: "[type] [name|--all]"
model: claude-sonnet-4-5
---

# Migrate Component

Migrate Claude Code components to current schema version and apply best practices.

**Arguments:**
- `$1` (required): Component type - `agent`, `skill`, `command`, `hook`
- `$2` (optional): Component name OR `--all` to migrate all of type

**Full arguments:** $ARGUMENTS

## Workflow

### Single Component
```
/claude-component-builder:migrate agent old-agent
    ↓
Task → agent-builder
    ↓
Detect version → Apply migrations → Validate
```

### All Components of Type
```
/claude-component-builder:migrate command --all
    ↓
Task → command-builder
    ↓
Find all commands → Migrate each → Report
```

## Migration Paths

### Agents
| From | To | Changes |
|------|-----|---------|
| pre-1.0 | 1.0 | Add YAML frontmatter |
| 0.x | current | Fix schema, optimize tools |
| 1.0 | current | Apply best practices |

### Skills
| From | To | Changes |
|------|-----|---------|
| Any | current | **Remove model field** (critical) |
| 0.x | current | Add directory structure |

### Commands
| From | To | Changes |
|------|-----|---------|
| Any | current | **Fix model format** (critical) |
| - | - | `haiku` → `claude-haiku-4-5` |
| - | - | `sonnet` → `claude-sonnet-4-5` |

### Hooks
| From | To | Changes |
|------|-----|---------|
| 0.x | current | Update event schema |
| Any | current | Security hardening |

## Examples

### Migrate Single Agent
```
/claude-component-builder:migrate agent old-reviewer
```

### Migrate All Commands
```
/claude-component-builder:migrate command --all
```

### Migrate All Skills
```
/claude-component-builder:migrate skill --all
```

### Migrate Single Hook
```
/claude-component-builder:migrate hook validate-bash
```

## Critical Migrations

### Skill Model Field Removal
```yaml
# Before (invalid)
---
name: my-skill
model: sonnet  # ❌ Not supported
---

# After (valid)
---
name: my-skill
# model field removed
---
```

### Command Model Format Fix
```yaml
# Before (API error)
---
description: Fast command
model: haiku  # ❌ Short alias fails
---

# After (works)
---
description: Fast command
model: claude-haiku-4-5  # ✅ Version alias
---
```

## Output Format

```markdown
## Migration Report: run-tests.md

**Schema Version**: 0.x → 2.0
**Status**: ✅ Migrated successfully

### Changes Applied
1. Updated model from short alias to version alias
2. Added missing argument-hint field
3. Standardized description format

### Diff Preview
```diff
  ---
  description: Run project test suite
- model: haiku
+ model: claude-haiku-4-5
+ argument-hint: "[test-pattern]"
  allowed-tools: Read, Grep, Glob, Bash
  ---
```

### Validation
- Pre-migration score: 6/10
- Post-migration score: 9/10
- Improvement: +50%

### Backup
- Original saved to: .claude/commands/run-tests.md.pre-migration-20250118-143022

### Rollback
To rollback: `mv .claude/commands/run-tests.md.pre-migration-20250118-143022 .claude/commands/run-tests.md`
```

## Safety Features

1. **Backup Creation**: Automatic backup before migration
2. **Diff Preview**: See changes before applying
3. **Validation**: Pre and post validation
4. **Rollback Instructions**: Easy recovery

## Execution

When invoked:
1. Parse type and target from arguments
2. Delegate via Task to appropriate builder
3. Builder detects version and applies migrations
4. Return migration report with diff and validation
