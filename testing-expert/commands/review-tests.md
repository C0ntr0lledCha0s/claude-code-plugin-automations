---
description: Review test quality for a file, directory, or the entire test suite with detailed analysis and improvement recommendations
allowed-tools: Read, Grep, Glob, Bash, Task
argument-hint: "[file-or-directory]"
---

# Review Tests

Perform a comprehensive quality review of tests, analyzing structure, coverage patterns, reliability, and maintainability.

## Arguments

- **`$1`**: (Optional) File path or directory to review. If omitted, reviews entire test suite.
- **`$ARGUMENTS`**: Full path or pattern to analyze

## Workflow

When this command is invoked with `/testing-expert:review-tests [path]`:

1. **Discover Tests**
   - If path provided, find tests in that location
   - If no path, discover all test files using patterns:
     - `**/*.test.{js,ts,jsx,tsx}`
     - `**/*.spec.{js,ts,jsx,tsx}`
     - `**/__tests__/**/*.{js,ts,jsx,tsx}`
     - `**/e2e/**/*.spec.ts`

2. **Identify Framework**
   - Check for `jest.config.*` → Jest
   - Check for `playwright.config.*` → Playwright
   - Check for `vitest.config.*` → Vitest
   - Check package.json for test dependencies

3. **Analyze Test Quality**
   - Structure: AAA pattern, describe nesting, naming
   - Coverage: Happy path, errors, edge cases
   - Reliability: Async handling, isolation, determinism
   - Maintainability: DRY, readability, helpers

   **Anti-pattern detection patterns**:
   ```bash
   # Detect potential flaky tests (timing issues)
   grep -r "setTimeout\|sleep\|delay" --include="*.test.*" --include="*.spec.*"

   # Detect shared mutable state
   grep -r "let \w\+ =" --include="*.test.*" | grep -v "beforeEach\|beforeAll"

   # Detect missing assertions (empty test bodies)
   grep -r "it('\|test('" --include="*.test.*" -A 3 | grep -B 1 "});"

   # Detect nested callbacks (potential async issues)
   grep -r "\.then(.*\.then(" --include="*.test.*"

   # Detect hardcoded timeouts
   grep -r "timeout: [0-9]" --include="*.test.*" --include="*.spec.*"
   ```

   **Quality metrics to calculate**:
   - Test-to-code ratio: `find src -name "*.ts" | wc -l` vs test files
   - Average assertions per test
   - describe/it nesting depth
   - Setup/teardown usage

4. **Generate Report**
   ```markdown
   ## Test Review Summary
   
   📁 **Scope**: [files reviewed]
   🔧 **Framework**: [Jest/Playwright/etc.]
   
   ### Quality Score: X/10
   
   #### ✅ Strengths
   - [what's done well]
   
   #### ⚠️ Issues Found
   - [specific issues with file:line references]
   
   #### 🔧 Recommendations
   - [prioritized improvements with examples]
   ```

5. **Provide Examples**
   - Show before/after code for recommended fixes
   - Reference framework-specific best practices

## Examples

### Review All Tests
```
/testing-expert:review-tests
```

Reviews entire test suite and provides comprehensive report.

### Review Specific Directory
```
/testing-expert:review-tests src/components
```

Reviews only tests for components directory.

### Review Single File
```
/testing-expert:review-tests src/utils/parser.test.ts
```

Deep dive into a specific test file.

## Quality Criteria

### Critical Issues (Must Fix)
- Flaky tests (timing, race conditions)
- Missing error handling tests
- Test pollution (shared state)
- No assertions

### High Priority
- Poor test isolation
- Incomplete coverage
- Unclear test names
- Missing edge cases

### Medium Priority
- Code duplication
- Suboptimal structure
- Missing setup/teardown
- Magic numbers/strings

### Low Priority
- Minor naming improvements
- Documentation
- Test organization

## Output Format

The review produces a structured report with:
- Overall quality score
- Issue counts by severity
- Specific issues with locations
- Prioritized recommendations
- Code examples for fixes

## Important Notes

- Use the test-reviewer agent for complex reviews
- Check for framework-specific configurations
- Consider the test pyramid balance
- Look at both unit and integration tests
- Verify tests actually test what they claim
