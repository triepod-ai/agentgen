# Claude Code Sub-Agents Installation Guide

## Overview

The `install-agents` command provides a powerful, flexible system for installing and managing Claude Code sub-agents across your development environment. With UV wrapper integration, this tool offers enhanced performance, rich terminal output, and multiple usage patterns.

### 🚀 Key Enhancements
- **UV Wrapper**: 10-100x faster dependency resolution
- **Rich Terminal UI**: Beautiful, colored output with progress indicators
- **Multiple Installation Methods**: 
  - Standalone wrapper
  - Installed CLI
  - Traditional shell script
- **Advanced Color Control**: Environment variable-based color management
- **Comprehensive Error Handling**: Actionable error messages and system status checks

## Installation Options

### Basic Usage
```bash
# Install all available agents
install-agents --all

# List available agents without installing
install-agents --list

# Perform a dry run to see what would be installed
install-agents --dry-run
```

### Advanced Installation Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--all` | Install all agents across categories | `install-agents --all` |
| `--list` | Show available agents without installing | `install-agents --list` |
| `--dry-run` | Simulate installation, show what would happen | `install-agents --dry-run` |
| `--force` | Force reinstallation of existing agents | `install-agents --force` |
| `--verbose` | Provide detailed installation logs | `install-agents --verbose` |
| `--skip-speak-check` | Skip text-to-speech configuration check | `install-agents --skip-speak-check` |
| `--profile` | Install agents from a predefined profile | `install-agents --profile development-team` |

### Color and Terminal Control

The `install-agents` system now supports advanced color and terminal output control through environment variables:

| Variable | Description | Values | Default |
|----------|-------------|--------|---------|
| `FORCE_COLOR` | Force colored output | `0`, `1` | Automatic |
| `NO_COLOR` | Disable all colored output | `1` | Color Enabled |
| `CLICOLOR_FORCE` | Force color in non-interactive environments | `1` | Automatic |

## Agent Categories

### 1. Development Agents
- Analyze, build, debug, review, and document code
- Best for software engineering workflows
- **Example**: `@build-backend`, `@review-code`

### 2. Infrastructure & DevOps
- Manage deployments, databases, environments
- Ideal for system configuration and monitoring
- **Example**: `@deploy-application`, `@configure-environment`

### 3. Data & AI
- Process data, train models, extract insights
- Perfect for data science and machine learning projects
- **Example**: `@process-data`, `@train-model`

### 4. Security Agents
- Conduct security audits, vulnerability assessments
- Critical for enterprise-level security compliance
- **Example**: `@secure-application`, `@security-specialist`

### 5. Specialized Tools
- Screenshot analysis, Git management, context export
- Targeted agents for specific technical tasks
- **Example**: `@manage-git`, `@analyze-screenshot`

## Real-World Usage Examples

### 1. New Project Setup
```bash
# Install all agents for a comprehensive toolkit
install-agents --all           # Traditional Method
./uv-wrapper.py install /path/to/project --all    # UV Wrapper
agentgen install /path/to/project --all           # Installed CLI
```

### 2. Selective Installation
```bash
# Install only development and security agents
install-agents --dev --security                   # Traditional Method
agentgen install /path/to/project --profile development-team   # Profile-based
```

### 3. Update Existing Agents
```bash
# Force update all installed agents
install-agents --all --force                   # Traditional Method
agentgen install /path/to/project --all --force   # UV Wrapper/CLI

# Perform a dry run to preview updates
install-agents --all --dry-run --verbose       # Traditional Method
agentgen install /path/to/project --all --dry-run --verbose  # Enhanced Method
```

### 4. Performance Optimization
```bash
# Enable parallel downloads (UV Wrapper)
UV_CONCURRENT_DOWNLOADS=10 agentgen install /path/to/project --all

# Disable color for CI/CD environments
NO_COLOR=1 install-agents --all --force
```

## Troubleshooting

### Common Issues

#### Agent Not Found
- **Symptom**: Specific agent doesn't appear after installation
- **Solutions**: 
  1. Verify submodule is correctly initialized
     ```bash
     git submodule update --init --recursive
     ```
  2. Check `/home/bryan/agentgen/submodules/claude-code-sub-agents`
  3. Confirm agent availability:
     ```bash
     install-agents --list       # Traditional Method
     agentgen list                # UV Wrapper/CLI
     ```

#### Permission Errors
- **Symptom**: Permission denied during installation
- **Solutions**:
  1. Use `sudo` for system-wide installation
     ```bash
     sudo install-agents --all
     sudo agentgen install /path/to/project --all
     ```
  2. Check and fix file permissions
     ```bash
     chmod +x /home/bryan/bin/install-agents
     chmod +x ./uv-wrapper.py
     ```
  3. Verify script executability and Python environment

#### Dependency Issues
- **Symptom**: Missing dependencies or environment problems
- **Solutions**:
  1. Install UV (recommended)
     ```bash
     curl -LsSf https://astral.sh/uv/install.sh | sh
     source ~/.bashrc
     ```
  2. Setup project environment
     ```bash
     ./uv-wrapper.py setup
     agentgen setup --dev
     ```

#### Text-to-Speech Configuration
- **Symptom**: Speak integration issues
- **Solutions**: 
  1. Skip TTS configuration
     ```bash
     install-agents --skip-speak-check
     agentgen install --skip-speak-check
     ```
  2. Control TTS via environment variables
     ```bash
     TTS_ENABLED=false install-agents --all
     TTS_PROVIDER=pyttsx3 agentgen install /path/to/project
     ```
  3. Configure in `~/.bash_aliases`

#### Color and Terminal Issues
- **Symptom**: Incorrect terminal colors or display problems
- **Solutions**:
  1. Force color mode
     ```bash
     FORCE_COLOR=1 install-agents
     ```
  2. Disable color for CI/CD
     ```bash
     NO_COLOR=1 agentgen install /path/to/project
     ```
  3. Debug terminal compatibility
     ```bash
     agentgen status --check-terminal
     ```

## Best Practices

1. **Regular Updates**: Keep agents updated for latest features
2. **Selective Installation**: Install only necessary agents
3. **Dry Run First**: Always preview changes with `--dry-run`
4. **Force with Caution**: Use `--force` sparingly
5. **Verbose Mode**: Enable detailed logging during complex installations

## Configuration

Agents are managed via a git submodule at:
`/home/bryan/agentgen/submodules/claude-code-sub-agents`

Agent documentation is automatically updated in `CLAUDE.md` during installation.

## Support

For issues or agent suggestions:
- Check GitHub repository
- File an issue at support@claude.ai
- Join our developer community slack

---

**Tip**: The `install-agents` command is designed to be flexible, fast, and developer-friendly. Experiment and find the workflow that suits your needs!