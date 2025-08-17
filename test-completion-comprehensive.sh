#!/bin/bash

# Comprehensive test of install-agents completion

source "$(dirname "$0")/install-agents-completion.bash"

echo "=== Comprehensive install-agents Completion Test ==="

# Test helper function
test_completion() {
    local description="$1"
    shift
    export COMP_WORDS=("$@")
    export COMP_CWORD=$((${#COMP_WORDS[@]} - 1))
    
    echo
    echo "Test: $description"
    echo "Command: ${COMP_WORDS[*]}"
    echo "Completing: '${COMP_WORDS[$COMP_CWORD]}'"
    
    _install_agents_completion
    
    if [[ ${#COMPREPLY[@]} -gt 0 ]]; then
        echo "Results (first 3): ${COMPREPLY[*]:0:3}..."
        echo "Total completions: ${#COMPREPLY[@]}"
    else
        echo "No completions"
    fi
}

# NEW DEFAULTS TESTS

# Test 1: NEW DEFAULT - Simple agent completion (current directory, symlinks)
test_completion "NEW DEFAULT: Simple agent completion" "install-agents" ""

# Test 2: NEW DEFAULT - Profile completion (current directory, symlinks)  
test_completion "NEW DEFAULT: Profile completion" "install-agents" "--profile" ""

# Test 3: NEW DEFAULT - Partial agent name (current directory)
test_completion "NEW DEFAULT: Partial agent name" "install-agents" "code"

# STANDARD TESTS

# Test 4: Basic options
test_completion "Basic options with --" "install-agents" "--"

# Test 5: Partial profile completion
test_completion "Partial profile name" "install-agents" "--profile" "dev"

# Test 6: Agent names after explicit target path (legacy)
test_completion "Agent names after target path (legacy)" "install-agents" "/tmp" ""

# Test 7: Agent names with partial match (legacy)
test_completion "Partial agent name (legacy)" "install-agents" "/tmp" "code"

# Test 8: Symlink global mode agent completion
test_completion "Symlink global mode agents" "install-agents" "--global" ""

# Test 9: Symlink project mode
test_completion "Symlink project completion" "install-agents" "--project" ""

# Test 10: Directory completion after --project
test_completion "Directory after --project" "install-agents" "--project" "/ho"

# Test 11: Options after explicit --symlink (redundant since it's default)
test_completion "Options after --symlink" "install-agents" "--symlink" "--"

# Test 12: No completion for --all mode
test_completion "No agents with --all" "install-agents" "--all" ""

# Test 13: No completion for --profile mode
test_completion "No agents with --profile" "install-agents" "--profile" "core" ""

# Test 14: Health check (no path needed, symlinks default)
test_completion "Health check mode" "install-agents" "--health" ""

# Test 15: Legacy copy mode
test_completion "Copy mode (legacy)" "install-agents" "--copy" "/tmp" ""

echo
echo "=== Comprehensive test completed ==="