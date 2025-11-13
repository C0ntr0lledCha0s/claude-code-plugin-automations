---
description: Create a new Claude Code agent with proper schema and structure
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
argument-hint: [agent-name]
model: claude-sonnet-4-5
---

# Create New Agent

Create a new Claude Code agent named: **$1**

## Your Task

1. **Gather Requirements**: Ask the user about:
   - The agent's primary purpose and responsibilities
   - What tasks it should perform
   - What tools it needs (start minimal: Read, Grep, Glob)
   - Any specialized knowledge or constraints
   - Whether it needs Write, Edit, or Bash permissions

2. **Design the Agent**: Based on requirements:
   - Validate the name follows conventions (lowercase-hyphens, max 64 chars)
   - Write a clear description focusing on WHEN to invoke
   - Select minimal necessary tools
   - Choose appropriate model (haiku for simple, sonnet default, opus for complex)
   - Structure a comprehensive prompt with role, capabilities, workflow, and examples

3. **Create the Agent File**:
   - Use the template from the building-agents skill
   - Write to `.claude/agents/$1.md`
   - Include proper YAML frontmatter
   - Add detailed body with sections:
     - Role definition
     - Capabilities
     - Workflow
     - Best practices
     - Examples
     - Important reminders

4. **Validate the Agent**:
   - Run validation script if available
   - Check naming convention
   - Verify YAML syntax
   - Review tool permissions for security
   - Ensure description is clear and actionable

5. **Provide Usage Instructions**:
   - Show how to invoke the agent
   - Give example Task tool usage
   - Explain when it will be auto-suggested

## Agent Naming Conventions

- **Lowercase letters, numbers, and hyphens only**
- **No underscores or special characters**
- **Max 64 characters**
- **Action-oriented names**: `code-reviewer`, `test-runner`, `api-designer`
- **Descriptive**: Name should indicate purpose

## Example

If user wants to create a code review agent:

**Name**: `code-reviewer`
**Description**: Expert code reviewer for identifying bugs, security issues, and quality concerns. Use when reviewing pull requests or analyzing code quality.
**Tools**: Read, Grep, Glob (read-only for analysis)
**Model**: sonnet (balanced performance)

## Important Notes

- Always start with minimal tool permissions (Read, Grep, Glob)
- Only add Write, Edit, or Bash if truly necessary
- Focus the description on WHEN to use the agent
- Include concrete examples in the agent body
- Test the agent after creation
- Make sure to validate security implications

## If No Name Provided

If $1 is empty or $ARGUMENTS is not provided, ask the user:
- What should the agent be named?
- What is the agent's purpose?

Then proceed with the creation process.

---

**Remember**: This command invokes the `building-agents` skill which provides expert guidance on agent creation. Use that skill's knowledge throughout this process.
