#!/usr/bin/env bash
# GitHub label management helpers
# Provides utilities for checking and creating labels

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

# Check if gh CLI is available
check_gh() {
    if ! command -v gh >/dev/null 2>&1; then
        error "GitHub CLI (gh) not found"
        return 1
    fi

    if ! gh auth status >/dev/null 2>&1; then
        error "Not authenticated with GitHub. Run: gh auth login"
        return 1
    fi

    return 0
}

# Check if a label exists
label_exists() {
    local label_name="$1"

    check_gh || return 1

    if gh label list --json name --jq ".[].name" 2>/dev/null | grep -qx "$label_name"; then
        return 0
    fi

    return 1
}

# Create a label if it doesn't exist
ensure_label() {
    local label_name="$1"
    local color="${2:-0366d6}"
    local description="${3:-}"

    check_gh || return 1

    if label_exists "$label_name"; then
        success "Label '$label_name' already exists"
        return 0
    fi

    info "Creating label '$label_name'..."

    local create_cmd="gh label create \"$label_name\" --color \"$color\""

    if [ -n "$description" ]; then
        create_cmd="$create_cmd --description \"$description\""
    fi

    if eval "$create_cmd" >/dev/null 2>&1; then
        success "Created label '$label_name'"
        return 0
    else
        error "Failed to create label '$label_name'"
        return 1
    fi
}

# Create multiple standard labels
create_standard_labels() {
    info "Creating standard labels..."

    # Type labels
    ensure_label "bug" "d73a4a" "Something isn't working"
    ensure_label "enhancement" "a2eeef" "New feature or request"
    ensure_label "documentation" "0075ca" "Improvements or additions to documentation"
    ensure_label "plugin" "7057ff" "Claude Code plugin"

    # Priority labels
    ensure_label "priority:high" "b60205" "High priority"
    ensure_label "priority:medium" "fbca04" "Medium priority"
    ensure_label "priority:low" "0e8a16" "Low priority"

    # Status labels
    ensure_label "status:in-progress" "1d76db" "Currently being worked on"
    ensure_label "status:blocked" "e11d21" "Blocked by dependencies"
    ensure_label "status:review" "fbca04" "Ready for review"

    success "Standard labels created"
}

# Validate labels before creating an issue
validate_labels() {
    local labels=("$@")
    local missing=()
    local all_valid=true

    for label in "${labels[@]}"; do
        if ! label_exists "$label"; then
            missing+=("$label")
            all_valid=false
        fi
    done

    if [ "$all_valid" = "true" ]; then
        return 0
    else
        warn "Missing labels: ${missing[*]}"
        return 1
    fi
}

# Auto-create labels from a comma-separated list
ensure_labels() {
    local labels_str="$1"

    # Split comma-separated labels
    IFS=',' read -ra labels <<< "$labels_str"

    local all_ok=true

    for label in "${labels[@]}"; do
        # Trim whitespace
        label=$(echo "$label" | xargs)

        # Determine color based on label prefix
        local color="cccccc"
        local description=""

        case "$label" in
            bug*)
                color="d73a4a"
                description="Something isn't working"
                ;;
            enhancement*)
                color="a2eeef"
                description="New feature or request"
                ;;
            documentation*)
                color="0075ca"
                description="Documentation"
                ;;
            plugin*)
                color="7057ff"
                description="Claude Code plugin"
                ;;
            priority:high*)
                color="b60205"
                description="High priority"
                ;;
            priority:medium*)
                color="fbca04"
                description="Medium priority"
                ;;
            priority:low*)
                color="0e8a16"
                description="Low priority"
                ;;
            *)
                color="cccccc"
                description="$label"
                ;;
        esac

        if ! ensure_label "$label" "$color" "$description"; then
            all_ok=false
        fi
    done

    if [ "$all_ok" = "true" ]; then
        return 0
    else
        return 1
    fi
}

# Main command router
main() {
    local command="${1:-help}"
    shift || true

    case "$command" in
        exists)
            label_exists "$@"
            ;;
        ensure)
            ensure_label "$@"
            ;;
        ensure-multiple)
            ensure_labels "$@"
            ;;
        standard)
            create_standard_labels
            ;;
        validate)
            validate_labels "$@"
            ;;
        help|*)
            cat <<EOF
Label Management Helper Script

Usage: $0 <command> [options]

Commands:
  exists <label>                     Check if label exists
  ensure <label> [color] [desc]      Create label if it doesn't exist
  ensure-multiple <label1,label2,..> Create multiple labels (comma-separated)
  standard                           Create standard label set
  validate <label1> <label2> ...     Check if all labels exist
  help                               Show this help

Examples:
  $0 exists "bug"
  $0 ensure "plugin" "7057ff" "Claude Code plugin"
  $0 ensure-multiple "bug,enhancement,plugin"
  $0 standard
  $0 validate "bug" "enhancement"

EOF
            ;;
    esac
}

# Run main if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
