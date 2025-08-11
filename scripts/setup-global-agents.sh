#!/bin/bash

# Setup Global Agents Script
# Creates symbolic links for commonly used agents in ~/.claude/agents/

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARCHIVE_DIR="$SCRIPT_DIR/../archive/agents"
GLOBAL_AGENTS_DIR="$HOME/.claude/agents"

# List of recommended global agents
RECOMMENDED_AGENTS=(
    "analyze-codebase.md"
    "analyze-screenshot.md"
    "build-backend.md"
    "build-frontend.md"
    "cloud-architect-specialist.md"
    "create-lesson.md"
    "database-specialist.md"
    "debug-issue.md"
    "deploy-application.md"
    "deployment-engineer-specialist.md"
    "extract-insights.md"
    "manage-database.md"
    "ml-specialist.md"
    "nextjs-pro.md"
    "orchestrate-agents.md"
    "orchestrate-tasks.md"
    "prompt-engineer.md"
    "python-specialist.md"
    "react-specialist.md"
    "test-automation.md"
    "update-status.md"
)

# Function to display help
show_help() {
    cat << EOF
Global Agents Setup Script

USAGE:
    setup-global-agents.sh [OPTIONS]

OPTIONS:
    --help              Show this help message
    --list              List available agents in archive
    --status            Show current global agents status
    --recommended       Install recommended global agents
    --all               Install all available agents as global
    --remove            Remove all global agent links
    --specific <agents> Install specific agents (space-separated)

EXAMPLES:
    # Install recommended global agents
    ./setup-global-agents.sh --recommended

    # Check current status
    ./setup-global-agents.sh --status

    # Install specific agents
    ./setup-global-agents.sh --specific "debug-issue.md python-specialist.md"

    # Remove all global agents
    ./setup-global-agents.sh --remove

EOF
}

# Create global agents directory if it doesn't exist
ensure_global_dir() {
    if [ ! -d "$GLOBAL_AGENTS_DIR" ]; then
        echo -e "${YELLOW}Creating global agents directory: $GLOBAL_AGENTS_DIR${NC}"
        mkdir -p "$GLOBAL_AGENTS_DIR"
    fi
}

# List available agents
list_agents() {
    echo -e "${BLUE}Available agents in archive:${NC}"
    ls -1 "$ARCHIVE_DIR"/*.md 2>/dev/null | xargs -n1 basename | sort | column -c 80
}

# Show current status
show_status() {
    echo -e "${BLUE}=== Global Agents Status ===${NC}"
    
    if [ ! -d "$GLOBAL_AGENTS_DIR" ]; then
        echo -e "${YELLOW}Global agents directory does not exist yet${NC}"
        return
    fi
    
    local count=$(find "$GLOBAL_AGENTS_DIR" -type l 2>/dev/null | wc -l)
    echo -e "Total global agents: ${GREEN}$count${NC}"
    
    if [ $count -gt 0 ]; then
        echo -e "\n${BLUE}Current global agents:${NC}"
        find "$GLOBAL_AGENTS_DIR" -type l -exec basename {} \; 2>/dev/null | sort | column -c 80
    fi
    
    # Check for broken links
    local broken=$(find "$GLOBAL_AGENTS_DIR" -type l -xtype l 2>/dev/null | wc -l)
    if [ $broken -gt 0 ]; then
        echo -e "\n${RED}Warning: $broken broken symbolic link(s) found${NC}"
        find "$GLOBAL_AGENTS_DIR" -type l -xtype l -exec basename {} \; 2>/dev/null
    fi
}

# Install recommended agents
install_recommended() {
    ensure_global_dir
    
    echo -e "${BLUE}Installing recommended global agents...${NC}"
    
    local installed=0
    local skipped=0
    
    for agent in "${RECOMMENDED_AGENTS[@]}"; do
        local source="$ARCHIVE_DIR/$agent"
        local target="$GLOBAL_AGENTS_DIR/$agent"
        
        if [ ! -f "$source" ]; then
            echo -e "${RED}✗${NC} $agent - source not found"
            continue
        fi
        
        if [ -L "$target" ] || [ -f "$target" ]; then
            echo -e "${YELLOW}⊝${NC} $agent - already exists"
            ((skipped++))
        else
            ln -s "$source" "$target"
            echo -e "${GREEN}✓${NC} $agent - linked"
            ((installed++))
        fi
    done
    
    echo -e "\n${GREEN}Installed: $installed${NC}, ${YELLOW}Skipped: $skipped${NC}"
}

# Install all agents
install_all() {
    ensure_global_dir
    
    echo -e "${BLUE}Installing all agents as global...${NC}"
    
    local installed=0
    local skipped=0
    
    for source in "$ARCHIVE_DIR"/*.md; do
        [ -f "$source" ] || continue
        
        local agent=$(basename "$source")
        local target="$GLOBAL_AGENTS_DIR/$agent"
        
        if [ -L "$target" ] || [ -f "$target" ]; then
            echo -e "${YELLOW}⊝${NC} $agent - already exists"
            ((skipped++))
        else
            ln -s "$source" "$target"
            echo -e "${GREEN}✓${NC} $agent - linked"
            ((installed++))
        fi
    done
    
    echo -e "\n${GREEN}Installed: $installed${NC}, ${YELLOW}Skipped: $skipped${NC}"
}

# Install specific agents
install_specific() {
    ensure_global_dir
    
    echo -e "${BLUE}Installing specific agents...${NC}"
    
    local agents=($@)
    local installed=0
    local failed=0
    
    for agent in "${agents[@]}"; do
        # Add .md extension if not present
        [[ "$agent" != *.md ]] && agent="${agent}.md"
        
        local source="$ARCHIVE_DIR/$agent"
        local target="$GLOBAL_AGENTS_DIR/$agent"
        
        if [ ! -f "$source" ]; then
            echo -e "${RED}✗${NC} $agent - source not found"
            ((failed++))
            continue
        fi
        
        if [ -L "$target" ] || [ -f "$target" ]; then
            echo -e "${YELLOW}⊝${NC} $agent - already exists"
        else
            ln -s "$source" "$target"
            echo -e "${GREEN}✓${NC} $agent - linked"
            ((installed++))
        fi
    done
    
    echo -e "\n${GREEN}Installed: $installed${NC}, ${RED}Failed: $failed${NC}"
}

# Remove all global agents
remove_all() {
    if [ ! -d "$GLOBAL_AGENTS_DIR" ]; then
        echo -e "${YELLOW}Global agents directory does not exist${NC}"
        return
    fi
    
    echo -e "${RED}Removing all global agent links...${NC}"
    
    local count=$(find "$GLOBAL_AGENTS_DIR" -type l 2>/dev/null | wc -l)
    
    if [ $count -eq 0 ]; then
        echo -e "${YELLOW}No global agents to remove${NC}"
        return
    fi
    
    # Confirm
    read -p "Are you sure you want to remove $count global agent link(s)? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        find "$GLOBAL_AGENTS_DIR" -type l -delete
        echo -e "${GREEN}Removed $count global agent link(s)${NC}"
    else
        echo -e "${YELLOW}Cancelled${NC}"
    fi
}

# Main script logic
case "${1:-}" in
    --help)
        show_help
        ;;
    --list)
        list_agents
        ;;
    --status)
        show_status
        ;;
    --recommended)
        install_recommended
        ;;
    --all)
        install_all
        ;;
    --remove)
        remove_all
        ;;
    --specific)
        shift
        if [ $# -eq 0 ]; then
            echo -e "${RED}Error: No agents specified${NC}"
            echo "Usage: $0 --specific agent1 agent2 ..."
            exit 1
        fi
        install_specific "$@"
        ;;
    *)
        show_help
        ;;
esac