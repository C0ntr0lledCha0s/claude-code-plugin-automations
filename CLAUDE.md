# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## ⚠️ CRITICAL: Always Validate Before Committing

**MANDATORY**: Before creating ANY commit with plugin components (agents, skills, commands, hooks), you MUST:

1. **Run validation scripts** on all modified components:
   ```bash
   # Quick validation of everything
   bash validate-all.sh

   # Or validate individual components:
   python3 agent-builder/skills/building-agents/scripts/validate-agent.py path/to/agent.md
   python3 agent-builder/skills/building-skills/scripts/validate-skill.py path/to/skill/
   python3 agent-builder/skills/building-commands/scripts/validate-command.py path/to/command.md
   python3 agent-builder/skills/building-hooks/scripts/validate-hooks.py path/to/hooks.json
   ```

2. **Fix ALL critical errors** before committing. The pre-commit hook will block commits with validation errors.

3. **Use agent-builder tools** when creating/modifying components:
   - Invoke the `building-agents`, `building-skills`, `building-commands`, or `building-hooks` skills
   - Use templates from `agent-builder/skills/*/templates/`
   - Reference examples from `agent-builder/skills/*/references/`

**Why this matters**: Validation catches security vulnerabilities, naming issues, and structural problems BEFORE they become part of git history.

## Repository Overview

This is a **meta-repository** containing Claude Code plugins. It's essentially Claude building tools for Claude - a collection of meta-agents, skills, commands, and hooks that extend Claude Code's capabilities.

**Key Concept**: This repository contains plugins that help build other plugins. The Agent Builder plugin is a "meta-agent" - an agent that creates other agents.

## Plugin Architecture

### Available Plugins

1. **agent-builder**: Meta-agent plugin for building Claude Code extensions
   - Location: `./agent-builder/`
   - Purpose: Scaffolds and validates agents, skills, commands, hooks, and plugins
   - Contains: 1 agent, 4 skills, 5 commands, validation scripts

2. **self-improvement**: Self-critique and quality analysis plugin
   - Location: `./self-improvement/`
   - Purpose: Enables Claude to critique its own work and create feedback loops
   - Contains: 1 agent, 3 skills, 5 commands, 1 hook

3. **github-workflows**: GitHub workflow automation plugin
   - Location: `./github-workflows/`
   - Purpose: Comprehensive GitHub automation for projects, issues, PRs, and commits
   - Contains: 1 agent, 3 skills, 9 commands, 1 hook

### Plugin Structure Standard

Each plugin follows this structure:
```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Manifest with metadata, version, components
├── agents/                  # Agent definitions (*.md files)
├── skills/                  # Skill directories (skill-name/SKILL.md)
├── commands/                # Slash commands (*.md files)
├── hooks/                   # Event hooks (hooks.json)
└── README.md               # Plugin documentation
```

### Marketplace Compatibility

- Root `.claude-plugin/marketplace.json` defines the marketplace manifest
- Enables one-command installation: `claude plugin install <name>`
- All plugins must have valid `plugin.json` manifests
- Follow strict naming: lowercase-hyphens, max 64 chars, no underscores

## Component Types

### Agents (.md files)
- **Purpose**: Specialized subagents for delegated tasks with independent context
- **Structure**: Single markdown file with YAML frontmatter
- **Required fields**: `name`, `description`
- **Optional fields**: `tools`, `model`
- **Naming**: Action-oriented (e.g., `code-reviewer`, `meta-architect`)

### Skills (directories)
- **Purpose**: Auto-invoked expertise that activates based on context
- **Structure**: Directory containing `SKILL.md` plus optional `scripts/`, `references/`, `assets/`
- **Required fields**: `name`, `description`
- **Optional fields**: `version`, `allowed-tools`, `model`
- **Naming**: Gerund form preferred (e.g., `building-agents`, `analyzing-quality`)
- **Key feature**: Use `{baseDir}` variable to reference skill resources

### Commands (.md files)
- **Purpose**: User-triggered workflows with parameters
- **Structure**: Single markdown file with YAML frontmatter
- **Recommended fields**: `description`, `allowed-tools`, `argument-hint`, `model`
- **Variables**: Access args via `$1`, `$2`, or `$ARGUMENTS`
- **Naming**: Verb-first (e.g., `new-agent`, `review-my-work`)

### Hooks (JSON configuration)
- **Purpose**: Event-driven automation and policy enforcement
- **Structure**: `hooks.json` with matcher patterns and hook definitions
- **Events**: `PreToolUse`, `PostToolUse`, `UserPromptSubmit`
- **Types**: `command` (bash scripts) or `prompt` (LLM prompts)

## Development Commands

### Validation

**Quick Validation** (recommended):
```bash
# Validate all plugins at once
bash validate-all.sh
```

**Individual Component Validation**:
```bash
# Validate agent
python3 agent-builder/skills/building-agents/scripts/validate-agent.py plugin-name/agents/agent-name.md

# Validate skill
python3 agent-builder/skills/building-skills/scripts/validate-skill.py plugin-name/skills/skill-name/

# Validate command
python3 agent-builder/skills/building-commands/scripts/validate-command.py plugin-name/commands/command-name.md

# Validate hooks
python3 agent-builder/skills/building-hooks/scripts/validate-hooks.py plugin-name/hooks/hooks.json

# Validate plugin.json
python3 -m json.tool plugin-name/.claude-plugin/plugin.json

# Validate marketplace.json
python3 -m json.tool .claude-plugin/marketplace.json
```

### Creating Components
Use the agent-builder slash commands:
```bash
/new-agent agent-name       # Create a new agent
/new-skill skill-name       # Create a new skill
/new-command command-name   # Create a new command
/new-hook hook-name         # Create a new hook
/new-plugin plugin-name     # Create a complete plugin
```

### Testing Components
After creating components:
1. Run the appropriate validation script
2. Test manual invocation (for agents/commands)
3. Verify auto-invocation triggers (for skills)
4. Test event triggering (for hooks)

## Key Files & Locations

### Root Level
- `.claude-plugin/marketplace.json`: Marketplace manifest listing all plugins (CRITICAL: must be updated when adding/modifying plugins)
- `README.md`: Main documentation with installation instructions
- `MARKETPLACE_CONTRIBUTION_WORKFLOW.md`: Guide for contributing improvements

### Agent Builder Plugin
- `agent-builder/agents/meta-architect.md`: Expert architect agent
- `agent-builder/skills/building-agents/`: Agent creation expertise
- `agent-builder/skills/building-skills/`: Skill creation expertise
- `agent-builder/skills/building-commands/`: Command creation expertise
- `agent-builder/skills/building-hooks/`: Hook creation expertise
- `agent-builder/skills/*/scripts/validate-*.py`: Validation scripts
- `agent-builder/skills/*/templates/`: Component templates

### Self-Improvement Plugin
- `self-improvement/agents/self-critic.md`: Self-critique agent
- `self-improvement/skills/analyzing-response-quality/`: Quality analysis
- `self-improvement/skills/suggesting-improvements/`: Improvement suggestions
- `self-improvement/skills/creating-feedback-loops/`: Feedback loop creation
- `self-improvement/commands/review-my-work.md`: Comprehensive work review
- `self-improvement/commands/quality-check.md`: Quick quality assessment
- `self-improvement/AUTOMATED_ANALYSIS.md`: Analysis results and patterns

## Important Conventions

### Naming Rules
- **Always lowercase-hyphens**: `my-component`, never `my_component` or `MyComponent`
- **Maximum 64 characters**
- **No special characters** except hyphens
- **Descriptive and unique** within the component type

### Tool Permissions Strategy
- **Start minimal**: Begin with `Read, Grep, Glob`
- **Add progressively**: Only include `Write, Edit, Bash` if necessary
- **Security first**: Always validate inputs when using `Bash`

### Description Best Practices
- **Agents**: Focus on WHEN to invoke (e.g., "Use when reviewing code for security concerns")
- **Skills**: Be specific about auto-invocation triggers (critical for Claude to know when to activate)
- **Commands**: Clear one-liner explaining what happens

## Working with This Repository

### Adding a New Plugin
1. Create plugin directory: `mkdir -p new-plugin/{.claude-plugin,agents,skills,commands,hooks}`
2. Create `plugin.json` manifest with all required fields
3. Add components following naming conventions
4. Write comprehensive README.md
5. Add validation scripts if applicable
6. **Update root `.claude-plugin/marketplace.json`** to register the plugin:
   - Add new plugin entry to the `plugins` array
   - Include all required fields: `name`, `source`, `description`, `version`, `category`, `keywords`, `author`, `repository`, `license`, `homepage`
   - Ensure `source` path matches the actual plugin directory name (e.g., `"./plugin-name"`)
   - Increment `metadata.stats.totalPlugins` count
   - Update `metadata.stats.lastUpdated` to current date
7. Test all components thoroughly

### Modifying Existing Plugins
1. Update component files directly
2. Bump version in `plugin.json` (follow semantic versioning)
3. Re-run validation scripts to ensure compliance
4. Update README.md with changes
5. **Update `.claude-plugin/marketplace.json` if metadata changed**:
   - Update plugin version in marketplace entry
   - Update description, keywords, or other metadata as needed
   - Update `metadata.stats.lastUpdated` to current date
   - Verify `source` path is still correct if plugin was renamed

### Testing Changes
1. Validate schema compliance using validation scripts
2. Test in a separate Claude Code project by symlinking
3. Verify auto-invocation for skills
4. Test all slash commands with various arguments
5. Trigger hooks with relevant events

## Architecture Insights

### Meta-Programming Pattern
The agent-builder plugin demonstrates meta-programming: it's a Claude agent that builds other Claude agents. This creates a self-referential system where the tools can improve themselves.

### Skill Composition
Multiple specialized skills work together. For example, when creating an agent, the `building-agents` skill auto-invokes, providing expertise, templates, and validation.

### Progressive Disclosure
Skills use `{baseDir}` to reference resources that are only loaded when needed, keeping the initial skill definition lightweight.

### Feedback Loop System
The self-improvement plugin creates a meta-feedback loop where Claude can identify its own limitations and contribute improvements back to the plugins.

## Security Considerations

- **Validate all inputs**: Especially in hooks and bash commands
- **Minimal permissions**: Start with read-only tools
- **No hardcoded secrets**: Use environment variables
- **Review bash commands**: Audit for dangerous operations like `rm -rf`
- **Test security**: Try to bypass your own validations

## Version Management

- Follow **semantic versioning**: MAJOR.MINOR.PATCH
- Update `plugin.json` version when making changes
- Update `marketplace.json` version and lastUpdated date
- Document breaking changes in README.md
- Tag releases in git: `git tag v1.0.0`
