#!/usr/bin/env bash
# Ensure required dependencies are installed for github-workflows plugin
# Handles: jq, python3, graphql tools

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

# Detect operating system
detect_os() {
    case "$(uname -s)" in
        Linux*)
            if grep -qi microsoft /proc/version 2>/dev/null; then
                echo "wsl"
            elif [ -f /etc/debian_version ]; then
                echo "debian"
            elif [ -f /etc/redhat-release ]; then
                echo "redhat"
            elif [ -f /etc/arch-release ]; then
                echo "arch"
            else
                echo "linux"
            fi
            ;;
        Darwin*)
            echo "macos"
            ;;
        MINGW*|MSYS*|CYGWIN*)
            echo "windows"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

# Check if jq is installed
check_jq() {
    if command -v jq >/dev/null 2>&1; then
        return 0
    fi
    return 1
}

# Install jq based on OS
install_jq() {
    local os
    os=$(detect_os)

    info "Installing jq JSON processor..."

    case "$os" in
        debian|wsl)
            if sudo apt-get update >/dev/null 2>&1 && sudo apt-get install -y jq >/dev/null 2>&1; then
                success "jq installed via apt"
                return 0
            fi
            ;;
        redhat)
            if command -v dnf >/dev/null 2>&1; then
                if sudo dnf install -y jq >/dev/null 2>&1; then
                    success "jq installed via dnf"
                    return 0
                fi
            else
                if sudo yum install -y jq >/dev/null 2>&1; then
                    success "jq installed via yum"
                    return 0
                fi
            fi
            ;;
        arch)
            if sudo pacman -S --noconfirm jq >/dev/null 2>&1; then
                success "jq installed via pacman"
                return 0
            fi
            ;;
        macos)
            if ! command -v brew >/dev/null 2>&1; then
                error "Homebrew not found. Install from: https://brew.sh"
                return 1
            fi
            if brew install jq >/dev/null 2>&1; then
                success "jq installed via Homebrew"
                return 0
            fi
            ;;
        windows)
            warn "Windows detected. Please install jq manually:"
            info "  Download from: https://stedolan.github.io/jq/download/"
            info "  Or use: choco install jq"
            return 1
            ;;
        *)
            error "Unsupported OS: $os"
            info "Please install jq manually: https://stedolan.github.io/jq/download/"
            return 1
            ;;
    esac

    error "Failed to install jq"
    return 1
}

# Check if python3 is installed
check_python() {
    if command -v python3 >/dev/null 2>&1; then
        return 0
    fi
    return 1
}

# Install python3 based on OS
install_python() {
    local os
    os=$(detect_os)

    info "Installing Python 3..."

    case "$os" in
        debian|wsl)
            if sudo apt-get update >/dev/null 2>&1 && sudo apt-get install -y python3 >/dev/null 2>&1; then
                success "Python 3 installed via apt"
                return 0
            fi
            ;;
        redhat)
            if command -v dnf >/dev/null 2>&1; then
                if sudo dnf install -y python3 >/dev/null 2>&1; then
                    success "Python 3 installed via dnf"
                    return 0
                fi
            else
                if sudo yum install -y python3 >/dev/null 2>&1; then
                    success "Python 3 installed via yum"
                    return 0
                fi
            fi
            ;;
        arch)
            if sudo pacman -S --noconfirm python >/dev/null 2>&1; then
                success "Python 3 installed via pacman"
                return 0
            fi
            ;;
        macos)
            if brew install python3 >/dev/null 2>&1; then
                success "Python 3 installed via Homebrew"
                return 0
            fi
            ;;
        *)
            error "Unsupported OS: $os"
            info "Please install Python 3 manually: https://www.python.org/downloads/"
            return 1
            ;;
    esac

    error "Failed to install Python 3"
    return 1
}

# Ensure jq is available
ensure_jq() {
    if check_jq; then
        success "jq is installed"
        return 0
    else
        warn "jq is not installed"
        if [ "${AUTO_INSTALL:-true}" = "true" ]; then
            if install_jq; then
                return 0
            else
                error "jq installation failed"
                info "Install manually: https://stedolan.github.io/jq/download/"
                return 1
            fi
        else
            info "Install jq: https://stedolan.github.io/jq/download/"
            return 1
        fi
    fi
}

# Ensure python3 is available
ensure_python() {
    if check_python; then
        success "Python 3 is installed"
        return 0
    else
        warn "Python 3 is not installed"
        if [ "${AUTO_INSTALL:-true}" = "true" ]; then
            if install_python; then
                return 0
            else
                error "Python 3 installation failed"
                info "Install manually: https://www.python.org/downloads/"
                return 1
            fi
        else
            info "Install Python 3: https://www.python.org/downloads/"
            return 1
        fi
    fi
}

# Main function - check all dependencies
main() {
    local auto_install="${1:-true}"
    local check_only="${2:-false}"

    export AUTO_INSTALL="$auto_install"

    local all_ok=true

    info "Checking dependencies..."

    # Check jq
    if ! ensure_jq; then
        all_ok=false
    fi

    # Check python3
    if ! ensure_python; then
        all_ok=false
    fi

    if [ "$all_ok" = "true" ]; then
        success "All dependencies are satisfied"
        return 0
    else
        error "Some dependencies are missing"
        return 1
    fi
}

# Run if executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi
