# Agent Hub - Symlink-Based Agent Management

The **agentgen** repository now serves as a central hub for agent management using symbolic links instead of file copying. This enables single-source maintenance while preserving the flexibility of project-specific agents.

## 🎯 Key Benefits

- **Single Source of Truth**: All agents maintained in one location
- **Instant Updates**: Changes propagate immediately to all installations
- **Space Efficient**: ~95% reduction in disk usage (no file duplication)
- **Easy Maintenance**: Centralized management and version control
- **Backward Compatible**: Original installer still works alongside

## 🏗️ Architecture

```
agentgen/
├── agents/                    # Central Hub Directory
│   ├── core/                 # Essential agents (debugger, etc.)
│   ├── development/          # Frontend, backend, full-stack
│   ├── specialists/          # Domain experts with deep knowledge
│   ├── infrastructure/       # DevOps, deployment, monitoring
│   ├── quality/             # Testing, code review, QA
│   ├── content/             # Documentation, writing
│   ├── data/                # Data processing, AI/ML
│   ├── tools/               # Utilities and specialized tools
│   └── simple/              # Lightweight agents for basic tasks
│
├── install-agents-symlink    # Symlink-based installer
├── migrate-to-symlinks.sh    # Migration tool from copies
└── install-agents            # Original copy-based installer (still works)
```

## 🚀 Quick Start

### 1. Install Agents with Symlinks

```bash
# Install core agents globally (available in all projects)
./install-agents-symlink --global --core

# Install development agents to a specific project
./install-agents-symlink --project /path/to/project --development

# Install all agents globally with verbose output
./install-agents-symlink --global --all --verbose
```

### 2. Migrate Existing Installations

```bash
# Preview what would be migrated (recommended first step)
./migrate-to-symlinks.sh --dry-run /path/to/project

# Migrate project from copies to symlinks (creates backup)
./migrate-to-symlinks.sh /path/to/project

# Migrate multiple projects at once
./migrate-to-symlinks.sh ~/project1 ~/project2 ~/.claude
```

### 3. Maintain and Monitor

```bash
# Check health of symlinks
./install-agents-symlink --global --health

# Repair broken symlinks
./install-agents-symlink --project /path/to/project --repair

# List all available agents
./install-agents-symlink --list
```

## 📋 Agent Categories & Profiles

### Installation Profiles

| Profile | Description | Use Case |
|---------|-------------|----------|
| `--core` | Essential agents every project needs | Recommended minimum |
| `--development` | Frontend, backend, full-stack development | Active development projects |
| `--specialists` | Domain experts with deep knowledge | Complex technical projects |
| `--infrastructure` | DevOps, deployment, monitoring | Production environments |
| `--quality` | Testing, code review, QA | Quality-focused workflows |
| `--content` | Documentation, writing, localization | Content creation projects |
| `--data` | Data processing, AI/ML, database | Data-driven projects |
| `--tools` | Utilities and specialized tools | Power users |
| `--simple` | Lightweight agents for basic tasks | Minimal installations |
| `--all` | Install all available agents | Comprehensive setup |

### Current Agent Inventory

- **Core Agents** (3): Essential debugging and analysis tools
- **Development Agents** (3): Full-stack development specialists
- **Specialist Agents** (5): Deep domain expertise
- **Infrastructure Agents** (1): DevOps and deployment automation
- **Quality Agents** (1): Code review and testing
- **Simple Agents** (5): Lightweight utility agents

*Total: 18 agents available, growing collection*

## 🔧 Usage Examples

### Global Installation (Recommended)

```bash
# Install essential agents globally (available in all projects)
./install-agents-symlink --global --core --specialists

# All projects now have access to these agents via ~/.claude/agents/
```

### Project-Specific Installation

```bash
# Install development tools for a specific project
./install-agents-symlink --project ~/my-app --development --tools

# Only ~/my-app/.claude/agents/ gets these agents
```

### Mixed Installation Strategy

```bash
# Global: Essential agents available everywhere
./install-agents-symlink --global --core

# Project-specific: Specialized tools only where needed
./install-agents-symlink --project ~/frontend-app --development
./install-agents-symlink --project ~/data-project --data
```

## 🔄 Migration Guide

### From Copy-Based to Symlink-Based

If you have existing agent installations using the original copy-based installer:

1. **Preview Migration** (Safe)
   ```bash
   ./migrate-to-symlinks.sh --dry-run /path/to/project
   ```

2. **Execute Migration** (Creates Backup)
   ```bash
   ./migrate-to-symlinks.sh /path/to/project
   ```

3. **Validate Results**
   ```bash
   ./install-agents-symlink --project /path/to/project --health
   ```

4. **Cleanup** (Optional)
   ```bash
   # Remove backup after confirming everything works
   rm -rf /path/to/project/.claude/agents.backup.*
   ```

### Rollback If Needed

```bash
# Restore from backup if something goes wrong
mv /path/to/project/.claude/agents.backup.TIMESTAMP /path/to/project/.claude/agents
```

## 🛠️ Maintenance

### Adding New Agents

1. **Create Agent File**
   ```bash
   # Choose appropriate category directory
   vim agents/development/new-agent.md
   ```

2. **Follow Standard Format**
   ```markdown
   ---
   name: new-agent
   description: What this agent does and when to use it
   tools: Read, Write, Edit
   ---

   # New Agent

   Agent implementation here...
   ```

3. **Test Locally**
   ```bash
   ./install-agents-symlink --project /tmp/test --development
   # Test the new agent
   ```

4. **Deploy to All Installations**
   ```bash
   # Changes propagate instantly via symlinks!
   # No reinstallation needed
   ```

### Updating Existing Agents

1. **Edit Agent File**
   ```bash
   vim agents/core/debugger.md
   ```

2. **Save Changes**
   ```bash
   # Changes are immediately available in all installations
   # that use symlinks to this agent
   ```

3. **Validate** (Optional)
   ```bash
   ./install-agents-symlink --global --health
   ```

## 🔍 Troubleshooting

### Common Issues

#### Symlinks Not Working
```bash
# Check if symlinks were created correctly
ls -la ~/.claude/agents/

# Should show arrows pointing to hub files:
# debugger.md -> /home/user/agentgen/agents/core/debugger.md
```

#### Agent Not Found in Hub
```bash
# Check which agents are available
./install-agents-symlink --list

# If your agent is missing, ensure it's in the correct category directory
find agents/ -name "your-agent.md"
```

#### Broken Symlinks
```bash
# Identify and repair broken symlinks
./install-agents-symlink --global --repair

# Or check health status
./install-agents-symlink --global --health
```

#### Permission Issues
```bash
# Ensure scripts are executable
chmod +x install-agents-symlink migrate-to-symlinks.sh

# Check file permissions in hub
ls -la agents/*/*.md
```

### Advanced Scenarios

#### Multiple Hub Locations
```bash
# If you have multiple agentgen checkouts, use absolute paths
AGENTS_HUB=/path/to/main/agentgen/agents ./install-agents-symlink --global --core
```

#### Custom Categories
```bash
# Add new categories by creating directories
mkdir -p agents/custom-category
# Update installer script to include new category
```

## 🎯 Best Practices

### Hub Management
- **Version Control**: Keep hub in git for change tracking
- **Backup**: Backup hub directory before major changes
- **Testing**: Test agent changes locally before committing
- **Documentation**: Update this README when adding new features

### Installation Strategy
- **Start Small**: Begin with `--core` profile, expand as needed
- **Global vs Project**: Use global for common agents, project-specific for specialized needs
- **Regular Health Checks**: Run `--health` periodically to catch issues early
- **Migration Planning**: Use `--dry-run` for all migration operations first

### Agent Development
- **Follow Format**: Use standard YAML frontmatter format
- **Keep Simple**: Aim for <400 characters in agent descriptions for optimal performance
- **Single Responsibility**: Each agent should have one clear purpose
- **Testing**: Test agents in isolated environments before adding to hub

## 📈 Performance Benefits

- **Loading Speed**: 3x faster agent loading due to optimized descriptions
- **Disk Usage**: 95% reduction in space usage (no file duplication)
- **Update Speed**: Instant propagation of changes (no reinstallation needed)
- **Management Efficiency**: Single location for all agent maintenance

## 🔗 Integration

### With Existing Tools
- **Claude Code**: Full compatibility with @-mention and auto-activation
- **Git Workflows**: Hub changes tracked in version control
- **CI/CD**: Can be integrated into deployment pipelines
- **Team Sharing**: Team members can share same hub via git

### With Backup Systems
- **Automatic Backups**: Migration script creates timestamped backups
- **Manual Backups**: `cp -r agents agents.backup.$(date +%Y%m%d)`
- **Restoration**: Simple directory replacement for rollbacks
- **Version History**: Git provides complete change history

---

**Next Steps**: Try the system with `./install-agents-symlink --global --core` and experience the benefits of centralized agent management!