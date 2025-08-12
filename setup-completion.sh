#!/bin/bash

# Setup bash completion for install-agents command
# This script sets up autocompletion for the install-agents command

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPLETION_FILE="$SCRIPT_DIR/install-agents-completion.bash"

# Colors for output
if [[ -t 1 ]]; then
    GREEN='\033[0;32m'
    BLUE='\033[0;34m'
    YELLOW='\033[1;33m'
    NC='\033[0m'
else
    GREEN=''
    BLUE=''
    YELLOW=''
    NC=''
fi

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if completion file exists
if [[ ! -f "$COMPLETION_FILE" ]]; then
    echo "Error: Completion file not found at $COMPLETION_FILE"
    exit 1
fi

print_info "Setting up bash completion for install-agents..."

# Option 1: Source directly in current session
print_info "Loading completion for current session..."
source "$COMPLETION_FILE"
print_success "Completion loaded for current session"

# Option 2: Add to user's bashrc for persistence
BASHRC="$HOME/.bashrc"
COMPLETION_LINE="source \"$COMPLETION_FILE\""

if [[ -f "$BASHRC" ]]; then
    if ! grep -q "install-agents-completion.bash" "$BASHRC"; then
        print_info "Adding completion to ~/.bashrc for future sessions..."
        echo "" >> "$BASHRC"
        echo "# install-agents bash completion" >> "$BASHRC"
        echo "$COMPLETION_LINE" >> "$BASHRC"
        print_success "Added completion to ~/.bashrc"
        print_info "Restart your terminal or run 'source ~/.bashrc' to enable completion in new sessions"
    else
        print_warning "Completion already configured in ~/.bashrc"
    fi
else
    print_warning "~/.bashrc not found, completion will only work in current session"
fi

# Option 3: System-wide installation (if possible)
if [[ -w /etc/bash_completion.d/ ]] 2>/dev/null; then
    print_info "System completion directory is writable, installing system-wide..."
    sudo cp "$COMPLETION_FILE" /etc/bash_completion.d/install-agents
    print_success "Installed system-wide completion"
elif [[ -d /usr/local/etc/bash_completion.d/ ]] && [[ -w /usr/local/etc/bash_completion.d/ ]] 2>/dev/null; then
    print_info "Installing to /usr/local/etc/bash_completion.d/..."
    cp "$COMPLETION_FILE" /usr/local/etc/bash_completion.d/install-agents
    print_success "Installed local system completion"
else
    print_warning "No system completion directory available or not writable"
fi

echo
print_success "Setup complete! Try typing 'install-agents <TAB>' to test completion"
echo
print_info "Available completions:"
echo "  • Command options: --help, --symlink, --profile, etc."
echo "  • Profile names: development-team, core, backend-focus, etc."
echo "  • Agent names: code-reviewer, debugger, test-automator, etc."
echo "  • Directory paths for target projects"
echo
print_info "Examples to test:"
echo "  install-agents --<TAB>           # Show all options"
echo "  install-agents --profile <TAB>   # Show available profiles"  
echo "  install-agents --symlink --<TAB> # Show symlink options"
echo "  install-agents /path/to/<TAB>    # Complete directory paths"