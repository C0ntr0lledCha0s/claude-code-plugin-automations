#!/bin/bash
set -eu

# SessionStart hook for claude.ai/code
# Installs npm dependencies for validation scripts and development tools

# Only run in Claude Code web environment
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

echo "🚀 Setting up Claude Code Plugin Automations environment..."

# Navigate to project root
cd "$CLAUDE_PROJECT_DIR"

# Check if node_modules exists and npm is available
if [ ! -d "node_modules" ]; then
  echo "📦 Installing npm dependencies..."

  # Install dependencies
  # Using npm install (not npm ci) to take advantage of container caching
  npm install --quiet --no-progress

  echo "✅ npm dependencies installed successfully"
else
  echo "✅ npm dependencies already installed"
fi

# Verify Python 3 is available (needed for validation scripts)
if command -v python3 &> /dev/null; then
  echo "✅ Python 3 is available"
else
  echo "⚠️  Python 3 not found - validation scripts may not work"
fi

# Verify marketplace plugins are configured
if [ -f ".claude/settings.json" ]; then
  echo "✅ Marketplace plugins configured"
else
  echo "⚠️  .claude/settings.json not found"
fi

echo "🎉 Environment setup complete!"
echo ""
echo "Available plugins:"
echo "  • agent-builder - Meta-agent for building Claude Code extensions"
echo "  • self-improvement - Self-critique and quality analysis"
echo "  • github-workflows - GitHub automation tools"
echo ""
echo "Try: npm run validate:quick to validate all plugins"
