# Install-Agents Quick Start Guide

## TL;DR - Get Started in 30 Seconds

```bash
# Navigate to agentgen directory
cd /home/bryan/agentgen

# Install core agents to current directory (most common)
./install-agents --profile core

# Install development team setup to current directory
./install-agents --profile development-team

# Install to specific project
./install-agents --profile development-team /path/to/my-project
```

## ⚡ New Improved Defaults

The install-agents script now has better defaults for easier usage:

- **Symlink mode is DEFAULT** (was copy mode) - **✅ Fully functional**
- **Current directory is DEFAULT** (no need to specify path)
- **Force is enabled by DEFAULT** (smoother updates)
- **All strategic profiles work in BOTH modes** (symlink and copy)

### Before vs After

| **Before (old)** | **After (new)** |
|------------------|-----------------|
| `./install-agents --symlink --force --profile core .` | `./install-agents --profile core` |
| `./install-agents --copy /path/to/project --profile dev` | `./install-agents --profile dev /path/to/project` |

## 📋 Available Profiles

Quick reference for team setups:

| Profile | Description | Best For |
|---------|-------------|----------|
| `enterprise-leadership` | Strategic decision-makers (9 agents) | Large organizations (50+ people) |
| `startup-mvp` | Rapid development (11 agents) | Startups (5-15 people) |
| `modern-web-stack` | TypeScript/React (12 agents) | Mid-size teams (15-50 people) |
| `core` | Essential 15 agents | All projects |
| `development-team` | Complete dev team | Full stack teams |
| `frontend-focus` | UI/UX specialists | Frontend teams |
| `backend-focus` | API & infrastructure | Backend teams |
| `ai-ml-team` | Data science & ML | AI/ML projects |
| `security-audit` | Security specialists | Security-focused projects |
| `simple-tools` | Ultra-fast single-tool agents | Lightweight setups |

## 🚀 Common Use Cases

### 1. New Project Setup
```bash
cd /home/bryan/agentgen

# Core agents for any project
./install-agents --profile core

# Full development team
./install-agents --profile development-team

# Specific project directory
./install-agents --profile core /path/to/new-project
```

### 2. Strategic Profile Setups (NEW)
```bash
# Enterprise leadership (both modes work)
./install-agents --symlink --profile enterprise-leadership /path/to/enterprise-project
./install-agents --copy --profile enterprise-leadership /path/to/enterprise-project

# Startup MVP (both modes work)
./install-agents --symlink --profile startup-mvp /path/to/startup-project
./install-agents --copy --profile startup-mvp /path/to/startup-project

# Modern web stack (both modes work)  
./install-agents --symlink --profile modern-web-stack /path/to/web-project
./install-agents --copy --profile modern-web-stack /path/to/web-project
```

### 3. Team-Specific Setups
```bash
# Frontend team
./install-agents --profile frontend-focus /path/to/ui-project

# Backend team  
./install-agents --profile backend-focus /path/to/api-project

# AI/ML team
./install-agents --profile ai-ml-team /path/to/ml-project
```

### 4. Global Installation
```bash
# Install core agents globally (available in all projects)
./install-agents --global --profile core

# Check what's installed globally
./install-agents --list-installed ~/.claude/agents
```

### 5. Individual Agents
```bash
# Install specific agents
./install-agents code-reviewer security-auditor

# To specific project
./install-agents code-reviewer test-automator /path/to/project
```

## 🔧 Maintenance Commands

```bash
# Check health of symlinks
./install-agents --health

# Repair broken symlinks
./install-agents --repair

# Preview what would be installed
./install-agents --dry-run --profile development-team

# List what's currently installed
./install-agents --list-installed /path/to/project
```

## 📊 Information Commands

```bash
# See all available profiles
./install-agents --list-profiles

# See what's in a specific profile
./install-agents --show-profile development-team

# List all available agents
./install-agents --list

# See installed agents in a project
./install-agents --list-installed /path/to/project
```

## 🔄 Legacy Copy Mode

For backward compatibility or when you need isolated agent copies:

```bash
# Use copy mode instead of symlink
./install-agents --copy --profile development-team /path/to/project

# Copy specific agents
./install-agents --copy code-reviewer security-auditor /path/to/project
```

## ⚠️ Important Notes

### Must Run from agentgen Directory
```bash
# ❌ Wrong - will fail
cd /some/other/directory
./install-agents --profile core

# ✅ Correct - always run from agentgen
cd /home/bryan/agentgen
./install-agents --profile core
```

### Understanding the Modes

**Symlink Mode (DEFAULT)**
- ✅ Single source of truth
- ✅ Instant updates when agents change
- ✅ 95% less disk space
- ✅ Easy maintenance

**Copy Mode (Legacy)**
- ✅ Independent files per project
- ✅ No dependencies on central hub
- ❌ Manual updates required
- ❌ More disk space used

## 🛠️ Troubleshooting

### Quick Fixes

| Problem | Solution |
|---------|----------|
| Script not found | `cd /home/bryan/agentgen` |
| Permission denied | `chmod +x ./install-agents` |
| Broken symlinks | `./install-agents --repair` |
| Agents not updating | `./install-agents --health` then `--repair` |
| Want fresh install | `./install-agents --profile development-team` (force enabled by default) |

### Health Check
```bash
# Check if everything is working
./install-agents --health

# If issues found, repair them
./install-agents --repair

# Force reinstall if needed
./install-agents --profile development-team
```

## 📖 Next Steps

1. **Choose a profile** that matches your team
2. **Install to current directory** for quick testing
3. **Install globally** for core agents you always need
4. **Install project-specific** profiles as needed
5. **Set up team standards** using consistent profiles

### Example Team Workflow
```bash
# Team lead sets up standards
cd /home/bryan/agentgen

# Global core agents for everyone
./install-agents --global --profile core

# Project-specific setup
./install-agents --profile development-team /path/to/team-project

# Document in team README:
# "Run: ./install-agents --profile development-team"
```

---

**Pro Tip**: The new defaults make most installations just one command: `./install-agents --profile PROFILE_NAME`