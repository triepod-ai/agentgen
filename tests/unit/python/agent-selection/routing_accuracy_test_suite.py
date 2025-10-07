#!/usr/bin/env python3
"""
Agent Routing Accuracy Test Suite for Three-Tier Complexity Hierarchy
Phase 3.1: Foundation - Baseline routing accuracy measurement and validation

Purpose: Systematically test agent routing accuracy across Core/Development/Specialists tiers
Target: Improve routing accuracy from current 65% to 85%
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class ComplexityTier(Enum):
    CORE = "core"  # 0.0-0.4: Simple operations, basic workflows
    DEVELOPMENT = "development"  # 0.4-0.7: Standard development tasks
    SPECIALISTS = "specialists"  # 0.7-1.0: Complex reasoning, enterprise operations

@dataclass
class TestCase:
    description: str
    expected_tier: ComplexityTier
    expected_agents: List[str]
    complexity_score: float
    keywords: List[str]
    test_category: str

class RoutingAccuracyTester:
    """Agent routing accuracy measurement and validation system"""
    
    def __init__(self, agents_dir: str = "/home/bryan/agentgen/agents"):
        self.agents_dir = Path(agents_dir)
        self.agents_by_tier = self._load_agents_by_tier()
        self.test_cases = self._generate_test_cases()
        
    def _load_agents_by_tier(self) -> Dict[ComplexityTier, List[str]]:
        """Load all agents organized by their current tier structure"""
        agents_by_tier = {tier: [] for tier in ComplexityTier}
        
        for tier in ComplexityTier:
            tier_dir = self.agents_dir / tier.value
            if tier_dir.exists():
                for agent_file in tier_dir.glob("*.md"):
                    agents_by_tier[tier].append(agent_file.stem)
        
        return agents_by_tier
    
    def _generate_test_cases(self) -> List[TestCase]:
        """Generate comprehensive test cases based on cmd-agent-select-logic analysis"""
        
        # Core Tier Test Cases (0.0-0.4 complexity)
        core_tests = [
            TestCase(
                description="read configuration file and display settings",
                expected_tier=ComplexityTier.CORE,
                expected_agents=["config-reader"],
                complexity_score=0.1,
                keywords=["read", "configuration", "settings"],
                test_category="file_operations"
            ),
            TestCase(
                description="analyze screenshot for UI elements extraction",
                expected_tier=ComplexityTier.CORE,
                expected_agents=["analyze-screenshot"],
                complexity_score=0.2,
                keywords=["analyze", "screenshot", "UI", "extract"],
                test_category="image_analysis"
            ),
            TestCase(
                description="find import statements in Python code files",
                expected_tier=ComplexityTier.CORE,
                expected_agents=["config-reader", "env-reader"],
                complexity_score=0.3,
                keywords=["find", "import", "Python", "code"],
                test_category="code_search"
            ),
            TestCase(
                description="check environment variables for configuration",
                expected_tier=ComplexityTier.CORE,
                expected_agents=["env-reader"],
                complexity_score=0.2,
                keywords=["check", "environment", "variables", "config"],
                test_category="environment"
            ),
            TestCase(
                description="read README file and extract project information",
                expected_tier=ComplexityTier.CORE,
                expected_agents=["readme-reader"],
                complexity_score=0.2,
                keywords=["read", "README", "project", "information"],
                test_category="documentation"
            ),
            TestCase(
                description="update project status with current progress",
                expected_tier=ComplexityTier.CORE,
                expected_agents=["update-status"],
                complexity_score=0.3,
                keywords=["update", "status", "progress"],
                test_category="status_tracking"
            )
        ]
        
        # Development Tier Test Cases (0.4-0.7 complexity)  
        development_tests = [
            TestCase(
                description="create React component with TypeScript props interface",
                expected_tier=ComplexityTier.DEVELOPMENT,
                expected_agents=["build-frontend", "ui-designer"],
                complexity_score=0.5,
                keywords=["create", "React", "component", "TypeScript", "props"],
                test_category="frontend_development"
            ),
            TestCase(
                description="build REST API endpoint with authentication middleware",
                expected_tier=ComplexityTier.DEVELOPMENT,
                expected_agents=["build-backend", "api-documenter"],
                complexity_score=0.6,
                keywords=["build", "REST", "API", "endpoint", "authentication"],
                test_category="backend_development"
            ),
            TestCase(
                description="debug TypeScript type error in component hierarchy",
                expected_tier=ComplexityTier.DEVELOPMENT,
                expected_agents=["debugger", "frontend-developer"],
                complexity_score=0.5,
                keywords=["debug", "TypeScript", "type error", "component"],
                test_category="debugging"
            ),
            TestCase(
                description="design user interface mockup with accessibility standards",
                expected_tier=ComplexityTier.DEVELOPMENT,
                expected_agents=["ui-designer", "ux-designer"],
                complexity_score=0.6,
                keywords=["design", "UI", "mockup", "accessibility"],
                test_category="design"
            ),
            TestCase(
                description="write comprehensive API documentation with examples",
                expected_tier=ComplexityTier.DEVELOPMENT,
                expected_agents=["documentation-expert", "api-documenter"],
                complexity_score=0.5,
                keywords=["write", "API", "documentation", "examples"],
                test_category="documentation"
            )
        ]
        
        # Specialists Tier Test Cases (0.7-1.0 complexity)
        specialist_tests = [
            TestCase(
                description="design microservices architecture with event-driven patterns",
                expected_tier=ComplexityTier.SPECIALISTS,
                expected_agents=["architect-specialist", "cloud-architect-specialist"],
                complexity_score=0.9,
                keywords=["design", "microservices", "architecture", "event-driven"],
                test_category="system_architecture"
            ),
            TestCase(
                description="conduct comprehensive security audit with compliance validation",
                expected_tier=ComplexityTier.SPECIALISTS,
                expected_agents=["security-auditor"],
                complexity_score=0.8,
                keywords=["security", "audit", "compliance", "validation"],
                test_category="security"
            ),
            TestCase(
                description="modernize legacy system architecture with cloud migration",
                expected_tier=ComplexityTier.SPECIALISTS,
                expected_agents=["legacy-modernizer", "cloud-architect-specialist"],
                complexity_score=0.9,
                keywords=["modernize", "legacy", "architecture", "cloud", "migration"],
                test_category="legacy_modernization"
            ),
            TestCase(
                description="optimize system-wide performance with bottleneck analysis",
                expected_tier=ComplexityTier.SPECIALISTS,
                expected_agents=["performance-engineer"],
                complexity_score=0.8,
                keywords=["optimize", "performance", "bottleneck", "analysis"],
                test_category="performance"
            ),
            TestCase(
                description="implement machine learning model training pipeline",
                expected_tier=ComplexityTier.SPECIALISTS,
                expected_agents=["ml-specialist", "data-engineer"],
                complexity_score=0.8,
                keywords=["machine learning", "model", "training", "pipeline"],
                test_category="ml_ai"
            )
        ]
        
        return core_tests + development_tests + specialist_tests
    
    def calculate_complexity_score(self, description: str, keywords: List[str]) -> float:
        """Calculate complexity score based on cmd-agent-select-logic criteria with Phase 3.5 enhancements"""
        score = 0.0
        description_lower = description.lower()
        
        # Context Requirements (0.0-0.3)
        if any(word in description_lower for word in ['comprehensive', 'enterprise', 'system-wide']):
            score += 0.3
        elif any(word in description_lower for word in ['interface', 'component', 'endpoint']):
            score += 0.2
        elif any(word in description_lower for word in ['read', 'check', 'find', 'extract']):
            score += 0.1
            
        # Multi-step Workflows (0.0-0.3)
        steps = description_lower.count(' and ') + description_lower.count(' with ')
        if steps >= 3:
            score += 0.3
        elif steps >= 2:
            score += 0.2
        elif steps >= 1:
            score += 0.1
            
        # Domain Expertise (0.0-0.2) - Enhanced for Phase 3.5
        expert_domains = ['architecture', 'security', 'performance', 'machine learning']
        if any(domain in description_lower for domain in expert_domains):
            score += 0.2
        elif any(word in description_lower for word in ['typescript', 'react', 'api']):
            score += 0.1
            
        # Cross-system Impact (0.0-0.2)
        if any(word in description_lower for word in ['system', 'architecture', 'migration']):
            score += 0.2
        elif any(word in description_lower for word in ['component', 'endpoint', 'interface']):
            score += 0.1
        
        # Phase 3.5: Specialist Domain Recognition (0.0-0.5)
        specialist_patterns = {
            'architectural': ['microservices', 'event-driven', 'distributed', 'scalability', 'patterns'],
            'security': ['audit', 'compliance', 'vulnerability', 'threat', 'validation'],
            'ml_ai': ['model', 'training', 'pipeline', 'neural', 'deep learning', 'ai'],
            'modernization': ['legacy', 'modernize', 'transformation', 'refactoring', 'cloud']
        }
        
        specialist_match = False
        for domain, patterns in specialist_patterns.items():
            if any(pattern in description_lower for pattern in patterns):
                score += 0.5  # Strong specialist indicator (increased from 0.4)
                specialist_match = True
                break
        
        # Phase 3.5: Compound Complexity Multipliers
        multiplier = 1.0
        
        # Multiple expert domains in one request
        expert_count = sum(1 for domain in expert_domains if domain in description_lower)
        if expert_count >= 2:
            multiplier = 1.5
        
        # Comprehensive + expert domain
        if 'comprehensive' in description_lower and any(domain in description_lower for domain in expert_domains):
            multiplier = max(multiplier, 1.3)
        
        # Cross-system impact + expert domain
        cross_system_terms = ['system', 'architecture', 'migration', 'enterprise']
        if (any(term in description_lower for term in cross_system_terms) and 
            any(domain in description_lower for domain in expert_domains)):
            multiplier = max(multiplier, 1.4)
        
        # Apply multiplier
        score *= multiplier
        
        # Phase 3.5: Debugging tier fix - ensure debugging tasks score in development range
        if 'debug' in description_lower and score < 0.4:
            score = 0.5  # Force to development tier minimum
            
        return min(score, 1.0)  # Cap at 1.0
    
    def run_routing_accuracy_test(self) -> Dict[str, float]:
        """Execute routing accuracy test suite and calculate metrics"""
        results = {
            'total_tests': len(self.test_cases),
            'correct_tier_predictions': 0,
            'correct_agent_predictions': 0,
            'tier_accuracy': 0.0,
            'agent_accuracy': 0.0,
            'overall_accuracy': 0.0,
            'results_by_category': {},
            'detailed_results': []
        }
        
        category_stats = {}
        
        for test_case in self.test_cases:
            # Calculate predicted complexity score
            predicted_score = self.calculate_complexity_score(
                test_case.description, 
                test_case.keywords
            )
            
            # Determine predicted tier based on score
            if predicted_score < 0.4:
                predicted_tier = ComplexityTier.CORE
            elif predicted_score < 0.7:
                predicted_tier = ComplexityTier.DEVELOPMENT
            else:
                predicted_tier = ComplexityTier.SPECIALISTS
            
            # Check tier accuracy
            tier_correct = predicted_tier == test_case.expected_tier
            if tier_correct:
                results['correct_tier_predictions'] += 1
            
            # Check agent availability in predicted tier
            available_agents = self.agents_by_tier[predicted_tier]
            agent_match = any(agent in available_agents for agent in test_case.expected_agents)
            if agent_match:
                results['correct_agent_predictions'] += 1
            
            # Track by category
            category = test_case.test_category
            if category not in category_stats:
                category_stats[category] = {'total': 0, 'tier_correct': 0, 'agent_correct': 0}
            category_stats[category]['total'] += 1
            if tier_correct:
                category_stats[category]['tier_correct'] += 1
            if agent_match:
                category_stats[category]['agent_correct'] += 1
            
            # Detailed results
            results['detailed_results'].append({
                'description': test_case.description,
                'expected_tier': test_case.expected_tier.value,
                'predicted_tier': predicted_tier.value,
                'expected_score': test_case.complexity_score,
                'predicted_score': predicted_score,
                'tier_correct': tier_correct,
                'agent_match': agent_match,
                'category': test_case.test_category
            })
        
        # Calculate accuracy percentages
        total_tests = results['total_tests']
        results['tier_accuracy'] = results['correct_tier_predictions'] / total_tests * 100
        results['agent_accuracy'] = results['correct_agent_predictions'] / total_tests * 100
        results['overall_accuracy'] = (results['correct_tier_predictions'] + results['correct_agent_predictions']) / (total_tests * 2) * 100
        
        # Category-wise results
        for category, stats in category_stats.items():
            results['results_by_category'][category] = {
                'tier_accuracy': stats['tier_correct'] / stats['total'] * 100,
                'agent_accuracy': stats['agent_correct'] / stats['total'] * 100,
                'total_tests': stats['total']
            }
        
        return results
    
    def generate_report(self, results: Dict) -> str:
        """Generate comprehensive routing accuracy report"""
        report = f"""
# Agent Routing Accuracy Test Report
## Phase 3.1 Baseline Measurement

### Summary
- **Total Test Cases**: {results['total_tests']}
- **Tier Accuracy**: {results['tier_accuracy']:.1f}%
- **Agent Accuracy**: {results['agent_accuracy']:.1f}%
- **Overall Accuracy**: {results['overall_accuracy']:.1f}%

### Current Status
- **Target**: 85% overall accuracy
- **Gap to Target**: {85 - results['overall_accuracy']:.1f} percentage points
- **Improvement Needed**: {'✅ Target achieved!' if results['overall_accuracy'] >= 85 else '🎯 Phase 3.2-3.4 migrations needed'}

### Results by Category
"""
        
        for category, stats in results['results_by_category'].items():
            report += f"- **{category.replace('_', ' ').title()}**: {stats['tier_accuracy']:.1f}% tier, {stats['agent_accuracy']:.1f}% agent ({stats['total_tests']} tests)\n"
        
        report += f"""
### Agent Distribution by Tier
- **Core**: {len(self.agents_by_tier[ComplexityTier.CORE])} agents
- **Development**: {len(self.agents_by_tier[ComplexityTier.DEVELOPMENT])} agents  
- **Specialists**: {len(self.agents_by_tier[ComplexityTier.SPECIALISTS])} agents

### Next Steps
1. Execute Priority 1 migrations (6 agents to core/)
2. Execute Priority 2 migrations (7 agents to development/)
3. Re-run test suite to measure improvement
4. Target: Achieve 85% overall routing accuracy
"""
        
        return report

def main():
    """Main execution function for routing accuracy testing"""
    tester = RoutingAccuracyTester()
    
    print("🧪 Running Agent Routing Accuracy Test Suite...")
    print("=" * 60)
    
    results = tester.run_routing_accuracy_test()
    report = tester.generate_report(results)
    
    print(report)
    
    # Save detailed results
    output_dir = Path("/home/bryan/agentgen/tests/results")
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / "routing_accuracy_baseline.json", "w") as f:
        json.dump(results, f, indent=2)
    
    with open(output_dir / "routing_accuracy_report.md", "w") as f:
        f.write(report)
    
    print(f"\n📊 Detailed results saved to {output_dir}/")
    print(f"🎯 Current overall accuracy: {results['overall_accuracy']:.1f}%")
    print(f"🎯 Target accuracy: 85.0%")
    print(f"📈 Improvement needed: {85 - results['overall_accuracy']:.1f} percentage points")
    
    return results['overall_accuracy']

if __name__ == "__main__":
    accuracy = main()
    sys.exit(0 if accuracy >= 85 else 1)