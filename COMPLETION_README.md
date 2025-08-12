# install-agents Bash Completion

Bash completion support for the `install-agents` command with intelligent context-aware suggestions.

## Features

### Smart Completion Types

- **Options**: Complete `--help`, `--symlink`, `--profile`, etc.
- **Profile Names**: Complete profile names after `--profile` or `--show-profile`
- **Agent Names**: Complete available agent names when appropriate
- **Directory Paths**: Complete directory paths when target paths are needed

### Context-Aware Logic

The completion system understands different install-agents modes:

- **Copy Mode**: `install-agents [target-path] [agent-names...]`
- **Symlink Global**: `install-agents --symlink --global --profile [name]`
- **Symlink Project**: `install-agents --symlink --project [path] --profile [name]`
- **Maintenance**: `install-agents --symlink --health` (no additional args needed)

### Intelligent Agent Name Completion

Agent names are only shown when appropriate:

✅ **Shows agents when:**
- After a target path: `install-agents /path/to/project [TAB]`
- In global symlink mode: `install-agents --symlink --global [TAB]`
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

### Option Completion
```bash
install-agents --<TAB>
# Shows: --help --symlink --copy --global --project --health --repair --force --all --list --profile --list-profiles --show-profile --simple --simple-read --simple-write --simple-bash --simple-grep --simple-edit --dry-run --verbose --skip-speak-check
```

### Profile Completion
```bash
install-agents --profile <TAB>
# Shows: ai-ml-team backend-focus development-team frontend-focus security-audit simple-tools

install-agents --profile dev<TAB>
# Shows: development-team
```

### Agent Name Completion
```bash
install-agents /path/to/project <TAB>
# Shows: code-reviewer-pro deployment-engineer analyze-screenshot debugger test-agent env-reader log-reader readme-reader config-reader full-stack-developer code-reviewer nextjs-pro api-documenter backend-architect ui-designer

install-agents /path/to/project code<TAB>
# Shows: code-reviewer-pro code-reviewer
```

### Directory Completion
```bash
install-agents --symlink --project /ho<TAB>
# Shows: /home

install-agents /usr/lo<TAB>
# Shows: /usr/local
```

### Symlink Mode Examples
```bash
install-agents --symlink --<TAB>
# Shows: --help --symlink --copy --global --project --health --repair --force --all --list --profile --list-profiles --show-profile --simple --simple-read --simple-write --simple-bash --simple-grep --simple-edit --dry-run --verbose --skip-speak-check

install-agents --symlink --global <TAB>
# Shows agent names (when no --profile specified)

install-agents --symlink --project <TAB>
# Shows directory paths
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