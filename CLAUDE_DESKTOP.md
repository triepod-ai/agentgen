# AgentGen - Claude Desktop Quick Reference

**WSL Environment for AgentGen Enterprise AI Development Platform**

Essential operations for Claude Desktop working with the AgentGen system in WSL2 environment.

## 🚀 Essential Operations (80% of Usage)

### Critical Setup (Required First)
```bash
# STEP 1: Navigate to agentgen directory (MANDATORY)
cd /home/bryan/agentgen

# STEP 2: Convert Windows paths to WSL (if needed)
WSL_PATH=$(convert_path "C:\Your\Windows\Path")

# Path conversion function
convert_path() {
    if [[ "$1" =~ ^[A-Za-z]: ]]; then
        wslpath -u "$1"  # C:\ → /mnt/c/
    else
        echo "$1"        # Already WSL path
    fi
}
```

### 🗂️ Claude Desktop Filesystem Access Strategy

**CRITICAL: Tool Selection for WSL Environment**

```bash
# ✅ RECOMMENDED: Always use Bash first for path discovery
Bash("ls -la /home/bryan/agentgen")        # Works reliably in WSL
Bash("find /home/bryan/agentgen/agents")   # Safe for directory exploration

# ⚠️ CAUTION: Read/LS tools may misinterpret WSL paths
Read("/home/bryan/agentgen/file.md")       # May fail with "C:\home\..." error
LS("/home/bryan/agentgen/")                # Use after confirming path with Bash

# 🔄 ERROR RECOVERY PATTERN
# If Read/LS fails with Windows path error → Switch to Bash immediately
Bash("cat /home/bryan/agentgen/file.md")   # Always works as fallback
```

**Best Practice Workflow:**
1. **Path Discovery**: Use `Bash("ls /path")` to verify directory structure
2. **File Operations**: After path confirmation, use `Read()` for file content
3. **Error Recovery**: If filesystem tools show "C:\..." errors, use Bash commands

### Primary Installation Commands
```bash
# Strategic Profiles (Most Common)
./install-agents --symlink --profile enterprise-leadership "$WSL_PATH"  # 9 strategic agents
./install-agents --symlink --profile modern-web-stack "$WSL_PATH"      # 12 React/TypeScript  
./install-agents --symlink --profile startup-mvp "$WSL_PATH"           # 11 lean development

# Standard Profiles  
./install-agents --profile core                          # Essential 16 agents (global)
./install-agents --profile development-team "$WSL_PATH"  # Full development team

# Health Management
./install-agents --symlink --health                      # Check system status
./install-agents --symlink --repair                      # Fix broken symlinks
```

### Profile Selection Matrix
| Profile | Agents | Focus | Best For |
|---------|--------|-------|----------|
| **enterprise-leadership** | 9 | Strategic decisions | C-level planning, enterprise architecture |
| **modern-web-stack** | 12 | React/TypeScript | Frontend apps, UI/UX projects |
| **startup-mvp** | 11 | Full-stack rapid | MVP development, resource constraints |
| **development-team** | 19 | Complete coverage | General development, all scenarios |

### Primary Orchestration 
```bash
# Main entry point (80% of complex tasks)
@orchestrate-tasks "comprehensive task description"

# Direct specialist invocation
@security-auditor "audit application vulnerabilities"
@architect-specialist "design microservices architecture"
@react-specialist "optimize component performance"
```

## 🏗️ Key Paths & Locations

### Essential Directories
```bash
# Core paths (memorize these)
AGENTGEN="/home/bryan/agentgen"                    # Base directory (work from here)
AGENT_HUB="/home/bryan/agentgen/agents"            # Central agent repository
USER_AGENTS="/home/bryan/.claude/agents"          # Global user agents
PROJECT_AGENTS="{project}/.claude/agents"         # Project-specific (highest priority)
```

### Agent Storage Priority
1. **Project** (`{project}/.claude/agents/`) - Overrides all others
2. **Global** (`~/.claude/agents/`) - User-wide availability  
3. **Hub** (`/home/bryan/agentgen/agents/`) - Reference source

## 🔧 Quick Troubleshooting

| Problem | Symptoms | Solution |
|---------|----------|----------|
| **Script not found** | `./install-agents: No such file` | `cd /home/bryan/agentgen` |
| **Permission denied** | `Permission denied: install-agents` | `chmod +x ./install-agents` |
| **Broken symlinks** | Agents not found after install | `./install-agents --symlink --repair` |
| **Path errors** | Windows paths fail | Use `convert_path()` function |

### Common Quick Fixes
```bash
# Fix permissions
chmod +x ./install-agents ./migrate-to-symlinks.sh

# Repair broken symlinks
./install-agents --symlink --repair

# Convert and install in one command  
./install-agents --profile modern-web-stack $(convert_path "C:\project")
```

## 🎯 Common Workflows

### New Project Setup
```bash
cd /home/bryan/agentgen
WSL_PATH=$(convert_path "C:\your\project\path")
./install-agents --symlink --profile modern-web-stack "$WSL_PATH"
@orchestrate-tasks "setup project with authentication and testing"
```

### Agent Health Check
```bash
cd /home/bryan/agentgen
./install-agents --symlink --health      # Check status
./install-agents --symlink --repair      # Fix issues if needed
```

### Quick Agent Creation
```bash
# Create project-specific agent
mkdir -p .claude/agents
cat > .claude/agents/my-agent.md << 'EOF'
---
name: my-agent
description: Brief description for auto-activation
tools: Read, Write, Edit
---
# Agent system prompt
Execute task → return results
EOF
```

## 📚 Detailed Documentation

For comprehensive information, see specialized reference documents:

| Topic | Document | Contains |
|-------|----------|----------|
| **System Architecture** | [CLAUDE_DESKTOP_ARCHITECTURE.md](CLAUDE_DESKTOP_ARCHITECTURE.md) | Agent categories, directory structure, complexity tiers |
| **Enhancement System** | [CLAUDE_DESKTOP_ENHANCEMENTS.md](CLAUDE_DESKTOP_ENHANCEMENTS.md) | BRAINPOD integration, ML pipelines, enhanced agents |
| **Development Guide** | [CLAUDE_DESKTOP_DEVELOPMENT.md](CLAUDE_DESKTOP_DEVELOPMENT.md) | Agent creation, optimization, testing procedures |
| **Troubleshooting** | [CLAUDE_DESKTOP_TROUBLESHOOTING.md](CLAUDE_DESKTOP_TROUBLESHOOTING.md) | Complete problem resolution, advanced configuration |

## 💡 Key Principles

- **Always** start from `/home/bryan/agentgen` directory
- **Convert** Windows paths before any operations  
- **Use** symlink mode for live updates and efficiency
- **Start** with @orchestrate-tasks for complex operations
- **Check** health status before reporting issues

---
*Optimized for Claude Desktop WSL2 environment - Essential operations only*