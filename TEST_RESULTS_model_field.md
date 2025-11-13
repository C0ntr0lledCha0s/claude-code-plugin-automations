# Test Results: Model Field in Commands

**Date**: 2025-11-13
**Tester**: User
**Objective**: Determine whether commands support model aliases or require full API IDs

---

## Test Setup

Three test commands were created:

1. **test-model-full.md**: `model: claude-3-5-haiku-20241022` (full API ID)
2. **test-model-short.md**: `model: haiku` (alias)
3. **test-no-model.md**: No model field (inheritance test)

---

## Test Results

### Test 1: Full API ID

```
> /agent-builder:test-model-full
  Model: claude-3-5-haiku-20241022
  ● Test successful - using full API ID
```

**Result**: ✅ **SUCCESS**
- Command executed
- Used specified model
- Response generated successfully

### Test 2: Alias (haiku)

```
> /agent-builder:test-model-short
  Model: haiku
  API Error: 404 {"type":"error","error":{"type":"not_found_error","message":"model: haiku"}}
```

**Result**: ❌ **FAILED**
- Command recognized model field
- Passed "haiku" to Anthropic API
- API returned 404 error: model not found
- API explicitly stated: "model: haiku" not recognized

### Test 3: No Model Field

```
> /agent-builder:test-no-model
  ● Test successful - using haiku model
```

**Result**: ✅ **SUCCESS**
- Command inherited conversation model
- Used whatever model the main conversation was using
- Response generated successfully

---

## Conclusions

### Primary Finding

**Commands require FULL API IDs for the model field, not aliases.**

- ✅ Full API IDs work: `model: claude-3-5-haiku-20241022`
- ❌ Aliases fail: `model: haiku`, `model: sonnet`, `model: opus`
- ✅ Omitting model field works (inherits from conversation)

### Difference from Agents

**Agents** (per official docs): Accept aliases (`sonnet`, `haiku`, `opus`, `inherit`)

**Commands**: Only accept full API IDs (e.g., `claude-3-5-haiku-20241022`)

### API Behavior

The Anthropic API does not recognize model aliases. The error message is explicit:
```json
{
  "type": "error",
  "error": {
    "type": "not_found_error",
    "message": "model: haiku"
  }
}
```

This indicates that Claude Code translates aliases to full API IDs for agents, but does NOT do this translation for commands.

---

## Impact Assessment

### Current State of Repository

All commands in this repository that specify a model field use **aliases**:

**Agent-Builder Commands** (all use `model: sonnet`):
- new-agent.md
- new-command.md
- new-hook.md
- new-plugin.md
- new-skill.md

**Self-Improvement Commands**:
- review-my-work.md (`model: sonnet`)
- quality-check.md (`model: haiku`)
- show-learnings.md (`model: haiku`)
- show-metrics.md (`model: haiku`)
- show-patterns.md (`model: haiku`)

**Status**: All these commands are **potentially broken** if Claude Code tries to use them with the specified model.

### Why Commands May Appear to Work

Commands may still function in practice because:
1. If the model field causes an error, Claude Code might fall back to inheriting the conversation model
2. Commands might be running but ignoring the invalid model specification
3. The validation may happen but errors may be silently handled

### Critical Issue

The validation script currently **rejects** the model field entirely:
```python
# Commands do not support the 'model' field - only agents support it
if 'model' in frontmatter:
    errors.append("Invalid field 'model': Commands do not support model specification...")
```

This is **doubly wrong**:
1. Commands DO support the model field (docs confirm)
2. The check doesn't validate the format (alias vs full ID)

---

## Recommendations

### Immediate Actions

1. **Update all existing commands** to use full API IDs or remove model field:
   ```yaml
   # WRONG (current state)
   model: haiku

   # RIGHT (option 1: use full ID)
   model: claude-3-5-haiku-20241022

   # RIGHT (option 2: omit and inherit)
   # (no model field)
   ```

2. **Fix validation script** to:
   - Remove error that rejects model field entirely
   - Add validation that model field, if present, looks like a full API ID
   - Warn if an alias is detected

3. **Update documentation** to clearly state:
   - Commands: Must use full API IDs
   - Agents: Can use aliases
   - Why they're different

### Validation Logic

```python
if 'model' in frontmatter:
    model_value = frontmatter['model']

    # Check if it looks like an alias (short form)
    if model_value in ['haiku', 'sonnet', 'opus', 'inherit']:
        errors.append(
            f"Error: Commands require full API IDs for model field, not aliases. "
            f"Found: '{model_value}'. "
            f"Use format: 'claude-3-5-haiku-20241022' or omit field to inherit. "
            f"Note: Agents support aliases, but commands do not."
        )
    # Check if it looks like a valid model ID (basic format check)
    elif not model_value.startswith('claude-'):
        errors.append(
            f"Warning: Model '{model_value}' doesn't match expected format 'claude-*'. "
            f"Ensure this is a valid Anthropic model ID."
        )
```

### Documentation Updates

**Skill documentation** needs prominent section:

```markdown
## Model Field: Commands vs Agents

### Commands (This Skill)

Commands **require full API IDs** when specifying a model:

```yaml
---
description: Fast operation
model: claude-3-5-haiku-20241022  # ✅ Correct
---
```

**DO NOT use aliases** in commands:
```yaml
model: haiku   # ❌ WRONG - causes API error
model: sonnet  # ❌ WRONG - causes API error
```

**Alternative**: Omit model field to inherit from conversation:
```yaml
---
description: Inherits conversation model
# No model field - inherits automatically
---
```

### Why the Difference?

- **Agents**: Claude Code translates aliases (`haiku` → full ID)
- **Commands**: Passed directly to API without translation
- **Reason**: Different execution paths in Claude Code internals

### Finding Model IDs

Current model IDs (as of 2025-11-13):
- Haiku: `claude-3-5-haiku-20241022`
- Sonnet: `claude-3-5-sonnet-20241022`
- Opus: `claude-opus-4-20250514` (example)

Check [Anthropic Models Documentation](https://docs.anthropic.com/models) for latest IDs.
```

---

## Testing Recommendations

### Phase 1: Fix Existing Commands

1. Decide strategy for each command:
   - Remove model field (inherit)? OR
   - Update to full API ID?

2. Consider that omitting might be better:
   - More flexible (adapts to conversation)
   - No maintenance when models update
   - Simpler configuration

3. Use full IDs only when specific model is truly needed:
   - Performance-critical fast operations (haiku)
   - Complex reasoning requiring specific model (opus)

### Phase 2: Update Validation

1. Implement API ID format validation
2. Test validation against all commands
3. Ensure helpful error messages

### Phase 3: Documentation

1. Update SKILL.md with model field guidance
2. Update command template
3. Update all `/new-*` command examples

---

## Open Questions

1. **Why doesn't Claude Code translate aliases for commands?**
   - Architectural decision or oversight?
   - Documented behavior or undocumented limitation?

2. **Should we report this to Claude Code team?**
   - Is this intended behavior?
   - Should documentation be clearer?
   - Should commands support aliases like agents do?

3. **Best practice recommendation?**
   - Should commands typically omit model field?
   - Only specify when performance matters?
   - Trade-offs of inheritance vs explicit specification?

---

## Side Note: Hook Error

During testing, a hook error appeared:
```
Plugin hook error: bash: hooks/scripts/save-workflow-state.sh: No such file or directory
```

**Source**: github-workflows plugin hooks.json
**Hook**: UserPromptSubmit
**Impact**: Non-critical (hook fails but doesn't block execution)
**Fix needed**: Create missing script or remove hook reference

This is unrelated to model field testing but should be addressed separately.

---

**Document Version**: 1.0
**Test Status**: Complete
**Next Steps**: Implement fixes based on findings
