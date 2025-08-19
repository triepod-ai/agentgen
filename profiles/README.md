# Agent Profile Selection Guide

*Version 2.0 | Updated 2025-08-19*

**The definitive profile selection guide for the agentgen system.** This document helps you choose the optimal agent configuration for your team size, project complexity, and development focus.

## Quick Selection Guide

| **Team Size** | **Primary Focus** | **Recommended Profile** | **Agents** |
|---------------|-------------------|-------------------------|------------|
| **50+ people** | Strategic leadership & enterprise decisions | [enterprise-leadership](#enterprise-leadership-9-agents) | 9 agents |
| **15-50 people** | Modern web applications (TypeScript/React) | [modern-web-stack](#modern-web-stack-12-agents) | 12 agents |
| **5-15 people** | Rapid MVP development & startup agility | [startup-mvp](#startup-mvp-11-agents) | 11 agents |
| **Any size** | Complete development workflow | [development-team](#development-team-18-agents) | 18 agents |
| **Any size** | Essential agents for all projects | [core](#core-15-agents) | 15 agents |

## Strategic Profiles (NEW - Phase 1 Complete)

**✅ All strategic profiles work perfectly in BOTH symlink and copy modes.**

### 🏢 enterprise-leadership (9 agents)
*Strategic decision-makers for large organizations (50+ people)*

**Target Audience:** CTOs, Engineering Directors, Solution Architects
**Focus:** Architecture, risk management, business strategy, organizational coordination
**Team Structure:** Strategic leadership layer, not hands-on development

```bash
# Strategic Leadership
architect-specialist, security-auditor, cloud-architect-specialist, performance-engineer

# Business & Quality Management  
product-manager, data-engineer, documentation-expert, qa-expert

# Strategic Coordination
orchestrate-tasks
```

**Use Cases:**
- Technology strategy decisions
- Architecture reviews and planning
- Risk assessment and security governance
- Performance and scalability planning
- Cross-team coordination and alignment

**Command Examples:**
```bash
# Install for enterprise strategy - Both modes work perfectly
./install-agents --symlink --profile enterprise-leadership --global
./install-agents --copy --profile enterprise-leadership --global

# Strategic architecture review
@architect-specialist "review enterprise architecture for scalability to 10M users"
@orchestrate-tasks "comprehensive security audit across all systems"
```

### 🚀 startup-mvp (11 agents)  
*Optimized for rapid development in startups (5-15 people)*

**Target Audience:** Startup founders, small development teams, MVP builders
**Focus:** Speed, quality, essential functionality for product development
**Team Structure:** Lean, multi-skilled, rapid iteration

```bash
# Core Development (Primary Development Force)
full-stack-developer, nextjs-pro, backend-architect, ui-designer

# Quality & Security (Quality Gatekeeper & Problem Solving)
code-reviewer, debugger, test-automator, security-auditor

# Product & Coordination (Feature Management & DevOps)
product-manager, deployment-engineer, orchestrate-tasks
```

**Use Cases:**
- MVP development and launch
- Rapid prototyping and iteration
- Early-stage product development
- Resource-constrained development
- Quick market validation

**Command Examples:**
```bash
# Install for startup development - Both modes work perfectly
./install-agents --symlink --profile startup-mvp /path/to/startup-project
./install-agents --copy --profile startup-mvp /path/to/startup-project

# Rapid MVP development
@orchestrate-tasks "build MVP authentication system with React frontend"
@nextjs-pro "create landing page with conversion tracking"
```

### 🌐 modern-web-stack (12 agents)
*TypeScript/React specialists for mid-size teams (15-50 people)*

**Target Audience:** Mid-size companies, TypeScript teams, modern web applications
**Focus:** TypeScript, React, Next.js, full-stack development, enterprise tooling
**Team Structure:** Specialized frontend expertise with full-stack integration

```bash
# Modern Frontend Architecture (5 agents)
nextjs-pro, react-pro, frontend-developer, ui-designer, ux-designer

# Full-Stack Integration (3 agents)  
full-stack-developer, backend-architect, performance-engineer

# Quality & DevOps (3 agents)
test-automator, code-reviewer, deployment-engineer

# Coordination (1 agent)
orchestrate-tasks
```

**Use Cases:**
- Modern web application development
- TypeScript/React enterprise projects  
- Component library and design system development
- Performance-critical web applications
- Full-stack JavaScript/TypeScript projects

**Command Examples:**
```bash
# Install for modern web development - Both modes work perfectly
./install-agents --symlink --profile modern-web-stack /path/to/web-app
./install-agents --copy --profile modern-web-stack /path/to/web-app

# Modern component development
@react-pro "build reusable component library with TypeScript"
@orchestrate-tasks "implement advanced React patterns with performance optimization"
```

## Complete Development Profiles

### 🏗️ development-team (18 agents)
*Complete development team for full-stack projects*

**Target Audience:** Complete project teams, full-stack development, comprehensive workflows
**Focus:** All aspects of software development with complete coverage
**Team Structure:** Full development lifecycle coverage

```bash
# Infrastructure & Architecture (3 agents)
cloud-architect-specialist, deployment-engineer, architect-specialist

# Development & Design (6 agents) 
ui-designer, ux-designer, frontend-developer, full-stack-developer, build-backend, analyze-screenshot

# Quality & Testing (4 agents)
code-reviewer, debugger, qa-expert, test-automator

# Documentation & Coordination (3 agents)
documentation-expert, agent-organizer, orchestrate-tasks

# Tools & Management (2 agents)
agent-builder, product-manager
```

**Use Cases:**
- Large-scale application development
- Enterprise software projects
- Complete development workflow coverage
- Teams needing comprehensive capabilities
- Complex multi-domain projects

### 🔧 core (15 agents)
*Essential agents available globally - matches ~/.claude/agents/ setup*

**Target Audience:** All developers, essential development workflows
**Focus:** Core development capabilities across all domains
**Team Structure:** Foundational development capabilities

```bash
# Core Development (6 agents)
code-reviewer, debugger, frontend-developer, full-stack-developer, build-backend, test-automator

# Management & Orchestration (4 agents)
orchestrate-tasks, orchestrate-agents, agent-builder, product-manager

# Documentation & Communication (3 agents)  
documentation-expert, claude-md-maintainer, create-lesson

# Analysis & Infrastructure (2 agents)
analyze-screenshot, cloud-architect
```

**Use Cases:**
- Standard development workflows
- Global agent installation
- Essential development capabilities
- Cross-project agent availability
- Foundational development setup

## Specialized Focus Profiles

### 🎨 frontend-focus (11 agents)
*UI/UX development team with design capabilities*

**Focus:** Frontend development, user interface, user experience
```bash
# Design & Frontend (5 agents)
ui-designer, ux-designer, frontend-developer, react-pro, nextjs-pro

# Quality & Testing (3 agents)
code-reviewer, qa-expert, test-automator

# Coordination (3 agents)
agent-organizer, context-manager
```

### ⚙️ backend-focus (13 agents)
*Backend development with API and infrastructure focus*

**Focus:** Server-side development, APIs, databases, infrastructure
```bash
# Backend Development (4 agents)
backend-architect, python-pro, typescript-pro, full-stack-developer

# Data & Infrastructure (4 agents)
database-optimizer, data-engineer, cloud-architect, deployment-engineer

# Quality & Testing (3 agents)
code-reviewer, debugger, qa-expert

# Coordination (1 agent)
agent-organizer
```

### 🤖 ai-ml-team (12 agents)
*Machine learning and data science development*

**Focus:** AI/ML, data science, intelligent applications
```bash
# AI/ML Core (5 agents)
ai-engineer, ml-engineer, data-scientist, data-engineer, prompt-engineer

# Backend & Infrastructure (3 agents)
python-pro, backend-architect, database-optimizer

# Quality & Testing (2 agents)
code-reviewer, debugger

# Coordination (1 agent)
agent-organizer
```

### 🔒 security-audit (9 agents)
*Security-focused team for vulnerability assessment*

**Focus:** Security assessment, vulnerability management, secure development
```bash
# Security Core (2 agents)
security-auditor, code-reviewer

# Architecture & Infrastructure (3 agents)
cloud-architect, deployment-engineer, architect-review

# Quality & Testing (2 agents)
qa-expert, test-automator

# Coordination (1 agent)
agent-organizer
```

### ⚡ simple-tools (33 agents)
*Ultra-fast single-tool agents optimized for specific tasks*

**Focus:** Specific single-purpose tasks, minimal loading time, high performance
```bash
# Read Agents (5): config-reader, log-reader, readme-reader, env-reader, analyze-screenshot
# Write Agents (4): gitignore-writer, readme-writer, env-writer, changelog-writer  
# Bash Agents (4): test-runner, build-runner, git-executor, dependency-installer
# Grep Agents (4): error-finder, todo-finder, import-finder, function-finder
# Edit Agents (4): comment-remover, whitespace-fixer, import-sorter, typo-fixer
```

## Profile Comparison Matrix

| Profile | Agents | Team Size | Complexity | Primary Focus | Best For |
|---------|--------|-----------|------------|---------------|----------|
| **enterprise-leadership** | 9 | 50+ | Strategic | Architecture & Strategy | CTOs, Engineering Directors |
| **startup-mvp** | 11 | 5-15 | Lean | Rapid Development | Startups, MVP Development |
| **modern-web-stack** | 12 | 15-50 | Specialized | TypeScript/React | Modern Web Apps |
| **development-team** | 18 | 10-50 | Complete | Full-Stack Development | Enterprise Projects |
| **core** | 15 | Any | Essential | General Development | All Projects |
| **frontend-focus** | 11 | 5-25 | Specialized | UI/UX Development | Frontend Teams |
| **backend-focus** | 13 | 5-30 | Specialized | APIs & Infrastructure | Backend Teams |
| **ai-ml-team** | 12 | 5-20 | Specialized | AI/ML Development | Data Science Teams |
| **security-audit** | 9 | 3-15 | Focused | Security Assessment | Security Teams |
| **simple-tools** | 33 | Any | Task-Specific | Single-Purpose Tasks | Utility Operations |

## Installation Examples

### Quick Start Commands

```bash
# Navigate to agentgen directory first (REQUIRED)
cd /home/bryan/agentgen

# Strategic profiles
./install-agents --profile enterprise-leadership --global
./install-agents --profile startup-mvp /path/to/startup
./install-agents --profile modern-web-stack /path/to/webapp

# Complete development
./install-agents --profile development-team /path/to/project
./install-agents --profile core --global

# Specialized focus
./install-agents --profile frontend-focus /path/to/frontend-project
./install-agents --profile backend-focus /path/to/api-project
./install-agents --profile ai-ml-team /path/to/ml-project

# Security and utilities
./install-agents --profile security-audit /path/to/secure-project
./install-agents --profile simple-tools --global
```

### Symlink Mode (Recommended - Fully Functional)

```bash
# Symlink installation for instant updates - ALL profiles work perfectly
./install-agents --symlink --profile startup-mvp /path/to/project
./install-agents --symlink --profile enterprise-leadership /path/to/project  
./install-agents --symlink --profile modern-web-stack /path/to/project
./install-agents --symlink --global --profile core

# Health check and maintenance
./install-agents --symlink --health
./install-agents --symlink --repair
```

## Migration and Upgrade Paths

### From Broad to Focused

```bash
# Start broad, then specialize
./install-agents --profile development-team /project  # Initial setup
./install-agents --profile frontend-focus /project    # Add frontend specialization
./install-agents --profile security-audit /project    # Add security focus
```

### Scaling Strategies

**Small Team (5-15) → Medium Team (15-50)**
```bash
startup-mvp → modern-web-stack  # Add specialized frontend expertise
startup-mvp → development-team  # Add comprehensive coverage
```

**Medium Team (15-50) → Enterprise (50+)**
```bash
modern-web-stack → development-team + enterprise-leadership  # Add strategy layer
development-team → enterprise-leadership  # Focus on strategic decisions
```

### Combination Strategies

```bash
# Global essential + project specialized
./install-agents --symlink --global --profile core
./install-agents --symlink --project --profile modern-web-stack

# Multiple focused profiles
./install-agents --profile frontend-focus /project
./install-agents --profile backend-focus /project  # Combines into full-stack team
```

## Decision Framework

### 1. Assess Your Team

**Team Size:**
- **1-4 people:** core or simple-tools
- **5-15 people:** startup-mvp or focused profiles (frontend-focus, backend-focus)
- **15-50 people:** modern-web-stack or development-team
- **50+ people:** enterprise-leadership + specialized profiles

**Team Experience:**
- **Junior/Learning:** core or development-team (comprehensive coverage)
- **Mixed Experience:** startup-mvp or modern-web-stack (balanced)  
- **Senior/Strategic:** enterprise-leadership (strategic focus)

### 2. Define Your Project

**Project Type:**
- **MVP/Startup:** startup-mvp
- **Modern Web App:** modern-web-stack
- **Enterprise Application:** development-team + enterprise-leadership
- **AI/ML Project:** ai-ml-team
- **Security-Critical:** security-audit + core

**Technology Stack:**
- **TypeScript/React:** modern-web-stack
- **Python/AI:** ai-ml-team  
- **Mixed/Flexible:** development-team or core
- **Legacy Modernization:** enterprise-leadership + development-team

**Development Phase:**
- **Planning/Architecture:** enterprise-leadership
- **Active Development:** startup-mvp, modern-web-stack, or development-team
- **Maintenance/Security:** security-audit + core
- **Scaling/Growth:** enterprise-leadership + specialized profiles

### 3. Consider Resource Constraints

**Budget/Resources:**
- **Limited:** startup-mvp or core
- **Moderate:** focused profiles (frontend-focus, backend-focus)
- **Unlimited:** development-team + enterprise-leadership

**Time to Market:**
- **Urgent:** startup-mvp
- **Standard:** modern-web-stack or development-team  
- **Strategic:** enterprise-leadership

## Real-World Scenarios

### Scenario 1: Early-Stage SaaS Startup
**Team:** 3 developers, 1 designer, limited runway
**Choice:** `startup-mvp`
**Reasoning:** Lean, rapid development focus with quality gates

### Scenario 2: Growing E-commerce Platform  
**Team:** 25 developers, TypeScript/React focus, scaling rapidly
**Choice:** `modern-web-stack`
**Reasoning:** Specialized expertise in modern web technologies

### Scenario 3: Enterprise Financial Application
**Team:** 100+ developers, complex compliance requirements
**Choice:** `enterprise-leadership` + `security-audit` + `development-team`
**Reasoning:** Strategic oversight, security focus, comprehensive development

### Scenario 4: AI Research Project
**Team:** 8 data scientists, 3 engineers
**Choice:** `ai-ml-team`  
**Reasoning:** Specialized AI/ML expertise with supporting development

### Scenario 5: Frontend Redesign Project
**Team:** 12 frontend developers, design system focus
**Choice:** `frontend-focus` + `modern-web-stack`
**Reasoning:** UI/UX specialization with modern component architecture

## Profile Management Commands

```bash
# List all available profiles  
./install-agents --list-profiles

# View specific profile details
./install-agents --show-profile development-team
./install-agents --show-profile startup-mvp

# Check installed agents
./install-agents --symlink --health

# Update profile installations
./install-agents --symlink --repair

# Migrate existing installations
./migrate-to-symlinks.sh /path/to/project
```

## Custom Profile Creation

### Creating Your Own Profile

1. **Create Profile File**
   ```bash
   # Create new profile
   nano profiles/my-custom-profile.profile
   ```

2. **Profile Template**
   ```yaml
   # My Custom Profile
   # Description of the profile purpose and team structure
   
   name: my-custom-profile
   description: Brief description of the profile purpose and optimal use cases
   
   agents:
     # Category 1
     - agent-name-1
     - agent-name-2
     
     # Category 2  
     - agent-name-3
     - agent-name-4
     
     # Comments are supported for organization
   ```

3. **Install Custom Profile**
   ```bash
   ./install-agents --profile my-custom-profile /path/to/project
   ```

### Profile Design Best Practices

**Agent Selection:**
- **Focus:** Choose agents aligned with primary use case
- **Balance:** Include development, quality, and coordination agents
- **Size:** Optimal range is 8-18 agents for performance
- **Dependencies:** Ensure agent compatibility and workflow coverage

**Team Structure:**
- **Core:** Essential development capabilities (3-5 agents)
- **Specialized:** Domain-specific expertise (3-6 agents)  
- **Quality:** Testing and review capabilities (2-4 agents)
- **Coordination:** Orchestration and management (1-2 agents)

## Troubleshooting

### Common Issues

**Profile Not Found**
```bash
# Check available profiles
./install-agents --list-profiles

# Verify profile file exists
ls profiles/*.profile
```

**Agent Installation Failures**
```bash
# Check agent availability  
ls agents/*/
ls ~/.claude/agents/

# Repair installation
./install-agents --symlink --repair
```

**Performance Issues**
```bash
# Use smaller profiles for better performance
# startup-mvp (11) vs development-team (18)

# Check symlink status
./install-agents --symlink --health
```

### Best Practices

1. **Start Small:** Begin with core or focused profiles, expand as needed
2. **Use Symlinks:** Enable instant updates and space efficiency  
3. **Global + Project:** Install core globally, specialized per project
4. **Regular Health Checks:** Run `--health` checks periodically
5. **Profile Combination:** Combine focused profiles for comprehensive coverage

---

## Support and Resources

- **Main Documentation:** `/README.md`
- **Agent Best Practices:** `/AGENT_BEST_PRACTICES.md`
- **Installation Guide:** `/INSTALL_AGENTS_USER_GUIDE.md`
- **Symlink Hub:** `/README_SYMLINK_HUB.md`

**Profile System Version:** 2.0
**Last Updated:** 2025-08-19
**Total Profiles Available:** 10