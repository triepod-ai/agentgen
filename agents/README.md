# Central Agent Hub

This directory contains all agents for the agentgen system. Agents are organized by category and can be installed via symlinks to maintain a single source of truth.

## Directory Structure

### Core Agents (Essential)
- `core/` - Essential agents every project needs
- Basic functionality and foundational tools

### Development Agents
- `development/` - Frontend, backend, full-stack development specialists
- Code creation, debugging, and implementation

### Specialist Agents (Deep Expertise)
- `specialists/` - Domain experts with deep knowledge
- Architecture, security, performance, ML specialists

### Infrastructure & DevOps
- `infrastructure/` - Deployment, monitoring, CI/CD, cloud management
- System administration and operations

### Quality & Testing
- `quality/` - Code review, testing, QA automation
- Quality assurance and testing workflows

### Content & Communication
- `content/` - Documentation, writing, localization
- Communication and content creation

### Data & AI
- `data/` - Data processing, AI/ML, database management
- Data workflows and machine learning

### Tools & Utilities
- `tools/` - Specialized tools and utilities
- Screenshot analysis, git management, etc.

### Simple Agents
- `simple/` - Lightweight agents for basic tasks
- Quick operations and minimal resource usage

## Installation

Use the symlink-based installer to deploy agents:

```bash
# Install core agents globally
./install-agents-symlink --global --core

# Install development agents to a project
./install-agents-symlink --project /path/to/project --development

# Install all categories
./install-agents-symlink --global --all
```

## Benefits of Symlink System

- **Single Source of Truth**: All agents maintained here
- **Instant Updates**: Changes propagate immediately
- **Space Efficient**: No file duplication
- **Version Control**: All changes tracked in git
- **Easy Maintenance**: Centralized management

## Agent Format

Each agent should follow the standard format:

```markdown
---
name: agent-name
description: When and how to use this agent
tools: tool1, tool2, tool3
---

# Agent System Prompt

Your detailed system prompt here...
```

## Adding New Agents

1. Choose appropriate category directory
2. Create agent file with `.md` extension
3. Follow naming convention: `agent-name.md`
4. Test locally before committing
5. Update this README if adding new categories