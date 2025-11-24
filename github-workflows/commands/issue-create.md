---
description: Create a well-formed issue with labels, milestone, relationships, and project board placement
allowed-tools: Bash, Read
argument-hint: "[title]"
---

# Create Issue

Create a new GitHub issue following project conventions with all metadata properly configured.

## Usage

```bash
/issue-create "Add validation for hook matchers"
/issue-create                                      # Interactive mode
```

## Arguments

- **First argument** (optional): Issue title. If omitted, prompts for title.

## What This Does

Creates an issue with all factors properly configured:

1. **Title** - Validates naming conventions (no type prefixes)
2. **Labels** - Applies type, priority, scope, and branch labels
3. **Milestone** - Optionally assigns to milestone
4. **Relationships** - Links to parent, blocking, or related issues
5. **Project** - Adds to project board with initial status
6. **Body** - Includes structured template with acceptance criteria

## Workflow

### Step 0: Load Environment and Detect Scope

Before any prompts, load the environment and attempt scope detection:

```bash
# Load environment
ENV_FILE=".claude/github-workflows/env.json"
if [[ -f "$ENV_FILE" ]]; then
    DETECTED_SCOPE=$(jq -r '.branch.scopeLabel // empty' "$ENV_FILE")
    SUGGESTED_SCOPES=$(jq -r '.labels.suggestedScopes[]? // empty' "$ENV_FILE")
fi

# If no scope from env, try branch name
if [[ -z "$DETECTED_SCOPE" ]]; then
    BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    # Match branch against suggested scopes
    for scope in $SUGGESTED_SCOPES; do
        if [[ "${BRANCH,,}" == *"${scope,,}"* ]]; then
            DETECTED_SCOPE="scope:$scope"
            break
        fi
    done
fi
```

### Step 1: Title Validation

Check title follows conventions:
- No type prefixes like `[BUG]`, `[FEATURE]`, `[ENHANCEMENT]`
- Descriptive and actionable
- 50-72 characters recommended

```
❌ "[BUG] Login fails" → Suggest: "Fix login authentication failure"
❌ "[FEATURE] Add auth" → Suggest: "Add user authentication"
✅ "Add validation for hook matchers"
```

### Step 2: Label Selection

Prompt for each label dimension:

**Type** (required):
```
Select issue type:
1. bug - Something isn't working
2. feature - New functionality
3. enhancement - Improve existing feature
4. documentation - Documentation changes
5. refactor - Code improvement
6. chore - Maintenance task

Your choice: _
```

**Priority** (required):
```
Select priority:
1. priority:high - Critical path, blocking others
2. priority:medium - Important, should do this sprint
3. priority:low - Nice to have

Your choice: _
```

**Scope** (REQUIRED - auto-detected or prompted):
```
Detecting scope from context...

✓ Auto-detected: scope:github-workflows (from branch: plugin/github-workflows)

Confirm this scope? [Y/n/other]: _

# OR if not detected:

Select scope (REQUIRED):
Available scopes (from project analysis):
1. scope:agent-builder
2. scope:self-improvement
3. scope:github-workflows
4. scope:testing-expert
5. scope:research-agent
6. [Other - enter custom scope]

Your choice: _
```

**Scope Detection Sources**:
1. Branch context from `env.json` (`branch.scopeLabel`)
2. Branch name parsing (e.g., `feature/auth` → `scope:auth`)
3. Suggested scopes from initialization (`labels.suggestedScopes`)

**Branch** (optional):
```
Associate with branch? (or skip):
Current branches with labels:
1. branch:plugin/github-workflows
2. branch:plugin/agent-builder
3. [Create new branch label]
4. [Skip]

Your choice: _
```

### Step 3: Milestone Assignment

```
Assign to milestone? (or skip):
Open milestones:
1. Phase: Hooks Validation (2/4 issues, due 2024-03-31)
2. v2.0.0 (8/12 issues, due 2024-04-15)
3. [Create new milestone]
4. [Skip]

Your choice: _
```

### Step 4: Relationships

```
Link to other issues? (or skip):

Parent issue (this is a subtask of):
Enter issue number or skip: _

Blocking issues (this is blocked by):
Enter issue numbers (comma-separated) or skip: _

Related issues:
Enter issue numbers (comma-separated) or skip: _
```

### Step 5: Project Board

```
Add to project board?
Available projects:
1. Agent Plugin Development (add to Backlog)
2. [Skip]

Your choice: _
```

### Step 6: Issue Body

Generate structured body:

```markdown
## Summary

[User provides description]

## Parent Issue

Part of #<parent-number> (if specified)

## Blocked By

- #<blocker-1>
- #<blocker-2>

## Related Issues

- #<related-1>
- #<related-2>

## Acceptance Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Additional Context

[User provides context]
```

### Step 7: Validate Required Labels

Before creating, verify all required labels are present:

```
Validating required labels...

✅ Type: enhancement
✅ Priority: priority:high
✅ Scope: scope:github-workflows

All required labels present. Proceeding with issue creation...
```

**If scope is missing**:
```
⚠️ VALIDATION FAILED

Missing required labels:
❌ Scope: Not set

You MUST specify a scope label. Available scopes:
1. scope:agent-builder
2. scope:self-improvement
3. scope:github-workflows
...

Select scope: _
```

### Step 8: Create Issue

Execute creation with all metadata:

```bash
gh issue create \
  --title "Add validation for hook matchers" \
  --body "$BODY" \
  --label "enhancement,priority:high,scope:github-workflows" \
  --milestone "Phase: Hooks Validation" \
  --project "Agent Plugin Development"
```

## Output

```
## Issue Created Successfully

**Issue**: #59 Add validation for hook matchers
**URL**: https://github.com/owner/repo/issues/59

### Applied Configuration

**Labels**:
- Type: enhancement
- Priority: priority:high
- Scope: plugin:agent-builder
- Branch: branch:plugin/agent-builder

**Milestone**: Phase: Hooks Validation

**Relationships**:
- Parent: #55
- Blocked by: #58
- Related: #56, #57

**Project**: Agent Plugin Development (Backlog)

### Next Steps

1. Refine acceptance criteria if needed
2. Move to Todo when ready to start
3. Assign developer when work begins
```

## Non-Interactive Mode

For scripting, pass all options:

```bash
/issue-create "Title" \
  --type enhancement \
  --priority high \
  --scope plugin:agent-builder \
  --branch plugin/agent-builder \
  --milestone "Phase: Hooks Validation" \
  --parent 55 \
  --blocked-by 58 \
  --related 56,57 \
  --project "Agent Plugin Development" \
  --body "Description here"
```

## Conventions Enforced

This command enforces the conventions from [GITHUB_CONVENTIONS.md](../GITHUB_CONVENTIONS.md):

- **No type prefixes** in titles
- **Required labels**: Type + Priority + Scope (ALL THREE)
- **Scope auto-detection** from branch context
- **Status via project board**, not labels
- **Phases via milestones**, not labels
- **Structured body** with acceptance criteria

### Why Scope is Required

Scope labels are mandatory because they:
1. Enable context-aware issue filtering (`/issue-track context`)
2. Allow automatic issue detection in commits (`/commit-smart`)
3. Improve project organization and searchability
4. Prevent "orphan" issues that don't belong to any component

## Integration

### With triaging-issues skill

After creation, the triaging-issues skill can:
- Detect duplicates
- Suggest additional labels
- Recommend priority adjustments

### With organizing-with-labels skill

Validates labels exist and suggests:
- Missing label dimensions
- Inconsistent labeling patterns
