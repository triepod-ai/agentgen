# Install-Agents Bash Completion Setup Guide

## Quick Setup

Run from the agentgen directory:

```bash
cd /home/bryan/agentgen
./setup-completion.sh
```

This will:
1. Enable completion for the current session
2. Add to ~/.bashrc for future sessions  
3. Install system-wide if possible

## 🎯 NEW IMPROVED DEFAULTS

The install-agents command now has improved defaults for better user experience:

- **✅ Symlink mode by default** (was copy mode)
- **✅ Current directory as target** (was explicit path required)
- **✅ Force enabled by default** (was disabled)

## Usage Examples with New Defaults

### Simple Usage (NEW)
```bash
# Install to current directory with symlinks (NEW DEFAULT)
install-agents --profile <TAB>
# Shows: ai-ml-team backend-focus core development-team frontend-focus security-audit simple-tools

install-agents <TAB>
# Shows: agent names for current directory installation

install-agents code<TAB>
# Shows: code-reviewer code-reviewer-pro config-reader
```

### Traditional Usage (Still Supported)
```bash
# Explicit project path
install-agents --project /path/to/project <TAB>
# Shows: directory paths

install-agents /path/to/project <TAB>
# Shows: agent names for explicit path

# Legacy copy mode
install-agents --copy /path/to/project <TAB>
# Shows: agent names for copy installation
```

### Advanced Features
```bash
# Global installation (symlinks only)
install-agents --global <TAB>
# Shows: agent names for global installation

# Maintenance (symlinks only)
install-agents --health     # Health check
install-agents --repair     # Repair broken symlinks

# Profile management
install-agents --show-profile <TAB>
# Shows: available profile names

install-agents --list-profiles    # List all profiles
```

## What Gets Completed

### 1. Options and Flags
All command options including:
- `--help`, `--symlink`, `--copy`, `--global`, `--project`
- `--health`, `--repair`, `--force`, `--all`, `--list`
- `--profile`, `--list-profiles`, `--show-profile`
- `--simple`, `--simple-read`, `--simple-write`, etc.
- `--dry-run`, `--verbose`, `--skip-speak-check`

### 2. Profile Names
Available profiles from `profiles/*.profile`:
- `ai-ml-team` - AI/ML focused agents
- `backend-focus` - Backend development agents
- `core` - Essential core agents
- `development-team` - Full development team setup
- `frontend-focus` - Frontend/UI development agents
- `security-audit` - Security and auditing agents
- `simple-tools` - Basic utility agents

### 3. Agent Names
Available agents from the agents hub (when appropriate):
- Core development: `code-reviewer`, `debugger`, `test-automator`
- Infrastructure: `deployment-engineer`, `performance-engineer`
- Content: `documentation-expert`, `create-lesson`, `update-status`
- Specialists: `python-specialist`, `react-specialist`, `security-auditor`
- And many more...

### 4. Directory Paths
Standard bash directory completion for:
- `--project` paths
- Explicit target paths in copy mode

## Smart Context-Aware Logic

The completion system understands different modes:

### ✅ Shows Agent Names When:
- Simple mode: `install-agents [agent-name]` (NEW DEFAULT)
- After explicit path: `install-agents /path [agent-name]`
- Global mode: `install-agents --global [agent-name]`
- No conflicting flags are used

### ❌ Doesn't Show Agent Names When:
- Using `--all` (all agents selected automatically)
- Using `--profile` (agents come from profile)
- Using `--simple-*` flags (specific agent sets)
- In maintenance modes (`--health`, `--repair`)
- In information modes (`--list`, `--list-profiles`)

## Manual Setup Options

### Current Session Only
```bash
source ./install-agents-completion.bash
```

### Add to User Profile
```bash
echo 'source /home/bryan/agentgen/install-agents-completion.bash' >> ~/.bashrc
```

### System-Wide Installation
```bash
sudo cp install-agents-completion.bash /etc/bash_completion.d/install-agents
```

## Testing Completion

### Basic Test
```bash
./test-completion.sh
```

### Comprehensive Test
```bash
./test-completion-comprehensive.sh
```

### Manual Testing
```bash
# Test basic completion
install-agents <TAB><TAB>

# Test profile completion
install-agents --profile <TAB><TAB>

# Test agent name completion (new default)
install-agents code<TAB><TAB>

# Test directory completion
install-agents --project /home<TAB><TAB>
```

## Troubleshooting

### Completion Not Working
1. Ensure you're in the correct directory: `/home/bryan/agentgen`
2. Source the completion script manually: `source ./install-agents-completion.bash`
3. Check if completion is loaded: `complete -p install-agents`
4. Restart terminal or run: `source ~/.bashrc`

### No Agent Names Showing
1. Verify agents directory exists: `ls agents/`
2. Check agents are found: `find agents -name "*.md" | head -5`
3. Ensure no conflicting flags: avoid `--all`, `--profile` when expecting agent names
4. Test simple mode: `install-agents <TAB>` (should show options or agents)

### Profile Names Not Showing
1. Check profiles directory: `ls profiles/*.profile`
2. Verify after `--profile` flag: `install-agents --profile <TAB>`

## Advanced Configuration

### Custom Profiles
Add new profiles to `profiles/` directory:
```bash
echo "agent1 agent2 agent3" > profiles/my-custom.profile
```

### Custom Agents
Add new agents to `agents/` directory structure.

## Performance Notes

- Completion scans directories dynamically for up-to-date results
- Uses bash built-in caching for performance
- Optimized pattern matching for fast response
- Minimal overhead even with large agent collections

## Related Files

- `install-agents-completion.bash` - Main completion script
- `setup-completion.sh` - Automated setup script
- `test-completion.sh` - Basic test suite
- `test-completion-comprehensive.sh` - Full test suite
- `COMPLETION_README.md` - Detailed completion documentation