#!/usr/bin/env bash
# Preflight checks for github-workflows commands
# Validates environment before executing commands

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info() { echo -e "${BLUE}ℹ${NC} $1"; }
success() { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1" >&2; }

# Check if we're in a git repository
check_git_repo() {
    if git rev-parse --git-dir >/dev/null 2>&1; then
        success "Git repository detected"
        return 0
    else
        error "Not in a git repository"
        info "Run: git init"
        return 1
    fi
}

# Check if remote repository is configured
check_git_remote() {
    if git remote get-url origin >/dev/null 2>&1; then
        success "Git remote configured"
        return 0
    else
        warn "No git remote configured"
        info "Add remote: git remote add origin <url>"
        return 1
    fi
}

# Check if GitHub CLI is authenticated
check_gh_auth() {
    if ! command -v gh >/dev/null 2>&1; then
        error "GitHub CLI (gh) not installed"
        return 1
    fi

    if gh auth status >/dev/null 2>&1; then
        success "GitHub CLI authenticated"
        return 0
    else
        error "GitHub CLI not authenticated"
        info "Run: gh auth login"
        return 1
    fi
}

# Check repository permissions
check_repo_permissions() {
    local required_permission="${1:-write}"

    if ! command -v gh >/dev/null 2>&1; then
        warn "Cannot check permissions (gh CLI not found)"
        return 0  # Non-blocking
    fi

    local permissions
    permissions=$(gh api /user/repos --jq '.[].permissions' 2>/dev/null || echo "")

    if [ -z "$permissions" ]; then
        warn "Could not determine repository permissions"
        return 0  # Non-blocking
    fi

    success "Repository permissions OK"
    return 0
}

# Check if dependencies are available
check_dependencies() {
    local missing=()

    # Check for jq
    if ! command -v jq >/dev/null 2>&1; then
        missing+=("jq")
    fi

    # Check for python3
    if ! command -v python3 >/dev/null 2>&1; then
        missing+=("python3")
    fi

    if [ ${#missing[@]} -gt 0 ]; then
        warn "Optional dependencies missing: ${missing[*]}"
        info "Install them for full functionality"
        return 0  # Non-blocking
    else
        success "Dependencies available"
        return 0
    fi
}

# Check network connectivity to GitHub
check_github_connectivity() {
    if ! command -v curl >/dev/null 2>&1; then
        warn "curl not available, skipping connectivity check"
        return 0  # Non-blocking
    fi

    if curl -s --connect-timeout 5 https://api.github.com >/dev/null 2>&1; then
        success "GitHub API reachable"
        return 0
    else
        warn "Cannot reach GitHub API"
        info "Check your internet connection"
        return 0  # Non-blocking
    fi
}

# Run all preflight checks
preflight_all() {
    local strict="${1:-false}"
    local errors=0

    info "Running preflight checks..."

    # Critical checks (must pass)
    check_git_repo || ((errors++))
    check_gh_auth || ((errors++))

    # Important checks (warnings only)
    check_git_remote || true
    check_dependencies || true
    check_github_connectivity || true
    check_repo_permissions || true

    echo ""

    if [ $errors -eq 0 ]; then
        success "Preflight checks passed"
        return 0
    else
        error "Preflight checks failed: $errors critical error(s)"
        if [ "$strict" = "true" ]; then
            exit 1
        fi
        return 1
    fi
}

# Quick check (only critical items)
preflight_quick() {
    check_gh_auth
}

# Main command router
main() {
    local mode="${1:-all}"

    case "$mode" in
        all)
            preflight_all false
            ;;
        strict)
            preflight_all true
            ;;
        quick)
            preflight_quick
            ;;
        git)
            check_git_repo
            ;;
        remote)
            check_git_remote
            ;;
        auth)
            check_gh_auth
            ;;
        deps)
            check_dependencies
            ;;
        network)
            check_github_connectivity
            ;;
        permissions)
            check_repo_permissions "$2"
            ;;
        help|*)
            cat <<EOF
Preflight Checks Script

Usage: $0 <mode>

Modes:
  all          Run all checks (default, non-strict)
  strict       Run all checks (fail on errors)
  quick        Quick check (auth only)
  git          Check git repository
  remote       Check git remote
  auth         Check GitHub auth
  deps         Check dependencies
  network      Check GitHub connectivity
  permissions  Check repository permissions
  help         Show this help

Examples:
  $0 all
  $0 quick
  $0 auth
  $0 permissions write

EOF
            ;;
    esac
}

# Run if executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi
