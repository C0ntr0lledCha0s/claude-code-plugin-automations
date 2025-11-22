---
description: Analyze project structure and suggest scope labels based on codebase organization
allowed-tools: Bash, Read, Glob, Grep
argument-hint: "[--create]"
---

# Suggest Scope Labels

Analyzes the project structure to suggest appropriate scope labels based on your codebase organization.

## Usage

```bash
/label-suggest              # Analyze and suggest scope labels
/label-suggest --create     # Analyze and create suggested labels
```

## Arguments

- **--create** (optional): Automatically create the suggested scope labels

## What This Does

1. **Analyze Project Structure**: Scan directories, configs, and code patterns
2. **Identify Scopes**: Detect modules, packages, plugins, or logical areas
3. **Generate Suggestions**: Propose scope labels with descriptions
4. **Optionally Create**: Create labels if --create flag is provided

## Analysis Patterns

The command analyzes:

### Directory Structure
```bash
# Top-level directories (excluding common non-scope dirs)
ls -d */ | grep -v -E '^(node_modules|dist|build|coverage|\.git)/'

# Plugin directories
find . -name "plugin.json" -o -name ".claude-plugin" -type d

# Package.json workspaces
jq -r '.workspaces[]?' package.json 2>/dev/null
```

### Configuration Files
```bash
# Monorepo patterns
cat lerna.json pnpm-workspace.yaml 2>/dev/null

# Conventional commits scopes
jq -r '.convention.commitScopes[]?' git-conventional-commits.json 2>/dev/null
```

### Code Patterns
```bash
# Major code areas
ls -d src/*/ lib/*/ packages/*/ 2>/dev/null
```

## Example Output

```
Analyzing project structure...

Detected Project Type: Claude Code Plugin Repository

Suggested Scope Labels:

  Plugin Modules:
    scope:agent-builder     - Agent builder plugin
    scope:self-improvement  - Self improvement plugin
    scope:github-workflows  - GitHub workflows plugin

  Component Types:
    scope:agents            - Agent definitions
    scope:skills            - Skill implementations
    scope:commands          - Slash commands
    scope:hooks             - Event hooks

  Infrastructure:
    scope:ci                - CI/CD and automation
    scope:docs              - Documentation

Total: 10 scope labels suggested

Run /label-suggest --create to create these labels
Or manually create with: gh label create "scope:name" --color "c2e0c6" --description "Description"
```

## Label Colors

Scope labels use a consistent color palette:
- **c2e0c6** (light green) - Primary scopes
- **c5def5** (light blue) - Secondary scopes
- **d4c5f9** (light purple) - Tertiary scopes

## Workflow

When this command is invoked:

1. **Scan project structure**:
   ```bash
   # Get top-level directories
   DIRS=$(ls -d */ 2>/dev/null | sed 's/\///')

   # Filter out common non-scope directories
   EXCLUDE="node_modules|dist|build|coverage|\.git|__pycache__|\.cache"
   SCOPES=$(echo "$DIRS" | grep -v -E "^($EXCLUDE)$")
   ```

2. **Check for existing scope configuration**:
   ```bash
   # Check git-conventional-commits.json
   if [[ -f "git-conventional-commits.json" ]]; then
     CONFIGURED_SCOPES=$(jq -r '.convention.commitScopes[]?' git-conventional-commits.json)
   fi
   ```

3. **Detect project type**:
   - Monorepo (lerna, pnpm workspaces, npm workspaces)
   - Plugin repository (.claude-plugin directories)
   - Single package (src/, lib/)
   - API project (api/, routes/, controllers/)

4. **Generate suggestions**:
   - Use configured scopes if available
   - Fall back to directory-based detection
   - Add common infrastructure scopes (ci, docs)

5. **Present suggestions with descriptions**:
   - Group by category (modules, components, infrastructure)
   - Include color codes
   - Show creation command

6. **Optionally create labels**:
   ```bash
   if [[ "$1" == "--create" ]]; then
     for scope in "${SUGGESTED_SCOPES[@]}"; do
       gh label create "scope:$scope" \
         --color "c2e0c6" \
         --description "$DESCRIPTION" \
         --force
     done
   fi
   ```

## Integration

### With /init
The `/init` command calls this analysis and includes suggested scopes in the environment file:
```json
{
  "labels": {
    "suggestedScopes": ["agent-builder", "self-improvement", "github-workflows"]
  }
}
```

### With /label-sync
After running `/label-suggest --create`, you can verify with:
```bash
gh label list | grep "scope:"
```

## Project Type Detection

| Pattern | Project Type | Scope Strategy |
|---------|-------------|----------------|
| `.claude-plugin/` dirs | Plugin repo | Plugin names as scopes |
| `packages/` or workspaces | Monorepo | Package names as scopes |
| `src/` only | Single package | Subdirectory names |
| `api/`, `routes/` | API project | Route/resource names |

## Examples

### Plugin Repository
```
Suggested Scope Labels:
  scope:agent-builder
  scope:self-improvement
  scope:github-workflows
  scope:marketplace
```

### Web Application
```
Suggested Scope Labels:
  scope:frontend
  scope:backend
  scope:api
  scope:database
  scope:auth
```

### Monorepo
```
Suggested Scope Labels:
  scope:core
  scope:cli
  scope:web
  scope:shared
  scope:docs
```

## Notes

- Suggestions are based on heuristics and may need adjustment
- Existing `git-conventional-commits.json` scopes take precedence
- Use descriptive scope names that match your team's vocabulary
- Keep scope count manageable (5-15 is typical)
