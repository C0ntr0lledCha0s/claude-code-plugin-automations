#!/bin/bash
# Comprehensive plugin validation script
# This script calls validate-plugins.sh for full validation of all plugin components

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Call the comprehensive validation script
exec bash "$SCRIPT_DIR/validate-plugins.sh" "$@"
