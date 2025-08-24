#!/bin/bash
# Agent Color System Validation Script
#
# Validates color compliance, accessibility, and consistency across all agents

set -e

# Colors and formatting
RED='\033[0;31m'
GREEN='\033[0;32m' 
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# Configuration
AGENTS_DIR="${1:-agents}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Valid colors
VALID_COLORS=("red" "orange" "yellow" "blue" "purple" "green" "brown" "teal" "black")

# Validation counters
TOTAL_AGENTS=0
VALID_AGENTS=0
MISSING_COLOR=0
INVALID_COLOR=0
MISSING_ACCESSIBILITY=0
INCONSISTENT_CATEGORY=0

# Color statistics
declare -A COLOR_COUNTS
declare -A CATEGORY_COUNTS

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_header() {
    echo -e "${WHITE}🔍 $1${NC}"
}

# Check if color is valid
is_valid_color() {
    local color=$1
    for valid_color in "${VALID_COLORS[@]}"; do
        if [[ "$color" == "$valid_color" ]]; then
            return 0
        fi
    done
    return 1
}

# Extract YAML frontmatter value
extract_yaml_value() {
    local file=$1
    local key=$2
    
    # Extract YAML frontmatter block
    local yaml_block=$(sed -n '/^---$/,/^---$/p' "$file" | sed '1d;$d')
    
    # Extract the value for the key
    echo "$yaml_block" | grep "^$key:" | sed "s/^$key: *//" | sed 's/^"\(.*\)"$/\1/' | sed "s/^'\(.*\)'$/\1/"
}

# Validate single agent file
validate_agent() {
    local file=$1
    local agent_name=$(basename "$file" .md)
    local is_valid=true
    
    TOTAL_AGENTS=$((TOTAL_AGENTS + 1))
    
    # Check if file has YAML frontmatter
    if ! grep -q "^---$" "$file"; then
        log_error "$agent_name: Missing YAML frontmatter"
        return 1
    fi
    
    # Extract values
    local color=$(extract_yaml_value "$file" "color")
    local category=$(extract_yaml_value "$file" "category") 
    local accessibility_icon=$(extract_yaml_value "$file" "accessibility" | grep "icon:" | cut -d':' -f2 | sed 's/^ *//' | sed 's/"//g' | sed "s/'//g")
    
    # Validate color
    if [[ -z "$color" ]]; then
        log_error "$agent_name: Missing color field"
        MISSING_COLOR=$((MISSING_COLOR + 1))
        is_valid=false
    elif ! is_valid_color "$color"; then
        log_error "$agent_name: Invalid color '$color'"
        INVALID_COLOR=$((INVALID_COLOR + 1))
        is_valid=false
    else
        COLOR_COUNTS[$color]=$((${COLOR_COUNTS[$color]:-0} + 1))
    fi
    
    # Validate accessibility metadata
    if ! grep -q "accessibility:" "$file"; then
        log_warning "$agent_name: Missing accessibility metadata"
        MISSING_ACCESSIBILITY=$((MISSING_ACCESSIBILITY + 1))
    elif [[ -z "$accessibility_icon" ]]; then
        log_warning "$agent_name: Missing accessibility icon"
        MISSING_ACCESSIBILITY=$((MISSING_ACCESSIBILITY + 1))
    fi
    
    # Validate category consistency
    if [[ -n "$color" && -n "$category" ]]; then
        case "$color" in
            "red") expected_category="critical" ;;
            "orange") expected_category="architecture" ;;
            "yellow") expected_category="development" ;;
            "blue") expected_category="infrastructure" ;;
            "purple") expected_category="data-ai" ;;
            "green") expected_category="simple" ;;
            "brown") expected_category="business" ;;
            "teal") expected_category="quality" ;;
            "black") expected_category="enhanced" ;;
            *) expected_category="" ;;
        esac
        
        if [[ -n "$expected_category" && "$category" != "$expected_category" ]]; then
            log_warning "$agent_name: Category '$category' doesn't match color '$color' (expected '$expected_category')"
            INCONSISTENT_CATEGORY=$((INCONSISTENT_CATEGORY + 1))
        fi
    fi
    
    # Count category
    if [[ -n "$category" ]]; then
        CATEGORY_COUNTS[$category]=$((${CATEGORY_COUNTS[$category]:-0} + 1))
    fi
    
    if $is_valid; then
        VALID_AGENTS=$((VALID_AGENTS + 1))
        return 0
    else
        return 1
    fi
}

# Main validation function
main() {
    log_header "Agent Color System Validation"
    echo
    
    # Check if agents directory exists
    if [[ ! -d "$AGENTS_DIR" ]]; then
        log_error "Agents directory '$AGENTS_DIR' not found"
        exit 1
    fi
    
    log_info "Validating agents in: $AGENTS_DIR"
    echo
    
    # Find all agent files
    local agent_files=()
    while IFS= read -r -d '' file; do
        agent_files+=("$file")
    done < <(find "$AGENTS_DIR" -name "*.md" -type f -print0 | sort -z)
    
    if [[ ${#agent_files[@]} -eq 0 ]]; then
        log_error "No agent files found in $AGENTS_DIR"
        exit 1
    fi
    
    log_info "Found ${#agent_files[@]} agent files"
    echo
    
    # Validate each agent
    log_header "Validating Individual Agents"
    local failed_agents=()
    
    for file in "${agent_files[@]}"; do
        if ! validate_agent "$file"; then
            failed_agents+=("$(basename "$file" .md)")
        fi
    done
    
    echo
    
    # Print summary statistics
    log_header "Validation Summary"
    
    echo -e "📊 ${WHITE}Overall Statistics:${NC}"
    echo "   Total Agents: $TOTAL_AGENTS"
    echo "   Valid Agents: $VALID_AGENTS"
    echo "   Failed Agents: $((TOTAL_AGENTS - VALID_AGENTS))"
    echo
    
    echo -e "🎨 ${WHITE}Color Distribution:${NC}"
    for color in "${VALID_COLORS[@]}"; do
        local count=${COLOR_COUNTS[$color]:-0}
        local icon
        case "$color" in
            "red") icon="🔴" ;;
            "orange") icon="🟠" ;;
            "yellow") icon="🟡" ;;
            "blue") icon="🔵" ;;
            "purple") icon="🟣" ;;
            "green") icon="🟢" ;;
            "brown") icon="🟤" ;;
            "teal") icon="🟦" ;;
            "black") icon="⚫" ;;
            *) icon="❓" ;;
        esac
        if [[ $count -gt 0 ]]; then
            echo "   $icon $color: $count agents"
        fi
    done
    echo
    
    # Error breakdown
    if [[ $MISSING_COLOR -gt 0 || $INVALID_COLOR -gt 0 || $MISSING_ACCESSIBILITY -gt 0 || $INCONSISTENT_CATEGORY -gt 0 ]]; then
        log_header "Issues Found"
        
        if [[ $MISSING_COLOR -gt 0 ]]; then
            log_error "Missing color field: $MISSING_COLOR agents"
        fi
        
        if [[ $INVALID_COLOR -gt 0 ]]; then
            log_error "Invalid color values: $INVALID_COLOR agents"
        fi
        
        if [[ $MISSING_ACCESSIBILITY -gt 0 ]]; then
            log_warning "Missing accessibility metadata: $MISSING_ACCESSIBILITY agents"
        fi
        
        if [[ $INCONSISTENT_CATEGORY -gt 0 ]]; then
            log_warning "Inconsistent color/category mapping: $INCONSISTENT_CATEGORY agents"
        fi
        echo
    fi
    
    # Recommendations
    if [[ ${#failed_agents[@]} -gt 0 ]]; then
        log_header "Recommendations"
        log_info "Run the following command to fix issues automatically:"
        echo "   ./scripts/update-agent-colors.py --agents-dir $AGENTS_DIR"
        echo
        
        log_info "Or fix individual agents:"
        for agent in "${failed_agents[@]}"; do
            echo "   ./scripts/update-agent-colors.py --agent $agent"
        done
        echo
    fi
    
    # Final status
    if [[ $VALID_AGENTS -eq $TOTAL_AGENTS ]]; then
        log_success "All agents pass color system validation! 🎉"
        exit 0
    else
        local failed_count=$((TOTAL_AGENTS - VALID_AGENTS))
        log_error "Validation failed: $failed_count/$TOTAL_AGENTS agents have issues"
        exit 1
    fi
}

# Script help
show_help() {
    cat << EOF
Agent Color System Validation Script

Usage: $0 [AGENTS_DIR]

Arguments:
  AGENTS_DIR    Directory containing agent files (default: agents)

Examples:
  $0                    # Validate agents in ./agents
  $0 /path/to/agents    # Validate agents in specific directory

This script validates:
  ✅ Color field presence and validity
  ✅ Accessibility metadata completeness
  ✅ Color-category consistency
  ✅ YAML frontmatter structure

Exit codes:
  0    All agents valid
  1    Validation errors found

EOF
}

# Handle script arguments
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac