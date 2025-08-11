# Agent Profiles

Agent profiles allow you to install groups of related agents at once, making it easy to set up teams of specialists for different project types.

## Available Profiles

### 🏗️ development-team
Complete development team for full-stack projects
- **Infrastructure**: cloud-architect, deployment-engineer, architect-review
- **Development**: ui-designer, ux-designer, frontend-developer, full-stack-developer  
- **Quality**: code-reviewer, debugger, qa-expert, documentation-expert
- **Coordination**: agent-organizer, context-manager

### 🔒 security-audit
Security-focused team for vulnerability assessment
- **Security**: security-auditor, code-reviewer
- **Architecture**: cloud-architect, deployment-engineer, architect-review
- **Quality**: qa-expert, test-automator
- **Coordination**: agent-organizer

### 🎨 frontend-focus
UI/UX development team with design capabilities
- **Design**: ui-designer, ux-designer, frontend-developer, react-pro, nextjs-pro
- **Quality**: code-reviewer, qa-expert, test-automator
- **Coordination**: agent-organizer, context-manager

### ⚙️ backend-focus
Backend development with API and infrastructure focus
- **Backend**: backend-architect, python-pro, typescript-pro, full-stack-developer
- **Infrastructure**: database-optimizer, data-engineer, cloud-architect, deployment-engineer
- **Quality**: code-reviewer, debugger, qa-expert
- **Coordination**: agent-organizer

### 🤖 ai-ml-team
Machine learning and data science development
- **AI/ML**: ai-engineer, ml-engineer, data-scientist, data-engineer, prompt-engineer
- **Backend**: python-pro, backend-architect, database-optimizer
- **Quality**: code-reviewer, debugger
- **Coordination**: agent-organizer

## Usage

```bash
# Install a complete profile
./install-agents --profile development-team /path/to/project

# List all available profiles
./install-agents --list-profiles

# View profile details
./install-agents --show-profile development-team
```

## Profile Format

Profiles are simple text files with agent lists:

```yaml
# Profile Name
name: my-profile
description: Brief description of the profile purpose

agents:
  - agent-name-1
  - agent-name-2
  # Comments are supported
  - agent-name-3
```

## Creating Custom Profiles

1. Create a new `.profile` file in the `profiles/` directory
2. Follow the format shown above
3. List the agents you want to include
4. Use `./install-agents --profile your-profile-name` to install

## Profile Categories

- **Complete Teams**: Full development teams with all necessary roles
- **Specialized Teams**: Focused on specific domains (frontend, backend, security)
- **Project Types**: Tailored for specific project requirements (AI/ML, web apps)
- **Custom Teams**: User-created profiles for specific needs
