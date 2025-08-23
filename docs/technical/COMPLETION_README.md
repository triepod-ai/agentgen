# install-agents Bash Completion

Bash completion support for the `install-agents` command with intelligent context-aware suggestions.

## Features

### Smart Completion Types

- **Options**: Complete `--help`, `--symlink`, `--profile`, etc.
- **Profile Names**: Complete profile names after `--profile` or `--show-profile`
- **Agent Names**: Complete available agent names when appropriate
- **Directory Paths**: Complete directory paths when target paths are needed

### Context-Aware Logic

The completion system understands different install-agents modes with **NEW IMPROVED DEFAULTS**:

**🎯 NEW DEFAULTS (Improved UX)**:
- **Symlink mode enabled by default** (was copy mode)
- **Current directory as target** (was explicit path required)
- **Force mode enabled** (was disabled)

**Common Usage Patterns**:
- **Simple Install**: `install-agents --profile [name]` (installs to current directory with symlinks)
- **Copy Mode (Legacy)**: `install-agents --copy [target-path] [agent-names...]`
- **Symlink Global**: `install-agents --global --profile [name]`
- **Symlink Project**: `install-agents --project [path] --profile [name]`
- **Maintenance**: `install-agents --health` (no additional args needed)

### Intelligent Agent Name Completion

Agent names are only shown when appropriate:

✅ **Shows agents when:**
- After a target path: `install-agents /path/to/project [TAB]`
- In simple mode: `install-agents [TAB]` (current directory, NEW DEFAULT)
- In global mode: `install-agents --global [TAB]`
- When no `--all`, `--profile`, or `--simple-*` flags are used

❌ **Doesn't show agents when:**
- Using `--all` flag (agents already determined)
- Using `--profile` flag (agents come from profile)
- Using `--simple-*` flags (specific agent sets)
- In maintenance modes (`--health`, `--repair`, etc.)

## Installation

### Automatic Setup
```bash
./setup-completion.sh
```

This will:
1. Load completion for the current session
2. Add to `~/.bashrc` for future sessions
3. Attempt system-wide installation if possible

### Manual Setup

**For current session only:**
```bash
source ./install-agents-completion.bash
```

**For all future sessions:**
```bash
echo "source /path/to/install-agents-completion.bash" >> ~/.bashrc
```

**System-wide (requires sudo):**
```bash
sudo cp install-agents-completion.bash /etc/bash_completion.d/install-agents
```

## Testing

Run the test suite:
```bash
./test-completion.sh                    # Basic tests
./test-completion-comprehensive.sh     # Full test suite
```

## Usage Examples

### 🎯 NEW DEFAULTS - Simplified Usage
```bash
# NEW: Simple installation to current directory (symlinks enabled by default)
install-agents --profile <TAB>
# Shows: ai-ml-team backend-focus development-team frontend-focus security-audit simple-tools

install-agents --profile dev<TAB>
# Shows: development-team

# NEW: Install specific agents to current directory  
install-agents <TAB>
# Shows: code-reviewer deployment-engineer analyze-screenshot debugger test-automator env-reader log-reader readme-reader config-reader full-stack-developer nextjs-pro api-documenter ui-designer

install-agents code<TAB>
# Shows: code-reviewer config-reader
```

### Option Completion
```bash
install-agents --<TAB>
# Shows: --help --symlink --copy --global --project --health --repair --force --all --list --profile --list-profiles --show-profile --simple --simple-read --simple-write --simple-bash --simple-grep --simple-edit --dry-run --verbose --skip-speak-check
```

### Legacy and Advanced Usage
```bash
# Explicit project path (backward compatibility)
install-agents /path/to/project <TAB>
# Shows: code-reviewer deployment-engineer analyze-screenshot debugger test-automator ...

install-agents /path/to/project code<TAB>
# Shows: code-reviewer config-reader

# Directory completion for explicit paths
install-agents --project /ho<TAB>
# Shows: /home

install-agents --copy /usr/lo<TAB>  # Legacy copy mode
# Shows: /usr/local
```

### Advanced Features
```bash
# Global installation (symlinks only)
install-agents --global <TAB>
# Shows agent names (when no --profile specified)

# Maintenance commands (symlinks only)
install-agents --<TAB>
# Shows: --health --repair (among other options)

# Profile information
install-agents --show-profile <TAB>
# Shows: ai-ml-team backend-focus development-team frontend-focus security-audit simple-tools
```

## Technical Details

### Architecture
- **Dynamic agent discovery**: Scans `agents/` directory for available agents
- **Profile detection**: Reads `profiles/*.profile` files
- **Context analysis**: Parses command line to understand completion context
- **Boolean logic**: Uses proper bash string handling for flags

### Performance
- **Efficient scanning**: Only scans directories when needed
- **Caching**: Uses bash completion built-in caching
- **Fast pattern matching**: Optimized regex patterns for option detection

### Compatibility
- **Bash 4.0+**: Uses modern bash features
- **POSIX compliant**: Works on Linux, macOS, WSL
- **Path handling**: Supports paths with spaces and special characters