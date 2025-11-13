# Next Steps: Building-Commands Investigation & Fixes

**Status**: Testing phase - awaiting user confirmation on version aliases
**Date**: 2025-11-13

---

## What We've Completed

### ✅ 1. Test Results - Basic Model Field Behavior (CONFIRMED)

- ❌ Short aliases fail: `model: haiku`, `model: sonnet` → API 404 error
- ✅ Full IDs work: `model: claude-3-5-haiku-20241022` → SUCCESS
- ✅ No model field works: Inherits from conversation → SUCCESS

**See**: [TEST_RESULTS_model_field.md](TEST_RESULTS_model_field.md)

### ✅ 2. Fixed Validation Script

**File**: [agent-builder/skills/building-commands/scripts/validate-command.py](agent-builder/skills/building-commands/scripts/validate-command.py#L91-L120)

**Changes**:
- ✅ Fixed crash when `argument-hint` is a list (was: AttributeError)
- ✅ Now handles both string and list types for argument-hint
- ✅ Rejects short aliases (`haiku`, `sonnet`, `opus`)
- ✅ Validates model field starts with `claude-`

**Testing**:
```bash
# Correctly rejects alias
python3 agent-builder/skills/building-commands/scripts/validate-command.py \
  agent-builder/commands/test-model-short.md
# Output: CRITICAL ERROR - requires full API IDs

# Correctly accepts full ID
python3 agent-builder/skills/building-commands/scripts/validate-command.py \
  agent-builder/commands/test-model-full.md
# Output: No critical errors
```

### ✅ 3. Updated SKILL.md Documentation

**File**: [agent-builder/skills/building-commands/SKILL.md](agent-builder/skills/building-commands/SKILL.md#L39-L124)

**Added**:
- Clear distinction between Required vs Recommended fields
- ⚠️ CRITICAL section explaining model field commands vs agents
- Examples of correct and incorrect usage
- Explanation of why aliases work in agents but not commands
- Documentation of `disable-model-invocation` field
- Links to Anthropic API documentation

### ✅ 4. Created Analysis Documents

- **Main Analysis**: [ANALYSIS_building_commands_effectiveness.md](ANALYSIS_building_commands_effectiveness.md)
- **Test Results**: [TEST_RESULTS_model_field.md](TEST_RESULTS_model_field.md)
- **This Document**: NEXT_STEPS.md

---

## 🚨 Awaiting User Testing

### New Discovery: Version Aliases

Per [Anthropic's model documentation](https://docs.claude.com/en/docs/about-claude/models/overview), there are **three formats**:

1. **Short aliases** (work in agents only):
   - `haiku`, `sonnet`, `opus`
   - ❌ Confirmed broken in commands

2. **Version aliases** (may work in commands?):
   - `claude-sonnet-4-5`
   - `claude-haiku-4-5`
   - `claude-opus-4-1`
   - ❓ Need to test

3. **Full IDs with dates** (confirmed working):
   - `claude-sonnet-4-5-20250929`
   - `claude-haiku-4-5-20251001`
   - `claude-opus-4-1-20250805`
   - ✅ Confirmed working

### Test Command Created

**File**: [agent-builder/commands/test-model-version-alias.md](agent-builder/commands/test-model-version-alias.md)

**Uses**: `model: claude-haiku-4-5` (version alias without date)

### Action Required

**Please test**: `/agent-builder:test-model-version-alias`

**Expected Outcomes**:
- **If it works**: Version aliases are acceptable, validation should allow them
- **If it fails**: Only full IDs work, validation is correct as-is

---

## Pending Tasks Based on Test Results

### Scenario A: Version Aliases Work

If `/test-model-version-alias` succeeds:

1. **Update validation script** to accept version aliases:
   ```python
   # Accept: claude-sonnet-4-5 OR claude-sonnet-4-5-20250929
   # Reject: sonnet, haiku, opus (short aliases only)
   ```

2. **Update documentation** to show both formats:
   ```yaml
   # Option 1: Version alias (auto-updates to latest snapshot)
   model: claude-haiku-4-5

   # Option 2: Full ID (locked to specific snapshot)
   model: claude-haiku-4-5-20251001
   ```

3. **Fix existing commands** using either format:
   - For stable behavior: Use full IDs
   - For auto-updates: Use version aliases

### Scenario B: Version Aliases Fail

If `/test-model-version-alias` fails with API 404:

1. **Validation is correct as-is** (already rejects short aliases)

2. **Update error message** to show example of full ID format

3. **Fix ALL existing commands** to remove model field or use full IDs

4. **Recommendation**: Remove model field from most commands (inheritance better)

---

## Current State of Commands in Repository

### Commands with Invalid Model Aliases

**Agent-Builder** (all use `model: sonnet`):
- [new-agent.md](agent-builder/commands/new-agent.md#L5)
- [new-command.md](agent-builder/commands/new-command.md#L5)
- [new-hook.md](agent-builder/commands/new-hook.md#L5)
- [new-plugin.md](agent-builder/commands/new-plugin.md#L5)
- [new-skill.md](agent-builder/commands/new-skill.md#L5)

**Self-Improvement**:
- [review-my-work.md](self-improvement/commands/review-my-work.md#L4) (`model: sonnet`)
- [quality-check.md](self-improvement/commands/quality-check.md#L4) (`model: haiku`)
- [show-learnings.md](self-improvement/commands/show-learnings.md#L4) (`model: haiku`)
- [show-metrics.md](self-improvement/commands/show-metrics.md#L4) (`model: haiku`)
- [show-patterns.md](self-improvement/commands/show-patterns.md#L4) (`model: haiku`)

**Total**: 11 commands with potentially broken model fields

### GitHub-Workflows Commands

**Status**: ✅ Good - Do NOT use model field (correctly inherit)

Examples:
- [pr-review-request.md](github-workflows/commands/pr-review-request.md) - No model field
- [workflow-status.md](github-workflows/commands/workflow-status.md) - No model field

---

## Recommended Fix Strategy

### Conservative Approach (Recommended)

**Remove model field from most commands**, let them inherit:

**Rationale**:
- More flexible (adapts to user's conversation model)
- No maintenance when models update
- Simpler configuration
- No risk of API errors

**Exception**: Only specify model when truly needed:
- Performance-critical fast operations
- Specific capability requirements

### Example Fixes

**Before** (agent-builder/commands/new-command.md):
```yaml
---
description: Create a new Claude Code slash command
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
argument-hint: [command-name]
model: sonnet  # ❌ BROKEN
---
```

**After** (Option 1 - Remove model field):
```yaml
---
description: Create a new Claude Code slash command
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
argument-hint: [command-name]
# No model field - inherits from conversation
---
```

**After** (Option 2 - Use version alias, IF test passes):
```yaml
---
description: Create a new Claude Code slash command
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
argument-hint: [command-name]
model: claude-sonnet-4-5  # Version alias
---
```

**After** (Option 3 - Use full ID):
```yaml
---
description: Create a new Claude Code slash command
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
argument-hint: [command-name]
model: claude-sonnet-4-5-20250929  # Full ID with date
---
```

---

## Additional Issues Found

### Minor: Hook Script Missing

**Issue**: github-workflows plugin references non-existent script
```json
"command": "bash hooks/scripts/save-workflow-state.sh"
```

**Error**: `bash: hooks/scripts/save-workflow-state.sh: No such file or directory`

**Impact**: Low (hook fails but doesn't block operations)

**Fix**: Create the script or remove the hook reference

---

## Timeline Estimate

### If Version Aliases Work
- Test version alias: 2 minutes (user)
- Update validation: 30 minutes
- Update documentation: 1 hour
- Fix commands: 30 minutes
- Final testing: 30 minutes
- **Total**: ~2.5 hours

### If Version Aliases Don't Work
- Test version alias: 2 minutes (user)
- Fix all 11 commands: 20 minutes
- Final testing: 30 minutes
- **Total**: ~1 hour

---

## Questions for User

1. **Version alias test result**: Does `/agent-builder:test-model-version-alias` work?

2. **Fix strategy preference**: Should we:
   - Remove model field from most commands (recommended)?
   - Update to version aliases (if they work)?
   - Update to full IDs?

3. **Hook script**: Should we:
   - Create the missing save-workflow-state.sh script?
   - Remove the hook reference?
   - Ignore for now (low priority)?

4. **Validation strictness**: Should validation:
   - Error on any model field issues (strict)?
   - Warn but allow (permissive)?
   - Current approach (error on short aliases, warn on non-claude- format)?

---

## Success Criteria

✅ All commands pass validation without critical errors
✅ No API 404 errors when commands execute
✅ Documentation clearly explains model field usage
✅ Template shows correct format
✅ Users understand when to specify model vs inherit

---

## References

- **Anthropic Models**: https://docs.claude.com/en/docs/about-claude/models/overview
- **Claude Code Commands**: https://code.claude.com/docs/en/slash-commands
- **Claude Code Agents**: https://code.claude.com/docs/en/sub-agents

---

**Next Action**: Await user test of `/agent-builder:test-model-version-alias`

**Document Version**: 1.0
**Last Updated**: 2025-11-13
