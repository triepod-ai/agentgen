#!/bin/bash

# Debug completion script

source /home/bryan/agentgen/install-agents-completion.bash

# Test completion with debug output
COMP_WORDS=("install-agents" "--global" "")
COMP_CWORD=2
COMPREPLY=()

echo "Testing with COMP_WORDS: ${COMP_WORDS[@]}"
echo "COMP_CWORD: $COMP_CWORD"
echo "cur: '${COMP_WORDS[COMP_CWORD]}'"
echo "prev: '${COMP_WORDS[COMP_CWORD-1]}'"
echo

# Check if agents hub exists
agents_hub="/home/bryan/agentgen/agents"
echo "Checking agents_hub: $agents_hub"
if [[ -d "$agents_hub" ]]; then
    echo "✓ Hub exists"

    # Check categories
    for category in business content core data development experimental infrastructure quality simple specialists test tools; do
        if [[ -d "$agents_hub/$category" ]]; then
            count=$(ls "$agents_hub/$category"/*.md 2>/dev/null | wc -l)
            echo "  $category: $count agents"
        fi
    done
fi
echo

# Call completion function
_install_agents_completion

echo "COMPREPLY has ${#COMPREPLY[@]} items:"
for item in "${COMPREPLY[@]}"; do
    echo "  - $item"
done