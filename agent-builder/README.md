# Agent Builder Plugin

**A comprehensive plugin for building Claude Code agents, skills, slash commands, hooks, and plugins.**

This plugin provides specialized builder agents and command-based orchestration for creating Claude Code extensions. Commands run in the main thread and delegate to builder agents via Task for parallel execution.

## Version 2.2.0 - Command-Based Orchestration

This release uses command-based orchestration with parallel execution:

- **Plugin Command Orchestrator**: The `/agent-builder:plugin` command plans and delegates to specialized builders
- **6 Specialized Builders**: Dedicated agents for agents, skills, commands, hooks, plugins, and skill review
- **8 Unified Commands**: Simplified interface for all component operations
- **Parallel Execution**: Independent operations execute simultaneously for better performance

## Features

- **Command-Based Orchestration**: Plugin command plans and delegates to specialized builders
- **Parallel Execution**: Independent component operations run simultaneously
- **Automated Scaffolding**: Quickly create agents, skills, commands, hooks, and plugins
- **Best Practices Guidance**: Built-in expertise on Claude Code architecture and conventions
- **Validation Tools**: Python scripts to validate schema compliance and naming conventions
- **Template Library**: Pre-built templates for all component types
- **Expert Skills**: Auto-invoked skills that provide specialized knowledge
- **Unified Commands**: Simple interface for all component operations

## Architecture

```
User Request
    |
    v
/agent-builder:plugin create my-plugin
    |
    v
Plugin Command (Main Thread Orchestrator)
    |
    +---> Task: plugin-builder (structure)
    +---> Task: agent-builder (for agents)
    +---> Task: skill-builder (for skills)
    +---> Task: command-builder (for commands)
    +---> Task: hook-builder (for hooks)
    |
    v
Components Created & Validated
```

## Components

### Agents (6)

| Agent | Purpose |
|-------|---------|
| **agent-builder** | Specialized builder for creating/maintaining Claude Code agents |
| **skill-builder** | Specialized builder for creating/maintaining skills (directories + SKILL.md) |
| **command-builder** | Specialized builder for creating/maintaining slash commands |
| **hook-builder** | Specialized builder for creating/maintaining event hooks (security-focused) |
| **plugin-builder** | Specialized builder for plugin structure, manifests, and marketplace registration |
| **skill-reviewer** | Quality reviewer for skills - analyzes triggers, content, progressive disclosure |

### Skills (6)

| Skill | Auto-Invokes When |
|-------|-------------------|
| **building-agents** | User mentions creating/building agents |
| **building-skills** | User mentions creating/building skills |
| **building-commands** | User mentions creating/building commands |
| **building-hooks** | User mentions creating/building hooks |
| **building-plugins** | User mentions creating/building plugins |
| **building-mcp-servers** | User mentions MCP integration, external APIs, tool servers |

### Unified Commands (8)

| Command | Description |
|---------|-------------|
| `/agent-builder:new [type] [name]` | Create a new component |
| `/agent-builder:update [type] [name]` | Update an existing component |
| `/agent-builder:audit [type\|--all]` | Audit components for quality/compliance |
| `/agent-builder:enhance [type] [name]` | Get quality analysis and improvements |
| `/agent-builder:migrate [type] [name\|--all]` | Migrate to current schema |
| `/agent-builder:compare [type] [n1] [n2]` | Compare two components |
| `/agent-builder:validate [path]` | Validate a component file/directory |
| `/agent-builder:plugin [action] [name]` | Plugin operations (create, validate) |

**Types**: `agent`, `skill`, `command`, `hook`, `plugin`

## Installation

### As a Local Plugin

```bash
cd ~/.claude/plugins/
git clone <repository-url> agent-builder
```

### For a Specific Project

```bash
cp -r agent-builder /path/to/your/project/
cd /path/to/your/project
ln -s $(pwd)/agent-builder/agents ~/.claude/agents
ln -s $(pwd)/agent-builder/skills ~/.claude/skills
ln -s $(pwd)/agent-builder/commands ~/.claude/commands
```

## Usage

### Creating Components

```bash
# Create an agent
/agent-builder:new agent code-reviewer

# Create a skill
/agent-builder:new skill analyzing-performance

# Create a command
/agent-builder:new command run-tests

# Create a hook
/agent-builder:new hook validate-writes

# Create a complete plugin
/agent-builder:new plugin my-custom-tools
```

### Auditing Components

```bash
# Audit all components (parallel execution)
/agent-builder:audit --all

# Audit specific type
/agent-builder:audit agent
/agent-builder:audit skill
```

### Updating Components

```bash
# Update a component interactively
/agent-builder:update agent code-reviewer

# Enhance with quality analysis
/agent-builder:enhance skill analyzing-code
```

### Comparing Components

```bash
# Compare two agents
/agent-builder:compare agent code-reviewer security-reviewer
```

### Validating Components

```bash
# Validate a specific file
/agent-builder:validate .claude/agents/my-agent.md

# Validate a skill directory
/agent-builder:validate .claude/skills/my-skill/

# Validate a plugin
/agent-builder:validate my-plugin/
```

### Plugin Operations

```bash
# Create a new plugin
/agent-builder:plugin create my-plugin

# Validate a plugin
/agent-builder:plugin validate my-plugin/
```

## How Orchestration Works

### Single Component Creation

```
/agent-builder:new agent code-reviewer
    |
    v
new.md command
    |-- Validates name: "code-reviewer" (lowercase-hyphens)
    |-- Determines type: agent
    |-- Delegates via Task to: agent-builder agent
    |
    v
agent-builder agent
    |-- Uses building-agents skill resources
    |-- Creates: agents/code-reviewer.md
    |-- Runs validation
    |
    v
Success: Agent created and validated
```

### Multi-Component Plugin Creation

```
/agent-builder:plugin create code-review-suite
    |
    v
plugin.md command (Main Thread)
    |-- Creates plugin structure via Task → plugin-builder (sequential)
    |-- Delegates components (PARALLEL Task calls):
    |   +---> agent-builder: Create reviewer agent
    |   +---> agent-builder: Create security-auditor agent
    |   +---> command-builder: Create review command
    |   +---> command-builder: Create scan command
    |-- Generates README (sequential)
    |-- Validates plugin (sequential)
    |
    v
Success: Plugin with 2 agents, 2 commands created
```

### Project-Wide Audit

```
/agent-builder:audit --all
    |
    v
audit.md command
    |-- Delegates to all builders (PARALLEL Task calls):
    |   +---> agent-builder: Audit all agents
    |   +---> skill-builder: Audit all skills
    |   +---> command-builder: Audit all commands
    |   +---> hook-builder: Audit all hooks
    |
    v
Consolidated Report with all findings
```

## Validation Scripts

Located in each skill's `scripts/` directory:

```bash
# Validate an agent
python agent-builder/skills/building-agents/scripts/validate-agent.py .claude/agents/my-agent.md

# Validate a skill
python agent-builder/skills/building-skills/scripts/validate-skill.py .claude/skills/my-skill/

# Validate a command
python agent-builder/skills/building-commands/scripts/validate-command.py .claude/commands/my-command.md

# Validate hooks
python agent-builder/skills/building-hooks/scripts/validate-hooks.py .claude/hooks.json
```

## Templates

Pre-built templates available in each skill's `templates/` directory:

- `skills/building-agents/templates/agent-template.md`
- `skills/building-skills/templates/skill-template.md`
- `skills/building-commands/templates/command-template.md`
- `skills/building-hooks/templates/hooks-template.json`

## Best Practices

### Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Agents | Action-oriented | `code-reviewer`, `test-runner` |
| Skills | Gerund (verb+ing) | `analyzing-data`, `generating-reports` |
| Commands | Verb-first | `run-tests`, `create-component` |
| Hooks | Event-based | `validate-write`, `log-bash` |
| Plugins | Domain-based | `code-review-suite`, `git-automation` |

### Tool Permissions

- **Start minimal**: Begin with `Read, Grep, Glob`
- **Add as needed**: Only include `Write, Edit, Bash` if necessary
- **Security first**: Always validate inputs when using `Bash`

### Component Selection

| Use Case | Component |
|----------|-----------|
| Specialized delegated task with independent context | Agent |
| Always-on expertise with automatic invocation | Skill |
| User-triggered workflow with parameters | Command |
| Event-driven automation and validation | Hook |
| Bundled related components | Plugin |

### Critical Rules

1. **Skills don't support model field** - skill-builder enforces this
2. **Commands need version aliases for model** (not short aliases like `haiku`)
3. **Hooks require security review** - hook-builder is security-focused
4. **All names: lowercase-hyphens, max 64 chars**

## Migration from v1.x

The old 28 commands have been replaced with 8 unified commands:

| Old Command | New Command |
|-------------|-------------|
| `/agent-builder:agents:new [name]` | `/agent-builder:new agent [name]` |
| `/agent-builder:skills:new [name]` | `/agent-builder:new skill [name]` |
| `/agent-builder:commands:new [name]` | `/agent-builder:new command [name]` |
| `/agent-builder:hooks:new [name]` | `/agent-builder:new hook [name]` |
| `/agent-builder:agents:audit` | `/agent-builder:audit agent` |
| `/agent-builder:agents:enhance [name]` | `/agent-builder:enhance agent [name]` |
| ... | ... |

## Contributing

To extend this plugin:

1. Add new templates to the `templates/` directories
2. Create new validation rules in the validation scripts
3. Add reference documentation to `references/` directories
4. Extend skills with additional patterns and examples

## License

MIT License

## Support

For issues, questions, or contributions:
https://github.com/C0ntr0lledCha0s/claude-code-plugin-automations

---

**Built with Claude Code** - An orchestrator coordinating specialized builders!
