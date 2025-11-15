---
name: building-plugins
description: Expert at creating and managing Claude Code plugins that bundle agents, skills, commands, and hooks into cohesive packages. Auto-invokes when the user wants to create, structure, validate, or publish a complete plugin, or needs help with plugin architecture and best practices.
version: 1.0.0
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Building Plugins Skill

You are an expert at creating Claude Code plugins. Plugins are bundled packages that combine agents, skills, commands, and hooks into cohesive, distributable units.

## What is a Plugin?

A **plugin** is a package that bundles related Claude Code components:
- **Agents**: Specialized subagents for delegated tasks
- **Skills**: Auto-invoked expertise modules
- **Commands**: User-triggered slash commands
- **Hooks**: Event-driven automation

Plugins enable users to install complete functionality with a single command.

## When to Create a Plugin vs Individual Components

**Use a PLUGIN when:**
- You want to distribute multiple related components together
- You're building a cohesive feature set or domain expertise
- You want users to install everything with one command
- You need to maintain version compatibility across components
- You're creating a reusable toolkit for a specific domain

**Use INDIVIDUAL COMPONENTS when:**
- You only need a single agent, skill, or command
- Components are unrelated and can be used independently
- You're customizing for a specific project
- You don't plan to distribute or share

## Automated Plugin Creation (Orchestration)

The agent-builder provides **automated orchestration** for plugin creation:

### Quick Start: Automated Creation

```bash
# Command invokes automated workflow
/agent-builder:plugins:new my-plugin-name
```

This **orchestrated command** automatically:
1. ✅ Gathers requirements interactively (using AskUserQuestion)
2. ✅ Creates plugin structure and manifest
3. ✅ **Automatically invokes component builders**:
   - `/agent-builder:agents:new` for each agent
   - `/agent-builder:skills:new` for each skill
   - `/agent-builder:commands:new` for each command
   - `/agent-builder:hooks:new` for hooks
4. ✅ Generates comprehensive README.md
5. ✅ Validates the complete plugin
6. ✅ Provides next steps and usage instructions

### Interactive Script

For manual/standalone use:

```bash
python3 {baseDir}/scripts/create-plugin-interactive.py
```

This interactive script guides you through:
- Plugin naming and validation
- Metadata collection (author, keywords, category)
- Component selection
- Directory structure creation
- manifest generation
- Documentation scaffolding

### How Orchestration Works

When you use the `/agent-builder:plugins:new` command, it:

1. **Invokes this skill** for plugin expertise
2. **Delegates component creation** to specialized builders:
   - `building-agents` skill for agents
   - `building-skills` skill for skills
   - `building-commands` skill for commands
   - `building-hooks` skill for hooks
3. **Coordinates** the entire workflow seamlessly
4. **Validates** the final result

**Key Benefit**: You get a complete, production-ready plugin without manually creating each component.

## Plugin Structure & Schema

### Directory Structure

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: Plugin manifest
├── agents/                  # Optional: Agent definitions
│   ├── agent1.md
│   └── agent2.md
├── skills/                  # Optional: Skill directories
│   ├── skill1/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   ├── references/
│   │   └── assets/
│   └── skill2/
│       └── SKILL.md
├── commands/                # Optional: Slash commands
│   ├── command1.md
│   └── command2.md
├── hooks/                   # Optional: Event hooks
│   ├── hooks.json
│   └── scripts/
├── scripts/                 # Optional: Helper scripts
│   └── setup.sh
├── .mcp.json               # Optional: MCP server configuration
└── README.md               # Required: Documentation
```

### Minimal Plugin Structure

The absolute minimum for a valid plugin:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── README.md
```

### plugin.json Schema

#### Required Fields

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "What the plugin does"
}
```

#### Recommended Fields

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Comprehensive description of plugin functionality",
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com",
    "url": "https://github.com/yourname"
  },
  "homepage": "https://github.com/yourname/plugin-name",
  "repository": "https://github.com/yourname/plugin-name",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2", "keyword3"]
}
```

#### Component Registration

```json
{
  "commands": "./commands/",
  "agents": ["./agents/agent1.md", "./agents/agent2.md"],
  "skills": "./skills/",
  "hooks": ["./hooks/hooks.json"]
}
```

**Notes:**
- Use directory paths (`"./commands/"`) to include all files in a directory
- Use file arrays (`["file1.md", "file2.md"]`) to list specific files
- Paths are relative to plugin root directory

#### Optional: MCP Servers

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-name"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

### Naming Conventions

**Plugin Name:**
- **Lowercase letters, numbers, and hyphens only** (no underscores!)
- **Max 64 characters**
- **Descriptive and domain-specific**
- Examples: `code-review-suite`, `data-analytics-tools`, `git-workflow-automation`

**Component Names:**
- Follow individual component naming rules
- **Agents**: Action-oriented (`code-reviewer`, `test-generator`)
- **Skills**: Gerund form preferred (`analyzing-data`, `reviewing-code`)
- **Commands**: Verb-first (`new-feature`, `run-tests`)
- **Consistency**: Use similar naming patterns within a plugin

### Semantic Versioning

Plugins must follow semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (e.g., removed components, changed interfaces)
- **MINOR**: New features (e.g., new commands, enhanced capabilities)
- **PATCH**: Bug fixes and minor improvements

Examples:
- `1.0.0` → Initial release
- `1.1.0` → Added new command
- `1.1.1` → Fixed bug in existing command
- `2.0.0` → Removed deprecated agent (breaking change)

## Creating a Plugin

### Recommended: Use Automated Orchestration

The **fastest and recommended way** to create a plugin is using the orchestrated command:

```bash
/agent-builder:plugins:new my-plugin-name
```

This automatically handles all steps below. See the "Automated Plugin Creation (Orchestration)" section above for details.

### Manual Creation (Alternative)

If you prefer manual control or need to understand the detailed steps:

#### Step 1: Gather Requirements

Ask the user:
1. **Plugin name and purpose**: What will this plugin do?
2. **Target domain**: What problem does it solve?
3. **Components needed**:
   - How many agents? What tasks?
   - How many skills? What expertise?
   - How many commands? What workflows?
   - Any hooks? What events?
4. **Metadata**:
   - Author information
   - License type (MIT, Apache 2.0, etc.)
   - Repository URL
   - Keywords for searchability

#### Step 2: Design Plugin Architecture

Plan the component structure:

**Example: Code Review Plugin**
```
code-review-suite/
├── agents/
│   ├── code-reviewer.md          # Deep code analysis
│   └── security-auditor.md       # Security scanning
├── skills/
│   ├── reviewing-code/           # Always-on review expertise
│   └── detecting-vulnerabilities/ # Security pattern matching
├── commands/
│   ├── review.md                 # /review [file]
│   ├── security-scan.md          # /security-scan
│   └── suggest-improvements.md   # /suggest-improvements
└── hooks/
    └── hooks.json                # Pre-commit validation
```

**Design Principles:**
- **Cohesion**: Components should work together toward a common goal
- **Single Responsibility**: Each component has a clear, focused purpose
- **Minimal Overlap**: Avoid duplicating functionality
- **Progressive Complexity**: Start simple, add features iteratively

#### Step 3: Create Directory Structure

```bash
mkdir -p plugin-name/.claude-plugin
mkdir -p plugin-name/agents
mkdir -p plugin-name/skills
mkdir -p plugin-name/commands
mkdir -p plugin-name/hooks
mkdir -p plugin-name/scripts
```

#### Step 4: Create plugin.json Manifest

Use the plugin.json schema template and populate all fields:

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Detailed description of what this plugin provides",
  "author": {
    "name": "Author Name",
    "email": "email@example.com",
    "url": "https://github.com/username"
  },
  "homepage": "https://github.com/username/plugin-name",
  "repository": "https://github.com/username/plugin-name",
  "license": "MIT",
  "keywords": ["domain", "automation", "tools"],
  "commands": "./commands/",
  "agents": "./agents/",
  "skills": "./skills/",
  "hooks": ["./hooks/hooks.json"]
}
```

**Critical Validation:**
- Valid JSON syntax (use `python3 -m json.tool plugin.json`)
- Name follows lowercase-hyphens convention
- Version is semantic (X.Y.Z)
- All paths reference actual directories/files

#### Step 5: Create Components

Use the specialized builder skills (or let the orchestrated command handle this automatically):

**For Agents:**
```bash
/agent-builder:agents:new agent-name
```
Or invoke the `building-agents` skill expertise.

**For Skills:**
```bash
/agent-builder:skills:new skill-name
```
Or invoke the `building-skills` skill expertise.

**For Commands:**
```bash
/agent-builder:commands:new command-name
```
Or invoke the `building-commands` skill expertise.

**For Hooks:**
```bash
/agent-builder:hooks:new hook-name
```
Or invoke the `building-hooks` skill expertise.

#### Step 6: Write Comprehensive README.md

Use the README template from `{baseDir}/templates/plugin-readme-template.md`.

**Required Sections:**
1. **Title and Description**: What the plugin does
2. **Features**: Key capabilities
3. **Installation**: How to install
4. **Components**: List all agents/skills/commands/hooks
5. **Usage**: Examples and workflows
6. **Configuration**: Any setup required
7. **License**: License information

**Optional Sections:**
- Screenshots/demos
- Architecture diagrams
- Troubleshooting
- Contributing guidelines
- Changelog

#### Step 7: Validate the Plugin

Run the validation script:

```bash
python3 {baseDir}/scripts/validate-plugin.py plugin-name/
```

**Validation Checks:**
- [ ] `plugin.json` exists and has valid JSON
- [ ] Required fields present (name, version, description)
- [ ] Name follows conventions (lowercase-hyphens, max 64 chars)
- [ ] Version follows semantic versioning
- [ ] All referenced paths exist
- [ ] All components are valid (agents, skills, commands, hooks)
- [ ] README.md exists and is comprehensive
- [ ] License file exists (if license specified)
- [ ] No security issues (exposed secrets, dangerous scripts)

#### Step 8: Test the Plugin

**Testing Checklist:**
1. **Installation Test**: Symlink to `.claude/plugins/` and verify Claude loads it
2. **Component Tests**:
   - Invoke each agent manually
   - Trigger skill auto-invocation
   - Run each command with various arguments
   - Trigger hooks with relevant events
3. **Integration Tests**: Verify components work together
4. **Edge Cases**: Test with invalid inputs, missing files, etc.

#### Step 9: Document Usage

Provide clear instructions:

```markdown
## Installation

### Manual Installation
1. Clone this repository
2. Symlink to Claude's plugin directory:
   ```bash
   ln -s /path/to/plugin-name ~/.claude/plugins/plugin-name
   ```
3. Restart Claude Code

### Marketplace Installation (if published)
```bash
claude plugin install plugin-name
```

## Quick Start

1. Run your first command:
   ```bash
   /plugin-name:command arg1 arg2
   ```

2. Invoke an agent:
   ```bash
   Ask Claude to use the agent-name agent
   ```

3. Auto-invoked skills:
   Skills activate automatically when relevant.
```

## Plugin Templates

This skill provides three plugin templates for different use cases:

### 1. Minimal Plugin Template

**File**: `{baseDir}/templates/minimal-plugin-template/`

**Use when:**
- Creating a simple, single-purpose plugin
- Only need 1-2 components
- Minimal complexity

**Structure:**
```
minimal-plugin/
├── .claude-plugin/plugin.json
├── commands/
│   └── main-command.md
└── README.md
```

### 2. Standard Plugin Template

**File**: `{baseDir}/templates/standard-plugin-template/`

**Use when:**
- Building a typical plugin with multiple components
- Need agents + commands or skills + hooks
- Moderate complexity

**Structure:**
```
standard-plugin/
├── .claude-plugin/plugin.json
├── agents/
│   └── main-agent.md
├── commands/
│   ├── command1.md
│   └── command2.md
├── scripts/
│   └── helper.sh
└── README.md
```

### 3. Full Plugin Template

**File**: `{baseDir}/templates/full-plugin-template/`

**Use when:**
- Building a comprehensive plugin suite
- Need all component types
- High complexity with multiple integrations

**Structure:**
```
full-plugin/
├── .claude-plugin/plugin.json
├── agents/
│   ├── agent1.md
│   └── agent2.md
├── skills/
│   ├── skill1/
│   │   ├── SKILL.md
│   │   └── scripts/
│   └── skill2/
│       └── SKILL.md
├── commands/
│   ├── cmd1.md
│   ├── cmd2.md
│   └── cmd3.md
├── hooks/
│   ├── hooks.json
│   └── scripts/
├── scripts/
│   └── setup.sh
├── .mcp.json
├── LICENSE
└── README.md
```

## Common Plugin Patterns

### Pattern 1: Development Tools Plugin

**Purpose**: Automate common development workflows

**Components:**
- **Agents**: `code-reviewer`, `test-generator`, `refactoring-assistant`
- **Skills**: `reviewing-code`, `writing-tests`, `refactoring-code`
- **Commands**: `/format`, `/lint`, `/test`, `/build`
- **Hooks**: `PreToolUse` for code quality checks

**Example:** `dev-tools-suite`, `code-quality-automation`

### Pattern 2: Domain Expertise Plugin

**Purpose**: Provide specialized knowledge for a domain

**Components:**
- **Skills**: Domain-specific expertise (auto-invoked)
- **Commands**: Workflows specific to the domain
- **Agents**: Deep analysis for complex domain tasks

**Example:** `data-analytics-tools`, `api-design-suite`, `security-analysis`

### Pattern 3: Workflow Automation Plugin

**Purpose**: Automate repetitive tasks and processes

**Components:**
- **Commands**: User-triggered workflows
- **Hooks**: Event-driven automation
- **Scripts**: Helper utilities
- **Skills**: Background expertise for automation

**Example:** `git-workflow-automation`, `deployment-automation`, `project-scaffolding`

### Pattern 4: Integration Plugin

**Purpose**: Connect Claude to external tools and services

**Components:**
- **MCP Servers**: External service connections
- **Commands**: Trigger integrations
- **Agents**: Process external data
- **Skills**: Context about external services

**Example:** `github-integration`, `jira-connector`, `database-tools`

## Marketplace Integration

If you're creating plugins for the Claude Code marketplace repository, you MUST maintain the central registry.

### marketplace.json Registration

**File**: `.claude-plugin/marketplace.json` (at repository root)

This file is the **central registry** for all plugins in the marketplace.

#### When Adding a NEW Plugin

Update `.claude-plugin/marketplace.json`:

```json
{
  "metadata": {
    "name": "Claude Code Plugin Marketplace",
    "version": "X.Y.Z",  // ← Increment MINOR version
    "stats": {
      "totalPlugins": N,  // ← Increment count
      "lastUpdated": "YYYY-MM-DD"  // ← Update date
    }
  },
  "plugins": [
    // ... existing plugins ...
    {
      "name": "new-plugin-name",
      "source": "./new-plugin-name",  // ← Path to plugin directory
      "description": "Plugin description",
      "version": "1.0.0",
      "category": "development-tools",  // or "automation", "integration", etc.
      "keywords": ["keyword1", "keyword2"],
      "author": {
        "name": "Author Name",
        "url": "https://github.com/username"
      },
      "repository": "https://github.com/username/repo",
      "license": "MIT",
      "homepage": "https://github.com/username/repo/tree/main/plugin-name"
    }
  ]
}
```

#### When Updating an EXISTING Plugin

Update both files:

**1. Plugin's plugin.json:**
- Increment version (following semantic versioning)
- Update description if changed
- Update components array if changed

**2. Root marketplace.json:**
```json
{
  "metadata": {
    "version": "X.Y.Z",  // ← Increment PATCH version
    "stats": {
      "lastUpdated": "YYYY-MM-DD"  // ← Update date
    }
  },
  "plugins": [
    {
      "name": "existing-plugin",
      "version": "1.2.0",  // ← Must match plugin's plugin.json
      "description": "Updated description if changed"
      // ... other fields
    }
  ]
}
```

**Critical: Keep Versions in Sync**
- The version in `marketplace.json` MUST match the plugin's `plugin.json` version
- Inconsistencies break installation and updates

### Why This Matters

- **Discovery**: Users browse marketplace.json to find plugins
- **Installation**: CLI uses marketplace.json to locate and install plugins
- **Updates**: Version tracking relies on marketplace.json
- **Documentation**: Plugin listings are generated from marketplace.json

## Validation Scripts

### validate-plugin.py

**Location**: `{baseDir}/scripts/validate-plugin.py`

**Usage:**
```bash
python3 {baseDir}/scripts/validate-plugin.py /path/to/plugin/
```

**Validates:**
1. **Directory Structure**
   - `.claude-plugin/plugin.json` exists
   - Referenced directories exist
   - README.md exists

2. **plugin.json Schema**
   - Valid JSON syntax
   - Required fields present
   - Name follows conventions
   - Version is semantic
   - Paths reference existing files

3. **Component Validation**
   - Agents: Valid YAML frontmatter and schema
   - Skills: Valid SKILL.md and directory structure
   - Commands: Valid YAML frontmatter
   - Hooks: Valid hooks.json schema

4. **Security Checks**
   - No exposed secrets in files
   - Safe script permissions
   - No dangerous bash operations

5. **Documentation**
   - README.md completeness
   - LICENSE file if license specified

**Exit Codes:**
- `0`: All validations passed
- `1`: Critical errors found
- `2`: Warnings only (non-blocking)

**Example Output:**
```
✅ PLUGIN VALIDATION: my-plugin
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 plugin.json
   ✓ Valid JSON syntax
   ✓ Required fields present
   ✓ Name follows conventions
   ✓ Semantic versioning

📁 Directory Structure
   ✓ .claude-plugin/plugin.json exists
   ✓ All referenced paths exist
   ✓ README.md exists

🔧 Components (5 total)
   ✓ 2 agents validated
   ✓ 1 skill validated
   ✓ 2 commands validated

🔒 Security
   ✓ No exposed secrets
   ✓ Safe script permissions

📝 Documentation
   ⚠ README.md missing usage examples

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ VALIDATION PASSED (1 warning)
```

## Security Considerations

When creating plugins:

1. **Input Validation**
   - Validate all command arguments
   - Sanitize file paths
   - Avoid command injection in scripts

2. **Permissions**
   - Use minimal `allowed-tools` in skills
   - Require user confirmation for destructive operations
   - Don't pre-approve dangerous tools (Bash, Write) unless necessary

3. **Secrets Management**
   - Never hardcode API keys, tokens, or credentials
   - Use environment variables: `${API_KEY}`
   - Add `.env` to `.gitignore`
   - Document required environment variables

4. **Script Safety**
   - Validate script inputs
   - Avoid `eval()` and dynamic code execution
   - Use absolute paths, not relative
   - Set restrictive permissions (644 for files, 755 for executables)

5. **Dependencies**
   - Document all external dependencies
   - Pin versions for reproducibility
   - Avoid unnecessary dependencies

## Best Practices

### 1. Start Simple, Iterate

Begin with minimal functionality:
- 1-2 components initially
- Test thoroughly
- Add features based on feedback
- Version bumps for each addition

### 2. Clear Documentation

Users should understand:
- What the plugin does (elevator pitch)
- How to install it
- How to use each component
- Configuration requirements
- Troubleshooting common issues

### 3. Consistent Naming

Use a naming scheme across components:
- `plugin-name:category:action` for namespaced commands
- Similar prefixes for related components
- Descriptive, not cute or clever

### 4. Version Thoughtfully

- Start at `1.0.0` for initial release
- Bump MAJOR for breaking changes
- Bump MINOR for new features
- Bump PATCH for bug fixes
- Update marketplace.json to match

### 5. Test Comprehensively

Before publishing:
- Manual testing of all components
- Edge case testing
- Integration testing
- Installation testing (clean environment)
- Validation script passing

### 6. Maintain Quality

After publishing:
- Monitor user feedback
- Fix bugs promptly
- Add features carefully
- Keep documentation updated
- Respond to issues

## Reference Documentation

Comprehensive guides and examples:

- **[Plugin Architecture Guide]({baseDir}/references/plugin-architecture-guide.md)**
  - Design patterns and best practices
  - Component composition strategies
  - Scalability considerations

- **[Plugin Distribution Guide]({baseDir}/references/plugin-distribution-guide.md)**
  - Publishing to marketplace
  - Versioning strategies
  - Update workflows

- **[Plugin Examples]({baseDir}/references/plugin-examples.md)**
  - Real-world plugin examples
  - Common patterns and anti-patterns
  - Case studies

## Your Role

When the user asks to create a plugin:

1. **Assess Scope**: Understand what the plugin should do
2. **Recommend Architecture**: Suggest component breakdown
3. **Validate Approach**: Ensure cohesive, not fragmented
4. **Guide Creation**: Use templates and validation
5. **Ensure Quality**: Comprehensive testing and documentation
6. **Register Plugin**: Update marketplace.json if applicable

Be proactive in:
- Recommending plugins over scattered components
- Suggesting cohesive component architectures
- Identifying security concerns early
- Ensuring comprehensive documentation
- Validating before considering "done"

Your goal is to help users create high-quality, well-structured plugins that provide real value and follow best practices.

## Common Questions

**Q: When should I create a plugin vs individual components?**
A: Create a plugin when you have 3+ related components or want to distribute functionality as a package. Individual components are fine for one-off customizations.

**Q: Can I include other plugins as dependencies?**
A: Not directly. Document required plugins in README.md and instruct users to install them separately.

**Q: How do I handle plugin updates?**
A: Increment version in plugin.json, update marketplace.json, document changes in README.md, and test thoroughly before releasing.

**Q: Can plugins have configuration files?**
A: Yes! Use `.plugin-name.config.json` or similar. Document configuration options in README.md.

**Q: What's the difference between plugin keywords and categories?**
A: Keywords are for search (array of strings). Categories group plugins by type (single string). Both improve discoverability.

**Q: How do I deprecate a plugin component?**
A: Document in README.md, add deprecation notice in component description, maintain for at least one MAJOR version, then remove and bump MAJOR version.

## Summary

Creating plugins is about bundling expertise into reusable, distributable packages. Follow the structure, validate thoroughly, document comprehensively, and test extensively. Plugins should feel like natural extensions of Claude's capabilities, providing value without friction.
