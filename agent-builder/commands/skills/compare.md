---
description: Compare two skills side-by-side to understand differences and trade-offs
allowed-tools: Read, Bash
argument-hint: '[skill1] [skill2]'
model: claude-haiku-4-5
---

# Compare Skills

Compare two skills side-by-side: **$1** vs **$2**

## Your Task

Run the skill comparison tool to analyze differences between two skill directories.

## Arguments

- `$1` - First skill name (directory name)
- `$2` - Second skill name (directory name)

## Workflow

1. **Invoke Script**: Run the compare script
   ```bash
   python3 {baseDir}/../scripts/compare-skills.py $1 $2
   ```

2. **Script Compares**:
   - **Frontmatter**: Side-by-side field comparison (name, description, version, allowed-tools)
   - **Directory Structure**: Compare subdirectories (scripts/, references/, assets/)
   - **Metrics**: Word count, headings, code blocks, list items
   - **Content**: Unified diff of SKILL.md body text
   - **Resources**: Count of scripts, references, templates

3. **Script Outputs**:
   - Field-by-field frontmatter comparison table
   - Directory structure differences
   - Resource file counts
   - Metric comparisons with differences
   - Line-by-line content diff (colored)
   - Auto-invocation trigger comparison
   - Similarity score

4. **Present Results**: Show the user the comparison report

## Example Usage

```
/agent-builder:skills:compare building-agents building-skills
```

## Comparison Sections

### 1. Frontmatter Comparison
```
Field                Skill1                    Skill2
--------------------------------------------------------------------
✓ name               building-agents           building-skills
✓ description        Expert at creating...     Expert at creating...
⚠️ version            1.0.0                     1.1.0
✓ allowed-tools      Read, Write, Edit         Read, Write, Edit
```

### 2. Directory Structure Comparison
Shows which subdirectories exist in each skill:
- scripts/ directory
- references/ directory
- assets/ or templates/ directory
- File counts in each directory

### 3. Resource Comparison
```
Resource Type        Skill1          Skill2          Difference
--------------------------------------------------------------------
Scripts              3               5               +2
References           2               1               -1
Templates            0               3               +3
```

### 4. Metrics Comparison
```
Metric               Skill1          Skill2          Difference
--------------------------------------------------------------------
word_count           1,234           2,456           +1,222
heading_count        8               12              +4
code_blocks          5               7               +2
list_items           15              22              +7
```

### 5. Content Diff
Unified diff format with color coding:
- Green lines: Added in skill2
- Red lines: Removed from skill1
- Blue lines: Change location markers

### 6. Auto-Invocation Triggers
Compare the triggers specified in descriptions:
- Common triggers
- Unique to Skill1
- Unique to Skill2

### 7. Summary
- Frontmatter status: Identical or Different
- Directory structure: Same or Different
- Content similarity: Percentage match
- Recommendation: Which patterns to follow

## Use Cases

1. **Reviewing Changes**: Compare before/after updates
2. **Understanding Variations**: See how similar skills differ
3. **Template Evaluation**: Check if new skill follows pattern of existing ones
4. **Merge Decisions**: Decide if two skills should be combined
5. **Migration Verification**: Confirm migration changed only intended fields
6. **Learning Patterns**: Study differences between mature and new skills

## Comparing Directory Structure

The comparison highlights structural differences:
```
Skill1 Structure:
  ✓ SKILL.md
  ✓ scripts/ (3 files)
  ✓ references/ (2 files)
  ✗ templates/

Skill2 Structure:
  ✓ SKILL.md
  ✓ scripts/ (5 files)
  ✓ references/ (1 file)
  ✓ templates/ (3 files)
```

## If Script Not Found

Script path: `agent-builder/skills/building-skills/scripts/compare-skills.py`

## Related Commands

- `/agent-builder:skills:update <name>` - Update a skill
- `/agent-builder:skills:enhance <name>` - Get quality score
- `/agent-builder:skills:audit` - Bulk validation
