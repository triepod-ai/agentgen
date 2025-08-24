# AgentGen - Claude Desktop Quick Reference Card

**Essential Commands & Patterns | 1-Page Cheat Sheet**

---

## 🚀 **Setup (30 seconds)**

```bash
# STEP 1: Navigate to agentgen (MANDATORY)
cd /home/bryan/agentgen

# STEP 2: Choose your team profile and install
./install-agents --symlink --profile enterprise-leadership /path/to/project  # 9 strategic agents
./install-agents --symlink --profile modern-web-stack /path/to/project      # 12 React/TypeScript
./install-agents --symlink --profile startup-mvp /path/to/project           # 11 lean development
```

## 🗂️ **Claude Desktop Tool Selection (CRITICAL)**

```bash
# ✅ ALWAYS USE BASH FIRST for path discovery
Bash("ls -la /home/bryan/agentgen")        # Works reliably in WSL
Bash("find /home/bryan/agentgen/agents")   # Safe for directory exploration

# ⚠️ THEN USE Read/LS for file operations
Read("/home/bryan/agentgen/file.md")       # Use after confirming path
LS("/home/bryan/agentgen/directory/")      # Use after Bash verification

# 🔄 IF ERROR (C:\home\...) → Switch to Bash immediately
Bash("cat /home/bryan/agentgen/file.md")   # Always works as fallback
```

## 🎯 **Primary Operations (80% of Usage)**

### **Orchestration (Most Common)**
```bash
# Main entry point - handles complex tasks automatically
@orchestrate-tasks "build authentication system with security audit"
@orchestrate-tasks "comprehensive code review and optimization"

# Direct specialist invocation
@security-auditor "audit application vulnerabilities"
@react-specialist "optimize component performance"
@architect-specialist "design microservices architecture"
```

### **Path Conversion (Windows→WSL)**
```bash
# Built-in function for Windows paths
convert_path() {
    if [[ "$1" =~ ^[A-Za-z]: ]]; then
        wslpath -u "$1"  # C:\ → /mnt/c/
    else
        echo "$1"        # Already WSL path
    fi
}

# Usage example
WSL_PATH=$(convert_path "C:\Your\Project\Path")
./install-agents --profile modern-web-stack "$WSL_PATH"
```

### **Health & Maintenance**
```bash
./install-agents --symlink --health    # Check system status
./install-agents --symlink --repair    # Fix broken symlinks
./install-agents --list               # Show available profiles
```

## 📊 **Agent Categories (112 Total)**

| Category | Count | Key Agents | Use For |
|----------|-------|------------|---------|
| **Specialists** | ~60 | react-specialist, security-auditor, architect-specialist | Complex domain tasks |
| **Tools** | ~15 | orchestrate-tasks, install-agents-manager | System coordination |
| **Development** | 8 | build-frontend, build-backend, full-stack-developer | Core development |
| **Quality** | 6 | code-reviewer-pro, qa-expert, test-automator | QA and testing |
| **Core** | 7 | analyze-codebase, context-manager, debugger | Basic operations |
| **Infrastructure** | 5 | deployment-engineer, cloud-architect | DevOps and deployment |
| **Content** | 5 | documentation-expert, create-lesson | Documentation |
| **Simple** | 5 | analyze-screenshot, config-reader | Quick utility tasks |
| **Data** | 3 | extract-insights, ml-engineer | Data analysis |
| **Business** | 3 | product-manager, business-integrator | Business logic |

## 🚨 **Troubleshooting Flowchart**

```
ERROR: Script not found
    ↓
cd /home/bryan/agentgen

ERROR: Permission denied  
    ↓
chmod +x ./install-agents

ERROR: Agents not found after install
    ↓
./install-agents --symlink --repair

ERROR: Windows path fails (C:\...)
    ↓
Use convert_path() function OR Bash commands

ERROR: Read/LS shows "C:\home\..." 
    ↓  
Switch to Bash("command") immediately
```

## 💡 **Pro Tips**

### **Strategic Profile Selection**
- **Enterprise Leadership** → C-level decisions, architecture planning
- **Modern Web Stack** → React/TypeScript projects, UI/UX focus  
- **Startup MVP** → Fast prototyping, resource constraints
- **Development Team** → General purpose, complete coverage (19 agents)

### **Best Practices**
- Start with `@orchestrate-tasks` for complex operations
- Use symlink mode (`--symlink`) for live updates
- Always run from `/home/bryan/agentgen` directory
- Use `Bash()` first, then `Read()` in Claude Desktop
- Trust auto-activation - agents activate based on task descriptions

### **Quick Commands**
```bash
# Emergency reset
chmod +x ./install-agents && ./install-agents --symlink --repair

# One-liner installation with path conversion
./install-agents --profile modern-web-stack $(convert_path "C:\project")

# Health check everything
./install-agents --symlink --health
```

---

## 📚 **Complete Documentation**

- **[CLAUDE_DESKTOP.md](CLAUDE_DESKTOP.md)**: Daily operations guide
- **[CLAUDE_DESKTOP_EXECUTIVE.md](CLAUDE_DESKTOP_EXECUTIVE.md)**: 5-minute strategic overview  
- **[CLAUDE.md](CLAUDE.md)**: Complete project documentation
- **[CLAUDE_DESKTOP_TROUBLESHOOTING.md](CLAUDE_DESKTOP_TROUBLESHOOTING.md)**: Problem resolution

---

**AgentGen: 112 specialized agents, 5-minute setup, immediate productivity gains**