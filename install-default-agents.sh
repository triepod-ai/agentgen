#!/bin/bash

# Default Agent Installation Script for AgentGen
# Installs a curated set of essential development agents

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default agents to install
DEFAULT_AGENTS=(
    "backend-architect"
    "frontend-developer"
    "full-stack-developer"
    "nextjs-pro"
    "ui-designer"
    "deployment-engineer"
    "debugger"
    "agent-organizer"
    "context-manager"
)

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Parse command line arguments
TARGET_PROJECT="${1:-.}"
FORCE_INSTALL="${2:-}"

# Show banner
echo ""
echo "════════════════════════════════════════════════════════════"
echo "     AgentGen Default Agent Installation Script"
echo "════════════════════════════════════════════════════════════"
echo ""

# Display agents to be installed
print_info "This script will install the following agents:"
echo ""
for agent in "${DEFAULT_AGENTS[@]}"; do
    echo "  • $agent"
done
echo ""

# Confirm installation
if [ "$FORCE_INSTALL" != "--force" ]; then
    read -p "Do you want to proceed with the installation? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Installation cancelled"
        exit 0
    fi
fi

# Check if install-agents command exists
if ! command -v install-agents &> /dev/null; then
    print_error "install-agents command not found"
    print_info "Please ensure install-agents is in your PATH"
    exit 1
fi

# Convert to absolute path
TARGET_PROJECT="$(cd "$TARGET_PROJECT" 2>/dev/null && pwd)" || {
    print_error "Target project path does not exist: $TARGET_PROJECT"
    exit 1
}

print_info "Installing agents to: $TARGET_PROJECT"
echo ""

# Counter for tracking progress
TOTAL=${#DEFAULT_AGENTS[@]}
CURRENT=0
SUCCESS=0
FAILED=0

# Install each agent
for agent in "${DEFAULT_AGENTS[@]}"; do
    ((CURRENT++))
    echo -ne "${BLUE}[${CURRENT}/${TOTAL}]${NC} Installing ${agent}... "
    
    if install-agents --force "$TARGET_PROJECT" "$agent" &> /tmp/agent_install_$$.log; then
        echo -e "${GREEN}✓${NC}"
        ((SUCCESS++))
    else
        echo -e "${RED}✗${NC}"
        print_error "Failed to install $agent. Check /tmp/agent_install_$$.log for details"
        ((FAILED++))
    fi
done

echo ""
echo "════════════════════════════════════════════════════════════"

# Summary
if [ $SUCCESS -eq $TOTAL ]; then
    print_success "All $TOTAL agents installed successfully! 🎉"
else
    print_warning "Installation complete: $SUCCESS succeeded, $FAILED failed"
fi

# Display usage instructions
echo ""
print_info "Your agents are ready to use!"
echo ""
echo "Quick Start Guide:"
echo "  • Use @agent-name for direct invocation (e.g., @debugger)"
echo "  • Agents auto-activate based on task context"
echo "  • Use @agent-organizer for complex multi-agent workflows"
echo ""
echo "Example Commands:"
echo "  @backend-architect design a REST API for user management"
echo "  @nextjs-pro create a dashboard component"
echo "  @debugger investigate the authentication error"
echo "  @deployment-engineer set up CI/CD pipeline"
echo ""

# Cleanup temp files
rm -f /tmp/agent_install_$$.log

print_success "Setup complete! Happy coding! 🚀"