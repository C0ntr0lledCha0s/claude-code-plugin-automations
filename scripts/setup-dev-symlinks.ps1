# Setup Development Symlinks for Claude Code Plugins
# Run this script as Administrator to create symlinks in ~/.claude/plugins/
# This makes CLAUDE_PLUGIN_ROOT work correctly during development

param(
    [switch]$Remove,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

# Plugin source directory
$PluginSourceDir = Split-Path -Parent $PSScriptRoot

# Target directory for symlinks
$ClaudePluginsDir = Join-Path $env:USERPROFILE ".claude\plugins"

# Plugins to symlink
$Plugins = @(
    "claude-component-builder",
    "self-improvement",
    "github-workflows",
    "research-agent",
    "project-manager"
)

# Check for admin privileges
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script requires Administrator privileges to create symlinks." -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator and try again." -ForegroundColor Yellow
    exit 1
}

# Create plugins directory if it doesn't exist
if (-not (Test-Path $ClaudePluginsDir)) {
    Write-Host "Creating $ClaudePluginsDir..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $ClaudePluginsDir -Force | Out-Null
}

foreach ($plugin in $Plugins) {
    $sourcePath = Join-Path $PluginSourceDir $plugin
    $targetPath = Join-Path $ClaudePluginsDir $plugin

    # Check if source exists
    if (-not (Test-Path $sourcePath)) {
        Write-Host "SKIP: $plugin - source not found at $sourcePath" -ForegroundColor Yellow
        continue
    }

    if ($Remove) {
        # Remove symlink
        if (Test-Path $targetPath) {
            Remove-Item $targetPath -Force
            Write-Host "REMOVED: $targetPath" -ForegroundColor Red
        } else {
            Write-Host "SKIP: $plugin - symlink doesn't exist" -ForegroundColor Yellow
        }
    } else {
        # Create symlink
        if (Test-Path $targetPath) {
            if ($Force) {
                Remove-Item $targetPath -Force -Recurse
                Write-Host "REMOVED existing: $targetPath" -ForegroundColor Yellow
            } else {
                Write-Host "SKIP: $plugin - already exists at $targetPath (use -Force to replace)" -ForegroundColor Yellow
                continue
            }
        }

        New-Item -ItemType SymbolicLink -Path $targetPath -Target $sourcePath | Out-Null
        Write-Host "CREATED: $targetPath -> $sourcePath" -ForegroundColor Green
    }
}

Write-Host ""
if ($Remove) {
    Write-Host "Symlinks removed. Plugins will no longer be available globally." -ForegroundColor Cyan
} else {
    Write-Host "Setup complete! CLAUDE_PLUGIN_ROOT will now be set correctly." -ForegroundColor Green
    Write-Host "Restart Claude Code for changes to take effect." -ForegroundColor Cyan
}
