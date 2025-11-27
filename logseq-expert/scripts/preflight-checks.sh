#!/bin/bash
#
# Logseq Preflight Checks
#
# Validates environment before running Logseq operations.
# Returns 0 if all checks pass, non-zero otherwise.
#
# Usage:
#   ./preflight-checks.sh [mode]
#
# Modes:
#   all     - Run all checks (default)
#   quick   - Quick checks only (config exists, basic connectivity)
#   strict  - All checks must pass
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"

# Configuration
MODE="${1:-all}"
ERRORS=0
WARNINGS=0

# Helper functions
info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    ((WARNINGS++)) || true
}

error() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((ERRORS++)) || true
}

# Check functions
check_config_exists() {
    local config_path=".claude/logseq-expert/env.json"

    if [[ -f "$config_path" ]]; then
        success "Configuration file exists"
        return 0
    else
        error "Configuration not found. Run: python $SCRIPT_DIR/init-environment.py"
        return 1
    fi
}

check_python() {
    if command -v python3 &> /dev/null; then
        local version=$(python3 --version 2>&1 | cut -d' ' -f2)
        success "Python 3 available ($version)"
        return 0
    else
        error "Python 3 not found"
        return 1
    fi
}

check_node() {
    if command -v node &> /dev/null; then
        local version=$(node --version)
        success "Node.js available ($version)"
        return 0
    else
        warn "Node.js not found (needed for MCP server)"
        return 0  # Warning only
    fi
}

check_logseq_api_token() {
    if [[ -n "$LOGSEQ_API_TOKEN" ]]; then
        success "LOGSEQ_API_TOKEN is set"
        return 0
    else
        # Check if token is in config
        local config_path=".claude/logseq-expert/env.json"
        if [[ -f "$config_path" ]]; then
            local token=$(python3 -c "import json; print(json.load(open('$config_path')).get('http',{}).get('token',''))" 2>/dev/null)
            if [[ -n "$token" && "$token" != '${LOGSEQ_API_TOKEN}' ]]; then
                success "API token found in config"
                return 0
            fi
        fi
        warn "LOGSEQ_API_TOKEN not set (HTTP API will not work)"
        return 0  # Warning only
    fi
}

check_http_connectivity() {
    local url="${LOGSEQ_API_URL:-http://127.0.0.1:12315}"
    local host=$(echo "$url" | sed -E 's|https?://([^:/]+).*|\1|')
    local port=$(echo "$url" | sed -E 's|.*:([0-9]+).*|\1|')
    port="${port:-12315}"

    # Quick socket check
    if timeout 2 bash -c "echo >/dev/tcp/$host/$port" 2>/dev/null; then
        success "Logseq HTTP API reachable at $host:$port"
        return 0
    else
        warn "Cannot reach Logseq at $host:$port (is Logseq running?)"
        return 0  # Warning only
    fi
}

check_cli_available() {
    if command -v logseq &> /dev/null; then
        success "Logseq CLI available"
        return 0
    elif command -v npx &> /dev/null; then
        # Check if @logseq/cli is available via npx (don't actually run it)
        success "npx available (can use @logseq/cli)"
        return 0
    else
        warn "Logseq CLI not found"
        return 0  # Warning only
    fi
}

check_mcp_server() {
    local mcp_path="$PLUGIN_DIR/servers/logseq-mcp/build/index.js"

    if [[ -f "$mcp_path" ]]; then
        success "MCP server built"
        return 0
    else
        warn "MCP server not built (run: npm run build in servers/logseq-mcp/)"
        return 0  # Warning only
    fi
}

check_graph_path() {
    local config_path=".claude/logseq-expert/env.json"

    if [[ -f "$config_path" ]]; then
        local graph_path=$(python3 -c "import json; print(json.load(open('$config_path')).get('cli',{}).get('graphPath',''))" 2>/dev/null)

        if [[ -n "$graph_path" && -d "$graph_path" ]]; then
            success "Graph path exists: $graph_path"
            return 0
        elif [[ -n "$graph_path" ]]; then
            warn "Graph path not found: $graph_path"
        else
            info "No graph path configured"
        fi
    fi
    return 0  # Not critical
}

# Main execution
main() {
    echo -e "\n${BLUE}=== Logseq Preflight Checks ===${NC}\n"
    echo "Mode: $MODE"
    echo ""

    case "$MODE" in
        quick)
            check_config_exists
            check_http_connectivity
            ;;
        strict)
            check_config_exists || true
            check_python || true
            check_node || true
            check_logseq_api_token || true
            check_http_connectivity || true
            check_cli_available || true
            check_mcp_server || true
            check_graph_path || true

            # In strict mode, warnings are errors
            ERRORS=$((ERRORS + WARNINGS))
            ;;
        all|*)
            check_config_exists || true
            check_python || true
            check_node || true
            check_logseq_api_token || true
            check_http_connectivity || true
            check_cli_available || true
            check_mcp_server || true
            check_graph_path || true
            ;;
    esac

    echo ""
    echo -e "${BLUE}=== Summary ===${NC}"

    if [[ $ERRORS -gt 0 ]]; then
        echo -e "${RED}$ERRORS error(s), $WARNINGS warning(s)${NC}"
        exit 1
    elif [[ $WARNINGS -gt 0 ]]; then
        echo -e "${YELLOW}$WARNINGS warning(s)${NC}"
        exit 0
    else
        echo -e "${GREEN}All checks passed${NC}"
        exit 0
    fi
}

main
