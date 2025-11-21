# Testing Expert Plugin

Expert plugin for quality code reviews focused on testing. Provides specialized expertise for Jest, Playwright, and general test quality analysis with automated review and improvement suggestions.

## Installation

### From Plugin Directory

```bash
# Navigate to your Claude Code plugins directory
cd ~/.claude/plugins/

# Clone or symlink this plugin
ln -s /path/to/testing-expert testing-expert
```

### Verify Installation

Restart Claude Code and check that the plugin is loaded:
- Skills should auto-invoke when working with tests
- Commands should be available via `/testing-expert:*`

## Components

### Agent: test-reviewer

Expert code reviewer specializing in test quality, coverage analysis, and testing best practices.

**When to use**: 
- Reviewing test code for quality
- Analyzing entire test suites
- Identifying testing gaps
- Getting improvement recommendations

**Invocation**: Spawned via Task tool for comprehensive test reviews

### Skills

#### jest-testing

**Auto-invokes when**:
- Working with Jest tests (`.test.js`, `.test.ts`)
- Discussing Jest configuration
- Asking about Jest matchers or mocks

**Provides**:
- Jest configuration expertise
- Matcher and assertion patterns
- Mocking strategies
- React Testing Library integration

#### playwright-testing

**Auto-invokes when**:
- Working with Playwright tests (`.spec.ts` in e2e directories)
- Discussing browser automation
- Asking about selectors or page objects

**Provides**:
- Playwright configuration expertise
- Locator best practices
- Page Object Model patterns
- Debugging and tracing guidance

#### analyzing-test-quality

**Auto-invokes when**:
- Asking about test quality metrics
- Discussing code coverage
- Reviewing test reliability
- Analyzing test maintainability

**Provides**:
- Framework-agnostic quality analysis
- Anti-pattern detection
- Coverage metrics interpretation
- Best practice recommendations

### Commands

#### `/testing-expert:review-tests [path]`

Review test quality for a file, directory, or entire test suite.

```bash
# Review all tests
/testing-expert:review-tests

# Review specific directory
/testing-expert:review-tests src/components

# Review single file
/testing-expert:review-tests src/utils/parser.test.ts
```

**Output**: Quality score, issues found, prioritized recommendations with code examples

#### `/testing-expert:analyze-coverage [report-path]`

Analyze test coverage reports and identify gaps.

```bash
# Analyze default coverage location
/testing-expert:analyze-coverage

# Analyze specific report
/testing-expert:analyze-coverage coverage/lcov.info
```

**Output**: Coverage metrics, critical gaps, specific test suggestions for uncovered code

#### `/testing-expert:suggest-tests <file-path>`

Generate test suggestions for source code.

```bash
# Suggest tests for a utility
/testing-expert:suggest-tests src/utils/parser.ts

# Suggest tests for a component
/testing-expert:suggest-tests src/components/UserForm.tsx
```

**Output**: Complete test cases with code examples, mocking recommendations, ready-to-use test file

## Usage Examples

### Comprehensive Test Review

```
Review all tests in my project and give me a quality report
```

Claude will:
1. Discover all test files
2. Analyze test quality patterns
3. Identify issues and anti-patterns
4. Provide prioritized recommendations

### Improve Test Coverage

```
I just added coverage reporting. Can you analyze the coverage and suggest what tests I should write?
```

Claude will:
1. Parse coverage reports
2. Identify critical gaps
3. Generate specific test cases
4. Provide runnable code examples

### Test a New Feature

```
I just wrote src/services/authentication.ts. What tests should I write for it?
```

Claude will:
1. Analyze the source code
2. Identify all testable units
3. Generate comprehensive test cases
4. Include mocking strategies

## Supported Frameworks

### Unit Testing
- **Jest** - Full support with configuration, matchers, mocks
- **Vitest** - Compatible patterns (Jest-like API)
- **Mocha/Chai** - Basic support

### E2E Testing
- **Playwright** - Full support with locators, page objects, fixtures
- **Cypress** - Basic support

### Coverage Tools
- **Istanbul/nyc**
- **c8**
- **Jest coverage**

## Best Practices

### Test Structure
- Use AAA (Arrange-Act-Assert) pattern
- One logical assertion per test
- Descriptive test names
- Proper setup/teardown

### Test Quality
- Test behavior, not implementation
- Mock at boundaries (APIs, databases)
- Keep tests fast and reliable
- Maintain test isolation

### Coverage
- Aim for 80%+ meaningful coverage
- Focus on critical paths first
- Don't test just for coverage metrics
- Consider mutation testing

## Configuration

### Customizing Analysis

The plugin respects your project's testing configuration:
- `jest.config.js/ts` - Jest settings
- `playwright.config.ts` - Playwright settings
- `package.json` - Test scripts and dependencies

### Coverage Thresholds

Default recommended thresholds:
```javascript
{
  statements: 80,
  branches: 75,
  functions: 80,
  lines: 80
}
```

## Contributing

Contributions are welcome! Please:
1. Follow the existing component patterns
2. Include tests for new functionality
3. Update documentation
4. Run validation before submitting

## License

MIT
