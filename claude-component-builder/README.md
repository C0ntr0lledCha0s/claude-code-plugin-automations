# Claude Component Builder Plugin

**A comprehensive plugin for building Claude Code agents, skills, slash commands, hooks, and plugins.**

This plugin provides specialized builder agents and command-based orchestration for creating Claude Code extensions. Commands run in the main thread and delegate to builder agents via Task for parallel execution.

## Version 2.4.0 - Streamlined Commands

This release simplifies the command interface:

- **4 Essential Commands**: Only the commands that add real value over natural language
- **Skills Auto-Invoke**: Say "create an agent" and the building-agents skill activates automatically
- **Plugin Orchestration**: Multi-component creation with parallel execution and rollback
- **Deep Analysis Mode**: Single-component quality analysis via `audit --deep`

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
/claude-component-builder:plugin create my-plugin
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

### Commands (4)

| Command | Description |
|---------|-------------|
| `/claude-component-builder:new-plugin [action] [name]` | Plugin operations (create, validate, update) |
| `/claude-component-builder:audit [type\|--all\|--deep path]` | Audit components or deep single-component analysis |
| `/claude-component-builder:validate [path]` | Validate a component file/directory |
| `/claude-component-builder:migrate [type] [name\|--all]` | Migrate to current schema (rare use) |

**Why only 4 commands?** Skills auto-invoke when you describe what you want:
- "Create an agent for code review" → `building-agents` skill activates
- "Update my skill's description" → `building-skills` skill handles it
- "Compare these two agents" → Claude does this naturally

Commands exist only for operations that **need** structured workflows.

## Installation

### As a Local Plugin

```bash
cd ~/.claude/plugins/
git clone <repository-url> claude-component-builder
```

### For a Specific Project

```bash
cp -r claude-component-builder /path/to/your/project/
cd /path/to/your/project
ln -s $(pwd)/claude-component-builder/agents ~/.claude/agents
ln -s $(pwd)/claude-component-builder/skills ~/.claude/skills
ln -s $(pwd)/claude-component-builder/commands ~/.claude/commands
```

## Usage

### Creating Components (Natural Language)

Just describe what you want - skills auto-invoke:

```
"Create an agent for reviewing code quality"
→ building-agents skill activates, creates agents/code-reviewer.md

"Build a skill for analyzing test coverage"
→ building-skills skill activates, creates skills/analyzing-coverage/

"Add a command for running the test suite"
→ building-commands skill activates, creates commands/run-tests.md
```

### Creating Plugins (Command Required)

Multi-component plugins need the orchestration workflow:

```bash
# Create a new plugin with multiple components
/claude-component-builder:new-plugin create my-plugin

# Validate an existing plugin
/claude-component-builder:new-plugin validate my-plugin/

# Update plugin metadata
/claude-component-builder:new-plugin update my-plugin
```

### Auditing Components

```bash
# Audit all components (parallel execution)
/claude-component-builder:audit --all

# Audit specific type
/claude-component-builder:audit agent
/claude-component-builder:audit skill

# Deep analysis of a single component
/claude-component-builder:audit --deep agents/code-reviewer.md
/claude-component-builder:audit --deep skills/building-agents/
```

### Validating Components

```bash
# Validate a specific file
/claude-component-builder:validate .claude/agents/my-agent.md

# Validate a skill directory
/claude-component-builder:validate .claude/skills/my-skill/

# Validate a plugin
/claude-component-builder:validate my-plugin/
```

### Schema Migration (Rare)

```bash
# Migrate all commands to current schema
/claude-component-builder:migrate command --all

# Migrate a specific component
/claude-component-builder:migrate agent old-agent
```

## How It Works

### Natural Language → Skill Auto-Invoke

```
User: "Create an agent for code review"
    |
    v
building-agents skill auto-invokes
    |-- Provides templates, patterns, validation rules
    |-- Claude uses skill knowledge to create agent
    |
    v
Claude creates: agents/code-reviewer.md
    |-- Valid YAML frontmatter
    |-- Proper naming (lowercase-hyphens)
    |-- Minimal tool permissions
```

### Multi-Component Plugin Creation

```
/claude-component-builder:new-plugin create code-review-suite
    |
    v
new-plugin.md command (Main Thread)
    |-- Research: Explores existing patterns
    |-- Plan: Presents template options
    |-- Confirm: Gets user approval
    |-- Structure: Creates directories (sequential)
    |-- Components: Creates agents, skills, commands (PARALLEL)
    |-- Finalize: Generates README, validates (sequential)
    |
    v
Success: Plugin with components created
```

### Project-Wide Audit

```
/claude-component-builder:audit --all
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

### Deep Single-Component Analysis

```
/claude-component-builder:audit --deep agents/code-reviewer.md
    |
    v
Detailed quality scoring (40 points total)
    |-- Schema: 10 pts
    |-- Security: 10 pts
    |-- Quality: 10 pts
    |-- Maintainability: 10 pts
    |
    v
Prioritized improvement recommendations
```

## Validation Scripts

Located in each skill's `scripts/` directory:

```bash
# Validate an agent
python claude-component-builder/skills/building-agents/scripts/validate-agent.py .claude/agents/my-agent.md

# Validate a skill
python claude-component-builder/skills/building-skills/scripts/validate-skill.py .claude/skills/my-skill/

# Validate a command
python claude-component-builder/skills/building-commands/scripts/validate-command.py .claude/commands/my-command.md

# Validate hooks
python claude-component-builder/skills/building-hooks/scripts/validate-hooks.py .claude/hooks.json
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
