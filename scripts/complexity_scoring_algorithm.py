#!/usr/bin/env python3
"""
Agent Complexity Scoring Algorithm for Three-Tier Hierarchy
Phase 3.1: Foundation - Systematic agent complexity assessment

Purpose: Calculate precise complexity scores (0.0-1.0) for agent tier classification
Criteria: Based on cmd-agent-select-logic strategic analysis framework
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ComplexityTier(Enum):
    CORE = "core"  # 0.0-0.4: Simple operations, basic workflows
    DEVELOPMENT = "development"  # 0.4-0.7: Standard development tasks  
    SPECIALISTS = "specialists"  # 0.7-1.0: Complex reasoning, enterprise operations

@dataclass
class AgentProfile:
    name: str
    description: str
    file_path: Path
    current_tier: str
    content_length: int
    tool_count: int
    mcp_tools: List[str]
    system_prompt_length: int

class ComplexityScorer:
    """Systematic complexity scoring based on cmd-agent-select-logic criteria"""
    
    def __init__(self, agents_dir: str = "/home/bryan/agentgen/agents"):
        self.agents_dir = Path(agents_dir)
        
        # Complexity indicators from strategic analysis
        self.context_indicators = {
            'minimal': ['read', 'check', 'find', 'extract', 'display', 'show'],
            'moderate': ['create', 'build', 'implement', 'design', 'analyze'],
            'extensive': ['comprehensive', 'enterprise', 'system-wide', 'modernize', 'optimize']
        }
        
        self.workflow_patterns = {
            'single_step': ['read', 'display', 'show', 'extract'],
            'multi_step': ['create and', 'build with', 'implement using', 'design for'],
            'complex_workflow': ['comprehensive', 'end-to-end', 'orchestrate', 'coordinate']
        }
        
        self.domain_expertise = {
            'basic': ['file', 'config', 'environment', 'status'],
            'development': ['frontend', 'backend', 'API', 'component', 'interface'],
            'specialist': ['architecture', 'security', 'performance', 'machine learning', 'enterprise']
        }
        
        self.system_impact = {
            'isolated': ['file', 'config', 'single'],
            'component': ['component', 'module', 'service'],
            'system': ['system', 'architecture', 'enterprise', 'migration']
        }
    
    def load_agent_profile(self, agent_file: Path) -> Optional[AgentProfile]:
        """Load agent metadata and content for complexity analysis"""
        try:
            content = agent_file.read_text(encoding='utf-8')
            
            # Extract YAML frontmatter
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    system_prompt = parts[2].strip()
                else:
                    frontmatter = {}
                    system_prompt = content
            else:
                frontmatter = {}
                system_prompt = content
            
            # Extract tools
            tools = frontmatter.get('tools', '')
            if isinstance(tools, str):
                tool_list = [t.strip() for t in tools.split(',') if t.strip()]
            elif isinstance(tools, list):
                tool_list = tools
            else:
                tool_list = []
            
            # Identify MCP tools
            mcp_tools = [tool for tool in tool_list if tool.startswith('mcp__')]
            
            # Determine current tier from path
            current_tier = agent_file.parent.name
            
            return AgentProfile(
                name=frontmatter.get('name', agent_file.stem),
                description=frontmatter.get('description', ''),
                file_path=agent_file,
                current_tier=current_tier,
                content_length=len(content),
                tool_count=len(tool_list),
                mcp_tools=mcp_tools,
                system_prompt_length=len(system_prompt)
            )
            
        except Exception as e:
            print(f"⚠️  Error loading {agent_file}: {e}")
            return None
    
    def calculate_context_requirements_score(self, profile: AgentProfile) -> float:
        """Score based on context complexity (0.0-0.3)"""
        description = profile.description.lower()
        
        if any(indicator in description for indicator in self.context_indicators['extensive']):
            return 0.3
        elif any(indicator in description for indicator in self.context_indicators['moderate']):
            return 0.2
        elif any(indicator in description for indicator in self.context_indicators['minimal']):
            return 0.1
        else:
            return 0.15  # Default moderate score
    
    def calculate_workflow_complexity_score(self, profile: AgentProfile) -> float:
        """Score based on workflow complexity (0.0-0.3)"""
        description = profile.description.lower()
        content = profile.file_path.read_text().lower()
        
        # Count workflow indicators
        complex_patterns = sum(1 for pattern in self.workflow_patterns['complex_workflow'] 
                             if pattern in description or pattern in content)
        multi_patterns = sum(1 for pattern in self.workflow_patterns['multi_step'] 
                           if pattern in description or pattern in content)
        
        # Check for step-by-step workflows
        step_indicators = content.count('step ') + content.count('##') + content.count('###')
        
        if complex_patterns >= 2 or step_indicators >= 5:
            return 0.3
        elif multi_patterns >= 2 or step_indicators >= 3:
            return 0.2
        elif step_indicators >= 1:
            return 0.1
        else:
            return 0.05
    
    def calculate_domain_expertise_score(self, profile: AgentProfile) -> float:
        """Score based on domain expertise required (0.0-0.2)"""
        description = profile.description.lower()
        content = profile.file_path.read_text().lower()
        
        specialist_count = sum(1 for term in self.domain_expertise['specialist'] 
                             if term in description or term in content)
        development_count = sum(1 for term in self.domain_expertise['development'] 
                              if term in description or term in content)
        
        if specialist_count >= 2:
            return 0.2
        elif specialist_count >= 1:
            return 0.15
        elif development_count >= 2:
            return 0.1
        elif development_count >= 1:
            return 0.05
        else:
            return 0.02
    
    def calculate_system_impact_score(self, profile: AgentProfile) -> float:
        """Score based on cross-system impact (0.0-0.2)"""
        description = profile.description.lower()
        content = profile.file_path.read_text().lower()
        
        system_indicators = sum(1 for term in self.system_impact['system'] 
                              if term in description or term in content)
        component_indicators = sum(1 for term in self.system_impact['component'] 
                                 if term in description or term in content)
        
        # Consider MCP tools as system integration
        mcp_weight = len(profile.mcp_tools) * 0.02
        
        if system_indicators >= 2:
            return min(0.2, 0.15 + mcp_weight)
        elif system_indicators >= 1:
            return min(0.2, 0.1 + mcp_weight)
        elif component_indicators >= 2:
            return min(0.2, 0.08 + mcp_weight)
        elif component_indicators >= 1:
            return min(0.2, 0.05 + mcp_weight)
        else:
            return min(0.2, 0.02 + mcp_weight)
    
    def calculate_complexity_score(self, profile: AgentProfile) -> Tuple[float, Dict[str, float]]:
        """Calculate overall complexity score with component breakdown"""
        
        # Calculate component scores
        context_score = self.calculate_context_requirements_score(profile)
        workflow_score = self.calculate_workflow_complexity_score(profile)
        domain_score = self.calculate_domain_expertise_score(profile)
        system_score = self.calculate_system_impact_score(profile)
        
        # Total complexity score
        total_score = context_score + workflow_score + domain_score + system_score
        
        # Cap at 1.0
        total_score = min(total_score, 1.0)
        
        breakdown = {
            'context_requirements': context_score,
            'workflow_complexity': workflow_score,
            'domain_expertise': domain_score,
            'system_impact': system_score,
            'total': total_score
        }
        
        return total_score, breakdown
    
    def determine_target_tier(self, complexity_score: float) -> ComplexityTier:
        """Determine target tier based on complexity score"""
        if complexity_score < 0.4:
            return ComplexityTier.CORE
        elif complexity_score < 0.7:
            return ComplexityTier.DEVELOPMENT
        else:
            return ComplexityTier.SPECIALISTS
    
    def analyze_all_agents(self) -> Dict[str, Dict]:
        """Analyze complexity scores for all agents"""
        results = {}
        
        # Scan all tiers
        for tier_dir in self.agents_dir.iterdir():
            if tier_dir.is_dir():
                for agent_file in tier_dir.glob("*.md"):
                    profile = self.load_agent_profile(agent_file)
                    if profile:
                        score, breakdown = self.calculate_complexity_score(profile)
                        target_tier = self.determine_target_tier(score)
                        
                        results[profile.name] = {
                            'current_tier': profile.current_tier,
                            'target_tier': target_tier.value,
                            'complexity_score': score,
                            'score_breakdown': breakdown,
                            'migration_needed': profile.current_tier != target_tier.value,
                            'file_path': str(profile.file_path),
                            'description': profile.description,
                            'tool_count': profile.tool_count,
                            'mcp_tools': profile.mcp_tools,
                            'content_length': profile.content_length
                        }
        
        return results
    
    def generate_migration_plan(self, analysis_results: Dict[str, Dict]) -> Dict[str, List[str]]:
        """Generate migration plan based on complexity analysis"""
        migrations = {
            'to_core': [],
            'to_development': [],
            'to_specialists': [],
            'no_change': []
        }
        
        for agent_name, data in analysis_results.items():
            if data['migration_needed']:
                target = data['target_tier']
                if target == 'core':
                    migrations['to_core'].append(agent_name)
                elif target == 'development':
                    migrations['to_development'].append(agent_name)
                elif target == 'specialists':
                    migrations['to_specialists'].append(agent_name)
            else:
                migrations['no_change'].append(agent_name)
        
        return migrations

def main():
    """Main execution function"""
    scorer = ComplexityScorer()
    
    print("🧮 Analyzing Agent Complexity Scores...")
    print("=" * 60)
    
    results = scorer.analyze_all_agents()
    migration_plan = scorer.generate_migration_plan(results)
    
    # Statistics
    total_agents = len(results)
    migrations_needed = sum(1 for data in results.values() if data['migration_needed'])
    
    print(f"📊 Analysis Complete:")
    print(f"   Total Agents: {total_agents}")
    print(f"   Migrations Needed: {migrations_needed}")
    print(f"   Migration Rate: {migrations_needed/total_agents*100:.1f}%")
    print()
    
    print("🎯 Migration Plan:")
    for tier, agents in migration_plan.items():
        if agents:
            print(f"   {tier.replace('_', ' ').title()}: {len(agents)} agents")
            for agent in sorted(agents)[:5]:  # Show first 5
                score = results[agent]['complexity_score']
                print(f"     - {agent} (score: {score:.2f})")
            if len(agents) > 5:
                print(f"     ... and {len(agents)-5} more")
            print()
    
    # Save results
    output_dir = Path("tests/results")
    output_dir.mkdir(exist_ok=True)
    
    import json
    with open(output_dir / "complexity_analysis.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    with open(output_dir / "migration_plan.json", "w") as f:
        json.dump(migration_plan, f, indent=2)
    
    print(f"💾 Results saved to {output_dir}/")
    
    return results, migration_plan

if __name__ == "__main__":
    results, plan = main()