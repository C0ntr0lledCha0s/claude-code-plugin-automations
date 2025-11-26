#!/bin/bash

# SessionStart hook for claude.ai/code
# Installs npm dependencies for validation scripts and development tools

# Debug log file location
DEBUG_LOG="${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/session-start-debug.log"

# Function to log debug messages
debug_log() {
  local timestamp=$(date '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo "timestamp-unavailable")
  echo "[$timestamp] $1" >> "$DEBUG_LOG" 2>/dev/null || true
}

# Function to output JSON and exit
output_json_and_exit() {
  local decision="$1"
  local message="${2:-}"
  if [ -n "$message" ]; then
    # Use printf and tr to avoid CRLF issues on Windows
    printf '{"decision": "%s", "reason": "%s"}\n' "$decision" "$message" | tr -d '\r'
  else
    printf '{"decision": "%s"}\n' "$decision" | tr -d '\r'
  fi
  exit 0
}

# Clear previous debug log and start fresh
mkdir -p "$(dirname "$DEBUG_LOG")" 2>/dev/null || true
echo "=== SessionStart Hook Debug Log ===" > "$DEBUG_LOG" 2>/dev/null || true
debug_log "Hook script started"

# Log environment information
debug_log "=== Environment Information ==="
debug_log "Shell: ${SHELL:-not set} (BASH_VERSION: ${BASH_VERSION:-unknown})"
debug_log "PWD: $(pwd)"
debug_log "USER: ${USER:-${USERNAME:-unknown}}"
debug_log "HOME: ${HOME:-unknown}"
debug_log "OS: ${OSTYPE:-unknown}"
debug_log "CLAUDE_PROJECT_DIR: ${CLAUDE_PROJECT_DIR:-NOT SET}"
debug_log "CLAUDE_CODE_REMOTE: ${CLAUDE_CODE_REMOTE:-NOT SET}"

# Check if running on Windows (Git Bash, MSYS, etc.)
debug_log "=== Platform Detection ==="
if [[ "${OSTYPE:-}" == "msys" ]] || [[ "${OSTYPE:-}" == "cygwin" ]] || [[ -n "${MSYSTEM:-}" ]]; then
  debug_log "Detected Windows environment (MSYS/Cygwin/Git Bash)"
  debug_log "MSYSTEM: ${MSYSTEM:-not set}"
fi

# Only run full setup in Claude Code web environment
debug_log "=== Checking Remote Environment ==="
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  debug_log "Not in Claude Code remote environment, running lightweight checks"

  # Lightweight dependency checks for local environments
  debug_log "=== Local Environment Dependency Checks ==="

  # Check jq (required for github-workflows plugin)
  if command -v jq &> /dev/null; then
    debug_log "jq available: $(jq --version 2>&1 || echo 'unknown')"
  else
    debug_log "WARNING: jq not found - install with: bash github-workflows/scripts/ensure-dependencies.sh"
  fi

  # Check python3 (required for validation scripts)
  if command -v python3 &> /dev/null; then
    debug_log "python3 available: $(python3 --version 2>&1 || echo 'unknown')"
  else
    debug_log "WARNING: python3 not found"
  fi

  debug_log "Outputting approval JSON and exiting"
  output_json_and_exit "approve" "Local environment - checks complete"
fi

debug_log "=== Running Full Setup (Remote Environment) ==="

# Navigate to project root
debug_log "Attempting to change to project directory: $CLAUDE_PROJECT_DIR"
if ! cd "$CLAUDE_PROJECT_DIR" 2>&1; then
  debug_log "ERROR: Failed to cd to $CLAUDE_PROJECT_DIR"
  output_json_and_exit "approve" "Failed to change directory but continuing"
fi
debug_log "Successfully changed to: $(pwd)"

# Check if node_modules exists and npm is available
debug_log "=== Checking npm Dependencies ==="
debug_log "Checking for node_modules directory..."
if [ ! -d "node_modules" ]; then
  debug_log "node_modules not found, installing dependencies..."

  # Check if npm is available
  if ! command -v npm &> /dev/null; then
    debug_log "ERROR: npm command not found"
    output_json_and_exit "approve" "npm not found - skipping dependency install"
  fi

  debug_log "Running npm install..."
  if npm install --quiet --no-progress 2>&1 | tee -a "$DEBUG_LOG"; then
    debug_log "npm install completed successfully"
  else
    debug_log "WARNING: npm install may have failed"
  fi
else
  debug_log "node_modules directory already exists"
fi

# Verify Python 3 is available (needed for validation scripts)
debug_log "=== Checking Python 3 ==="
if command -v python3 &> /dev/null; then
  py_version=$(python3 --version 2>&1 || echo "unknown")
  debug_log "Python 3 available: $py_version"
else
  debug_log "WARNING: Python 3 not found"
fi

# Check jq availability (needed for github-workflows plugin shell scripts)
debug_log "=== Checking jq ==="
if command -v jq &> /dev/null; then
  jq_version=$(jq --version 2>&1 || echo "unknown")
  debug_log "jq available: $jq_version"
else
  debug_log "WARNING: jq not found - some github-workflows features may not work"
  debug_log "To install jq, run: bash github-workflows/scripts/ensure-dependencies.sh"
fi

# Verify marketplace plugins are configured
debug_log "=== Checking Plugin Configuration ==="
if [ -f ".claude/settings.json" ]; then
  debug_log "settings.json found"
else
  debug_log "WARNING: .claude/settings.json not found"
fi

debug_log "=== Setup Complete ==="
debug_log "Hook completed successfully"

# Output final success JSON
output_json_and_exit "approve" "Environment setup complete"
