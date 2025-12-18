#!/bin/bash
# Setup Development Symlinks for Claude Code Plugins
# Creates symlinks in ~/.claude/plugins/ so CLAUDE_PLUGIN_ROOT works correctly

set -euo pipefail

# Get script directory and plugin source
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_SOURCE_DIR="$(dirname "$SCRIPT_DIR")"

# Target directory
CLAUDE_PLUGINS_DIR="$HOME/.claude/plugins"

# Plugins to symlink
PLUGINS=(
    "claude-component-builder"
    "self-improvement"
    "github-workflows"
    "research-agent"
    "project-manager"
)

# Parse arguments
REMOVE=false
FORCE=false
for arg in "$@"; do
    case $arg in
        --remove|-r) REMOVE=true ;;
        --force|-f) FORCE=true ;;
        --help|-h)
            echo "Usage: $0 [--remove] [--force]"
            echo "  --remove, -r  Remove symlinks instead of creating them"
            echo "  --force, -f   Replace existing symlinks/directories"
            exit 0
            ;;
    esac
done

# Create plugins directory if needed
if [[ ! -d "$CLAUDE_PLUGINS_DIR" ]]; then
    echo "Creating $CLAUDE_PLUGINS_DIR..."
    mkdir -p "$CLAUDE_PLUGINS_DIR"
fi

for plugin in "${PLUGINS[@]}"; do
    source_path="$PLUGIN_SOURCE_DIR/$plugin"
    target_path="$CLAUDE_PLUGINS_DIR/$plugin"

    # Check if source exists
    if [[ ! -d "$source_path" ]]; then
        echo "SKIP: $plugin - source not found at $source_path"
        continue
    fi

    if $REMOVE; then
        # Remove symlink
        if [[ -L "$target_path" || -d "$target_path" ]]; then
            rm -rf "$target_path"
            echo "REMOVED: $target_path"
        else
            echo "SKIP: $plugin - symlink doesn't exist"
        fi
    else
        # Create symlink
        if [[ -e "$target_path" ]]; then
            if $FORCE; then
                rm -rf "$target_path"
                echo "REMOVED existing: $target_path"
            else
                echo "SKIP: $plugin - already exists at $target_path (use --force to replace)"
                continue
            fi
        fi

        # Convert Windows path if needed
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
            # Git Bash on Windows - use junction points (no admin required)
            source_path_win=$(cygpath -w "$source_path")
            target_path_win=$(cygpath -w "$target_path")
            cmd //c mklink //j "$target_path_win" "$source_path_win" > /dev/null 2>&1 || {
                echo "ERROR: Failed to create junction for $plugin"
                continue
            }
        else
            ln -s "$source_path" "$target_path"
        fi
        echo "CREATED: $target_path -> $source_path"
    fi
done

echo ""
if $REMOVE; then
    echo "Symlinks removed. Plugins will no longer be available globally."
else
    echo "Setup complete! CLAUDE_PLUGIN_ROOT will now be set correctly."
    echo "Restart Claude Code for changes to take effect."
fi
