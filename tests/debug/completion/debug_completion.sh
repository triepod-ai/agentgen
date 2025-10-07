#!/bin/bash
source ./install-agents-completion.bash

export COMP_WORDS=("install-agents" "test-autom")
export COMP_CWORD=1

echo "COMP_WORDS: ${COMP_WORDS[*]}"
echo "COMP_CWORD: $COMP_CWORD"
echo "cur: ${COMP_WORDS[COMP_CWORD]}"

# Debug the logic
echo "Debug completion logic..."
_install_agents_completion

echo "COMPREPLY: ${COMPREPLY[*]}"
