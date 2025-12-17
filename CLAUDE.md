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

**Total: 7 plugins** | 16 agents | 35 skills | 59 commands

#### Development Tools

1. **agent-builder**: Plugin for building Claude Code extensions
   - Location: `./agent-builder/`
   - Purpose: Scaffolds and validates agents, skills, commands, hooks, MCP servers, and plugins
   - Contains: 6 agents, 6 skills, 8 commands, 1 hook, validation scripts
   - Key agents: `agent-builder`, `skill-builder`, `command-builder`, `hook-builder`, `plugin-builder`, `skill-reviewer`
   - Key skills: `building-agents`, `building-skills`, `building-commands`, `building-hooks`, `building-plugins`, `building-mcp-servers`
   - Orchestration: The `plugin` command provides full orchestration for multi-component creation

2. **testing-expert**: Test quality and coverage analysis plugin
   - Location: `./testing-expert/`
   - Purpose: Jest/Playwright expertise, test review, coverage analysis
   - Contains: 1 agent, 3 skills, 3 commands, 1 hook
   - Key skills: `jest-testing`, `playwright-testing`, `analyzing-test-quality`

3. **research-agent**: Deep investigation and analysis plugin
   - Location: `./research-agent/`
   - Purpose: Codebase investigation, pattern analysis, best practices research
   - Contains: 1 agent, 3 skills, 4 commands, 1 hook
   - Key skills: `investigating-codebases`, `analyzing-patterns`, `researching-best-practices`

#### Productivity & Automation

4. **self-improvement**: Self-critique and quality analysis plugin
   - Location: `./self-improvement/`
   - Purpose: Enables Claude to critique its own work and create feedback loops
   - Contains: 1 agent, 5 skills, 9 commands, 1 hook
   - Key skills: `analyzing-response-quality`, `suggesting-improvements`, `improving-components`, `analyzing-component-quality`

5. **github-workflows**: GitHub workflow automation plugin
   - Location: `./github-workflows/`
   - Purpose: Comprehensive GitHub automation for projects, issues, PRs, commits, releases, and branching
   - Contains: 4 agents, 9 skills, 30 commands, 1 hook
   - Key agents: `workflow-orchestrator`, `pr-reviewer`, `issue-manager`, `release-manager`
   - Key skills: `managing-branches`, `managing-commits`, `managing-projects`, `organizing-with-labels`, `reviewing-pull-requests`, `triaging-issues`, `creating-issues`, `managing-relationships`, `managing-worktrees`

6. **project-manager**: Project orchestration and planning plugin
   - Location: `./project-manager/`
   - Purpose: Sprint planning, roadmap creation, task delegation, backlog prioritization
   - Contains: 1 agent, 2 skills, 5 commands, 1 hook
   - Key skills: `planning-sprints`, `coordinating-projects`

#### Domain-Specific

7. **logseq-expert**: Logseq database expertise plugin (in development)
   - Location: `./logseq-expert/`
   - Purpose: Datascript schema expertise, Datalog query building, MD-to-DB migration
   - Contains: 1 agent, 7 skills, 14 commands
   - Key skills: `understanding-db-schema`, `querying-logseq-data`, `building-logseq-plugins`, `migrating-to-db`, `connecting-to-logseq`, `reading-logseq-data`, `writing-to-logseq`

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
- **Naming**: Action-oriented (e.g., `code-reviewer`, `security-auditor`)

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

### CI/CD Pipeline

**This repository has automated CI/CD pipelines** for validation and changelog management. See [CI_CD_GUIDE.md](./CI_CD_GUIDE.md) for full details.

**Quick Commands:**
```bash
# Install dependencies (first time only)
npm install

# Validate all plugins (uses npm scripts)
npm run validate

# Quick validation (bash script)
npm run validate:quick

# Generate/update changelog
npm run changelog

# Bump version and create release
npm run version:patch   # 1.0.0 → 1.0.1
npm run version:minor   # 1.0.0 → 1.1.0
npm run version:major   # 1.0.0 → 2.0.0
```

### Validation

**Quick Validation** (recommended):
```bash
# Validate all plugins at once
bash validate-all.sh
# OR
npm run validate:quick
```

**Comprehensive Validation:**
```bash
# Validate all plugins with detailed output
bash validate-plugins.sh
# OR
npm run validate
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

# Validate plugin.json (full validation)
python3 agent-builder/skills/building-plugins/scripts/validate-plugin.py plugin-name/.claude-plugin/plugin.json

# Validate JSON syntax only
python3 -m json.tool plugin-name/.claude-plugin/plugin.json
python3 -m json.tool .claude-plugin/marketplace.json
```

### Creating Components
Use the agent-builder slash commands:
```bash
/agent-builder:new agent my-agent          # Create a new agent
/agent-builder:new skill my-skill          # Create a new skill
/agent-builder:new command my-command      # Create a new command
/agent-builder:new hook my-hook            # Create a new hook

# For plugins (multi-component), use the dedicated plugin command:
/agent-builder:plugin create my-plugin     # Create a complete plugin with orchestration
/agent-builder:plugin validate my-plugin   # Validate an existing plugin
/agent-builder:plugin update my-plugin     # Update plugin metadata or components

# Other agent-builder commands:
/agent-builder:update agent my-agent       # Update existing component
/agent-builder:validate path/to/component  # Validate component schema
/agent-builder:audit agent                 # Audit components for quality
/agent-builder:enhance agent my-agent      # Get improvement suggestions
/agent-builder:migrate agent my-agent      # Migrate to current schema
/agent-builder:compare agent a b           # Compare two components
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
- `CI_CD_GUIDE.md`: CI/CD pipeline documentation
- `CONTRIBUTING.md`: Contribution guidelines
- `validate-all.sh`: Quick validation script for all plugins
- `validate-plugins.sh`: Comprehensive validation with detailed output

### Agent Builder Plugin
- `agent-builder/agents/agent-builder.md`: Specialized agent builder
- `agent-builder/agents/skill-builder.md`: Specialized skill builder
- `agent-builder/agents/command-builder.md`: Specialized command builder
- `agent-builder/agents/hook-builder.md`: Specialized hook builder
- `agent-builder/agents/plugin-builder.md`: Specialized plugin builder
- `agent-builder/agents/skill-reviewer.md`: Skill quality reviewer
- `agent-builder/skills/building-agents/`: Agent creation expertise
- `agent-builder/skills/building-skills/`: Skill creation expertise
- `agent-builder/skills/building-commands/`: Command creation expertise
- `agent-builder/skills/building-hooks/`: Hook creation expertise
- `agent-builder/skills/building-plugins/`: Plugin creation expertise (includes settings pattern)
- `agent-builder/skills/building-mcp-servers/`: MCP server integration expertise
- `agent-builder/commands/plugin.md`: Plugin orchestration command (handles multi-component creation)
- `agent-builder/skills/*/scripts/validate-*.py`: Validation scripts
- `agent-builder/skills/*/templates/`: Component templates

### Self-Improvement Plugin
- `self-improvement/agents/self-critic.md`: Self-critique agent
- `self-improvement/skills/analyzing-response-quality/`: Quality analysis
- `self-improvement/skills/suggesting-improvements/`: Improvement suggestions
- `self-improvement/skills/creating-feedback-loops/`: Feedback loop creation
- `self-improvement/skills/improving-components/`: Auto-improvement of components
- `self-improvement/skills/analyzing-component-quality/`: Component quality analysis
- `self-improvement/commands/review-my-work.md`: Comprehensive work review
- `self-improvement/commands/quality-check.md`: Quick quality assessment
- `self-improvement/commands/analyze-component.md`: Component analysis
- `self-improvement/commands/improve-component.md`: Auto-improvement
- `self-improvement/AUTOMATED_ANALYSIS.md`: Analysis results and patterns

### GitHub Workflows Plugin
- `github-workflows/agents/workflow-orchestrator.md`: Cross-domain workflow coordinator
- `github-workflows/agents/pr-reviewer.md`: PR review expert
- `github-workflows/agents/issue-manager.md`: Issue lifecycle expert
- `github-workflows/agents/release-manager.md`: Release workflow expert
- `github-workflows/skills/managing-branches/`: Branching strategy expertise
- `github-workflows/skills/managing-commits/`: Commit quality and conventional commits
- `github-workflows/skills/managing-projects/`: GitHub Projects v2 expertise
- `github-workflows/skills/organizing-with-labels/`: Label and milestone management
- `github-workflows/skills/reviewing-pull-requests/`: PR review workflows
- `github-workflows/skills/triaging-issues/`: Issue triage and management
- `github-workflows/skills/creating-issues/`: Issue creation and validation
- `github-workflows/skills/managing-relationships/`: Issue relationships (parent/blocking)
- `github-workflows/commands/`: 30 commands for branches, worktrees, releases, PRs, issues, milestones

### Research Agent Plugin
- `research-agent/agents/investigator.md`: Deep investigation agent
- `research-agent/skills/investigating-codebases/`: Codebase exploration
- `research-agent/skills/analyzing-patterns/`: Pattern analysis
- `research-agent/skills/researching-best-practices/`: Best practices lookup
- `research-agent/commands/investigate.md`: Feature/component investigation
- `research-agent/commands/research.md`: Comprehensive research
- `research-agent/commands/best-practice.md`: Best practices lookup
- `research-agent/commands/compare.md`: Comparative analysis

### Project Manager Plugin
- `project-manager/agents/project-coordinator.md`: Strategic planning advisor
- `project-manager/skills/planning-sprints/`: Sprint planning expertise
- `project-manager/skills/coordinating-projects/`: Project coordination
- `project-manager/commands/plan-sprint.md`: Interactive sprint planning
- `project-manager/commands/roadmap-create.md`: Roadmap creation
- `project-manager/commands/project-status.md`: Project health check
- `project-manager/commands/delegate-task.md`: Task routing
- `project-manager/commands/prioritize-backlog.md`: Backlog prioritization

### Testing Expert Plugin
- `testing-expert/agents/test-reviewer.md`: Test quality reviewer
- `testing-expert/skills/jest-testing/`: Jest framework expertise
- `testing-expert/skills/playwright-testing/`: Playwright E2E testing
- `testing-expert/skills/analyzing-test-quality/`: Test quality analysis
- `testing-expert/commands/review-tests.md`: Test review
- `testing-expert/commands/suggest-tests.md`: Test suggestions
- `testing-expert/commands/analyze-coverage.md`: Coverage analysis

### Logseq Expert Plugin (In Development)
- `logseq-expert/agents/logseq-db-expert.md`: Logseq database expert
- `logseq-expert/skills/understanding-db-schema/`: Datascript schema expertise
- `logseq-expert/skills/querying-logseq-data/`: Datalog query building
- `logseq-expert/skills/building-logseq-plugins/`: Plugin development
- `logseq-expert/skills/migrating-to-db/`: MD-to-DB migration
- `logseq-expert/commands/query.md`: Query assistance
- `logseq-expert/commands/explain.md`: Schema explanation
- `logseq-expert/commands/check-migration.md`: Migration validation

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

### Command-Based Orchestration Pattern
The `plugin` command demonstrates how to orchestrate multiple specialized agents from the main thread. It:
- Runs in the main thread (can use Task tool)
- Researches existing patterns before creating
- Presents options and gets user confirmation
- Creates components in parallel when independent
- Sequences operations when dependencies exist (structure before components)
- Validates all components after creation

This is the preferred pattern for multi-component operations because commands run in the main thread and can directly invoke agents via Task.

### Advisory Agent Pattern
Some agents that cannot directly execute use the **advisory pattern**:
- Agent analyzes the situation and provides recommendations
- Agent returns structured advice to the main thread
- Main thread (or user) executes the recommended actions
- Examples: `project-coordinator`, `workflow-orchestrator`

**Note**: For the agent-builder plugin, this pattern was replaced with command-based orchestration (the `plugin` command) which is more effective because commands can directly execute via Task.

### Subagent Architecture Constraints

**IMPORTANT**: Subagents (agents invoked via the Task tool) **cannot spawn other subagents**. This is a hard architectural restriction in Claude Code to prevent infinite loops.

```
Subagent Architecture:
┌─────────────────────────────────────────┐
│ Main Thread (Claude Code CLI)           │
│ - Can use Task tool ✓                   │
│ - Skills auto-invoke here ✓             │
│                                         │
│   ┌─────────────────────────────────┐   │
│   │ Subagent (invoked via Task)     │   │
│   │ - CANNOT use Task tool ✗        │   │
│   │ - Skills still auto-invoke ✓    │   │
│   │ - Cannot spawn nested agents    │   │
│   └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**Key implications:**
- **Skills and commands CAN use Task** (they run in the main thread)
- **Agents CANNOT effectively use Task** (they run as subagents)
- **Skills auto-invoke in both contexts** (main thread and subagents)

**For orchestration patterns**, use:
1. **Commands** - Run in main thread, can delegate to agents (e.g., `plugin` command)
2. **Skills** - Run in main thread, can coordinate agents if needed
3. **Advisory agents** - Only when direct execution isn't needed (return recommendations)

**DO NOT** add `Task` to agent tools - it creates false orchestration expectations.

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
