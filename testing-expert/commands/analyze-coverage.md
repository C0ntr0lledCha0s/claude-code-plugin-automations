---
description: Analyze test coverage reports, identify gaps, and recommend tests for uncovered code paths
allowed-tools: Read, Grep, Glob, Bash
argument-hint: "[coverage-report-path]"
---

# Analyze Coverage

Analyze code coverage reports to identify gaps and recommend specific tests for uncovered code.

## Arguments

- **`$1`**: (Optional) Path to coverage report or directory. Defaults to common locations:
  - `coverage/lcov-report/`
  - `coverage/`
  - `.nyc_output/`

## Workflow

When this command is invoked with `/testing-expert:analyze-coverage [path]`:

1. **Locate Coverage Data**
   - Find coverage reports (lcov.info, coverage-final.json)
   - Parse coverage summary
   - Identify coverage tool (Istanbul/nyc, c8, Jest)

   **Search patterns**:
   ```bash
   # Find coverage files
   find . -name "lcov.info" -o -name "coverage-final.json" -o -name "coverage-summary.json" 2>/dev/null
   ```

2. **Analyze Metrics**
   - Statement coverage
   - Branch coverage
   - Function coverage
   - Line coverage

   **Parsing lcov.info**:
   ```bash
   # Extract per-file summaries
   grep -E "^(SF|LF|LH|BRF|BRH|FNF|FNH):" coverage/lcov.info

   # SF: Source File
   # LF/LH: Lines Found/Hit
   # BRF/BRH: Branches Found/Hit
   # FNF/FNH: Functions Found/Hit
   ```

   **Parsing coverage-summary.json**:
   ```bash
   # Read summary metrics
   cat coverage/coverage-summary.json | jq '.total'
   ```

3. **Identify Gaps**
   - Uncovered functions
   - Uncovered branches
   - Complex uncovered code
   - Critical path gaps

   **Finding uncovered lines in lcov**:
   ```bash
   # Extract uncovered line ranges (DA:line,0 means uncovered)
   grep "^DA:" coverage/lcov.info | grep ",0$"

   # Find uncovered functions (FNDA:0,funcName)
   grep "^FNDA:0," coverage/lcov.info
   ```

   **Parsing coverage-final.json for uncovered**:
   ```bash
   # Find files with < 80% line coverage
   cat coverage/coverage-final.json | jq 'to_entries | .[] | select(.value.s | to_entries | map(select(.value == 0)) | length > 0) | .key'
   ```

4. **Prioritize by Risk**
   - Error handling code
   - Validation logic
   - Business-critical paths
   - Edge case handlers

5. **Generate Test Suggestions**
   For each significant gap:
   - Describe what needs testing
   - Provide test outline
   - Suggest test data

## Report Format

```markdown
## Coverage Analysis Report

### Overall Coverage
| Metric     | Coverage | Target | Status |
|------------|----------|--------|--------|
| Statements | 85%      | 80%    | ✅      |
| Branches   | 72%      | 75%    | ⚠️      |
| Functions  | 90%      | 80%    | ✅      |
| Lines      | 85%      | 80%    | ✅      |

### Critical Gaps

#### 1. [File:Function] - 0% covered
**Risk**: High - handles error scenarios
**Suggested test**:
```javascript
it('should handle network error', async () => {
  // Test outline
});
```

### Recommendations
1. [Prioritized list of tests to add]
```

## Examples

### Analyze Default Coverage
```
/testing-expert:analyze-coverage
```

Finds and analyzes coverage in default locations.

### Analyze Specific Report
```
/testing-expert:analyze-coverage coverage/lcov.info
```

Analyzes specific coverage file.

### Analyze After Test Run
```bash
npm test -- --coverage
/testing-expert:analyze-coverage
```

Run tests with coverage then analyze results.

## Coverage Priorities

### High Priority Gaps
- Error handling (catch blocks)
- Validation functions
- Authentication/authorization
- Data transformation
- API boundaries

### Medium Priority
- Edge cases
- Conditional branches
- Utility functions
- Event handlers

### Lower Priority
- Simple getters/setters
- Debug/logging code
- Configuration

## Important Notes

- High coverage ≠ good tests
- Focus on meaningful coverage
- Consider mutation testing for quality
- Branch coverage often reveals logic gaps
- Some code may be intentionally uncovered

## Generating Coverage

If no coverage exists, suggest running:

### Jest
```bash
npx jest --coverage
```

### Vitest
```bash
npx vitest --coverage
```

### Node.js (c8)
```bash
npx c8 node script.js
```

## Error Handling

If coverage reports are not found:
- Suggest running tests with coverage flag
- Check for correct coverage tool
- Verify output directory configuration
