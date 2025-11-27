#!/usr/bin/env python3
"""
Logseq Connection Test Script

Tests connectivity to Logseq using the configured or specified backend.

Usage:
    python test-connection.py [--backend http|cli|mcp] [--verbose]
"""

import json
import os
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

# ANSI colors
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
NC = "\033[0m"


def load_config() -> dict:
    """Load configuration from env.json if it exists."""
    config_path = Path(__file__).parent.parent.parent / ".claude" / "logseq-expert" / "env.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}


def test_http_connection(url: str, token: str, verbose: bool = False) -> tuple[bool, str, Optional[dict]]:
    """
    Test HTTP API connection.

    Returns: (success, message, graph_info)
    """
    if verbose:
        print(f"Testing HTTP API at {url}...")

    try:
        # Test basic connectivity
        req = urllib.request.Request(
            f"{url}/api",
            data=json.dumps({"method": "logseq.App.getCurrentGraph"}).encode(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

            if verbose:
                print(f"  Response: {json.dumps(data, indent=2)}")

            graph_info = data.get("result") if isinstance(data, dict) else None

            return True, "Connected to Logseq HTTP API", graph_info

    except urllib.error.HTTPError as e:
        if e.code == 401:
            return False, "Authentication failed - invalid token", None
        return False, f"HTTP error {e.code}: {e.reason}", None
    except urllib.error.URLError as e:
        return False, f"Connection failed: {e.reason}", None
    except Exception as e:
        return False, f"Error: {str(e)}", None


def test_cli_connection(graph_path: Optional[str], verbose: bool = False) -> tuple[bool, str, Optional[dict]]:
    """
    Test CLI connection.

    Returns: (success, message, graph_info)
    """
    if verbose:
        print("Testing CLI connection...")

    try:
        # Try to list graphs or run a simple query
        cmd = ["logseq", "graphs", "list"]

        if verbose:
            print(f"  Running: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            if verbose:
                print(f"  Output: {result.stdout}")
            return True, "CLI available", {"graphs": result.stdout.strip().split("\n")}
        else:
            return False, f"CLI error: {result.stderr}", None

    except FileNotFoundError:
        # Try npx
        try:
            result = subprocess.run(
                ["npx", "-y", "@logseq/cli", "graphs", "list"],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                return True, "CLI available (via npx)", {"graphs": result.stdout.strip().split("\n")}
            return False, f"CLI error: {result.stderr}", None
        except Exception as e:
            return False, f"CLI not found: {str(e)}", None
    except subprocess.TimeoutExpired:
        return False, "CLI command timed out", None
    except Exception as e:
        return False, f"CLI error: {str(e)}", None


def test_mcp_connection(verbose: bool = False) -> tuple[bool, str, Optional[dict]]:
    """
    Test MCP server availability.

    Returns: (success, message, server_info)
    """
    if verbose:
        print("Testing MCP server...")

    plugin_root = Path(__file__).parent.parent
    server_path = plugin_root / "servers" / "logseq-mcp"
    build_path = server_path / "build" / "index.js"

    if not server_path.exists():
        return False, "MCP server directory not found", None

    if not build_path.exists():
        return False, "MCP server not built - run: npm run build", None

    # Check if node is available
    try:
        node_check = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if node_check.returncode != 0:
            return False, "Node.js not found", None

        node_version = node_check.stdout.strip()

        if verbose:
            print(f"  Node version: {node_version}")
            print(f"  Server path: {build_path}")

        return True, f"MCP server ready (Node {node_version})", {
            "path": str(build_path),
            "node_version": node_version
        }

    except Exception as e:
        return False, f"Error checking MCP server: {str(e)}", None


def run_full_test(backend: Optional[str] = None, verbose: bool = False) -> dict:
    """Run connection test for specified or all backends."""
    config = load_config()
    results = {}

    backends_to_test = [backend] if backend else ["http", "cli", "mcp"]

    for b in backends_to_test:
        if b == "http":
            url = config.get("http", {}).get("url", os.environ.get("LOGSEQ_API_URL", "http://127.0.0.1:12315"))
            token = config.get("http", {}).get("token", os.environ.get("LOGSEQ_API_TOKEN", ""))

            if not token:
                results["http"] = {
                    "success": False,
                    "message": "No API token configured",
                    "info": None
                }
            else:
                success, message, info = test_http_connection(url, token, verbose)
                results["http"] = {"success": success, "message": message, "info": info}

        elif b == "cli":
            graph_path = config.get("cli", {}).get("graphPath")
            success, message, info = test_cli_connection(graph_path, verbose)
            results["cli"] = {"success": success, "message": message, "info": info}

        elif b == "mcp":
            success, message, info = test_mcp_connection(verbose)
            results["mcp"] = {"success": success, "message": message, "info": info}

    return results


def print_results(results: dict):
    """Print test results."""
    print(f"\n{BLUE}=== Connection Test Results ==={NC}\n")

    for backend, result in results.items():
        status = f"{GREEN}PASS{NC}" if result["success"] else f"{RED}FAIL{NC}"
        print(f"{backend.upper()}: {status}")
        print(f"  {result['message']}")
        if result["info"]:
            for key, value in result["info"].items():
                print(f"  {key}: {value}")
        print()

    # Summary
    passed = sum(1 for r in results.values() if r["success"])
    total = len(results)

    if passed == total:
        print(f"{GREEN}All {total} tests passed!{NC}")
    elif passed > 0:
        print(f"{YELLOW}{passed}/{total} tests passed{NC}")
    else:
        print(f"{RED}All tests failed{NC}")


def main():
    args = sys.argv[1:]

    verbose = "--verbose" in args or "-v" in args
    backend = None

    if "--backend" in args:
        idx = args.index("--backend")
        if idx + 1 < len(args):
            backend = args[idx + 1]
            if backend not in ["http", "cli", "mcp"]:
                print(f"Unknown backend: {backend}")
                print("Valid options: http, cli, mcp")
                sys.exit(1)

    if "--json" in args:
        results = run_full_test(backend, verbose)
        print(json.dumps(results, indent=2))
        sys.exit(0 if any(r["success"] for r in results.values()) else 1)

    results = run_full_test(backend, verbose)
    print_results(results)

    # Exit with success if any backend works
    sys.exit(0 if any(r["success"] for r in results.values()) else 1)


if __name__ == "__main__":
    main()
