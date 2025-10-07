#!/bin/bash

# Test script for install-agents completion

# Source the completion
source "$(dirname "$0")/install-agents-completion.bash"

echo "Testing install-agents bash completion..."

# Test 1: Profile completion
echo
echo "Test 1: Profile name completion after --profile"
export COMP_WORDS=("install-agents" "--profile" "")
export COMP_CWORD=2
_install_agents_completion
echo "Available profiles: ${COMPREPLY[*]}"

# Test 2: Option completion
echo
echo "Test 2: Option completion with --"
export COMP_WORDS=("install-agents" "--")
export COMP_CWORD=1
_install_agents_completion
echo "Available options (first 10): ${COMPREPLY[*]:0:10}"

# Test 3: Partial profile completion
echo
echo "Test 3: Partial profile completion 'dev'"
export COMP_WORDS=("install-agents" "--profile" "dev")
export COMP_CWORD=2
_install_agents_completion
echo "Matching profiles: ${COMPREPLY[*]}"

# Test 4: Agent name completion
echo
echo "Test 4: Agent name completion"
export COMP_WORDS=("install-agents" "/tmp" "")
export COMP_CWORD=2
_install_agents_completion
echo "Available agents (first 5): ${COMPREPLY[*]:0:5}"

# Test 5: Symlink options
echo
echo "Test 5: Options after --symlink"
export COMP_WORDS=("install-agents" "--symlink" "--")
export COMP_CWORD=2
_install_agents_completion
echo "Symlink options (first 10): ${COMPREPLY[*]:0:10}"

echo
echo "Completion test completed successfully!"