#!/bin/bash

# Quick installer for the development team profile
# Installs the complete development team for full-stack projects

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get target project (default to current directory)
TARGET_PROJECT="${1:-.}"

echo ""
echo "🏗️  Installing Development Team Profile"
echo "=================================="
echo ""
echo "This will install a complete development team including:"
echo "• Infrastructure & Architecture agents"
echo "• Development & Design agents (including analyze-screenshot)"  
echo "• Quality & Documentation agents"
echo "• Coordination agents"
echo ""

# Convert to absolute path and validate
TARGET_PROJECT="$(cd "$TARGET_PROJECT" 2>/dev/null && pwd)" || {
    echo -e "${YELLOW}[WARNING]${NC} Target project path does not exist: $1"
    echo "Creating directory: $1"
    mkdir -p "$1"
    TARGET_PROJECT="$(cd "$1" && pwd)"
}

echo -e "${BLUE}[INFO]${NC} Target project: $TARGET_PROJECT"
echo ""

# Run the installation
if ./install-agents-enhanced.sh --profile development-team "$TARGET_PROJECT"; then
    echo ""
    echo "🎉 Development team installation complete!"
    echo ""
    echo "Your team is ready to use:"
    echo "• @cloud-architect - Infrastructure design and planning"
    echo "• @deployment-engineer - CI/CD and deployment automation"
    echo "• @ui-designer - User interface design and prototyping"
    echo "• @frontend-developer - Client-side development and optimization"
    echo "• @full-stack-developer - End-to-end application development"
    echo "• @analyze-screenshot - Visual analysis and UI extraction"
    echo "• @code-reviewer - Code quality and best practices review"
    echo "• @debugger - Bug investigation and resolution"
    echo "• @qa-expert - Testing strategy and quality assurance"
    echo "• @agent-organizer - Multi-agent workflow coordination"
    echo ""
    echo "Happy coding! 🚀"
else
    echo "❌ Installation failed. Check the output above for details."
    exit 1
fi
