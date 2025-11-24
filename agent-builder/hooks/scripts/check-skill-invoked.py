#!/usr/bin/env python3
"""
Check if appropriate agent-builder skill should be invoked before writing component files.

This hook checks if the Write tool is targeting a Claude Code component file
(skill, command, agent, hook, or plugin) and provides guidance on using the
appropriate agent-builder skill.

Exit codes:
  0 - Approve (not a component file, or guidance provided)
  2 - Block with message (component file detected, skill reminder)
"""

import json
import os
import re
import sys


def get_component_type(file_path: str) -> tuple:
    """
    Determine if the file path is a Claude Code component.

    Returns: (component_type, skill_name) or (None, None)
    """
    # Normalize path
    path = file_path.replace("\\", "/")

    # Component patterns and their corresponding skills
    patterns = [
        # Skills: */skills/*/SKILL.md
        (r".*/skills/[^/]+/SKILL\.md$", "skill", "building-skills"),

        # Commands: */commands/*.md
        (r".*/commands/[^/]+\.md$", "command", "building-commands"),

        # Agents: */agents/*.md
        (r".*/agents/[^/]+\.md$", "agent", "building-agents"),

        # Hooks: */hooks/hooks.json or */.claude/hooks.json
        (r".*/hooks/hooks\.json$", "hook", "building-hooks"),
        (r".*/\.claude/hooks\.json$", "hook", "building-hooks"),

        # Plugins: */.claude-plugin/plugin.json
        (r".*/\.claude-plugin/plugin\.json$", "plugin", "building-plugins"),
    ]

    for pattern, component_type, skill_name in patterns:
        if re.match(pattern, path, re.IGNORECASE):
            return component_type, skill_name

    return None, None


def main():
    # Get the file path from environment or stdin
    # The Write tool passes the file_path parameter
    file_path = os.environ.get("TOOL_INPUT_FILE_PATH", "")

    if not file_path:
        # Try to get from tool input JSON
        try:
            tool_input = os.environ.get("TOOL_INPUT", "{}")
            data = json.loads(tool_input)
            file_path = data.get("file_path", "")
        except json.JSONDecodeError:
            pass

    if not file_path:
        # If we still don't have the path, approve and let the prompt hook handle it
        result = {
            "decision": "approve",
            "reason": "Could not determine file path, deferring to prompt hook"
        }
        print(json.dumps(result))
        sys.exit(0)

    # Check if it's a component file
    component_type, skill_name = get_component_type(file_path)

    if component_type:
        # This is a component file - provide reminder
        result = {
            "decision": "approve",
            "reason": f"Writing {component_type} file",
            "additionalContext": (
                f"REMINDER: You are writing a {component_type} file. "
                f"Ensure you have invoked 'agent-builder:{skill_name}' for guidance. "
                f"Use templates from agent-builder/skills/{skill_name}/templates/."
            )
        }
        print(json.dumps(result))
        sys.exit(0)
    else:
        # Not a component file - approve silently
        result = {
            "decision": "approve",
            "suppressOutput": True
        }
        print(json.dumps(result))
        sys.exit(0)


if __name__ == "__main__":
    main()
