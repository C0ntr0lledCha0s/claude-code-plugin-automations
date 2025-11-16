"""
Pytest configuration and shared fixtures for research-agent tests.
"""

import pytest
import os
from pathlib import Path

# Test fixture paths
FIXTURES_DIR = Path(__file__).parent / 'fixtures'
SAMPLE_CODEBASE_DIR = FIXTURES_DIR / 'sample-codebase'

@pytest.fixture
def sample_codebase_path():
    """Path to sample codebase fixture"""
    return str(SAMPLE_CODEBASE_DIR)

@pytest.fixture
def sample_files():
    """Dictionary of key sample files for testing"""
    return {
        'factory': SAMPLE_CODEBASE_DIR / 'src' / 'factories' / 'userFactory.ts',
        'singleton': SAMPLE_CODEBASE_DIR / 'src' / 'services' / 'authService.ts',
        'repository': SAMPLE_CODEBASE_DIR / 'src' / 'auth' / 'userRepository.ts',
        'login_handler': SAMPLE_CODEBASE_DIR / 'src' / 'auth' / 'loginHandler.ts',
        'middleware': SAMPLE_CODEBASE_DIR / 'src' / 'auth' / 'authMiddleware.ts',
        'api_routes': SAMPLE_CODEBASE_DIR / 'src' / 'api' / 'userRoutes.ts',
    }

@pytest.fixture
def expected_patterns():
    """Expected patterns to find in sample codebase"""
    return {
        'factory': {
            'type': 'creational',
            'name': 'Factory Pattern',
            'file': 'src/factories/userFactory.ts',
            'keywords': ['factory', 'createUser', 'switch', 'role']
        },
        'singleton': {
            'type': 'creational',
            'name': 'Singleton Pattern',
            'file': 'src/services/authService.ts',
            'keywords': ['singleton', 'getInstance', 'private static instance']
        },
        'repository': {
            'type': 'structural',
            'name': 'Repository Pattern',
            'file': 'src/auth/userRepository.ts',
            'keywords': ['repository', 'findById', 'findByEmail', 'create', 'update', 'delete']
        }
    }

@pytest.fixture
def expected_auth_flow():
    """Expected authentication flow steps"""
    return [
        'Validate credentials',
        'Find user in database',
        'Verify password',
        'Generate JWT token',
        'Set HTTP-only cookie',
        'Return user data'
    ]

def pytest_configure(config):
    """Pytest configuration hook"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test requiring real investigation"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test for validation logic"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
