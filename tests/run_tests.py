#!/usr/bin/env python3
"""
Standalone test runner for agent invocation tests.
Does not require pytest - uses built-in unittest.
"""
import sys
import unittest
from pathlib import Path
import yaml
import re
from typing import Dict, List, Optional

# Add the quality-scorer module to path
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / 'self-improvement' / 'skills' / 'analyzing-component-quality' / 'scripts'))

# Orchestrator agents that are permitted to have Task tool
ORCHESTRATOR_AGENTS = ['project-coordinator', 'investigator', 'workflow-orchestrator', 'meta-architect']


def extract_frontmatter(file_path: Path) -> Dict:
    """Extract YAML frontmatter from a markdown file."""
    content = file_path.read_text(encoding='utf-8')
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            return {}
    return {}


def get_agent_tools(file_path: Path) -> List[str]:
    """Extract the list of tools from an agent file."""
    frontmatter = extract_frontmatter(file_path)
    tools = frontmatter.get('tools', '')

    if isinstance(tools, str):
        return [t.strip() for t in tools.split(',') if t.strip()]
    elif isinstance(tools, list):
        return tools
    return []


def get_agent_name(file_path: Path) -> Optional[str]:
    """Extract the agent name from frontmatter."""
    frontmatter = extract_frontmatter(file_path)
    return frontmatter.get('name')


def get_all_agent_files() -> List[Path]:
    """Find all agent definition files across all plugins."""
    return sorted(REPO_ROOT.glob('*/agents/*.md'))


class TestAgentTaskToolPermissions(unittest.TestCase):
    """Test Task tool is properly restricted to orchestrator agents."""

    def setUp(self):
        self.agent_files = get_all_agent_files()

    def test_all_agents_parse_successfully(self):
        """All agent files should parse without errors."""
        for agent_file in self.agent_files:
            frontmatter = extract_frontmatter(agent_file)
            self.assertIsNotNone(frontmatter, f"Failed to parse {agent_file}")
            self.assertIn('name', frontmatter, f"Agent {agent_file} missing 'name' field")
            self.assertIn('description', frontmatter, f"Agent {agent_file} missing 'description' field")

    def test_orchestrator_agents_exist(self):
        """Verify orchestrator agents are defined in the repository."""
        agent_names = [get_agent_name(f) for f in self.agent_files]

        self.assertIn('project-coordinator', agent_names, "project-coordinator agent not found")
        self.assertIn('investigator', agent_names, "investigator agent not found")

    def test_non_orchestrator_agents_no_task_tool(self):
        """Non-orchestrator agents should NOT have Task tool."""
        violations = []

        for agent_file in self.agent_files:
            agent_name = get_agent_name(agent_file)
            tools = get_agent_tools(agent_file)

            if agent_name not in ORCHESTRATOR_AGENTS and 'Task' in tools:
                violations.append(f"{agent_name} has Task tool but is not an orchestrator")

        self.assertEqual(violations, [],
            f"Non-orchestrator agents with Task tool found:\n" +
            "\n".join(f"  - {v}" for v in violations)
        )


class TestQualityScorerOrchestratorExemption(unittest.TestCase):
    """Test quality scorer handles orchestrators correctly."""

    def test_quality_scorer_has_orchestrator_list(self):
        """Verify quality-scorer.py has ORCHESTRATOR_AGENTS constant."""
        try:
            # Import quality_scorer module (note: filename has hyphen but we added to path)
            quality_scorer_path = REPO_ROOT / 'self-improvement' / 'skills' / 'analyzing-component-quality' / 'scripts' / 'quality-scorer.py'

            content = quality_scorer_path.read_text()
            self.assertIn('ORCHESTRATOR_AGENTS', content,
                "quality-scorer.py should have ORCHESTRATOR_AGENTS constant")
            self.assertIn('project-coordinator', content,
                "quality-scorer.py should include project-coordinator in ORCHESTRATOR_AGENTS")
            self.assertIn('investigator', content,
                "quality-scorer.py should include investigator in ORCHESTRATOR_AGENTS")
        except Exception as e:
            self.fail(f"Error reading quality-scorer.py: {e}")

    def test_quality_scorer_exemption_logic(self):
        """Verify quality-scorer.py has exemption logic for orchestrators."""
        quality_scorer_path = REPO_ROOT / 'self-improvement' / 'skills' / 'analyzing-component-quality' / 'scripts' / 'quality-scorer.py'

        content = quality_scorer_path.read_text()

        # Check for exemption logic pattern
        self.assertIn('if agent_name not in ORCHESTRATOR_AGENTS', content,
            "quality-scorer.py should check if agent is NOT in ORCHESTRATOR_AGENTS before penalizing")

        # Check for positive message for orchestrators
        self.assertIn('Orchestrator agent', content,
            "quality-scorer.py should have message for orchestrator agents")


class TestCircularDelegationPrevention(unittest.TestCase):
    """Test no circular delegation patterns exist."""

    def setUp(self):
        self.agent_files = get_all_agent_files()

    def test_no_agent_references_itself(self):
        """No agent should explicitly delegate to itself."""
        self_references = []

        for agent_file in self.agent_files:
            agent_name = get_agent_name(agent_file)
            content = agent_file.read_text(encoding='utf-8')

            # Check for explicit self-delegation patterns
            delegation_patterns = [
                f'delegate to {agent_name}',
                f'Task → {agent_name}',
                f'Task tool → {agent_name}',
            ]

            for pattern in delegation_patterns:
                if pattern.lower() in content.lower():
                    self_references.append(
                        f"{agent_name} references delegating to itself: '{pattern}'"
                    )

        self.assertEqual(self_references, [],
            f"Potential circular delegation patterns found:\n" +
            "\n".join(f"  - {r}" for r in self_references)
        )


class TestAgentToolConsistency(unittest.TestCase):
    """Test agent tool declarations are consistent."""

    def setUp(self):
        self.agent_files = get_all_agent_files()

    def test_tool_names_are_valid(self):
        """Tool names should be valid Claude Code tools."""
        valid_tools = {
            'Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob',
            'Task', 'WebSearch', 'WebFetch', 'NotebookEdit',
            'TodoWrite', 'AskUserQuestion', 'BashOutput', 'KillShell'
        }

        invalid_tools = []

        for agent_file in self.agent_files:
            agent_name = get_agent_name(agent_file)
            tools = get_agent_tools(agent_file)

            for tool in tools:
                if tool not in valid_tools:
                    invalid_tools.append(f"{agent_name}: unknown tool '{tool}'")

        self.assertEqual(invalid_tools, [],
            f"Invalid tool names found:\n" +
            "\n".join(f"  - {i}" for i in invalid_tools)
        )


def main():
    """Run all tests and report results."""
    print("=" * 60)
    print("Agent Invocation Tests")
    print("=" * 60)
    print()

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAgentTaskToolPermissions))
    suite.addTests(loader.loadTestsFromTestCase(TestQualityScorerOrchestratorExemption))
    suite.addTests(loader.loadTestsFromTestCase(TestCircularDelegationPrevention))
    suite.addTests(loader.loadTestsFromTestCase(TestAgentToolConsistency))

    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print()
    print("=" * 60)
    if result.wasSuccessful():
        print("✓ All tests passed!")
        return 0
    else:
        print(f"✗ {len(result.failures)} failure(s), {len(result.errors)} error(s)")
        return 1


if __name__ == '__main__':
    sys.exit(main())
