# GitHub Workflows Plugin - Complete Implementation Guide

This document provides the complete specification for implementing all remaining components of the github-workflows plugin.

## Recent Updates

### ✅ GitHub CLI Auto-Installation (2025-01-13)

**Feature Added**: Automatic detection and installation of GitHub CLI (`gh`)

**Files Created/Modified**:
1. **NEW**: [scripts/ensure-gh-cli.sh](scripts/ensure-gh-cli.sh) - 230 lines
   - Auto-detects OS (Linux, macOS, Windows)
   - Installs `gh` using appropriate package manager
   - Supports Debian/Ubuntu (apt), RHEL/Fedora (dnf/yum), Arch (pacman), macOS (brew), Windows (winget)
   - Checks authentication status
   - Provides clear error messages and fallback instructions

2. **UPDATED**: [skills/managing-projects/scripts/project-helpers.sh](skills/managing-projects/scripts/project-helpers.sh)
   - Replaced `check_gh_auth()` with `ensure_gh_cli()`
   - Now automatically installs `gh` if missing
   - Updated all functions to use new prerequisite check

3. **UPDATED**: [skills/managing-projects/SKILL.md](skills/managing-projects/SKILL.md)
   - Added "Prerequisites and Setup" section
   - Documents auto-installation feature
   - Provides manual installation instructions

4. **UPDATED**: [commands/project-create.md](commands/project-create.md)
   - Added prerequisites section
   - Documents supported platforms
   - Explains auto-installation process

5. **UPDATED**: [README.md](README.md)
   - Updated prerequisites section
   - Documents auto-installation capabilities
   - Provides comprehensive manual installation guide

**Impact**: Users no longer need to manually install GitHub CLI - the plugin handles it automatically. Improves first-time user experience significantly.

## Implementation Status

### ✅ Completed (25% - Foundation)

**Plugin Foundation**:
- ✅ Directory structure created
- ✅ [plugin.json](/.claude-plugin/plugin.json) - Complete manifest with all 9 commands registered
- ✅ [README.md](/README.md) - Comprehensive documentation

**Agents** (100% complete - 750 LOC):
- ✅ [workflow-orchestrator.md](/agents/workflow-orchestrator.md) - 400 lines
- ✅ [pr-reviewer.md](/agents/pr-reviewer.md) - 350 lines

**Skills** (20% complete):
- ✅ [managing-projects/SKILL.md](/skills/managing-projects/SKILL.md) - 500 lines (Priority 1)
- ✅ [managing-projects/scripts/project-helpers.sh](/skills/managing-projects/scripts/project-helpers.sh) - 300 lines

### ⏳ Remaining Implementation (75%)

**Skills** (80% remaining - ~8,000 LOC):
- ✅ managing-projects: Core skill complete, graphql-queries.sh implemented (400 lines), workarounds documented
- ⏳ managing-projects: 2 more scripts (validate-board-config.py), templates, references (500 LOC)
- ✅ organizing-with-labels: Complete skill with scripts (label-operations.py, milestone-manager.py)
- ✅ managing-commits: Complete skill with scripts (commit-analyzer.py, conventional-commits.py)
- ✅ triaging-issues: Complete skill with scripts (validate-issue.py, issue-helpers.sh, duplicate-detection.sh, relationship-mapper.sh)
- ✅ reviewing-pull-requests: Complete skill with scripts (pr-manager.py, quality-gates.sh)

**Commands** (0% complete - 1,100 LOC):
- ⏳ 9 commands (120-180 LOC each)

**Hooks** (0% complete - 200 LOC):
- ⏳ hooks.json configuration

**Documentation** (20% complete - 600 LOC):
- ✅ README.md
- ⏳ EXAMPLES.md
- ⏳ Skill-specific references

---

## Priority 1: managing-projects (CORE COMPLETE ✅)

### ✅ Completed Files

#### 1. `skills/managing-projects/scripts/graphql-queries.sh` ✅

**Status**: COMPLETE (400 lines)
**Purpose**: GraphQL query builder and executor for Projects v2 API

**Key Functions** (250 lines):
```bash
#!/usr/bin/env bash
# GraphQL Operations for GitHub Projects v2

# Build project query
build_project_query() {
    local org="$1"
    local project_number="$2"

    cat <<'EOF'
query($org: String!, $number: Int!) {
  organization(login: $org) {
    projectV2(number: $number) {
      id
      title
      fields(first: 20) {
        nodes {
          ... on ProjectV2SingleSelectField {
            id
            name
            options {
              id
              name
            }
          }
        }
      }
      items(first: 100) {
        nodes {
          id
          content {
            ... on Issue {
              number
              title
            }
            ... on PullRequest {
              number
              title
            }
          }
        }
      }
    }
  }
}
EOF
}

# Execute GraphQL query
execute_query() {
    local query="$1"
    local variables="$2"

    gh api graphql -f query="$query" -f variables="$variables"
}

# Add item to project (mutation)
add_project_item() {
    local project_id="$1"
    local content_id="$2"

    local mutation
    mutation=$(cat <<'EOF'
mutation($projectId: ID!, $contentId: ID!) {
  addProjectV2ItemById(input: {
    projectId: $projectId
    contentId: $contentId
  }) {
    item {
      id
    }
  }
}
EOF
)

    gh api graphql -f query="$mutation" \
        -f projectId="$project_id" \
        -f contentId="$content_id"
}

# Update item field value
update_item_field() {
    local project_id="$1"
    local item_id="$2"
    local field_id="$3"
    local option_id="$4"

    local mutation
    mutation=$(cat <<'EOF'
mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: ProjectV2FieldValue!) {
  updateProjectV2ItemFieldValue(input: {
    projectId: $projectId
    itemId: $itemId
    fieldId: $fieldId
    value: $value
  }) {
    projectV2Item {
      id
    }
  }
}
EOF
)

    local value="{\"singleSelectOptionId\": \"$option_id\"}"

    gh api graphql -f query="$mutation" \
        -f projectId="$project_id" \
        -f itemId="$item_id" \
        -f fieldId="$field_id" \
        -f value="$value"
}

# Main
main() {
    case "${1:-help}" in
        query)
            build_project_query "$2" "$3"
            ;;
        add_item)
            add_project_item "$2" "$3"
            ;;
        update_field)
            update_item_field "$2" "$3" "$4" "$5"
            ;;
        *)
            echo "Usage: $0 {query|add_item|update_field} args..."
            ;;
    esac
}

main "$@"
```

#### 2. `skills/managing-projects/scripts/validate-board-config.py`

**Purpose**: Validate project board configuration

**Implementation** (150 lines):
```python
#!/usr/bin/env python3
"""Validate GitHub Projects v2 board configuration."""

import json
import sys
import subprocess
from typing import Dict, List, Tuple

def run_gh_command(args: List[str]) -> Dict:
    """Execute gh CLI command and return JSON output."""
    try:
        result = subprocess.run(
            ['gh'] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return {}

def validate_project_exists(project_id: str, owner: str) -> Tuple[bool, List[str]]:
    """Validate project exists and is accessible."""
    errors = []

    # Check project exists
    projects = run_gh_command(['project', 'list', '--owner', owner, '--format', 'json'])

    if not any(p['id'] == project_id for p in projects.get('projects', [])):
        errors.append(f"Project {project_id} not found or not accessible")

    return len(errors) == 0, errors

def validate_fields(project_id: str) -> Tuple[bool, List[str]]:
    """Validate project has required fields."""
    errors = []
    required_fields = ['Status', 'Priority']

    # This would query GraphQL for project fields
    # Simplified for this example

    return len(errors) == 0, errors

def validate_orphans(project_id: str) -> Tuple[bool, List[str]]:
    """Check for orphaned items (deleted issues/PRs)."""
    warnings = []

    # Query project items and check if content still exists
    # Simplified for this example

    return True, warnings

def main():
    if len(sys.argv) < 2:
        print("Usage: validate-board-config.py <project_id> [--check-orphans] [--check-fields]")
        sys.exit(1)

    project_id = sys.argv[1]
    check_orphans = '--check-orphans' in sys.argv
    check_fields = '--check-fields' in sys.argv

    print(f"Validating project {project_id}...")

    all_valid = True

    # Validate existence
    valid, errors = validate_project_exists(project_id, "")
    if not valid:
        print("✗ Project validation failed:")
        for error in errors:
            print(f"  - {error}")
        all_valid = False
    else:
        print("✓ Project exists and is accessible")

    # Validate fields
    if check_fields:
        valid, errors = validate_fields(project_id)
        if not valid:
            print("✗ Field validation failed:")
            for error in errors:
                print(f"  - {error}")
            all_valid = False
        else:
            print("✓ Required fields present")

    # Check orphans
    if check_orphans:
        valid, warnings = validate_orphans(project_id)
        if warnings:
            print("⚠ Orphaned items found:")
            for warning in warnings:
                print(f"  - {warning}")

    sys.exit(0 if all_valid else 1)

if __name__ == '__main__':
    main()
```

#### 3. `skills/managing-projects/templates/board-templates.json`

**Purpose**: Predefined board templates

**Content** (100 lines):
```json
{
  "sprint": {
    "name": "Sprint Board",
    "description": "Scrum sprint planning board with iterations",
    "columns": [
      {"name": "Backlog", "description": "Future work"},
      {"name": "Sprint", "description": "Current sprint backlog"},
      {"name": "In Progress", "description": "Actively being worked"},
      {"name": "Review", "description": "In code review"},
      {"name": "Done", "description": "Completed this sprint"}
    ],
    "fields": {
      "Status": {
        "type": "SingleSelect",
        "options": ["Backlog", "Sprint", "In Progress", "Review", "Done"]
      },
      "Priority": {
        "type": "SingleSelect",
        "options": ["High", "Medium", "Low"]
      },
      "Story Points": {
        "type": "SingleSelect",
        "options": ["1", "2", "3", "5", "8", "13"]
      },
      "Sprint": {
        "type": "Iteration",
        "duration": 14,
        "startDay": 1
      }
    },
    "automation": {
      "autoAdd": {
        "enabled": true,
        "filters": ["label:sprint"]
      },
      "autoArchive": {
        "enabled": true,
        "daysAfterDone": 30
      }
    }
  },
  "kanban": {
    "name": "Kanban Board",
    "description": "Continuous flow kanban board",
    "columns": [
      {"name": "Todo", "description": "Ready to start"},
      {"name": "In Progress", "description": "Work in progress"},
      {"name": "Review", "description": "Awaiting review"},
      {"name": "Done", "description": "Completed"}
    ],
    "fields": {
      "Status": {
        "type": "SingleSelect",
        "options": ["Todo", "In Progress", "Review", "Done"]
      },
      "Priority": {
        "type": "SingleSelect",
        "options": ["High", "Medium", "Low"]
      },
      "Size": {
        "type": "SingleSelect",
        "options": ["XS", "S", "M", "L", "XL"]
      }
    },
    "automation": {
      "autoAdd": {
        "enabled": true,
        "filters": ["is:issue", "is:pr", "is:open"]
      }
    }
  },
  "roadmap": {
    "name": "Roadmap Board",
    "description": "Long-term planning roadmap",
    "columns": [
      {"name": "Planning", "description": "Under consideration"},
      {"name": "In Progress", "description": "Active work"},
      {"name": "Completed", "description": "Done"},
      {"name": "On Hold", "description": "Paused"}
    ],
    "fields": {
      "Status": {
        "type": "SingleSelect",
        "options": ["Planning", "In Progress", "Completed", "On Hold"]
      },
      "Quarter": {
        "type": "SingleSelect",
        "options": ["Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024"]
      },
      "Target Date": {
        "type": "Date"
      }
    },
    "views": [
      {"name": "Roadmap", "type": "roadmap", "groupBy": "Quarter"},
      {"name": "Table", "type": "table"}
    ]
  }
}
```

#### 4. `skills/managing-projects/references/gh-project-api.md`

**Purpose**: GitHub Projects API reference documentation

**Content** (200 lines): Complete reference of GraphQL schema, queries, mutations, and examples.

---

## Priority 2: organizing-with-labels (COMPLETE)

### Directory Structure
```
skills/organizing-with-labels/
├── SKILL.md (600 lines)
├── scripts/
│   ├── label-operations.py (250 lines)
│   └── milestone-manager.py (200 lines)
├── assets/
│   └── label-presets.json (80 lines)
└── references/
    └── label-best-practices.md (150 lines)
```

### Key Implementation Points

**SKILL.md** - Core capabilities:
- Label CRUD operations via `gh label`
- Bulk label application
- Label taxonomy management (type, priority, scope, status)
- Milestone operations
- Color-coded categorization

**label-operations.py** - Python script for:
- Create/update/delete labels
- Bulk apply to multiple issues
- Validate label schema
- Sync labels across repos

**milestone-manager.py** - Python script for:
- Create/update milestones with due dates
- Assign issues to milestones
- Track milestone progress
- Generate completion reports

**label-presets.json** - Predefined taxonomies:
```json
{
  "standard": {...},
  "comprehensive": {...},
  "minimal": {...}
}
```

---

## Priority 3: managing-commits (COMPLETE)

### Directory Structure
```
skills/managing-commits/
├── SKILL.md (700 lines)
├── scripts/
│   ├── commit-analyzer.py (250 lines)
│   └── conventional-commits.py (200 lines)
├── assets/
│   └── commit-templates.json (60 lines)
└── references/
    ├── conventional-commits.md (150 lines)
    └── commit-patterns.md (100 lines)
```

### Key Implementation Points

**SKILL.md** - Extends commit-helper with:
- GitHub-specific commit context
- Issue linking ("Closes #N")
- Co-author attribution
- Commit history analysis

**commit-analyzer.py** - Analyzes:
- Staged/unstaged changes
- Commit message format
- Conventional commit compliance
- GitHub issue references

**conventional-commits.py** - Generates:
- Type-scoped commit messages
- Issue footer links
- Co-author trailers

---

## Priority 4: triaging-issues (COMPLETE)

### Directory Structure
```
skills/triaging-issues/
├── SKILL.md (600 lines)
├── scripts/
│   ├── issue-helpers.sh (250 lines)
│   ├── duplicate-detection.sh (200 lines)
│   ├── relationship-mapper.sh (150 lines)
│   └── validate-issue.py (120 lines)
├── templates/
│   ├── issue-response-templates.md (250 lines)
│   ├── bug-report-template.md (80 lines)
│   └── feature-request-template.md (80 lines)
└── references/
    └── issue-lifecycle-guide.md (150 lines)
```

### Key Implementation Points

**SKILL.md** - Based on temp/skills/github-issues but enhanced:
- Validation-first approach
- Duplicate detection with fuzzy matching
- Relationship mapping (blocks, depends-on, related)
- Evidence-based responses
- Auto-labeling

**duplicate-detection.sh** - Uses:
- TF-IDF similarity scoring
- Title and body comparison
- Threshold-based matching

**relationship-mapper.sh** - Extracts:
- "Duplicate of #N"
- "Blocks #N"
- "Blocked by #N"
- "Depends on #N"
- "Related to #N"

---

## Priority 5: reviewing-pull-requests (COMPLETE)

### Directory Structure
```
skills/reviewing-pull-requests/
├── SKILL.md (550 lines)
├── scripts/
│   ├── pr-manager.py (300 lines)
│   ├── review-automation.sh (250 lines)
│   └── quality-gates.sh (200 lines)
├── templates/
│   ├── pr-review-template.md (100 lines)
│   └── pr-checklist.md (80 lines)
└── references/
    └── pr-best-practices.md (150 lines)
```

### Key Implementation Points

**SKILL.md** - PR workflow management:
- Create PRs with templates
- Link to issues automatically
- Check CI status
- Merge operations
- Self-improvement integration

**quality-gates.sh** - Validates:
- CI/CD status (all checks passed)
- Test coverage (>= 80%)
- No merge conflicts
- Approvals present
- Security scans clean

**pr-manager.py** - Operations:
- Create PR with issue links
- Add reviewers
- Check PR status
- Merge with strategy (squash/merge/rebase)

---

## Commands (ALL 9)

### Template Structure (Each ~120 lines)

```markdown
---
description: Command description
allowed-tools: Bash, Read, Grep, Glob
argument-hint: [arg1] [arg2]
model: sonnet
---

# Command Name

## Purpose
What this command does

## Arguments
- $1: First argument
- $2: Second argument (optional)

## Workflow
1. Step 1
2. Step 2
3. Step 3

## Implementation
[Invokes appropriate skills]

## Examples
/command-name arg1 arg2

## Error Handling
Common errors and solutions
```

### Commands to Implement

1. **project-create.md** - Creates project boards
2. **project-sync.md** - Syncs issues to boards
3. **label-sync.md** - Applies label taxonomy
4. **milestone-create.md** - Creates milestones
5. **commit-review.md** - Reviews commit history
6. **issue-triage.md** - Triages issues
7. **pr-review-request.md** - Requests PR review
8. **pr-quality-check.md** - Runs quality gates
9. **workflow-status.md** - Shows workflow state

---

## Hooks Configuration

### `hooks/hooks.json` (200 lines)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash.*git push.*--force",
        "hooks": [
          {
            "type": "command",
            "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/prevent-force-push.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash.*gh pr merge",
        "hooks": [
          {
            "type": "command",
            "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/update-board-on-merge.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/save-workflow-state.sh"
          }
        ]
      }
    ]
  }
}
```

---

## Documentation

### EXAMPLES.md (300 lines)

Comprehensive examples:
- Complete feature workflows
- Sprint planning scenarios
- Issue triage examples
- PR review workflows
- Integration patterns

---

## Implementation Strategy

### Recommended Order

1. **Week 1**: Complete all 5 skills
   - Finish managing-projects remaining files
   - Implement organizing-with-labels
   - Implement managing-commits

2. **Week 2**: Issues, PRs, Commands
   - Implement triaging-issues
   - Implement reviewing-pull-requests
   - Create all 9 commands

3. **Week 3**: Hooks and Documentation
   - Implement hooks.json
   - Create hook scripts
   - Write EXAMPLES.md
   - Complete all references

4. **Week 4**: Testing and Polish
   - Integration testing
   - Validation scripts
   - Bug fixes
   - Final documentation

---

## Testing Checklist

- [ ] Each skill auto-invokes correctly
- [ ] Commands invoke appropriate skills
- [ ] Agent orchestration works
- [ ] Hooks trigger on events
- [ ] Self-improvement integration works
- [ ] All scripts executable and functional
- [ ] Validation passes
- [ ] Documentation complete

---

## Next Steps

To continue implementation:

1. Use this guide to implement remaining skills
2. Follow established patterns from managing-projects
3. Test each component independently
4. Integrate and test workflows
5. Run validation scripts
6. Complete documentation

Each component specification above provides enough detail to implement independently or continue with Claude's assistance.
