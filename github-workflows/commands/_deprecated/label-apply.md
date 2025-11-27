---
description: Bulk apply labels to issues based on filters
allowed-tools: Bash
argument-hint: "<label> [--filter FILTER] [--remove]"
---

# Label Apply

Bulk apply (or remove) labels to/from multiple issues based on filters.

## Usage

```bash
/label-apply priority:high --filter "is:open no:milestone"
/label-apply needs-triage --filter "is:open no:label"
/label-apply scope:backend --filter "is:open label:api"
/label-apply stale --remove --filter "updated:>2024-01-01"
```

## Arguments

- **First argument** (required): Label to apply or remove
  - Must be an existing label in the repository
  - Creates label if it doesn't exist (with confirmation)

- **--filter FILTER** (optional): GitHub search filter
  - Uses GitHub issue search syntax
  - Default: `is:open` (all open issues)

- **--remove** (optional): Remove the label instead of applying

## What This Does

1. **Search issues**: Find issues matching the filter
2. **Validate label**: Check if label exists
3. **Preview changes**: Show which issues will be affected
4. **Apply/Remove**: Bulk update issues
5. **Report results**: Summary of changes

## Filter Examples

```bash
# All open issues without labels
is:open no:label

# Issues in a specific milestone
is:open milestone:"Sprint 5"

# Issues with specific label
is:open label:bug

# Issues assigned to someone
is:open assignee:username

# Issues created recently
is:open created:>2024-01-01

# Combined filters
is:open label:bug no:milestone -label:wontfix
```

## Workflow

When this command is invoked:

### Step 1: Parse Arguments

```bash
LABEL="$1"
FILTER="${2:-is:open}"
ACTION="${3:-add}"  # add or remove
```

### Step 2: Validate Label

```bash
# Check if label exists
EXISTING=$(gh label list --json name --jq ".[] | select(.name == \"$LABEL\")")

if [ -z "$EXISTING" ]; then
  echo "Label '$LABEL' doesn't exist."
  echo "Create it? [y/N]"
  # If yes: gh label create "$LABEL"
fi
```

### Step 3: Search Issues

```bash
# Get matching issues
ISSUES=$(gh issue list --search "$FILTER" --json number,title,labels --limit 100)

# Count
COUNT=$(echo "$ISSUES" | jq length)
echo "Found $COUNT issues matching filter"
```

### Step 4: Preview Changes

```bash
echo "Issues to modify:"
echo "$ISSUES" | jq -r '.[] | "  #\(.number): \(.title)"'

echo ""
echo "Action: $ACTION label '$LABEL'"
echo "Proceed? [y/N]"
```

### Step 5: Apply Changes

```bash
# For each issue
echo "$ISSUES" | jq -r '.[].number' | while read -r NUM; do
  if [ "$ACTION" = "add" ]; then
    gh issue edit "$NUM" --add-label "$LABEL"
  else
    gh issue edit "$NUM" --remove-label "$LABEL"
  fi
  echo "✓ #$NUM"
done
```

### Step 6: Report Results

```bash
echo ""
echo "Summary:"
echo "  Issues modified: $COUNT"
echo "  Label: $LABEL ($ACTION)"
echo "  Filter: $FILTER"
```

## Common Use Cases

### Triage New Issues

```bash
# Apply needs-triage to unlabeled issues
/label-apply needs-triage --filter "is:open no:label"
```

### Priority Escalation

```bash
# Escalate old high-priority bugs
/label-apply priority:critical --filter "is:open label:bug label:priority:high created:<2024-01-01"
```

### Sprint Management

```bash
# Mark issues for current sprint
/label-apply sprint:current --filter "is:open milestone:\"Sprint 5\""
```

### Cleanup

```bash
# Remove stale label from recently updated issues
/label-apply stale --remove --filter "is:open updated:>2024-01-01"
```

### Scope Labeling

```bash
# Apply scope label based on existing labels
/label-apply scope:frontend --filter "is:open label:ui"
/label-apply scope:backend --filter "is:open label:api"
```

## Output Example

```
Searching issues with filter: is:open no:label

Found 5 issues:
  #42: Fix authentication bug
  #45: Add password reset feature
  #47: Update documentation
  #50: Refactor API routes
  #52: Add unit tests

Action: ADD label 'needs-triage'
Proceed? [y/N] y

✓ #42
✓ #45
✓ #47
✓ #50
✓ #52

Summary:
  Issues modified: 5
  Label: needs-triage (add)
  Filter: is:open no:label
```

## Safety Features

- **Preview before apply**: Always shows affected issues
- **Confirmation required**: Won't apply without user confirmation
- **Rate limiting**: Respects GitHub API rate limits
- **Error handling**: Reports failures without stopping

## Integration

Works with:
- **label-suggest**: Use suggestions to determine which labels to apply
- **label-sync**: Ensure label taxonomy exists before bulk applying
- **organizing-with-labels skill**: For label management best practices

## Notes

- Limited to 100 issues per run (pagination not implemented)
- Some filters may not work with `gh issue list --search`
- Use `--remove` carefully - no undo
- Consider creating a backup label before bulk removal
