"""
Shared fixtures for agent invocation and component tests.

Provides common utilities for:
- Finding agent/skill/command files
- Parsing YAML frontmatter
- Extracting tool permissions
"""
import pytest
from pathlib import Path
import yaml
import re
from typing import Dict, List, Optional


@pytest.fixture
def repo_root() -> Path:
    """Return repository root path."""
    return Path(__file__).parent.parent


@pytest.fixture
def all_agent_files(repo_root: Path) -> List[Path]:
    """Find all agent definition files across all plugins."""
    return sorted(repo_root.glob('*/agents/*.md'))


@pytest.fixture
def all_skill_files(repo_root: Path) -> List[Path]:
    """Find all skill definition files across all plugins."""
    return sorted(repo_root.glob('*/skills/*/SKILL.md'))


@pytest.fixture
def all_command_files(repo_root: Path) -> List[Path]:
    """Find all command definition files across all plugins."""
    return sorted(repo_root.glob('*/commands/*.md'))


def extract_frontmatter(file_path: Path) -> Dict:
    """
    Extract YAML frontmatter from a markdown file.

    Args:
        file_path: Path to the markdown file

    Returns:
        Dictionary containing the parsed YAML frontmatter
    """
    content = file_path.read_text(encoding='utf-8')
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            return {}
    return {}


def get_agent_tools(file_path: Path) -> List[str]:
    """
    Extract the list of tools from an agent file.

    Args:
        file_path: Path to the agent markdown file

    Returns:
        List of tool names the agent has access to
    """
    frontmatter = extract_frontmatter(file_path)
    tools = frontmatter.get('tools', '')

    if isinstance(tools, str):
        return [t.strip() for t in tools.split(',') if t.strip()]
    elif isinstance(tools, list):
        return tools
    return []


def get_agent_name(file_path: Path) -> Optional[str]:
    """
    Extract the agent name from frontmatter.

    Args:
        file_path: Path to the agent markdown file

    Returns:
        Agent name or None if not found
    """
    frontmatter = extract_frontmatter(file_path)
    return frontmatter.get('name')


@pytest.fixture
def extract_frontmatter_fixture():
    """Fixture wrapper for extract_frontmatter function."""
    return extract_frontmatter


@pytest.fixture
def get_agent_tools_fixture():
    """Fixture wrapper for get_agent_tools function."""
    return get_agent_tools


@pytest.fixture
def get_agent_name_fixture():
    """Fixture wrapper for get_agent_name function."""
    return get_agent_name
