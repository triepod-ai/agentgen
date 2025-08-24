#!/bin/bash
# List agents with color coding
# This script can be integrated into install-agents

# Colors for output - with proper terminal detection
if [[ -t 1 ]] || [[ "${FORCE_COLOR:-}" == "1" ]] || [[ "${CLICOLOR_FORCE:-}" == "1" ]]; then
    # Terminal supports colors or color is forced
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    PURPLE='\033[0;35m'
    CYAN='\033[0;36m'
    WHITE='\033[1;37m'
    ORANGE='\033[0;33m'
    BROWN='\033[38;5;94m'
    TEAL='\033[0;96m'
    BLACK='\033[0;90m'
    NC='\033[0m' # No Color
else
    # No color support or NO_COLOR is set
    RED='' GREEN='' YELLOW='' BLUE='' PURPLE='' CYAN='' WHITE='' ORANGE='' BROWN='' TEAL='' BLACK='' NC=''
fi

# Disable colors if NO_COLOR is set (https://no-color.org)
if [[ "${NO_COLOR:-}" != "" ]]; then
    RED='' GREEN='' YELLOW='' BLUE='' PURPLE='' CYAN='' WHITE='' ORANGE='' BROWN='' TEAL='' BLACK='' NC=''
fi

AGENTS_DIR="${1:-agents}"

# Color mapping
get_color_display() {
    local color="$1"
    local icon="$2"
    
    case "$color" in
        "red") echo -e "${RED}🔴${NC}" ;;
        "orange") echo -e "${ORANGE}🟠${NC}" ;;
        "yellow") echo -e "${YELLOW}🟡${NC}" ;;
        "blue") echo -e "${BLUE}🔵${NC}" ;;
        "purple") echo -e "${PURPLE}🟣${NC}" ;;
        "green") echo -e "${GREEN}🟢${NC}" ;;
        "brown") echo -e "${BROWN}🟤${NC}" ;;
        "teal") echo -e "${TEAL}🟦${NC}" ;;
        "black") echo -e "${BLACK}⚫${NC}" ;;
        *) echo -e "❓" ;;
    esac
}

# Extract YAML frontmatter value
extract_yaml_value() {
    local file="$1"
    local key="$2"
    
    # Extract YAML frontmatter block
    local yaml_block=$(sed -n '/^---$/,/^---$/p' "$file" | sed '1d;$d')
    
    # Extract the value for the key
    echo "$yaml_block" | grep "^$key:" | sed "s/^$key: *//" | sed 's/^"\(.*\)"$/\1/' | sed "s/^'\(.*\)'$/\1/"
}

# Get agent metadata
get_agent_metadata() {
    local file="$1"
    local agent_name=$(basename "$file" .md)
    
    if [ ! -f "$file" ]; then
        return 1
    fi
    
    local color=$(extract_yaml_value "$file" "color")
    local category=$(extract_yaml_value "$file" "category")
    local description=$(extract_yaml_value "$file" "description" | head -1)
    
    # Extract icon from accessibility metadata
    local icon=$(sed -n '/^---$/,/^---$/p' "$file" | grep -A5 "accessibility:" | grep "icon:" | sed 's/.*icon: *//' | sed 's/['"'"'"]//g' | head -1)
    
    echo "$agent_name|$color|$category|$icon|$description"
}

# List agents by color category
list_agents_by_color() {
    echo -e "${WHITE}🎨 Agents by Color Category${NC}"
    echo ""
    
    # Declare associative arrays
    declare -A color_categories
    declare -A color_descriptions
    declare -A color_agents
    
    # Color category definitions
    color_categories["red"]="Critical/Security"
    color_categories["orange"]="Architecture/Orchestration"
    color_categories["yellow"]="Development/Specialists"
    color_categories["blue"]="Infrastructure/DevOps"
    color_categories["purple"]="Data/AI"
    color_categories["green"]="Simple/Tools"
    color_categories["brown"]="Business/Content"
    color_categories["teal"]="Quality/Testing"
    color_categories["black"]="Enhanced/Premium"
    
    color_descriptions["red"]="High-priority security, critical system operations"
    color_descriptions["orange"]="System design, coordination, complex orchestration"
    color_descriptions["yellow"]="Core development work, language specialists"
    color_descriptions["blue"]="Infrastructure, deployment, system management"
    color_descriptions["purple"]="Data processing, machine learning, AI operations"
    color_descriptions["green"]="Basic utilities, simple operations, development tools"
    color_descriptions["brown"]="Business logic, content creation, documentation"
    color_descriptions["teal"]="Testing, QA, code review, quality assurance"
    color_descriptions["black"]="Knowledge-enhanced agents with advanced capabilities"
    
    # Initialize arrays
    for color in red orange yellow blue purple green brown teal black; do
        color_agents["$color"]=""
    done
    
    # Scan all agent files
    local total_agents=0
    while IFS= read -r -d '' file; do
        local metadata
        if metadata=$(get_agent_metadata "$file"); then
            IFS='|' read -r agent_name color category icon description <<< "$metadata"
            
            if [[ -n "$color" && -n "${color_categories[$color]}" ]]; then
                color_agents["$color"]+="$agent_name|$icon|$description"$'\n'
                ((total_agents++))
            fi
        fi
    done < <(find "$AGENTS_DIR" -name "*.md" -type f ! -name "README.md" -print0 | sort -z)
    
    # Display by color category
    local categories_with_agents=0
    for color in red orange yellow blue purple green brown teal black; do
        if [[ -n "${color_agents[$color]}" ]]; then
            local color_display=$(get_color_display "$color")
            local category_name="${color_categories[$color]}"
            local description="${color_descriptions[$color]}"
            
            echo -e "$color_display ${WHITE}$category_name${NC}"
            echo -e "   ${description}"
            echo ""
            
            local agent_count=0
            while IFS= read -r line; do
                if [[ -n "$line" ]]; then
                    IFS='|' read -r agent_name icon description <<< "$line"
                    
                    # Enhanced display format
                    if [[ -n "$icon" ]]; then
                        echo -e "   $icon ${CYAN}$agent_name${NC}"
                    else
                        echo -e "   • ${CYAN}$agent_name${NC}"
                    fi
                    
                    # Show truncated description
                    if [[ -n "$description" ]]; then
                        local truncated_desc=$(echo "$description" | head -1 | cut -c1-60)
                        if [[ ${#description} -gt 60 ]]; then
                            truncated_desc="${truncated_desc}..."
                        fi
                        echo -e "     ${description:0:60}${truncated_desc:60:3}"
                    fi
                    ((agent_count++))
                fi
            done <<< "${color_agents[$color]}"
            
            echo -e "   ${agent_count} agents"
            echo ""
            ((categories_with_agents++))
        fi
    done
    
    echo -e "${WHITE}📊 Summary${NC}"
    echo "   Total Categories: $categories_with_agents"
    echo "   Total Agents: $total_agents"
}

# Main execution
main() {
    if [ ! -d "$AGENTS_DIR" ]; then
        echo "Error: Agents directory '$AGENTS_DIR' not found"
        exit 1
    fi
    
    list_agents_by_color
}

# Handle script arguments
case "${1:-}" in
    -h|--help)
        cat << EOF
List Agents with Color Coding

Usage: $0 [AGENTS_DIR]

Arguments:
  AGENTS_DIR    Directory containing agent files (default: agents)

This script lists all agents grouped by color category with:
  🎨 Visual color coding and icons
  📝 Agent descriptions
  📊 Category statistics

Examples:
  $0                    # List agents in ./agents
  $0 /path/to/agents    # List agents in specific directory

EOF
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac