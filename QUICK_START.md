# AgentGen Quick Start Guide

**Get up and running with 30+ specialized AI agents in under 30 seconds.**

## Prerequisites

- Claude Code extension installed in VSCode
- Terminal access to the agentgen directory

## 🚀 30-Second Setup

### Step 1: Navigate to AgentGen
```bash
cd /path/to/agentgen
```

### Step 2: Choose Your Team Profile & Install
```bash
# For startups & small teams (11 agents)
./install-agents --profile startup-mvp

# For modern web development (12 agents)  
./install-agents --profile modern-web-stack

# For enterprise leadership (9 agents)
./install-agents --profile enterprise-leadership
```

### Step 3: Start Using Agents
```bash
# Primary orchestration - handles complex multi-step workflows
@orchestrate-tasks "build authentication system with testing"

# Direct agent invocation for specific tasks
@build-frontend "create responsive dashboard"
@security-auditor "audit authentication vulnerabilities"
```

**That's it! You're ready to transform your development workflow.**

---

## Team Profile Selection Guide

### 🚀 **startup-mvp** (11 agents)
**Best for**: Fast prototyping, resource constraints, MVP validation
- **Key Agents**: full-stack-developer, build-frontend, build-backend, debugger
- **Focus**: Rapid development with minimal overhead
- **Use Cases**: Building MVPs, small team collaboration, tight deadlines

### 🌐 **modern-web-stack** (12 agents)  
**Best for**: Modern web applications, React/TypeScript focus, UI/UX excellence
- **Key Agents**: react-specialist, nextjs-pro, ui-designer, frontend-developer
- **Focus**: Cutting-edge web technologies and user experience
- **Use Cases**: SaaS applications, e-commerce, content platforms

### 🏢 **enterprise-leadership** (9 agents)
**Best for**: Strategic decision-making, enterprise architecture, security compliance
- **Key Agents**: architect-specialist, product-manager, security-auditor, performance-engineer
- **Focus**: High-level strategy and enterprise-grade solutions
- **Use Cases**: Enterprise software, compliance-heavy industries, strategic planning

---

## Essential Usage Patterns

### Multi-Step Workflows (Recommended)
```bash
# Let orchestration handle complexity
@orchestrate-tasks "comprehensive code review and security audit"
@orchestrate-tasks "build user authentication with password reset"
@orchestrate-tasks "optimize database performance and add monitoring"
```

### Direct Agent Invocation
```bash
# Development tasks
@build-backend "create REST API for user management"
@build-frontend "implement responsive navigation component"
@full-stack-developer "build complete blog system"

# Quality & Security
@code-reviewer "analyze recent pull request changes"  
@security-auditor "scan for security vulnerabilities"
@debugger "investigate TypeError in authentication"

# Architecture & Planning
@architect-specialist "design microservices architecture"
@product-manager "analyze user requirements for dashboard"
```

### Automatic Agent Selection
```bash
# Claude Code will automatically select the right agent
"analyze this screenshot for UI requirements"     # → @analyze-screenshot
"review code quality in my recent changes"        # → @code-reviewer
"debug the failing authentication tests"          # → @debugger
```

---

## Advanced Setup Options

### Symlink Mode (Recommended)
```bash
# Install with symlinks for instant updates
./install-agents --symlink --profile startup-mvp

# Global installation (available in all projects)
./install-agents --symlink --global --profile core
```

### Custom Installations
```bash
# Install to specific directory
./install-agents --profile development-team /path/to/target

# Install individual categories
./install-agents --category development,quality

# Install all available agents
./install-agents --all
```

### Health Check & Maintenance
```bash
# Verify installation
./install-agents --health

# Repair broken symlinks
./install-agents --repair

# Update to latest agents
./install-agents --update
```

---

## Troubleshooting

### Common Issues

**Agent not found error**
```bash
# Solution: Ensure you're in the agentgen directory
cd /path/to/agentgen
./install-agents --profile your-chosen-profile
```

**Permission denied**
```bash
# Solution: Make install script executable
chmod +x install-agents
```

**Agents not responding**
```bash
# Solution: Check Claude Code extension is active
# Restart VSCode if needed
```

### Getting Help

1. **Installation Issues**: See [Installation Help](docs/getting-started/INSTALL_AGENTS_HELP.md)
2. **Usage Questions**: See [User Guide](docs/getting-started/INSTALL_AGENTS_USER_GUIDE.md)
3. **Technical Details**: See [Documentation Hub](docs/README.md)

---

## Next Steps

### Learning More
- **[Documentation Hub](docs/README.md)** - Comprehensive documentation organized by experience level
- **[Agent Categories](agents/README.md)** - Browse all available agents by specialization
- **[Technical Guides](docs/technical/)** - Advanced configuration and architecture details

### Contributing
- **[Development Archive](docs/archive/development/)** - Enhancement studies and development history
- **[Test Reports](docs/archive/analysis/)** - Performance analysis and validation results

---

## Success Metrics

After setup, you should see:
- ✅ Agents responding to @-mentions with typeahead
- ✅ @orchestrate-tasks handling complex workflows automatically  
- ✅ Context-aware agent selection for your tasks
- ✅ 3x faster development workflow with AI assistance

---

**Ready to transform your development experience?** Start with `@orchestrate-tasks` and let AgentGen guide your workflow.
