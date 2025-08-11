"""
Utility functions for AgentGen UV wrapper.

Provides common functionality for file operations, validation,
and system integration.
"""

import os
import sys
import json
import hashlib
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import subprocess
import shutil


def validate_agent_name(name: str) -> bool:
    """Validate agent name format."""
    if not name:
        return False
    
    # Agent names should be lowercase with hyphens
    if not name.replace('-', '').replace('_', '').isalnum():
        return False
    
    # Should not start or end with hyphen
    if name.startswith('-') or name.endswith('-'):
        return False
    
    return True


def optimize_for_400_chars(content: str) -> str:
    """Optimize content to fit within 400 character limit."""
    if len(content) <= 400:
        return content
    
    # Extract frontmatter and prompt
    parts = content.split('---\n')
    if len(parts) < 3:
        # No proper frontmatter, just truncate
        return content[:397] + "..."
    
    frontmatter = f"---\n{parts[1]}---\n"
    prompt = '---\n'.join(parts[2:])
    
    # Calculate available space for prompt
    available_chars = 400 - len(frontmatter)
    
    if available_chars <= 50:
        # Not enough space, keep minimal prompt
        return frontmatter + "Execute immediately."
    
    # Optimize prompt
    optimized_prompt = _compress_prompt(prompt, available_chars - 20)  # Reserve some space
    
    return frontmatter + optimized_prompt + "\n\nExecute immediately."


def _compress_prompt(prompt: str, max_chars: int) -> str:
    """Compress prompt text using various techniques."""
    # Common replacements for compression
    replacements = [
        ("You are a ", ""),
        ("You are an ", ""),
        ("specialized in", "for"),
        ("specializing in", "for"),
        ("immediately upon invocation", "immediately"),
        ("When invoked:", ":"),
        ("1. ", ""),
        ("2. ", "→ "),
        ("3. ", "→ "),
        ("4. ", "→ "),
        ("Provide ", ""),
        ("Generate ", ""),
        ("Create ", ""),
        ("comprehensive", "complete"),
        ("detailed", ""),
        ("step by step", "step-by-step"),
        ("workflow:", ":"),
    ]
    
    # Apply replacements
    compressed = prompt
    for old, new in replacements:
        compressed = compressed.replace(old, new)
    
    # Remove extra whitespace
    compressed = ' '.join(compressed.split())
    
    # If still too long, truncate intelligently
    if len(compressed) > max_chars:
        # Try to truncate at sentence boundary
        sentences = compressed.split('. ')
        result = ""
        for sentence in sentences:
            if len(result + sentence + ". ") <= max_chars - 3:  # Reserve space for "..."
                result += sentence + ". "
            else:
                break
        
        if result:
            compressed = result.rstrip() + "..."
        else:
            # No sentence boundary found, just truncate
            compressed = compressed[:max_chars - 3] + "..."
    
    return compressed


def check_dependencies() -> Dict[str, bool]:
    """Check if required dependencies are available."""
    dependencies = {
        'redis': False,
        'requests': False,
        'openai': False,
        'pyttsx3': False,
        'click': False,
        'rich': False
    }
    
    for dep in dependencies:
        try:
            __import__(dep)
            dependencies[dep] = True
        except ImportError:
            pass
    
    return dependencies


def ensure_directory(path: Union[str, Path]) -> Path:
    """Ensure directory exists, create if it doesn't."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def backup_file(file_path: Path) -> Optional[Path]:
    """Create a backup of the file with timestamp."""
    if not file_path.exists():
        return None
    
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_suffix(f"{file_path.suffix}.backup.{timestamp}")
    
    try:
        shutil.copy2(file_path, backup_path)
        return backup_path
    except Exception:
        return None


def get_file_hash(file_path: Path) -> str:
    """Get SHA-256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception:
        return ""


def validate_yaml_frontmatter(content: str) -> bool:
    """Validate YAML frontmatter format."""
    lines = content.split('\n')
    
    if not lines or lines[0].strip() != "---":
        return False
    
    # Find end of frontmatter
    end_idx = -1
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            end_idx = i
            break
    
    if end_idx == -1:
        return False
    
    # Check required fields
    frontmatter_lines = lines[1:end_idx]
    has_name = any(line.strip().startswith('name:') for line in frontmatter_lines)
    has_description = any(line.strip().startswith('description:') for line in frontmatter_lines)
    
    return has_name and has_description


def run_command_with_output(cmd: List[str], cwd: Optional[Path] = None) -> tuple[int, str, str]:
    """Run command and return exit code, stdout, stderr."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def find_project_root() -> Optional[Path]:
    """Find project root by looking for key files."""
    current = Path.cwd()
    
    # Look for project indicators
    indicators = [
        'pyproject.toml',
        'install-agents',
        '.claude',
        'submodules'
    ]
    
    # Search up the directory tree
    for parent in [current] + list(current.parents):
        if any((parent / indicator).exists() for indicator in indicators):
            return parent
    
    return None


def get_agent_complexity(content: str) -> str:
    """Determine agent complexity based on content analysis."""
    # Simple heuristics for complexity classification
    word_count = len(content.split())
    has_multiple_steps = content.count('→') > 1 or content.count('.') > 3
    has_complex_tools = any(tool in content.lower() for tool in [
        'sequential', 'playwright', 'context7', 'magic'
    ])
    
    if word_count < 50 and not has_multiple_steps:
        return "green"  # Simple tasks
    elif word_count > 150 or has_complex_tools:
        return "red"    # Complex reasoning
    else:
        return "yellow" # Standard development


def format_agent_list(agents: Dict[str, List[str]]) -> str:
    """Format agent list for display."""
    output = []
    
    for category, agent_list in agents.items():
        output.append(f"\n{category.upper()}:")
        for agent in sorted(agent_list):
            output.append(f"  • {agent}")
    
    return '\n'.join(output)


def create_temp_script(content: str, suffix: str = '.sh') -> Path:
    """Create a temporary script file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as f:
        f.write(content)
        script_path = Path(f.name)
    
    # Make executable
    script_path.chmod(0o755)
    return script_path


def cleanup_temp_files(files: List[Path]) -> None:
    """Clean up temporary files."""
    for file_path in files:
        try:
            if file_path.exists():
                file_path.unlink()
        except Exception:
            pass


def detect_speak_command() -> bool:
    """Detect if speak command is available."""
    return shutil.which('speak') is not None


def get_git_info(repo_path: Path) -> Dict[str, Any]:
    """Get git repository information."""
    info = {
        'is_repo': False,
        'has_submodules': False,
        'submodules_initialized': False,
        'current_branch': None,
        'has_uncommitted_changes': False
    }
    
    if not (repo_path / '.git').exists():
        return info
    
    info['is_repo'] = True
    
    try:
        # Check for submodules
        gitmodules_path = repo_path / '.gitmodules'
        if gitmodules_path.exists():
            info['has_submodules'] = True
            
            # Check if submodules are initialized
            submodule_dir = repo_path / 'submodules'
            if submodule_dir.exists():
                info['submodules_initialized'] = any(submodule_dir.iterdir())
        
        # Get current branch
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            info['current_branch'] = result.stdout.strip()
        
        # Check for uncommitted changes
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            info['has_uncommitted_changes'] = bool(result.stdout.strip())
    
    except Exception:
        pass
    
    return info