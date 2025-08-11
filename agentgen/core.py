"""
Core AgentGen functionality with UV integration.

This module provides the core classes and utilities for the AgentGen system,
including UV-powered dependency management and enhanced agent operations.
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass
import tempfile

try:
    from pydantic import BaseModel, Field
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    BaseModel = object
    Field = lambda *args, **kwargs: None


@dataclass
class AgentConfig:
    """Agent configuration data structure."""
    name: str
    description: str
    tools: List[str]
    color: Optional[str] = None
    category: Optional[str] = None
    complexity: str = "yellow"  # green, yellow, red
    prompt: str = ""


class AgentManager:
    """Enhanced agent management with UV integration."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.agents_dir = project_root / ".claude" / "agents"
        self.submodule_dir = project_root / "submodules" / "claude-code-sub-agents"
        self.profiles_dir = project_root / "profiles"
        self.uv_available = shutil.which("uv") is not None
    
    def ensure_uv_environment(self) -> bool:
        """Ensure UV environment is properly set up."""
        if not self.uv_available:
            return False
        
        # Check if pyproject.toml exists
        pyproject_path = self.project_root / "pyproject.toml"
        if not pyproject_path.exists():
            return False
        
        # Check if .venv exists, create if needed
        venv_path = self.project_root / ".venv"
        if not venv_path.exists():
            try:
                subprocess.run(
                    ["uv", "venv"],
                    cwd=self.project_root,
                    check=True,
                    capture_output=True
                )
            except subprocess.CalledProcessError:
                return False
        
        return True
    
    def create_agent(self, config: AgentConfig) -> bool:
        """Create a new agent with the given configuration."""
        try:
            agent_file = self.agents_dir / f"{config.name}.md"
            
            # Ensure agents directory exists
            self.agents_dir.mkdir(parents=True, exist_ok=True)
            
            # Create agent content
            frontmatter = [
                "---",
                f"name: {config.name}",
                f"description: {config.description}",
            ]
            
            if config.tools:
                tools_str = ", ".join(config.tools)
                frontmatter.append(f"tools: {tools_str}")
            
            if config.color:
                frontmatter.append(f"color: {config.color}")
            
            frontmatter.append("---")
            
            content = "\n".join(frontmatter) + "\n\n" + config.prompt
            
            # Optimize for <400 characters if needed
            if len(content) > 400:
                content = self._optimize_agent_content(content)
            
            with open(agent_file, 'w') as f:
                f.write(content)
            
            return True
            
        except Exception:
            return False
    
    def _optimize_agent_content(self, content: str) -> str:
        """Optimize agent content to fit within 400 character limit."""
        lines = content.split('\n')
        
        # Find the prompt section (after ---)
        prompt_start = -1
        for i, line in enumerate(lines):
            if line.strip() == "---" and prompt_start == -1:
                continue
            elif line.strip() == "---" and prompt_start == -1:
                prompt_start = i + 1
                break
        
        if prompt_start == -1:
            return content
        
        # Get frontmatter and prompt separately
        frontmatter = '\n'.join(lines[:prompt_start])
        prompt = '\n'.join(lines[prompt_start:])
        
        # Optimize prompt with compression techniques
        optimizations = [
            # Replace common phrases
            ("immediately upon invocation", "immediately"),
            ("Execute workflow immediately", "Execute immediately"),
            ("You are a ", ""),
            ("specialist specializing in", "specialist for"),
            ("when invoked:", ":"),
            ("step by step", "step-by-step"),
            ("Provide ", ""),
            ("comprehensive ", ""),
            ("detailed ", ""),
        ]
        
        for old, new in optimizations:
            prompt = prompt.replace(old, new)
        
        # Use arrow notation for workflows
        prompt = prompt.replace("1. ", "").replace("2. ", "→ ").replace("3. ", "→ ")
        
        # Combine and check length
        optimized = frontmatter + prompt
        
        # If still too long, truncate prompt but keep essential structure
        if len(optimized) > 400:
            available_chars = 400 - len(frontmatter) - 20  # Reserve some space
            if available_chars > 0:
                prompt = prompt[:available_chars] + "...\n\nExecute immediately."
                optimized = frontmatter + prompt
        
        return optimized
    
    def list_agents(self) -> Dict[str, List[str]]:
        """List all available agents by category."""
        agents = {}
        
        # List from submodule
        if self.submodule_dir.exists():
            for category_dir in self.submodule_dir.iterdir():
                if category_dir.is_dir() and not category_dir.name.startswith('.'):
                    category_agents = []
                    for agent_file in category_dir.glob("*.md"):
                        if agent_file.name not in ["README.md", "CLAUDE.md"]:
                            category_agents.append(agent_file.stem)
                    if category_agents:
                        agents[category_dir.name] = category_agents
        
        # Add root level agents
        if self.submodule_dir.exists():
            root_agents = []
            for agent_file in self.submodule_dir.glob("*.md"):
                if agent_file.name not in ["README.md", "CLAUDE.md"]:
                    root_agents.append(agent_file.stem)
            if root_agents:
                agents["general"] = root_agents
        
        return agents
    
    def get_agent_config(self, agent_name: str) -> Optional[AgentConfig]:
        """Get configuration for a specific agent."""
        # Try to find agent file
        agent_file = self._find_agent_file(agent_name)
        if not agent_file or not agent_file.exists():
            return None
        
        try:
            with open(agent_file, 'r') as f:
                content = f.read()
            
            # Parse frontmatter
            lines = content.split('\n')
            if not lines[0].strip() == "---":
                return None
            
            # Find end of frontmatter
            frontmatter_end = -1
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == "---":
                    frontmatter_end = i
                    break
            
            if frontmatter_end == -1:
                return None
            
            # Parse frontmatter
            config_data = {}
            for line in lines[1:frontmatter_end]:
                if ':' in line:
                    key, value = line.split(':', 1)
                    config_data[key.strip()] = value.strip()
            
            # Get prompt
            prompt = '\n'.join(lines[frontmatter_end + 1:])
            
            # Create config
            return AgentConfig(
                name=config_data.get('name', agent_name),
                description=config_data.get('description', ''),
                tools=config_data.get('tools', '').split(', ') if config_data.get('tools') else [],
                color=config_data.get('color'),
                prompt=prompt.strip()
            )
            
        except Exception:
            return None
    
    def _find_agent_file(self, agent_name: str) -> Optional[Path]:
        """Find agent file in various locations."""
        search_paths = [
            self.agents_dir / f"{agent_name}.md",
            self.submodule_dir / f"{agent_name}.md",
        ]
        
        # Search in category directories
        if self.submodule_dir.exists():
            for category_dir in self.submodule_dir.iterdir():
                if category_dir.is_dir():
                    search_paths.append(category_dir / f"{agent_name}.md")
        
        for path in search_paths:
            if path.exists():
                return path
        
        return None
    
    def run_with_uv(self, command: List[str], **kwargs) -> subprocess.CompletedProcess:
        """Run a command with UV environment if available."""
        if self.uv_available and self.ensure_uv_environment():
            # Prepend with uv run for Python commands
            if command and command[0].endswith('.py'):
                command = ['uv', 'run'] + command
        
        return subprocess.run(command, cwd=self.project_root, **kwargs)


class ProfileManager:
    """Manage agent profiles and collections."""
    
    def __init__(self, profiles_dir: Path):
        self.profiles_dir = profiles_dir
    
    def list_profiles(self) -> List[Dict[str, str]]:
        """List all available profiles."""
        profiles = []
        
        if not self.profiles_dir.exists():
            return profiles
        
        for profile_file in self.profiles_dir.glob("*.profile"):
            profile_info = self._parse_profile(profile_file)
            if profile_info:
                profiles.append(profile_info)
        
        return profiles
    
    def _parse_profile(self, profile_file: Path) -> Optional[Dict[str, str]]:
        """Parse a profile file and extract metadata."""
        try:
            with open(profile_file, 'r') as f:
                content = f.read()
            
            lines = content.strip().split('\n')
            profile_data = {
                'name': profile_file.stem,
                'description': 'No description',
                'agents': []
            }
            
            for line in lines:
                line = line.strip()
                if line.startswith('description:'):
                    profile_data['description'] = line.replace('description:', '').strip()
                elif line.startswith('- '):
                    agent_name = line.replace('- ', '').strip()
                    profile_data['agents'].append(agent_name)
                elif line and not line.startswith('#') and not line.startswith('name:') and not line.startswith('agents:'):
                    # Simple list format
                    profile_data['agents'].append(line)
            
            return profile_data
            
        except Exception:
            return None


def get_system_info() -> Dict[str, Any]:
    """Get system information for diagnostics."""
    return {
        'uv_available': shutil.which('uv') is not None,
        'uv_version': _get_uv_version(),
        'python_version': sys.version,
        'platform': sys.platform,
        'pydantic_available': PYDANTIC_AVAILABLE
    }


def _get_uv_version() -> Optional[str]:
    """Get UV version if available."""
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None