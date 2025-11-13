#!/usr/bin/env bash
# Ensure GitHub CLI is installed and authenticated
# Auto-installs if missing

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

# Minimum required version of gh CLI
MIN_GH_VERSION="2.0.0"

# Check if gh is installed
check_gh_installed() {
    if command -v gh >/dev/null 2>&1; then
        return 0
    fi
    return 1
}

# Parse version string and convert to comparable number
version_to_number() {
    local version="$1"
    # Extract major.minor.patch and convert to comparable number
    # e.g., "2.40.1" -> 2040001
    echo "$version" | awk -F. '{ printf("%d%03d%03d\n", $1, $2, $3) }'
}

# Check if installed gh version meets minimum requirement
check_gh_version() {
    local current_version
    local min_version_num
    local current_version_num

    # Get current version (output format: "gh version 2.40.1 (2024-01-15)")
    current_version=$(gh version 2>/dev/null | head -n1 | awk '{print $3}')

    if [[ -z "$current_version" ]]; then
        warn "Could not determine gh CLI version"
        return 1
    fi

    min_version_num=$(version_to_number "$MIN_GH_VERSION")
    current_version_num=$(version_to_number "$current_version")

    if [[ $current_version_num -lt $min_version_num ]]; then
        warn "GitHub CLI version $current_version is below minimum required version $MIN_GH_VERSION"
        info "Please upgrade: https://github.com/cli/cli/releases"
        return 1
    fi

    return 0
}

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

# Install gh CLI
install_gh_cli() {
    local os
    os=$(detect_os)

    info "Detected OS: $os"
    info "Installing GitHub CLI..."

    case "$os" in
        debian|wsl)
            info "Using apt package manager"
            # Official GitHub CLI installation for Debian/Ubuntu
            if ! curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg >/dev/null 2>&1; then
                error "Failed to add GitHub CLI GPG key"
                return 1
            fi

            sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg

            echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list >/dev/null

            sudo apt update >/dev/null 2>&1
            if sudo apt install -y gh >/dev/null 2>&1; then
                success "GitHub CLI installed successfully"
                return 0
            else
                error "Failed to install GitHub CLI via apt"
                return 1
            fi
            ;;

        redhat)
            info "Using dnf/yum package manager"
            if command -v dnf >/dev/null 2>&1; then
                sudo dnf install -y 'dnf-command(config-manager)' >/dev/null 2>&1
                sudo dnf config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo >/dev/null 2>&1
                if sudo dnf install -y gh >/dev/null 2>&1; then
                    success "GitHub CLI installed successfully"
                    return 0
                fi
            else
                sudo yum-config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo >/dev/null 2>&1
                if sudo yum install -y gh >/dev/null 2>&1; then
                    success "GitHub CLI installed successfully"
                    return 0
                fi
            fi
            error "Failed to install GitHub CLI via dnf/yum"
            return 1
            ;;

        arch)
            info "Using pacman package manager"
            if sudo pacman -S --noconfirm github-cli >/dev/null 2>&1; then
                success "GitHub CLI installed successfully"
                return 0
            else
                error "Failed to install GitHub CLI via pacman"
                return 1
            fi
            ;;

        macos)
            info "Using Homebrew package manager"
            if ! command -v brew >/dev/null 2>&1; then
                error "Homebrew not found. Please install Homebrew first: https://brew.sh"
                return 1
            fi

            if brew install gh >/dev/null 2>&1; then
                success "GitHub CLI installed successfully"
                return 0
            else
                error "Failed to install GitHub CLI via Homebrew"
                return 1
            fi
            ;;

        windows)
            info "Using winget package manager"
            if winget install --id GitHub.cli >/dev/null 2>&1; then
                success "GitHub CLI installed successfully"
                return 0
            else
                error "Failed to install GitHub CLI via winget"
                warn "Try installing manually: https://github.com/cli/cli/releases"
                return 1
            fi
            ;;

        *)
            error "Unsupported operating system: $os"
            info "Please install GitHub CLI manually:"
            info "  https://github.com/cli/cli#installation"
            return 1
            ;;
    esac
}

# Check authentication status
check_gh_auth() {
    if gh auth status >/dev/null 2>&1; then
        return 0
    fi
    return 1
}

# Setup authentication
setup_auth() {
    warn "GitHub CLI is not authenticated"
    info "Starting authentication process..."
    info "Please follow the prompts to authenticate with GitHub"

    if gh auth login; then
        success "Successfully authenticated with GitHub"
        return 0
    else
        error "Authentication failed"
        return 1
    fi
}

# Main function
main() {
    local auto_install="${1:-true}"
    local auto_auth="${2:-false}"

    # Check if gh is installed
    if check_gh_installed; then
        success "GitHub CLI is installed"

        # Check version
        if ! check_gh_version; then
            warn "GitHub CLI version check failed or version is too old"
            info "Current minimum required version: $MIN_GH_VERSION"
            info "Upgrade recommended for best compatibility"
            # Continue anyway (non-blocking warning)
        fi

        # Check authentication
        if check_gh_auth; then
            success "GitHub CLI is authenticated"
            return 0
        else
            warn "GitHub CLI is not authenticated"

            if [ "$auto_auth" = "true" ]; then
                setup_auth
                return $?
            else
                info "Run: gh auth login"
                return 1
            fi
        fi
    else
        warn "GitHub CLI (gh) is not installed"

        if [ "$auto_install" = "true" ]; then
            if install_gh_cli; then
                success "Installation complete"

                # Verify version after installation
                if ! check_gh_version; then
                    warn "Installed version may be outdated"
                    info "Minimum required version: $MIN_GH_VERSION"
                fi

                # Check auth after installation
                if [ "$auto_auth" = "true" ]; then
                    setup_auth
                    return $?
                else
                    info "Run: gh auth login"
                    return 0
                fi
            else
                error "Installation failed"
                info "Please install GitHub CLI manually:"
                info "  https://github.com/cli/cli#installation"
                return 1
            fi
        else
            info "Please install GitHub CLI:"
            info "  https://github.com/cli/cli#installation"
            return 1
        fi
    fi
}

# Run if executed directly
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi
