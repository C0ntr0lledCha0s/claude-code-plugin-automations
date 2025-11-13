---
description: Create a new Claude Code skill with directory structure and resources
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
argument-hint: [skill-name]
model: claude-sonnet-4-5
---

# Create New Skill

Create a new Claude Code skill named: **$1**

## Your Task

1. **Gather Requirements**: Ask the user about:
   - What domain expertise should this skill provide?
   - When should Claude automatically invoke it?
   - What resources does it need (scripts, docs, templates)?
   - What tools should be pre-approved (allowed-tools)?
   - Will it need helper scripts or reference documentation?

2. **Design the Skill**: Based on requirements:
   - Validate the name follows conventions (lowercase-hyphens, gerund form preferred, max 64 chars)
   - Write a description focused on WHEN to auto-invoke
   - Plan directory structure (scripts/, references/, assets/)
   - Identify required resources
   - Select allowed tools (conservative: Read, Grep, Glob)
   - Choose appropriate model

3. **Create Directory Structure**:
   ```
   .claude/skills/$1/
   ├── SKILL.md
   ├── scripts/       (if needed)
   ├── references/    (if needed)
   └── assets/        (if needed)
   ```

4. **Create SKILL.md**:
   - Use the template from the building-skills skill
   - Include proper YAML frontmatter with:
     - name: $1
     - description: Clear auto-invocation triggers
     - version: 1.0.0
     - allowed-tools: Minimal set
   - Add detailed body with sections:
     - Skill overview
     - Capabilities
     - When to use (critical for auto-invocation)
     - How to use (including {baseDir} references)
     - Resources available
     - Examples
     - Important notes

5. **Create Resources** (if needed):
   - Scripts in `scripts/` directory
   - Documentation in `references/` directory
   - Templates in `assets/` directory
   - Make scripts executable: `chmod +x scripts/*.sh`

6. **Validate the Skill**:
   - Run validation script if available
   - Check naming (gerund form preferred: analyzing-, building-, generating-)
   - Verify YAML syntax
   - Test {baseDir} references
   - Review allowed-tools for security
   - Ensure description triggers auto-invocation

7. **Provide Usage Instructions**:
   - Explain when Claude will auto-invoke this skill
   - Show how to test auto-invocation
   - Document the resources created

## Skill Naming Conventions

- **Lowercase letters, numbers, and hyphens only**
- **No underscores or special characters**
- **Max 64 characters**
- **Gerund form preferred** (verb + -ing): `analyzing-data`, `generating-reports`, `reviewing-code`, `writing-tests`
- **Descriptive**: Name should indicate domain

## Auto-Invocation Description

The description field is CRITICAL. It must clearly state WHEN Claude should use the skill:

**Good**:
- "Expert at analyzing CSV files. Use when loading, analyzing, or transforming CSV data."
- "Generates comprehensive unit tests. Use when creating tests, improving coverage, or writing test fixtures."

**Bad**:
- "Data analysis expert" (too vague)
- "Helps with testing" (doesn't specify when)

## The {baseDir} Variable

Skills can reference resources using `{baseDir}`:

```markdown
For API docs, see `{baseDir}/references/api-guide.md`
Run: `python {baseDir}/scripts/analyze.py`
Load template: `{baseDir}/assets/template.json`
```

## Example

If user wants to create a CSV analysis skill:

**Name**: `analyzing-csv-data`
**Description**: Expert at analyzing CSV and tabular data. Use when loading, analyzing, summarizing, or transforming CSV files.
**Directory**:
```
.claude/skills/analyzing-csv-data/
├── SKILL.md
├── scripts/
│   ├── csv_analyzer.py
│   └── generate_summary.py
├── references/
│   └── pandas-guide.md
└── assets/
    └── report-template.json
```

**Allowed-tools**: Read, Grep, Glob, Bash (for running Python scripts)

## Important Notes

- Skills are auto-invoked by Claude when relevant
- Description must be specific about WHEN to use
- Use {baseDir} to reference resources
- Start with minimal allowed-tools
- Create directory structure before SKILL.md
- Make all shell scripts executable
- Test that auto-invocation works correctly

## If No Name Provided

If $1 is empty, ask the user:
- What should the skill be named?
- What expertise should it provide?
- When should Claude automatically use it?

Then proceed with the creation process.

---

**Remember**: This command invokes the `building-skills` skill which provides expert guidance on skill creation. Use that skill's knowledge throughout this process.
