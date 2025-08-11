#!/usr/bin/env python3
"""
Demo script showing UV wrapper capabilities for AgentGen
"""

import sys
import subprocess
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.columns import Columns

console = Console()

def run_command(cmd, description):
    """Run a command and display the results."""
    console.print(f"\n🚀 {description}", style="bold blue")
    console.print(f"Command: [cyan]{' '.join(cmd)}[/cyan]")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path(__file__).parent)
        if result.stdout:
            console.print("Output:", style="green")
            console.print(result.stdout)
        if result.stderr:
            console.print("Error:", style="red")
            console.print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        console.print(f"❌ Error: {e}", style="bold red")
        return False

def main():
    """Main demo function."""
    console.print(Panel.fit(
        "🤖 AgentGen UV Wrapper Demo\n\n"
        "This demo shows the enhanced capabilities of the UV-powered\n"
        "AgentGen system with fast dependency management and rich CLI.",
        title="Welcome to AgentGen UV Demo",
        style="bold magenta"
    ))
    
    demos = [
        {
            "cmd": ["uv", "run", "python", "-m", "agentgen.cli", "--version"],
            "desc": "Check AgentGen version"
        },
        {
            "cmd": ["uv", "run", "python", "-m", "agentgen.cli", "status"],
            "desc": "System status check"
        },
        {
            "cmd": ["uv", "run", "python", "-m", "agentgen.cli", "status", "--check-deps"],
            "desc": "Check Python dependencies"
        },
        {
            "cmd": ["./uv-wrapper.py", "profiles"],
            "desc": "List available agent profiles (using standalone wrapper)"
        },
        {
            "cmd": ["uv", "run", "python", "-m", "agentgen.cli", "list"],
            "desc": "List all available agents"
        }
    ]
    
    for demo in demos:
        if not run_command(demo["cmd"], demo["desc"]):
            console.print(f"❌ Demo command failed: {demo['desc']}", style="bold red")
            break
        console.print("─" * 60)
    
    # Show usage examples
    console.print("\n" + "=" * 60)
    console.print("📚 Usage Examples", style="bold green")
    
    examples = [
        "# Setup AgentGen with UV",
        "./uv-wrapper.py setup --dev",
        "",
        "# Install all agents to a project", 
        "agentgen install /path/to/project --all",
        "",
        "# Install specific agents",
        "agentgen install /path/to/project code-reviewer debugger",
        "",
        "# Install from a profile",
        "agentgen install /path/to/project --profile development-team",
        "",
        "# Export agent configurations",
        "agentgen export --output backup.json --format json",
        "",
        "# Run existing scripts with UV environment",
        "agentgen run test-agent-builder",
        "",
        "# Development mode with enhanced tools",
        "agentgen dev --dev --watch"
    ]
    
    syntax = Syntax("\n".join(examples), "bash", theme="monokai", line_numbers=True)
    console.print(syntax)
    
    # Show benefits
    console.print("\n" + "=" * 60)
    console.print("✨ Key Benefits of UV Wrapper", style="bold yellow")
    
    benefits = [
        "⚡ 10-100x faster dependency resolution",
        "🎨 Rich terminal interface with colors", 
        "🔍 Enhanced error handling and validation",
        "📦 Export/import agent configurations",
        "🛠️ Development tools and utilities",
        "🔄 Seamless integration with existing scripts",
        "🧹 Clean, reproducible environments"
    ]
    
    for benefit in benefits:
        console.print(f"  {benefit}")
    
    console.print(Panel.fit(
        "🎉 Demo Complete!\n\n"
        "The UV wrapper provides a modern Python interface to your\n"
        "existing agent system while preserving all functionality.\n\n"
        "Try: agentgen --help",
        title="Demo Summary",
        style="bold green"
    ))

if __name__ == "__main__":
    main()