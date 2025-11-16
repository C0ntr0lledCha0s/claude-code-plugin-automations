"""
Tests for pattern detection in sample codebase.

These tests verify that the sample codebase contains expected patterns
that the research-agent should be able to detect.
"""

import pytest
import re
from pathlib import Path

pytestmark = pytest.mark.unit


class TestSampleCodebasePatterns:
    """Verify sample codebase contains expected patterns"""

    def test_factory_pattern_present(self, sample_files):
        """Sample codebase should contain Factory pattern"""
        factory_file = sample_files['factory']
        content = factory_file.read_text()

        # Should have factory class
        assert 'class UserFactory' in content

        # Should have factory method
        assert 'createUser' in content

        # Should have switch/conditional logic
        assert 'switch' in content or 'if' in content

        # Should create different types
        assert 'AdminUser' in content
        assert 'RegularUser' in content

    def test_singleton_pattern_present(self, sample_files):
        """Sample codebase should contain Singleton pattern"""
        singleton_file = sample_files['singleton']
        content = singleton_file.read_text()

        # Should have static instance
        assert 'private static instance' in content

        # Should have getInstance method
        assert 'getInstance' in content

        # Should have private constructor
        assert 'private constructor' in content

    def test_repository_pattern_present(self, sample_files):
        """Sample codebase should contain Repository pattern"""
        repo_file = sample_files['repository']
        content = repo_file.read_text()

        # Should have repository class
        assert 'class UserRepository' in content

        # Should have CRUD methods
        assert 'findById' in content
        assert 'findByEmail' in content
        assert 'create' in content
        assert 'update' in content
        assert 'delete' in content

    def test_authentication_flow_present(self, sample_files):
        """Sample codebase should contain authentication flow"""
        login_file = sample_files['login_handler']
        content = login_file.read_text()

        # Should document flow steps
        assert 'Flow:' in content or 'Step' in content

        # Should have key authentication steps
        auth_steps = [
            'validate', 'credentials', 'password',
            'token', 'cookie'
        ]

        found_steps = sum(1 for step in auth_steps if step.lower() in content.lower())
        assert found_steps >= 4  # Should mention most steps

    def test_middleware_pattern_present(self, sample_files):
        """Sample codebase should contain middleware pattern"""
        middleware_file = sample_files['middleware']
        content = middleware_file.read_text()

        # Should have middleware function/class
        assert 'Middleware' in content

        # Should use next() pattern
        assert 'next' in content or 'NextFunction' in content

        # Should handle request/response
        assert 'Request' in content
        assert 'Response' in content

    def test_rest_api_pattern_present(self, sample_files):
        """Sample codebase should contain REST API patterns"""
        api_file = sample_files['api_routes']
        content = api_file.read_text()

        # Should have router
        assert 'Router' in content

        # Should have HTTP methods
        http_methods = ['get', 'post', 'put', 'delete']
        found_methods = sum(1 for method in http_methods if f'.{method}(' in content.lower())
        assert found_methods >= 3  # Should have most CRUD operations


class TestPatternDocumentation:
    """Verify patterns are well-documented in sample codebase"""

    def test_factory_pattern_documented(self, sample_files):
        """Factory pattern should have documentation comments"""
        content = sample_files['factory'].read_text()

        # Should mention "Factory" in comments
        assert '* Factory' in content or '// Factory' in content

        # Should explain purpose
        assert 'Creational' in content or 'design pattern' in content.lower()

    def test_singleton_pattern_documented(self, sample_files):
        """Singleton pattern should have documentation comments"""
        content = sample_files['singleton'].read_text()

        # Should mention "Singleton" in comments
        assert '* Singleton' in content or '// Singleton' in content

        # Should explain pattern
        assert 'single instance' in content.lower() or 'one instance' in content.lower()

    def test_repository_pattern_documented(self, sample_files):
        """Repository pattern should have documentation comments"""
        content = sample_files['repository'].read_text()

        # Should mention "Repository" in comments
        assert '* Repository' in content or '// Repository' in content

        # Should explain purpose
        assert 'database' in content.lower() or 'data access' in content.lower()

    def test_flow_steps_documented(self, sample_files):
        """Authentication flow should be documented step-by-step"""
        content = sample_files['login_handler'].read_text()

        # Should have numbered steps or flow documentation
        has_numbered_steps = bool(re.search(r'(Step \d+|Flow:|^\s*\d+\.)', content, re.MULTILINE))
        assert has_numbered_steps


class TestCodebaseStructure:
    """Verify sample codebase has expected structure"""

    def test_directory_structure_exists(self, sample_codebase_path):
        """Sample codebase should have organized directory structure"""
        base_path = Path(sample_codebase_path)

        expected_dirs = [
            'src',
            'src/auth',
            'src/api',
            'src/services',
            'src/factories'
        ]

        for dir_path in expected_dirs:
            assert (base_path / dir_path).exists(), f"Missing directory: {dir_path}"

    def test_package_json_exists(self, sample_codebase_path):
        """Sample codebase should have package.json"""
        package_json = Path(sample_codebase_path) / 'package.json'
        assert package_json.exists()

        # Should have valid JSON structure
        import json
        content = json.loads(package_json.read_text())
        assert 'name' in content
        assert 'dependencies' in content

    def test_readme_exists(self, sample_codebase_path):
        """Sample codebase should have README documenting patterns"""
        readme = Path(sample_codebase_path) / 'README.md'
        assert readme.exists()

        content = readme.read_text()

        # Should document patterns
        assert 'Factory Pattern' in content
        assert 'Singleton Pattern' in content
        assert 'Repository Pattern' in content

    def test_all_expected_files_exist(self, sample_files):
        """All expected sample files should exist"""
        for file_key, file_path in sample_files.items():
            assert file_path.exists(), f"Missing sample file: {file_key} ({file_path})"


class TestSecurityPatterns:
    """Verify sample codebase demonstrates security best practices"""

    def test_password_hashing_present(self, sample_files):
        """Should demonstrate password hashing"""
        auth_service = sample_files['singleton'].read_text()

        # Should use bcrypt
        assert 'bcrypt' in auth_service

        # Should have hash and compare methods
        assert 'hashPassword' in auth_service
        assert 'comparePassword' in auth_service

    def test_jwt_token_present(self, sample_files):
        """Should demonstrate JWT token usage"""
        auth_service = sample_files['singleton'].read_text()

        # Should use jwt library
        assert 'jwt' in auth_service.lower()

        # Should have token generation
        assert 'generateToken' in auth_service or 'sign' in auth_service

        # Should have token verification
        assert 'verifyToken' in auth_service or 'verify' in auth_service

    def test_httponly_cookie_present(self, sample_files):
        """Should demonstrate HTTP-only cookie for security"""
        login_handler = sample_files['login_handler'].read_text()

        # Should set httpOnly flag
        assert 'httpOnly' in login_handler

        # Should mention cookie security
        assert 'cookie' in login_handler.lower()

    def test_input_validation_present(self, sample_files):
        """Should demonstrate input validation"""
        login_handler = sample_files['login_handler'].read_text()

        # Should validate inputs
        validation_keywords = ['validate', 'validation', 'if (!', 'required']
        found = sum(1 for kw in validation_keywords if kw in login_handler)
        assert found >= 2  # Should have validation logic

    def test_error_handling_present(self, sample_files):
        """Should demonstrate error handling"""
        login_handler = sample_files['login_handler'].read_text()

        # Should have try-catch
        assert 'try' in login_handler
        assert 'catch' in login_handler

        # Should handle errors gracefully
        assert 'error' in login_handler.lower()


class TestDependencyPatterns:
    """Verify sample codebase shows component dependencies"""

    def test_service_dependencies(self, sample_files):
        """Login handler should depend on services"""
        login_handler = sample_files['login_handler'].read_text()

        # Should import/use auth service
        assert 'authService' in login_handler or 'AuthService' in login_handler

        # Should import/use repository
        assert 'UserRepository' in login_handler

    def test_middleware_dependencies(self, sample_files):
        """Middleware should depend on auth service"""
        middleware = sample_files['middleware'].read_text()

        # Should use auth service
        assert 'authService' in middleware or 'AuthService' in middleware

        # Should use repository for user lookup
        assert 'UserRepository' in middleware or 'userRepo' in middleware

    def test_api_route_dependencies(self, sample_files):
        """API routes should use middleware and repository"""
        api_routes = sample_files['api_routes'].read_text()

        # Should use authentication middleware
        assert 'authMiddleware' in api_routes or 'authenticate' in api_routes

        # Should use repository
        assert 'UserRepository' in api_routes or 'userRepo' in api_routes


class TestPatternVariations:
    """Test that patterns show realistic variations"""

    def test_factory_handles_unknown_types(self, sample_files):
        """Factory should handle unknown types gracefully"""
        content = sample_files['factory'].read_text()

        # Should have error handling for unknown types
        assert 'throw' in content or 'Error' in content

    def test_singleton_thread_safety_consideration(self, sample_files):
        """Singleton should show consideration for initialization"""
        content = sample_files['singleton'].read_text()

        # Should check if instance exists
        assert 'if (!this.instance)' in content or 'if (!AuthService.instance)' in content

    def test_repository_abstracts_storage(self, sample_files):
        """Repository should abstract storage mechanism"""
        content = sample_files['repository'].read_text()

        # Should not expose storage details in interface
        # Methods should be generic: findById, create, etc.
        assert 'findById' in content
        assert 'create' in content

        # Storage can be anything (Map, database, etc.)
        # The interface should be consistent
