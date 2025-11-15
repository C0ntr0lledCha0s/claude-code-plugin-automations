---
description: Create a new Claude Code plugin with automated component orchestration
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, AskUserQuestion, SlashCommand
argument-hint: [plugin-name]
model: claude-sonnet-4-5
---

# Create New Plugin (Orchestrated)

Create a new Claude Code plugin with **automated component creation**.

Plugin name: **$1**

## Orchestration Workflow

This command automatically orchestrates the creation of a complete plugin by:
1. ✅ Gathering requirements interactively
2. ✅ Creating plugin structure and manifest
3. ✅ **Automatically invoking component builders** for agents, skills, commands, hooks
4. ✅ Generating comprehensive documentation
5. ✅ Validating the complete plugin

---

## Step 1: Gather Requirements

First, ask the user what components they want to include.

Use the **AskUserQuestion** tool:

```yaml
questions:
  - question: "What type of plugin template would you like to start with?"
    header: "Template"
    multiSelect: false
    options:
      - label: "Minimal"
        description: "Simple plugin with 1-2 commands (best for beginners)"
      - label: "Standard"
        description: "Plugin with agents and commands (most common)"
      - label: "Full"
        description: "Complete plugin with all component types"
      - label: "Custom"
        description: "I'll specify exactly what I need"

  - question: "Which components should this plugin include?"
    header: "Components"
    multiSelect: true
    options:
      - label: "Agents"
        description: "Specialized subagents for complex tasks"
      - label: "Skills"
        description: "Auto-invoked expertise modules"
      - label: "Commands"
        description: "User-triggered slash commands"
      - label: "Hooks"
        description: "Event-driven automation"
```

Based on the user's selections, determine what to create.

## Step 2: Gather Plugin Metadata

Ask for plugin details:

```yaml
questions:
  - question: "What category best describes this plugin?"
    header: "Category"
    multiSelect: false
    options:
      - label: "Development Tools"
        description: "Code generation, testing, linting, formatting"
      - label: "Automation"
        description: "Workflow automation, task automation"
      - label: "Integration"
        description: "External service integrations, APIs"
      - label: "Productivity"
        description: "General productivity enhancements"

  - question: "What is the plugin's primary purpose?"
    header: "Purpose"
    multiSelect: false
    options:
      - label: "I'll type it"
        description: "Let me describe the plugin purpose"
```

Then ask for:
- Plugin name (if not provided in $1)
- Description
- Author name and email
- Keywords (3-5 recommended)

## Step 3: Validate Plugin Name

If plugin name is provided in $1, use it. Otherwise, ask the user.

**Validation rules:**
- Must be lowercase-hyphens only (no underscores, no spaces, no uppercase)
- Max 64 characters
- Descriptive and unique
- No special characters except hyphens

**Example valid names:**
- `code-review-suite`
- `data-analysis-tools`
- `git-workflow-automation`

If name is invalid, explain the issue and ask for a corrected name.

## Step 4: Create Plugin Directory Structure

Create the base plugin structure:

```bash
# Create plugin root and essential directories
mkdir -p $PLUGIN_NAME/.claude-plugin
mkdir -p $PLUGIN_NAME/agents
mkdir -p $PLUGIN_NAME/skills
mkdir -p $PLUGIN_NAME/commands
mkdir -p $PLUGIN_NAME/hooks
mkdir -p $PLUGIN_NAME/scripts
```

## Step 5: Create plugin.json Manifest

Generate the plugin manifest with collected metadata:

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Description from user input",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/username"
  },
  "homepage": "https://github.com/username/plugin-name",
  "repository": "https://github.com/username/plugin-name",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "commands": "./commands/",
  "agents": "./agents/",
  "skills": "./skills/",
  "hooks": ["./hooks/hooks.json"]
}
```

**Use the Write tool** to create `$PLUGIN_NAME/.claude-plugin/plugin.json`

## Step 6: Orchestrate Component Creation

**This is the key orchestration step!** Based on what components the user selected, automatically invoke the appropriate builders.

### For Each Agent Requested

Ask the user: "What should this agent be named and what will it do?"

Then **automatically invoke the agent builder**:

```bash
# Use SlashCommand tool to invoke the agent builder
/agent-builder:agents:new agent-name
```

The agent will be created in `$PLUGIN_NAME/agents/`

**Repeat for each agent** the user wants to create.

### For Each Skill Requested

Ask the user: "What should this skill be named and what expertise will it provide?"

Then **automatically invoke the skill builder**:

```bash
# Use SlashCommand tool to invoke the skill builder
/agent-builder:skills:new skill-name
```

The skill directory will be created in `$PLUGIN_NAME/skills/`

**Repeat for each skill** the user wants to create.

### For Each Command Requested

Ask the user: "What should this command be named and what will it do?"

Then **automatically invoke the command builder**:

```bash
# Use SlashCommand tool to invoke the command builder
/agent-builder:commands:new command-name
```

The command will be created in `$PLUGIN_NAME/commands/`

**Repeat for each command** the user wants to create.

### For Hooks (If Requested)

If the user wants hooks, ask: "What events should trigger hooks?"

Then **automatically invoke the hook builder**:

```bash
# Use SlashCommand tool to invoke the hook builder
/agent-builder:hooks:new hook-configuration
```

The hooks configuration will be created in `$PLUGIN_NAME/hooks/`

## Step 7: Generate README.md

Use the template from `agent-builder/skills/building-plugins/templates/plugin-readme-template.md`

Customize it with:
- Plugin name and description
- List of all created components (agents, skills, commands, hooks)
- Installation instructions
- Basic usage examples for each component
- License information

**Use the Write tool** to create `$PLUGIN_NAME/README.md`

## Step 8: Validate the Plugin

Run the validation script to ensure everything is correct:

```bash
python3 agent-builder/skills/building-plugins/scripts/validate-plugin.py $PLUGIN_NAME/
```

If validation fails:
- Show the errors to the user
- Offer to fix the issues automatically
- Re-run validation after fixes

## Step 9: Summary and Next Steps

Provide a comprehensive summary:

```markdown
✅ Plugin Created Successfully!

📦 Plugin: $PLUGIN_NAME
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 Structure:
$PLUGIN_NAME/
├── .claude-plugin/plugin.json
├── agents/ (X agents)
│   └── [list agent files]
├── skills/ (X skills)
│   └── [list skill directories]
├── commands/ (X commands)
│   └── [list command files]
├── hooks/
│   └── hooks.json
└── README.md

🔧 Components Created:
- X Agents: [names]
- X Skills: [names]
- X Commands: [names]
- Hooks: [configured events]

📝 Next Steps:

1. **Test the plugin**:
   ```bash
   ln -s $(pwd)/$PLUGIN_NAME ~/.claude/plugins/$PLUGIN_NAME
   ```

2. **Customize components**:
   - Edit agent prompts in agents/
   - Enhance skill expertise in skills/
   - Add command logic in commands/

3. **Validate**:
   ```bash
   python3 agent-builder/skills/building-plugins/scripts/validate-plugin.py $PLUGIN_NAME/
   ```

4. **Documentation**:
   - Update README.md with detailed usage
   - Add examples to component files
   - Document configuration options

5. **(Optional) Publish**:
   - Create GitHub repository
   - Tag version: git tag v1.0.0
   - Submit to Claude Code marketplace
```

## Error Handling

### If No Plugin Name Provided

If $1 is empty, ask:
```
"What should your plugin be named? (lowercase-hyphens only, e.g., 'my-awesome-plugin')"
```

### If Plugin Directory Already Exists

If `$PLUGIN_NAME/` directory exists:
```
"⚠️  Directory '$PLUGIN_NAME' already exists.
Would you like to:
1. Choose a different name
2. Overwrite (WARNING: will delete existing)
3. Cancel"
```

### If Component Builder Fails

If any SlashCommand invocation fails:
```
"❌ Failed to create [component-type]: [error]

Would you like to:
1. Retry
2. Skip this component
3. Create manually later"
```

## Template Integration

Optionally, if the user selected a template type, you can:

1. **Copy template files** from `agent-builder/skills/building-plugins/templates/[template-type]/`
2. **Customize** the copied files with user's metadata
3. **Skip component creation** if template already includes them

This provides a faster starting point.

## Important Notes

- ✅ **Automated Orchestration**: This command automatically calls other builders
- ✅ **Interactive**: Uses AskUserQuestion for requirements gathering
- ✅ **Validated**: Runs validation automatically before completion
- ✅ **Comprehensive**: Creates complete plugin with all selected components
- ✅ **Template Support**: Can use templates for faster setup

## Advanced: Custom Component Creation

If the user wants to add components later, remind them they can use:

```bash
# Add more components to existing plugin
cd $PLUGIN_NAME

# Create additional agents
/agent-builder:agents:new new-agent

# Create additional skills
/agent-builder:skills:new new-skill

# Create additional commands
/agent-builder:commands:new new-command

# Update plugin.json if needed
# Re-run validation
python3 ../agent-builder/skills/building-plugins/scripts/validate-plugin.py ./
```

---

## Execution Strategy

When this command is invoked:

1. **Invoke building-plugins skill**: Auto-invoke for plugin expertise
2. **Gather requirements**: Use AskUserQuestion tool
3. **Create structure**: Use Bash and Write tools
4. **Orchestrate components**: Use SlashCommand tool to invoke other builders
5. **Generate docs**: Use templates and Write tool
6. **Validate**: Use Bash to run validation script
7. **Report**: Provide comprehensive summary

**Remember**: The goal is to create a **complete, production-ready plugin** with minimal manual work. Automate everything possible while keeping the user informed of progress.
