#!/usr/bin/env python3
"""
Logseq Environment Initialization Script

Interactive setup wizard for configuring Logseq integration.
Creates the environment configuration file with detected settings.

Usage:
    python init-environment.py [--force] [--non-interactive]
"""

import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Optional

# ANSI colors
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
CYAN = "\033[0;36m"
BOLD = "\033[1m"
NC = "\033[0m"

# Import sibling modules
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from detect_backend import check_http_api, check_cli, check_mcp_server


def get_env_dir() -> Path:
    """Get the environment directory path."""
    # Store in project's .claude directory
    project_root = Path.cwd()
    env_dir = project_root / ".claude" / "logseq-expert"
    return env_dir


def get_env_path() -> Path:
    """Get the full path to env.json."""
    return get_env_dir() / "env.json"


def detect_os() -> str:
    """Detect the operating system."""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    return "linux"


def find_logseq_graphs() -> list[Path]:
    """Find Logseq graph directories."""
    graphs = []
    os_type = detect_os()

    # Common locations
    home = Path.home()
    search_paths = []

    if os_type == "macos":
        search_paths = [
            home / "Documents" / "logseq",
            home / "logseq",
            home / "Library" / "Application Support" / "Logseq",
        ]
    elif os_type == "windows":
        search_paths = [
            home / "Documents" / "logseq",
            home / "logseq",
            Path(os.environ.get("APPDATA", "")) / "Logseq",
        ]
    else:  # Linux
        search_paths = [
            home / "logseq",
            home / "Documents" / "logseq",
            home / ".logseq",
        ]

    for path in search_paths:
        if path.exists() and path.is_dir():
            # Look for graph directories (contain logseq/ folder or db.sqlite)
            for item in path.iterdir():
                if item.is_dir():
                    if (item / "logseq").exists() or (item / "db.sqlite").exists():
                        graphs.append(item)

    return graphs


def prompt(message: str, default: Optional[str] = None) -> str:
    """Prompt user for input."""
    if default:
        result = input(f"{message} [{default}]: ").strip()
        return result if result else default
    return input(f"{message}: ").strip()


def prompt_yes_no(message: str, default: bool = True) -> bool:
    """Prompt user for yes/no."""
    default_str = "Y/n" if default else "y/N"
    result = input(f"{message} [{default_str}]: ").strip().lower()
    if not result:
        return default
    return result in ("y", "yes", "true", "1")


def print_header(text: str):
    """Print a section header."""
    print(f"\n{BOLD}{BLUE}{'=' * 50}{NC}")
    print(f"{BOLD}{BLUE}{text}{NC}")
    print(f"{BOLD}{BLUE}{'=' * 50}{NC}\n")


def print_step(num: int, text: str):
    """Print a step."""
    print(f"{CYAN}[{num}]{NC} {text}")


def run_interactive_setup() -> dict:
    """Run interactive setup wizard."""
    print_header("Logseq Expert Plugin Setup")

    config = {
        "backend": "auto",
        "http": {
            "url": "http://127.0.0.1:12315",
            "token": ""
        },
        "cli": {
            "graphPath": "",
            "inApp": False
        },
        "mcp": {
            "enabled": True,
            "serverPath": ""
        },
        "preferences": {
            "defaultGraph": None,
            "confirmWrites": False,
            "backupBeforeWrite": False
        },
        "initialized": True,
        "os": detect_os()
    }

    # Step 1: Detect backends
    print_step(1, "Detecting available backends...")
    print()

    http_result = check_http_api()
    cli_result = check_cli()
    mcp_result = check_mcp_server()

    print(f"  HTTP API: {GREEN}Available{NC}" if http_result["available"] else f"  HTTP API: {YELLOW}Not running{NC}")
    print(f"  CLI:      {GREEN}Available{NC}" if cli_result["available"] else f"  CLI:      {YELLOW}Not installed{NC}")
    print(f"  MCP:      {GREEN}Available{NC}" if mcp_result["available"] else f"  MCP:      {YELLOW}Not built{NC}")
    print()

    # Step 2: HTTP API Configuration
    print_step(2, "HTTP API Configuration")

    if http_result["available"]:
        print(f"  {GREEN}Logseq is running with HTTP API enabled{NC}")
    else:
        print(f"  {YELLOW}To enable HTTP API:{NC}")
        print("    1. Open Logseq")
        print("    2. Settings > Advanced > Developer mode: ON")
        print("    3. Settings > Advanced > HTTP APIs server: ON")
        print()

    config["http"]["url"] = prompt("  HTTP API URL", "http://127.0.0.1:12315")

    # Token setup
    existing_token = os.environ.get("LOGSEQ_API_TOKEN", "")
    if existing_token:
        print(f"  {GREEN}Found LOGSEQ_API_TOKEN in environment{NC}")
        use_env = prompt_yes_no("  Use environment variable for token?", True)
        if use_env:
            config["http"]["token"] = "${LOGSEQ_API_TOKEN}"
        else:
            config["http"]["token"] = prompt("  Enter API token")
    else:
        print(f"  {YELLOW}No LOGSEQ_API_TOKEN found in environment{NC}")
        print("  To create a token in Logseq: Settings > Advanced > Authorization tokens")
        token = prompt("  Enter API token (or leave empty to skip)")
        if token:
            config["http"]["token"] = token
            print(f"  {YELLOW}Tip: Set LOGSEQ_API_TOKEN environment variable for security{NC}")

    print()

    # Step 3: CLI Configuration
    print_step(3, "CLI Configuration")

    if cli_result["available"]:
        print(f"  {GREEN}CLI is available{NC}")
        if cli_result["path"]:
            print(f"  Path: {cli_result['path']}")
    else:
        print(f"  {YELLOW}CLI not installed. Install with: npm install -g @logseq/cli{NC}")

    # Find graphs
    graphs = find_logseq_graphs()
    if graphs:
        print(f"\n  Found {len(graphs)} graph(s):")
        for i, g in enumerate(graphs, 1):
            graph_type = "DB" if (g / "db.sqlite").exists() else "MD"
            print(f"    {i}. {g.name} ({graph_type}) - {g}")

        print()
        choice = prompt("  Select default graph (number) or enter path", "")
        if choice.isdigit() and 0 < int(choice) <= len(graphs):
            config["cli"]["graphPath"] = str(graphs[int(choice) - 1])
            config["preferences"]["defaultGraph"] = graphs[int(choice) - 1].name
        elif choice:
            config["cli"]["graphPath"] = choice
    else:
        print(f"  {YELLOW}No graphs found automatically{NC}")
        config["cli"]["graphPath"] = prompt("  Enter graph path (or leave empty)", "")

    print()

    # Step 4: MCP Server
    print_step(4, "MCP Server Configuration")

    if mcp_result["available"]:
        print(f"  {GREEN}MCP server is built and ready{NC}")
        config["mcp"]["serverPath"] = mcp_result["path"]
    else:
        print(f"  {YELLOW}MCP server not built yet{NC}")
        if mcp_result["path"]:
            print(f"  To build: cd {mcp_result['path']} && npm install && npm run build")

    config["mcp"]["enabled"] = prompt_yes_no("  Enable MCP server?", True)

    print()

    # Step 5: Preferences
    print_step(5, "Preferences")

    config["preferences"]["confirmWrites"] = prompt_yes_no("  Confirm before write operations?", False)
    config["preferences"]["backupBeforeWrite"] = prompt_yes_no("  Create backups before writes?", False)

    print()

    # Summary
    print_header("Configuration Summary")

    print(f"Backend priority: {CYAN}auto{NC} (MCP > HTTP > CLI)")
    print(f"HTTP URL: {config['http']['url']}")
    print(f"HTTP Token: {'configured' if config['http']['token'] else 'not set'}")
    print(f"Graph path: {config['cli']['graphPath'] or 'not set'}")
    print(f"MCP enabled: {config['mcp']['enabled']}")
    print()

    return config


def run_non_interactive_setup() -> dict:
    """Run non-interactive setup with auto-detection."""
    config = {
        "backend": "auto",
        "http": {
            "url": os.environ.get("LOGSEQ_API_URL", "http://127.0.0.1:12315"),
            "token": "${LOGSEQ_API_TOKEN}" if os.environ.get("LOGSEQ_API_TOKEN") else ""
        },
        "cli": {
            "graphPath": os.environ.get("LOGSEQ_GRAPH_PATH", ""),
            "inApp": False
        },
        "mcp": {
            "enabled": True,
            "serverPath": ""
        },
        "preferences": {
            "defaultGraph": None,
            "confirmWrites": False,
            "backupBeforeWrite": False
        },
        "initialized": True,
        "os": detect_os()
    }

    # Auto-detect MCP server path
    mcp_result = check_mcp_server()
    if mcp_result["path"]:
        config["mcp"]["serverPath"] = mcp_result["path"]

    return config


def save_config(config: dict, force: bool = False) -> bool:
    """Save configuration to env.json."""
    env_path = get_env_path()

    if env_path.exists() and not force:
        print(f"{YELLOW}Configuration already exists at {env_path}{NC}")
        if not prompt_yes_no("Overwrite?", False):
            return False

    # Create directory if needed
    env_path.parent.mkdir(parents=True, exist_ok=True)

    with open(env_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"{GREEN}Configuration saved to {env_path}{NC}")
    return True


def main():
    args = sys.argv[1:]

    force = "--force" in args
    non_interactive = "--non-interactive" in args

    # Check if already initialized
    env_path = get_env_path()
    if env_path.exists() and not force:
        print(f"{YELLOW}Already initialized. Use --force to reinitialize.{NC}")

        # Show current config
        with open(env_path) as f:
            config = json.load(f)
        print(f"\nCurrent config: {env_path}")
        print(json.dumps(config, indent=2))
        return

    if non_interactive:
        config = run_non_interactive_setup()
    else:
        config = run_interactive_setup()

        if not prompt_yes_no("Save configuration?", True):
            print("Setup cancelled.")
            return

    save_config(config, force)

    print(f"\n{GREEN}Setup complete!{NC}")
    print("\nNext steps:")
    print("  1. Ensure Logseq is running with HTTP API enabled")
    print("  2. Set LOGSEQ_API_TOKEN environment variable if not done")
    print("  3. Use /logseq:status to verify connection")


if __name__ == "__main__":
    main()
