---
description: Audit all skills in repository for quality and compliance
allowed-tools: Read, Bash
argument-hint: [--verbose]
model: claude-haiku-4-5
---

# Audit All Skills

Run comprehensive quality audit on all skills in the repository.

## Your Task

Execute the bulk skill audit tool to validate all skills and generate a report.

## Arguments

- `$1` - (optional) `--verbose` or `-v` to show warnings and recommendations

## Workflow

1. **Run Audit**: Execute audit script
   ```bash
   python3 {baseDir}/../scripts/audit-skills.py $ARGUMENTS
   ```

2. **Script Scans**:
   - `.claude/skills/` directories
   - Plugin `skills/` directories
   - All skill directories with SKILL.md files

3. **Script Validates Each Skill**:
   - Directory name format (lowercase-hyphens)
   - Required fields (name, description)
   - **Model field check (CRITICAL: must not exist)**
   - Tool permissions (valid tools only)
   - Auto-invocation clarity in description
   - Directory structure (SKILL.md, scripts/, references/)
   - {baseDir} usage for resources
   - Security (Bash validation, permissions)
   - Script executable permissions

4. **Script Generates Report**:
   - Total skill count
   - Status breakdown:
     - ✅ Valid (no issues)
     - ⚠️ Warnings (improvements recommended)
     - ❌ Errors (critical issues, blocks commit)
     - 💥 Parse Errors (invalid YAML/structure)
   - Lists all skills with errors
   - Shows warnings (if --verbose)
   - Provides remediation guidance

5. **Present Results**: Show the user the audit report

## Example Usage

```
# Basic audit (errors only)
/agent-builder:skills:audit

# Detailed audit (includes warnings)
/agent-builder:skills:audit --verbose
```

## Report Sections

1. **Summary**
   - Total skills
   - Count by status

2. **Skills with Errors** (always shown)
   - Lists each skill with critical issues
   - Shows specific error messages
   - Blocks git commit if pre-commit hook enabled

3. **Skills with Warnings** (--verbose only)
   - Lists skills with recommended improvements
   - Non-blocking, but should be addressed

4. **Recommendations**
   - Suggested next actions
   - Links to fix tools

## Exit Codes

- `0` - All skills valid or only warnings
- `1` - Critical errors found (blocks commit)

## Common Issues Found

- **Model Field (CRITICAL)**: Skill has `model:` field (not supported)
- **Unclear Auto-Invocation**: Description doesn't state WHEN to invoke
- **Missing {baseDir}**: Scripts/references not using {baseDir} variable
- **Non-Executable Scripts**: Scripts in scripts/ directory lack +x permission
- **Security Issues**: Bash access without validation documentation
- **Missing Fields**: No name or description
- **Naming Issues**: Uppercase, underscores, too long, non-gerund form
- **Directory Mismatch**: Directory name doesn't match frontmatter name

## What to Do With Results

1. **Fix Critical Errors First** (❌)
   - Model field: Use `/agent-builder:skills:migrate <name> --apply`
   - Other errors: Use `/agent-builder:skills:update <name>`

2. **Address Warnings** (⚠️)
   - Use `/agent-builder:skills:enhance <name>` to see specific improvements

3. **Re-run Audit**
   - Verify improvements: `/agent-builder:skills:audit`

## Integration with Pre-Commit Hooks

If pre-commit hook is configured, this audit runs automatically before commits and blocks commits with errors.

## If Script Not Found

Script path: `agent-builder/skills/building-skills/scripts/audit-skills.py`
