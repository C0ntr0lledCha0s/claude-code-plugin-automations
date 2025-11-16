---
description: Automatically apply quality improvements to a Claude Code component based on analysis
allowed-tools: Read, Edit, Bash
argument-hint: "<component-path>"
model: sonnet
---

# Improve Component Quality

You are improving the quality of a Claude Code component by applying systematic enhancements based on quality analysis.

## Task

Improve the component at path: `$1`

## Process

### 1. Analyze Current Quality

First, analyze the component to identify improvement opportunities:

```bash
/analyze-component $1
```

Or directly invoke the `analyzing-component-quality` skill to get quality scores and improvement suggestions.

### 2. Plan Improvements

Based on the quality analysis, create an improvement plan:

```markdown
## Improvement Plan for [Component Name]

**Current Quality**: X.X/5
**Target Quality**: X.X/5

### Priority 1: Critical Issues
- [ ] [Issue 1]
- [ ] [Issue 2]

### Priority 2: Important Issues
- [ ] [Issue 3]
- [ ] [Issue 4]

### Priority 3: Nice to Have
- [ ] [Issue 5]
```

### 3. Apply Improvements

Invoke the `improving-components` skill and apply improvements systematically:

#### A. Description Enhancement

If description is vague or missing triggers:

```yaml
# Before
description: Helps with testing

# After (use Edit tool)
description: Expert at writing Jest unit tests for JavaScript/TypeScript. Auto-invokes when user writes new functions or asks "test this code". Generates comprehensive test suites with mocks, assertions, and edge cases following AAA pattern.
```

Apply using Edit tool:
```bash
Edit $1:
  old_string: "description: [old vague description]"
  new_string: "description: [specific detailed description]"
```

#### B. Tool Permission Optimization

If tools are excessive or unjustified:

```yaml
# Before
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task

# After (for research skill)
allowed-tools: Read, Grep, Glob, WebSearch, WebFetch
```

Apply using Edit tool:
```bash
Edit $1:
  old_string: "allowed-tools: [old excessive list]"
  new_string: "allowed-tools: [minimal necessary list]"
```

#### C. Documentation Enhancement

If missing examples or structure:

Add sections like:
```markdown
## Capabilities

- [Specific capability 1]
- [Specific capability 2]

## Examples

### Example 1: [Scenario]
```
User: "How does X work?"
Skill: [Action]
Result: [Outcome]
```

### Example 2: [Scenario]
[Another example]
```

Apply using Edit tool to insert at appropriate location.

#### D. Security Improvements

If security concerns exist:

- Remove unnecessary Bash access
- Add input validation notes
- Eliminate dangerous tool combinations
- Add security documentation

### 4. Validate Improvements

After applying changes:

```bash
# Re-run quality analysis
python self-improvement/skills/analyzing-component-quality/scripts/quality-scorer.py "$1"
```

Verify:
- ✓ Quality score improved
- ✓ Critical issues resolved
- ✓ No new issues introduced
- ✓ Component still functional

### 5. Present Results

Show a comprehensive before/after report:

```markdown
# Component Improvement Report

**Component**: [name]
**Type**: [type]
**Location**: `$1`

## Changes Applied

### 1. Description Enhanced
**Before**:
```yaml
description: Helps with code
```

**After**:
```yaml
description: Expert at analyzing code quality using ESLint, Prettier, and static analysis. Auto-invokes when user finishes writing code or asks "is this code good?". Provides actionable improvement suggestions with severity levels.
```

**Impact**: Description Clarity improved from 2/5 to 5/5 (+3 points)

### 2. Tool Permissions Optimized
**Before**: `Read, Write, Edit, Bash, Grep, Glob, Task`
**After**: `Read, Bash`

**Removed**:
- Write, Edit: Code analysis doesn't modify files
- Grep, Glob: Linters handle searching
- Task: Skills don't delegate to agents

**Kept**:
- Read: Needed to read code files
- Bash: Needed to run linters (eslint, prettier)

**Impact**:
- Tool Permissions improved from 2/5 to 4/5 (+2 points)
- Security improved from 3/5 to 4/5 (+1 point)

### 3. Documentation Added
**Added**:
- Capabilities section
- 3 usage examples
- When to use vs. when not to use
- Integration examples

**Impact**: Usability improved from 3/5 to 5/5 (+2 points)

## Quality Score Improvement

| Dimension | Before | After | Change |
|-----------|--------|-------|--------|
| Description Clarity | 2/5 | 5/5 | +3 |
| Tool Permissions | 2/5 | 4/5 | +2 |
| Auto-Invoke Triggers | 2/5 | 5/5 | +3 |
| Security | 3/5 | 4/5 | +1 |
| Usability | 3/5 | 5/5 | +2 |
| **Overall** | **2.4/5** | **4.6/5** | **+2.2** |

**Quality Level**: Poor → Excellent ✅

## Remaining Recommendations

[Any suggestions not automatically applied, if any]

## Files Modified

- `$1` - Component improved

## Next Steps

1. **Review changes**: Examine the diff to ensure all changes are appropriate
2. **Test component**: Verify it still works as intended
3. **Commit changes**:
   ```bash
   git add $1
   git commit -m "feat(self-improvement): enhance [component-name] quality

   - Improved description clarity and specificity
   - Optimized tool permissions for security
   - Added comprehensive documentation and examples

   Quality score: 2.4/5 → 4.6/5 (+2.2 points)"
   ```

4. **Validate with agent-builder** (optional):
   ```bash
   python agent-builder/skills/building-[type]s/scripts/validate-[type].py "$1"
   ```
```

## Improvement Guidelines

### What to Improve

**Always improve**:
- Vague descriptions → Specific descriptions
- Excessive tools → Minimal necessary tools
- Security vulnerabilities → Secure patterns
- Missing documentation → Comprehensive docs

**Carefully improve**:
- Existing functionality (preserve behavior)
- Working auto-invoke triggers (ensure backward compatible)
- Tool lists (verify each change necessary)

**Never change**:
- Component name (breaking change)
- Core functionality (preserve intent)
- Version number (user manages this)

### Safety Checks

Before applying each improvement:
- [ ] Preserves component functionality
- [ ] Doesn't break existing usage
- [ ] Improves quality score
- [ ] No new issues introduced
- [ ] Changes are justified

### When to Ask User

Ask user confirmation before:
- Removing tools that might be needed
- Making changes that could affect existing usage
- Large-scale restructuring
- Uncertain about intent

**Example**:
```
I've identified that the Task tool may be unnecessary for this skill.
Removing it would improve security score from 3/5 to 5/5.

Current: allowed-tools: Read, Grep, Glob, Task
Proposed: allowed-tools: Read, Grep, Glob

Should I remove the Task tool? (y/n)
```

## Advanced Improvements

### Pattern-Based Improvements

Apply common improvement patterns:

**Pattern 1**: Research Skill Optimization
```
IF component_type == 'skill' AND 'research' in description:
  KEEP: Read, Grep, Glob, WebSearch, WebFetch
  REMOVE: Write, Edit, Bash, Task
```

**Pattern 2**: Code Generation Skill Optimization
```
IF component_type == 'skill' AND 'generate' in description:
  KEEP: Read, Write, Grep, Glob
  REMOVE: Bash (unless running tests), Task
```

**Pattern 3**: Agent Tool Optimization
```
IF component_type == 'agent':
  REMOVE: Task (agents shouldn't delegate to agents)
```

### Bulk Improvements

If multiple components need similar improvements:

```markdown
Detected pattern: 5 skills have Task tool but don't delegate to agents

Apply bulk improvement?
- research-skill: Remove Task tool
- analysis-skill: Remove Task tool
- pattern-skill: Remove Task tool
- best-practices-skill: Remove Task tool
- investigation-skill: Remove Task tool

Total impact: +10 security points across 5 components

Apply to all? (y/n)
```

## Output Format

Provide a comprehensive improvement report that:
- ✓ Shows before/after for each change
- ✓ Quantifies quality improvements
- ✓ Explains rationale for changes
- ✓ Lists all modified files
- ✓ Provides next steps
- ✓ Includes validation results

## Important Notes

- **Preserve functionality**: Never change what the component does
- **Incremental changes**: Apply one category at a time
- **Validate after**: Always re-run quality scoring
- **Show evidence**: Demonstrate quality improved
- **Be conservative**: When unsure, ask user
- **Document reasoning**: Explain why each change helps

Your improvements make components more effective, secure, and maintainable for the entire Claude Code ecosystem.
