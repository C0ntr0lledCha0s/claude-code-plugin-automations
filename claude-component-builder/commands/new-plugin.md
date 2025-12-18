---
description: Create, validate, or update Claude Code plugins with full orchestration. Handles research, planning, user confirmation, and parallel component creation.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task, AskUserQuestion
argument-hint: "[action] [name]"
model: claude-sonnet-4-5
---

# Plugin Orchestrator

Create, validate, or update Claude Code plugins. This command handles the complete workflow including research, planning, user confirmation, and parallel component creation.

**Arguments:**
- `$1` (required): Action - `create`, `validate`, `update`
- `$2` (required for create/update): Plugin name

**Full arguments:** $ARGUMENTS

## Why This Command Exists

Creating plugins involves multiple components (agents, skills, commands, hooks) that must be coordinated. This command:
- Runs in the **main thread** (can use Task tool)
- Orchestrates **parallel creation** of components
- Ensures proper **sequencing** (structure before components)
- Provides **validation** at each step

## Workflow: Create

### Phase 1: Research Existing Patterns

Before creating, explore the codebase:
```
Use Explore agent to find:
- Existing similar plugins
- Naming conventions in use
- Related components that might overlap
```

### Phase 2: Present Options to User

Present 2-3 template options:

```markdown
## 📋 Plugin Options

### Option A: Minimal Plugin
- 1-2 commands only
- Basic structure
- Best for: Simple utilities

### Option B: Standard Plugin (Recommended)
- 1-2 agents + 2-3 commands
- README with examples
- Best for: Most use cases

### Option C: Comprehensive Plugin
- Multiple agents + skills + commands + hooks
- Full documentation
- Best for: Major features

**Questions:**
1. Which template? (A/B/C)
2. What components do you need?
3. Any specific requirements?
```

### Phase 3: Confirm Before Creating

Use AskUserQuestion to get explicit confirmation:
```
Before I create the plugin, please confirm:
- Plugin name: [name]
- Template: [selected]
- Components: [list]

Proceed? (yes/no)
```

### Phase 4: Create Structure (Sequential)

First, create the plugin directory structure:
```
Task → plugin-builder
Prompt: "Create plugin structure '[name]' with directories for [components]"
```

This MUST complete before creating components.

### Phase 5: Create Components (Parallel)

After structure exists, create components in parallel:
```
Task → agent-builder: "Create [agent-name] agent in [plugin]/agents/"
Task → agent-builder: "Create [agent-name] agent in [plugin]/agents/"
Task → skill-builder: "Create [skill-name] skill in [plugin]/skills/"
Task → skill-builder: "Create [skill-name] skill in [plugin]/skills/"
Task → command-builder: "Create [command-name] command in [plugin]/commands/"
Task → hook-builder: "Create hooks in [plugin]/hooks/"
```

**Parallel execution**: These can run simultaneously since they're independent.

### Phase 6: Finalize (Sequential)

After components exist:
```
Task → plugin-builder: "Finalize plugin - generate README, update marketplace.json"
```

### Phase 7: Validate

Run full validation:
```bash
python3 claude-component-builder/skills/building-plugins/scripts/validate-plugin.py [plugin]/.claude-plugin/plugin.json
```

### Phase 8: Report Results

```markdown
## ✅ Plugin Created: [name]

### Structure
```
[name]/
├── .claude-plugin/plugin.json ✅
├── agents/ (2 agents)
├── commands/ (3 commands)
└── README.md ✅
```

### Components Created
| Type | Name | Status |
|------|------|--------|
| Agent | [name] | ✅ |
| Command | [name] | ✅ |

### Validation
- Plugin structure: ✅ Valid
- All components: ✅ Passed

### Installation
```bash
ln -s $(pwd)/[name] ~/.claude/plugins/[name]
```

### Next Steps
1. Test individual components
2. Customize prompts as needed
3. Update README with examples
```

## Workflow: Validate

```
/claude-component-builder:plugin validate my-plugin
```

1. Locate plugin directory
2. Validate plugin.json structure and required fields
3. Check all referenced component paths exist
4. Validate each component:
   - Task → agent-builder: "Validate agents in [plugin]"
   - Task → skill-builder: "Validate skills in [plugin]"
   - Task → command-builder: "Validate commands in [plugin]"
   - Task → hook-builder: "Validate hooks in [plugin]"
5. Check README.md exists and has content
6. Report consolidated results

## Workflow: Update

```
/claude-component-builder:plugin update my-plugin
```

1. Read current plugin.json
2. AskUserQuestion: What would you like to update?
   - Add new components
   - Update metadata (version, description, keywords)
   - Add/modify hooks
   - Update README
3. Execute requested changes
4. Re-validate plugin
5. Report what changed

## Template Structures

### Minimal Plugin
```
plugin-name/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── main.md
└── README.md
```

### Standard Plugin
```
plugin-name/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   └── main-agent.md
├── commands/
│   ├── analyze.md
│   └── fix.md
├── scripts/
│   └── helper.sh
└── README.md
```

### Comprehensive Plugin
```
plugin-name/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── orchestrator.md
│   └── specialist.md
├── skills/
│   └── domain-expertise/
│       ├── SKILL.md
│       └── references/
├── commands/
│   ├── analyze.md
│   ├── fix.md
│   └── report.md
├── hooks/
│   ├── hooks.json
│   └── scripts/
│       └── validate.sh
├── scripts/
└── README.md
```

## Plugin.json Schema

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Plugin description",
  "author": {
    "name": "Author Name",
    "url": "https://github.com/username"
  },
  "repository": "https://github.com/...",
  "homepage": "https://github.com/.../tree/main/plugin-name",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "agents": ["./agents/main-agent.md"],
  "skills": ["./skills/domain-expertise"],
  "commands": ["./commands/analyze.md", "./commands/fix.md"],
  "hooks": "./hooks/hooks.json"
}
```

## Examples

### Create a Code Review Plugin
```
/claude-component-builder:plugin create code-review
```

Interactive prompts will guide you through:
- Selecting template type
- Defining components
- Setting metadata

### Validate an Existing Plugin
```
/claude-component-builder:plugin validate my-plugin
```

### Update Plugin Metadata
```
/claude-component-builder:plugin update my-plugin
```

## Error Handling

### Invalid Action
```
❌ Invalid action: "$1"

Valid actions: create, validate, update
```

### Plugin Already Exists (for create)
```
⚠️ Plugin directory already exists: "$2"

Options:
1. Choose a different name
2. Use `/claude-component-builder:plugin update $2` to modify
3. Delete existing and recreate
```

### Plugin Not Found (for validate/update)
```
❌ Plugin not found: "$2"

Searched locations:
- ./$2/
- ./plugins/$2/
- ~/.claude/plugins/$2/

Use `/claude-component-builder:plugin create $2` to create it.
```

### Component Creation Failed
```
⚠️ Failed to create component: [name]

Error: [details]

Options:
1. Retry this component
2. Skip and continue
3. Rollback (delete created components)
```

## Execution

When invoked:
1. Parse `$1` as action, `$2` as name
2. Validate arguments
3. Route to appropriate workflow (create/validate/update)
4. For create: orchestrate full multi-component creation
5. Return comprehensive results

## Progress Tracking with TodoWrite

**CRITICAL**: Use TodoWrite throughout execution to track multi-phase progress:

```
Phase 1 → TodoWrite: ["Research existing patterns" in_progress]
Phase 2 → TodoWrite: ["Research" completed, "Plan plugin structure" in_progress]
Phase 3 → TodoWrite: ["Plan" completed, "Get user confirmation" in_progress]
Phase 4 → TodoWrite: ["Create plugin structure" in_progress]
Phase 5 → TodoWrite: [
  "Create plugin structure" completed,
  "Create agent-1" in_progress,
  "Create agent-2" in_progress,  # Parallel!
  "Create command-1" in_progress  # Parallel!
]
Phase 6 → TodoWrite: [all components completed, "Finalize plugin" in_progress]
Phase 7 → TodoWrite: ["Validate plugin" in_progress]
Phase 8 → TodoWrite: [all completed]
```

**Why?** Multi-phase workflows need visibility. TodoWrite shows users:
- What's currently happening
- What's running in parallel
- Overall progress toward completion

## Rollback Strategy

### Automatic Recovery Actions

The plugin command attempts automatic recovery when components fail:

1. **Single component fails**: Skip and continue with remaining components
2. **Multiple components fail**: Pause and prompt user for action
3. **Structure creation fails**: Full abort, no cleanup needed

### Manual Rollback by Phase

#### Phase 4 Failure (Structure Creation)
```bash
# Structure partially created - remove directory
rm -rf my-plugin/
# Restart
/claude-component-builder:plugin create my-plugin
```

#### Phase 5 Failure (Component Creation)
```bash
# Some components created, some failed
# Option 1: Retry failed components individually
/claude-component-builder:new agent my-plugin/agents/failed-agent

# Option 2: Delete and restart
rm -rf my-plugin/
/claude-component-builder:plugin create my-plugin
```

#### Phase 6 Failure (Finalization)
```bash
# Components exist but README/manifest incomplete
# Manually finalize:
# 1. Create README.md from template
# 2. Verify plugin.json has all component paths
# 3. Re-validate
python3 claude-component-builder/skills/building-plugins/scripts/validate-plugin.py my-plugin/.claude-plugin/plugin.json
```

#### Marketplace Registration Failure
```bash
# Plugin created but marketplace.json update failed
# 1. Manually add entry to .claude-plugin/marketplace.json
# 2. Validate JSON syntax
python3 -m json.tool .claude-plugin/marketplace.json
# 3. Verify plugin directory path matches source field
```

### Partial Success Handling

When some components succeed and others fail:

```markdown
## Partial Creation Report

### Succeeded (3)
- agents/analyzer.md ✅
- agents/reporter.md ✅
- commands/analyze.md ✅

### Failed (2)
- skills/processing-data/ ❌ (validation error)
- commands/report.md ❌ (write permission)

### Recovery Options
1. **Continue**: Keep successful components, retry failed ones
2. **Rollback**: Delete my-plugin/ and restart
3. **Manual Fix**: Edit failed components and re-validate
```

### Emergency Full Rollback

If everything needs to be undone:

```bash
# 1. Remove plugin directory
rm -rf my-plugin/

# 2. Remove marketplace entry (if added)
# Edit .claude-plugin/marketplace.json to remove the plugin entry

# 3. Validate marketplace
python3 -m json.tool .claude-plugin/marketplace.json

# 4. Verify git status
git status  # Should show removed files only
```

## Key Principles

1. **Research First**: Understand existing patterns before creating
2. **Confirm Before Acting**: Never create without user approval
3. **Parallel When Possible**: Independent components created simultaneously
4. **Sequential When Required**: Structure before components, components before finalization
5. **Validate Always**: Every component validated after creation
6. **Track Progress**: Use TodoWrite to maintain visibility throughout execution
