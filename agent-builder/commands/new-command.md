---
description: Create a new Claude Code slash command for user-triggered workflows
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
argument-hint: [command-name]
model: claude-sonnet-4-5
---

# Create New Command

Create a new Claude Code slash command named: **$1**

## Your Task

1. **Gather Requirements**: Ask the user about:
   - What action should the command perform?
   - What arguments does it need? (e.g., filename, PR number, search term)
   - What tools are required?
   - Should it work with specific file types or contexts?
   - Is it part of a namespace (e.g., git/commit, test/run)?

2. **Design the Command**: Based on requirements:
   - Validate the name follows conventions (lowercase-hyphens, action-oriented)
   - Write a clear description for help system
   - Define argument structure ($1, $2, or $ARGUMENTS)
   - Select necessary tools
   - Choose appropriate model
   - Plan the workflow step-by-step

3. **Handle Namespacing** (if applicable):
   - If command should be in a namespace (e.g., `git/commit`):
     - Create directory: `.claude/commands/git/`
     - File: `.claude/commands/git/commit.md`
     - Invoked as: `/project:git:commit`

4. **Create Command File**:
   - Write to `.claude/commands/$1.md` (or namespaced path)
   - Include YAML frontmatter with:
     - description: Clear one-line description
     - allowed-tools: Minimal necessary tools
     - model: Appropriate model choice
     - argument-hint: Parameter description (e.g., `[filename] [options]`)
   - Add body with:
     - Command purpose
     - Argument documentation ($1, $2, $ARGUMENTS)
     - Workflow steps
     - Usage examples
     - Important notes

5. **Validate the Command**:
   - Run validation script if available
   - Check naming convention (action-oriented)
   - Verify YAML syntax
   - Test argument handling
   - Review tool permissions
   - Ensure description is clear

6. **Provide Usage Instructions**:
   - Show invocation syntax: `/project:command-name arg1 arg2`
   - Give concrete usage examples
   - Explain argument meanings

## Command Naming Conventions

- **Lowercase letters, numbers, and hyphens only**
- **No underscores or special characters**
- **Action-oriented**: Start with verb (`review-pr`, `run-tests`, `deploy-app`, `create-component`)
- **Descriptive**: Name indicates what the command does
- **Namespacing**: Use directories for organization

## Argument Handling

Commands support special variables:

- **`$1`, `$2`, `$3`**: Positional arguments
  ```markdown
  Copy file from $1 to $2
  ```
  Usage: `/copy-file src.txt dest.txt`

- **`$ARGUMENTS`**: All arguments as single string
  ```markdown
  Commit with message: $ARGUMENTS
  ```
  Usage: `/git-commit Add authentication feature`

- **Optional arguments**: Use ${2:-.} syntax
  ```markdown
  Search in ${2:-.}
  ```
  Usage: `/search "term" ./src` or `/search "term"`

## Common Patterns

### Git Workflow Command
```markdown
---
description: Commit changes and push to remote
argument-hint: [commit-message]
allowed-tools: Read, Grep, Bash
---

Commit with message: $ARGUMENTS
Then push to origin.
```

### Code Generation Command
```markdown
---
description: Create a new React component with tests
argument-hint: [component-name]
allowed-tools: Read, Write, Grep, Glob
---

Generate component: $1
Include: $1.tsx, $1.test.tsx, $1.stories.tsx
```

### Analysis Command
```markdown
---
description: Analyze code for security vulnerabilities
argument-hint: [directory]
allowed-tools: Read, Grep, Glob, Bash
---

Scan directory: ${1:-./src}
Report security issues.
```

## Namespacing Commands

Organize related commands:

```
.claude/commands/
├── git/
│   ├── commit.md      → /project:git:commit
│   ├── pr.md          → /project:git:pr
│   └── rebase.md      → /project:git:rebase
├── test/
│   ├── run.md         → /project:test:run
│   └── coverage.md    → /project:test:coverage
└── deploy/
    └── staging.md     → /project:deploy:staging
```

## Security Considerations

- **Validate arguments**: Check for injection attacks
- **Sanitize paths**: Prevent path traversal
- **Restrict tools**: Minimal necessary permissions
- **Avoid secrets**: Never include credentials
- **Review Bash**: Audit shell commands carefully

## Example

If user wants to create a PR review command:

**Name**: `review-pr`
**File**: `.claude/commands/review-pr.md`
**Arguments**: PR number as $1
**Tools**: Read, Grep, Bash (to use gh CLI)
**Description**: Review a pull request for quality and security

```markdown
---
description: Review a pull request for quality and security
allowed-tools: Read, Grep, Bash
argument-hint: [PR-number]
model: claude-sonnet-4-5
---

# Review Pull Request

Review PR #$1 for:
- Code quality
- Security vulnerabilities
- Test coverage

Use GitHub CLI: `gh pr view $1`
```

Usage: `/project:review-pr 123`

## Model Field Guidance

**IMPORTANT**: Commands support version aliases or full IDs, but NOT short aliases:

✅ **Correct formats**:
```yaml
# No model field (recommended - inherits from conversation)
# OR
model: claude-haiku-4-5        # Version alias (auto-updates)
# OR
model: claude-haiku-4-5-20251001  # Full ID (stable)
```

❌ **WRONG - causes API 404 errors**:
```yaml
model: haiku   # Short alias - only works in agents
model: sonnet  # Short alias - only works in agents
```

**Recommendation**: For most commands, omit the model field and let it inherit from the conversation. Only specify when you need specific performance (haiku for speed) or stable behavior (full ID).

## Important Notes

- Commands are user-triggered (not auto-invoked like skills)
- Use argument-hint to guide users
- Document all arguments clearly
- Test with various argument combinations
- Consider edge cases (missing args, invalid input)
- Model field: Use version aliases (claude-haiku-4-5) NOT short aliases (haiku)

## If No Name Provided

If $1 is empty, ask the user:
- What should the command be named?
- What action should it perform?
- What arguments does it need?

Then proceed with the creation process.

---

**Remember**: This command invokes the `building-commands` skill which provides expert guidance on command creation. Use that skill's knowledge throughout this process.
