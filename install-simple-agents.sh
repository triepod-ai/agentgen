#!/bin/bash

# Simple Agents Installer
# Installs ultra-fast single-tool agents for specific tasks

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default to current directory if no path provided
PROJECT_PATH="${1:-.}"

# Validate project path
if [ ! -d "$PROJECT_PATH" ]; then
    echo -e "${RED}Error: Project directory '$PROJECT_PATH' does not exist${NC}"
    exit 1
fi

# Create .claude/agents directory
AGENTS_DIR="$PROJECT_PATH/.claude/agents"
mkdir -p "$AGENTS_DIR"

echo -e "${BLUE}Installing Simple Single-Tool Agents...${NC}"
echo "Target: $AGENTS_DIR"
echo ""

# Simple agents to install
declare -a SIMPLE_AGENTS=(
    # Read agents
    "simple-agents/config-reader.md"
    "simple-agents/log-reader.md"
    "simple-agents/readme-reader.md"
    "simple-agents/env-reader.md"
    "archive/agents/analyze-screenshot.md"  # Include existing single-tool agent
    
    # Write agents
    "simple-agents/gitignore-writer.md"
    "simple-agents/readme-writer.md"
    "simple-agents/env-writer.md"
    "simple-agents/changelog-writer.md"
    
    # Bash agents
    "simple-agents/test-runner.md"
    "simple-agents/build-runner.md"
    "simple-agents/git-executor.md"
    "simple-agents/dependency-installer.md"
    
    # Grep agents
    "simple-agents/error-finder.md"
    "simple-agents/todo-finder.md"
    "simple-agents/import-finder.md"
    "simple-agents/function-finder.md"
    
    # Edit agents
    "simple-agents/comment-remover.md"
    "simple-agents/whitespace-fixer.md"
    "simple-agents/import-sorter.md"
    "simple-agents/typo-fixer.md"
)

# Install agents
INSTALLED=0
SKIPPED=0

echo -e "${YELLOW}Installing agents by category:${NC}"
echo ""

# Track current category
CURRENT_CATEGORY=""

for agent_path in "${SIMPLE_AGENTS[@]}"; do
    # Determine category from path
    if [[ "$agent_path" == *"config-reader"* ]]; then
        NEW_CATEGORY="Read Agents (Analyzers)"
    elif [[ "$agent_path" == *"gitignore-writer"* ]]; then
        NEW_CATEGORY="Write Agents (Generators)"
    elif [[ "$agent_path" == *"test-runner"* ]]; then
        NEW_CATEGORY="Bash Agents (Executors)"
    elif [[ "$agent_path" == *"error-finder"* ]]; then
        NEW_CATEGORY="Grep Agents (Searchers)"
    elif [[ "$agent_path" == *"comment-remover"* ]]; then
        NEW_CATEGORY="Edit Agents (Modifiers)"
    fi
    
    # Print category header if changed
    if [ "$NEW_CATEGORY" != "$CURRENT_CATEGORY" ] && [ -n "$NEW_CATEGORY" ]; then
        echo ""
        echo -e "${BLUE}$NEW_CATEGORY:${NC}"
        CURRENT_CATEGORY="$NEW_CATEGORY"
    fi
    
    if [ -f "$agent_path" ]; then
        agent_name=$(basename "$agent_path" .md)
        target_file="$AGENTS_DIR/$agent_name.md"
        
        if [ -f "$target_file" ]; then
            echo "  ⏭️  Skipping $agent_name (already exists)"
            ((SKIPPED++))
        else
            cp "$agent_path" "$target_file"
            
            # Get tool from agent
            tool=$(grep "^tools:" "$agent_path" | sed 's/tools: //' || echo "Unknown")
            
            echo -e "  ${GREEN}✓${NC} Installed $agent_name (Tool: $tool)"
            ((INSTALLED++))
        fi
    else
        echo -e "  ${RED}✗${NC} Agent file not found: $agent_path"
    fi
done

# Summary
echo ""
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}Installation Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo ""
echo "📊 Summary:"
echo "  • Installed: $INSTALLED agents"
echo "  • Skipped: $SKIPPED agents (already existed)"
echo "  • Total available: $((INSTALLED + SKIPPED)) simple agents"
echo ""
echo "🚀 These single-tool agents are optimized for:"
echo "  • Ultra-fast loading (<100ms)"
echo "  • Specific, focused tasks"
echo "  • Minimal token usage"
echo "  • Clear, predictable behavior"
echo ""
echo "📝 Usage examples:"
echo -e "  ${YELLOW}@config-reader${NC} - Read and parse config files"
echo -e "  ${YELLOW}@error-finder${NC} - Find all errors in codebase"
echo -e "  ${YELLOW}@test-runner${NC} - Run test suite"
echo -e "  ${YELLOW}@gitignore-writer${NC} - Generate .gitignore"
echo -e "  ${YELLOW}@whitespace-fixer${NC} - Clean up formatting"
echo ""
echo "💡 Tip: These agents work great in combination!"
echo "   Example: @error-finder → @typo-fixer → @test-runner"