#!/usr/bin/env python3
"""
UV Wrapper for AgentGen - Standalone launcher script

This is a standalone script that can be used to run AgentGen with UV
without requiring the full package to be installed.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def main():
    """Main entry point for the UV wrapper."""
    # Get the directory containing this script
    script_dir = Path(__file__).parent.absolute()
    
    # Check if UV is available
    uv_path = shutil.which("uv")
    if not uv_path:
        print("❌ UV not found. Please install UV: https://docs.astral.sh/uv/")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        sys.exit(1)
    
    # Check if we're in the right directory
    if not (script_dir / "pyproject.toml").exists():
        print("❌ pyproject.toml not found. Make sure you're in the AgentGen directory.")
        sys.exit(1)
    
    # Get command line arguments
    args = sys.argv[1:] if len(sys.argv) > 1 else ["--help"]
    
    # Map common commands
    command_map = {
        "setup": ["run", "python", "-m", "agentgen.cli", "setup"],
        "install": ["run", "python", "-m", "agentgen.cli", "install"],
        "list": ["run", "python", "-m", "agentgen.cli", "list"],
        "status": ["run", "python", "-m", "agentgen.cli", "status"],
        "dev": ["run", "python", "-m", "agentgen.cli", "dev"],
        "export": ["run", "python", "-m", "agentgen.cli", "export"],
        "profiles": ["run", "python", "-m", "agentgen.cli", "profiles"],
        "run": ["run", "python", "-m", "agentgen.cli", "run"],
        "show-profile": ["run", "python", "-m", "agentgen.cli", "show-profile"]
    }
    
    # Handle direct script execution
    if args and args[0] in ["install-agents", "test-agent-builder.sh"]:
        script_path = script_dir / args[0]
        if script_path.exists():
            # Run the script directly
            cmd = [str(script_path)] + args[1:]
            os.execv(str(script_path), cmd)
        else:
            print(f"❌ Script not found: {args[0]}")
            sys.exit(1)
    
    # Build UV command
    if args and args[0] in command_map:
        uv_args = command_map[args[0]] + args[1:]
    else:
        # Default to running the CLI
        uv_args = ["run", "python", "-m", "agentgen.cli"] + args
    
    # Execute with UV
    try:
        os.chdir(script_dir)
        os.execv(uv_path, [uv_path] + uv_args)
    except Exception as e:
        print(f"❌ Failed to execute command: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()