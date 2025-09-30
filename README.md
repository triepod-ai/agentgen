# AgentGen - Claude Code AI Agent Management System

**Centralized hub for installing and managing 100+ specialized AI agents for Claude Code.**

## What is AgentGen?

AgentGen is a management and deployment system for Claude Code AI agents. It provides a centralized repository of 100+ specialized agents organized into strategic team profiles, with tools for installation, coordination, and orchestration.

### Key Features

- **🏢 Strategic Team Profiles** - Pre-configured agent teams for different organizational needs
- **⚡ Simple Installation** - One-command deployment from centralized hub  
- **🔗 Symlink Architecture** - Instant updates across all projects, no file duplication
- **🧠 Agent Orchestration** - Coordinate multiple agents for complex workflows
- **📊 Context-Manager Integration** - Project-aware agent coordination and knowledge sharing

## Quick Start

### 1. Navigate to AgentGen Directory
```bash
cd /home/bryan/agentgen  # Required - must run from here
```

### 2. Choose Your Team Profile

**Enterprise Organizations (50+ people)**
```bash
./install-agents --profile enterprise-leadership
# 9 strategic agents: architect-specialist, security-auditor, product-manager, etc.
```

**Modern Web Teams (15-50 people)**  
```bash
./install-agents --profile modern-web-stack
# 12 React/TypeScript specialists: react-specialist, nextjs-pro, ui-designer, etc.
```

**Startups & Small Teams (5-15 people)**
```bash
./install-agents --profile startup-mvp
# 11 lean development agents: full-stack-developer, debugger, test-automator, etc.
```

**General Development**
```bash
./install-agents --profile core
# Essential agents for any project
```

### 3. Start Using Your Agents

```bash
# Orchestrated workflows (recommended)
@orchestrate-tasks "build authentication system with security audit"
@orchestrate-tasks "optimize application performance"

# Direct agent usage  
@security-auditor "scan for vulnerabilities"
@react-specialist "create responsive dashboard"
@architect-specialist "design microservices architecture"
```

**✅ Complete!** Your agents are installed and ready to use.

## Available Agent Categories

| Category | Count | Examples | Use Cases |
|----------|-------|----------|-----------|
| **🏗️ Development** | 21+ | `@react-specialist`, `@full-stack-developer`, `@python-specialist` | Building features, components, APIs |
| **🔵 Infrastructure** | 6+ | `@deployment-engineer`, `@cloud-architect`, `@performance-engineer` | DevOps, deployment, system management |
| **🟦 Quality & Testing** | 14+ | `@code-reviewer`, `@test-automator`, `@debugger` | Code quality, testing, bug fixes |
| **🔴 Security** | 4+ | `@security-auditor`, `@context-manager` | Security audits, vulnerability scanning |
| **🟣 Data & AI** | 11+ | `@ml-specialist`, `@data-engineer`, `@database-specialist` | Data processing, ML, database operations |
| **🟢 Simple Tools** | 30+ | `@analyze-screenshot`, `@config-reader`, `@log-reader` | Utilities, file operations, simple tasks |
| **🟤 Business** | 4+ | `@product-manager`, `@create-lesson`, `@changelog-writer` | Business logic, content, documentation |
| **🟠 Architecture** | 9+ | `@architect-specialist`, `@orchestrate-tasks`, `@agent-organizer` | System design, orchestration |

## Team Profile Comparison

| Profile | Team Size | Focus | Best For |
|---------|-----------|-------|----------|
| **enterprise-leadership** | 50+ | Strategic decisions, compliance, security | C-level decisions, enterprise architecture |
| **modern-web-stack** | 15-50 | React/TypeScript, UI/UX excellence | Modern web applications, component libraries |
| **startup-mvp** | 5-15 | Lean development, rapid prototyping | Fast iteration, resource constraints |
| **core** | Any | Essential development tools | Baseline agents for any project |

## Usage Patterns

### Orchestration (Recommended)
```bash
# Intelligent task coordination
@orchestrate-tasks "comprehensive security audit with modernization"
@orchestrate-tasks "build user authentication with testing"

# Multi-agent coordination for complex projects
@orchestrate-agents-adv "legacy system modernization"
```

### Direct Agent Usage
```bash
# @-mention with auto-complete
@react-specialist "create admin dashboard with real-time updates"
@security-auditor "vulnerability assessment for payment system" 
@debugger "investigate memory leaks in Node.js application"
```

### Auto-Activation
Agents automatically activate based on task descriptions:
```bash
"analyze this screenshot for data extraction"     # → @analyze-screenshot
"review code for security vulnerabilities"       # → @security-auditor
"create responsive React component"               # → @react-specialist
```

## Installation Options

### Symlink Mode (Recommended - Default)
- **Storage Efficient** - No file duplication
- **Instant Updates** - Changes propagate immediately
- **Single Source** - Centralized management

```bash
./install-agents --profile modern-web-stack           # Project installation
./install-agents --global --profile core              # Global installation
```

### Copy Mode (Legacy)
- **Independent Files** - Isolated per project
- **No Hub Dependencies** - Self-contained installations

```bash
./install-agents --copy --profile enterprise-leadership /path/to/project
```

## Additional Commands

```bash
# Health & Maintenance
./install-agents --health                    # Check system integrity
./install-agents --repair                    # Fix broken symlinks
./install-agents --list-profiles             # Show all available profiles
./install-agents --list-installed .          # Show installed agents

# Migration
./migrate-to-symlinks.sh /path/to/project    # Upgrade to symlink mode

# Bash Completion
./setup-completion.sh                        # Enable intelligent auto-complete
```

## System Benefits

- **3x Faster Loading** - Optimized agent initialization (<100ms)
- **Intelligent Routing** - Complexity-based model selection (Green/Yellow/Red tiers)
- **Context Preservation** - Maintains project understanding across agent interactions
- **Cost Optimization** - Tiered model usage minimizes token consumption
- **Enterprise Patterns** - Based on Microsoft Azure, Speakeasy, Databricks research

## Context-Manager Integration

AgentGen includes an operational context-manager system that provides:
- **Project Awareness** - Agents understand your project structure automatically
- **Cross-Agent Coordination** - Shared knowledge and task handoffs
- **Reduced Redundancy** - No need to re-explain project context
- **Activity Tracking** - Monitor multi-agent operations

## Architecture

AgentGen supports both single-agent and multi-agent patterns:

### Single-Agent (80% of use cases)
- Direct specialist expertise
- Fast execution with minimal overhead
- Clear accountability

### Multi-Agent (20% of use cases - Complex scenarios)  
- Cross-domain coordination
- Enterprise-scale workflows
- Quality gates and validation

## Troubleshooting

### Common Issues

**Installation Problems**
```bash
cd /home/bryan/agentgen                     # Must run from agentgen directory
chmod +x ./install-agents                  # Fix permissions
./install-agents --health                  # Check system status
```

**Agent Not Responding**
```bash
./install-agents --list-installed .        # Verify installation
@orchestrate-tasks "test agent functionality"  # Try orchestration
```

**Performance Issues**
```bash
./install-agents --profile core            # Use fewer agents
./migrate-to-symlinks.sh .                 # Upgrade for better performance
```

## Documentation

- **[Quick Start Guide](docs/getting-started/INSTALL_AGENTS_QUICK_START.md)** - 30-second setup
- **[User Guide](docs/getting-started/INSTALL_AGENTS_USER_GUIDE.md)** - Complete usage documentation
- **[Agent Reference](docs/reference/)** - Detailed agent catalog
- **[Advanced Features](docs/advanced/)** - Orchestration and enterprise deployment
- **[Technical Architecture](docs/technical/)** - System design and configuration

## Support

- **GitHub Issues** - Bug reports and feature requests
- **Documentation** - Comprehensive guides and references
- **Health Commands** - Built-in diagnostics and repair tools

---

**Ready to get started?** Choose your team profile and install AgentGen in under 30 seconds.

```bash
cd /home/bryan/agentgen
./install-agents --profile modern-web-stack  # or enterprise-leadership, startup-mvp
```