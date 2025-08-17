# Install-Agents Complete User Guide

## Table of Contents
- [Overview](#overview)
- [Quick Start](#quick-start)
- [Installation Modes](#installation-modes)
- [Available Profiles](#available-profiles)
- [Command Reference](#command-reference)
- [Real-World Examples](#real-world-examples)
- [Maintenance & Health](#maintenance--health)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Advanced Configuration](#advanced-configuration)

## Overview

The `install-agents` command is your gateway to deploying Claude Code sub-agents across your development environment. With the latest improvements, it features **symlink mode as default**, offering instant updates, space efficiency, and a single source of truth for all agents.

### Key Benefits

- **🔗 Symlink Mode (Default)**: Single source of truth with instant updates
- **⚡ Improved Defaults**: Current directory, force enabled, simplified usage
- **💾 Space Efficient**: ~95% reduction in disk usage vs copying
- **🚀 Instant Propagation**: Changes to agents hub immediately available everywhere
- **🔄 Legacy Support**: Copy mode still available for backward compatibility
- **🎨 Rich Terminal UI**: Beautiful, colored output with progress indicators
- **📦 Comprehensive Profiles**: Pre-configured agent sets for different teams
- **🔍 Health Monitoring**: Built-in health checks and repair functionality

## Quick Start

### Prerequisites
⚠️ **CRITICAL**: Must run from `/home/bryan/agentgen/` directory

```bash
# Always start here
cd /home/bryan/agentgen
```

### 30-Second Setup

```bash
# Most common: Install core agents to current directory
./install-agents --profile core

# Full development team setup
./install-agents --profile development-team

# Install to specific project
./install-agents --profile development-team /path/to/my-project
```

### Verify Installation

```bash
# Check what was installed
./install-agents --list-installed .

# Health check for symlinks
./install-agents --health
```

## Installation Modes

### Symlink Mode (DEFAULT - Recommended)

**Benefits:**
- Single source of truth in `/home/bryan/agentgen/agents/`
- Instant updates when agents are modified
- 95% less disk space usage
- Easy maintenance and updates

**How it works:**
- Creates symbolic links from projects to central hub
- All projects share the same agent files
- Modifications to hub instantly affect all projects

```bash
# Symlink mode (default behavior)
./install-agents --profile development-team

# Explicit symlink mode
./install-agents --symlink --profile development-team
```

### Copy Mode (Legacy)

**Benefits:**
- Independent files per project
- No dependencies on central hub
- Projects isolated from each other

**Trade-offs:**
- Manual updates required for each project
- More disk space usage
- Potential inconsistencies between projects

```bash
# Copy mode for backward compatibility
./install-agents --copy --profile development-team /path/to/project
```

### Global Installation

Install agents globally for all projects:

```bash
# Core agents available everywhere
./install-agents --global --profile core

# Check global installation
./install-agents --list-installed ~/.claude/agents
```

## Available Profiles

Profiles are pre-configured sets of agents designed for specific teams and workflows:

| Profile | Agents | Description | Best For |
|---------|--------|-------------|----------|
| **core** | 15 essential agents | Core development toolkit | All projects |
| **development-team** | 20+ agents | Complete development team | Full-stack teams |
| **frontend-focus** | UI/UX specialists | Frontend development | React/Vue/Angular teams |
| **backend-focus** | API & infrastructure | Backend development | API/service teams |
| **ai-ml-team** | Data science & ML | AI/ML development | Data science teams |
| **security-audit** | Security specialists | Security assessment | Security-focused teams |
| **simple-tools** | Single-tool agents | Ultra-fast agents | Lightweight setups |

### Profile Details

```bash
# See all available profiles
./install-agents --list-profiles

# See what's in a specific profile
./install-agents --show-profile development-team

# Example output:
# Profile: development-team
# Description: Complete development team with architecture, development, QA, and coordination agents
# Agents to be installed:
#   - architect-specialist
#   - build-backend
#   - build-frontend
#   - code-reviewer
#   - debugger
#   - ...
```

## Command Reference

### Basic Commands

| Command | Description | Example |
|---------|-------------|---------|
| `--profile <name>` | Install profile | `./install-agents --profile core` |
| `--all` | Install all agents | `./install-agents --all` |
| `agent-names...` | Install specific agents | `./install-agents code-reviewer test-automator` |

### Mode Selection

| Command | Description | Example |
|---------|-------------|---------|
| `--symlink` | Use symlink mode (DEFAULT) | `./install-agents --symlink --profile core` |
| `--copy` | Use copy mode (legacy) | `./install-agents --copy --profile core` |
| `--global` | Install globally | `./install-agents --global --profile core` |
| `--project <path>` | Specify project directory | `./install-agents --project /path/to/project` |

### Information Commands

| Command | Description | Example |
|---------|-------------|---------|
| `--list` | Show all available agents | `./install-agents --list` |
| `--list-profiles` | Show all profiles | `./install-agents --list-profiles` |
| `--show-profile <name>` | Show profile details | `./install-agents --show-profile core` |
| `--list-installed <path>` | Show installed agents | `./install-agents --list-installed .` |

### Utility Commands

| Command | Description | Example |
|---------|-------------|---------|
| `--dry-run` | Preview installation | `./install-agents --dry-run --profile core` |
| `--verbose` | Detailed output | `./install-agents --verbose --profile core` |
| `--health` | Check symlink health | `./install-agents --health` |
| `--repair` | Repair broken symlinks | `./install-agents --repair` |
| `--force` | Force overwrite (DEFAULT) | Already enabled by default |

### Simple Agents

| Command | Description | Example |
|---------|-------------|---------|
| `--simple` | All simple agents | `./install-agents --simple` |
| `--simple-read` | Read-based agents | `./install-agents --simple-read` |
| `--simple-write` | Write-based agents | `./install-agents --simple-write` |
| `--simple-bash` | Bash-based agents | `./install-agents --simple-bash` |
| `--simple-grep` | Grep-based agents | `./install-agents --simple-grep` |
| `--simple-edit` | Edit-based agents | `./install-agents --simple-edit` |

## Real-World Examples

### New Project Setup

```bash
cd /home/bryan/agentgen

# Quick start with core agents
./install-agents --profile core

# Full development environment
./install-agents --profile development-team

# Specific project setup
./install-agents --profile development-team /path/to/new-project

# Preview before installing
./install-agents --dry-run --profile development-team
```

### Team-Specific Configurations

```bash
# Frontend team setup
./install-agents --profile frontend-focus /path/to/ui-project

# Backend team setup
./install-agents --profile backend-focus /path/to/api-project

# AI/ML research team
./install-agents --profile ai-ml-team /path/to/ml-project

# Security-focused project
./install-agents --profile security-audit /path/to/secure-app
```

### Global vs Project-Specific

```bash
# Install core agents globally (available everywhere)
./install-agents --global --profile core

# Install specialized agents per project
./install-agents --profile frontend-focus /path/to/frontend-app
./install-agents --profile backend-focus /path/to/backend-api
./install-agents --profile ai-ml-team /path/to/ml-pipeline
```

### Individual Agent Management

```bash
# Install specific agents to current directory
./install-agents code-reviewer security-auditor

# Install to specific project
./install-agents code-reviewer test-automator /path/to/project

# Add more agents to existing installation
./install-agents performance-engineer /path/to/existing-project
```

### Legacy Copy Mode Usage

```bash
# When you need isolated agent copies
./install-agents --copy --profile development-team /path/to/isolated-project

# Copy specific agents
./install-agents --copy code-reviewer security-auditor /path/to/project

# Useful for:
# - Projects with specific agent versions
# - Offline environments
# - Testing agent modifications
```

## Maintenance & Health

### Health Monitoring

```bash
# Check health of symlinks in current directory
./install-agents --health

# Check specific project
./install-agents --list-installed /path/to/project

# Example health check output:
# [INFO] Checking health of symlinks in: /path/to/project/.claude/agents
# ✓ code-reviewer -> /home/bryan/agentgen/agents/quality/code-reviewer.md
# ✓ debugger -> /home/bryan/agentgen/agents/quality/debugger.md
# ✗ old-agent -> /home/bryan/agentgen/agents/deprecated/old-agent.md (BROKEN)
# Health check complete: 15 working, 1 broken out of 16 total symlinks
```

### Repair Operations

```bash
# Repair broken symlinks
./install-agents --repair

# Preview repairs (dry run)
./install-agents --dry-run --repair

# Force reinstall everything
./install-agents --profile development-team  # Force is enabled by default
```

### Update Workflows

```bash
# Update all agents in current project
./install-agents --profile development-team

# Update specific agent
./install-agents code-reviewer

# Update with verbose output
./install-agents --verbose --profile development-team

# Preview updates
./install-agents --dry-run --profile development-team
```

## Troubleshooting

### Common Issues and Solutions

#### Must Run from agentgen Directory

**Problem:** Script fails or agents not found
```bash
# ❌ Wrong
cd /some/other/directory
./install-agents --profile core

# ✅ Correct
cd /home/bryan/agentgen
./install-agents --profile core
```

#### Agent Not Found

**Problem:** Specific agent doesn't appear after installation

**Solutions:**
```bash
# Check if agents hub exists
ls -la /home/bryan/agentgen/agents/

# List available agents
./install-agents --list

# Verify symlink health
./install-agents --health

# Check specific agent location
find /home/bryan/agentgen/agents/ -name "agent-name.md"
```

#### Permission Errors

**Problem:** Permission denied during installation

**Solutions:**
```bash
# Check script permissions
chmod +x /home/bryan/agentgen/install-agents

# Verify target directory permissions
ls -la /path/to/project/.claude/

# Create directory if needed
mkdir -p /path/to/project/.claude/agents

# For global installation
mkdir -p ~/.claude/agents
./install-agents --global --profile core
```

#### Symlink Issues

**Problem:** Broken symlinks or agents not updating

**Solutions:**
```bash
# Check symlink health
./install-agents --health

# Repair broken symlinks
./install-agents --repair

# Reinstall with force (default behavior)
./install-agents --profile development-team

# Fall back to copy mode if needed
./install-agents --copy --profile development-team
```

#### Hub Directory Issues

**Problem:** Agents hub not found

**Solutions:**
```bash
# Check if hub exists
ls -la /home/bryan/agentgen/agents/

# If missing, the script will fall back to copy mode
# Or reinitialize the repository:
cd /home/bryan/agentgen
git pull origin main
```

### Debugging Commands

```bash
# Verbose installation
./install-agents --verbose --profile development-team

# Dry run to see what would happen
./install-agents --dry-run --profile development-team

# Check current installation
./install-agents --list-installed .

# Health check with details
./install-agents --health

# List all available options
./install-agents --help
```

### Environment Variables

Control behavior with environment variables:

```bash
# Disable colors
NO_COLOR=1 ./install-agents --profile core

# Force colors
FORCE_COLOR=1 ./install-agents --profile core

# Disable text-to-speech
TTS_ENABLED=false ./install-agents --profile core

# Skip speak command check
./install-agents --skip-speak-check --profile core
```

## Best Practices

### Installation Strategy

1. **Start with Global Core Agents**
   ```bash
   ./install-agents --global --profile core
   ```

2. **Use Project-Specific Profiles**
   ```bash
   ./install-agents --profile frontend-focus /path/to/ui-project
   ./install-agents --profile backend-focus /path/to/api-project
   ```

3. **Preview Before Installing**
   ```bash
   ./install-agents --dry-run --profile development-team
   ```

4. **Use Symlink Mode for Teams**
   - Enables instant updates across all projects
   - Maintains consistency across team members

### Team Collaboration

1. **Document Team Standards**
   ```markdown
   # Team Setup Instructions
   cd /home/bryan/agentgen
   ./install-agents --global --profile core
   ./install-agents --profile development-team
   ```

2. **Version Control Integration**
   - Include `.claude/agents/` in your repository (for symlinks)
   - Document agent setup in project README
   - Use consistent profiles across team members

3. **Onboarding New Team Members**
   ```bash
   # Standard team setup
   cd /home/bryan/agentgen
   ./install-agents --global --profile core
   ./install-agents --profile development-team /path/to/team-project
   ```

### Maintenance Routine

1. **Regular Health Checks**
   ```bash
   # Weekly health check
   ./install-agents --health
   
   # Repair if needed
   ./install-agents --repair
   ```

2. **Update Strategy**
   ```bash
   # Update all projects when agents change
   # (Automatic with symlink mode!)
   
   # For copy mode projects, force update:
   ./install-agents --copy --profile development-team /path/to/project
   ```

3. **Monitor Agent Usage**
   ```bash
   # Check what's installed
   ./install-agents --list-installed /path/to/project
   
   # Remove unused agents
   rm /path/to/project/.claude/agents/unused-agent.md
   ```

## Advanced Configuration

### Custom Profiles

Create custom profiles in `/home/bryan/agentgen/profiles/`:

```yaml
# my-team.profile
name: my-team
description: Custom profile for our development team
agents:
  - code-reviewer
  - security-auditor
  - performance-engineer
  - frontend-developer
  - backend-architect
```

Usage:
```bash
./install-agents --profile my-team
```

### Environment Configuration

Set up environment variables in `~/.bashrc` or `~/.bash_profile`:

```bash
# Agent installation preferences
export FORCE_COLOR=1
export TTS_ENABLED=true
export AGENTGEN_DEFAULT_PROFILE=development-team

# Aliases for common operations
alias install-core='cd /home/bryan/agentgen && ./install-agents --profile core'
alias install-dev='cd /home/bryan/agentgen && ./install-agents --profile development-team'
alias agent-health='cd /home/bryan/agentgen && ./install-agents --health'
alias agent-repair='cd /home/bryan/agentgen && ./install-agents --repair'
```

### CI/CD Integration

For automated deployments:

```bash
#!/bin/bash
# deploy-agents.sh

set -e

# Navigate to agentgen
cd /home/bryan/agentgen

# Disable colors and TTS for CI
export NO_COLOR=1
export TTS_ENABLED=false

# Install agents
./install-agents --skip-speak-check --profile "${AGENT_PROFILE:-development-team}" "${PROJECT_PATH}"

# Verify installation
./install-agents --list-installed "${PROJECT_PATH}"
```

### Hub Management

Update agents in the central hub:

```bash
# Navigate to hub
cd /home/bryan/agentgen/agents

# Modify agents
vim core/code-reviewer.md

# Changes are instantly available to all symlinked projects!

# For copy mode projects, update manually:
cd /home/bryan/agentgen
./install-agents --copy code-reviewer /path/to/copy-mode-project
```

### Migration Strategies

#### From Copy Mode to Symlink Mode

```bash
# 1. Backup existing installation
cp -r /path/to/project/.claude/agents /path/to/project/.claude/agents.backup

# 2. Remove copied agents
rm -rf /path/to/project/.claude/agents/*

# 3. Install with symlink mode
./install-agents --profile development-team /path/to/project

# 4. Verify installation
./install-agents --list-installed /path/to/project
./install-agents --health
```

#### Bulk Project Updates

```bash
#!/bin/bash
# update-all-projects.sh

PROJECTS=(
    "/path/to/project1"
    "/path/to/project2"
    "/path/to/project3"
)

cd /home/bryan/agentgen

for project in "${PROJECTS[@]}"; do
    echo "Updating $project"
    ./install-agents --profile development-team "$project"
    ./install-agents --list-installed "$project"
done
```

---

## Summary

The `install-agents` command provides a powerful, flexible system for managing Claude Code sub-agents. With symlink mode as the new default, you get:

- **Instant updates** across all projects
- **Space efficiency** with 95% less disk usage
- **Single source of truth** for all agent management
- **Backward compatibility** with copy mode
- **Rich profile system** for team-specific setups

Start with `./install-agents --profile core` and expand from there based on your team's needs!