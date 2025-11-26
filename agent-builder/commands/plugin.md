---
description: Plugin operations - create, validate, or update Claude Code plugins
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task, AskUserQuestion
argument-hint: "[action] [name]"
model: claude-sonnet-4-5
---

# Plugin Operations

Perform operations on Claude Code plugins using the orchestrator pattern.

**Arguments:**
- `$1` (required): Action - `create`, `validate`, `update`
- `$2` (required for create/update): Plugin name

**Full arguments:** $ARGUMENTS

## Actions

### create
Create a new plugin with components.

### validate
Validate an existing plugin.

### update
Update plugin metadata or add components.

## Workflow: Create

```
/agent-builder:plugin create code-review-suite
    ↓
meta-architect (orchestrator)
    ↓
1. Gather requirements (AskUserQuestion)
2. Create plugin structure
3. Delegate component creation (PARALLEL)
   ├─ agent-builder (for agents)
   ├─ skill-builder (for skills)
   ├─ command-builder (for commands)
   └─ hook-builder (for hooks)
4. Generate README.md
5. Validate complete plugin
    ↓
Report comprehensive results
```

## Workflow: Validate

```
/agent-builder:plugin validate my-plugin
    ↓
1. Check plugin.json
2. Validate all referenced components
3. Check README.md
4. Security assessment
    ↓
Report validation results
```

## Workflow: Update

```
/agent-builder:plugin update my-plugin
    ↓
meta-architect
    ↓
1. Read current plugin.json
2. Gather update requirements
3. Apply changes
4. Re-validate
    ↓
Report update results
```

## Examples

### Create a Plugin
```
/agent-builder:plugin create code-review-suite
```

Interactive prompts will ask:
- Template type (minimal, standard, full)
- Components to include
- Plugin metadata (author, keywords, etc.)

### Validate a Plugin
```
/agent-builder:plugin validate my-plugin
```

### Update a Plugin
```
/agent-builder:plugin update my-plugin
```

## Plugin Structure Created

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── agents/                  # Agent definitions
│   └── *.md
├── skills/                  # Skill directories
│   └── skill-name/
│       └── SKILL.md
├── commands/                # Slash commands
│   └── *.md
├── hooks/                   # Event hooks
│   ├── hooks.json
│   └── scripts/
├── scripts/                 # Helper scripts
└── README.md               # Documentation
```

## Plugin.json Schema

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Plugin description",
  "author": {
    "name": "Author Name",
    "email": "email@example.com",
    "url": "https://github.com/username"
  },
  "repository": "https://github.com/...",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": "./commands/",
  "agents": "./agents/",
  "skills": "./skills/",
  "hooks": ["./hooks/hooks.json"]
}
```

## Template Types

### Minimal
- 1 command
- Basic structure
- For simple plugins

### Standard
- 1-2 agents
- 2-3 commands
- Optional skills
- Most common

### Full
- Multiple agents
- Multiple skills
- Multiple commands
- Hooks
- MCP servers
- For comprehensive plugins

## Validation Checks

| Check | Description |
|-------|-------------|
| plugin.json | Valid JSON, required fields |
| Paths | All referenced paths exist |
| Components | Each component passes validation |
| README | Exists and has content |
| Structure | Follows conventions |

## Output: Create

```markdown
## Plugin Created: [name]

### Structure
```
plugin-name/
├── .claude-plugin/plugin.json ✅
├── agents/ (2 agents)
├── commands/ (3 commands)
└── README.md ✅
```

### Components Created
| Type | Name | Status |
|------|------|--------|
| Agent | code-reviewer | ✅ |
| Agent | security-auditor | ✅ |
| Command | review | ✅ |
| Command | scan | ✅ |
| Command | report | ✅ |

### Validation
- Plugin structure: ✅ Valid
- All components: ✅ Passed
- README: ✅ Generated

### Installation
```bash
ln -s $(pwd)/plugin-name ~/.claude/plugins/plugin-name
```

### Next Steps
1. Customize component prompts
2. Add reference documentation
3. Test all components
4. Update README with examples
```

## Error Handling

### Invalid Action
```
❌ Invalid action: "$1"

Valid actions: create, validate, update
```

### Plugin Exists
```
⚠️ Plugin directory already exists: "$2"

Options:
1. Choose a different name
2. Use /agent-builder:plugin update to modify
3. Delete existing and recreate
```

## Execution

When invoked:
1. Parse action and name from arguments
2. Route to appropriate workflow
3. For create: orchestrate multi-component creation
4. Return comprehensive results
