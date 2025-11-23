#!/bin/bash
# Check and install required dependencies for github-workflows plugin

check_and_install_jq() {
    if command -v jq &> /dev/null; then
        return 0
    fi

    echo "jq not found. Attempting to install..."

    # Detect OS and install
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install jq && echo "Success: jq installed via Homebrew" && return 0
        else
            echo "Warning: Homebrew not found. Install jq manually: brew install jq"
            return 1
        fi
    elif [[ -f /etc/debian_version ]]; then
        # Debian/Ubuntu/WSL
        sudo apt-get update -qq && sudo apt-get install -y -qq jq && echo "Success: jq installed via apt" && return 0
    elif [[ -f /etc/fedora-release ]] || [[ -f /etc/redhat-release ]]; then
        # Fedora/RHEL
        sudo dnf install -y jq && echo "Success: jq installed via dnf" && return 0
    elif [[ -f /etc/arch-release ]]; then
        # Arch
        sudo pacman -S --noconfirm jq && echo "Success: jq installed via pacman" && return 0
    else
        echo "Warning: Could not auto-install jq. Please install manually for your OS."
        return 1
    fi
}

# Run checks
check_and_install_jq
