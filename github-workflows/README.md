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

### Components (v2.0.0)

**Agents** (4):
- `workflow-orchestrator` - Coordinates complex multi-step workflows (advisory)
- `pr-reviewer` - Comprehensive PR review with quality gates
- `issue-manager` - Issue lifecycle management
- `release-manager` - Release workflow automation

**Skills** (9 - auto-invoke based on context):
- `creating-issues` - Issue creation and convention enforcement
- `managing-branches` - Git branching strategy expertise
- `managing-commits` - Git commit quality and conventions
- `managing-projects` - GitHub Projects v2 board management
- `managing-relationships` - Issue parent/child and dependencies
- `managing-worktrees` - Git worktree parallel development
- `organizing-with-labels` - Label and milestone operations
- `reviewing-pull-requests` - PR workflows and reviews
- `triaging-issues` - Issue management and triage

**Commands** (9 core - high-frequency user actions):
- `/init` - Initialize session environment
- `/workflow-status` - View current workflow state
- `/commit-smart` - Intelligent commit with file grouping
- `/branch-start` - Start any branch type (feature/hotfix/release)
- `/branch-finish` - Complete branch with proper merging
- `/pr-create` - Create pull request
- `/issue-create` - Create well-formed issue
- `/issue-track` - Sync issue cache for commit integration
- `/release-prepare` - Prepare release with changelog

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

**Token Setup**:

The plugin requires specific GitHub token scopes for full functionality:

| Scope | Required For | Commands |
|-------|-------------|----------|
| `repo` | Issues, PRs, commits | All commands |
| `read:project` | GitHub Projects v2 | `/project-create`, `/project-sync` |
| `read:org` | Organization projects | Org-level project boards |

**Setup with GitHub CLI** (recommended):
```bash
# Initial authentication with required scopes
gh auth login -s repo,read:project,read:org

# Or add scopes to existing auth
gh auth refresh -s read:project,read:org

# Verify your scopes
gh auth status
```

**Setup with Personal Access Token**:
1. Go to https://github.com/settings/tokens
2. Create token with scopes: `repo`, `read:project`, `read:org`
3. Set as environment variable: `export GH_TOKEN=ghp_xxxx`

**Verify Setup**:
```bash
# Check authentication and scopes
gh auth status

# Test project access
gh api graphql -f query='query { viewer { projectsV2(first: 1) { nodes { title } } } }'
```

> **Note**: Without `read:project` scope, project-related commands will fail with "INSUFFICIENT_SCOPES" errors.

**System Dependencies**:
- **jq**: JSON processor for advanced operations (required for relationship management, some scripts)
  ```bash
  # Debian/Ubuntu/WSL
  sudo apt update && sudo apt install jq -y

  # macOS
  brew install jq

  # Fedora/RHEL
  sudo dnf install jq
  ```
- **python3**: For validation and analysis scripts (usually pre-installed)

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

### 1. Initialize Session

```bash
/github-workflows:init
```

Sets up your session with:
- Project context detection
- Issue cache synchronization
- Environment variables

### 2. Start Feature Branch

```bash
/github-workflows:branch-start feature auth --issue 42
```

Creates feature branch with:
- Flow-aware base branch (develop for gitflow)
- Issue linking
- Naming convention enforcement

### 3. Smart Commit

```bash
/github-workflows:commit-smart
```

Intelligently analyzes and commits changes with automatic file grouping and conventional commit formatting.

### 4. Create PR

```bash
/github-workflows:pr-create
```

Creates PR with:
- Automatic issue linking
- Auto-generated description
- Label suggestions

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

### Enhanced Commit Messages

GitHub-aware commit generation:
```markdown
The managing-commits skill provides:
1. Conventional commit format generation
2. Automatic "Closes #N" for linked issues
3. Co-author detection from collaborators
4. Format validation and conventions
```

## Commands Reference

### Session & Status

**`/init`**
- Initialize GitHub workflow environment
- Sets up project context and issue cache
- Configures session environment variables

**`/workflow-status`**
- Shows current workflow state
- Branch, commits, PRs, board status
- Next recommended actions

### Branching

**`/branch-start <type> <name> [--issue N]`**
- Start branch following configured strategy
- Types: feature, bugfix, hotfix, release, docs, refactor
- Example: `/branch-start feature auth --issue 42`

**`/branch-finish [branch-name]`**
- Complete branch with proper merging
- Handles hotfix dual-merge (main + develop)
- Creates version tags for releases/hotfixes

### Commits

**`/commit-smart [mode]`**
- Intelligent commit workflow with file grouping
- Modes: all, staged, context, scope
- Analyzes changes and generates conventional commits

### Issues

**`/issue-create [title]`**
- Create well-formed issue with labels
- Validates naming conventions
- Adds to project board automatically

**`/issue-track [filter]`**
- Sync issue cache for commit integration
- Filters: assigned, labeled, milestone, project, all
- Enables automatic issue references in commits

### Pull Requests

**`/pr-create [--title TITLE] [--draft]`**
- Create PR with proper formatting
- Auto-generates description from commits
- Links to related issues

### Releases

**`/release-prepare [version-type]`**
- Prepare release with changelog
- Types: major, minor, patch, auto
- Analyzes commits since last release

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

### Insufficient Scopes

```
Error: Your token has not been granted the required scopes (INSUFFICIENT_SCOPES)
Solution: Run `gh auth refresh -s read:project` to add the required scope
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
│   └── plugin.json              # Plugin manifest (v2.0.0)
├── agents/                      # 4 agents
│   ├── workflow-orchestrator.md # Multi-step coordinator
│   ├── pr-reviewer.md           # PR review specialist
│   ├── issue-manager.md         # Issue lifecycle
│   └── release-manager.md       # Release workflows
├── skills/                      # 9 auto-invoking skills
│   ├── creating-issues/         # Issue creation
│   ├── managing-branches/       # Branching strategies
│   ├── managing-commits/        # Commit quality
│   ├── managing-projects/       # Project boards
│   ├── managing-relationships/  # Issue dependencies
│   ├── managing-worktrees/      # Parallel development
│   ├── organizing-with-labels/  # Labels & milestones
│   ├── reviewing-pull-requests/ # PR workflows
│   └── triaging-issues/         # Issue triage
├── commands/                    # 9 core commands
├── hooks/                       # Automation hooks
└── README.md                    # This file
```

### Testing

Run validation scripts:
```bash
# Validate skills
python /path/to/claude-component-builder/skills/building-skills/scripts/validate-skill.py \
  skills/managing-projects/

# Validate agents
python /path/to/claude-component-builder/skills/building-agents/scripts/validate-agent.py \
  agents/workflow-orchestrator.md

# Validate commands
python /path/to/claude-component-builder/skills/building-commands/scripts/validate-command.py \
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

### v2.0.0 (Current)
- ✅ Streamlined to 9 core commands (from 31)
- ✅ 9 auto-invoking skills
- ✅ 4 specialized agents
- ✅ Hooks configuration
- ✅ Complete documentation

### Future Plans
- Advanced automation rules
- GitHub Actions integration
- Team analytics
- Custom field types
- Webhook integrations

---

**Built with ❤️ using Claude Code**
