# Agent Builder Plugin

**A comprehensive meta-agent plugin for building Claude Code agents, skills, slash commands, hooks, and plugins.**

This plugin provides automated scaffolding, validation, and best practices guidance for creating Claude Code extensions. It's essentially a Claude meta-agent - a system that helps Claude build other Claude agents and components.

## Features

- **Automated Component Creation**: Quickly scaffold agents, skills, commands, hooks, and plugins
- **Best Practices Guidance**: Built-in expertise on Claude Code architecture and conventions
- **Validation Tools**: Python scripts to validate schema compliance and naming conventions
- **Template Library**: Pre-built templates for all component types
- **Expert Skills**: Auto-invoked skills that provide specialized knowledge when building components
- **Slash Commands**: Quick commands for creating new components

## Components

### Meta-Architect Agent

**`meta-architect`**: Expert Claude Code architect specializing in designing and building all types of Claude Code components. Provides comprehensive guidance on architecture, schema validation, and best practices.

### Skills

1. **`building-agents`**: Expert at creating Claude Code agents (subagents). Auto-invoked when you want to create a new agent or need help with agent architecture.

2. **`building-skills`**: Expert at creating Claude Code skills. Auto-invoked when you need help designing skill architecture or understanding when to use skills vs agents.

3. **`building-commands`**: Expert at creating slash commands. Auto-invoked when you want to create user-triggered workflows with parameters.

4. **`building-hooks`**: Expert at creating event hooks for automation and validation. Auto-invoked when you need help with event-driven automation.

### Slash Commands

- **`/new-agent [name]`**: Create a new Claude Code agent with proper schema and structure
- **`/new-skill [name]`**: Create a new skill with directory structure and resources
- **`/new-command [name]`**: Create a new slash command for user-triggered workflows
- **`/new-hook [name]`**: Create a new event hook for automation and validation
- **`/new-plugin [name]`**: Create a new plugin with complete directory structure

## Installation

### As a Local Plugin

1. Clone or copy this plugin to your plugins directory:
   ```bash
   cd ~/.claude/plugins/
   git clone <repository-url> agent-builder
   ```

2. The plugin will be automatically loaded by Claude Code

### For a Specific Project

1. Copy the plugin to your project:
   ```bash
   cp -r agent-builder /path/to/your/project/
   ```

2. Link the components to your `.claude` directory:
   ```bash
   cd /path/to/your/project
   ln -s $(pwd)/agent-builder/agents ~/.claude/agents
   ln -s $(pwd)/agent-builder/skills ~/.claude/skills
   ln -s $(pwd)/agent-builder/commands ~/.claude/commands
   ```

## Usage

### Quick Start: Creating Components

#### Create a New Agent
```bash
/new-agent code-reviewer
```
Claude will guide you through:
- Defining the agent's purpose
- Selecting appropriate tools
- Structuring the agent prompt
- Validating the schema

#### Create a New Skill
```bash
/new-skill analyzing-performance
```
Claude will help you:
- Design the skill structure
- Set up directory with scripts and docs
- Write auto-invocation triggers
- Create supporting resources

#### Create a New Command
```bash
/new-command run-tests
```
Claude will assist with:
- Defining arguments and parameters
- Selecting necessary tools
- Creating the command workflow
- Adding usage examples

#### Create a New Hook
```bash
/new-hook validate-writes
```
Claude will guide you through:
- Choosing the event type
- Writing validation logic
- Creating the hook script
- Testing the hook behavior

#### Create a New Plugin
```bash
/new-plugin my-custom-tools
```
Claude will help you:
- Design the plugin structure
- Create the manifest file
- Set up component directories
- Write documentation

### Expert Guidance

Simply ask Claude for help, and the relevant skills will automatically activate:

- "I want to create an agent that reviews security vulnerabilities"
- "Help me build a skill for analyzing CSV files"
- "I need a command to commit and push changes"
- "How do I create a hook to prevent writes to certain directories?"

The skills will auto-invoke and provide expert guidance based on best practices.

### Using the Meta-Architect Agent

For complex architectural decisions or comprehensive guidance:

```
Use the meta-architect agent to help me design a plugin for data analysis
```

The meta-architect has deep knowledge of:
- Component selection (agent vs skill vs command)
- Schema requirements and validation
- Naming conventions and best practices
- Security considerations
- Tool permission strategies

## Component Structure Reference

### Agents
```
.claude/agents/agent-name.md

---
name: agent-name
description: Brief description and when to use
tools: Read, Grep, Glob, Bash
model: sonnet
---

Agent body content...
```

### Skills
```
.claude/skills/skill-name/
├── SKILL.md
├── scripts/
├── references/
└── assets/

---
name: skill-name
description: What it does and when to auto-invoke
version: 1.0.0
allowed-tools: Read, Grep, Glob, Bash
---

Skill body content...
```

### Commands
```
.claude/commands/command-name.md

---
description: What the command does
allowed-tools: Read, Grep, Bash
argument-hint: [arg1] [arg2]
model: sonnet
---

Command body with $1, $2, $ARGUMENTS...
```

### Hooks
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash /path/to/script.sh"
          }
        ]
      }
    ]
  }
}
```

## Validation Scripts

The plugin includes validation scripts for all component types:

- **`validate-agent.py`**: Validates agent YAML frontmatter and schema
- **`validate-skill.py`**: Validates skill directory structure and SKILL.md
- **`validate-command.py`**: Validates command schema and arguments
- **`validate-hooks.py`**: Validates hooks.json structure and events

### Running Validation

```bash
# Validate an agent
python agent-builder/skills/building-agents/scripts/validate-agent.py .claude/agents/my-agent.md

# Validate a skill
python agent-builder/skills/building-skills/scripts/validate-skill.py .claude/skills/my-skill/

# Validate a command
python agent-builder/skills/building-commands/scripts/validate-command.py .claude/commands/my-command.md

# Validate hooks configuration
python agent-builder/skills/building-hooks/scripts/validate-hooks.py .claude/hooks.json
```

## Templates

Pre-built templates are available for all component types:

- `skills/building-agents/templates/agent-template.md`
- `skills/building-skills/templates/skill-template.md`
- `skills/building-commands/templates/command-template.md`
- `skills/building-hooks/templates/hooks-template.json`
- `skills/building-hooks/templates/validation-hook.sh`

Use these as starting points for your own components.

## Best Practices

### Naming Conventions

- **Always use lowercase-hyphens**: `my-agent`, not `my_agent` or `MyAgent`
- **Max 64 characters** for names
- **Agents**: Action-oriented names (`code-reviewer`, `test-runner`)
- **Skills**: Gerund form preferred (`analyzing-data`, `generating-reports`)
- **Commands**: Start with verbs (`run-tests`, `create-component`)

### Tool Permissions

- **Start minimal**: Begin with `Read, Grep, Glob`
- **Add as needed**: Only include Write, Edit, Bash if necessary
- **Security first**: Always validate inputs when using Bash

### Descriptions

- **Agents**: Focus on WHEN to invoke the agent
- **Skills**: Critical for auto-invocation - be very specific about triggers
- **Commands**: Clear one-liner explaining what the command does

### Component Selection

- **Use Agents**: For specialized delegated tasks with independent context
- **Use Skills**: For always-on expertise with automatic invocation
- **Use Commands**: For user-triggered workflows with parameters
- **Use Hooks**: For event-driven automation and validation

## Examples

### Example: Creating a Code Review Agent

```bash
/new-agent security-reviewer
```

Claude will create:
```yaml
---
name: security-reviewer
description: Security expert for identifying vulnerabilities, insecure patterns, and compliance issues. Use when reviewing code for security concerns.
tools: Read, Grep, Glob
model: sonnet
---

# Security Reviewer Agent

You are a security expert specializing in code security analysis...
```

### Example: Creating a Data Analysis Skill

```bash
/new-skill analyzing-csv-data
```

Claude will create:
```
.claude/skills/analyzing-csv-data/
├── SKILL.md
├── scripts/
│   └── csv_analyzer.py
├── references/
│   └── pandas-guide.md
└── assets/
    └── report-template.json
```

### Example: Creating a Git Workflow Command

```bash
/new-command git:commit-push
```

Claude will create:
```markdown
---
description: Commit changes and push to remote repository
allowed-tools: Read, Grep, Bash
argument-hint: [commit-message]
---

# Git Commit and Push

Commit with message: $ARGUMENTS
Then push to remote.
```

Usage: `/git:commit-push Add authentication feature`

## Architecture

This plugin demonstrates advanced Claude Code patterns:

1. **Meta-Programming**: A Claude agent that builds other Claude agents
2. **Skill Composition**: Multiple specialized skills working together
3. **Progressive Disclosure**: Skills reveal resources as needed via `{baseDir}`
4. **Auto-Invocation**: Skills automatically activate when relevant
5. **Validation Pipeline**: Scripts ensure schema compliance
6. **Template Library**: Reusable patterns for common components

## Contributing

To extend this plugin:

1. Add new templates to the `templates/` directories
2. Create new validation rules in the validation scripts
3. Add reference documentation to `references/` directories
4. Extend the skills with additional patterns and examples

## License

MIT License

## Support

For issues, questions, or contributions, please visit:
https://github.com/C0ntr0lledCha0s/claude-code-plugin-automations

---

**Built with Claude Code** - A meta-agent building meta-agents! 🤖🔨
