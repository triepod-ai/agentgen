#!/usr/bin/env python3
"""
AgentGen CLI - UV-powered wrapper for the AI agent generation system.

Provides a modern Python interface to the existing shell-based agent system
with enhanced dependency management, performance optimization, and developer experience.
"""

import os
import sys
import subprocess
import json
import shutil
import re
from pathlib import Path
from typing import List, Optional, Dict, Any
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

console = Console()

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
INSTALL_AGENTS_SCRIPT = PROJECT_ROOT / "install-agents"


class AgentGenError(Exception):
    """Base exception for AgentGen operations."""
    pass


def convert_ansi_to_rich(text: str) -> str:
    """Convert ANSI color codes to Rich markup."""
    # More comprehensive ANSI color code mappings to Rich styles
    ansi_to_rich = {
        # Basic colors
        '\033[0;31m': '[red]',      # Red
        '\033[0;32m': '[green]',    # Green  
        '\033[1;33m': '[bold yellow]', # Yellow (bright)
        '\033[0;33m': '[yellow]',   # Yellow
        '\033[0;34m': '[blue]',     # Blue
        '\033[1;34m': '[bold blue]', # Blue (bright)
        '\033[0;35m': '[magenta]',  # Magenta
        '\033[0;36m': '[cyan]',     # Cyan
        '\033[0;37m': '[white]',    # White
        '\033[1;37m': '[bold white]', # White (bright)
        
        # Reset codes
        '\033[0m': '[/]',           # Reset
        '\033[m': '[/]',            # Reset (alternate)
    }
    
    # Replace ANSI codes with Rich markup
    for ansi_code, rich_style in ansi_to_rich.items():
        text = text.replace(ansi_code, rich_style)
    
    # Remove any remaining ANSI escape sequences using regex
    text = re.sub(r'\033\[[0-9;]*m', '', text)
    
    return text


def run_with_color_support(cmd, convert_to_rich=False, **kwargs):
    """Run subprocess with proper color/TTY support."""
    # Ensure TERM is set for color support
    env = os.environ.copy()
    if 'TERM' not in env:
        env['TERM'] = 'xterm-256color'
    
    # Force color output for known color-supporting commands
    env['FORCE_COLOR'] = '1'
    env['CLICOLOR_FORCE'] = '1'
    
    # Merge any provided env with our color-supporting env
    if 'env' in kwargs:
        env.update(kwargs['env'])
    kwargs['env'] = env
    
    if convert_to_rich:
        # Capture output to convert ANSI to Rich
        kwargs['capture_output'] = True
        kwargs['text'] = True
        result = subprocess.run(cmd, **kwargs)
        
        if result.stdout:
            # Convert ANSI codes to Rich markup and print
            rich_output = convert_ansi_to_rich(result.stdout)
            # Create a new console instance to avoid style conflicts
            rich_console = Console()
            rich_console.print(rich_output, markup=True, highlight=False)
        
        if result.stderr:
            rich_error = convert_ansi_to_rich(result.stderr)
            rich_console = Console()
            rich_console.print(rich_error, markup=True, highlight=False, file=sys.stderr)
            
        return result
    else:
        # For color support, we need to inherit the terminal properly
        # Don't capture output unless explicitly requested
        if 'capture_output' not in kwargs:
            kwargs['stdout'] = None
            kwargs['stderr'] = None
            kwargs['text'] = True
        
        return subprocess.run(cmd, **kwargs)


class UVWrapper:
    """UV wrapper for enhanced Python dependency management."""
    
    def __init__(self):
        self.uv_path = shutil.which("uv")
        if not self.uv_path:
            raise AgentGenError("UV not found. Please install UV: https://docs.astral.sh/uv/")
    
    def run_with_uv(self, script_path: Path, args: List[str] = None) -> subprocess.CompletedProcess:
        """Run a script with UV environment management."""
        args = args or []
        
        # Use uv run for Python scripts, direct execution for shell scripts
        if script_path.suffix == ".py":
            cmd = [self.uv_path, "run", str(script_path)] + args
        else:
            # For shell scripts, ensure Python dependencies are available
            cmd = [str(script_path)] + args
        
        return run_with_color_support(cmd, capture_output=False, text=True)
    
    def install_dependencies(self, dev: bool = False) -> None:
        """Install project dependencies with UV."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Installing dependencies...", total=None)
            
            cmd = [self.uv_path, "sync"]
            if dev:
                cmd.append("--dev")
            
            result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise AgentGenError(f"Dependency installation failed: {result.stderr}")
            
            progress.update(task, description="✅ Dependencies installed!")


@click.group()
@click.version_option(version="0.2.0")
@click.pass_context
def main(ctx):
    """🤖 AgentGen - AI Agent Generation System with UV Integration
    
    A modern Python wrapper for the AI agent generation system providing
    enhanced dependency management, performance optimization, and developer experience.
    """
    ctx.ensure_object(dict)
    ctx.obj['uv'] = UVWrapper()


@main.command()
@click.option('--dev', is_flag=True, help='Install development dependencies')
def setup(dev):
    """🔧 Setup the AgentGen environment with UV."""
    try:
        uv = UVWrapper()
        console.print("🚀 Setting up AgentGen environment...", style="bold blue")
        
        # Install dependencies
        uv.install_dependencies(dev=dev)
        
        # Initialize git submodules if needed
        submodule_dir = PROJECT_ROOT / "submodules" / "claude-code-sub-agents"
        if not submodule_dir.exists():
            console.print("📦 Initializing git submodules...", style="yellow")
            subprocess.run(
                ["git", "submodule", "update", "--init", "--recursive"],
                cwd=PROJECT_ROOT,
                check=True
            )
        
        console.print("✅ AgentGen setup complete!", style="bold green")
        console.print("\n💡 Next steps:")
        console.print("  • Run 'agentgen install --help' to see installation options")
        console.print("  • Run 'agentgen list' to see available agents")
        console.print("  • Run 'agentgen profiles' to see available profiles")
        
    except Exception as e:
        console.print(f"❌ Setup failed: {e}", style="bold red")
        sys.exit(1)


@main.command()
@click.argument('target', required=False)
@click.argument('agents', nargs=-1)
@click.option('--all', 'install_all', is_flag=True, help='Install all available agents')
@click.option('--profile', help='Install agents from a profile')
@click.option('--force', is_flag=True, help='Force installation, overwrite existing agents')
@click.option('--dry-run', is_flag=True, help='Show what would be installed without making changes')
@click.option('--verbose', is_flag=True, help='Show detailed installation progress')
@click.option('--simple', is_flag=True, help='Install all simple single-tool agents')
@click.option('--simple-read', is_flag=True, help='Install Read-based agents')
@click.option('--simple-write', is_flag=True, help='Install Write-based agents')
@click.option('--simple-bash', is_flag=True, help='Install Bash-based agents')
@click.option('--simple-grep', is_flag=True, help='Install Grep-based agents')
@click.option('--simple-edit', is_flag=True, help='Install Edit-based agents')
@click.option('--skip-speak-check', is_flag=True, help='Skip speak command validation')
def install(target, agents, install_all, profile, force, dry_run, verbose, simple, 
           simple_read, simple_write, simple_bash, simple_grep, simple_edit, skip_speak_check):
    """🚀 Install AI agents to a target project.
    
    TARGET: Path to the project where agents will be installed
    AGENTS: Specific agent names to install
    """
    if not target:
        console.print("❌ Target project path is required", style="bold red")
        console.print("Example: agentgen install /path/to/project --all")
        sys.exit(1)
    
    # Build command arguments
    args = [str(target)]
    if agents:
        args.extend(agents)
    
    # Build flags
    flags = []
    if install_all:
        flags.append('--all')
    if profile:
        flags.extend(['--profile', profile])
    if force:
        flags.append('--force')
    if dry_run:
        flags.append('--dry-run')
    if verbose:
        flags.append('--verbose')
    if simple:
        flags.append('--simple')
    if simple_read:
        flags.append('--simple-read')
    if simple_write:
        flags.append('--simple-write')
    if simple_bash:
        flags.append('--simple-bash')
    if simple_grep:
        flags.append('--simple-grep')
    if simple_edit:
        flags.append('--simple-edit')
    if skip_speak_check:
        flags.append('--skip-speak-check')
    
    try:
        console.print(f"🤖 Installing agents to: {target}", style="bold blue")
        
        # Run the install-agents script
        cmd = [str(INSTALL_AGENTS_SCRIPT)] + flags + args
        result = run_with_color_support(cmd, cwd=PROJECT_ROOT)
        
        if result.returncode == 0:
            console.print("✅ Agent installation completed!", style="bold green")
        else:
            console.print("❌ Agent installation failed", style="bold red")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"❌ Installation error: {e}", style="bold red")
        sys.exit(1)


@main.command()
def list():
    """📋 List all available agents and profiles."""
    try:
        console.print("🤖 Available Agents:", style="bold blue")
        run_with_color_support([str(INSTALL_AGENTS_SCRIPT), "--list"], convert_to_rich=True)
    except Exception as e:
        console.print(f"❌ Failed to list agents: {e}", style="bold red")
        sys.exit(1)


@main.command()
def profiles():
    """📂 List all available agent profiles."""
    try:
        console.print("📂 Available Profiles:", style="bold blue")
        run_with_color_support([str(INSTALL_AGENTS_SCRIPT), "--list-profiles"], convert_to_rich=True)
    except Exception as e:
        console.print(f"❌ Failed to list profiles: {e}", style="bold red")
        sys.exit(1)


@main.command()
@click.argument('profile_name')
def show_profile(profile_name):
    """🔍 Show details of a specific agent profile."""
    try:
        console.print(f"🔍 Profile Details: {profile_name}", style="bold blue")
        run_with_color_support([str(INSTALL_AGENTS_SCRIPT), "--show-profile", profile_name], convert_to_rich=True)
    except Exception as e:
        console.print(f"❌ Failed to show profile: {e}", style="bold red")
        sys.exit(1)


@main.command()
@click.option('--check-deps', is_flag=True, help='Check Python dependencies status')
@click.option('--check-git', is_flag=True, help='Check git submodules status')
@click.option('--check-speak', is_flag=True, help='Check speak command availability')
def status(check_deps, check_git, check_speak):
    """🔍 Show system status and health checks."""
    console.print("🔍 AgentGen System Status", style="bold blue")
    
    # Create status table
    table = Table(title="System Components")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="magenta")
    table.add_column("Details", style="green")
    
    # Check UV
    uv_status = "✅ Available" if shutil.which("uv") else "❌ Not Found"
    uv_version = subprocess.run(["uv", "--version"], capture_output=True, text=True).stdout.strip() if shutil.which("uv") else "N/A"
    table.add_row("UV Package Manager", uv_status, uv_version)
    
    # Check install-agents script
    script_status = "✅ Available" if INSTALL_AGENTS_SCRIPT.exists() else "❌ Not Found"
    table.add_row("Install Agents Script", script_status, str(INSTALL_AGENTS_SCRIPT))
    
    # Check git submodules
    if check_git:
        submodule_dir = PROJECT_ROOT / "submodules" / "claude-code-sub-agents"
        git_status = "✅ Initialized" if submodule_dir.exists() else "❌ Not Initialized"
        table.add_row("Git Submodules", git_status, str(submodule_dir))
    
    # Check speak command
    if check_speak:
        speak_status = "✅ Available" if shutil.which("speak") else "❌ Not Found"
        table.add_row("Speak Command", speak_status, "TTS notifications")
    
    # Check Python dependencies
    if check_deps:
        try:
            import redis, requests, openai, pyttsx3
            deps_status = "✅ Installed"
        except ImportError as e:
            deps_status = f"❌ Missing: {e.name}"
        table.add_row("Python Dependencies", deps_status, "Redis, OpenAI, etc.")
    
    console.print(table)


@main.command()
@click.argument('script_name')
@click.argument('script_args', nargs=-1)
def run(script_name, script_args):
    """🚀 Run project scripts with UV environment management.
    
    SCRIPT_NAME: Name of the script to run
    SCRIPT_ARGS: Arguments to pass to the script
    """
    try:
        uv = UVWrapper()
        
        # Find the script
        script_paths = [
            PROJECT_ROOT / f"{script_name}",
            PROJECT_ROOT / f"{script_name}.sh",
            PROJECT_ROOT / f"{script_name}.py",
            PROJECT_ROOT / "scripts" / f"{script_name}",
            PROJECT_ROOT / "scripts" / f"{script_name}.sh",
            PROJECT_ROOT / "scripts" / f"{script_name}.py"
        ]
        
        script_path = None
        for path in script_paths:
            if path.exists():
                script_path = path
                break
        
        if not script_path:
            console.print(f"❌ Script not found: {script_name}", style="bold red")
            console.print("Available scripts:", style="yellow")
            for script_dir in [PROJECT_ROOT, PROJECT_ROOT / "scripts"]:
                if script_dir.exists():
                    for script in script_dir.glob("*.sh"):
                        console.print(f"  • {script.stem}")
            sys.exit(1)
        
        console.print(f"🚀 Running: {script_path.name}", style="bold blue")
        result = uv.run_with_uv(script_path, list(script_args))
        
        if result.returncode != 0:
            console.print(f"❌ Script failed with exit code: {result.returncode}", style="bold red")
            sys.exit(result.returncode)
        
    except Exception as e:
        console.print(f"❌ Script execution error: {e}", style="bold red")
        sys.exit(1)


@main.command()
@click.option('--output', '-o', type=click.Path(), help='Output directory for exported agents')
@click.option('--format', 'export_format', type=click.Choice(['json', 'yaml', 'markdown']), 
              default='json', help='Export format')
def export(output, export_format):
    """📤 Export agent configurations for backup or sharing."""
    try:
        agents_dir = PROJECT_ROOT / ".claude" / "agents"
        if not agents_dir.exists():
            console.print("❌ No agents directory found", style="bold red")
            sys.exit(1)
        
        output_path = Path(output) if output else PROJECT_ROOT / f"agents_export.{export_format}"
        
        console.print(f"📤 Exporting agents to: {output_path}", style="bold blue")
        
        agents_data = {}
        for agent_file in agents_dir.glob("*.md"):
            with open(agent_file, 'r') as f:
                content = f.read()
                agents_data[agent_file.stem] = content
        
        if export_format == 'json':
            import json
            with open(output_path, 'w') as f:
                json.dump(agents_data, f, indent=2)
        elif export_format == 'yaml':
            import yaml
            with open(output_path, 'w') as f:
                yaml.dump(agents_data, f, default_flow_style=False)
        elif export_format == 'markdown':
            with open(output_path, 'w') as f:
                for name, content in agents_data.items():
                    f.write(f"# Agent: {name}\n\n{content}\n\n---\n\n")
        
        console.print(f"✅ Exported {len(agents_data)} agents!", style="bold green")
        
    except Exception as e:
        console.print(f"❌ Export failed: {e}", style="bold red")
        sys.exit(1)


@main.command()
@click.option('--dev', is_flag=True, help='Run development server mode')
@click.option('--watch', is_flag=True, help='Watch for file changes')
def dev(dev, watch):
    """🔧 Development tools and utilities."""
    console.print("🔧 AgentGen Development Mode", style="bold blue")
    
    if dev:
        try:
            # Install dev dependencies
            uv = UVWrapper()
            uv.install_dependencies(dev=True)
            
            console.print("✅ Development environment ready!", style="bold green")
            console.print("Available commands:")
            console.print("  • agentgen run test-agent-builder")
            console.print("  • agentgen status --check-deps --check-git")
            
        except Exception as e:
            console.print(f"❌ Development setup failed: {e}", style="bold red")
            sys.exit(1)
    
    if watch:
        console.print("👀 File watching not implemented yet", style="yellow")


if __name__ == "__main__":
    main()