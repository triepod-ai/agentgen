# Claude Code Agents - Consolidated Collection

## Overview

This directory contains 33 optimized agents (25 general + 7 specialists + 1 meta-agent) with complexity-based model selection for maximum efficiency. Each agent is optimized for <400 characters and focuses on immediate execution.

### 🌐 Global Agents Available
22 specialist agents are configured as global agents via symbolic links in `~/.claude/agents/`, making them available across all projects. See [GLOBAL_AGENTS_SETUP.md](./GLOBAL_AGENTS_SETUP.md) for details.

### 🆕 Agent Builder Meta-Agent
The `agent-builder` is a specialized meta-agent that creates other agents following enterprise patterns:
- **Interactive Requirements Gathering**: Structured interview process
- **Automatic Optimization**: 400-character compression engine
- **Template-Based Generation**: Green/Yellow/Red tier templates
- **Validation & Testing**: Syntax, conflicts, and performance checks
- **Batch Creation Support**: Team standardization capabilities

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
- **Complexity-Based Models**: Green (Haiku), Blue (Sonnet 3.5), Yellow (Sonnet 3.7), Orange (Sonnet 4), Red (Opus) based on task complexity
- **Orchestration Patterns**: Four-layer intelligent routing with cost-optimized model selection
- **Tool Integration**: MCP protocol compatibility for external service access

## Agent Categories

### Core Development (8 agents)
`analyze-codebase`, `analyze-performance`, `build-frontend`, `build-backend`, `debug-issue`, `test-automation`, `review-code`, `generate-documentation`

### Infrastructure & DevOps (5 agents)
`deploy-application`, `manage-database`, `configure-environment`, `monitor-system`, `secure-application`

### Content & Communication (4 agents)
`write-content`, `translate-text`, `create-lesson`, `update-status`

### Data & AI (4 agents)
`process-data`, `train-model`, `query-database`, `extract-insights`

### Specialized Tools (5 agents)
`analyze-screenshot`, `manage-git`, `export-context`, `orchestrate-tasks`, `orchestrate-agents`, `@general-request`, `@orchestrate-agents-adv`

### Specialist Agents (7 agents)
`python-specialist`, `react-specialist`, `database-specialist`, `architect-specialist`, `security-specialist`, `ml-specialist`, `orchestrate-agents`

### Meta-Agent (1 agent)
`agent-builder` - Creates and optimizes other agents following enterprise patterns

## Usage Examples

### Creating New Agents with Agent-Builder
```bash
# Invoke the agent-builder
@agent-builder create a debugging specialist

# The agent-builder will:
# 1. Interview you about requirements
# 2. Generate optimized configuration
# 3. Apply 400-character compression
# 4. Validate and deploy the agent
```

### Standard Agent Usage
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

## Complexity System

- **Green (Easy) - Haiku Model**: Simple, single-step tasks (9 agents)
- **Blue (Standard) - Sonnet 3.5 Model**: Moderate complexity tasks (7 agents)
- **Yellow (Advanced) - Sonnet 3.7 Model**: Multi-step workflows (14 agents)
- **Orange (Complex) - Sonnet 4 Model**: Enterprise coordination (7 agents)
- **Red (Enterprise) - Opus Model**: Advanced reasoning and multi-agent orchestration (10 agents)

## Orchestration Hierarchy

1. **@general-request** (Sonnet 3.7/Yellow): Preliminary research and request analysis
2. **@orchestrate-tasks** (Sonnet 3.7/Yellow): Intelligence layer with complexity analysis and routing
3. **@orchestrate-agents** (Sonnet 4/Orange): Simple coordination for 1-3 agents
4. **@orchestrate-agents-adv** (Opus/Red): Complex enterprise coordination for 4+ agents

### Cost Benefits
- **Up to 70-80% cost reduction** through intelligent model selection
- Cleaner context management
- Intelligent, layered routing of complex tasks