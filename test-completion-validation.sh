#!/bin/bash

# Test script to validate install-agents completion

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "Testing install-agents bash completion..."
echo

# Source the completion
source /home/bryan/agentgen/install-agents-completion.bash

# Function to test completion
test_completion() {
    local test_string="$1"
    local description="$2"

    # Set up COMP_WORDS and COMP_CWORD to simulate tab completion
    IFS=' ' read -ra COMP_WORDS <<< "$test_string"
    COMP_CWORD=$((${#COMP_WORDS[@]} - 1))

    # Clear COMPREPLY
    COMPREPLY=()

    # Call the completion function
    _install_agents_completion

    # Check results
    if [ ${#COMPREPLY[@]} -gt 0 ]; then
        echo -e "${GREEN}✓${NC} $description"
        echo "  Found ${#COMPREPLY[@]} completions"
        # Show first 5 completions
        for i in {0..4}; do
            [ ${i} -lt ${#COMPREPLY[@]} ] && echo "    - ${COMPREPLY[$i]}"
        done
        [ ${#COMPREPLY[@]} -gt 5 ] && echo "    ... and $((${#COMPREPLY[@]} - 5)) more"
    else
        echo -e "${YELLOW}⚠${NC} $description"
        echo "  No completions found"
    fi
    echo
}

# Test various completion scenarios
echo "=== Testing Option Completions ==="
test_completion "install-agents --" "Options starting with --"
test_completion "install-agents --pro" "Options starting with --pro"
test_completion "install-agents --list" "Options starting with --list"

echo "=== Testing Profile Completions ==="
test_completion "install-agents --profile " "Available profiles after --profile"
test_completion "install-agents --profile dev" "Profiles starting with 'dev'"

echo "=== Testing Agent Name Completions ==="
# Note: Agent completion might be slow due to find command
echo "Testing agent completions (this might take a moment)..."
test_completion "install-agents --global " "Agent names in global mode"
test_completion "install-agents code" "Agents starting with 'code'"

echo "=== Testing Directory Completions ==="
test_completion "install-agents --project " "Directory completion after --project"
test_completion "install-agents --project /home/" "Directory completion with path"

echo "=== Testing Show Profile Completions ==="
test_completion "install-agents --show-profile " "Profiles for --show-profile"

echo -e "${GREEN}✓${NC} Completion testing complete!"
echo
echo "To manually test in your shell:"
echo "  1. Run: source /home/bryan/agentgen/install-agents-completion.bash"
echo "  2. Type: install-agents <TAB>"
echo "  3. Try various options and arguments"