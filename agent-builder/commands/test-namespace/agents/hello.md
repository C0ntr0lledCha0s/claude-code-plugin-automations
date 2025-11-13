---
description: Test command to verify namespacing works correctly
model: haiku
---

# Test Namespace Command: Hello

This is a test command located at `agent-builder/commands/test-namespace/agents/hello.md`.

**Expected command name:** `/hello` (NOT `/test-namespace:agents:hello`)

According to the docs: "The subdirectories are used for organization and appear in the command description, but they do not affect the command name itself."

**What this test validates:**
- Command should be invoked as `/hello`
- Description should show the namespace path for organization
- Subdirectories don't create nested command names

**Test instructions:**
1. Type `/hello` in Claude Code
2. Verify this message appears
3. Check if namespace appears in command help/description

---

✅ If you see this message, namespacing is working!
The command name is derived from the filename (`hello.md` → `/hello`), not the directory path.
