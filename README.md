# Claude Code Agents - Consolidated Collection

## Overview

This directory contains 32 optimized agents (25 general + 7 specialists) with complexity-based model selection for maximum efficiency. Each agent is optimized for <400 characters and focuses on immediate execution.

## Agent Installation

### Quick Start
```bash
# Install all agents
install-agents --all

# List available agents
install-agents --list

# Detailed installation guide
cat INSTALL_AGENTS_HELP.md
```

### Installation Methods
- **Full Installation**: `install-agents --all`
- **Selective Installation**: `install-agents --dev --security`
- **Dry Run**: `install-agents --dry-run`

See `INSTALL_AGENTS_HELP.md` for comprehensive installation instructions and troubleshooting.

## Design Philosophy

Based on enterprise agent architecture patterns from Microsoft Azure, Speakeasy, and Databricks:

- **Action-First Naming**: Clear action verbs (analyze, build, debug, etc.)
- **<400 Character Limit**: Optimized for fast loading and context efficiency
- **Immediate Execution**: All agents execute workflows immediately upon invocation
- **Specialized Focus**: Single responsibility agents with clear trigger patterns
- **Complexity-Based Models**: Green (haiku), Yellow (sonnet), Red (opus) based on task complexity
- **Orchestration Patterns**: Sequential, concurrent, and hierarchical coordination support
- **Tool Integration**: MCP protocol compatibility for external service access

## Remaining content same as previous README (complexity system, agent categories, architecture patterns, etc.)