---
description: Update existing documentation to match current code
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
argument-hint: "[file-path] [--check-only]"
---

# Documentation Updater

Update documentation to match the current state of the code.

**Target:** $ARGUMENTS

## Parsing Arguments

1. **File path**: Required - the file to update documentation for
2. **--check-only**: Optional - only report what needs updating, don't make changes

## Update Process

### Step 1: Analyze Current Code
1. Read the target file
2. Parse all functions, classes, and exports
3. Extract:
   - Function signatures (parameters, return types)
   - Class structures (properties, methods)
   - Module exports

### Step 2: Analyze Existing Documentation
1. Find existing documentation for each item
2. Extract documented:
   - Parameter names and types
   - Return values
   - Descriptions

### Step 3: Compare and Identify Mismatches
1. **Missing Parameters**: Params in code but not in docs
2. **Extra Parameters**: Params in docs but not in code
3. **Type Mismatches**: Different types in code vs docs
4. **Missing Documentation**: Items with no docs
5. **Stale Descriptions**: Descriptions that don't match behavior

### Step 4: Generate Updates

For each mismatch:
1. Generate corrected documentation
2. Preserve existing good content
3. Add placeholders for new items
4. Mark items for human review if unclear

### Step 5: Apply Changes (unless --check-only)

1. Show diff of proposed changes
2. Ask for confirmation
3. Apply updates
4. Report summary

## Output Modes

### Check-Only Mode (--check-only)
```markdown
## Documentation Update Report

### Outdated Documentation Found

**file.js:functionName**
- Parameter `newParam` added but not documented
- Return type changed from `string` to `Promise<string>`

**file.js:className**
- Method `newMethod` added but not documented
- Property `oldProp` removed but still documented

### Summary
- 3 functions need updates
- 2 classes need updates
- 5 total documentation changes needed
```

### Update Mode (default)
1. Show proposed changes with diffs
2. Ask for confirmation
3. Apply changes
4. Show summary of updates made

## Handling Ambiguous Cases

When the correct documentation is unclear:
1. Add a `TODO:` marker
2. Include both old and new information
3. Flag for human review

Example:
```javascript
/**
 * TODO: Verify description still accurate after refactor
 * [Previous: Does X and Y]
 * [Current signature suggests: Does X with new behavior]
 *
 * @param {string} param - TODO: Confirm purpose
 */
```

## Best Practices

1. **Preserve human-written content** when possible
2. **Don't over-generate** - only update what's actually wrong
3. **Mark uncertainty** - don't guess at descriptions
4. **Show diffs** before making changes
5. **Allow partial updates** - let user accept/reject individual changes
