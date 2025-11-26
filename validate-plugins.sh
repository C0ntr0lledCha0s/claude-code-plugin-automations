#!/bin/bash
# Comprehensive plugin validation script
# Validates all plugins in the repository

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🔍 Validating all plugins in the repository..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

# Function to validate a plugin
validate_plugin() {
    local plugin_dir="$1"
    local plugin_name=$(basename "$plugin_dir")

    echo "📦 Validating plugin: $plugin_name"
    echo "   Location: $plugin_dir"

    # Check if plugin.json exists
    if [ ! -f "$plugin_dir/.claude-plugin/plugin.json" ]; then
        echo -e "   ${RED}✗${NC} Missing plugin.json manifest"
        ERRORS=$((ERRORS + 1))
        return
    fi

    # Validate plugin.json syntax
    if ! python3 -m json.tool "$plugin_dir/.claude-plugin/plugin.json" >/dev/null 2>&1; then
        echo -e "   ${RED}✗${NC} Invalid JSON in plugin.json"
        ERRORS=$((ERRORS + 1))
        return
    fi

    echo -e "   ${GREEN}✓${NC} plugin.json exists and is valid JSON"

    # Validate agents
    echo "   [DEBUG] Checking for agents directory: $plugin_dir/agents"
    if [ -d "$plugin_dir/agents" ]; then
        echo "   [DEBUG] Agents directory exists, looking for *.md files"
        for agent in "$plugin_dir/agents"/*.md; do
            echo "   [DEBUG] Processing: $agent"
            if [ -f "$agent" ]; then
                agent_name=$(basename "$agent")
                # Run validation and capture output
                # Temporarily disable exit-on-error to capture validation output
                set +e
                validation_output=$(python3 agent-builder/skills/building-agents/scripts/validate-agent.py "$agent" 2>&1)
                validation_exit_code=$?
                set -e

                if [ $validation_exit_code -eq 0 ]; then
                    echo -e "   ${GREEN}✓${NC} Agent: $agent_name"
                else
                    echo -e "   ${RED}✗${NC} Agent: $agent_name (validation failed with exit code $validation_exit_code)"
                    echo "      Validation output: $validation_output"
                    ERRORS=$((ERRORS + 1))
                fi
            fi
        done
    fi

    # Validate hooks
    if [ -f "$plugin_dir/hooks/hooks.json" ]; then
        if python3 agent-builder/skills/building-hooks/scripts/validate-hooks.py "$plugin_dir/hooks/hooks.json" >/dev/null 2>&1; then
            echo -e "   ${GREEN}✓${NC} hooks.json is valid"
        else
            echo -e "   ${RED}✗${NC} hooks.json validation failed"
            ERRORS=$((ERRORS + 1))
        fi
    fi

    # Validate skills
    if [ -d "$plugin_dir/skills" ]; then
        for skill_dir in "$plugin_dir/skills"/*; do
            if [ -d "$skill_dir" ] && [ -f "$skill_dir/SKILL.md" ]; then
                skill_name=$(basename "$skill_dir")
                if python3 agent-builder/skills/building-skills/scripts/validate-skill.py "$skill_dir" >/dev/null 2>&1; then
                    echo -e "   ${GREEN}✓${NC} Skill: $skill_name"
                else
                    echo -e "   ${YELLOW}⚠${NC}  Skill: $skill_name (validation warnings)"
                    WARNINGS=$((WARNINGS + 1))
                fi
            fi
        done
    fi

    # Validate commands
    if [ -d "$plugin_dir/commands" ]; then
        for command in "$plugin_dir/commands"/*.md; do
            if [ -f "$command" ]; then
                command_name=$(basename "$command")
                if python3 agent-builder/skills/building-commands/scripts/validate-command.py "$command" >/dev/null 2>&1; then
                    echo -e "   ${GREEN}✓${NC} Command: $command_name"
                else
                    echo -e "   ${RED}✗${NC} Command: $command_name (validation failed)"
                    ERRORS=$((ERRORS + 1))
                fi
            fi
        done
    fi

    echo ""
}

# Find all plugin directories
for plugin_dir in */; do
    # Skip directories that don't look like plugins
    if [ -d "$plugin_dir/.claude-plugin" ]; then
        validate_plugin "$plugin_dir"
    fi
done

# Validate marketplace.json
echo "📋 Validating marketplace.json..."
if [ -f ".claude-plugin/marketplace.json" ]; then
    if python3 -m json.tool .claude-plugin/marketplace.json >/dev/null 2>&1; then
        echo -e "   ${GREEN}✓${NC} marketplace.json is valid JSON"

        # Check that all plugins in marketplace exist
        while IFS= read -r plugin_source; do
            plugin_dir="${plugin_source#./}"
            # Remove carriage return if present (Windows line endings)
            plugin_dir="${plugin_dir%$'\r'}"
            if [ ! -d "$plugin_dir" ]; then
                echo -e "   ${RED}✗${NC} Plugin directory not found: $plugin_dir"
                ERRORS=$((ERRORS + 1))
            fi
        done < <(python3 -c "import json; data=json.load(open('.claude-plugin/marketplace.json', encoding='utf-8')); print('\n'.join([p['source'] for p in data.get('plugins', [])]))")
    else
        echo -e "   ${RED}✗${NC} marketplace.json is invalid JSON"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "   ${RED}✗${NC} marketplace.json not found"
    ERRORS=$((ERRORS + 1))
fi

# Run agent invocation tests
echo ""
echo "🧪 Running agent invocation tests..."
if [ -f "tests/run_tests.py" ]; then
    if python3 tests/run_tests.py 2>&1; then
        echo -e "   ${GREEN}✓${NC} Agent invocation tests passed"
    else
        echo -e "   ${RED}✗${NC} Agent invocation tests failed"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "   ${YELLOW}⚠${NC}  tests/run_tests.py not found, skipping tests"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""
echo "════════════════════════════════════════"
echo "Validation Summary:"
echo "════════════════════════════════════════"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ All validations passed!${NC}"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠ Validation completed with $WARNINGS warning(s)${NC}"
    exit 0
else
    echo -e "${RED}✗ Validation failed with $ERRORS error(s) and $WARNINGS warning(s)${NC}"
    exit 1
fi
