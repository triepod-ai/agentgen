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

## 🧠 Context-Manager System (OPERATIONAL)

**Status**: ✅ **FULLY OPERATIONAL** - Context-manager is active with complete knowledge graph

### **Knowledge Graph Location**: `/sub-agents/context/context-manager.json`
- **Last Updated**: 2025-08-14T12:08:08Z
- **Project Structure**: Complete directory tree with 36+ agents mapped
- **Activity Tracking**: Real-time agent activity logging
- **Cross-Agent Context**: Shared project understanding across all orchestration agents

### **Automatic Integration**
All orchestration agents integrate with context-manager:
- **@orchestrate-tasks**: Primary entry point with automatic context query
- **@orchestrate-agents**: Standard coordination with context awareness
- **@orchestrate-agents-adv**: Enterprise coordination with full context integration
- **Specialist Agents**: Many include mandatory context-manager communication protocols

### **Communication Protocol**
```json
{
  "requesting_agent": "agent-name",
  "request_type": "get_task_briefing",
  "payload": {
    "query": "Context query for project understanding"
  }
}
```

### **Benefits**
- **No Redundant Questions**: Agents understand project structure automatically
- **Informed Decisions**: All orchestration based on current project state
- **Cross-Agent Coordination**: Shared context enables better agent collaboration
- **Activity Tracking**: Monitor and coordinate multi-agent operations

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

- **Phase 1 Strategic Profiles Implementation COMPLETE** - Successfully implemented 3 strategic team-composition-based profiles with **100% functionality in BOTH symlink and copy modes**: enterprise-leadership (9 agents), startup-mvp (11 agents), and modern-web-stack (12 agents). Critical symlink mode bug resolved by debugger agent. All profiles tested and validated for production use. This strategic advancement aligns with enterprise patterns and provides decision matrix for optimal team composition selection ⭐⭐⭐ (Completed: 2025-08-19)
- **@cmd-agent-select-logic Enhanced Documentation** - Comprehensive documentation suite for advanced intelligent agent selection framework with hierarchical classification, multi-domain detection, and strategic escalation ⭐⭐⭐ (Added: 2025-08-18)
  - **[CMD_AGENT_SELECT_LOGIC_USER_GUIDE.md](./CMD_AGENT_SELECT_LOGIC_USER_GUIDE.md)** - Complete user guide with usage scenarios, troubleshooting, and best practices
  - **[CMD_AGENT_SELECT_LOGIC_TECHNICAL_DOCS.md](./CMD_AGENT_SELECT_LOGIC_TECHNICAL_DOCS.md)** - Architecture overview, algorithms, and performance optimization details
  - **[CMD_AGENT_SELECT_LOGIC_API_REFERENCE.md](./CMD_AGENT_SELECT_LOGIC_API_REFERENCE.md)** - API specifications, confidence scoring, and routing decision matrices
  - **[CMD_AGENT_SELECT_LOGIC_IMPLEMENTATION.md](./CMD_AGENT_SELECT_LOGIC_IMPLEMENTATION.md)** - 3-phase implementation roadmap with testing and deployment strategies
- **@orchestrate-tasks Testing Complete** - Achieved 100% test success rate (25/25 scenarios) through systematic debugging, comprehensive test infrastructure, and quality improvements ⭐⭐⭐ (Completed: 2025-08-17)
- **@install-agents-manager Agent Created** - New intelligent agent manager for automatic agent installation during sessions, integrated with all orchestration agents ⭐⭐⭐ (Added: 2025-08-17)
- **Enhanced Orchestration Agents** - All three orchestration agents (@orchestrate-tasks, @orchestrate-agents, @orchestrate-agents-adv) now include automatic agent installation via @install-agents-manager integration ⭐⭐⭐ (Updated: 2025-08-17)
- **Bash Completion System Complete** - Full bash completion for install-agents with NEW improved defaults and comprehensive documentation ⭐⭐ (Updated: 2025-08-17)
- **[INSTALL_AGENTS_USER_GUIDE.md](./INSTALL_AGENTS_USER_GUIDE.md)** - Complete user guide for install-agents command with comprehensive examples ⭐⭐⭐ (Added: 2025-08-17)
- **[INSTALL_AGENTS_QUICK_START.md](./INSTALL_AGENTS_QUICK_START.md)** - Quick start guide focusing on new improved defaults and 30-second setup ⭐⭐ (Added: 2025-08-17)
- **[INSTALL_AGENTS_HELP.md](./INSTALL_AGENTS_HELP.md)** - Updated comprehensive help documentation reflecting symlink mode defaults and improved UX ⭐⭐ (Updated: 2025-08-17)
- **install-agents --help** - Updated script help output with clear examples and improved defaults documentation (Updated: 2025-08-17)
- **[ORCHESTRATION_TESTING_METHODOLOGY.md](./ORCHESTRATION_TESTING_METHODOLOGY.md)** - Comprehensive testing methodology and results for @orchestrate-tasks agent with 100% success rate achievement ⭐⭐⭐ (Added: 2025-08-17)
- **[ORCHESTRATION_GUIDE.md](./ORCHESTRATION_GUIDE.md)** - Quick reference guide for orchestration system with operational context-manager integration ⭐⭐⭐ (Added: 2025-08-14)
- **Context-Manager System Operational** - Context-manager now fully operational with knowledge graph and automatic integration across all orchestration agents ⭐⭐⭐ (Updated: 2025-08-14)
- **@orchestrate-tasks Primary Entry Point** - Recommended orchestration entry point with intelligent routing and automatic context integration ⭐⭐ (Updated: 2025-08-14)
- **[COMPLETION_SETUP_GUIDE.md](./COMPLETION_SETUP_GUIDE.md)** - Complete bash completion setup guide with NEW improved defaults (symlink mode, current directory, force enabled) ⭐⭐ (Added: 2025-08-17)
- **[COMPLETION_README.md](./COMPLETION_README.md)** - Updated bash completion documentation reflecting improved UX defaults ⭐⭐ (Updated: 2025-08-17)
- **[README_SYMLINK_HUB.md](./README_SYMLINK_HUB.md)** - Symlink-based agent hub documentation ⭐⭐⭐ (Added: 2025-01-11)
- **[SYMLINK_HUB_IMPLEMENTATION_PLAN.md](./SYMLINK_HUB_IMPLEMENTATION_PLAN.md)** - Technical implementation plan for symlink system (Added: 2025-01-11)
- **[README_UV.md](./README_UV.md)** - UV Wrapper Documentation ⭐ - Modern Python interface with 10-100x faster dependency management (Added: 2025-01-10)
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

**⚠️ IMPORTANT: Must run from agentgen directory**
The `install-agents` script must be run from `/home/bryan/agentgen/` directory as it needs access to the agents hub and configuration files.

```bash
# Navigate to agentgen first
cd /home/bryan/agentgen

# UNIFIED INSTALLER with symlinks (recommended)
./install-agents --symlink --global --profile core
./install-agents --symlink --project /path/to/target --profile development

# NEW: Strategic team-composition profiles (Phase 1) - Both modes work perfectly
./install-agents --symlink --project /path/to/target --profile enterprise-leadership  # 9 strategic decision-makers
./install-agents --copy --project /path/to/target --profile startup-mvp              # 11 lean rapid development (copy mode)
./install-agents --symlink --project /path/to/target --profile modern-web-stack     # 12 TypeScript/React specialists

# Copy mode installation (traditional)
./install-agents --profile development-team /path/to/target

# Maintenance (symlink mode)
./install-agents --symlink --health
./install-agents --symlink --repair

# Migrate existing installations to symlinks
./migrate-to-symlinks.sh /path/to/target

# Legacy symlink-only installer (still available)
./install-agents-symlink --project /path/to/target --profile development
```

**Common Mistake:**
```bash
# ❌ Wrong - redundant command name
install-agents install-agents --profile development-team

# ✅ Correct - run from agentgen directory
cd /home/bryan/agentgen
./install-agents --profile development-team /path/to/target
```

### 1. Setup with UV (Alternative)
```bash
# Navigate to agentgen first
cd /home/bryan/agentgen

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

### 3. Leverage Orchestration (Context-Manager Integrated)
```bash
# Primary orchestration entry point (RECOMMENDED)
@orchestrate-tasks "comprehensive code review and security audit"
@orchestrate-tasks "build authentication system with testing"

# Direct orchestration (for specific coordination needs)
@orchestrate-agents "review code quality and fix bugs"  # 1-3 agents
@orchestrate-agents-adv "enterprise security audit with modernization"  # 4+ agents

# Traditional single-agent workflows
analyze-codebase → review-code → deploy-application
```

### 4. Strategic Profile Selection (NEW)
Choose team composition based on organizational context:

```bash
# Enterprise Leadership (9 agents) - Strategic decision-makers
# Both modes work perfectly
./install-agents --symlink --profile enterprise-leadership
./install-agents --copy --profile enterprise-leadership
# Best for: C-level decisions, strategic planning, enterprise architecture
# Key agents: architect-specialist, product-manager, security-auditor, performance-engineer

# Startup MVP (11 agents) - Lean rapid development  
# Both modes work perfectly
./install-agents --symlink --profile startup-mvp
./install-agents --copy --profile startup-mvp
# Best for: Fast prototyping, resource constraints, MVP validation
# Key agents: full-stack-developer, build-frontend, build-backend, debugger

# Modern Web Stack (12 agents) - TypeScript/React specialists
# Both modes work perfectly
./install-agents --symlink --profile modern-web-stack
./install-agents --copy --profile modern-web-stack
# Best for: Modern web applications, React/TypeScript focus, UI/UX excellence
# Key agents: react-specialist, nextjs-pro, ui-designer, frontend-developer
```

**Decision Matrix:**
- **Budget/Timeline**: enterprise-leadership → startup-mvp → modern-web-stack
- **Team Size**: enterprise-leadership (large) → modern-web-stack (medium) → startup-mvp (small)
- **Technical Focus**: modern-web-stack (frontend) → startup-mvp (full-stack) → enterprise-leadership (architecture)

### 5. Follow Best Practices
- Start with single-agent patterns before multi-agent complexity
- Match complexity tier to task requirements
- Use <400 character agent descriptions for optimal performance
- Leverage MCP protocol for external service integration
- **Strategic Shift**: Team-composition-based profiles align with real-world team structures and enterprise patterns

## 📊 System Benefits

- **3x Faster Loading**: <400 character limit ensures rapid initialization
- **Intelligent Routing**: Complexity-based model selection
- **Better Context**: Optimized prompts preserve main conversation context
- **Cost Optimization**: Tiered model usage minimizes token consumption
- **Enterprise Patterns**: Based on Microsoft Azure, Speakeasy, Databricks research
- **Context-Manager Integration**: Automatic project understanding and cross-agent coordination
- **Intelligent Orchestration**: @orchestrate-tasks provides smart routing and task breakdown
- **Symlink Efficiency**: Instant updates, no duplication, single source of truth
- **Proven Reliability**: 100% test success rate with comprehensive validation methodology
- **Systematic Quality**: Evidence-based improvements with debugging infrastructure
- **Strategic Profiles**: Team-composition-based profiles (Phase 1) enable real-world organizational alignment
- **Enterprise-Grade Selection**: Decision matrix approach for optimal team composition based on context and constraints

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

This project has the following specialized AI sub-agents available:

### Available Agents

- **agent-builder** (specialization): Specialized agent for domain-specific tasks
- **agent-organizer** (general): Specialized agent for domain-specific tasks
- **analyze-screenshot** (general): Specialized agent for domain-specific tasks
- **api-documenter** (specialization): Specialized agent for domain-specific tasks
- **architect-specialist** (general): Specialized agent for domain-specific tasks
- **build-backend** (general): Specialized agent for domain-specific tasks
- **build-frontend** (general): Specialized agent for domain-specific tasks
- **build-runner** (general): Specialized agent for domain-specific tasks
- **cloud-architect-specialist** (general): Specialized agent for domain-specific tasks
- **code-reviewer** (quality-testing): Specialized agent for domain-specific tasks
- **config-reader** (general): Specialized agent for domain-specific tasks
- **context-manager** (general): Specialized agent for domain-specific tasks
- **database-specialist** (general): Specialized agent for domain-specific tasks
- **data-engineer** (data-ai): Specialized agent for domain-specific tasks
- **debugger** (quality-testing): Specialized agent for domain-specific tasks
- **deployment-engineer** (infrastructure): Specialized agent for domain-specific tasks
- **documentation-expert** (specialization): Specialized agent for domain-specific tasks
- **documentation-hub** (general): Specialized agent for domain-specific tasks
- **env-reader** (general): Specialized agent for domain-specific tasks
- **frontend-developer** (development): Specialized agent for domain-specific tasks
- **full-stack-developer** (development): Specialized agent for domain-specific tasks
- **log-reader** (general): Specialized agent for domain-specific tasks
- **ml-specialist** (general): Specialized agent for domain-specific tasks
- **nextjs-pro** (development): Specialized agent for domain-specific tasks
- **orchestrate-tasks** (general): Specialized agent for domain-specific tasks
- **performance-engineer** (infrastructure): Specialized agent for domain-specific tasks
- **product-manager** (business): Specialized agent for domain-specific tasks
- **python-specialist** (general): Specialized agent for domain-specific tasks
- **qa-expert** (quality-testing): Specialized agent for domain-specific tasks
- **react-pro** (development): Specialized agent for domain-specific tasks
- **react-specialist** (general): Specialized agent for domain-specific tasks
- **readme-reader** (general): Specialized agent for domain-specific tasks
- **security-auditor** (security): Specialized agent for domain-specific tasks
- **test-automator** (quality-testing): Specialized agent for domain-specific tasks
- **ui-designer** (development): Specialized agent for domain-specific tasks
- **ux-designer** (development): Specialized agent for domain-specific tasks

### Usage Instructions

These agents can be invoked in three ways:

1. **Automatic Invocation**: Claude Code will automatically select the appropriate agent based on your task
2. **Explicit Invocation**: Use phrases like "Use the ux-designer to..." or "Have ux-designer handle this"
3. **Agent Organizer**: For complex multi-agent workflows, the agent-organizer can coordinate multiple specialists

### Examples

```bash
# Direct invocation
"Use the code-reviewer to analyze this pull request"
"Have the security-auditor scan for vulnerabilities"

# Multi-agent coordination
"Use backend-architect to design the API, then have security-auditor review it"
```

### Agent Categories

- **business**: Product management and business analysis
- **data-ai**: Data engineering, AI/ML, and database optimization
- **development**: Frontend, backend, and full-stack development
- **infrastructure**: Cloud, DevOps, and performance engineering
- **quality-testing**: Code review, QA, and testing automation
- **security**: Security auditing and vulnerability assessment
- **specialization**: API documentation and specialized expertise

### Best Practices

- **Start with @orchestrate-tasks** for complex, multi-step operations
- Trust automatic delegation for optimal agent selection
- All orchestration agents automatically integrate with context-manager for project awareness
- Use explicit invocation when you need specific expertise
- Context-manager eliminates need to re-explain project structure
- For enterprise coordination, @orchestrate-tasks will route to appropriate orchestrator

---
*Agents installed via claude-code-sub-agents repository*

