#!/bin/bash
# AgentGen Global Installation Script
# Installs install-agents command globally

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
AGENTGEN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${HOME}/bin"
WRAPPER_PATH="${BIN_DIR}/install-agents"

echo "AgentGen Global Installation"
echo "============================="
echo ""

# Create ~/bin if it doesn't exist
if [[ ! -d "$BIN_DIR" ]]; then
    echo "Creating ${BIN_DIR}..."
    mkdir -p "$BIN_DIR"
fi

# Create the global wrapper script
echo "Installing global wrapper to ${WRAPPER_PATH}..."
cat > "$WRAPPER_PATH" << EOF
#!/bin/bash
# Global wrapper for install-agents command
# Allows running install-agents from anywhere

# AgentGen installation directory
AGENTGEN_DIR="$AGENTGEN_DIR"

# Check if agentgen directory exists
if [[ ! -d "\$AGENTGEN_DIR" ]]; then
    echo "Error: AgentGen directory not found at \$AGENTGEN_DIR" >&2
    exit 1
fi

# Execute the actual install-agents script with all arguments
exec "\$AGENTGEN_DIR/install-agents" "\$@"
EOF

# Make wrapper executable
chmod +x "$WRAPPER_PATH"

echo -e "${GREEN}✓${NC} Global wrapper installed"

# Check if ~/bin is in PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo ""
    echo -e "${YELLOW}⚠${NC}  ${BIN_DIR} is not in your PATH"
    echo ""
    echo "Add this line to your ~/.bashrc or ~/.zshrc:"
    echo ""
    echo "    export PATH=\"\$HOME/bin:\$PATH\""
    echo ""
    echo "Then reload your shell:"
    echo "    source ~/.bashrc"
else
    echo -e "${GREEN}✓${NC} ${BIN_DIR} is in PATH"
fi

# Offer to install bash completion
echo ""
read -p "Install bash completion? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    COMPLETION_DIR="${HOME}/.bash_completion.d"
    mkdir -p "$COMPLETION_DIR"

    # Copy completion script
    if [[ -f "${AGENTGEN_DIR}/install-agents-completion.bash" ]]; then
        cp "${AGENTGEN_DIR}/install-agents-completion.bash" "${COMPLETION_DIR}/"
        echo -e "${GREEN}✓${NC} Bash completion installed"

        # Check if it's sourced in bashrc
        if ! grep -q "bash_completion.d" ~/.bashrc 2>/dev/null; then
            echo ""
            echo "Add this to your ~/.bashrc to enable completion:"
            echo ""
            echo "    # Load bash completions"
            echo "    for completion in ~/.bash_completion.d/*; do"
            echo "        [ -r \"\$completion\" ] && source \"\$completion\""
            echo "    done"
        fi
    else
        echo -e "${YELLOW}⚠${NC}  Completion script not found"
    fi
fi

echo ""
echo -e "${GREEN}Installation complete!${NC}"
echo ""
echo "Usage:"
echo "  install-agents --help"
echo "  install-agents --symlink --profile development-team"
echo "  install-agents --list"
echo ""
echo "Documentation:"
echo "  ${AGENTGEN_DIR}/README.md"
echo "  ${AGENTGEN_DIR}/docs/getting-started/INSTALL_AGENTS_QUICK_START.md"
