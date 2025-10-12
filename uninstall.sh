#!/bin/bash
# AgentGen Global Uninstallation Script
# Removes globally installed install-agents command

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

BIN_DIR="${HOME}/bin"
WRAPPER_PATH="${BIN_DIR}/install-agents"
COMPLETION_DIR="${HOME}/.bash_completion.d"
COMPLETION_PATH="${COMPLETION_DIR}/install-agents-completion.bash"

echo "AgentGen Global Uninstallation"
echo "==============================="
echo ""

REMOVED=0

# Remove global wrapper
if [[ -f "$WRAPPER_PATH" ]]; then
    echo "Removing global wrapper from ${WRAPPER_PATH}..."
    rm -f "$WRAPPER_PATH"
    echo -e "${GREEN}✓${NC} Global wrapper removed"
    REMOVED=1
else
    echo -e "${YELLOW}⚠${NC}  No global wrapper found at ${WRAPPER_PATH}"
fi

# Remove bash completion
if [[ -f "$COMPLETION_PATH" ]]; then
    read -p "Remove bash completion? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -f "$COMPLETION_PATH"
        echo -e "${GREEN}✓${NC} Bash completion removed"
        REMOVED=1
    fi
fi

echo ""
if [[ $REMOVED -eq 1 ]]; then
    echo -e "${GREEN}Uninstallation complete!${NC}"
else
    echo "Nothing to uninstall."
fi

echo ""
echo "Note: The agentgen repository at $(dirname "${BASH_SOURCE[0]}") was not removed."
echo "You can delete it manually if desired."
