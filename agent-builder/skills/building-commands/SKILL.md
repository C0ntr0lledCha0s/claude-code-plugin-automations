---
name: building-commands
description: Expert at creating and modifying Claude Code slash commands. Auto-invokes when the user wants to create, update, modify, enhance, or validate a slash command, needs help designing command workflows, or wants to understand command arguments and parameters.
version: 1.1.0
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Building Commands Skill

You are an expert at creating Claude Code slash commands. Slash commands are user-triggered workflows that provide parameterized, action-oriented functionality.

## When to Create a Command vs Other Components

**Use a COMMAND when:**
- The user explicitly triggers a specific workflow
- You need parameterized inputs via arguments
- The action is discrete and well-defined
- Users need a simple way to invoke complex operations

**Use a SKILL instead when:**
- You want automatic, context-aware assistance
- The functionality should be "always on"

**Use an AGENT instead when:**
- You need dedicated context and isolation
- The task requires heavy computation

## Command Schema & Structure

### File Location
- **Project-level**: `.claude/commands/command-name.md`
- **User-level**: `~/.claude/commands/command-name.md`
- **Plugin-level**: `plugin-dir/commands/command-name.md`
- **Supports namespacing**: `.claude/commands/git/commit.md` → `/project:git:commit`

### File Format
Single Markdown file with YAML frontmatter and Markdown body.

### Recommended Fields
```yaml
---
description: Brief description of what the command does
allowed-tools: Read, Grep, Glob, Bash
argument-hint: [parameter-description]
---
```

### All Available Fields
```yaml
---
description: Brief description of command functionality
allowed-tools: Read, Write, Edit, Grep, Glob, Bash    # Pre-approved tools
argument-hint: [filename] [options]                    # Parameter guide for users
disable-model-invocation: false                        # Prevent auto-invocation
---
```

### Naming Conventions
- **Lowercase letters, numbers, and hyphens only**
- **No underscores or special characters**
- **Action-oriented**: Use verbs (`review-pr`, `run-tests`, `deploy-app`)
- **Descriptive**: Name should indicate what the command does
- **Namespacing**: Use directories for organization (`git/commit`, `test/run`)

## Command Body Content

The Markdown body contains instructions for Claude to execute when the command is invoked.

### Command Variables

Commands support special variables for arguments:

- **`$1`, `$2`, `$3`, etc.**: Positional arguments
- **`$ARGUMENTS`**: All arguments as a single string

### Template Structure

```markdown
---
description: One-line description of what this command does
allowed-tools: Read, Grep, Bash
argument-hint: [arg1] [arg2]
---

# Command Name

[Brief description of the command's purpose]

## Arguments

- `$1`: Description of first argument
- `$2`: Description of second argument
- Or use `$ARGUMENTS` for all arguments

## Workflow

When this command is invoked:

1. **Step 1**: Action to perform
2. **Step 2**: Action to perform
3. **Step 3**: Action to perform

## Examples

### Example Usage: /command-name value1 value2
Expected behavior:
1. [What happens]
2. [What happens]
3. [Result]

## Important Notes

- Note about usage or constraints
- Note about required context or setup
```

## Creating a Command

### Step 1: Gather Requirements
Ask the user:
1. What action should the command perform?
2. What arguments does it need?
3. What tools are required?
4. Should it work with specific file types or contexts?

### Step 2: Design the Command
- Choose an action-oriented name (lowercase-hyphens)
- Write a clear description for the help system
- Define argument structure
- Select necessary tools
- Plan the workflow

### Step 3: Write the Command File
- Use proper YAML frontmatter
- Document arguments clearly
- Provide step-by-step workflow
- Include usage examples
- Add important notes

### Step 4: Validate the Command
- Check naming convention
- Verify YAML syntax
- Test argument handling
- Review tool permissions
- Ensure description is clear

### Step 5: Test the Command
- Place in `.claude/commands/` directory
- Invoke with arguments: `/command-name arg1 arg2`
- Verify behavior matches expectations
- Test edge cases
- Iterate based on results

## Generator Scripts

This skill includes a helper script to streamline command creation:

### create-command.py - Interactive Command Generator

Full-featured interactive script that guides you through creating a complete slash command.

**Usage:**
```bash
python3 {baseDir}/scripts/create-command.py
```

**Features:**
- Interactive prompts for name, description, tools, model
- Validates naming conventions (action-oriented)
- Handles argument configuration ($1, $2, $ARGUMENTS)
- Generates argument-hint field automatically
- Creates complete command with proper structure
- Preview before saving
- Automatic validation

**Example Session:**
```
⚡ CLAUDE CODE COMMAND GENERATOR
========================================

Command name: run-tests
Description: Runs test suite and reports results
Allowed tools [Read, Grep, Bash]: Read, Grep, Bash
Model [1] haiku / [2] sonnet / [3] opus → 1

Does this command take arguments? (y/n) [y]: y
Argument hint (e.g., '[filename]', '[source] [dest]'): [test-path]

Workflow description: Run tests in specified path and analyze results

✅ Command created: .claude/commands/run-tests.md
```

**What It Creates:**

The generated command file includes:

1. **YAML Frontmatter** - With all specified fields
2. **Command Overview** - Clear description of purpose
3. **Arguments Section** - If command takes arguments
4. **Workflow Section** - Step-by-step execution plan
5. **Examples** - Usage examples with expected behavior
6. **Error Handling** - How to handle missing/invalid arguments
7. **Important Notes** - Usage guidelines and requirements

**Generated Structure:**
```markdown
---
description: Runs test suite and reports results
allowed-tools: Read, Grep, Bash
argument-hint: [test-path]
---

# Run Tests

[Brief description of what this command does and when to use it]

## Arguments

- **`$1`**: [Description of first argument]
- **`$ARGUMENTS`**: Use this to capture all arguments as a single string

## Your Task

[Workflow description provided during creation]

## Workflow

When this command is invoked:

1. **Validate**: Check that required arguments are provided
2. **Process**: Execute the main logic
3. **Output**: Provide clear results to the user

## Examples

### Example Usage
```
/run-tests [example arguments]
```

Expected behavior:
1. [What happens]
2. [What happens]
3. [Result]

## Important Notes

- [Note about usage]
- [Note about requirements]
- [Note about side effects]

## Error Handling

If arguments are missing or invalid:
- Display clear error message
- Show usage example
- Provide guidance for correction
```

**When to Use:**
- Creating new slash commands from scratch
- Need guided workflow with validation
- Want proper argument handling structure
- Building commands with multiple parameters

**After Creation:**
1. Edit the generated command file
2. Customize the workflow section with specific steps
3. Add detailed examples for common use cases
4. Implement error handling logic
5. Test the command: `/command-name args`
6. Iterate based on testing results

## Argument Handling Patterns

### Pattern 1: Single Argument
```yaml
argument-hint: [filename]
```

Body:
```markdown
Process the file: $1
```

Usage: `/process-file data.csv`

### Pattern 2: Multiple Arguments
```yaml
argument-hint: [source] [destination]
```

Body:
```markdown
Copy from $1 to $2
```

Usage: `/copy-file src.txt dest.txt`

### Pattern 3: Flexible Arguments
```yaml
argument-hint: [search-term] [optional-path]
```

Body:
```markdown
Search for "$1" in ${2:-.}
```

Usage: `/search "error" ./src` or `/search "error"`

### Pattern 4: All Arguments
```yaml
argument-hint: [commit-message]
```

Body:
```markdown
Create commit with message: $ARGUMENTS
```

Usage: `/commit Add new feature for user authentication`

## Tool Selection Strategy

### Read-only Commands
```yaml
allowed-tools: Read, Grep, Glob
```
Use for: Analysis, searching, reporting

### File Operations
```yaml
allowed-tools: Read, Write, Edit, Grep, Glob
```
Use for: Code generation, file manipulation

### System Commands
```yaml
allowed-tools: Read, Grep, Glob, Bash
```
Use for: Testing, building, git operations

### Full Workflow
```yaml
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
```
Use for: Complete workflows (test + commit + push)

## Model Selection

- **haiku**: Simple, fast commands (quick searches, simple operations)
- **sonnet**: Default for most commands (balanced performance)
- **opus**: Complex reasoning or critical operations
- **omit**: Use parent model (inherit)

## Common Command Patterns

### Pattern 1: Git Workflow Command
```yaml
---
description: Commit changes and push to remote
allowed-tools: Read, Grep, Bash
argument-hint: [commit-message]
---

# Git Commit and Push

Commit all changes with the message: $ARGUMENTS

Then push to the remote repository.

## Workflow

1. Run `git add .`
2. Create commit with message from $ARGUMENTS
3. Push to origin
4. Report status
```

Usage: `/git-commit-push Add authentication feature`

### Pattern 2: Code Review Command
```yaml
---
description: Review a pull request for quality and security
allowed-tools: Read, Grep, Bash
argument-hint: [PR-number]
---

# Review Pull Request

Review pull request #$1 for:
- Code quality issues
- Security vulnerabilities
- Test coverage
- Documentation

Use GitHub CLI to fetch PR details and analyze changes.
```

Usage: `/review-pr 123`

### Pattern 3: Test Runner Command
```yaml
---
description: Run specific test suite and report results
allowed-tools: Read, Grep, Bash
argument-hint: [test-path]
---

# Run Tests

Execute tests in: $1

Report:
- Pass/fail status
- Coverage metrics
- Failed test details
```

Usage: `/run-tests ./tests/unit`

### Pattern 4: Scaffolding Command
```yaml
---
description: Create a new React component with tests
allowed-tools: Read, Write, Grep, Glob
argument-hint: [component-name]
---

# Create React Component

Generate a new React component: $1

Include:
- Component file: $1.tsx
- Test file: $1.test.tsx
- Storybook file: $1.stories.tsx
```

Usage: `/create-component UserProfile`

### Pattern 5: Documentation Command
```yaml
---
description: Generate API documentation from code
allowed-tools: Read, Write, Grep, Glob, Bash
argument-hint: [source-directory]
---

# Generate API Docs

Generate API documentation for: ${1:-./src}

Output: ./docs/api.md
```

Usage: `/generate-docs ./src/api` or `/generate-docs`

## Namespacing Commands

Organize related commands in subdirectories:

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
    ├── staging.md     → /project:deploy:staging
    └── production.md  → /project:deploy:production
```

Benefits:
- Organized command structure
- Clear naming hierarchy
- Easy to discover related commands

## Security Considerations

When creating commands:

1. **Validate Arguments**: Check for injection attacks
2. **Sanitize Paths**: Prevent path traversal
3. **Restrict Tools**: Minimal necessary permissions
4. **Avoid Secrets**: Never include credentials
5. **Review Bash**: Audit shell commands carefully

### Security Example: Safe File Processing

```markdown
---
description: Process a data file safely
allowed-tools: Read, Bash
---

# Process File

Process file: $1

## Safety Checks

1. Validate $1 is a valid file path
2. Check file exists and is readable
3. Verify file extension is allowed
4. Process with restricted permissions
```

## Validation Checklist

Before finalizing a command, verify:

- [ ] Name is action-oriented, lowercase-hyphens
- [ ] Description clearly states what the command does
- [ ] YAML frontmatter is valid syntax
- [ ] argument-hint describes parameters
- [ ] Arguments ($1, $2, $ARGUMENTS) are documented
- [ ] Tools are minimal and appropriate
- [ ] Model choice is suitable for complexity
- [ ] Workflow is clearly documented
- [ ] Security considerations are addressed
- [ ] Usage examples are provided
- [ ] File is placed in correct directory

## Reference Templates

Full templates and examples are available at:
- `{baseDir}/templates/command-template.md` - Basic command template
- `{baseDir}/references/command-examples.md` - Real-world examples

## Your Role

When the user asks to create a command:

1. Determine if a command is the right choice (vs agent/skill)
2. Gather requirements about action and arguments
3. Design the command structure
4. Generate the command file with proper schema
5. Document arguments and workflow clearly
6. Validate naming, syntax, and security
7. Place the file in the correct location
8. Provide usage examples

Be proactive in:
- Suggesting appropriate tool permissions
- Recommending argument structures
- Identifying security risks
- Organizing commands with namespacing
- Creating clear documentation

Your goal is to help users create powerful, safe, and well-documented slash commands that streamline their workflows.
