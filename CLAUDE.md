# Claude Code Agent System Documentation

This document provides references to all agent system documentation and best practices for the agentgen project.

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

### 1. Choose the Right Agent
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

### 2. Leverage Orchestration
```bash
# Sequential workflow
analyze-codebase → review-code → deploy-application

# Concurrent processing
Multiple agents analyze different aspects in parallel

# Hierarchical coordination
orchestrate-agents coordinates specialist teams
```

### 3. Follow Best Practices
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

- **api-documenter** (specialization): Specialized agent for domain-specific tasks
- **code-reviewer** (quality-testing): Specialized agent for domain-specific tasks
- **debugger** (quality-testing): Specialized agent for domain-specific tasks
- **test-automator** (quality-testing): Specialized agent for domain-specific tasks

### Usage Instructions

These agents can be invoked in three ways:

1. **Automatic Invocation**: Claude Code will automatically select the appropriate agent based on your task
2. **Explicit Invocation**: Use phrases like "Use the $agent to..." or "Have $agent handle this"
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

- Trust automatic delegation for optimal agent selection
- Provide rich context about your requirements
- Use explicit invocation when you need specific expertise
- For complex projects, consider using the agent-organizer for multi-agent coordination

---
*Agents installed via claude-code-sub-agents repository*

