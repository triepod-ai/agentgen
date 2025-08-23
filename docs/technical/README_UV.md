# AgentGen UV Wrapper

🚀 Modern Python wrapper for the AI Agent Generation System using UV for fast dependency management and enhanced developer experience.

## Quick Start

### 1. Install UV (if not already installed)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
```

### 2. Setup AgentGen with UV
```bash
# Option 1: Use the standalone wrapper
./uv-wrapper.py setup

# Option 2: Install as a package
uv pip install -e .
agentgen setup
```

### 3. Install Agents
```bash
# Using the wrapper
./uv-wrapper.py install /path/to/project --all

# Using the installed CLI
agentgen install /path/to/project --all
```

## Features

### 🔧 Enhanced CLI Interface
- **Rich Terminal UI**: Beautiful, colored output with progress indicators
- **Command Validation**: Input validation and helpful error messages  
- **Tab Completion**: Shell completion for commands and options
- **Development Mode**: Enhanced development tools and utilities

### ⚡ Performance Optimizations
- **UV Integration**: 10-100x faster dependency resolution vs pip
- **Environment Isolation**: Clean, reproducible environments
- **Parallel Operations**: Concurrent agent processing where possible
- **Caching**: Intelligent caching of agent configurations and dependencies

### 🛠️ Developer Experience
- **Type Safety**: Full type hints and Pydantic models where available
- **Error Handling**: Comprehensive error handling with actionable messages
- **Development Tools**: Built-in development utilities and debugging
- **Export/Import**: Agent configuration export for backup and sharing

## Usage Examples

### Basic Operations
```bash
# Setup environment
agentgen setup --dev

# Check system status
agentgen status --check-deps --check-git --check-speak

# List available agents
agentgen list

# Install specific agents
agentgen install /path/to/project code-reviewer debugger

# Install from profile
agentgen install /path/to/project --profile development-team
```

### Development Workflow
```bash
# Development mode with live reloading
agentgen dev --dev --watch

# Run project scripts with UV environment
agentgen run test-agent-builder
agentgen run install-default-agents

# Export agent configurations
agentgen export --output agents_backup.json --format json
```

### Agent Management
```bash
# View agent profiles
agentgen profiles

# Show specific profile details
agentgen show-profile development-team

# Install simple single-tool agents
agentgen install /path/to/project --simple
agentgen install /path/to/project --simple-read --simple-bash
```

## Architecture

### UV Integration Benefits
1. **Fast Dependency Resolution**: 10-100x faster than pip
2. **Reproducible Environments**: Lock files ensure consistency  
3. **Project Isolation**: Each project gets its own environment
4. **Modern Tooling**: Built-in formatting, linting, testing

### Component Structure
```
agentgen/
├── agentgen/
│   ├── __init__.py          # Package initialization
│   ├── cli.py               # Rich CLI interface
│   ├── core.py              # Core agent management
│   └── utils.py             # Utility functions
├── pyproject.toml           # UV project configuration
├── uv-wrapper.py            # Standalone launcher
└── README_UV.md            # This documentation
```

### Integration Points
- **Existing Shell Scripts**: Seamless integration with install-agents
- **Agent Configurations**: Enhanced parsing and validation
- **Git Submodules**: Automatic submodule management
- **Speak Integration**: TTS notification support

## Configuration

### Project Setup (pyproject.toml)
```toml
[project]
name = "agentgen"
version = "0.2.0"
dependencies = [
    "redis>=4.0.0",
    "requests>=2.28.0", 
    "openai>=1.0.0",
    "pyttsx3>=2.90",
    "psutil>=5.9.0",
    "click>=8.0.0",
    "rich>=13.0.0",
    "pydantic>=2.0.0",
    "pyyaml>=6.0.0"
]

[project.scripts]
agentgen = "agentgen.cli:main"
```

### Development Dependencies
```bash
# Install with development dependencies
agentgen setup --dev

# Includes: pytest, black, ruff, mypy
```

## Commands Reference

### Setup & Installation
- `agentgen setup [--dev]` - Setup environment with UV
- `agentgen install <target> [agents...] [options]` - Install agents
- `agentgen status [--check-*]` - System health check

### Agent Management  
- `agentgen list` - List all available agents
- `agentgen profiles` - List agent profiles
- `agentgen show-profile <name>` - Show profile details
- `agentgen export [--output] [--format]` - Export configurations

### Development Tools
- `agentgen dev [--dev] [--watch]` - Development mode
- `agentgen run <script> [args...]` - Run scripts with UV environment

### Legacy Compatibility
- `./uv-wrapper.py install-agents [args...]` - Direct script execution
- `./uv-wrapper.py test-agent-builder.sh` - Run existing scripts

## Migration Guide

### From Shell Scripts to UV Wrapper

**Before:**
```bash
./install-agents --all /path/to/project
./install-agents --list
./install-agents --profile development-team /path/to/project
```

**After (UV Wrapper):**
```bash
agentgen install /path/to/project --all
agentgen list  
agentgen install /path/to/project --profile development-team
```

### Benefits of Migration
1. **Faster Execution**: UV's optimized dependency management
2. **Better Error Messages**: Rich CLI with detailed feedback
3. **Enhanced Features**: Export, development tools, status checking
4. **Future-Proof**: Modern Python tooling and practices

## Troubleshooting

### Common Issues

**UV Not Found:**
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
```

**Dependencies Missing:**
```bash
# Reinstall dependencies
agentgen setup --dev
```

**Git Submodules Not Initialized:**
```bash
# Initialize submodules
git submodule update --init --recursive
# Or let agentgen do it
agentgen setup
```

**Agent Installation Fails:**
```bash
# Check system status
agentgen status --check-deps --check-git

# Use dry-run to diagnose
agentgen install /path/to/project --all --dry-run
```

### Performance Optimization

**For Large Projects:**
```bash
# Use UV's parallel processing
UV_CONCURRENT_DOWNLOADS=10 agentgen install /path/to/project --all

# Enable development mode for faster iteration
agentgen dev --dev
```

**For CI/CD:**
```bash
# Skip interactive prompts
agentgen install /path/to/project --all --force --skip-speak-check
```

## Integration with Existing System

The UV wrapper is designed to **enhance**, not replace, your existing agent system:

### Preserved Functionality
- ✅ All existing shell scripts continue to work
- ✅ Agent configurations remain unchanged
- ✅ Git submodule structure preserved
- ✅ Profile system fully compatible

### Enhanced Features
- ⚡ 10-100x faster dependency management with UV
- 🎨 Rich terminal interface with progress indicators
- 🔍 Enhanced error handling and validation
- 📦 Export/import capabilities for agent configurations
- 🛠️ Development tools and utilities

### Backward Compatibility
```bash
# Original way still works
./install-agents --all /path/to/project

# UV wrapper provides the same interface
./uv-wrapper.py install /path/to/project --all

# Plus enhanced CLI
agentgen install /path/to/project --all
```

This ensures a smooth transition while providing significant performance and usability improvements.