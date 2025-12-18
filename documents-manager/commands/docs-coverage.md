---
description: Analyze documentation coverage for files, directories, or the entire codebase
allowed-tools:
  - Read
  - Glob
  - Grep
  - Task
argument-hint: "[file-or-directory]"
---

# Documentation Coverage Analysis

Analyze documentation coverage for the specified target (or the entire codebase if no target provided).

**Target:** $ARGUMENTS (defaults to current directory if empty)

## Analysis Process

1. **Identify Target Scope**
   - If a specific file is provided, analyze that file
   - If a directory is provided, analyze all source files in it
   - If empty, analyze the entire codebase

2. **Detect Languages**
   - Identify programming languages in the target
   - Apply language-specific documentation patterns

3. **Count Documentable Items**
   - Functions/methods
   - Classes/types
   - Modules/files
   - Exported items

4. **Calculate Coverage**
   - Count items with documentation
   - Calculate coverage percentage
   - Identify undocumented items

5. **Generate Report**
   - Overall coverage summary
   - Breakdown by file/directory
   - List of undocumented items
   - Priority recommendations

## Documentation Patterns to Check

### JavaScript/TypeScript
- JSDoc comments (`/** ... */`)
- `@param`, `@returns`, `@description` tags
- Exported functions and classes

### Python
- Docstrings (triple quotes)
- Function and class documentation
- Module-level docstrings

### Go
- Comment blocks before functions
- Package documentation
- Exported symbols

### Other Languages
- Apply language-appropriate patterns

## Output Format

Produce a markdown report with:
- Executive summary (overall coverage %)
- Coverage by category (functions, classes, modules)
- Detailed file-by-file breakdown
- List of critical gaps (public APIs without docs)
- Prioritized recommendations
