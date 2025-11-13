---
description: Second test command in the same namespace directory
model: haiku
---

# Test Namespace Command: World

This is a test command located at `agent-builder/commands/test-namespace/agents/world.md`.

**Expected command name:** `/world` (NOT `/test-namespace:agents:world`)

**Purpose:** Verify multiple commands in the same namespace directory work correctly.

**Key insight from docs:**
> "The subdirectories are used for organization and appear in the command description, but they do not affect the command name itself."

This means:
- `/hello` and `/world` both exist as flat commands
- They're organized in `test-namespace/agents/` for structure
- No actual command nesting happens

---

✅ If you see this message, the second namespaced command works!
