# Namespace Test Instructions

## What We Created

A test namespace structure to validate how command subdirectories work in Claude Code:

```
agent-builder/commands/
├── test-namespace/
│   ├── README.md           # Test documentation
│   └── agents/
│       ├── hello.md        # Test command 1
│       └── world.md        # Test command 2
├── new-agent.md            # Existing commands (unchanged)
├── new-skill.md
├── new-command.md
├── new-hook.md
└── new-plugin.md
```

## Changes Made

1. **Updated plugin.json**: Changed commands from explicit array to directory reference
   ```json
   "commands": "./commands/"
   ```

2. **Created test commands** in subdirectory structure

## How to Test

### Step 1: Check Command Discovery

Try running the test commands:
```bash
/hello
/world
```

### Step 2: Expected Outcomes

**Hypothesis A (What the docs say):**
- Command name is `/hello` (filename only, not path)
- Subdirectories are for organization
- Both commands should execute

**Hypothesis B (Alternative interpretation):**
- Command might be namespaced: `/test-namespace:agents:hello`
- Or plugin-namespaced: `/agent-builder:hello`

**Hypothesis C (Potential issue):**
- Commands in subdirectories might not be discovered
- Only top-level commands work

### Step 3: Observe & Document

When you run `/hello` or `/world`, check:

1. **Does the command exist?**
   - ✅ Yes → Subdirectory discovery works
   - ❌ No → Subdirectories not supported or require special config

2. **What is the command name?**
   - `/hello` → Flat naming (filename only)
   - `/test-namespace:agents:hello` → Full path namespacing
   - `/agent-builder:hello` → Plugin namespacing

3. **Does it execute correctly?**
   - Should display test message from the command file

4. **Do both commands work?**
   - Tests if multiple commands in same namespace work

## Key Questions to Answer

- [ ] Are commands in subdirectories automatically discovered?
- [ ] Is command name derived from filename only?
- [ ] Does namespace path appear anywhere (descriptions, help)?
- [ ] Do existing commands (`/new-agent`, etc.) still work?

## What This Tells Us

**If subdirectory commands work:**
- ✅ We can use namespacing for better organization
- ✅ Can implement the proposed structure for maintenance commands
- Example: `agents/new.md`, `agents/update.md`, etc.

**If subdirectory commands don't work:**
- ❌ Must keep flat command structure
- ❌ Stick with prefixed names like `new-agent`, `update-agent`
- Consider alternative organization strategies

## Cleanup After Testing

Once you've validated the behavior:

### If namespacing works:
```bash
# Keep the test as reference, or implement full namespace structure
# Proceed with refactoring all commands into subdirectories
```

### If namespacing doesn't work:
```bash
# Remove test directory
rm -rf agent-builder/commands/test-namespace/

# Revert plugin.json to explicit command list
# Keep flat command structure with prefixed names
```

## Next Steps Based on Results

### If Successful:
1. Implement full namespace structure for agent-builder
2. Move existing commands to subdirectories
3. Add new maintenance commands (update, enhance, etc.)
4. Update documentation

### If Unsuccessful:
1. Remove test directory
2. Keep flat structure
3. Use naming conventions instead: `agent:new`, `agent:update`, etc.
4. Or use prefixes: `agent-new`, `agent-update`, etc.

---

**Ready to test!** Try running `/hello` and report back what happens.
