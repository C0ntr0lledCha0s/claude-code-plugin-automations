# GitHub Workflows Plugin

Comprehensive GitHub workflow automation for Claude Code, including project boards, labels, milestones, commits, issues, and pull requests with integrated quality gates.

## Overview

The GitHub Workflows plugin provides end-to-end automation for GitHub-based development workflows. It coordinates project management, issue triage, commit quality, and pull request reviews into seamless, automated workflows.

### Key Features

- **Project Boards (v2)**: Complete project management with GraphQL-powered boards, custom fields, and automation
- **Labels & Milestones**: Taxonomy management, bulk operations, and milestone tracking
- **Commit Management**: Conventional commits with GitHub context and validation
- **Issue Triage**: Intelligent issue management with duplicate detection and relationship mapping
- **Pull Request Workflows**: Automated reviews with self-improvement plugin integration and quality gates

## Architecture

### Components

**Agents** (2):
- `workflow-orchestrator` - Coordinates complex multi-step workflows
- `pr-reviewer` - Comprehensive PR review with quality gates

**Skills** (5):
- `managing-projects` - GitHub Projects v2 board management
- `organizing-with-labels` - Label and milestone operations
- `managing-commits` - Git commit quality and conventions
- `triaging-issues` - Issue management and triage
- `reviewing-pull-requests` - PR workflows and reviews

**Commands** (9):
- `/project-create` - Create project boards
- `/project-sync` - Sync issues to boards
- `/label-sync` - Apply label taxonomy
- `/milestone-create` - Create milestones
- `/commit-review` - Review commit history
- `/issue-triage` - Triage issues
- `/pr-review-request` - Request comprehensive PR review
- `/pr-quality-check` - Run quality gates
- `/workflow-status` - View workflow state

## Installation

### Prerequisites

**Required**:
- Git repository
- Claude Code with plugin support

**GitHub CLI** (`gh`):
The plugin automatically installs and configures GitHub CLI for you on:
- **Linux**: Debian/Ubuntu (apt), RHEL/Fedora (dnf/yum), Arch (pacman)
- **macOS**: via Homebrew
- **Windows**: via winget

If automatic installation fails, install manually:
```bash
# Debian/Ubuntu/WSL
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list
sudo apt update && sudo apt install gh

# macOS
brew install gh

# Windows
winget install --id GitHub.cli

# Authenticate after installation
gh auth login
```

More info: https://github.com/cli/cli#installation

**Optional Dependencies**:
The plugin will auto-install these if missing:
- **jq**: JSON processor for advanced operations
- **python3**: For validation and analysis scripts

### Robustness Features

The plugin includes several features to ensure reliability:

- **Automatic Dependency Installation**: Detects and installs missing tools (gh, jq, python3)
- **Preflight Checks**: Validates environment before executing commands
- **Retry Logic**: Automatically retries failed operations with exponential backoff
- **Label Auto-Creation**: Creates labels if they don't exist before use
- **Error Recovery**: Helpful error messages with actionable solutions
- **Version Checking**: Ensures minimum required versions of tools

### Install Plugin

```bash
# Add to your .claude/settings.json
{
  "plugins": [
    "/path/to/claude-code-plugin-automations/github-workflows"
  ]
}
```

Or link manually:
```bash
cd /path/to/your/project/.claude
ln -s /path/to/claude-code-plugin-automations/github-workflows/skills/* skills/
ln -s /path/to/claude-code-plugin-automations/github-workflows/agents/* agents/
ln -s /path/to/claude-code-plugin-automations/github-workflows/commands/* commands/
```

## Quick Start

### 1. Create a Project Board

```bash
/project-create "Sprint 5" kanban
```

Creates a kanban board with:
- Columns: Todo, In Progress, Review, Done
- Fields: Priority, Size, Assignee
- Auto-add automation

### 2. Apply Label Taxonomy

```bash
/label-sync standard
```

Creates standard labels:
- Types: bug, feature, docs, refactor
- Priorities: priority:high, priority:medium, priority:low
- Scopes: scope:frontend, scope:backend, scope:docs

### 3. Smart Commit

```bash
/github-workflows:commit-smart
```

Intelligently analyzes and commits changes with automatic file grouping and conventional commit formatting.

### 4. Create PR with Quality Check

```bash
/pr-review-request
```

Creates PR with:
- Automatic issue linking
- Self-improvement quality check
- Quality gate validation
- Approval decision

## Usage Examples

### Example 1: Complete Feature Workflow

```markdown
User: "I want to implement user authentication"

Claude:
1. Creates issue #42: "Implement user authentication"
2. Applies labels: feature, priority:high, scope:backend
3. Adds to "Q1 Sprint" board
4. Guides branch creation: feature/user-auth
5. Helps with conventional commits
6. Creates PR with quality check when ready
7. Reviews and approves/requests changes

Complete workflow automation! 🚀
```

### Example 2: Sprint Planning

```markdown
User: "/project-create 'Sprint 5' sprint"

Claude:
Creates sprint board with:
- Backlog, Sprint, In Progress, Review, Done columns
- Sprint iteration field (2-week sprints)
- Story points field (Fibonacci scale)
- Auto-add automation for sprint-labeled issues

Board ready for planning!
```

### Example 3: PR Review with Quality Gates

```markdown
User: "/pr-review-request 123"

Claude:
Running comprehensive review...

Quality Gates:
✅ CI/CD: All checks passed
✅ Tests: 95% coverage
✅ Security: No vulnerabilities
✅ Quality Check: All scores >= 4/5

Self-Improvement Analysis:
- Correctness: 5/5 ⭐
- Security: 5/5 ⭐
- Completeness: 4/5 ✅
- Efficiency: 4/5 ✅
- Clarity: 4/5 ✅

Decision: APPROVED ✅

Excellent work! Ready to merge. 🚀
```

## Integration

### With Self-Improvement Plugin

Automatic quality checks for PRs:
```markdown
Before approving any PR:
1. Invokes `/quality-check` from self-improvement plugin
2. Analyzes quality scores across 6 dimensions
3. Identifies critical vs minor issues
4. Makes approve/request-changes decision
5. Includes quality report in review
```

### With commit-helper Skill

Enhanced commit messages:
```markdown
Extends commit-helper with GitHub context:
1. Gets conventional commit from commit-helper
2. Adds "Closes #N" for linked issues
3. Adds co-authors from PR collaborators
4. Validates format and conventions
```

## Commands Reference

### Project Management

**`/project-create [name] [template]`**
- Creates project board with template
- Templates: sprint, kanban, roadmap
- Example: `/project-create "Q1 Planning" sprint`

**`/project-sync [project-number]`**
- Syncs issues and PRs to board
- Updates field values based on labels
- Example: `/project-sync 1`

### Labels & Milestones

**`/label-sync [preset]`**
- Applies label taxonomy
- Presets: standard, comprehensive, minimal
- Example: `/label-sync standard`

**`/milestone-create [title] [due-date]`**
- Creates milestone with date
- Example: `/milestone-create "v2.0" "2024-03-31"`

### Commits

**`/commit-smart [mode]`**
- Intelligent commit workflow with file grouping
- Modes: all, staged, context, scope, interactive
- Analyzes changes and generates conventional commits

**`/commit-review`**
- Reviews commit history for issues
- Validates conventions
- Suggests improvements

### Issues

**`/issue-triage [issue-number]`**
- Comprehensive issue triage
- Duplicate detection
- Relationship mapping
- Auto-labeling

### Pull Requests

**`/pr-review-request [pr-number]`**
- Full PR review with quality gates
- Self-improvement integration
- Approval decision

**`/pr-quality-check [pr-number]`**
- Runs quality gates without review
- Reports quality scores
- Recommends actions

### Workflow

**`/workflow-status`**
- Shows current workflow state
- Branch, commits, PRs, board status
- Next recommended actions

## Configuration

### Project Board Templates

Customize board templates in `skills/managing-projects/templates/board-templates.json`:

```json
{
  "sprint": {
    "columns": ["Backlog", "Sprint", "In Progress", "Review", "Done"],
    "fields": {
      "Status": ["Backlog", "Sprint", "In Progress", "Review", "Done"],
      "Priority": ["High", "Medium", "Low"],
      "Story Points": ["1", "2", "3", "5", "8", "13"]
    }
  },
  "kanban": {
    "columns": ["Todo", "In Progress", "Review", "Done"],
    "fields": {
      "Status": ["Todo", "In Progress", "Review", "Done"],
      "Priority": ["High", "Medium", "Low"],
      "Size": ["XS", "S", "M", "L", "XL"]
    }
  }
}
```

### Label Taxonomies

Customize label presets in `skills/organizing-with-labels/assets/label-presets.json`:

```json
{
  "standard": {
    "type": [
      {"name": "bug", "color": "d73a4a", "description": "Something isn't working"},
      {"name": "feature", "color": "0075ca", "description": "New feature or request"}
    ],
    "priority": [
      {"name": "priority:high", "color": "b60205"},
      {"name": "priority:medium", "color": "d93f0b"},
      {"name": "priority:low", "color": "fbca04"}
    ]
  }
}
```

## Troubleshooting

### Not Authenticated

```
Error: gh CLI not authenticated
Solution: Run `gh auth login`
```

### Project Not Found

```
Error: Project #1 not found
Solution: Check project exists with `gh project list --owner ORG`
```

### GraphQL Errors

```
Error: GraphQL query failed
Solution: Check syntax and field names
```

**Multiple solutions available:**
1. **Use the helper script**: `skills/managing-projects/scripts/graphql-queries.sh`
   - Provides high-level commands for common operations
   - Example: `graphql-queries.sh add_item PROJECT_ID CONTENT_ID`

2. **Use direct gh api commands**: See `skills/managing-projects/references/graphql-workarounds.md`
   - Complete reference with copy-paste ready commands
   - Covers all GitHub Projects v2 operations
   - Includes troubleshooting and examples
   - No additional scripts needed

3. **Check the API documentation**: `references/gh-project-api.md`

### Rate Limiting

```
Error: API rate limit exceeded
Solution: Wait or check limits with `gh api rate_limit`
```

## Development

### Project Structure

```
github-workflows/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── agents/
│   ├── workflow-orchestrator.md # Main coordinator
│   └── pr-reviewer.md           # PR review specialist
├── skills/
│   ├── managing-projects/       # Project boards
│   ├── organizing-with-labels/  # Labels & milestones
│   ├── managing-commits/        # Commit quality
│   ├── triaging-issues/         # Issue management
│   └── reviewing-pull-requests/ # PR workflows
├── commands/                    # 9 user commands
├── hooks/                       # Automation hooks
└── README.md                    # This file
```

### Testing

Run validation scripts:
```bash
# Validate skills
python /path/to/agent-builder/skills/building-skills/scripts/validate-skill.py \
  skills/managing-projects/

# Validate agents
python /path/to/agent-builder/skills/building-agents/scripts/validate-agent.py \
  agents/workflow-orchestrator.md

# Validate commands
python /path/to/agent-builder/skills/building-commands/scripts/validate-command.py \
  commands/project-create.md
```

## Contributing

Contributions welcome! Please:

1. Follow existing patterns and conventions
2. Add tests for new features
3. Update documentation
4. Validate all components before PR

## License

MIT License - see LICENSE file

## Support

- Issues: [GitHub Issues](https://github.com/C0ntr0lledCha0s/claude-code-plugin-automations/issues)
- Discussions: [GitHub Discussions](https://github.com/C0ntr0lledCha0s/claude-code-plugin-automations/discussions)

## Roadmap

### Phase 1 (Current)
- ✅ Plugin foundation
- ✅ Core agents
- ✅ Project boards skill
- ⏳ All 5 skills (in progress)
- ⏳ All 9 commands
- ⏳ Hooks configuration
- ⏳ Complete documentation

### Phase 2 (Future)
- Advanced automation rules
- GitHub Actions integration
- Release management
- Team analytics
- Custom field types
- Webhook integrations

---

**Built with ❤️ using Claude Code**
