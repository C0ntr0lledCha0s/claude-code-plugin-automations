---
description: Analyze source code and suggest specific tests that should be written, including test cases and code examples
allowed-tools: Read, Grep, Glob, Bash
argument-hint: "[file-path]"
---

# Suggest Tests

Analyze source code and generate specific test suggestions with test cases and code examples.

## Arguments

- **`$1`**: (Required) Path to the source file to analyze
- **`$ARGUMENTS`**: File path or module to analyze

## Workflow

When this command is invoked with `/testing-expert:suggest-tests <file>`:

1. **Read Source Code**
   - Parse the file
   - Identify exports (functions, classes)
   - Analyze complexity

2. **Identify Testable Units**
   - Exported functions
   - Class methods
   - Event handlers
   - Callbacks

3. **Analyze Each Unit**
   - Input parameters
   - Return values
   - Side effects
   - Error conditions
   - Edge cases
   - Dependencies

   **Code analysis patterns**:
   ```bash
   # Find exported functions
   grep -E "^export (async )?(function|const|class)" $1

   # Find error handling that needs testing
   grep -E "throw new|catch \(|\.catch\(" $1

   # Find conditionals (branches to test)
   grep -E "if \(|switch \(|\? .* :" $1 | wc -l

   # Find async operations
   grep -E "async |await |Promise|\.then\(" $1

   # Find external dependencies to mock
   grep -E "^import .* from ['\"](?!\.)" $1
   ```

   **Complexity indicators**:
   - Function parameters (more = more test cases)
   - Conditional statements (branches)
   - Try-catch blocks (error scenarios)
   - Loops (boundary conditions)

4. **Generate Test Cases**
   For each testable unit:
   - Happy path scenarios
   - Error scenarios
   - Boundary conditions
   - Edge cases

5. **Provide Code Examples**
   - Complete test code
   - Appropriate mocking
   - Clear assertions

## Output Format

```markdown
## Suggested Tests for [filename]

### Function: `functionName`

#### Test Cases

1. **Happy path: returns expected result**
   ```javascript
   it('should return processed value for valid input', () => {
     const result = functionName({ valid: 'input' });
     expect(result).toEqual({ processed: 'output' });
   });
   ```

2. **Error case: throws on invalid input**
   ```javascript
   it('should throw ValidationError for invalid input', () => {
     expect(() => functionName(null)).toThrow(ValidationError);
   });
   ```

3. **Edge case: handles empty array**
   ```javascript
   it('should return empty result for empty array', () => {
     const result = functionName([]);
     expect(result).toEqual([]);
   });
   ```

### Mocking Requirements
- `dependency1` - mock for [reason]
- `fetch` - mock API calls

### Test File Template
[Complete test file ready to use]
```

## Examples

### Suggest Tests for Utility Function
```
/testing-expert:suggest-tests src/utils/parser.ts
```

Analyzes parser and suggests test cases for all exported functions.

### Suggest Tests for React Component
```
/testing-expert:suggest-tests src/components/UserForm.tsx
```

Suggests tests for rendering, user interactions, and state changes.

### Suggest Tests for API Handler
```
/testing-expert:suggest-tests src/api/users.ts
```

Suggests tests for success, errors, validation, and edge cases.

## Test Case Categories

### Functional Tests
- Expected behavior with valid input
- Return value verification
- State changes
- Side effects

### Error Handling
- Invalid input types
- Missing required fields
- Null/undefined handling
- Network failures
- Timeout scenarios

### Boundary Conditions
- Empty inputs ([], '', {})
- Maximum values
- Minimum values
- Unicode/special characters

### Edge Cases
- Concurrent calls
- Race conditions
- Large datasets
- Nested structures

## Analysis Patterns

### For Functions
- Input validation
- Return type
- Thrown errors
- Async behavior
- Pure vs impure

### For Classes
- Constructor
- Public methods
- State management
- Event handling
- Lifecycle

### For React Components
- Rendering
- Props handling
- User interactions
- State updates
- Effects

## Important Notes

- Requires file path as argument
- Generates framework-appropriate tests
- Includes mocking recommendations
- Provides complete, runnable code
- Considers existing test patterns in codebase

## Error Handling

If file not found:
- Check file path spelling
- Verify file exists
- Show similar files in directory

If file is not testable:
- Explain why (e.g., only types, constants)
- Suggest related testable files
