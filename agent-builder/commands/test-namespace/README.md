# Namespacing Test for Commands

This directory contains test commands to validate how namespacing works in Claude Code.

## Test Structure

```
agent-builder/commands/test-namespace/
└── agents/
    ├── hello.md    → Creates /hello command
    └── world.md    → Creates /world command
```

## Expected Behavior (Based on Docs)

According to [Claude Code documentation](https://code.claude.com/docs/en/slash-commands#namespacing):

> "The subdirectories are used for organization and appear in the command description, but they do not affect the command name itself."

This means:
- **Command name** is derived from the **filename only** (not the directory path)
- **Subdirectories** are for **organization** and may appear in descriptions
- **No nested command names** like `/test-namespace:agents:hello`

## Test Commands

### `/hello`
- File: `test-namespace/agents/hello.md`
- Should be invoked as: `/hello`
- Tests: Basic namespacing functionality

### `/world`
- File: `test-namespace/agents/world.md`
- Should be invoked as: `/world`
- Tests: Multiple commands in same namespace

## How to Test

1. **List available commands** (if there's a `/help` or commands list)
   - Look for `/hello` and `/world`
   - Check if namespace path appears in description

2. **Invoke the commands:**
   ```
   /hello
   /world
   ```

3. **Observe:**
   - Do the commands execute?
   - Is the command name flat (e.g., `/hello`) or nested?
   - Does the description show organizational context?

## Questions to Answer

- ✓ Do subdirectories automatically get discovered?
- ✓ Is the command name just the filename?
- ? Does the namespace appear in command descriptions?
- ? Is there any conflict resolution if same filename exists in different subdirs?
- ? Does this work the same way for plugin commands as project commands?

## Potential Issues

If namespacing doesn't work as expected:
1. Commands might not be discovered at all
2. Command names might include the full path
3. Multiple files with same name might conflict
4. Plugin loading might fail

## Cleanup

After testing, either:
- Delete this entire `test-namespace/` directory if not using namespacing
- Keep as reference if implementing full namespace structure
