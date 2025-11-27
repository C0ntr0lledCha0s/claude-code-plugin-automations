#!/usr/bin/env python3
"""
Logseq Backend Detection Script

Detects available Logseq integration backends and returns the best option.
Priority order: MCP -> HTTP API -> CLI

Usage:
    python detect-backend.py [--json] [--check <backend>]

Options:
    --json          Output results as JSON
    --check <name>  Check specific backend (http, cli, mcp)
"""

import json
import os
import shutil
import socket
import subprocess
import sys
from pathlib import Path
from typing import Optional

# ANSI colors
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
NC = "\033[0m"  # No Color


def check_http_api(url: str = "http://127.0.0.1:12315", token: Optional[str] = None) -> dict:
    """Check if Logseq HTTP API is available."""
    result = {
        "available": False,
        "url": url,
        "authenticated": False,
        "error": None
    }

    try:
        import urllib.request
        import urllib.error

        # Parse URL to get host and port
        if url.startswith("http://"):
            host_port = url[7:].split("/")[0]
        elif url.startswith("https://"):
            host_port = url[8:].split("/")[0]
        else:
            host_port = url.split("/")[0]

        host, port = host_port.split(":") if ":" in host_port else (host_port, "12315")

        # Quick socket check first
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        socket_result = sock.connect_ex((host, int(port)))
        sock.close()

        if socket_result != 0:
            result["error"] = f"Cannot connect to {host}:{port} - is Logseq running?"
            return result

        result["available"] = True

        # Try authenticated request if token provided
        if token:
            try:
                req = urllib.request.Request(
                    f"{url}/api",
                    data=json.dumps({"method": "logseq.App.getCurrentGraph"}).encode(),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {token}"
                    },
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    if response.status == 200:
                        result["authenticated"] = True
            except urllib.error.HTTPError as e:
                if e.code == 401:
                    result["error"] = "Invalid token"
                else:
                    result["error"] = f"HTTP {e.code}"
            except Exception as e:
                result["error"] = str(e)

    except Exception as e:
        result["error"] = str(e)

    return result


def check_cli() -> dict:
    """Check if Logseq CLI is available."""
    result = {
        "available": False,
        "path": None,
        "version": None,
        "error": None
    }

    # Check for @logseq/cli via npm/npx
    cli_path = shutil.which("logseq")

    if cli_path:
        result["path"] = cli_path
        result["available"] = True

        # Try to get version
        try:
            version_output = subprocess.run(
                ["logseq", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if version_output.returncode == 0:
                result["version"] = version_output.stdout.strip()
        except Exception as e:
            result["error"] = f"Version check failed: {e}"
    else:
        # Check if npx can run it
        try:
            npx_check = subprocess.run(
                ["npx", "-y", "@logseq/cli", "--version"],
                capture_output=True,
                text=True,
                timeout=30
            )
            if npx_check.returncode == 0:
                result["available"] = True
                result["path"] = "npx @logseq/cli"
                result["version"] = npx_check.stdout.strip()
        except FileNotFoundError:
            result["error"] = "Neither 'logseq' CLI nor 'npx' found"
        except subprocess.TimeoutExpired:
            result["error"] = "CLI check timed out"
        except Exception as e:
            result["error"] = str(e)

    return result


def check_mcp_server(server_path: Optional[str] = None) -> dict:
    """Check if MCP server is available and configured."""
    result = {
        "available": False,
        "path": None,
        "built": False,
        "error": None
    }

    # Default server location
    if server_path is None:
        plugin_root = Path(__file__).parent.parent
        server_path = plugin_root / "servers" / "logseq-mcp"
    else:
        server_path = Path(server_path)

    if not server_path.exists():
        result["error"] = f"MCP server not found at {server_path}"
        return result

    result["path"] = str(server_path)

    # Check if built
    build_path = server_path / "build" / "index.js"
    if build_path.exists():
        result["built"] = True
        result["available"] = True
    else:
        # Check if source exists
        src_path = server_path / "src" / "index.ts"
        if src_path.exists():
            result["error"] = "MCP server exists but not built. Run: npm run build"
        else:
            result["error"] = "MCP server source not found"

    return result


def detect_best_backend() -> dict:
    """Detect all backends and return the best available option."""
    # Load config if exists
    config_path = Path(__file__).parent.parent.parent / ".claude" / "logseq-expert" / "env.json"
    config = {}
    if config_path.exists():
        try:
            with open(config_path) as f:
                config = json.load(f)
        except Exception:
            pass

    # Get settings from config or environment
    http_url = config.get("http", {}).get("url", os.environ.get("LOGSEQ_API_URL", "http://127.0.0.1:12315"))
    http_token = config.get("http", {}).get("token", os.environ.get("LOGSEQ_API_TOKEN"))
    mcp_path = config.get("mcp", {}).get("serverPath")

    results = {
        "recommended": None,
        "backends": {
            "http": check_http_api(http_url, http_token),
            "cli": check_cli(),
            "mcp": check_mcp_server(mcp_path)
        },
        "config_loaded": config_path.exists()
    }

    # Determine best backend (priority: MCP with HTTP -> HTTP -> CLI)
    if results["backends"]["mcp"]["available"] and results["backends"]["http"]["available"]:
        results["recommended"] = "mcp"
    elif results["backends"]["http"]["available"]:
        results["recommended"] = "http"
    elif results["backends"]["cli"]["available"]:
        results["recommended"] = "cli"

    return results


def print_results(results: dict, as_json: bool = False):
    """Print detection results."""
    if as_json:
        print(json.dumps(results, indent=2))
        return

    print(f"\n{BLUE}=== Logseq Backend Detection ==={NC}\n")

    # HTTP API
    http = results["backends"]["http"]
    status = f"{GREEN}Available{NC}" if http["available"] else f"{RED}Unavailable{NC}"
    print(f"HTTP API: {status}")
    print(f"  URL: {http['url']}")
    if http["available"]:
        auth = f"{GREEN}Yes{NC}" if http["authenticated"] else f"{YELLOW}No token{NC}"
        print(f"  Authenticated: {auth}")
    if http["error"]:
        print(f"  {RED}Error: {http['error']}{NC}")

    print()

    # CLI
    cli = results["backends"]["cli"]
    status = f"{GREEN}Available{NC}" if cli["available"] else f"{RED}Unavailable{NC}"
    print(f"CLI: {status}")
    if cli["path"]:
        print(f"  Path: {cli['path']}")
    if cli["version"]:
        print(f"  Version: {cli['version']}")
    if cli["error"]:
        print(f"  {RED}Error: {cli['error']}{NC}")

    print()

    # MCP Server
    mcp = results["backends"]["mcp"]
    status = f"{GREEN}Available{NC}" if mcp["available"] else f"{RED}Unavailable{NC}"
    print(f"MCP Server: {status}")
    if mcp["path"]:
        print(f"  Path: {mcp['path']}")
        built = f"{GREEN}Yes{NC}" if mcp["built"] else f"{YELLOW}No{NC}"
        print(f"  Built: {built}")
    if mcp["error"]:
        print(f"  {RED}Error: {mcp['error']}{NC}")

    print()

    # Recommendation
    if results["recommended"]:
        print(f"{GREEN}Recommended backend: {results['recommended'].upper()}{NC}")
    else:
        print(f"{RED}No backends available!{NC}")
        print(f"\n{YELLOW}To enable backends:{NC}")
        print("  HTTP: Start Logseq with API server enabled")
        print("  CLI:  npm install -g @logseq/cli")
        print("  MCP:  Build the MCP server in servers/logseq-mcp/")


def main():
    args = sys.argv[1:]

    as_json = "--json" in args

    if "--check" in args:
        idx = args.index("--check")
        if idx + 1 < len(args):
            backend = args[idx + 1]
            if backend == "http":
                result = check_http_api()
            elif backend == "cli":
                result = check_cli()
            elif backend == "mcp":
                result = check_mcp_server()
            else:
                print(f"Unknown backend: {backend}")
                sys.exit(1)

            if as_json:
                print(json.dumps(result, indent=2))
            else:
                print(f"{backend.upper()}: {'Available' if result['available'] else 'Unavailable'}")

            sys.exit(0 if result["available"] else 1)

    results = detect_best_backend()
    print_results(results, as_json)

    # Exit with appropriate code
    sys.exit(0 if results["recommended"] else 1)


if __name__ == "__main__":
    main()
