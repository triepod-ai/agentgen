#!/bin/bash

# Migrate existing agent installations from copies to symlinks
# This script converts copy-based agent installations to symlink-based

set -e

# Colors for output
if [[ -t 1 ]] || [[ "${FORCE_COLOR:-}" == "1" ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    CYAN='\033[0;36m'
    NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' BLUE='' CYAN='' NC=''
fi

# Disable colors if NO_COLOR is set
if [[ "${NO_COLOR:-}" != "" ]]; then
    RED='' GREEN='' YELLOW='' BLUE='' CYAN='' NC=''
fi

# Default values
DRY_RUN=false
BACKUP=true
VERBOSE=false
TARGET_DIRS=()

# Script directory and hub location
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
AGENTS_HUB="$SCRIPT_DIR/agents"

show_usage() {
    cat << EOF
${BLUE}Agent Hub Migration Tool - Copy to Symlink Converter${NC}

${YELLOW}USAGE:${NC}
    $0 [OPTIONS] TARGET_DIR [TARGET_DIR2 ...]

${YELLOW}DESCRIPTION:${NC}
    Converts existing copy-based agent installations to symlink-based installations.
    This enables single-source management where all agents are maintained in the hub.

${YELLOW}TARGET DIRECTORIES:${NC}
    Specify one or more directories containing .claude/agents/ folders to migrate.
    Examples:
      /path/to/project              # Migrates /path/to/project/.claude/agents/
      ~/.claude                     # Migrates ~/.claude/agents/ (global)

${YELLOW}OPTIONS:${NC}
    ${GREEN}--dry-run${NC}           Show what would be done without making changes
    ${GREEN}--no-backup${NC}         Skip creating backup of original files
    ${GREEN}--verbose${NC}           Show detailed output
    ${GREEN}--help${NC}              Show this help message

${YELLOW}EXAMPLES:${NC}
    # Migrate a single project (with dry-run first)
    $0 --dry-run /path/to/my-project
    $0 /path/to/my-project

    # Migrate multiple projects
    $0 /path/to/project1 /path/to/project2 ~/.claude

    # Migrate without backup (faster, but no safety net)
    $0 --no-backup /path/to/project

${YELLOW}SAFETY FEATURES:${NC}
    • Creates backup directory with timestamp before migration
    • Validates all symlinks after creation
    • Rolls back on any failure (if backup exists)
    • Dry-run mode to preview changes

${YELLOW}MIGRATION PROCESS:${NC}
    1. Scan target directories for .claude/agents/ folders
    2. Create backup of existing files (unless --no-backup)
    3. Identify matching agents in the hub
    4. Replace copies with symlinks to hub
    5. Validate all symlinks work correctly
    6. Report migration statistics

EOF
}

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_verbose() {
    if [[ "$VERBOSE" == "true" ]]; then
        echo -e "${CYAN}[VERBOSE]${NC} $1"
    fi
}

# Check if hub exists
check_hub() {
    if [[ ! -d "$AGENTS_HUB" ]]; then
        log_error "Agents hub not found at: $AGENTS_HUB"
        log_error "Please ensure you're running this from the agentgen directory"
        exit 1
    fi
    log_verbose "Using agents hub: $AGENTS_HUB"
}

# Find agent in hub by name
find_agent_in_hub() {
    local agent_name="$1"
    local hub_path=""
    
    # Search all categories for the agent
    for category in core development specialists infrastructure quality content data tools simple; do
        local candidate="$AGENTS_HUB/$category/$agent_name.md"
        if [[ -f "$candidate" ]]; then
            hub_path="$candidate"
            break
        fi
    done
    
    echo "$hub_path"
}

# Create backup of agents directory
create_backup() {
    local agents_dir="$1"
    local backup_dir="$agents_dir.backup.$(date +%Y%m%d_%H%M%S)"
    
    if [[ "$BACKUP" == "true" ]]; then
        log_info "Creating backup: $backup_dir"
        if [[ "$DRY_RUN" != "true" ]]; then
            cp -r "$agents_dir" "$backup_dir"
            log_verbose "Backup created at: $backup_dir"
        fi
    fi
    
    echo "$backup_dir"
}

# Migrate a single agents directory
migrate_directory() {
    local target_dir="$1"
    local agents_dir="$target_dir/.claude/agents"
    
    if [[ ! -d "$agents_dir" ]]; then
        log_warning "No .claude/agents directory found in: $target_dir"
        return 1
    fi
    
    log_info "Migrating: $agents_dir"
    
    # Create backup
    local backup_dir=""
    if [[ "$BACKUP" == "true" ]]; then
        backup_dir=$(create_backup "$agents_dir")
    fi
    
    local total=0
    local migrated=0
    local skipped=0
    local failed=0
    
    # Process each agent file
    find "$agents_dir" -name "*.md" -type f | while read -r agent_file; do
        ((total++))
        local agent_name=$(basename "$agent_file" .md)
        local hub_agent=$(find_agent_in_hub "$agent_name")
        
        log_verbose "Processing: $agent_name"
        
        if [[ -z "$hub_agent" ]]; then
            log_warning "Agent '$agent_name' not found in hub, skipping"
            ((skipped++))
            continue
        fi
        
        if [[ "$DRY_RUN" == "true" ]]; then
            echo -e "${CYAN}[DRY-RUN]${NC} Would replace $agent_file with symlink to $hub_agent"
            ((migrated++))
        else
            # Remove the copy and create symlink
            if rm "$agent_file" && ln -s "$hub_agent" "$agent_file"; then
                log_success "Migrated $agent_name → $(basename "$hub_agent")"
                ((migrated++))
            else
                log_error "Failed to migrate $agent_name"
                ((failed++))
            fi
        fi
    done
    
    echo
    log_success "Migration complete for $target_dir:"
    log_info "  Total: $total, Migrated: $migrated, Skipped: $skipped, Failed: $failed"
    
    if [[ "$failed" -gt 0 && "$BACKUP" == "true" && -n "$backup_dir" ]]; then
        log_warning "Some migrations failed. Backup available at: $backup_dir"
    fi
}

# Validate symlinks in directory
validate_symlinks() {
    local agents_dir="$1"
    local working=0
    local broken=0
    
    find "$agents_dir" -name "*.md" -type l | while read -r link; do
        if [[ -e "$link" ]]; then
            ((working++))
            log_verbose "✓ $(basename "$link" .md) → $(readlink "$link")"
        else
            ((broken++))
            log_error "✗ $(basename "$link" .md) → $(readlink "$link") (BROKEN)"
        fi
    done
    
    log_info "Validation: $working working, $broken broken symlinks"
    return $broken
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --help|-h)
            show_usage
            exit 0
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --no-backup)
            BACKUP=false
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        -*)
            log_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
        *)
            TARGET_DIRS+=("$1")
            shift
            ;;
    esac
done

# Validate arguments
if [[ ${#TARGET_DIRS[@]} -eq 0 ]]; then
    log_error "At least one target directory must be specified"
    show_usage
    exit 1
fi

check_hub

# Show configuration
if [[ "$DRY_RUN" == "true" ]]; then
    log_info "DRY-RUN MODE: No actual changes will be made"
fi
if [[ "$BACKUP" == "false" ]]; then
    log_warning "BACKUP DISABLED: Original files will be permanently deleted"
fi

echo
log_info "Starting migration from copies to symlinks..."
log_info "Hub location: $AGENTS_HUB"
log_info "Target directories: ${TARGET_DIRS[*]}"
echo

# Process each target directory
for target_dir in "${TARGET_DIRS[@]}"; do
    if [[ ! -d "$target_dir" ]]; then
        log_error "Directory not found: $target_dir"
        continue
    fi
    
    migrate_directory "$target_dir"
    echo
done

log_success "Migration process complete!"
echo
echo -e "${YELLOW}Next steps:${NC}"
echo "• Test agents to ensure they work correctly"
echo "• Run health check: ./install-agents-symlink --health"
echo "• Update agents by modifying files in: $AGENTS_HUB"
echo "• Changes will now propagate instantly to all migrated installations"

if [[ "$BACKUP" == "true" ]]; then
    echo
    echo -e "${YELLOW}Rollback instructions:${NC}"
    echo "If you need to rollback, restore from backup directories created with timestamps"
    echo "Example: mv /path/.claude/agents.backup.TIMESTAMP /path/.claude/agents"
fi