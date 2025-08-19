# Claude Code Agents - Consolidated Collection

## Overview

This directory contains 36+ optimized agents organized in 11 categories with complexity-based model selection for maximum efficiency. Each agent is optimized for <400 characters and focuses on immediate execution.

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
# Install strategic profiles
./install-agents --profile enterprise-leadership
./install-agents --profile startup-mvp
./install-agents --profile modern-web-stack

# Traditional installations
./install-agents --profile development-team
./install-agents --all

# List available profiles and agents
./install-agents --list-profiles
./install-agents --list

# Detailed installation guide
cat INSTALL_AGENTS_HELP.md
```

### Strategic Profiles (NEW - Phase 1 Complete)

Our **Phase 1 Strategic Profile Implementation** introduces 3 team-composition-based profiles designed to replace broad category-based approaches with targeted, role-specific agent sets. **All profiles now work perfectly in BOTH symlink and copy modes.**

#### Enterprise Leadership (9 agents)
**Target Audience**: Large organizations (50+ people), strategic decision-makers  
**Focus**: Architecture, risk management, business strategy, organizational coordination

```bash
# Both installation modes work perfectly
./install-agents --symlink --profile enterprise-leadership
./install-agents --copy --profile enterprise-leadership
```

**Key Agents**: architect-specialist, security-auditor, cloud-architect-specialist, performance-engineer, product-manager, data-engineer, documentation-expert, qa-expert, orchestrate-tasks

#### Startup MVP (11 agents)  
**Target Audience**: Startups (5-15 people), rapid development teams  
**Focus**: Speed, quality, essential functionality, lean development

```bash
# Both installation modes work perfectly
./install-agents --symlink --profile startup-mvp
./install-agents --copy --profile startup-mvp
```

**Key Agents**: full-stack-developer, nextjs-pro, backend-architect, ui-designer, code-reviewer, debugger, test-automator, security-auditor, product-manager, deployment-engineer, orchestrate-tasks

#### Modern Web Stack (12 agents)
**Target Audience**: Mid-size teams (15-50 people), TypeScript/React specialists  
**Focus**: Modern frontend architecture, full-stack integration, performance optimization

```bash
# Both installation modes work perfectly
./install-agents --symlink --profile modern-web-stack
./install-agents --copy --profile modern-web-stack
```

**Key Agents**: nextjs-pro, react-pro, frontend-developer, ui-designer, ux-designer, full-stack-developer, backend-architect, performance-engineer, test-automator, code-reviewer, deployment-engineer, orchestrate-tasks

### Profile Selection Guide

| Team Size | Profile | Use Case | Key Benefits |
|-----------|---------|----------|--------------|
| 5-15 people | `startup-mvp` | Rapid MVP development | Speed, essential quality gates, lean coordination |
| 15-50 people | `modern-web-stack` | TypeScript/React applications | Modern architecture, full-stack integration |
| 50+ people | `enterprise-leadership` | Strategic decision-making | Architecture oversight, risk management, business alignment |
| Any size | `development-team` | General development | Comprehensive coverage, traditional approach |
| Any size | `core` | Essential workflows | Basic development needs, lightweight |

### Strategic Profile Benefits

The new **Phase 1 Profile Reorganization** replaces broad category-based approaches with targeted, role-specific agent sets:

#### **Focused Expertise**
- Each profile optimized for specific team sizes and organizational contexts
- Reduced cognitive load through role-appropriate agent selection
- Strategic alignment between team needs and available capabilities

#### **Improved Efficiency** 
- Faster onboarding with pre-configured agent sets matching team workflows
- Reduced decision fatigue when selecting agents
- Context-appropriate tool selection for better productivity

#### **Enterprise Alignment**
- **Enterprise Leadership**: Strategic oversight and architectural decision-making
- **Startup MVP**: Speed and quality balance for rapid market entry
- **Modern Web Stack**: Technology-specific optimization for modern development

#### **Migration Strategy**
- **Phase 1** (Current): 3 strategic profiles alongside traditional profiles
- **Phase 2** (Planned): Additional specialized profiles for emerging technologies
- **Phase 3** (Future): Full transition to role-based profile system

### Installation Methods
- **Strategic Profiles**: `./install-agents --profile enterprise-leadership` (symlink default)
- **Symlink Mode**: `./install-agents --symlink --profile startup-mvp` (instant updates)
- **Copy Mode**: `./install-agents --copy --profile modern-web-stack` (independent files)
- **Global Installation**: `./install-agents --symlink --global --profile core`
- **Dry Run**: `./install-agents --dry-run --profile startup-mvp`

**✅ All modes fully functional** - Both symlink and copy modes work perfectly with strategic profiles.

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

### Strategic Profile Implementation
```bash
# Enterprise Leadership - Strategic decision-making for large orgs
# Both modes work perfectly
./install-agents --symlink --profile enterprise-leadership
./install-agents --copy --profile enterprise-leadership
@architect-specialist "Design microservices architecture for 50+ person team"
@security-auditor "Conduct enterprise-grade security assessment" 
@performance-engineer "Optimize system for enterprise scale"

# Startup MVP - Rapid development for startups  
# Both modes work perfectly
./install-agents --symlink --profile startup-mvp
./install-agents --copy --profile startup-mvp
@full-stack-developer "Build MVP user authentication quickly"
@nextjs-pro "Create landing page with conversion tracking"
@product-manager "Define MVP feature priorities"

# Modern Web Stack - TypeScript/React for mid-size teams
# Both modes work perfectly
./install-agents --symlink --profile modern-web-stack
./install-agents --copy --profile modern-web-stack
@react-pro "Implement advanced React patterns with TypeScript"
@ux-designer "Design user-centered component library"
@test-automator "Set up modern testing pipeline"
```

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
# Orchestration (Recommended for complex tasks)
@orchestrate-tasks "Review code quality and fix security issues"
@orchestrate-tasks "Build complete authentication system with testing"

# Direct agent usage
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

## Orchestration Hierarchy (Context-Manager Integrated)

**Recommended Entry Point**: `@orchestrate-tasks` for all orchestration needs

1. **@orchestrate-tasks** (Sonnet 3.7/Yellow): **Primary entry point** - Intelligence layer with automatic context-manager integration, complexity analysis, and intelligent routing
2. **@orchestrate-agents** (Sonnet 4/Orange): Standard coordination for 1-3 agents with context awareness
3. **@orchestrate-agents-adv** (Opus/Red): Complex enterprise coordination for 4+ agents with full context integration

**Context-Manager Integration**: All orchestration agents automatically query the context-manager for project understanding before task execution, ensuring informed decision-making and avoiding redundant questions.

### Cost Benefits
- **Up to 70-80% cost reduction** through intelligent model selection
- Cleaner context management
- Intelligent, layered routing of complex tasks