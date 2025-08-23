# Default Agent Installation Set

This document lists the default agents installed for the AgentGen project, providing a comprehensive development toolkit.

## 📦 Installed Agents (13 Total)

### Development Agents (5)
- **backend-architect** - Backend system architecture and API design specialist
- **frontend-developer** - Frontend development and user interface specialist
- **full-stack-developer** - Full-stack development combining frontend and backend expertise
- **nextjs-pro** - Next.js framework specialist for modern React applications
- **ui-designer** - User interface design and UX specialist

### Infrastructure & Operations (2)
- **deployment-engineer** - CI/CD pipelines, deployment strategies, and DevOps
- **agent-organizer** - Coordinates multiple agents for complex workflows

### Quality & Testing (3)
- **code-reviewer** - Comprehensive code review and quality assurance
- **debugger** - Advanced debugging and troubleshooting specialist
- **test-automator** - Automated test creation and test suite management

### Documentation & API (2)
- **api-documenter** - API documentation generation and OpenAPI specs
- **documentation-hub** - Central documentation management and organization

### System Management (1)
- **context-manager** - Context and memory management for complex projects

## 🚀 Quick Start Usage

### Direct Invocation (@-mention)
```bash
@backend-architect design a microservices architecture
@nextjs-pro create a dashboard with server components
@debugger investigate the memory leak in production
@deployment-engineer setup GitHub Actions CI/CD
```

### Coordinated Workflows
```bash
# Multi-agent collaboration
@agent-organizer coordinate: backend-architect for API design, then frontend-developer for UI implementation

# Sequential processing
@code-reviewer analyze changes → @test-automator create tests → @api-documenter update docs
```

### Auto-Activation Examples
The agents will automatically activate based on task context:
- "Design a REST API" → backend-architect
- "Create a React component" → frontend-developer or nextjs-pro
- "Fix this bug" → debugger
- "Setup deployment pipeline" → deployment-engineer
- "Review this code" → code-reviewer

## 🎯 Agent Specializations

### Full-Stack Development
- **backend-architect** + **frontend-developer** + **full-stack-developer**
- Complete application development from API to UI

### Modern Web Apps
- **nextjs-pro** + **ui-designer** + **frontend-developer**
- Next.js applications with excellent UX

### Quality Assurance
- **code-reviewer** + **test-automator** + **debugger**
- Comprehensive quality control and testing

### DevOps & Deployment
- **deployment-engineer** + **backend-architect**
- Infrastructure and deployment automation

### Documentation
- **api-documenter** + **documentation-hub**
- Complete project documentation

## 💡 Best Practices

1. **Let agents auto-activate** - They recognize relevant tasks automatically
2. **Use @-mentions for specific needs** - Direct control when needed
3. **Leverage agent-organizer** - For complex multi-step workflows
4. **Combine specialists** - Different agents for different project phases
5. **Trust the context-manager** - Maintains project understanding across sessions

## 📝 Installation Script

To install these agents in another project:
```bash
./install-default-agents.sh /path/to/project
```

Or install individually:
```bash
install-agents /path/to/project backend-architect frontend-developer nextjs-pro
```

## 🔧 Customization

Add more agents as needed:
```bash
# Browse available agents
install-agents --list

# Install additional agents
install-agents . agent-name
```

---

*Last Updated: August 9, 2025*
*Total Agents: 13*
*Categories: Development, Infrastructure, Quality, Documentation*