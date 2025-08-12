# Claude Code Agent System Documentation

This document provides references to all agent system documentation and best practices for the agentgen project.

## 🔗 NEW: Symlink-Based Agent Hub System

**[README_SYMLINK_HUB.md](./README_SYMLINK_HUB.md)** - Symlink Management System ⭐⭐⭐
The agentgen repository now serves as the **central hub** for all agents using symbolic links:
- Single source of truth - all agents maintained in one location (`agents/` directory)
- Instant updates - changes propagate immediately to all projects
- Space efficient - ~95% reduction in disk usage (no file duplication)
- **Unified installer**: `./install-agents` now supports both `--symlink` and `--copy` modes
- Legacy installer: `./install-agents-symlink` (standalone symlink-only installer)
- Migration tool: `./migrate-to-symlinks.sh` to convert existing installations
- Full testing suite to verify symlink functionality
- Currently managing 18+ agents across 9 categories (core, development, specialists, etc.)
- Backward compatible with existing copy-based installations

**[SYMLINK_HUB_IMPLEMENTATION_PLAN.md](./SYMLINK_HUB_IMPLEMENTATION_PLAN.md)** - Implementation Details
Complete technical plan for the symlink-based agent hub system:
- Architecture design and directory structure
- Migration strategy from copy-based to symlink-based
- Testing and validation procedures
- Rollback and recovery plans

## 🌐 Global Agents Configuration

**[GLOBAL_AGENTS_SETUP.md](./GLOBAL_AGENTS_SETUP.md)** - Global Agent Management ⭐
Documentation for globally available agents configured via symbolic links in `~/.claude/agents/`:
- 22 specialist agents available across all projects
- Setup instructions for creating global symbolic links
- Precedence rules (project agents override global)
- Management best practices and troubleshooting

## 📚 Core Documentation

### **[README.md](./README.md)** - Main Agent System Overview
Complete overview of the 32 optimized agents with complexity-based model selection:
- Design philosophy based on enterprise patterns
- Usage patterns (@-mention, auto-activation, explicit invocation)
- Complexity system (Green/Yellow/Red tiers)
- Architecture patterns (single-agent and multi-agent coordination)
- Comprehensive agent categories and performance benefits

### **[AGENT_BEST_PRACTICES.md](./AGENT_BEST_PRACTICES.md)** - Enterprise Guidelines ⭐
Comprehensive best practices based on research from Microsoft Azure, Speakeasy, and Databricks:
- Core design principles and complexity-appropriate architecture
- Architecture pattern selection criteria
- Implementation guidelines (security, performance, error handling)
- Testing and validation strategies
- Production deployment guidelines
- Decision framework for pattern selection

### **[PROJECT_STATUS.md](./PROJECT_STATUS.md)** - Current System Status
Real-time project status including:
- Recent session accomplishments
- Agent consolidation results (74 → 32 agents, 57% reduction)
- Complexity-based model implementation
- Performance improvements and optimizations

### **[AGENT_CONSOLIDATION_STRATEGY.md](./AGENT_CONSOLIDATION_STRATEGY.md)** - Consolidation Process
Technical details of the agent consolidation process:
- Consolidation methodology and criteria
- Agent categorization and optimization
- Migration strategy from legacy agents

## Documentation Guidelines
- When creating **documentation**, always create a reference to it in CLAUDE.MD so the AI can find the context of the changes if needed.

### Recent Documentation Updates

- **[COMPLETION_README.md](./COMPLETION_README.md)** - Bash completion for install-agents command with intelligent context-aware suggestions ⭐ (Added: 2025-01-11)
- **[README_SYMLINK_HUB.md](./README_SYMLINK_HUB.md)** - Symlink-based agent hub documentation ⭐⭐⭐ (Added: 2025-01-11)
- **[SYMLINK_HUB_IMPLEMENTATION_PLAN.md](./SYMLINK_HUB_IMPLEMENTATION_PLAN.md)** - Technical implementation plan for symlink system (Added: 2025-01-11)
- **[README_UV.md](./README_UV.md)** - UV Wrapper Documentation ⭐ - Modern Python interface with 10-100x faster dependency management (Added: 2025-01-10)
- **[INSTALL_AGENTS_HELP.md](./INSTALL_AGENTS_HELP.md)** - Comprehensive help documentation for install-agents command (Added: 2025-01-10)
- **[DEFAULT_AGENTS.md](./DEFAULT_AGENTS.md)** - Default agent profiles and configurations (Added: 2025-01-10)
- **[SIMPLE_AGENTS.md](./SIMPLE_AGENTS.md)** - Simple agent profiles for basic tasks (Added: 2025-01-10)
- **[profiles/README.md](./profiles/README.md)** - Agent profiles organization and usage guide (Added: 2025-01-10)

## 🏗️ Architecture Patterns

Based on enterprise research, our agent system supports:

### Single-Agent Patterns
- **Reactive**: Basic input → processing → output (Green agents)
- **Memory-Augmented**: Context-aware processing (Yellow agents)
- **Tool-Using**: MCP integration for external APIs (All tiers)
- **Planning**: Multi-step workflow orchestration (Yellow/Red)
- **Reflection**: Self-improving with feedback loops (Red specialists)

### Multi-Agent Patterns
- **Sequential**: Linear pipeline processing
- **Concurrent**: Parallel processing with aggregation
- **Hierarchical**: Supervisor agents coordinating sub-agents
- **Handoff**: Dynamic delegation between specialists
- **Competitive**: Multiple agents, best result selected

## 🎯 Quick Start Guide

### 0. Setup with Symlinks (NEW - Recommended)
```bash
# UNIFIED INSTALLER with symlinks (recommended)
./install-agents --symlink --global --profile core
./install-agents --symlink --project . --profile development

# Maintenance (symlink mode)
./install-agents --symlink --health
./install-agents --symlink --repair

# Migrate existing installations to symlinks
./migrate-to-symlinks.sh .

# Legacy symlink-only installer (still available)
./install-agents-symlink --project . --profile development
```

### 1. Setup with UV (Alternative)
```bash
# Modern Python interface with UV (10-100x faster)
./uv-wrapper.py setup --dev
agentgen install /path/to/project --all

# Traditional shell interface (still supported)
./install-agents --all /path/to/project
```

### 2. Choose the Right Agent
```bash
# Simple tasks (Green complexity)
@analyze-screenshot extract-data-from-ui
@update-status current-progress

# Standard development (Yellow complexity)
@debug-issue investigate-TypeError
@build-backend create-user-api

# Complex reasoning (Red complexity)
@analyze-performance optimize-system-bottlenecks
@secure-application audit-vulnerabilities
```

### 3. Leverage Orchestration
```bash
# Sequential workflow
analyze-codebase → review-code → deploy-application

# Concurrent processing
Multiple agents analyze different aspects in parallel

# Hierarchical coordination
orchestrate-agents coordinates specialist teams
```

### 4. Follow Best Practices
- Start with single-agent patterns before multi-agent complexity
- Match complexity tier to task requirements
- Use <400 character agent descriptions for optimal performance
- Leverage MCP protocol for external service integration

## 📊 System Benefits

- **3x Faster Loading**: <400 character limit ensures rapid initialization
- **Intelligent Routing**: Complexity-based model selection
- **Better Context**: Optimized prompts preserve main conversation
- **Cost Optimization**: Tiered model usage minimizes token consumption
- **Enterprise Patterns**: Based on Microsoft Azure, Speakeasy, Databricks research
- **NEW: Symlink Efficiency**: Instant updates, no duplication, single source of truth

## 🔧 Agent Categories

### Core Development (8 agents)
`analyze-codebase`, `analyze-performance`, `build-frontend`, `build-backend`, `debug-issue`, `test-automation`, `review-code`, `generate-documentation`

### Infrastructure & DevOps (5 agents)
`deploy-application`, `manage-database`, `configure-environment`, `monitor-system`, `secure-application`

### Content & Communication (4 agents)
`write-content`, `translate-text`, `create-lesson`, `update-status`

### Data & AI (4 agents)
`process-data`, `train-model`, `query-database`, `extract-insights`

### Specialized Tools (5 agents)
`analyze-screenshot`, `manage-git`, `export-context`, `orchestrate-tasks`, `orchestrate-agents`

### Specialist Agents (7 agents)
`python-specialist`, `react-specialist`, `database-specialist`, `architect-specialist`, `security-specialist`, `ml-specialist`, `orchestrate-agents`

## 📋 Legacy Information

### Deprecated Agents
All 70+ legacy agents are preserved in the `/deprecated/` directory for reference and migration support.

### Migration Support
See `AGENT_CONSOLIDATION_STRATEGY.md` for detailed mapping of old agents to new consolidated ones.

## 🔗 External References

- **Microsoft Azure Architecture Center**: AI Agent Orchestration Patterns
- **Speakeasy**: Practical Guide to Agent Architectures  
- **Databricks**: Agent System Design Patterns
- **Model Context Protocol (MCP)**: Tool integration standard

---

**Note**: This documentation reflects enterprise-grade agent architecture patterns and provides practical guidance for building robust, scalable agent systems based on proven industry practices.



## Installed Sub-Agents

This project has specialized AI sub-agents installed from two sources:

### Agent Sources and Access

#### 1. Primary Agent Hub (`/agents/` folder) 
- **Location**: Central repository in `agents/` directory
- **Distribution**: Symlink-based system for instant updates
- **Access**: Direct @-mention (e.g., `@code-reviewer`) or auto-activation
- **Count**: 18+ optimized agents across 9 categories

#### 2. Submodule Agent Collection (`/submodules/claude-code-sub-agents/`)
- **Location**: Git submodule repository
- **Installation**: Via `install-agents` command - copies/symlinks to `.claude/agents/`
- **Access**: **No direct agent access** - submodule is a source repository only
- **Process**: `install-agents` → agents copied to project → then available as regular subagents

### How Submodule Agents Work

**Important**: The submodule itself doesn't provide agent access. Instead:

1. **Installation**: Run `install-agents [options]` to copy agents from submodule
2. **Integration**: Agents become available in your `.claude/agents/` directory
3. **Usage**: Interact with installed agents directly (not the submodule)

```bash
# Install agents from submodule
./install-agents --all .                    # Copy all agents to project
./install-agents --profile development .    # Install development profile

# Then use installed agents normally
@code-reviewer analyze this PR              # Direct @-mention
@agent-organizer coordinate multiple tasks  # Complex workflows
```

### Currently Available Agents

The following agents are installed and available in this project:

- **agent-organizer** (general): Multi-agent workflow coordination
- **analyze-screenshot** (general): Image analysis and UI extraction  
- **api-documenter** (specialization): API documentation generation
- **backend-architect** (development): Server-side architecture design
- **code-reviewer** (quality-testing): Code quality and security review
- **config-reader** (general): Configuration file analysis
- **context-manager** (general): Project context management
- **debugger** (quality-testing): Error investigation and resolution
- **deployment-engineer** (infrastructure): CI/CD and deployment automation
- **documentation-expert** (specialization): Technical writing specialist
- **documentation-hub** (general): Documentation discovery and analysis
- **env-reader** (general): Environment configuration analysis
- **frontend-developer** (development): UI/UX development specialist
- **full-stack-developer** (development): End-to-end application development
- **log-reader** (general): Log analysis and error extraction
- **nextjs-pro** (development): Next.js application specialist
- **readme-reader** (general): README and documentation analysis
- **test-automator** (quality-testing): Automated testing implementation
- **ui-designer** (development): User interface design specialist

### Usage Instructions

**Three Ways to Use Installed Agents:**

1. **@-Mention (Recommended)**: `@agent-name` with task description
2. **Explicit Request**: "Use the [agent-name] to..." 
3. **Auto-Activation**: Describe task naturally - appropriate agent activates

### Examples

```bash
# @-mention usage (primary method)
@code-reviewer analyze this pull request
@debugger investigate the authentication error
@agent-organizer coordinate backend and frontend teams

# Explicit invocation
Use the ui-designer to create a responsive navigation component
Have the security-auditor scan for vulnerabilities

# Multi-agent coordination
@agent-organizer: Use backend-architect for API design, then security-auditor for review
```

### Agent Categories

- **general**: Core utilities and analysis tools
- **development**: Frontend, backend, and full-stack specialists  
- **quality-testing**: Code review, QA, and testing automation
- **infrastructure**: Cloud, DevOps, and deployment engineering
- **specialization**: API documentation and domain expertise

### Best Practices

- **Use @-mentions** for direct, efficient agent invocation
- **Leverage agent-organizer** for complex multi-agent workflows
- **Provide rich context** about your requirements and constraints
- **Trust auto-activation** for optimal agent selection based on task descriptions

---
*Agents sourced from claude-code-sub-agents repository via install-agents command*


# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.