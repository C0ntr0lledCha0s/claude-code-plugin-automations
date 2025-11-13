---
description: Create a new Claude Code plugin with complete directory structure
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
argument-hint: [plugin-name]
model: claude-sonnet-4-5
---

# Create New Plugin

Create a new Claude Code plugin named: **$1**

## Your Task

1. **Gather Requirements**: Ask the user about:
   - Plugin name and purpose
   - What components will it include? (agents, skills, commands, hooks)
   - Author information
   - License type (MIT, Apache, etc.)
   - Repository URL (if applicable)
   - Keywords for searchability

2. **Design Plugin Structure**: Plan the directory layout:
   ```
   plugin-name/
   ├── .claude-plugin/
   │   └── plugin.json       # Manifest
   ├── agents/               # Optional
   ├── skills/               # Optional
   ├── commands/             # Optional
   ├── hooks/                # Optional
   ├── scripts/              # Optional helper scripts
   └── README.md            # Documentation
   ```

3. **Validate Plugin Name**:
   - Must be lowercase-hyphens only
   - Max 64 characters
   - Descriptive and unique
   - No underscores or special characters

4. **Create Directory Structure**:
   ```bash
   mkdir -p $1/.claude-plugin
   mkdir -p $1/agents
   mkdir -p $1/skills
   mkdir -p $1/commands
   mkdir -p $1/hooks
   mkdir -p $1/scripts
   ```

5. **Create plugin.json Manifest**:
   ```json
   {
     "name": "$1",
     "version": "1.0.0",
     "description": "Plugin description",
     "author": {
       "name": "Author Name",
       "email": "email@example.com",
       "url": "https://github.com/username"
     },
     "homepage": "https://github.com/username/$1",
     "repository": "https://github.com/username/$1",
     "license": "MIT",
     "keywords": ["keyword1", "keyword2"],
     "commands": ["./commands/"],
     "agents": "./agents/",
     "skills": "./skills/",
     "hooks": ["./hooks/hooks.json"]
   }
   ```

6. **Create README.md**:
   Include:
   - Plugin name and description
   - Installation instructions
   - Component list (agents, skills, commands, hooks)
   - Usage examples
   - Configuration options
   - License information

7. **Initialize Components** (based on requirements):
   - Create initial agents if needed
   - Set up skill directories if needed
   - Add starter commands if needed
   - Configure hooks if needed

8. **Validate the Plugin**:
   - Check plugin.json syntax (valid JSON)
   - Verify directory structure
   - Ensure all referenced files exist
   - Validate naming conventions

9. **Provide Usage Instructions**:
   - How to install the plugin
   - How to use included components
   - How to contribute or extend

## Plugin Manifest Schema (plugin.json)

### Required Fields
```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "What the plugin does"
}
```

### Optional Fields
```json
{
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com",
    "url": "https://github.com/yourname"
  },
  "homepage": "https://github.com/yourname/plugin-name",
  "repository": "https://github.com/yourname/plugin-name",
  "license": "MIT",
  "keywords": ["tag1", "tag2", "tag3"],
  "commands": ["./commands/cmd1.md", "./commands/cmd2.md"],
  "agents": "./agents/",
  "skills": "./skills/",
  "hooks": ["./hooks/hooks.json"],
  "mcpServers": {
    "server-name": {
      "command": "executable-path",
      "args": ["arg1", "arg2"],
      "env": {
        "VAR": "value"
      }
    }
  }
}
```

## Plugin Directory Structure

### Minimal Plugin
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── README.md
```

### Full Plugin
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── agent1.md
│   └── agent2.md
├── skills/
│   ├── skill1/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── references/
│   └── skill2/
│       └── SKILL.md
├── commands/
│   ├── cmd1.md
│   └── cmd2.md
├── hooks/
│   ├── hooks.json
│   └── scripts/
│       └── validate.sh
├── scripts/
│   └── setup.sh
├── .mcp.json
└── README.md
```

## Naming Conventions

- **Plugin name**: lowercase-hyphens, max 64 chars
- **Descriptive**: Indicates plugin purpose
- **Unique**: Not conflicting with existing plugins
- **Examples**: `code-review-suite`, `data-analysis-tools`, `git-workflow-automation`

## Example Plugin Types

### Development Tools Plugin
```
dev-tools-plugin/
├── .claude-plugin/plugin.json
├── agents/
│   ├── code-reviewer.md
│   └── test-generator.md
├── commands/
│   ├── format-code.md
│   └── run-linter.md
└── README.md
```

### Data Analysis Plugin
```
data-analytics-plugin/
├── .claude-plugin/plugin.json
├── skills/
│   ├── analyzing-csv/
│   └── generating-reports/
├── commands/
│   └── analyze-dataset.md
└── README.md
```

### Git Workflow Plugin
```
git-workflow-plugin/
├── .claude-plugin/plugin.json
├── commands/
│   ├── git/
│   │   ├── commit.md
│   │   ├── pr.md
│   │   └── rebase.md
├── hooks/
│   ├── hooks.json
│   └── scripts/
│       └── validate-commit.sh
└── README.md
```

## README.md Template

```markdown
# Plugin Name

Brief description of what this plugin does.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

[Installation instructions]

## Components

### Agents
- **agent-name**: Description

### Skills
- **skill-name**: Description

### Commands
- `/command-name`: Description

### Hooks
- **EventName**: Description

## Usage

### Example 1
[Usage example]

### Example 2
[Usage example]

## Configuration

[Configuration options]

## License

MIT License
```

## Validation Checklist

Before finalizing plugin:

- [ ] plugin.json has valid JSON syntax
- [ ] Name is lowercase-hyphens, max 64 chars
- [ ] Version follows semantic versioning (1.0.0)
- [ ] Description is clear and concise
- [ ] Directory structure follows conventions
- [ ] All referenced files exist
- [ ] README.md is complete
- [ ] Components follow naming conventions
- [ ] Scripts are executable if present
- [ ] License is specified

## Important Notes

- Plugins bundle related components for distribution
- Use semantic versioning (major.minor.patch)
- Document all components in README
- Test all components before publishing
- Include clear installation instructions
- Consider adding examples directory

## Marketplace Repository: Maintaining Manifest Files

**If working in the claude-code-plugin-automations (marketplace) repository**, you MUST update TWO manifest files:

### 1. Update Plugin's plugin.json
**File**: `<plugin-name>/.claude-plugin/plugin.json`

When modifying a plugin:
- Increment version number (follow semantic versioning)
- Update description if changed
- Update commands array if commands added/removed
- Update other metadata as needed

### 2. Update Root marketplace.json
**File**: `.claude-plugin/marketplace.json`

**CRITICAL**: This file lists all plugins in the marketplace. You MUST update it when:

**When adding a NEW plugin**:
```json
{
  "metadata": {
    "version": "X.Y.Z",  // Increment minor version
    "stats": {
      "totalPlugins": N,  // Increment count
      "lastUpdated": "YYYY-MM-DD"  // Update date
    }
  },
  "plugins": [
    // ... existing plugins ...
    {
      "name": "new-plugin-name",
      "source": "./new-plugin-name",
      "description": "Plugin description",
      "version": "1.0.0",
      "category": "category-name",
      "keywords": ["keyword1", "keyword2"],
      "author": { /* ... */ },
      "repository": "...",
      "license": "MIT",
      "homepage": "..."
    }
  ]
}
```

**When updating an EXISTING plugin**:
```json
{
  "metadata": {
    "version": "X.Y.Z",  // Increment patch version
    "stats": {
      "lastUpdated": "YYYY-MM-DD"  // Update date
    }
  },
  "plugins": [
    {
      "name": "existing-plugin",
      "description": "Updated description if changed",
      "version": "1.2.0",  // Match plugin's new version
      // Update other fields as needed
    }
  ]
}
```

**Fields to Keep in Sync**:
- Plugin version in marketplace.json MUST match plugin's plugin.json version
- Description should match between both files
- Update lastUpdated date in metadata.stats

**Why This Matters**:
- marketplace.json is the central registry for all plugins
- Users rely on it for plugin discovery and installation
- Inconsistencies break plugin installation and updates
- The marketplace uses this file to display available plugins

## If No Name Provided

If $1 is empty, ask the user:
- What should the plugin be named?
- What is the plugin's purpose?
- What components will it include?

Then proceed with the creation process.

---

**Remember**: Use the building-agents, building-skills, building-commands, and building-hooks skills as needed to create plugin components.
