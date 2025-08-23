# CMD Agent Select Logic - Category Mapping

This document provides the mapping between cmd-agent-select-logic domains and install-agents categories to ensure proper alignment.

## Domain to Category Mapping

### CMD-Agent-Select-Logic Domains → Install-Agents Categories

| CMD Domain | Install Category | Available Agents | Primary Agents |
|------------|------------------|------------------|----------------|
| **frontend** | development, specialists | frontend-developer, ui-designer, ux-designer, react-pro, nextjs-pro, react-specialist, typescript-pro | @build-frontend, @frontend-developer, @react-specialist |
| **backend** | development, infrastructure, specialists | build-backend, full-stack-developer, database-specialist, python-specialist, postgres-pro, cloud-architect | @build-backend, @full-stack-developer, @database-specialist |
| **security** | specialists, quality | security-auditor, code-reviewer-pro | @security-auditor |
| **infrastructure** | infrastructure, specialists | deployment-engineer, cloud-architect, cloud-architect-specialist, performance-engineer | @deployment-engineer, @cloud-architect-specialist |
| **quality** | quality, development | code-reviewer, code-reviewer-pro, qa-expert, test-automator, debugger, debug-issue | @code-reviewer, @test-automator, @qa-expert |
| **documentation** | content, specialists | documentation-expert, create-lesson, update-status | @documentation-expert, @create-lesson |
| **data** | data, specialists | data-engineer, data-scientist, ml-engineer, ml-specialist | @data-engineer, @ml-specialist |
| **business** | business | product-manager, business-data-validator, business-integrator | @product-manager |

## Install-Agents Categories → CMD Domains

### Category Coverage in CMD System

| Install Category | CMD Domains Covered | Missing Coverage |
|------------------|-------------------|------------------|
| **business** | business | ✅ Full coverage |
| **content** | documentation | ✅ Full coverage |
| **core** | (utility agents) | ⚠️ Not domain-specific |
| **data** | data | ✅ Full coverage |
| **development** | frontend, backend, quality | ✅ Full coverage |
| **infrastructure** | infrastructure | ✅ Full coverage |
| **quality** | quality | ✅ Full coverage |
| **simple** | (utility agents) | ⚠️ Not domain-specific |
| **specialists** | ALL domains | ✅ Full coverage |
| **tools** | (orchestration) | ⚠️ Meta-tools |

## Agent Availability Matrix

### Frontend Domain Agents
```yaml
available_agents:
  development:
    - build-frontend
    - frontend-developer
    - react-pro
  specialists:
    - react-specialist
    - nextjs-pro
    - typescript-pro
    - ui-designer
    - ux-designer
```

### Backend Domain Agents
```yaml
available_agents:
  development:
    - build-backend
    - full-stack-developer
  specialists:
    - database-specialist
    - python-specialist
    - postgres-pro
  infrastructure:
    - cloud-architect
    - database-manager
```

### Security Domain Agents
```yaml
available_agents:
  specialists:
    - security-auditor
  quality:
    - code-reviewer-pro
```

### Infrastructure Domain Agents
```yaml
available_agents:
  infrastructure:
    - deployment-engineer
    - cloud-architect
    - deploy-application
    - manage-database
  specialists:
    - cloud-architect-specialist
    - performance-engineer
```

## Routing Recommendations

### High-Confidence Routes (≥0.8)
- Frontend component creation → @build-frontend
- Backend API development → @build-backend  
- Security audit → @security-auditor
- Cloud architecture → @cloud-architect-specialist
- Code quality review → @code-reviewer

### Medium-Confidence Routes (0.6-0.79)
- Frontend development → @frontend-developer, @react-specialist
- Backend development → @full-stack-developer, @database-specialist
- Testing workflows → @test-automator, @qa-expert
- Documentation → @documentation-expert, @create-lesson

### Low-Confidence Routes (<0.6)
- Route to orchestration agents (@orchestrate-tasks, @orchestrate-agents)
- Complex scenarios → @agent-organizer (strategic escalation)

## Category Integration Strategy

### Phase 1: Direct Mapping (Completed)
- Map existing CMD domains to install-agents categories
- Ensure all agents are properly categorized
- Identify routing priorities within each domain

### Phase 2: Enhanced Coverage
- Add routing rules for "pro" specialist agents (react-pro, nextjs-pro, etc.)
- Integrate business domain routing
- Enhance data/AI domain coverage

### Phase 3: Optimization
- Performance testing across all categories
- Confidence score calibration per agent
- Dynamic routing based on project context

This mapping ensures the cmd-agent-select-logic system can properly route tasks to all available agents in the install-agents ecosystem.