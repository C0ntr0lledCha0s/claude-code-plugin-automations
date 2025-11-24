---
description: Intelligently commit changes by analyzing file groups, conversation context, and staged changes
allowed-tools: Bash, Read, Grep, Glob
argument-hint: "[mode: all|staged|context|scope]"
---

# Smart Commit

Intelligently analyze and commit changes with automatic file grouping and conventional commit formatting.

## Usage

```bash
/commit-smart              # Interactive mode (default)
/commit-smart all          # Analyze all changes, suggest grouped commits
/commit-smart staged       # Commit only staged changes
/commit-smart context      # Review conversation and commit relevant files
/commit-smart scope        # Commit by functional scope
```

## Arguments

- **First argument** (optional): Commit mode - accessed as first positional parameter
  - `all`: Analyze all changes and suggest grouped commits
  - `staged`: Commit only staged changes
  - `context`: Review conversation history and commit relevant files
  - `scope`: Commit by scope (auth, api, ui, etc.)
  - `interactive`: Interactive mode with confirmation prompts (default)

**Input validation**: Only accepts predefined modes: `all`, `staged`, `context`, `scope`, `interactive`. Invalid inputs are rejected to prevent command injection.

## Workflow

When this command is invoked:

1. **Validate argument** (CRITICAL - prevents command injection):
   - ONLY accept predefined modes from the allowlist
   - Reject any invalid input immediately
   - DO NOT pass user input directly to shell commands

2. **Load issue cache**: Read `.claude/github-workflows/active-issues.json` for tracked issues

3. **Analyze changes**: Run git status and diff to identify all modified files

4. **Detect related issues**:
   - Load `relatedIssues` array from `env.json` (set via `/issue-track select`)
   - Check branch name for issue numbers (e.g., `feature/issue-42`)
   - Detect branch scope and match against issue labels
   - Score issues by relevance:
     - **+100**: Branch-selected issue (in `relatedIssues` array)
     - **+50**: Scope match (issue has branch's detected scope label)
     - **+10-30**: Keyword/file matches

5. **Invoke managing-commits skill**: Delegate to skill for intelligent grouping

6. **Group files**: Skill groups files by scope, type, and relationships

7. **Generate commit messages**: Create conventional commit messages with issue refs:
   - Use `Closes #N` for ALL branch-selected issues (from `relatedIssues` array)
   - Use `Refs #N` for scope-matched or keyword-matched issues
   - Add to commit footer automatically with multiple refs when appropriate

8. **Present plan**: Show user the proposed commits with file lists and issue refs

9. **Get approval**: Ask user to confirm, edit, or cancel

10. **Execute commits**: Create each commit sequentially with proper staging

**Security Note**: The argument MUST be validated against this exact allowlist: `all`, `staged`, `context`, `scope`, `interactive`. If the provided argument does not exactly match one of these strings (or is empty, defaulting to `interactive`), reject it immediately with an error message and stop execution.

## What This Does

This command invokes the `managing-commits` skill to:

1. **Analyze your working directory** for modified, staged, and new files
2. **Group files intelligently** by scope, type, and logical relationships
3. **Generate conventional commit messages** with proper format and issue references
4. **Create atomic commits** that are focused, buildable, and meaningful
5. **Integrate conversation context** to understand what you're working on

The skill uses multiple strategies:
- **Scope-based grouping**: Group by functional area (auth, api, ui, etc.)
- **Type-based grouping**: Group by change type (feat, fix, docs, test, etc.)
- **Relationship grouping**: Keep logically related files together
- **Atomic commit principles**: One logical change per commit

## Examples

**Interactive mode** (asks for confirmation):
```bash
/commit-smart
```

**Commit all changes** (suggests multiple grouped commits):
```bash
/commit-smart all
```

**Commit only staged files**:
```bash
/commit-smart staged
```

**Commit based on conversation** (reviews chat history):
```bash
/commit-smart context
```

## Issue Integration

This command automatically integrates with tracked GitHub issues:

### Before Committing

1. **Reads issue cache**: Loads `.claude/github-workflows/active-issues.json`
2. **Detects branch issue**: Extracts issue number from branch name
3. **Suggests references**: Uses `issue-tracker.py suggest-refs`

### Issue Reference Types

- `Closes #N`: Issue will close when PR merges (use for branch issue)
- `Fixes #N`: Same as Closes (preferred for bugs)
- `Refs #N`: References issue without closing
- `Progresses #N`: Indicates partial progress on issue

### Example with Issue Integration

```bash
# On branch feature/auth (with issues #42, #43 selected via /issue-track select)
/commit-smart

# Output:
Analyzing changes...
Branch scope: auth (scope:auth)
Selected issues: #42 "Implement user authentication", #43 "Add JWT validation"

Found 3 files changed:
  - src/auth/jwt.ts
  - src/auth/types.ts
  - tests/auth/jwt.test.ts

Proposed commit:
feat(auth): add JWT token refresh mechanism

Implements automatic token refresh 5 minutes before expiration
to maintain seamless user sessions.

Closes #42
Closes #43

Create this commit? [y/n]
```

### Sync Issues First

For best results, sync issues and select branch issues before committing:
```bash
/issue-track sync              # Sync issues from GitHub
/issue-track select 42 43      # Select issues for this branch
/commit-smart                  # Commit with auto-refs
```

## Important Notes

- Follows conventional commits format (type(scope): subject)
- Automatically detects related GitHub issues from cache
- Separates implementation, tests, and docs into distinct commits
- Validates commit quality before executing
- Integrates with the `managing-commits` skill for validation
- Uses `issue-tracker.py` script for issue detection

## Error Handling

If the mode argument is invalid or missing from the allowlist:
1. Display error: "Invalid mode: '{provided_value}'. Must be one of: all, staged, context, scope, interactive"
2. Show usage example: `/commit-smart [mode]`
3. Stop execution immediately - do not proceed with analysis or commits
4. Never pass the invalid input to any shell command or git operation

If there are no changes to commit:
1. Display message: "No changes detected. Working directory is clean."
2. Exit gracefully without error

If git operations fail:
1. Display the git error message
2. Explain what went wrong in user-friendly terms
3. Suggest corrective actions

Use this when you want clean, well-organized commits without manual file selection!
