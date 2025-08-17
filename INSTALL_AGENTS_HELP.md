# Claude Code Sub-Agents Installation Guide

## Overview

The `install-agents` command provides a powerful, flexible system for installing and managing Claude Code sub-agents across your development environment. The tool now features **symlink mode as default**, offering instant updates, space efficiency, and a single source of truth for all agents.

### 🚀 Key Features
- **Symlink Mode (DEFAULT)**: Single source of truth with instant updates
- **Improved Defaults**: Current directory, force enabled, simplified usage
- **Space Efficient**: ~95% reduction in disk usage vs copying
- **Instant Propagation**: Changes to agents hub immediately available everywhere
- **Legacy Support**: Copy mode still available for backward compatibility
- **Rich Terminal UI**: Beautiful, colored output with progress indicators
- **Comprehensive Profiles**: Pre-configured agent sets for different teams
- **Health Monitoring**: Built-in health checks and repair functionality

## Quick Start

### ⚠️ IMPORTANT: Must run from agentgen directory
The `install-agents` script must be run from `/home/bryan/agentgen/` directory.

```bash
# Navigate to agentgen first
cd /home/bryan/agentgen

# SIMPLE USAGE (NEW DEFAULTS - current directory, symlink mode, force enabled)
./install-agents --profile development-team
./install-agents --profile core
./install-agents code-reviewer test-automator

# EXPLICIT PROJECT PATH
./install-agents --profile development-team /path/to/my-project
./install-agents --project /path/to/my-project --profile core

# LEGACY COPY MODE (for backward compatibility)
./install-agents --copy --profile development-team /path/to/my-project

# GLOBAL INSTALLATION (symlink mode only)
./install-agents --symlink --global --profile core
```

### Installation Modes

#### Symlink Mode (DEFAULT - Recommended)
- **Single source of truth**: All agents maintained in one hub location
- **Instant updates**: Changes propagate immediately to all projects
- **Space efficient**: ~95% reduction in disk usage
- **Easy maintenance**: Update once, deploy everywhere

#### Copy Mode (Legacy)
- **Independent files**: Each project has its own agent copies
- **Isolation**: Projects don't affect each other
- **Backup compatibility**: Works without central hub

## Command Reference

### Installation Mode Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--symlink` | Use symlink-based installation (DEFAULT) | `./install-agents --symlink --profile core` |
| `--copy` | Use copy-based installation (legacy) | `./install-agents --copy --profile core` |
| `--project <path>` | Install to specific project directory | `./install-agents --project /path/to/project` |
| `--global` | Install globally (symlink mode only) | `./install-agents --global --profile core` |

### Content Selection Flags

| Flag | Description | Example |
|------|-------------|---------||
| `--profile <name>` | Install agents from a predefined profile | `./install-agents --profile development-team` |
| `--all` | Install all available agents | `./install-agents --all` |
| `--simple` | Install all simple single-tool agents | `./install-agents --simple` |
| `agent-names...` | Install specific named agents | `./install-agents code-reviewer test-automator` |

### Utility Flags

| Flag | Description | Example |
|------|-------------|---------||
| `--list` | Show available agents without installing | `./install-agents --list` |
| `--list-profiles` | Show available profiles | `./install-agents --list-profiles` |
| `--show-profile <name>` | Show details of specific profile | `./install-agents --show-profile development-team` |
| `--list-installed <path>` | List agents in target project | `./install-agents --list-installed /path/to/project` |
| `--dry-run` | Simulate installation, show what would happen | `./install-agents --dry-run --profile core` |
| `--verbose` | Provide detailed installation logs | `./install-agents --verbose --profile core` |
| `--force` | Force reinstallation (DEFAULT - enabled) | `./install-agents --profile core` |
| `--skip-speak-check` | Skip text-to-speech configuration check | `./install-agents --skip-speak-check` |

### Maintenance Flags (Symlink Mode Only)

| Flag | Description | Example |
|------|-------------|---------||
| `--health` | Check health of existing symlinks | `./install-agents --health` |
| `--repair` | Repair broken symlinks | `./install-agents --repair` |

### Color and Terminal Control

The `install-agents` system now supports advanced color and terminal output control through environment variables:

| Variable | Description | Values | Default |
|----------|-------------|--------|---------|
| `FORCE_COLOR` | Force colored output | `0`, `1` | Automatic |
| `NO_COLOR` | Disable all colored output | `1` | Color Enabled |
| `CLICOLOR_FORCE` | Force color in non-interactive environments | `1` | Automatic |

## Available Profiles

Profiles are pre-configured sets of agents designed for specific teams and workflows:

### Core Profiles
- **`core`**: Essential 15-agent profile for all development workflows
- **`development-team`**: Complete team with architecture, development, QA, and coordination
- **`simple-tools`**: Ultra-fast single-tool agents for specific tasks

### Specialized Profiles
- **`frontend-focus`**: UI/UX development and user experience optimization
- **`backend-focus`**: API development, database optimization, and infrastructure
- **`ai-ml-team`**: Data science, model development, and intelligent applications
- **`security-audit`**: Vulnerability assessment and secure development

### Profile Usage
```bash
# View all available profiles
./install-agents --list-profiles

# See what's in a specific profile
./install-agents --show-profile development-team

# Install a profile
./install-agents --profile development-team
```

## Agent Categories

Agents are organized into logical categories for easy discovery:

- **business**: Product management and business analysis
- **data-ai**: Data engineering, AI/ML, and database optimization
- **development**: Frontend, backend, and full-stack development
- **infrastructure**: Cloud, DevOps, and performance engineering
- **quality-testing**: Code review, QA, and testing automation
- **security**: Security auditing and vulnerability assessment
- **specialization**: API documentation and specialized expertise
- **simple**: Ultra-fast single-tool agents for specific tasks

## Real-World Usage Examples

### 1. New Project Setup
```bash
# Navigate to agentgen directory
cd /home/bryan/agentgen

# Install core agents to current directory (NEW DEFAULT)
./install-agents --profile core

# Install to specific project
./install-agents --profile development-team /path/to/my-project

# Install all agents for comprehensive toolkit
./install-agents --all
```

### 2. Team-Specific Setups
```bash
# Frontend team setup
./install-agents --profile frontend-focus /path/to/frontend-project

# Backend team setup
./install-agents --profile backend-focus /path/to/backend-project

# AI/ML team setup
./install-agents --profile ai-ml-team /path/to/ml-project

# Security audit setup
./install-agents --profile security-audit /path/to/secure-project
```

### 3. Global Installation for Core Agents
```bash
# Install core agents globally (available in all projects)
./install-agents --global --profile core

# Check what's installed globally
./install-agents --list-installed ~/.claude/agents
```

### 4. Maintenance and Updates
```bash
# Health check for symlinks
./install-agents --health

# Repair broken symlinks
./install-agents --repair

# Preview what would be updated
./install-agents --dry-run --profile development-team

# Force update existing agents
./install-agents --profile development-team  # Force is enabled by default
```

### 5. Legacy Copy Mode
```bash
# Use copy mode for isolated installations
./install-agents --copy --profile development-team /path/to/project

# Copy mode with specific agents
./install-agents --copy code-reviewer security-auditor /path/to/project
```

### 6. Simple Single-Tool Agents
```bash
# Install ultra-fast simple agents
./install-agents --simple

# Install specific simple agent categories
./install-agents --simple-read --simple-bash
```

## Troubleshooting

### Common Issues

#### Must Run from agentgen Directory
- **Symptom**: Script fails or agents not found
- **Solution**: Always run from `/home/bryan/agentgen/`
  ```bash
  cd /home/bryan/agentgen
  ./install-agents --profile development-team
  ```

#### Agent Not Found
- **Symptom**: Specific agent doesn't appear after installation
- **Solutions**: 
  1. Check if agents hub exists:
     ```bash
     ls -la /home/bryan/agentgen/agents/
     ```
  2. List available agents:
     ```bash
     ./install-agents --list
     ```
  3. Verify symlink health:
     ```bash
     ./install-agents --health
     ```

#### Permission Errors
- **Symptom**: Permission denied during installation
- **Solutions**:
  1. Check script permissions:
     ```bash
     chmod +x /home/bryan/agentgen/install-agents
     ```
  2. Verify target directory permissions:
     ```bash
     ls -la /path/to/project/.claude/
     ```
  3. For global installation:
     ```bash
     mkdir -p ~/.claude/agents
     ./install-agents --global --profile core
     ```

#### Symlink Issues
- **Symptom**: Broken symlinks or agents not updating
- **Solutions**:
  1. Check symlink health:
     ```bash
     ./install-agents --health
     ```
  2. Repair broken symlinks:
     ```bash
     ./install-agents --repair
     ```
  3. Reinstall with force:
     ```bash
     ./install-agents --profile development-team  # Force enabled by default
     ```
  4. Fall back to copy mode:
     ```bash
     ./install-agents --copy --profile development-team
     ```

#### Text-to-Speech Configuration
- **Symptom**: Speak integration warnings or issues
- **Solutions**: 
  1. Skip TTS configuration:
     ```bash
     ./install-agents --skip-speak-check --profile core
     ```
  2. Install speak command:
     ```bash
     # Check if speak is available
     command -v speak
     
     # Install from speak-app if needed
     ls /home/bryan/bin/speak-app/
     ```

#### Color and Terminal Issues
- **Symptom**: Incorrect terminal colors or display problems
- **Solutions**:
  1. Force color mode:
     ```bash
     FORCE_COLOR=1 ./install-agents --profile core
     ```
  2. Disable color for CI/CD:
     ```bash
     NO_COLOR=1 ./install-agents --profile core
     ```
  3. Check terminal capabilities:
     ```bash
     echo $TERM
     ```

## Best Practices

### Installation Strategy
1. **Start with Profiles**: Use predefined profiles rather than individual agents
2. **Symlink Mode**: Prefer symlink mode for easier maintenance
3. **Global Core Agents**: Install core agents globally for all projects
4. **Project-Specific**: Install specialized profiles per project type

### Maintenance
1. **Regular Health Checks**: Run `--health` periodically
2. **Preview Changes**: Use `--dry-run` before major updates
3. **Repair When Needed**: Use `--repair` if symlinks break
4. **Update Hub**: Modify agents in `/home/bryan/agentgen/agents/` for instant updates

### Team Collaboration
1. **Document Profiles**: Record which profiles each project uses
2. **Consistent Setup**: Use same profiles across team members
3. **Version Control**: Include `.claude/` directory in project repos (for symlinks)
4. **Share Configurations**: Document agent setup in project README

## System Architecture

### Symlink Hub System
- **Central Hub**: `/home/bryan/agentgen/agents/` contains all agent source files
- **Instant Updates**: Changes to hub files immediately available in all projects
- **Space Efficiency**: ~95% reduction in disk usage vs copying files
- **Single Source of Truth**: One location to maintain all agents

### Directory Structure
```
/home/bryan/agentgen/
├── install-agents              # Main installer script
├── agents/                     # Central agents hub
│   ├── core/                   # Core agents
│   ├── development/            # Development agents
│   ├── specialists/            # Specialist agents
│   └── ...                     # Other categories
├── profiles/                   # Profile configurations
│   ├── core.profile           # Core profile
│   ├── development-team.profile
│   └── ...                     # Other profiles
└── submodules/                 # Legacy support
    └── claude-code-sub-agents/
```

### Project Integration
- **Agents Directory**: `.claude/agents/` in each project
- **CLAUDE.md**: Automatically updated with agent instructions
- **Symlinks**: Point to central hub for instant updates
- **Health Monitoring**: Built-in checks for symlink integrity

## Advanced Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `FORCE_COLOR` | Force colored output | Auto-detect |
| `NO_COLOR` | Disable all colors | Disabled |
| `TTS_ENABLED` | Enable text-to-speech | true |
| `CLICOLOR_FORCE` | Force color in non-interactive | Auto-detect |

### Custom Profiles
Create custom profiles in `/home/bryan/agentgen/profiles/`:
```yaml
name: my-custom-profile
description: Custom profile for my team
agents:
  - code-reviewer
  - security-auditor
  - performance-engineer
```

## Migration Guide

### From Copy Mode to Symlink Mode
```bash
# 1. Remove existing copied agents
rm -rf /path/to/project/.claude/agents/*

# 2. Install with symlink mode
./install-agents --profile development-team /path/to/project

# 3. Verify installation
./install-agents --list-installed /path/to/project
```

### Updating Legacy Installations
```bash
# Force update with new defaults
./install-agents --profile development-team /path/to/project

# Check health after update
./install-agents --health
```

---

**Note**: The `install-agents` command is designed for simplicity and efficiency. The new symlink-based approach provides instant updates and significant space savings while maintaining full backward compatibility.