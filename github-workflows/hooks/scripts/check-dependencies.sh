#!/bin/bash
# Check and install required dependencies for github-workflows plugin
# SessionStart hook - MUST output valid JSON to stdout

set -euo pipefail

# Function to output JSON and exit
output_json() {
    local decision="$1"
    local reason="${2:-}"
    if [ -n "$reason" ]; then
        printf '{"decision": "%s", "reason": "%s"}\n' "$decision" "$reason" | tr -d '\r'
    else
        printf '{"decision": "%s"}\n' "$decision" | tr -d '\r'
    fi
}

check_and_install_jq() {
    if command -v jq &> /dev/null; then
        return 0
    fi

    # All informational output goes to stderr, not stdout
    echo "jq not found. Attempting to install..." >&2

    # Detect OS and install
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            if brew install jq >&2 2>&1; then
                echo "Success: jq installed via Homebrew" >&2
                return 0
            fi
        else
            echo "Warning: Homebrew not found. Install jq manually: brew install jq" >&2
            return 1
        fi
    elif [[ -f /etc/debian_version ]]; then
        # Debian/Ubuntu/WSL
        if sudo apt-get update -qq >&2 2>&1 && sudo apt-get install -y -qq jq >&2 2>&1; then
            echo "Success: jq installed via apt" >&2
            return 0
        fi
    elif [[ -f /etc/fedora-release ]] || [[ -f /etc/redhat-release ]]; then
        # Fedora/RHEL
        if sudo dnf install -y jq >&2 2>&1; then
            echo "Success: jq installed via dnf" >&2
            return 0
        fi
    elif [[ -f /etc/arch-release ]]; then
        # Arch
        if sudo pacman -S --noconfirm jq >&2 2>&1; then
            echo "Success: jq installed via pacman" >&2
            return 0
        fi
    else
        echo "Warning: Could not auto-install jq. Please install manually for your OS." >&2
        return 1
    fi
    return 1
}

# Run checks and output JSON result
if check_and_install_jq; then
    output_json "approve" "Dependencies checked successfully"
else
    # Even if jq install fails, approve the session but warn
    output_json "approve" "jq not available - some features may be limited"
fi
