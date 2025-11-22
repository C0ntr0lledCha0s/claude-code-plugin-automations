#!/usr/bin/env python3
"""
Issue Tracker - Sync and cache GitHub issues for commit integration.

Usage:
    python issue-tracker.py sync [filter] [value]   # Sync issues from GitHub
    python issue-tracker.py show                    # Display cached issues
    python issue-tracker.py find-related [files...] # Find related issues
    python issue-tracker.py get [number]            # Get specific issue
    python issue-tracker.py suggest-refs            # Suggest issue refs for staged changes
    python issue-tracker.py clear                   # Clear the cache
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Cache file location (in .claude for project-specific storage)
CACHE_DIR = ".claude/github-workflows"
CACHE_FILE = "active-issues.json"

def get_cache_path():
    """Get the cache file path, creating directory if needed."""
    cache_dir = Path(CACHE_DIR)
    cache_dir.mkdir(exist_ok=True)
    return cache_dir / CACHE_FILE

def run_gh_command(args):
    """Run a GitHub CLI command and return JSON output."""
    try:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout) if result.stdout.strip() else []
    except subprocess.CalledProcessError as e:
        print(f"Error running gh command: {e.stderr}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        return None

def get_repo_info():
    """Get current repository owner/name."""
    try:
        result = subprocess.run(
            ["gh", "repo", "view", "--json", "nameWithOwner"],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(result.stdout)
        return data.get("nameWithOwner", "unknown/unknown")
    except Exception:
        return "unknown/unknown"

def sync_issues(filter_type="assigned", filter_value=None):
    """Sync issues from GitHub based on filter."""
    args = ["issue", "list", "--state", "open", "--json",
            "number,title,state,labels,assignees,milestone,createdAt,updatedAt,url,body"]

    if filter_type == "assigned":
        args.extend(["--assignee", "@me"])
    elif filter_type == "labeled" and filter_value:
        args.extend(["--label", filter_value])
    elif filter_type == "milestone" and filter_value:
        args.extend(["--milestone", filter_value])
    elif filter_type == "all":
        pass  # No additional filters
    else:
        args.extend(["--assignee", "@me"])  # Default to assigned

    print(f"Syncing issues (filter: {filter_type})...", file=sys.stderr)
    issues = run_gh_command(args)

    if issues is None:
        return False

    # Process issues
    processed = []
    for issue in issues:
        processed.append({
            "number": issue.get("number"),
            "title": issue.get("title", ""),
            "state": issue.get("state", "open"),
            "labels": [l.get("name", "") for l in issue.get("labels", [])],
            "assignees": [a.get("login", "") for a in issue.get("assignees", [])],
            "milestone": issue.get("milestone", {}).get("title") if issue.get("milestone") else None,
            "created_at": issue.get("createdAt", ""),
            "updated_at": issue.get("updatedAt", ""),
            "url": issue.get("url", ""),
            "body_preview": (issue.get("body", "") or "")[:200]
        })

    # Save to cache
    cache_data = {
        "lastSync": datetime.now(timezone.utc).isoformat(),
        "repository": get_repo_info(),
        "filter": filter_type,
        "filterValue": filter_value,
        "issues": processed
    }

    cache_path = get_cache_path()
    with open(cache_path, "w") as f:
        json.dump(cache_data, f, indent=2)

    print(f"Cached {len(processed)} issues to {cache_path}", file=sys.stderr)
    return True

def load_cache():
    """Load issues from cache."""
    cache_path = get_cache_path()
    if not cache_path.exists():
        return None

    try:
        with open(cache_path) as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading cache: {e}", file=sys.stderr)
        return None

def show_issues():
    """Display cached issues as a task list."""
    cache = load_cache()

    if not cache:
        print("No cached issues. Run: python issue-tracker.py sync")
        return

    # Check cache age
    last_sync = datetime.fromisoformat(cache["lastSync"].replace("Z", "+00:00"))
    age_minutes = (datetime.now(timezone.utc) - last_sync).total_seconds() / 60

    if age_minutes > 60:
        print(f"⚠️  Cache is {int(age_minutes)} minutes old. Consider running: sync")
        print()

    print(f"📋 Active Issues (synced {int(age_minutes)} minutes ago)")
    print(f"Repository: {cache['repository']}")
    print(f"Filter: {cache['filter']}")
    if cache.get('filterValue'):
        print(f"Value: {cache['filterValue']}")
    print()

    issues = cache.get("issues", [])
    if not issues:
        print("No issues found.")
        return

    # Sort by priority
    high_priority = []
    normal = []

    for issue in issues:
        labels = issue.get("labels", [])
        is_high = any("high" in l.lower() for l in labels)
        if is_high:
            high_priority.append(issue)
        else:
            normal.append(issue)

    def print_issue(issue):
        labels = ", ".join(issue.get("labels", [])) or "none"
        milestone = issue.get("milestone") or "none"
        print(f"┌─ #{issue['number']} {issue['title']}")
        print(f"│  Labels: {labels}")
        if milestone != "none":
            print(f"│  Milestone: {milestone}")
        print(f"└─ Use: Closes #{issue['number']} or Refs #{issue['number']}")
        print()

    if high_priority:
        print("HIGH PRIORITY:")
        for issue in high_priority:
            print_issue(issue)

    if normal:
        print("NORMAL PRIORITY:")
        for issue in normal:
            print_issue(issue)

    print("💡 Tip: Use /commit-smart to auto-suggest these in commits")

def get_current_branch():
    """Get the current git branch name."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception:
        return None

def extract_issue_from_branch(branch_name):
    """Extract issue number from branch name."""
    if not branch_name:
        return None

    # Patterns: feature/issue-42, feature/42-auth, fix/42, 42-something
    patterns = [
        r"issue-(\d+)",
        r"/(\d+)-",
        r"^(\d+)-",
        r"-(\d+)$"
    ]

    for pattern in patterns:
        match = re.search(pattern, branch_name)
        if match:
            return int(match.group(1))

    return None

def find_related_issues(files=None):
    """Find issues related to given files or staged changes."""
    cache = load_cache()
    if not cache:
        print("No cached issues. Run sync first.", file=sys.stderr)
        return []

    issues = cache.get("issues", [])
    if not issues:
        return []

    # Get files to analyze
    if not files:
        # Get staged files
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only"],
                capture_output=True,
                text=True,
                check=True
            )
            files = result.stdout.strip().split("\n") if result.stdout.strip() else []
        except Exception:
            files = []

    # Score each issue
    scored = []
    branch = get_current_branch()
    branch_issue = extract_issue_from_branch(branch)

    for issue in issues:
        score = 0
        reasons = []

        # Branch match (highest priority)
        if branch_issue and issue["number"] == branch_issue:
            score += 100
            reasons.append("branch name match")

        # Keyword matching
        issue_text = f"{issue['title']} {issue.get('body_preview', '')}".lower()

        for file in files:
            # Extract keywords from file path
            parts = Path(file).stem.replace("-", " ").replace("_", " ").split()
            for part in parts:
                if len(part) > 2 and part.lower() in issue_text:
                    score += 10
                    if f"file keyword: {part}" not in reasons:
                        reasons.append(f"file keyword: {part}")

        # Label matching
        labels = issue.get("labels", [])
        for file in files:
            if "test" in file and any("test" in l.lower() for l in labels):
                score += 5
            if "auth" in file and any("auth" in l.lower() for l in labels):
                score += 5
            if "api" in file and any("api" in l.lower() for l in labels):
                score += 5

        if score > 0:
            scored.append({
                "issue": issue,
                "score": score,
                "reasons": reasons
            })

    # Sort by score
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored

def suggest_refs():
    """Suggest issue references for current staged changes."""
    related = find_related_issues()

    if not related:
        print("No related issues found.")
        return

    branch = get_current_branch()
    branch_issue = extract_issue_from_branch(branch)

    print("Suggested issue references for your commit:\n")

    for i, item in enumerate(related[:5]):  # Top 5
        issue = item["issue"]
        score = item["score"]
        reasons = item["reasons"]

        # Determine reference type
        if branch_issue and issue["number"] == branch_issue:
            ref_type = "Closes"
            confidence = "HIGH"
        elif score >= 50:
            ref_type = "Closes"
            confidence = "HIGH"
        elif score >= 20:
            ref_type = "Refs"
            confidence = "MEDIUM"
        else:
            ref_type = "Refs"
            confidence = "LOW"

        print(f"{i+1}. [{confidence}] {ref_type} #{issue['number']}")
        print(f"   Title: {issue['title']}")
        print(f"   Match: {', '.join(reasons)}")
        print()

    # Provide formatted footer
    if related:
        top_issue = related[0]["issue"]
        branch_match = branch_issue and top_issue["number"] == branch_issue
        ref = "Closes" if branch_match else "Refs"
        print(f"Suggested commit footer:\n{ref} #{top_issue['number']}")

def get_issue(number):
    """Get a specific issue from cache."""
    cache = load_cache()
    if not cache:
        return None

    for issue in cache.get("issues", []):
        if issue["number"] == number:
            return issue

    return None

def clear_cache():
    """Clear the issue cache."""
    cache_path = get_cache_path()
    if cache_path.exists():
        cache_path.unlink()
        print(f"Cleared cache: {cache_path}")
    else:
        print("No cache to clear.")

def main():
    if len(sys.argv) < 2:
        show_issues()
        return

    command = sys.argv[1]

    if command == "sync":
        filter_type = sys.argv[2] if len(sys.argv) > 2 else "assigned"
        filter_value = sys.argv[3] if len(sys.argv) > 3 else None
        if sync_issues(filter_type, filter_value):
            show_issues()

    elif command == "show":
        show_issues()

    elif command == "find-related":
        files = sys.argv[2:] if len(sys.argv) > 2 else None
        related = find_related_issues(files)
        print(json.dumps(related, indent=2, default=str))

    elif command == "suggest-refs":
        suggest_refs()

    elif command == "get":
        if len(sys.argv) < 3:
            print("Usage: issue-tracker.py get <number>")
            return
        number = int(sys.argv[2])
        issue = get_issue(number)
        if issue:
            print(json.dumps(issue, indent=2))
        else:
            print(f"Issue #{number} not found in cache.")

    elif command == "clear":
        clear_cache()

    elif command == "json":
        # Output cache as JSON for other tools
        cache = load_cache()
        if cache:
            print(json.dumps(cache, indent=2))
        else:
            print("{}")

    else:
        print(f"Unknown command: {command}")
        print(__doc__)

if __name__ == "__main__":
    main()
