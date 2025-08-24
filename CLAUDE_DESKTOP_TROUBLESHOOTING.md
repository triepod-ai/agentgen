# AgentGen Troubleshooting Guide - Claude Desktop Reference

Comprehensive problem resolution, debugging procedures, and advanced configuration for AgentGen system issues.

## 🚨 Quick Problem Resolution

### Most Common Issues (90% of Problems)

| Symptom | Cause | Solution | Prevention |
|---------|-------|----------|------------|
| `./install-agents: No such file` | Wrong directory | `cd /home/bryan/agentgen` | Always start from agentgen |
| `Permission denied: install-agents` | Missing execute permissions | `chmod +x ./install-agents` | Check permissions first |
| Agent not found after install | Broken symlinks | `./install-agents --symlink --repair` | Use health checks |
| Windows path errors | Path not converted | Use `convert_path()` function | Always convert paths |
| Orchestration agent not found | Missing installation | Install via @install-agents-manager | Use auto-installation |

### Emergency Quick Fixes
```bash
# Universal agent system reset
cd /home/bryan/agentgen
chmod +x ./install-agents ./migrate-to-symlinks.sh
./install-agents --symlink --health
./install-agents --symlink --repair

# Path conversion emergency
WSL_PATH=$(wslpath -u "C:\Your\Windows\Path")
./install-agents --profile core "$WSL_PATH"

# Permission emergency reset  
find .claude/agents -type f -exec chmod 644 {} \;
find .claude/agents -type d -exec chmod 755 {} \;
```

## 🔧 Installation Issues

### Symlink Problems

#### Broken Symlinks Detection
```bash
# Check for broken symlinks
find .claude/agents -type l ! -exec test -e {} \; -print

# Comprehensive health check
./install-agents --symlink --health

# Example output:
# ✅ Central hub accessible: /home/bryan/agentgen/agents
# ❌ Broken symlink: .claude/agents/missing-agent.md
# ✅ 34/36 agents functional
```

#### Symlink Repair Process
```bash
# Automatic repair
./install-agents --symlink --repair

# Manual repair for specific agent
rm .claude/agents/broken-agent.md
ln -sf /home/bryan/agentgen/agents/core/working-agent.md .claude/agents/working-agent.md

# Verify repair
ls -la .claude/agents/ | grep broken-agent
# Should show proper symlink target
```

#### Migration Issues
```bash
# Migration from copy to symlink mode
./migrate-to-symlinks.sh /path/to/project

# If migration fails:
# 1. Backup existing agents
cp -r .claude/agents .claude/agents.backup

# 2. Force clean migration
rm -rf .claude/agents
./install-agents --symlink --profile development-team /current/path

# 3. Restore custom agents manually
cp .claude/agents.backup/custom-agent.md .claude/agents/
```

### Profile Installation Issues

#### Profile Not Found
```bash
# List available profiles
./install-agents --list

# Common profiles:
# ✅ core, development-team, enterprise-leadership
# ✅ modern-web-stack, startup-mvp
# ❌ invalid-profile-name

# Check profile file exists
ls -la profiles/your-profile.txt
```

#### Incomplete Profile Installation
```bash
# Verify installation completeness
expected_count=$(cat profiles/development-team.txt | wc -l)
actual_count=$(find .claude/agents -name "*.md" | wc -l)

echo "Expected: $expected_count agents"
echo "Installed: $actual_count agents"

# If mismatch, reinstall
./install-agents --profile development-team --force
```

## 🔄 Agent Operation Issues

### Agent Not Recognized

#### Diagnosis Steps
```bash
# 1. Check agent file exists
ls -la .claude/agents/your-agent.md

# 2. Validate YAML frontmatter
head -n 10 .claude/agents/your-agent.md
# Should show:
# ---
# name: your-agent
# description: ...
# ---

# 3. Check agent syntax
./validate-agent.sh .claude/agents/your-agent.md
```

#### Common Agent File Issues
```yaml
# ❌ Invalid YAML frontmatter
name: agent-without-dashes
description missing quotes: This breaks parsing

# ✅ Valid YAML frontmatter  
---
name: agent-with-dashes
description: "Properly quoted description"
tools: Read, Write, Edit
---
```

#### Auto-Activation Problems
```bash
# Test agent description triggers
echo "debug authentication error" | monitor_agent_activation
# Should activate: debugger, security-auditor, or backend specialists

# If wrong agent activates:
# 1. Check description keywords
# 2. Verify competing agents don't have conflicting triggers
# 3. Update description with specific triggers
```

### Performance Issues

#### Slow Agent Response
```bash
# Profile agent performance
time echo "test task" | @your-agent

# Targets by complexity:
# Green: <500ms
# Yellow: <2s
# Red: <5s

# If exceeding targets:
# 1. Check agent character count
wc -c .claude/agents/your-agent.md
# Target: <400 characters

# 2. Minimize tools
# Remove unnecessary tools from frontmatter

# 3. Optimize prompt
# Use arrow workflows: Step1 → Step2 → Result
```

#### High Token Usage
```bash
# Check agent prompt length
wc -w .claude/agents/verbose-agent.md
# Target: <100 words for optimal agents

# Optimization techniques:
sed -i 's/detailed analysis/analysis/g' .claude/agents/your-agent.md
sed -i 's/comprehensive/complete/g' .claude/agents/your-agent.md
sed -i 's/Execute the following workflow:/Execute:/g' .claude/agents/your-agent.md
```

## 🌐 Path and Environment Issues

### Windows-WSL Path Conversion

#### Path Conversion Debugging
```bash
# Test path conversion function
convert_path() {
    if [[ "$1" =~ ^[A-Za-z]: ]]; then
        wslpath -u "$1"
    else
        echo "$1"
    fi
}

# Test cases
convert_path "C:\Users\bryan\project"    # Should: /mnt/c/Users/bryan/project
convert_path "/home/bryan/project"       # Should: /home/bryan/project (unchanged)
convert_path "D:\workspace\app"          # Should: /mnt/d/workspace/app
```

#### Common Path Problems
```bash
# Problem: Spaces in Windows paths
WINDOWS_PATH="C:\Program Files\Project Name"
# ❌ Wrong: install-agents --profile core C:\Program Files\Project Name
# ✅ Correct: 
WSL_PATH=$(convert_path "$WINDOWS_PATH")
./install-agents --profile core "$WSL_PATH"

# Problem: Backslash escaping
# ❌ Wrong: "C:\\Users\\bryan\\project"
# ✅ Correct: "C:\Users\bryan\project" or 'C:\Users\bryan\project'
```

#### Environment Detection Issues
```bash
# Verify WSL environment
echo $WSLENV                    # Should show WSL environment variables
uname -r | grep microsoft      # Should show microsoft kernel

# If environment detection fails:
export WSLENV="PATH/l"
export WSL_DISTRO_NAME="Ubuntu"

# Test environment detection
if [[ -n "$WSLENV" ]] || [[ "$(uname -r)" == *microsoft* ]]; then
    echo "✅ WSL environment detected"
else
    echo "❌ WSL environment not detected"
fi
```

## 🎛️ Advanced Configuration

### Claude Desktop Settings

#### .claude/settings.local.json Configuration
```json
{
  "tools": {
    "bash": {
      "permissions": [
        "Bash(cd:*)",
        "Bash(ls:*)",
        "Bash(convert_path:*)",
        "Bash(/home/bryan/agentgen/install-agents:*)",
        "Bash(/home/bryan/agentgen/migrate-to-symlinks.sh:*)",
        "Bash(chmod:*)",
        "Bash(find:*)"
      ]
    }
  },
  "hooks": {
    "user-prompt-submit": "/home/bryan/.claude/scripts/path-converter.sh"
  }
}
```

#### Settings Validation
```bash
# Check settings file size (should be <15KB)
ls -lh .claude/settings.local.json

# Validate JSON syntax
jq '.' .claude/settings.local.json > /dev/null
echo "JSON syntax: $?"  # Should be 0

# Check for bloated permissions
grep -c "Bash(" .claude/settings.local.json
# Should be <50 for reasonable file size
```

### Custom Hook Configuration
```bash
# Create path converter hook
mkdir -p /home/bryan/.claude/scripts
cat > /home/bryan/.claude/scripts/path-converter.sh << 'EOF'
#!/bin/bash
# Auto-convert Windows paths in user prompts
input="$1"
if [[ "$input" =~ [A-Za-z]:\\[^[:space:]]+ ]]; then
    # Extract Windows path and convert
    win_path=$(echo "$input" | grep -o '[A-Za-z]:\\[^[:space:]]\+')
    wsl_path=$(wslpath -u "$win_path")
    echo "${input/$win_path/$wsl_path}"
else
    echo "$input"
fi
EOF
chmod +x /home/bryan/.claude/scripts/path-converter.sh
```

## 🔍 Orchestration Issues

### Context-Manager Problems

#### Context-Manager Not Accessible
```bash
# Check context-manager status
ls -la /sub-agents/context/context-manager.json
# Should show recent timestamp

# If missing or stale:
# 1. Check context-manager agent is installed
ls -la .claude/agents/context-manager.md

# 2. Trigger context-manager update
@context-manager "refresh project context"

# 3. Verify update worked
ls -la /sub-agents/context/context-manager.json
```

#### Cross-Agent Communication Issues
```bash
# Test agent communication protocol
echo '{"requesting_agent":"test","request_type":"status","payload":{"test":true}}' | \
@context-manager

# Should return structured JSON response
# If not working:
# 1. Check context-manager agent definition
# 2. Verify JSON parsing in agent prompt
# 3. Test with simpler communication
```

### Orchestration Agent Missing
```bash
# Check orchestration agents installed
ls -la .claude/agents/ | grep orchestrate
# Should show: orchestrate-tasks.md, orchestrate-agents.md, orchestrate-agents-adv.md

# If missing, install automatically
@install-agents-manager "install missing orchestration agents"

# Or install manually
./install-agents --profile core $(pwd)
```

## 🛠️ System Diagnostics

### Comprehensive Health Check
```bash
#!/bin/bash
# Complete AgentGen health diagnostic

echo "🔍 AgentGen System Diagnostic"
echo "=============================="

# 1. Environment Check
echo "1. Environment Status:"
echo "   Working Directory: $(pwd)"
echo "   WSL Environment: $([[ -n "$WSLENV" ]] && echo "✅ Detected" || echo "❌ Missing")"
echo "   AgentGen Access: $([[ -d "/home/bryan/agentgen" ]] && echo "✅ Available" || echo "❌ Missing")"

# 2. Installation Check  
echo "2. Installation Status:"
echo "   install-agents: $([[ -x "./install-agents" ]] && echo "✅ Executable" || echo "❌ Missing/No permission")"
echo "   Agent Hub: $([[ -d "/home/bryan/agentgen/agents" ]] && echo "✅ Available" || echo "❌ Missing")"

# 3. Agent Status
echo "3. Agent Status:"
agent_count=$(find .claude/agents -name "*.md" 2>/dev/null | wc -l)
echo "   Installed Agents: $agent_count"
broken_symlinks=$(find .claude/agents -type l ! -exec test -e {} \; -print 2>/dev/null | wc -l)
echo "   Broken Symlinks: $broken_symlinks"

# 4. Orchestration Check
echo "4. Orchestration Status:"
echo "   orchestrate-tasks: $([[ -f ".claude/agents/orchestrate-tasks.md" ]] && echo "✅ Available" || echo "❌ Missing")"
echo "   context-manager: $([[ -f "/sub-agents/context/context-manager.json" ]] && echo "✅ Active" || echo "⚠️  Inactive")"

# 5. Performance Check
echo "5. Performance Indicators:"
large_agents=$(find .claude/agents -name "*.md" -exec wc -c {} + 2>/dev/null | awk '$1 > 400' | wc -l)
echo "   Agents >400 chars: $large_agents (target: 0)"

echo
echo "Diagnostic Complete. See troubleshooting guide for issue resolution."
```

### Performance Monitoring
```bash
# Monitor agent response times
monitor_performance() {
    agents=("debugger" "security-auditor" "react-specialist")
    test_task="analyze current status"
    
    for agent in "${agents[@]}"; do
        if [[ -f ".claude/agents/$agent.md" ]]; then
            echo "Testing $agent:"
            start_time=$(date +%s%N)
            result=$(echo "$test_task" | timeout 10s @$agent 2>/dev/null)
            end_time=$(date +%s%N)
            
            if [[ $? -eq 0 ]]; then
                response_time=$(((end_time - start_time) / 1000000))
                echo "  ✅ Response time: ${response_time}ms"
            else
                echo "  ❌ Agent timeout or error"
            fi
        else
            echo "  ❌ Agent not installed: $agent"
        fi
    done
}
```

## 🔄 Recovery Procedures

### Complete System Reset
```bash
# Nuclear option: Full AgentGen reset
reset_agentgen_system() {
    echo "⚠️  Performing complete AgentGen system reset"
    
    # 1. Backup current setup
    backup_dir="/tmp/agentgen-backup-$(date +%s)"
    mkdir -p "$backup_dir"
    [[ -d ".claude" ]] && cp -r .claude "$backup_dir/"
    
    # 2. Clean slate
    rm -rf .claude/agents
    
    # 3. Navigate to agentgen
    cd /home/bryan/agentgen || {
        echo "❌ Cannot access /home/bryan/agentgen"
        return 1
    }
    
    # 4. Fix permissions
    chmod +x ./install-agents ./migrate-to-symlinks.sh
    
    # 5. Fresh installation
    ./install-agents --symlink --profile development-team $(pwd)
    
    # 6. Health check
    ./install-agents --symlink --health
    
    echo "✅ System reset complete. Backup available at: $backup_dir"
}
```

### Selective Agent Repair
```bash
# Repair specific problematic agents
repair_agent() {
    agent_name="$1"
    
    echo "Repairing agent: $agent_name"
    
    # Remove broken agent
    rm -f ".claude/agents/$agent_name.md"
    
    # Find source in hub
    source_agent=$(find /home/bryan/agentgen/agents -name "$agent_name.md" -type f)
    
    if [[ -n "$source_agent" ]]; then
        # Recreate symlink
        ln -sf "$source_agent" ".claude/agents/$agent_name.md"
        echo "✅ Repaired: $agent_name"
    else
        echo "❌ Source not found for: $agent_name"
        return 1
    fi
}
```

## 📊 Error Codes & Messages

### Common Error Patterns
```yaml
error_patterns:
  "No such file or directory":
    cause: "Wrong working directory"
    solution: "cd /home/bryan/agentgen"
  
  "Permission denied":
    cause: "Missing execute permissions"
    solution: "chmod +x ./install-agents"
  
  "Broken pipe":
    cause: "Agent process interrupted"
    solution: "Restart agent or check system resources"
  
  "Invalid YAML":
    cause: "Malformed agent frontmatter"
    solution: "Fix YAML syntax in agent file"
  
  "Agent not found":
    cause: "Missing installation or broken symlink"
    solution: "Reinstall profile or repair symlinks"
```

### Debug Logging
```bash
# Enable debug logging
export AGENTGEN_DEBUG=1

# Run operations with verbose output
AGENTGEN_DEBUG=1 ./install-agents --profile core --verbose

# Check system logs
tail -f /var/log/claude-desktop.log  # If available
```

---

*Complete troubleshooting and problem resolution guide for AgentGen Claude Desktop system*