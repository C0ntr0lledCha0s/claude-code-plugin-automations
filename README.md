# Claude Code Plugins

A collection of plugins and meta-agents for [Claude Code](https://claude.ai/code), Anthropic's official CLI for Claude. These plugins extend Claude's capabilities with specialized agents, skills, commands, and hooks.

## 🚀 What is Claude Code?

Claude Code is an interactive CLI tool that helps with software engineering tasks. It supports:
- **Agents**: Specialized subagents for delegated tasks
- **Skills**: Auto-invoked expertise modules
- **Slash Commands**: User-triggered workflows
- **Hooks**: Event-driven automation
- **Plugins**: Bundled collections of the above

## 📦 Available Plugins

### Agent Builder (Meta-Agent)

**A meta-agent for building other Claude agents!**

The Agent Builder plugin provides comprehensive tools for creating Claude Code extensions. It includes expert agents, auto-invoked skills, validation scripts, and templates for all component types.

**Features:**
- 🤖 Meta-architect agent for expert guidance
- 🛠️ 4 specialized skills that auto-invoke when building components
- ⚡ 5 slash commands for quick scaffolding
- ✅ Validation scripts for schema compliance
- 📝 Complete template library
- 🔒 Security-focused best practices

**Quick Start:**
```bash
# Create a new agent
/new-agent code-reviewer

# Create a new skill
/new-skill analyzing-data

# Create a new command
/new-command run-tests

# Create a new hook
/new-hook validate-writes

# Create a complete plugin
/new-plugin my-tools
```

[See full documentation →](./agent-builder/README.md)

### Self-Improvement Plugin

**Claude critiquing Claude - A feedback loop for continuous improvement!**

The Self-Improvement plugin enables Claude to critique its own work, identify quality issues, and create feedback loops for continuous learning. It includes a self-critic agent and skills for quality analysis, improvement suggestions, and feedback loops.

**Features:**
- 🔍 Self-critic agent for honest, constructive feedback
- 📊 Quality analysis across 6 dimensions (correctness, completeness, clarity, efficiency, security, usability)
- 💡 Actionable improvement suggestions with before/after examples
- 🔄 Feedback loop systems for continuous learning
- ⚡ Quick quality checks and comprehensive reviews
- 📈 Pattern tracking and learning from mistakes

**Quick Start:**
```bash
# Comprehensive review of recent work
/review-my-work

# Quick quality assessment
/quality-check
```

**Use Cases:**
- Catch bugs before delivery
- Learn from recurring mistakes
- Iterative refinement of solutions
- Security hardening through self-review
- Communication improvement

[See full documentation →](./self-improvement-plugin/README.md)

## 📥 Installation

### For All Projects (User-Level)

Install plugins to your user-level Claude directory:

```bash
# Clone the repository
git clone https://github.com/C0ntr0lledCha0s/claude-code-plugins.git
cd claude-code-plugins

# Link plugins to Claude user directory
mkdir -p ~/.claude/plugins
ln -s $(pwd)/agent-builder ~/.claude/plugins/agent-builder
ln -s $(pwd)/self-improvement-plugin ~/.claude/plugins/self-improvement
```

### For a Specific Project

Install plugins at the project level:

```bash
# Navigate to your project
cd /path/to/your/project

# Clone the plugins
git clone https://github.com/C0ntr0lledCha0s/claude-code-plugins.git

# Link components to project .claude directory
mkdir -p .claude/{agents,skills,commands}

ln -s $(pwd)/claude-code-plugins/agent-builder/agents/* .claude/agents/
ln -s $(pwd)/claude-code-plugins/agent-builder/skills/* .claude/skills/
ln -s $(pwd)/claude-code-plugins/agent-builder/commands/* .claude/commands/

ln -s $(pwd)/claude-code-plugins/self-improvement-plugin/agents/* .claude/agents/
ln -s $(pwd)/claude-code-plugins/self-improvement-plugin/skills/* .claude/skills/
ln -s $(pwd)/claude-code-plugins/self-improvement-plugin/commands/* .claude/commands/
```

### Using plugin.json (Recommended)

If your Claude Code version supports it, use the plugin manifest:

```bash
# Add to your project's .claude/settings.json
{
  "plugins": [
    "/path/to/claude-code-plugins/agent-builder",
    "/path/to/claude-code-plugins/self-improvement-plugin"
  ]
}
```

## 🎯 Use Cases

### Building Custom Agents

Create specialized agents for your workflow:
- Code review agents
- Testing agents
- Documentation agents
- Security audit agents
- Refactoring agents

### Creating Auto-Invoked Skills

Build skills that automatically activate:
- Data analysis expertise
- Language-specific knowledge
- Framework-specific guidance
- Domain-specific best practices

### Automating Workflows

Design slash commands for common tasks:
- Git workflows (commit, push, PR creation)
- Testing and building
- Code generation and scaffolding
- Deployment and releases

### Policy Enforcement

Implement hooks for validation:
- Prevent writes to protected directories
- Validate bash commands for security
- Auto-format code after changes
- Enforce coding standards

## 📚 Documentation

### Quick Links

- [Agent Builder Plugin Documentation](./agent-builder/README.md)
- [Creating Agents](./agent-builder/skills/building-agents/SKILL.md)
- [Creating Skills](./agent-builder/skills/building-skills/SKILL.md)
- [Creating Commands](./agent-builder/skills/building-commands/SKILL.md)
- [Creating Hooks](./agent-builder/skills/building-hooks/SKILL.md)

### Claude Code Resources

- [Official Claude Code Documentation](https://docs.claude.com/claude-code)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)

## 🏗️ Project Structure

```
claude-code-plugins/
├── agent-builder/              # Meta-agent plugin
│   ├── .claude-plugin/
│   │   └── plugin.json        # Plugin manifest
│   ├── agents/                # Meta-architect agent
│   ├── skills/                # 4 builder skills
│   ├── commands/              # 5 creation commands
│   └── README.md
├── README.md                  # This file
├── LICENSE                    # MIT License
└── .gitignore                # Git ignore rules
```

## 🔧 Development

### Creating Your Own Plugin

Use the Agent Builder to create new plugins:

```bash
/new-plugin my-awesome-plugin
```

Claude will guide you through:
1. Defining the plugin structure
2. Creating component directories
3. Writing the manifest file
4. Adding documentation

### Contributing New Plugins

To add a plugin to this repository:

1. **Create your plugin** using the Agent Builder
2. **Validate** all components using the validation scripts
3. **Document** your plugin with a comprehensive README
4. **Test** all components thoroughly
5. **Submit a PR** with your plugin in a new directory

### Plugin Guidelines

All plugins should:
- Follow Claude Code naming conventions (lowercase-hyphens)
- Include a plugin.json manifest
- Provide comprehensive documentation
- Include validation scripts where applicable
- Follow security best practices
- Include usage examples

## 🧪 Testing

### Validate Components

The Agent Builder includes validation scripts:

```bash
# Validate an agent
python agent-builder/skills/building-agents/scripts/validate-agent.py .claude/agents/my-agent.md

# Validate a skill
python agent-builder/skills/building-skills/scripts/validate-skill.py .claude/skills/my-skill/

# Validate a command
python agent-builder/skills/building-commands/scripts/validate-command.py .claude/commands/my-command.md

# Validate hooks
python agent-builder/skills/building-hooks/scripts/validate-hooks.py .claude/hooks.json
```

### Manual Testing

Test components by:
1. Creating test cases for agents, skills, and commands
2. Triggering hooks with various scenarios
3. Verifying auto-invocation of skills
4. Checking error handling and edge cases

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Report Issues

Found a bug or have a feature request? [Open an issue](https://github.com/C0ntr0lledCha0s/claude-code-plugins/issues)

### Submit Plugins

Have a useful plugin to share? Submit a PR with:
- Complete plugin directory
- Comprehensive README
- Validation scripts (if applicable)
- Usage examples
- Tests

### Improve Documentation

Help improve:
- Plugin documentation
- Usage examples
- Best practices guides
- Tutorial content

### Code Review

Review PRs from other contributors:
- Check for security issues
- Verify naming conventions
- Test functionality
- Suggest improvements

## 📋 Naming Conventions

All components follow strict naming conventions:

- **Lowercase letters, numbers, and hyphens only**
- **No underscores or special characters**
- **Maximum 64 characters**

### Specific Conventions

- **Plugins**: `plugin-name` (descriptive, unique)
- **Agents**: `agent-name` (action-oriented: `code-reviewer`, `test-runner`)
- **Skills**: `skill-name` (gerund form: `analyzing-data`, `generating-reports`)
- **Commands**: `command-name` (verb-first: `run-tests`, `create-component`)
- **Hooks**: Event-based names (descriptive of validation/action)

## 🔒 Security

### Best Practices

When creating plugins:
- **Minimize tool permissions**: Start with Read, Grep, Glob
- **Validate all inputs**: Check for injection attacks
- **Avoid hardcoded secrets**: Use environment variables
- **Review bash commands**: Audit for dangerous operations
- **Test security**: Try to bypass your own validations

### Reporting Security Issues

Found a security vulnerability? Please email security@example.com (or open a private security advisory)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Anthropic** for creating Claude and Claude Code
- **The Claude Code community** for inspiration and feedback
- **Contributors** who help improve these plugins

## 🔗 Links

- [Claude Code Documentation](https://docs.claude.com/claude-code)
- [Claude](https://claude.ai)
- [Anthropic](https://anthropic.com)
- [GitHub Repository](https://github.com/C0ntr0lledCha0s/claude-code-plugins)

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/C0ntr0lledCha0s/claude-code-plugins/issues)
- **Discussions**: [GitHub Discussions](https://github.com/C0ntr0lledCha0s/claude-code-plugins/discussions)
- **Discord**: [Join our community](#) (if applicable)

## 🗺️ Roadmap

### Completed Plugins
- ✅ **Agent Builder Plugin**: Meta-agent for building Claude Code extensions
- ✅ **Self-Improvement Plugin**: Continuous improvement through self-critique and feedback loops

### Future Plugin Ideas
- **Testing Suite Plugin**: Automated test generation and execution
- **Documentation Plugin**: Auto-generate docs from code
- **Security Scanner Plugin**: Vulnerability detection and reporting
- **Performance Analyzer Plugin**: Code optimization suggestions
- **Git Workflow Plugin**: Advanced git operations and automation
- **API Generator Plugin**: REST/GraphQL API scaffolding
- **Database Plugin**: Schema management and migration tools
- **Code Review Plugin**: Automated code review with best practices
- **Refactoring Plugin**: Intelligent code refactoring suggestions

---

**Built with ❤️ using Claude Code** - A meta-agent building meta-agents! 🤖

## Star History

If you find these plugins useful, please consider starring the repository! ⭐
