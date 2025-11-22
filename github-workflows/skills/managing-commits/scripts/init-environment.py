#!/usr/bin/env python3
"""
Initialize GitHub workflow environment.

Usage:
    python init-environment.py              # Initialize environment
    python init-environment.py --force      # Force re-initialization
    python init-environment.py --check      # Check if initialized
    python init-environment.py --show       # Show current environment
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Environment file location (in .claude for project-specific storage)
ENV_DIR = ".claude/github-workflows"
ENV_FILE = "env.json"

def get_env_path():
    """Get the environment file path, creating directory if needed."""
    env_dir = Path(ENV_DIR)
    env_dir.mkdir(exist_ok=True)
    return env_dir / ENV_FILE

def run_gh_command(args, default=None):
    """Run a GitHub CLI command and return output."""
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if default is not None:
            return default
        return None
    except FileNotFoundError:
        print("Error: GitHub CLI (gh) not found. Install from https://cli.github.com/", file=sys.stderr)
        return None

def run_git_command(args, default=None):
    """Run a git command and return output."""
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return default
    except FileNotFoundError:
        return default

def get_repository_info():
    """Get repository owner and name."""
    output = run_gh_command(["repo", "view", "--json", "owner,name,url"])
    if output:
        try:
            data = json.loads(output)
            return {
                "owner": data.get("owner", {}).get("login", "unknown"),
                "name": data.get("name", "unknown"),
                "fullName": f"{data.get('owner', {}).get('login', 'unknown')}/{data.get('name', 'unknown')}",
                "url": data.get("url", "")
            }
        except json.JSONDecodeError:
            pass
    return None

def get_user_info():
    """Get current GitHub user info."""
    output = run_gh_command(["api", "user", "--jq", ".login,.name"])
    if output:
        lines = output.split("\n")
        return {
            "login": lines[0] if len(lines) > 0 else "unknown",
            "name": lines[1] if len(lines) > 1 else ""
        }
    return None

def get_project_board(owner):
    """Get the most recent active project board."""
    # Try user projects first
    output = run_gh_command([
        "project", "list",
        "--owner", "@me",
        "--format", "json",
        "--limit", "5"
    ])

    if output:
        try:
            data = json.loads(output)
            projects = data.get("projects", [])
            if projects:
                # Return most recent (first in list)
                project = projects[0]
                return {
                    "number": project.get("number"),
                    "title": project.get("title", ""),
                    "url": project.get("url", "")
                }
        except json.JSONDecodeError:
            pass

    # Try org projects if user has none
    if owner and owner != "unknown":
        output = run_gh_command([
            "project", "list",
            "--owner", owner,
            "--format", "json",
            "--limit", "5"
        ])

        if output:
            try:
                data = json.loads(output)
                projects = data.get("projects", [])
                if projects:
                    project = projects[0]
                    return {
                        "number": project.get("number"),
                        "title": project.get("title", ""),
                        "url": project.get("url", "")
                    }
            except json.JSONDecodeError:
                pass

    return None

def get_milestone(owner, repo):
    """Get the current active milestone."""
    if not owner or not repo:
        return None

    output = run_gh_command([
        "api",
        f"repos/{owner}/{repo}/milestones",
        "--jq", ".[0] | {title: .title, number: .number, dueOn: .due_on}"
    ])

    if output:
        try:
            data = json.loads(output)
            if data.get("title"):
                return {
                    "title": data.get("title", ""),
                    "number": data.get("number"),
                    "dueOn": data.get("dueOn", "")
                }
        except json.JSONDecodeError:
            pass

    return None

def get_branch_info():
    """Get current branch and detect related issue."""
    branch_name = run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])

    if not branch_name:
        return None

    # Extract issue number from branch name
    issue_number = None
    patterns = [
        r"issue-(\d+)",
        r"/(\d+)-",
        r"^(\d+)-",
        r"-(\d+)$"
    ]

    for pattern in patterns:
        match = re.search(pattern, branch_name)
        if match:
            issue_number = int(match.group(1))
            break

    return {
        "name": branch_name,
        "relatedIssue": issue_number
    }

def get_issue_cache_info():
    """Get information about the issue cache."""
    cache_path = Path(".claude/github-workflows") / "active-issues.json"

    if not cache_path.exists():
        return None

    try:
        with open(cache_path) as f:
            data = json.load(f)
            return {
                "count": len(data.get("issues", [])),
                "lastSync": data.get("lastSync", ""),
                "filter": data.get("filter", "")
            }
    except Exception:
        return None

def sync_issues():
    """Sync issues using the issue-tracker script."""
    script_dir = Path(__file__).parent
    tracker_script = script_dir / "issue-tracker.py"

    if tracker_script.exists():
        try:
            subprocess.run(
                [sys.executable, str(tracker_script), "sync", "assigned"],
                capture_output=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError:
            pass

    return False

def load_environment():
    """Load existing environment file."""
    env_path = get_env_path()
    if env_path.exists():
        try:
            with open(env_path) as f:
                return json.load(f)
        except Exception:
            pass
    return None

def is_initialized_today():
    """Check if environment was initialized today."""
    env = load_environment()
    if not env:
        return False

    try:
        init_time = datetime.fromisoformat(env["initialized"].replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        return (now - init_time) < timedelta(hours=24)
    except Exception:
        return False

def initialize_environment(force=False):
    """Initialize the GitHub workflow environment."""

    # Check if already initialized
    if not force and is_initialized_today():
        print("Environment already initialized today. Use --force to re-initialize.")
        show_environment()
        return True

    print("Initializing GitHub workflow environment...\n")

    # Gather all context
    env = {
        "initialized": datetime.now(timezone.utc).isoformat()
    }

    # Repository info
    print("  Detecting repository...", end=" ")
    repo_info = get_repository_info()
    if repo_info:
        env["repository"] = repo_info
        print(f"✓ {repo_info['fullName']}")
    else:
        print("✗ Not found")
        return False

    # User info
    print("  Getting user info...", end=" ")
    user_info = get_user_info()
    if user_info:
        env["user"] = user_info
        print(f"✓ {user_info['login']}")
    else:
        print("✗ Not authenticated")

    # Project board
    print("  Finding project board...", end=" ")
    owner = repo_info.get("owner", "") if repo_info else ""
    project = get_project_board(owner)
    if project:
        env["projectBoard"] = project
        print(f"✓ {project['title']} (#{project['number']})")
    else:
        print("- None found")

    # Milestone
    print("  Getting milestone...", end=" ")
    repo_name = repo_info.get("name", "") if repo_info else ""
    milestone = get_milestone(owner, repo_name)
    if milestone:
        env["milestone"] = milestone
        due = f" (due {milestone['dueOn'][:10]})" if milestone.get('dueOn') else ""
        print(f"✓ {milestone['title']}{due}")
    else:
        print("- None active")

    # Branch info
    print("  Detecting branch...", end=" ")
    branch = get_branch_info()
    if branch:
        env["branch"] = branch
        issue_str = f" → Issue #{branch['relatedIssue']}" if branch.get('relatedIssue') else ""
        print(f"✓ {branch['name']}{issue_str}")
    else:
        print("- Not in git repo")

    # Sync issues
    print("  Syncing issues...", end=" ")
    if sync_issues():
        cache_info = get_issue_cache_info()
        if cache_info:
            env["issueCache"] = cache_info
            print(f"✓ {cache_info['count']} issues cached")
        else:
            print("✓ Done")
    else:
        print("- Sync failed")

    # Save environment
    env_path = get_env_path()
    with open(env_path, "w") as f:
        json.dump(env, f, indent=2)

    print(f"\n✅ Environment saved to {env_path}")

    # Show summary
    print("\n" + "=" * 50)
    show_summary(env)

    return True

def show_environment():
    """Show current environment details."""
    env = load_environment()
    if not env:
        print("Environment not initialized. Run: python init-environment.py")
        return

    print(json.dumps(env, indent=2))

def show_summary(env):
    """Show a summary of the environment."""
    print("\n📋 Workflow Environment Summary\n")

    if env.get("repository"):
        print(f"Repository: {env['repository']['fullName']}")

    if env.get("user"):
        print(f"User: {env['user']['login']}")

    if env.get("projectBoard"):
        print(f"Project Board: {env['projectBoard']['title']} (#{env['projectBoard']['number']})")

    if env.get("milestone"):
        due = f" - due {env['milestone']['dueOn'][:10]}" if env['milestone'].get('dueOn') else ""
        print(f"Milestone: {env['milestone']['title']}{due}")

    if env.get("branch"):
        issue = f" → Issue #{env['branch']['relatedIssue']}" if env['branch'].get('relatedIssue') else ""
        print(f"Branch: {env['branch']['name']}{issue}")

    if env.get("issueCache"):
        print(f"Cached Issues: {env['issueCache']['count']}")

    print("\n💡 Tips:")
    print("  - Use /commit-smart to commit with auto issue refs")
    print("  - Use /workflow-status for detailed workflow state")
    print("  - Use /issue-track to refresh issue cache")

def check_initialized():
    """Check if environment is initialized and recent."""
    if is_initialized_today():
        print("initialized")
        return 0
    elif load_environment():
        print("stale")
        return 1
    else:
        print("not_initialized")
        return 2

def main():
    if len(sys.argv) < 2:
        initialize_environment()
        return

    arg = sys.argv[1]

    if arg == "--force":
        initialize_environment(force=True)
    elif arg == "--check":
        sys.exit(check_initialized())
    elif arg == "--show":
        show_environment()
    elif arg == "--summary":
        env = load_environment()
        if env:
            show_summary(env)
        else:
            print("Not initialized")
    else:
        print(f"Unknown argument: {arg}")
        print(__doc__)

if __name__ == "__main__":
    main()
