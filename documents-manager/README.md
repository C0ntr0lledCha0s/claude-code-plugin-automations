# Documents Manager Plugin

A comprehensive documentation management plugin for Claude Code that helps analyze, generate, update, and enforce documentation standards in your codebase.

## Features

- **Documentation Coverage Analysis** - Measure how well your code is documented
- **Automated Documentation Generation** - Generate JSDoc, docstrings, and README files
- **Documentation Auditing** - Comprehensive quality assessment with scoring
- **Documentation Sync** - Keep documentation in sync with code changes
- **Multi-Language Support** - JavaScript, TypeScript, Python, Go, Rust, and more

## Installation

### From Marketplace

```bash
claude plugin install documents-manager
```

### Manual Installation

1. Clone this repository
2. Symlink to Claude's plugin directory:
   ```bash
   ln -s /path/to/documents-manager ~/.claude/plugins/documents-manager
   ```
3. Restart Claude Code

## Components

### Agent

| Agent | Description |
|-------|-------------|
| `docs-analyzer` | Comprehensive documentation analysis and generation agent for complex multi-file documentation tasks |

### Skills

| Skill | Description |
|-------|-------------|
| `analyzing-docs` | Auto-invokes when evaluating documentation quality, coverage, or completeness |
| `writing-docs` | Auto-invokes when generating docstrings, README files, or API documentation |
| `managing-docs` | Auto-invokes when organizing documentation structure or setting up doc frameworks |

### Commands

| Command | Description |
|---------|-------------|
| `/documents-manager:docs-coverage [path]` | Analyze documentation coverage for files or directories |
| `/documents-manager:docs-generate <path> [--type]` | Generate documentation for a file or module |
| `/documents-manager:docs-audit [directory]` | Comprehensive documentation audit with quality scoring |
| `/documents-manager:docs-update <path> [--check-only]` | Update documentation to match current code |

### Hooks

| Hook | Trigger | Description |
|------|---------|-------------|
| `docs-reminder` | PostToolUse (Write) | Suggests documentation for new code |
| `docs-sync-check` | PostToolUse (Edit) | Reminds to update docs when signatures change |

## Usage

### Check Documentation Coverage

```bash
# Check entire codebase
/documents-manager:docs-coverage

# Check specific directory
/documents-manager:docs-coverage src/utils/

# Check specific file
/documents-manager:docs-coverage src/api/users.ts
```

### Generate Documentation

```bash
# Generate API docs for a file
/documents-manager:docs-generate src/api/users.ts --type api

# Generate README for a module
/documents-manager:docs-generate src/utils/ --type readme

# Auto-detect documentation type
/documents-manager:docs-generate src/services/auth.py
```

### Audit Documentation

```bash
# Full codebase audit
/documents-manager:docs-audit

# Audit specific directory
/documents-manager:docs-audit src/
```

### Update Documentation

```bash
# Update docs to match code
/documents-manager:docs-update src/api/users.ts

# Check what needs updating (no changes)
/documents-manager:docs-update src/api/users.ts --check-only
```

## Supported Languages

| Language | Documentation Style |
|----------|-------------------|
| JavaScript | JSDoc |
| TypeScript | TSDoc/JSDoc |
| Python | Docstrings (Google/NumPy style) |
| Go | Go doc comments |
| Rust | Rustdoc |
| Java | Javadoc |

## Coverage Metrics

The plugin measures documentation coverage across:

- **Functions/Methods** - Parameter and return documentation
- **Classes/Types** - Class descriptions and property documentation
- **Modules/Files** - File-level documentation headers
- **Exports** - Public API documentation

### Quality Scoring

Documentation quality is scored on four dimensions (0-10 each):

1. **Completeness** - All APIs documented with full details
2. **Accuracy** - Documentation matches actual code behavior
3. **Clarity** - Clear, well-organized, consistent style
4. **Usefulness** - Practical examples and helpful content

## Configuration

The plugin works out of the box with sensible defaults. Skills auto-invoke based on context.

### Customizing Hooks

To disable documentation reminders, you can remove or modify the hooks in `hooks/hooks.json`.

## Best Practices

1. **Start with Coverage** - Run `/documents-manager:docs-coverage` to understand your current state
2. **Audit First** - Use `/documents-manager:docs-audit` for a comprehensive assessment
3. **Generate Incrementally** - Document high-priority files first (public APIs, exports)
4. **Keep in Sync** - Use `/documents-manager:docs-update` after significant refactors
5. **Review Generated Docs** - Always review auto-generated documentation before committing

## Integration with Other Plugins

The documents-manager plugin works well with:

- **self-improvement** - Quality check documentation improvements
- **github-workflows** - Include documentation updates in PRs
- **testing-expert** - Document test coverage alongside code coverage

## License

MIT
