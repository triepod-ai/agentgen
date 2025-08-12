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

# Test 1: Basic options
test_completion "Basic options with --" "install-agents" "--"

# Test 2: Profile completion
test_completion "Profile names after --profile" "install-agents" "--profile" ""

# Test 3: Partial profile completion
test_completion "Partial profile name" "install-agents" "--profile" "dev"

# Test 4: Agent names after target path
test_completion "Agent names after target path" "install-agents" "/tmp" ""

# Test 5: Agent names with partial match
test_completion "Partial agent name" "install-agents" "/tmp" "code"

# Test 6: Symlink global mode agent completion
test_completion "Symlink global mode agents" "install-agents" "--symlink" "--global" ""

# Test 7: Symlink project mode
test_completion "Symlink project completion" "install-agents" "--symlink" "--project" ""

# Test 8: Directory completion after --project
test_completion "Directory after --project" "install-agents" "--symlink" "--project" "/ho"

# Test 9: Options after --symlink
test_completion "Options after --symlink" "install-agents" "--symlink" "--"

# Test 10: No completion for --all mode
test_completion "No agents with --all" "install-agents" "/tmp" "--all" ""

# Test 11: No completion for --profile mode
test_completion "No agents with --profile" "install-agents" "/tmp" "--profile" "core" ""

# Test 12: Health check (no path needed)
test_completion "Health check mode" "install-agents" "--symlink" "--health" ""

echo
echo "=== Comprehensive test completed ==="