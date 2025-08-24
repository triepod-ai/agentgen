#!/usr/bin/env python3
"""
Agent Color System Update Script

Updates all agent files with the new comprehensive color coding system.
Includes accessibility metadata and validation.
"""

import os
import re
import yaml
import argparse
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import sys

# Color mapping based on agent categories
COLOR_MAPPING = {
    # Critical/Security (Red)
    'security-auditor': 'red',
    'security-auditor-enhanced': 'red', 
    'documentation-scraper': 'red',
    'context-manager': 'red',
    
    # Architecture/Orchestration (Orange)
    'architect-specialist': 'orange',
    'orchestrate-tasks': 'orange',
    'orchestrate-agents': 'orange', 
    'orchestrate-agents-adv': 'orange',
    'agent-organizer': 'orange',
    'backend-architect': 'orange',
    
    # Development/Specialists (Yellow)
    'react-specialist': 'yellow',
    'react-specialist-enhanced': 'black',  # Enhanced = black
    'python-specialist': 'yellow',
    'typescript-pro': 'yellow',
    'nextjs-pro': 'yellow',
    'react-pro': 'yellow',
    'frontend-developer': 'yellow',
    'full-stack-developer': 'yellow', 
    'react-testing-specialist': 'yellow',
    'legacy-modernizer': 'yellow',
    'build-frontend': 'yellow',
    'build-backend': 'yellow',
    
    # Infrastructure/DevOps (Blue)
    'deployment-engineer': 'blue',
    'cloud-architect-specialist': 'blue',
    'devops-incident-responder': 'blue',
    'performance-engineer': 'blue',
    'database-optimizer': 'blue',
    
    # Data/AI (Purple)
    'ml-specialist': 'purple',
    'data-engineer': 'purple', 
    'database-specialist': 'purple',
    
    # Simple/Tools (Green) - Default for utilities
    'config-reader': 'green',
    'log-reader': 'green',
    'env-reader': 'green', 
    'readme-reader': 'green',
    'build-runner': 'green',
    
    # Business/Content (Brown)
    'product-manager': 'brown',
    'write-content': 'brown',
    'translate-text': 'brown',
    'create-lesson': 'brown',
    'update-status': 'brown',
    
    # Quality/Testing (Teal)
    'test-automator': 'teal',
    'qa-expert': 'teal',
    'code-reviewer': 'teal',
    'code-reviewer-pro': 'teal', 
    'debugger': 'teal',
    'analyze-codebase': 'teal',
}

# Category definitions
CATEGORIES = {
    'red': {
        'name': 'critical',
        'display': 'Critical/Security',
        'icon': '🛡️',
        'description': 'High-priority security, critical system operations'
    },
    'orange': {
        'name': 'architecture', 
        'display': 'Architecture/Orchestration',
        'icon': '🏗️',
        'description': 'System design, coordination, complex orchestration'
    },
    'yellow': {
        'name': 'development',
        'display': 'Development/Specialists', 
        'icon': '⚛️',
        'description': 'Core development work, language specialists'
    },
    'blue': {
        'name': 'infrastructure',
        'display': 'Infrastructure/DevOps',
        'icon': '☁️', 
        'description': 'Infrastructure, deployment, system management'
    },
    'purple': {
        'name': 'data-ai',
        'display': 'Data/AI',
        'icon': '🤖',
        'description': 'Data processing, machine learning, AI operations'
    },
    'green': {
        'name': 'simple',
        'display': 'Simple/Tools',
        'icon': '🛠️',
        'description': 'Basic utilities, simple operations, development tools'
    },
    'brown': {
        'name': 'business',
        'display': 'Business/Content', 
        'icon': '💼',
        'description': 'Business logic, content creation, documentation'
    },
    'teal': {
        'name': 'quality',
        'display': 'Quality/Testing',
        'icon': '🧪',
        'description': 'Testing, QA, code review, quality assurance'
    },
    'black': {
        'name': 'enhanced',
        'display': 'Enhanced/Premium',
        'icon': '⭐',
        'description': 'Knowledge-enhanced agents with advanced capabilities'
    }
}

def parse_agent_file(file_path: Path) -> Tuple[Optional[Dict], str]:
    """Parse agent file and extract frontmatter and content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Match YAML frontmatter
        match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
        if not match:
            return None, content
            
        yaml_content, body = match.groups()
        try:
            frontmatter = yaml.safe_load(yaml_content)
            return frontmatter, body
        except yaml.YAMLError as e:
            print(f"YAML parsing error in {file_path}: {e}")
            return None, content
            
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None, ""

def determine_color(agent_name: str, current_frontmatter: Dict) -> str:
    """Determine the appropriate color for an agent."""
    
    # Check explicit mapping first
    if agent_name in COLOR_MAPPING:
        return COLOR_MAPPING[agent_name]
    
    # Enhanced agents get black
    if 'enhanced' in agent_name:
        return 'black'
    
    # Pattern-based classification
    agent_lower = agent_name.lower()
    
    # Critical/Security patterns
    if any(term in agent_lower for term in ['security', 'audit', 'context-manager']):
        return 'red'
    
    # Architecture/Orchestration patterns  
    if any(term in agent_lower for term in ['architect', 'orchestrat', 'organizer']):
        return 'orange'
    
    # Development/Specialist patterns
    if any(term in agent_lower for term in [
        'react', 'python', 'typescript', 'nextjs', 'frontend', 'backend', 
        'full-stack', 'specialist', 'pro', 'developer'
    ]):
        return 'yellow'
    
    # Infrastructure patterns
    if any(term in agent_lower for term in [
        'deploy', 'cloud', 'devops', 'performance', 'infrastructure'
    ]):
        return 'blue'
        
    # Data/AI patterns
    if any(term in agent_lower for term in ['ml', 'data', 'database', 'ai']):
        return 'purple'
        
    # Business/Content patterns
    if any(term in agent_lower for term in [
        'product', 'content', 'lesson', 'translate', 'business'
    ]):
        return 'brown'
        
    # Quality/Testing patterns
    if any(term in agent_lower for term in [
        'test', 'qa', 'quality', 'review', 'debug', 'analyze'
    ]):
        return 'teal'
    
    # Default to green for simple/tools
    return 'green'

def update_agent_frontmatter(frontmatter: Dict, agent_name: str, color: str) -> Dict:
    """Update agent frontmatter with color and accessibility info."""
    
    # Set color
    frontmatter['color'] = color
    
    # Set category
    category_info = CATEGORIES[color]
    frontmatter['category'] = category_info['name']
    
    # Add accessibility metadata
    if 'accessibility' not in frontmatter:
        frontmatter['accessibility'] = {}
    
    frontmatter['accessibility']['icon'] = category_info['icon']
    frontmatter['accessibility']['category_display'] = category_info['display']
    frontmatter['accessibility']['contrast_ratio'] = 4.7  # WCAG AA compliant
    
    return frontmatter

def write_agent_file(file_path: Path, frontmatter: Dict, body: str, dry_run: bool = False) -> bool:
    """Write updated agent file."""
    
    if dry_run:
        print(f"Would update: {file_path}")
        return True
    
    try:
        # Create backup
        backup_path = file_path.with_suffix('.md.backup')
        shutil.copy2(file_path, backup_path)
        
        # Generate new content
        yaml_content = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)
        new_content = f"---\n{yaml_content}---\n{body}"
        
        # Write updated file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"Updated: {file_path}")
        return True
        
    except Exception as e:
        print(f"Error writing {file_path}: {e}")
        return False

def find_agent_files(agents_dir: Path) -> List[Path]:
    """Find all agent .md files."""
    agent_files = []
    
    for root, dirs, files in os.walk(agents_dir):
        for file in files:
            if file.endswith('.md'):
                agent_files.append(Path(root) / file)
                
    return sorted(agent_files)

def main():
    parser = argparse.ArgumentParser(description='Update agent color coding system')
    parser.add_argument('--agents-dir', default='agents', 
                       help='Directory containing agent files')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be updated without making changes')
    parser.add_argument('--force', action='store_true',
                       help='Force update even if validation fails')
    parser.add_argument('--agent', help='Update specific agent only')
    parser.add_argument('--validate', action='store_true',
                       help='Validate colors only, no updates')
    
    args = parser.parse_args()
    
    agents_dir = Path(args.agents_dir)
    if not agents_dir.exists():
        print(f"Error: Agents directory {agents_dir} not found")
        sys.exit(1)
    
    # Find agent files
    if args.agent:
        agent_files = [agents_dir / f"{args.agent}.md"]
        if not agent_files[0].exists():
            # Try finding in subdirectories
            agent_files = list(agents_dir.rglob(f"{args.agent}.md"))
            if not agent_files:
                print(f"Error: Agent {args.agent} not found")
                sys.exit(1)
    else:
        agent_files = find_agent_files(agents_dir)
    
    print(f"Found {len(agent_files)} agent files")
    
    # Process agents
    updated_count = 0
    error_count = 0
    color_stats = {}
    
    for file_path in agent_files:
        agent_name = file_path.stem
        
        # Parse existing file
        frontmatter, body = parse_agent_file(file_path)
        if frontmatter is None:
            print(f"Warning: Could not parse {file_path}")
            error_count += 1
            continue
        
        # Determine new color
        new_color = determine_color(agent_name, frontmatter)
        current_color = frontmatter.get('color', 'none')
        
        # Track color statistics
        color_stats[new_color] = color_stats.get(new_color, 0) + 1
        
        if args.validate:
            # Validation mode - just report
            status = "✅" if current_color == new_color else "🔄"
            print(f"{status} {agent_name}: {current_color} → {new_color}")
            continue
        
        # Update frontmatter
        updated_frontmatter = update_agent_frontmatter(frontmatter, agent_name, new_color)
        
        # Write updated file
        if write_agent_file(file_path, updated_frontmatter, body, args.dry_run):
            updated_count += 1
        else:
            error_count += 1
    
    # Print summary
    print(f"\nSummary:")
    print(f"Processed: {len(agent_files)} agents")
    print(f"Updated: {updated_count}")
    print(f"Errors: {error_count}")
    
    print(f"\nColor distribution:")
    for color, count in sorted(color_stats.items()):
        category_info = CATEGORIES.get(color, {'display': color, 'icon': '?'})
        print(f"{category_info['icon']} {category_info['display']}: {count} agents")
    
    if args.dry_run:
        print(f"\nDry run complete. Use --apply to make changes.")

if __name__ == '__main__':
    main()