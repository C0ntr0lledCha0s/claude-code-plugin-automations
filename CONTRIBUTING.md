# Contributing to Claude Code Plugins

Thank you for your interest in contributing! This guide will help you create high-quality plugin components that pass validation and follow best practices.

## Before You Start

This repository contains **meta-plugins** - plugins that help build other plugins. The agent-builder plugin provides tools, templates, and validation scripts to ensure quality.

## Development Workflow

### Creating New Components

**ALWAYS use the agent-builder tools** when creating components:

#### 1. Creating an Agent
```bash
# Invoke the building-agents skill by mentioning "create agent" in your request
# Or use the slash command:
/agent-builder:new-agent agent-name

# Then validate:
python3 agent-builder/skills/building-agents/scripts/validate-agent.py plugin-name/agents/agent-name.md
```

#### 2. Creating a Skill
```bash
# Invoke the building-skills skill
/agent-builder:new-skill skill-name

# Then validate:
python3 agent-builder/skills/building-skills/scripts/validate-skill.py plugin-name/skills/skill-name/
```

#### 3. Creating a Command
```bash
# Invoke the building-commands skill
/agent-builder:new-command command-name

# Then validate:
python3 agent-builder/skills/building-commands/scripts/validate-command.py plugin-name/commands/command-name.md
```

#### 4. Creating a Hook
```bash
# Invoke the building-hooks skill
/agent-builder:new-hook hook-name

# Then validate:
python3 agent-builder/skills/building-hooks/scripts/validate-hooks.py plugin-name/hooks/hooks.json
```

### Validation Checklist

Before committing ANY changes to plugin components:

- [ ] **Run validation scripts** on all modified components
- [ ] **Fix ALL critical errors** (security warnings, schema violations)
- [ ] **Address warnings** when possible (naming conventions, missing sections)
- [ ] **Run full validation**: `bash validate-all.sh`
- [ ] **Test the component** manually to ensure it works as expected

### Component Creation Steps

#### For Agents:

1. **Use the template**: Start from `agent-builder/skills/building-agents/templates/agent-template.md`
2. **Required fields**: `name`, `description`
3. **Naming**: Action-oriented, lowercase-hyphens (e.g., `code-reviewer`, `meta-architect`)
4. **Description**: Focus on WHEN to invoke the agent
5. **Validate**: Run the validation script
6. **Test**: Manually invoke the agent with the Task tool

#### For Skills:

1. **Use the template**: Start from `agent-builder/skills/building-skills/templates/skill-template.md`
2. **Required sections**:
   - `## When to Use This Skill` (CRITICAL for auto-invocation)
   - `## Your Capabilities`
3. **Naming**: Gerund form preferred (e.g., `building-agents`, `analyzing-quality`)
4. **Auto-invocation triggers**: Be VERY specific about keywords and contexts
5. **Directory structure**: Create `scripts/`, `references/`, `assets/` as needed
6. **Use `{baseDir}`**: Reference skill resources with this variable
7. **Validate**: Run the validation script
8. **Test**: Trigger auto-invocation by using the keywords in a conversation

#### For Commands:

1. **Use the template**: Start from `agent-builder/skills/building-commands/templates/command-template.md`
2. **Required sections**:
   - `## Arguments` (if command accepts arguments)
   - `## Workflow` (document execution steps)
   - `## Error Handling` (how errors are handled)
3. **Naming**: Verb-first, lowercase-hyphens (e.g., `review-pr`, `create-project`)
4. **Security**: NEVER use `$1`, `$2` followed by backticks in markdown - write "First argument" instead
5. **Validation**: If using Bash tool, validate ALL user input against allowlists
6. **Validate**: Run the validation script
7. **Test**: Invoke the command with various arguments

#### For Hooks:

1. **Use the template**: Start from `agent-builder/skills/building-hooks/templates/hooks-template.json`
2. **Event types**: `PreToolUse`, `PostToolUse`, `UserPromptSubmit`
3. **Hook types**: `command` (bash scripts) or `prompt` (LLM prompts)
4. **Security**: Validate all inputs, avoid dangerous operations
5. **Validate**: Run the validation script
6. **Test**: Trigger the hook event and verify behavior

### Common Pitfalls to Avoid

#### Security Issues

❌ **DON'T**:
```markdown
## Arguments
- `$1` (required): The file path
```

✅ **DO**:
```markdown
## Arguments
- **First argument** (required): The file path
```

**Why**: The pattern `$1` ` triggers the security validator because it looks like a command injection risk.

#### Naming Issues

❌ **DON'T**: Use underscores or camelCase
- `my_agent.md`
- `MySkill/SKILL.md`

✅ **DO**: Use lowercase-hyphens
- `my-agent.md`
- `my-skill/SKILL.md`

#### Missing Validation

❌ **DON'T**: Commit without validating
```bash
git add .
git commit -m "add new component"  # ❌ Will fail pre-commit hook!
```

✅ **DO**: Validate first
```bash
bash validate-all.sh
git add .
git commit -m "feat: add new component"  # ✅ Passes validation
```

### Testing Your Components

#### Testing Agents
```bash
# In Claude Code, use the Task tool to invoke your agent
# Example: "Use the code-reviewer agent to review this code"
```

#### Testing Skills
```bash
# Trigger auto-invocation by using keywords from the skill's description
# Example: If skill auto-invokes on "commit messages", say "help me write a commit message"
```

#### Testing Commands
```bash
# Invoke directly with arguments
/my-command arg1 arg2
```

#### Testing Hooks
```bash
# Trigger the event the hook listens for
# Example: For PreToolUse hooks, use the tool the hook matches
```

### Validation Script Reference

All validation scripts are in `agent-builder/skills/*/scripts/`:

```bash
# Validate an agent
python3 agent-builder/skills/building-agents/scripts/validate-agent.py path/to/agent.md

# Validate a skill
python3 agent-builder/skills/building-skills/scripts/validate-skill.py path/to/skill-dir/

# Validate a command
python3 agent-builder/skills/building-commands/scripts/validate-command.py path/to/command.md

# Validate hooks
python3 agent-builder/skills/building-hooks/scripts/validate-hooks.py path/to/hooks.json

# Validate a plugin manifest
python3 -m json.tool path/to/plugin.json

# Validate marketplace manifest
python3 -m json.tool .claude-plugin/marketplace.json

# Validate ALL components at once
bash validate-all.sh
```

### Pre-Commit Hook

The repository has a pre-commit hook that automatically runs `validate-all.sh` before allowing commits. This prevents invalid components from entering git history.

If validation fails:
1. Read the error messages carefully
2. Fix all critical errors
3. Re-run validation
4. Try committing again

To bypass the hook (NOT recommended):
```bash
git commit --no-verify
```

### Updating Existing Components

When modifying existing components:

1. **Read the component first** to understand its structure
2. **Use agent-builder skills** for guidance (they auto-invoke on keywords like "modify skill")
3. **Validate after changes** to ensure you didn't break anything
4. **Bump version** in `plugin.json` following semantic versioning
5. **Update plugin documentation** (README.md) with changes
6. **Update marketplace.json** if metadata changed

### Adding a New Plugin

When creating an entirely new plugin:

1. **Create directory structure**:
   ```bash
   mkdir -p new-plugin/{.claude-plugin,agents,skills,commands,hooks}
   ```

2. **Create plugin.json manifest**:
   ```json
   {
     "name": "new-plugin",
     "version": "1.0.0",
     "description": "Plugin description",
     "agents": "./agents/",
     "skills": "./skills/",
     "commands": "./commands/",
     "hooks": "./hooks/hooks.json"
   }
   ```

3. **Create components** using agent-builder tools

4. **Write README.md** documenting the plugin

5. **Add to marketplace.json**:
   - Add new entry to `plugins` array
   - Update `metadata.stats.totalPlugins`
   - Update `metadata.stats.lastUpdated`

6. **Validate everything**:
   ```bash
   bash validate-all.sh
   ```

7. **Test thoroughly** before committing

### Getting Help

- **Read templates**: Check `agent-builder/skills/*/templates/` for examples
- **Check references**: Look at `agent-builder/skills/*/references/` for documentation
- **Examine existing components**: Look at agent-builder, self-improvement, or github-workflows plugins for examples
- **Use agent-builder skills**: They auto-invoke when you mention relevant keywords
- **Ask for help**: Mention "agent-builder" or "meta-architect" in your request

### Quality Standards

All contributions should:

- ✅ Pass ALL validation scripts without critical errors
- ✅ Follow naming conventions (lowercase-hyphens)
- ✅ Include comprehensive documentation
- ✅ Have clear, specific descriptions for auto-invocation (skills)
- ✅ Validate user input securely (commands/hooks using Bash)
- ✅ Include error handling
- ✅ Use templates as starting points
- ✅ Follow the principle of progressive disclosure (skills)
- ✅ Be tested manually before committing

### Commit Message Format

Follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`

Example:
```
feat(agent-builder): add new validation for command arguments

Adds comprehensive argument validation to catch command injection
vulnerabilities before they reach production.

Closes #123
```

---

## Questions?

- Check `CLAUDE.md` for repository guidance
- Review `README.md` for installation and usage
- Examine `MARKETPLACE_CONTRIBUTION_WORKFLOW.md` for marketplace contribution process
- Look at existing plugins for examples
- Use agent-builder tools for interactive guidance

Happy contributing! 🎉
