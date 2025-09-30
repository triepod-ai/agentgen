#!/bin/bash
# Bash completion for install-agents command

_install_agents_completion() {
    local cur prev opts profiles agents
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    
    # Get script directory dynamically
    local script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    local profiles_dir="$script_dir/profiles"
    local agents_hub="$script_dir/agents"
    
    # Available options
    local global_opts="--help --symlink --copy --global --project --health --repair --force --all --list --list-installed --profile --list-profiles --show-profile --simple --simple-read --simple-write --simple-bash --simple-grep --simple-edit --dry-run --verbose --skip-speak-check"
    
    # Get available profiles (remove .profile extension)
    if [[ -d "$profiles_dir" ]]; then
        profiles=$(ls "$profiles_dir"/*.profile 2>/dev/null | xargs -n1 basename | sed 's/\.profile$//' | tr '\n' ' ')
    fi
    
    # Get available agents from hub (optimized with timeout and caching)
    if [[ -d "$agents_hub" ]]; then
        # Use a faster approach: ls in each category directory
        agents=""
        for category in business content core data development experimental infrastructure quality simple specialists test tools; do
            if [[ -d "$agents_hub/$category" ]]; then
                category_agents=$(ls "$agents_hub/$category"/*.md 2>/dev/null | xargs -n1 basename 2>/dev/null | sed 's/\.md$//' | tr '\n' ' ')
                agents="$agents $category_agents"
            fi
        done
    fi
    
    # Handle specific argument completions
    case "$prev" in
        --profile|--show-profile)
            COMPREPLY=($(compgen -W "$profiles" -- "$cur"))
            return 0
            ;;
        --project)
            # Complete with directories
            COMPREPLY=($(compgen -d -- "$cur"))
            return 0
            ;;
        install-agents)
            # First argument completion
            COMPREPLY=($(compgen -W "$global_opts" -- "$cur"))
            return 0
            ;;
    esac
    
    # Check if we're completing agent names (after target path or with certain options)
    local has_target_path=""
    local has_all_option=""
    local has_profile_option=""
    local has_simple_option=""
    
    # Analyze previous arguments
    for ((i=1; i<COMP_CWORD; i++)); do
        case "${COMP_WORDS[i]}" in
            --all)
                has_all_option="true"
                ;;
            --profile)
                has_profile_option="true"
                ;;
            --simple|--simple-*)
                has_simple_option="true"
                ;;
            --symlink|--copy|--global|--health|--repair|--force|--list|--list-installed|--list-profiles|--show-profile|--dry-run|--verbose|--skip-speak-check|--help)
                # These are options, not target paths
                ;;
            --project)
                # Skip the next argument (project path)
                ((i++))
                has_target_path="true"
                ;;
            -*)
                # Other option
                ;;
            *)
                # Could be a target path or agent name
                # If it's not an option and we don't have a target path yet, assume it's the target path
                if [[ -z "$has_target_path" ]]; then
                    # Check if we're in global mode - if not, this is a target path
                    if [[ ! " ${COMP_WORDS[*]} " =~ --global ]]; then
                        has_target_path="true"
                    fi
                fi
                ;;
        esac
    done
    
    # If we have a dash prefix, complete with options
    if [[ "$cur" == -* ]]; then
        COMPREPLY=($(compgen -W "$global_opts" -- "$cur"))
        return 0
    fi
    
    # Determine what we should complete based on context
    local needs_directory=""
    local can_complete_agents=""
    
    # Check if we're in a mode that needs a directory
    if [[ ! " ${COMP_WORDS[*]} " =~ --global ]] &&
       [[ ! " ${COMP_WORDS[*]} " =~ --health ]] &&
       [[ ! " ${COMP_WORDS[*]} " =~ --repair ]] &&
       [[ ! " ${COMP_WORDS[*]} " =~ --list ]] &&
       [[ ! " ${COMP_WORDS[*]} " =~ --list-installed ]] &&
       [[ ! " ${COMP_WORDS[*]} " =~ --list-profiles ]] &&
       [[ ! " ${COMP_WORDS[*]} " =~ --show-profile ]]; then
        needs_directory="true"
    fi
    
    # Check if we can complete with agent names
    # NEW DEFAULT: Current directory is default target, so we can complete agents in simple mode
    if [[ -n "$has_target_path" || " ${COMP_WORDS[*]} " =~ --global ]]; then
        can_complete_agents="true"
    elif [[ -z "$has_target_path" ]] &&
         [[ ! " ${COMP_WORDS[*]} " =~ --project ]] &&
         [[ ! " ${COMP_WORDS[*]} " =~ --health ]] &&
         [[ ! " ${COMP_WORDS[*]} " =~ --repair ]] &&
         [[ ! " ${COMP_WORDS[*]} " =~ --list ]] &&
         [[ ! " ${COMP_WORDS[*]} " =~ --list-installed ]] &&
         [[ ! " ${COMP_WORDS[*]} " =~ --list-profiles ]] &&
         [[ ! " ${COMP_WORDS[*]} " =~ --show-profile ]]; then
        # NEW DEFAULT: Simple mode - current directory is target
        can_complete_agents="true"
    fi
    
    # If we need a directory and don't have a target path yet (project mode only)
    if [[ -n "$needs_directory" && -z "$has_target_path" ]] && [[ " ${COMP_WORDS[*]} " =~ --project ]]; then
        COMPREPLY=($(compgen -d -- "$cur"))
        return 0
    fi
    
    # Complete with agent names if we can and should
    if [[ -n "$can_complete_agents" ]] && 
       [[ -z "$has_all_option" && -z "$has_profile_option" && -z "$has_simple_option" ]]; then
        COMPREPLY=($(compgen -W "$agents" -- "$cur"))
        return 0
    fi
    
    # Default completion
    COMPREPLY=($(compgen -W "$global_opts" -- "$cur"))
}

# Register the completion function
complete -F _install_agents_completion install-agents

# Also complete for the script path if used directly
complete -F _install_agents_completion ./install-agents