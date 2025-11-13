---
description: Brief description of what this command does
allowed-tools: Read, Grep, Glob, Bash
argument-hint: "[arg1] [arg2]"
# model: claude-haiku-4-5  # Optional: version alias (recommended) or full ID
---

# Command Name

Brief description of the command's purpose and what it accomplishes.

## Arguments

- **`$1`**: Description of first argument (e.g., file path, PR number, search term)
- **`$2`**: Description of second argument (optional)
- **`$ARGUMENTS`**: Use this to capture all arguments as a single string (for commit messages, etc.)

## Workflow

When this command is invoked with `/command-name arg1 arg2`:

1. **Validate Arguments**: Check that required arguments are provided and valid
2. **Gather Context**: Read relevant files or fetch necessary information
3. **Perform Action**: Execute the main command logic
4. **Report Results**: Provide clear feedback about what was done

## Examples

### Example Usage 1
```
/command-name value1 value2
```

Expected behavior:
1. Validates value1 and value2
2. Performs [specific action]
3. Reports completion status

### Example Usage 2
```
/command-name "argument with spaces"
```

Expected behavior:
1. Handles argument with proper quoting
2. Performs [specific action]
3. Returns results

## Important Notes

- Note about required setup or context
- Note about side effects or state changes
- Note about error handling
- Note about permissions needed

## Error Handling

If arguments are missing or invalid:
- Display clear error message
- Show usage example
- Suggest correct format
