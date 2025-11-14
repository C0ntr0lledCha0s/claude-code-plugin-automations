---
description: Analyze a skill's quality and get AI-powered improvement suggestions
allowed-tools: Read, Bash
argument-hint: '[skill-name]'
model: claude-haiku-4-5
---

# Enhance Skill

Analyze and score the skill named: **$1**

## Your Task

Run the skill enhancement analyzer to get quality scores and recommendations.

## Arguments

- `$1` - The skill name (directory name)

## Workflow

1. **Invoke Script**: Run the enhance-skill.py script
   ```bash
   python3 {baseDir}/../scripts/enhance-skill.py $1
   ```

2. **Script Analyzes**:
   - Schema compliance (naming, required fields, gerund form)
   - Model field check (CRITICAL - must not be present)
   - Auto-invocation clarity (WHEN to invoke, triggers)
   - Directory structure (subdirs, {baseDir} usage, script permissions)
   - Security (Bash access, validation, permissions)
   - Content quality (sections, examples, documentation)
   - Maintainability (structure, formatting, references)

3. **Script Returns**:
   - Overall score (0-10)
   - Detailed scores for each of 7 categories
   - Specific findings (✅/⚠️/❌)
   - Prioritized recommendations (🔴 CRITICAL, 🟡 HIGH, 🟢 MEDIUM)
   - Next steps

4. **Present Results**: Show the user their skill's score and recommendations

## Example Usage

```
/agent-builder:skills:enhance building-commands
```

## Scoring Categories

1. **Schema Compliance** (10 points)
   - Valid name format (lowercase-hyphens)
   - Gerund form naming (building-, analyzing-)
   - Required fields (name, description)
   - Name matches directory

2. **Model Field Check** (10 points)
   - CRITICAL: No model field present
   - Skills don't support model specification
   - Only agents can have model field

3. **Auto-Invocation Clarity** (10 points)
   - Description states WHEN to invoke
   - Has "When to Use" section
   - Documents auto-invocation triggers
   - Specific (not vague)

4. **Directory Structure** (10 points)
   - Valid subdirectories (scripts/, references/, assets/)
   - Uses {baseDir} variable appropriately
   - Scripts are executable
   - Has reference documentation

5. **Security** (10 points)
   - Bash access validated
   - No dangerous operations
   - Input validation documented
   - Minimal tool permissions

6. **Content Quality** (10 points)
   - Has key sections (when to use, capabilities, examples)
   - Appropriate length (200-3000 words)
   - Clear documentation
   - Multiple examples

7. **Maintainability** (10 points)
   - Clear section headings
   - Uses lists and formatting
   - Code blocks for examples
   - Well-organized

## What to Do With Results

- **Score ≥ 8**: Excellent! Only minor improvements possible
- **Score 6-7**: Good skill, some improvements recommended
- **Score < 6**: Needs improvement, address findings

Use `/agent-builder:skills:update <skill-name>` to apply improvements.

## Key Skill Requirements

Unlike commands, skills must:
- **Not have** a model field
- Clearly state **when** to auto-invoke
- Use gerund form naming (recommended)
- Focus on "always-on" expertise

## If Script Not Found

Script path: `agent-builder/skills/building-skills/scripts/enhance-skill.py`
