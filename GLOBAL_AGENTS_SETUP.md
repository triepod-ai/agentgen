# Global Agents Setup Documentation

## Overview

Global agents are made available across all projects by placing them in `~/.claude/agents/`. This setup uses symbolic links to maintain a single source of truth while making agents globally accessible.

## Current Global Agents

The following agents have been configured as global agents (always available in any project):

### Development Agents
- **analyze-codebase** - Project structure and architecture analysis
- **build-backend** - Backend API and service development
- **build-frontend** - Frontend UI component development
- **debug-issue** - Systematic debugging and issue resolution
- **test-automation** - Test creation and automation

### Specialist Agents
- **python-specialist** - Advanced Python development
- **react-specialist** / **react-pro** - React expertise
- **nextjs-pro** - Next.js application development
- **database-specialist** - Database design and optimization
- **ml-specialist** - Machine learning and AI development

### Infrastructure & DevOps
- **deploy-application** - Deployment and CI/CD workflows
- **deployment-engineer-specialist** - Advanced deployment engineering
- **cloud-architect-specialist** - Cloud infrastructure design
- **manage-database** - Database operations and management

### Orchestration & Management
- **orchestrate-agents** - Multi-agent coordination
- **orchestrate-tasks** - Task workflow orchestration
- **prompt-engineer** - Prompt optimization and design

### Utility Agents
- **analyze-screenshot** - Image analysis and data extraction
- **create-lesson** - Educational content creation
- **extract-insights** - Data analysis and insights
- **update-status** - Project status reporting

## Setup Instructions

### Automated Setup Script

Use the provided setup script for easy management:

```bash
# Install recommended global agents
./scripts/setup-global-agents.sh --recommended

# Check current status
./scripts/setup-global-agents.sh --status

# Install all available agents
./scripts/setup-global-agents.sh --all

# Install specific agents
./scripts/setup-global-agents.sh --specific debug-issue python-specialist

# Remove all global agents
./scripts/setup-global-agents.sh --remove
```

### Manual Setup (Symbolic Links)

```bash
# Navigate to your agent archive directory
cd ~/agentgen/archive/agents/

# Create symbolic links to ~/.claude/agents/
ln -s /home/bryan/agentgen/archive/agents/agent-name.md ~/.claude/agents/

# Or batch link multiple agents
ln -s /home/bryan/agentgen/archive/agents/*.md ~/.claude/agents/
```

### Directory Structure

```
~/.claude/agents/               # Global agents (user-level)
├── analyze-codebase.md -> /home/bryan/agentgen/archive/agents/analyze-codebase.md
├── build-backend.md -> /home/bryan/agentgen/archive/agents/build-backend.md
├── debug-issue.md -> /home/bryan/agentgen/archive/agents/debug-issue.md
└── ... (other symlinked agents)

/home/bryan/agentgen/archive/agents/  # Source agent definitions
├── analyze-codebase.md
├── build-backend.md
├── debug-issue.md
└── ... (actual agent files)

.claude/agents/                 # Project-specific agents (project-level)
└── (project-specific agents override global ones)
```

## Usage Patterns

### Invoking Global Agents

Global agents are available in any project:

```bash
# Direct @-mention (with typeahead)
@analyze-codebase review project structure
@debug-issue investigate TypeError
@python-specialist optimize this algorithm

# Explicit invocation
Use the analyze-codebase agent to review architecture
Have the debug-issue agent investigate this error
```

### Precedence Rules

1. **Project agents** (`.claude/agents/`) take precedence over global agents
2. **Global agents** (`~/.claude/agents/`) are available when no project agent exists
3. Name conflicts are resolved in favor of project-specific agents

## Management Best Practices

### Adding New Global Agents

```bash
# Link individual agent
ln -s /path/to/agent.md ~/.claude/agents/

# Verify the link
ls -la ~/.claude/agents/agent.md
```

### Removing Global Agents

```bash
# Remove symbolic link (doesn't delete source file)
rm ~/.claude/agents/agent-name.md
```

### Updating Global Agents

Since these are symbolic links, updating the source file in `/home/bryan/agentgen/archive/agents/` automatically updates the global agent.

### Listing Global Agents

```bash
# List all global agents
ls -la ~/.claude/agents/

# Show only symbolic links
find ~/.claude/agents -type l -ls
```

## Benefits of This Setup

1. **Consistency**: Same agents available across all projects
2. **Maintenance**: Single source of truth in archive directory
3. **Flexibility**: Project-specific agents can override globals
4. **Efficiency**: No duplication of agent files
5. **Version Control**: Archive directory can be version controlled

## Troubleshooting

### Agent Not Found
- Verify symbolic link exists: `ls -la ~/.claude/agents/agent-name.md`
- Check source file exists: `ls -la /home/bryan/agentgen/archive/agents/agent-name.md`
- Ensure no typos in agent name

### Agent Not Activating
- Check if project has an agent with same name (takes precedence)
- Verify agent description includes activation triggers
- Try explicit invocation first

### Broken Symbolic Links
```bash
# Find broken links
find ~/.claude/agents -type l -xtype l

# Remove broken link
rm ~/.claude/agents/broken-link.md

# Recreate link
ln -s /correct/path/to/agent.md ~/.claude/agents/
```

## Integration with Install Scripts

The `install-agents` script can be enhanced to support global installation:

```bash
# Proposed enhancement (not yet implemented)
install-agents --global agent-name  # Install to ~/.claude/agents/
install-agents --local agent-name   # Install to .claude/agents/
```

## Related Documentation

- [README.md](./README.md) - Main agent system documentation
- [AGENT_BEST_PRACTICES.md](./AGENT_BEST_PRACTICES.md) - Agent design guidelines
- [INSTALL_AGENTS_HELP.md](./INSTALL_AGENTS_HELP.md) - Installation guide
- [CLAUDE.md](./CLAUDE.md) - Project-specific Claude configuration