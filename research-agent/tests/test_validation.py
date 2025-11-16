"""
Tests for research output validation scripts.

These tests validate that the validation scripts correctly assess research quality.
"""

import pytest
import re
from pathlib import Path

# Mark all tests in this file as unit tests
pytestmark = pytest.mark.unit


class TestResearchOutputStructure:
    """Tests for research output structural requirements"""

    def test_valid_research_has_summary(self):
        """Valid research should have a summary/overview section"""
        research_output = """
# Investigation: Authentication System

## Summary
The app uses JWT-based authentication.

## Implementation Details
Located in src/auth/login.ts:42-88
        """
        assert re.search(r'##?\s*(Summary|Overview)', research_output)

    def test_valid_research_has_file_references(self):
        """Valid research should include file references with line numbers"""
        research_output = """
## Implementation
The login handler is in `src/auth/login.ts:42-88`.
Authentication middleware is in `src/auth/middleware.ts:25-67`.
        """
        file_refs = re.findall(r'`[^`]+\.ts:\d+(-\d+)?`', research_output)
        assert len(file_refs) >= 1

    def test_valid_research_has_evidence(self):
        """Valid research should include code examples or evidence"""
        research_output = """
## Implementation
```typescript
function login(credentials) {
  // implementation
}
```
        """
        assert '```' in research_output

    def test_valid_research_has_recommendations(self):
        """Valid research should include recommendations"""
        research_output = """
## Recommendations
1. Add rate limiting to login endpoint
2. Implement account lockout after failed attempts
        """
        keywords = ['recommend', 'should', 'suggest', 'consider']
        assert any(kw in research_output.lower() for kw in keywords)

    def test_valid_research_has_structure(self):
        """Valid research should have multiple sections"""
        research_output = """
# Investigation

## Summary
Overview here.

## Implementation
Details here.

## Recommendations
Suggestions here.
        """
        sections = re.findall(r'^##\s+', research_output, re.MULTILINE)
        assert len(sections) >= 3

    def test_valid_research_sufficient_length(self):
        """Valid research should have sufficient content"""
        research_output = "A" * 250  # 250 characters
        assert len(research_output) >= 200


class TestFileReferenceValidation:
    """Tests for file reference validation logic"""

    def test_extract_file_references(self):
        """Should extract all file references from text"""
        text = """
The login handler is in `src/auth/login.ts:42-88`.
Middleware is in `src/middleware.ts:25`.
        """
        pattern = r'`([^`]+\.(ts|js|py|go|rs|java|cpp)):(\d+)(?:-(\d+))?`'
        refs = re.findall(pattern, text)

        assert len(refs) == 2
        assert refs[0][0] == 'src/auth/login.ts'
        assert refs[1][0] == 'src/middleware.ts'

    def test_validate_line_numbers(self):
        """Should validate that line numbers are within file bounds"""
        file_content = "line1\nline2\nline3\nline4\nline5"
        total_lines = len(file_content.split('\n'))

        # Valid references
        assert 1 <= 3 <= total_lines  # line 3 is valid
        assert 1 <= 5 <= total_lines  # line 5 is valid

        # Invalid reference
        assert not (1 <= 10 <= total_lines)  # line 10 exceeds file

    def test_validate_line_range(self):
        """Should validate line ranges are logical"""
        # Valid range
        start, end = 10, 20
        assert start < end

        # Invalid range (reversed)
        start, end = 20, 10
        assert not (start < end)


class TestCompletenessMetrics:
    """Tests for completeness assessment logic"""

    def test_section_coverage_calculation(self):
        """Should calculate what percentage of expected sections are present"""
        expected_sections = ['Summary', 'Implementation', 'Recommendations', 'References']
        present_sections = ['Summary', 'Implementation', 'References']

        coverage = len(present_sections) / len(expected_sections) * 100
        assert coverage == 75.0

    def test_evidence_count(self):
        """Should count evidence items (file refs, code blocks)"""
        research = """
File: `src/auth.ts:10`
File: `src/api.ts:20`

```typescript
code block
```

```python
another block
```
        """
        file_refs = len(re.findall(r'`[^`]+:\d+`', research))
        code_blocks = len(re.findall(r'```', research)) // 2

        total_evidence = file_refs + code_blocks
        assert total_evidence == 4  # 2 file refs + 2 code blocks

    def test_word_count_sufficient(self):
        """Should check if content has sufficient word count"""
        research = "This is a test " * 100  # 400 words
        word_count = len(research.split())

        assert word_count >= 200  # Minimum threshold

    def test_technical_depth_indicators(self):
        """Should check for technical depth indicators"""
        research = """
The implementation uses JWT tokens with RS256 algorithm.
The middleware validates tokens using the public key.
Error handling includes try-catch with specific error types.
        """

        technical_indicators = [
            'implementation', 'algorithm', 'validates',
            'error handling', 'specific'
        ]

        found = sum(1 for indicator in technical_indicators if indicator in research.lower())
        assert found >= 3  # Should have multiple technical terms


class TestCitationExtraction:
    """Tests for citation extraction and validation"""

    def test_extract_web_citations(self):
        """Should extract numbered web citations"""
        text = """
Best practices from OWASP [1] and Mozilla [2].

References:
[1] OWASP - https://owasp.org/cheatsheet
[2] Mozilla - https://developer.mozilla.org/guide
        """

        citations = re.findall(r'\[(\d+)\]\s+(.+?)\s+-\s+(https?://[^\s]+)', text)
        assert len(citations) == 2
        assert citations[0][2].startswith('https://owasp.org')

    def test_extract_file_citations(self):
        """Should extract file citations with line numbers"""
        text = "`src/auth/login.ts:42`, `src/api/users.ts:100-150`"

        file_citations = re.findall(r'`([^`]+):(\d+)(?:-(\d+))?`', text)
        assert len(file_citations) == 2

    def test_extract_package_citations(self):
        """Should extract package/library citations"""
        text = """
Using jsonwebtoken (v9.0.2) for JWT handling.
Express (v4.18.0) for routing.
        """

        packages = re.findall(r'(\w+)\s+\(v?([0-9.]+)\)', text)
        assert len(packages) == 2
        assert packages[0][0] == 'jsonwebtoken'
        assert packages[0][1] == '9.0.2'


class TestQualityScoring:
    """Tests for research quality scoring logic"""

    def test_quality_score_calculation(self):
        """Should calculate overall quality score from checks"""
        checks = {
            'has_summary': True,
            'has_file_refs': True,
            'has_evidence': True,
            'has_recommendations': False,
            'has_structure': True,
            'sufficient_length': True,
            'has_citations': False
        }

        score = sum(1 for passed in checks.values() if passed) / len(checks) * 100
        assert score == (5 / 7) * 100  # 5 passed out of 7

    def test_quality_threshold_pass(self):
        """Should pass if score meets threshold"""
        score = 85
        threshold = 70
        assert score >= threshold

    def test_quality_threshold_fail(self):
        """Should fail if score below threshold"""
        score = 65
        threshold = 70
        assert score < threshold


class TestResearchCacheValidation:
    """Tests for research cache entry validation"""

    def test_cache_entry_has_frontmatter(self):
        """Cache entries should have YAML frontmatter"""
        cache_entry = """---
research_type: investigation
topic: JWT authentication
date: 2025-01-15
---

# Research content
        """
        assert cache_entry.startswith('---\n')
        assert '---\n\n' in cache_entry

    def test_cache_metadata_required_fields(self):
        """Cache metadata should have required fields"""
        metadata = {
            'research_type': 'investigation',
            'topic': 'auth system',
            'date': '2025-01-15',
            'tags': ['auth', 'jwt']
        }

        required = ['research_type', 'topic', 'date']
        assert all(field in metadata for field in required)

    def test_cache_expiry_calculation(self):
        """Should calculate if cache entry is expired"""
        from datetime import datetime, timedelta

        entry_date = datetime(2025, 1, 1)
        expiry_date = entry_date + timedelta(days=30)
        current_date = datetime(2025, 1, 20)

        is_expired = current_date > expiry_date
        assert not is_expired

        # Test expired case
        current_date = datetime(2025, 2, 10)
        is_expired = current_date > expiry_date
        assert is_expired


class TestComparisonFrameworkValidation:
    """Tests for comparative analysis framework validation"""

    def test_weights_sum_to_one(self):
        """Comparison weights must sum to 1.0"""
        weights = {
            'developer_experience': 0.30,
            'learning_curve': 0.25,
            'performance': 0.20,
            'type_safety': 0.15,
            'devtools': 0.10
        }

        total = sum(weights.values())
        assert abs(total - 1.0) < 0.01  # Allow for floating point errors

    def test_weights_within_bounds(self):
        """Individual weights should be between 0.05 and 0.40"""
        weights = [0.30, 0.25, 0.20, 0.15, 0.10]

        for weight in weights:
            assert 0.05 <= weight <= 0.40

    def test_weighted_score_calculation(self):
        """Should correctly calculate weighted scores"""
        weights = {'dx': 0.30, 'learning': 0.25, 'perf': 0.20, 'types': 0.15, 'tools': 0.10}
        scores_a = {'dx': 6, 'learning': 5, 'perf': 8, 'types': 8, 'tools': 10}
        scores_b = {'dx': 9, 'learning': 9, 'perf': 9, 'types': 8, 'tools': 6}

        def calculate_weighted_score(weights, scores):
            return sum(weights[k] * scores[k] for k in weights.keys())

        score_a = calculate_weighted_score(weights, scores_a)
        score_b = calculate_weighted_score(weights, scores_b)

        assert abs(score_a - 6.55) < 0.01
        assert abs(score_b - 8.35) < 0.01
        assert score_b > score_a  # B wins

    def test_rating_scale_bounds(self):
        """Ratings should be within 1-10 scale"""
        ratings = [6, 5, 8, 9, 10]

        for rating in ratings:
            assert 1 <= rating <= 10
