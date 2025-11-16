# GitHub Workflows Plugin - Development Guide

Comprehensive guide for developing, testing, and maintaining the github-workflows plugin.

## Table of Contents
- [Quick Start](#quick-start)
- [Architecture Overview](#architecture-overview)
- [Development Workflow](#development-workflow)
- [Validation](#validation)
- [Testing](#testing)
- [Creating Components](#creating-components)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Quick Start

**For Contributors:**
1. Clone repository
2. Install dependencies: `npm install`
3. Run validation: `bash validate-all.sh`
4. Run tests: `bash github-workflows/tests/run-all-tests.sh`
5. Make changes
6. Validate again before committing

**For Users:**
- See [README.md](README.md) for installation and usage

---

## Validation Commands

### Validate All Components
```bash
# From repository root
bash validate-all.sh
```

### Validate Individual Components

**Agents:**
```bash
python3 agent-builder/skills/building-agents/scripts/validate-agent.py github-workflows/agents/workflow-orchestrator.md
python3 agent-builder/skills/building-agents/scripts/validate-agent.py github-workflows/agents/pr-reviewer.md
```

**Skills:**
```bash
python3 agent-builder/skills/building-skills/scripts/validate-skill.py github-workflows/skills/managing-commits/
python3 agent-builder/skills/building-skills/scripts/validate-skill.py github-workflows/skills/managing-projects/
python3 agent-builder/skills/building-skills/scripts/validate-skill.py github-workflows/skills/organizing-with-labels/
python3 agent-builder/skills/building-skills/scripts/validate-skill.py github-workflows/skills/triaging-issues/
python3 agent-builder/skills/building-skills/scripts/validate-skill.py github-workflows/skills/reviewing-pull-requests/
```

**Commands:**
```bash
for cmd in github-workflows/commands/*.md; do
  python3 agent-builder/skills/building-commands/scripts/validate-command.py "$cmd"
done
```

**Hooks:**
```bash
python3 agent-builder/skills/building-hooks/scripts/validate-hooks.py github-workflows/hooks/hooks.json
```

**Plugin Manifest:**
```bash
python3 -m json.tool github-workflows/.claude-plugin/plugin.json
```

## Component Locations

- **Agents**: `github-workflows/agents/*.md`
- **Skills**: `github-workflows/skills/*/SKILL.md`
- **Commands**: `github-workflows/commands/*.md`
- **Hooks**: `github-workflows/hooks/hooks.json`
- **Helper Scripts**: `github-workflows/skills/*/scripts/`

## Before Committing

1. Run `bash validate-all.sh` from repository root
2. Fix all critical errors (especially security warnings in commands)
3. Verify the pre-commit hook is enabled (`.git/hooks/pre-commit`)
4. Test modified components manually

## Creating New Components

Use the agent-builder tools:
- `/agent-builder:new-agent <name>` - Create new agent
- `/agent-builder:new-skill <name>` - Create new skill
- `/agent-builder:new-command <name>` - Create new command
- `/agent-builder:new-hook <name>` - Create new hook

Or invoke the skills by mentioning keywords like "create command", "modify skill", etc.

## Testing

- **Skills**: Trigger auto-invocation by mentioning "commits", "projects", "labels", "issues", or "pull requests"
- **Commands**:
  - `/github-workflows:commit-smart` - Smart commit with grouping
  - `/github-workflows:project-create` - Create project board
  - `/github-workflows:pr-review-request` - Request PR review
  - `/github-workflows:issue-triage` - Triage issues
  - `/github-workflows:label-sync` - Sync labels
  - And more...

---

## Architecture Overview

### Component Hierarchy

```
github-workflows/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── agents/                   # Specialized agents (2)
│   ├── workflow-orchestrator.md  # Multi-step workflow coordinator
│   └── pr-reviewer.md            # PR review specialist
├── skills/                   # Auto-invoked expertise (5)
│   ├── managing-projects/        # GitHub Projects v2
│   ├── organizing-with-labels/   # Labels & milestones
│   ├── managing-commits/         # Conventional commits
│   ├── triaging-issues/          # Issue management
│   └── reviewing-pull-requests/  # PR workflows
├── commands/                 # User-triggered workflows (10)
├── hooks/                    # Event-driven automation
│   ├── hooks.json                # Hook configuration
│   └── scripts/                  # Hook executables
└── tests/                    # Integration tests
```

### Key Concepts

**Agents**: Delegated tasks with independent context
- workflow-orchestrator: Coordinates complex multi-step workflows
- pr-reviewer: Comprehensive PR reviews with quality gates

**Skills**: Auto-invoked when keywords detected
- Each skill has SKILL.md + optional scripts/, references/, assets/
- Skills use {baseDir} variable for resource paths

**Commands**: User-triggered with `/github-workflows:command-name`
- Accept arguments validated via allowlists
- Can invoke skills or agents

**Hooks**: Event-driven automation
- PreToolUse: Before tool execution
- PostToolUse: After tool execution
- UserPromptSubmit: On user message (use sparingly!)

---

## Development Workflow

### 1. Setup Development Environment

```bash
# Clone repository
git clone https://github.com/C0ntr0lledCha0s/claude-code-plugin-automations.git
cd claude-code-plugin-automations

# Install dependencies
npm install

# Verify installation
bash validate-all.sh
```

### 2. Make Changes

**Modifying Agents:**
1. Edit `github-workflows/agents/*.md`
2. Update tools, description, or workflow logic
3. Validate: `python3 agent-builder/skills/building-agents/scripts/validate-agent.py github-workflows/agents/AGENT_NAME.md`

**Modifying Skills:**
1. Edit `github-workflows/skills/SKILL_NAME/SKILL.md`
2. Update scripts in `scripts/` directory if needed
3. Validate: `python3 agent-builder/skills/building-skills/scripts/validate-skill.py github-workflows/skills/SKILL_NAME/`

**Modifying Commands:**
1. Edit `github-workflows/commands/*.md`
2. Update argument validation and workflow
3. Validate: `python3 agent-builder/skills/building-commands/scripts/validate-command.py github-workflows/commands/COMMAND_NAME.md`

**Modifying Hooks:**
1. Edit `github-workflows/hooks/hooks.json`
2. Update scripts in `hooks/scripts/` if needed
3. Validate: `python3 agent-builder/skills/building-hooks/scripts/validate-hooks.py github-workflows/hooks/hooks.json`

### 3. Testing Changes

**Run validation:**
```bash
bash validate-all.sh
```

**Run integration tests:**
```bash
bash github-workflows/tests/run-all-tests.sh
```

**Manual testing:**
```bash
# Test skills by mentioning keywords
"Review my commits"        # Triggers managing-commits
"Create a project board"   # Triggers managing-projects
"Triage this issue"        # Triggers triaging-issues

# Test commands directly
/github-workflows:commit-smart all
/github-workflows:project-create "Test Board" kanban
/github-workflows:pr-review-request 123
```

### 4. Commit Changes

Use conventional commits:
```bash
git add .
/commit-smart context    # Smart commit based on conversation

# Or manually:
git commit -m "fix(hooks): improve error handling in update-board-on-merge"
```

### 5. Submit Pull Request

```bash
git push origin feature/your-feature
gh pr create --title "feat(component): description" --body "..."
```

---

## Validation

### Quick Validation
```bash
# Validate everything
bash validate-all.sh

# Validate specific plugin
bash validate-all.sh github-workflows
```

### Component-Specific Validation

**Agents:**
```bash
python3 agent-builder/skills/building-agents/scripts/validate-agent.py \
  github-workflows/agents/workflow-orchestrator.md
```

**Skills:**
```bash
python3 agent-builder/skills/building-skills/scripts/validate-skill.py \
  github-workflows/skills/managing-commits/
```

**Commands:**
```bash
python3 agent-builder/skills/building-commands/scripts/validate-command.py \
  github-workflows/commands/commit-smart.md
```

**Hooks:**
```bash
python3 agent-builder/skills/building-hooks/scripts/validate-hooks.py \
  github-workflows/hooks/hooks.json
```

**JSON Files:**
```bash
python3 -m json.tool github-workflows/.claude-plugin/plugin.json
```

### CI/CD Validation

The GitHub Actions workflow (`.github/workflows/validate-plugins.yml`) automatically validates:
- All plugin manifests
- JSON syntax
- Agent definitions
- Skill definitions
- Command definitions
- Hook configurations
- Security issues (hardcoded paths, secrets)

---

## Testing

### Integration Tests

**Run all tests:**
```bash
cd github-workflows/tests
bash run-all-tests.sh
```

**Run specific test suite:**
```bash
bash test-hooks.sh       # Test hook configuration
bash test-graphql.sh     # Test GraphQL operations
```

### Manual Testing Checklist

**Agents:**
- [ ] workflow-orchestrator can coordinate multi-step workflows
- [ ] pr-reviewer can review PRs with quality gates
- [ ] Agents have Write/Edit permissions
- [ ] Agents can invoke commands and skills

**Skills:**
- [ ] managing-commits triggers on commit-related questions
- [ ] managing-projects handles GitHub Projects v2 operations
- [ ] organizing-with-labels manages labels and milestones
- [ ] triaging-issues handles issue management
- [ ] reviewing-pull-requests integrates with self-improvement

**Commands:**
- [ ] All commands validate input arguments
- [ ] Commands provide helpful error messages
- [ ] Commands execute workflows correctly
- [ ] Command descriptions are accurate

**Hooks:**
- [ ] Hooks use ${PLUGIN_DIR} not hardcoded paths
- [ ] Hook scripts have proper error handling
- [ ] Hooks trigger on correct events
- [ ] No performance-killing UserPromptSubmit hooks

### Test Coverage

Current test suites cover:
- Hook configuration validation
- Hook script existence and permissions
- Path variable usage
- Error handling in scripts
- GraphQL retry logic
- Exponential backoff implementation
- Authentication checks

---

## Creating Components

### Creating a New Agent

Use agent-builder:
```bash
/agent-builder:agents:new my-agent-name
```

Or manually:
1. Create `github-workflows/agents/my-agent.md`
2. Add YAML frontmatter:
   ```yaml
   ---
   name: my-agent
   description: What this agent does and when to use it
   capabilities: ["capability1", "capability2"]
   tools: Bash, Read, Write, Edit, Grep, Glob
   model: sonnet
   ---
   ```
3. Add agent instructions
4. Update `github-workflows/.claude-plugin/plugin.json`
5. Validate and test

### Creating a New Skill

Use agent-builder:
```bash
/agent-builder:skills:new my-skill-name
```

Or manually:
1. Create `github-workflows/skills/my-skill/`
2. Create `SKILL.md` with frontmatter
3. Add `scripts/`, `references/`, `assets/` as needed
4. Use `{baseDir}` for resource paths
5. Validate and test

### Creating a New Command

Use agent-builder:
```bash
/agent-builder:commands:new my-command
```

Or manually:
1. Create `github-workflows/commands/my-command.md`
2. Add YAML frontmatter with argument validation
3. Document workflow and security
4. Update `plugin.json`
5. Validate and test

### Creating Helper Scripts

**Bash scripts:**
```bash
#!/usr/bin/env bash
set -euo pipefail

# Add retry logic for robustness
# Use {baseDir} or relative paths
# Validate inputs
# Provide clear error messages
```

**Python scripts:**
```python
#!/usr/bin/env python3
import sys
import json

# Validate inputs
# Use try/except for error handling
# Return clear exit codes
```

---

## Troubleshooting

### Common Issues

**Issue: "Command not found" when running slash command**
- Verify command is in `plugin.json`
- Check command file exists in `commands/`
- Ensure plugin is enabled in `.claude/settings.json`

**Issue: "Skill not triggering automatically"**
- Check skill description has clear auto-invocation keywords
- Verify skill is in `skills/` directory with `SKILL.md`
- Test with explicit skill-related questions

**Issue: "Hook not executing"**
- Verify `hooks.json` syntax is valid
- Check hook scripts have execute permissions: `chmod +x hooks/scripts/*.sh`
- Ensure hooks use `${PLUGIN_DIR}` not hardcoded paths
- Check matcher patterns match the tool being used

**Issue: "GraphQL operations failing"**
- Verify GitHub CLI is authenticated: `gh auth status`
- Check repository permissions
- Test with retry logic disabled to see actual error
- Verify GraphQL syntax in queries

**Issue: "Validation errors"**
- Run specific validator to see detailed error
- Common issues:
  - Missing required fields in frontmatter
  - Hardcoded paths instead of variables
  - Unsafe input handling in commands
  - Invalid JSON syntax

### Debug Mode

Enable verbose output:
```bash
# For bash scripts
bash -x github-workflows/hooks/scripts/update-board-on-merge.sh PR_NUMBER

# For GraphQL operations
export RETRY_MAX_ATTEMPTS=1  # Disable retry to see errors
```

### Getting Help

1. Check this DEVELOPMENT.md
2. Review [README.md](README.md)
3. Check [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)
4. Search [GitHub Issues](https://github.com/C0ntr0lledCha0s/claude-code-plugin-automations/issues)
5. Ask in [Discussions](https://github.com/C0ntr0lledCha0s/claude-code-plugin-automations/discussions)

---

## Best Practices

### Code Quality

- **Always validate input** in commands before passing to shell
- **Use allowlists** for argument validation (never use user input directly)
- **Add error handling** (`set -euo pipefail` in bash, try/except in Python)
- **Add retry logic** for network operations (GraphQL, API calls)
- **Use variables** instead of hardcoded paths (`${PLUGIN_DIR}`, `{baseDir}`)

### Documentation

- **Keep descriptions clear** and specific about when to use components
- **Provide examples** in skills and command documentation
- **Document breaking changes** in commit messages
- **Update README** when adding features
- **Add inline comments** for complex logic

### Testing

- **Test before committing** using validation scripts
- **Add integration tests** for new features
- **Test manually** with realistic scenarios
- **Verify auto-invocation** triggers work correctly
- **Check performance** (especially hooks)

### Version Management

- **Increment versions** when making changes:
  - Patch (1.1.0 → 1.1.1): Bug fixes
  - Minor (1.1.0 → 1.2.0): New features, backward compatible
  - Major (1.1.0 → 2.0.0): Breaking changes
- **Keep versions synchronized** across plugin and skills
- **Document changes** in commit messages
- **Update changelog** for releases

### Security

- **Validate all inputs** especially in commands and hooks
- **Never log sensitive data** (tokens, passwords, etc.)
- **Use ${PLUGIN_DIR}** instead of hardcoded paths
- **Check permissions** before executing operations
- **Audit bash commands** for injection vulnerabilities
- **Review hooks carefully** as they run automatically

### Performance

- **Minimize UserPromptSubmit hooks** (they run on every message!)
- **Use matchers** to conditionally execute hooks
- **Cache expensive operations** (GitHub API calls, GraphQL queries)
- **Add retry logic** with exponential backoff
- **Keep skills focused** to avoid unnecessary invocations

---

## Release Process

1. **Update versions** in all components
2. **Run full validation**: `bash validate-all.sh`
3. **Run all tests**: `bash github-workflows/tests/run-all-tests.sh`
4. **Update CHANGELOG**: Document all changes
5. **Create release commit**: `feat(release): bump to v1.2.0`
6. **Tag release**: `git tag v1.2.0`
7. **Push**: `git push && git push --tags`
8. **Create GitHub release** with changelog

---

## Additional Resources

- **Plugin Architecture**: See [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)
- **P0 Fixes**: See [P0_FIXES_SUMMARY.md](P0_FIXES_SUMMARY.md)
- **Validation Results**: See [VALIDATION_REPORT.md](VALIDATION_REPORT.md)
- **Claude Code Docs**: https://code.claude.com/docs

---

**Questions?** Open an issue or discussion on GitHub!
