# Research Agent Tests

Comprehensive test suite for the research-agent plugin, validating research quality, pattern detection, and plugin functionality.

## Overview

This test suite includes:
1. **Unit Tests** - Validation logic, scoring algorithms, pattern detection
2. **Integration Tests** - Full research workflows (requires Claude Code integration - planned)
3. **Fixtures** - Sample codebase with known patterns for testing

## Test Categories

### 1. Validation Tests (`test_validation.py`)
Tests for research output quality validation:
- Research structure validation (summary, file references, evidence)
- File reference extraction and validation
- Completeness metrics calculation
- Citation extraction and analysis
- Quality scoring algorithms
- Cache entry validation
- Comparison framework validation (weights, scores, calculations)

**Run**: `pytest tests/test_validation.py -v`

### 2. Pattern Detection Tests (`test_pattern_detection.py`)
Tests verifying sample codebase contains expected patterns:
- Design pattern presence (Factory, Singleton, Repository)
- Authentication flow documentation
- Middleware patterns
- REST API patterns
- Security best practices
- Component dependencies

**Run**: `pytest tests/test_pattern_detection.py -v`

## Test Fixtures

### Sample Codebase (`fixtures/sample-codebase/`)
A realistic Node.js/TypeScript codebase with intentional design patterns:

**Patterns Included**:
- **Factory Pattern**: `src/factories/userFactory.ts` - Creates users based on role
- **Singleton Pattern**: `src/services/authService.ts` - Single auth service instance
- **Repository Pattern**: `src/auth/userRepository.ts` - Abstracts user data access

**Architecture Features**:
- JWT authentication flow with middleware
- RESTful API with route protection
- Password hashing with bcrypt
- HTTP-only cookies for security
- Role-based access control
- Error handling and validation

**Purpose**: Research-agent tests validate that investigations can correctly identify these patterns and trace execution flows.

## Running Tests

### Prerequisites

```bash
# Install pytest
pip install pytest

# Or install all dev dependencies
pip install -r requirements-dev.txt  # If created
```

### Run All Tests

```bash
# From research-agent directory
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=scripts --cov-report=html

# Specific test markers
pytest tests/ -v -m unit        # Only unit tests
pytest tests/ -v -m integration # Only integration tests (when implemented)
pytest tests/ -v -m "not slow"  # Skip slow tests
```

### Run Specific Test Files

```bash
# Validation tests only
pytest tests/test_validation.py -v

# Pattern detection tests only
pytest tests/test_pattern_detection.py -v

# Specific test class
pytest tests/test_validation.py::TestResearchOutputStructure -v

# Specific test
pytest tests/test_validation.py::TestResearchOutputStructure::test_valid_research_has_summary -v
```

### Test Output Options

```bash
# Verbose output with test names
pytest tests/ -v

# Show print statements
pytest tests/ -v -s

# Stop on first failure
pytest tests/ -v -x

# Show slowest tests
pytest tests/ --durations=10
```

## Test Markers

Tests are marked for categorization:

- `@pytest.mark.unit` - Unit tests for validation logic (fast)
- `@pytest.mark.integration` - Integration tests requiring real investigation (slow, planned)
- `@pytest.mark.slow` - Slow-running tests

Filter by marker:
```bash
pytest tests/ -v -m unit
pytest tests/ -v -m "not integration"
```

## Current Test Status

### ✅ Implemented
- [x] Validation logic tests
- [x] Pattern detection tests
- [x] Sample codebase fixtures
- [x] Test configuration (conftest.py)
- [x] Test documentation

### ⏳ Planned
- [ ] Integration tests invoking actual research commands
- [ ] Best practices research tests
- [ ] Comparative analysis end-to-end tests
- [ ] Cache management tests
- [ ] Performance benchmarks

**Note**: Integration tests requiring actual Claude Code investigation are planned but not yet implemented, as they require integration with Claude Code's plugin testing framework (which doesn't currently exist).

## Integration Tests (Planned)

When Claude Code supports plugin integration testing, we'll add:

```python
# Planned: test_investigating.py
@pytest.mark.integration
def test_investigation_identifies_factory_pattern(sample_codebase_path):
    """Research-agent should identify Factory pattern in sample codebase"""
    result = run_command(f"/investigate factory pattern in {sample_codebase_path}")

    assert 'Factory Pattern' in result or 'Factory' in result
    assert 'UserFactory' in result
    assert 'src/factories/userFactory.ts' in result

# Planned: test_best_practices.py
@pytest.mark.integration
def test_best_practices_returns_current_standards():
    """Best practice research should return current (2025) standards"""
    result = run_command("/best-practice JWT authentication")

    assert '2025' in result or '2024' in result
    assert 'HTTP-only' in result or 'HttpOnly' in result
    assert 'bcrypt' in result or 'hashing' in result.lower()

# Planned: test_commands.py
@pytest.mark.integration
def test_compare_command_provides_recommendation():
    """Compare command should provide clear recommendation"""
    result = run_command("/compare Redux vs Zustand for React")

    assert 'recommend' in result.lower() or 'choose' in result.lower()
    assert 'Redux' in result and 'Zustand' in result
```

## CI/CD Integration

Tests automatically run on:
- Every push to `main`
- All pull requests
- Manual workflow dispatch

See `.github/workflows/test-research-agent.yml` for CI configuration.

**CI Command**:
```bash
# Same command used in CI
pytest tests/ -v --tb=short
```

## Writing New Tests

### Guidelines

1. **Use fixtures** from `conftest.py` for consistent test data
2. **Mark tests appropriately** with `@pytest.mark.unit` or `@pytest.mark.integration`
3. **Write descriptive test names** that explain what's being tested
4. **Include docstrings** explaining the test purpose
5. **Test one thing** per test function
6. **Use assertions** with helpful messages

### Example Test

```python
import pytest

@pytest.mark.unit
def test_validation_identifies_missing_summary():
    """Validation should detect when research lacks a summary section"""
    research_without_summary = """
    ## Implementation
    Details here.
    """

    import re
    has_summary = bool(re.search(r'##?\s*(Summary|Overview)', research_without_summary))

    assert not has_summary, "Should not find summary in this research"
```

## Test Coverage

Current test coverage:

- **Validation Scripts**: ~80% (validation logic, scoring algorithms)
- **Sample Codebase**: 100% (all expected patterns present)
- **Integration Workflows**: 0% (planned)

**Generate Coverage Report**:
```bash
pytest tests/ --cov=scripts --cov-report=html
open htmlcov/index.html  # View in browser
```

## Troubleshooting

### Tests fail due to missing pytest

**Solution**:
```bash
pip install pytest
```

### Tests fail due to missing fixtures

**Solution**: Ensure you're running from the `research-agent/` directory:
```bash
cd research-agent/
pytest tests/ -v
```

### Import errors for validation scripts

**Solution**: Add parent directory to Python path:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest tests/ -v
```

### Tests pass locally but fail in CI

**Solution**: Check Python version compatibility. CI uses Python 3.10+.

## Contributing Tests

When adding new features to research-agent:

1. **Add unit tests** for new validation logic
2. **Update fixtures** if new patterns are needed
3. **Document** expected behavior in test docstrings
4. **Run full suite** before committing: `pytest tests/ -v`
5. **Check coverage** to ensure good test coverage

## Resources

- **pytest documentation**: https://docs.pytest.org/
- **Python testing best practices**: https://docs.python-guide.org/writing/tests/
- **Sample codebase README**: `fixtures/sample-codebase/README.md`

---

**Last Updated**: 2025-01-15
**Test Framework**: pytest 7.0+
**Python Version**: 3.8+
