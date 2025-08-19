# src/core/classifier.py
import time
from typing import Tuple
from .models import ComplexityLevel, TaskAnalysis

class HierarchicalClassifier:
    def __init__(self):
        # Performance target: <25ms for coarse classification
        self.simple_keywords = [
            'read', 'check', 'status', 'get', 'show', 'list', 'display',
            'view', 'find', 'search', 'look', 'see'
        ]
        self.complex_keywords = [
            'comprehensive', 'system-wide', 'enterprise', 'architecture',
            'modernize', 'platform', 'microservices', 'strategic',
            'complete', 'full', 'entire', 'overhaul', 'transform'
        ]
        # Standard indicators - medium complexity
        self.standard_keywords = [
            'implement', 'build', 'create', 'develop', 'integrate',
            'configure', 'setup', 'deploy', 'debug', 'fix', 'test'
        ]
    
    def classify_task(self, description: str) -> TaskAnalysis:
        """Basic task classification using keyword matching with <25ms target"""
        
        start_time = time.perf_counter()
        
        # Level 1: Fast coarse classification (target <15ms)
        coarse_level, confidence = self._coarse_classification(description)
        
        # Level 2: Detailed analysis for standard tasks only if time permits
        if coarse_level == "STANDARD" and (time.perf_counter() - start_time) < 0.010:  # 10ms budget
            detailed_result = self._detailed_analysis(description)
            complexity_score = detailed_result['complexity_score']
            complexity_level = detailed_result['classification']
        else:
            # Fast path - use coarse classification
            complexity_score = 0.2 if coarse_level == "SIMPLE" else (0.9 if coarse_level == "COMPLEX" else 0.5)
            complexity_level = ComplexityLevel(coarse_level.lower())
        
        # Quick resource estimation
        estimated_tokens = self._estimate_tokens(description, complexity_score)
        estimated_time = self._estimate_time(complexity_score)
        
        analysis_time = (time.perf_counter() - start_time) * 1000
        
        return TaskAnalysis(
            description=description,
            complexity_score=complexity_score,
            complexity_level=complexity_level,
            estimated_tokens=estimated_tokens,
            estimated_time_minutes=estimated_time,
            analysis_time_ms=analysis_time
        )
    
    def _coarse_classification(self, description: str) -> Tuple[str, float]:
        """Fast heuristic classification targeting <15ms"""
        
        # Simple preprocessing - minimal string operations
        tokens = description.lower().split()
        token_count = len(tokens)
        
        if token_count == 0:
            return "STANDARD", 0.3
        
        # Fast keyword matching using sets for O(1) lookups
        simple_set = set(self.simple_keywords)
        complex_set = set(self.complex_keywords)
        standard_set = set(self.standard_keywords)
        
        simple_matches = sum(1 for token in tokens if token in simple_set)
        complex_matches = sum(1 for token in tokens if token in complex_set)
        standard_matches = sum(1 for token in tokens if token in standard_set)
        
        # Calculate scores (normalized)
        simple_score = simple_matches / token_count
        complex_score = complex_matches / token_count
        standard_score = standard_matches / token_count
        
        # Decision logic - prioritize simple and complex for fast routing
        if simple_score > 0.15 and complex_score == 0:
            return "SIMPLE", min(simple_score * 6, 0.9)
        elif complex_score > 0.08 or (complex_score > 0 and token_count < 4):
            return "COMPLEX", min(complex_score * 12, 0.9)
        elif standard_score > 0.1:
            return "STANDARD", min(standard_score * 4 + 0.3, 0.8)
        else:
            # Length-based heuristic for unknown patterns
            if token_count <= 4:
                return "SIMPLE", 0.5
            elif token_count >= 12:
                return "COMPLEX", 0.6
            else:
                return "STANDARD", 0.4
    
    def _detailed_analysis(self, description: str) -> dict:
        """More thorough analysis for standard tasks when time permits"""
        
        # Multi-factor scoring for standard tasks
        tokens = description.lower().split()
        
        # Factor 1: Domain complexity (multiple domains = higher complexity)
        domain_indicators = ['ui', 'api', 'database', 'security', 'test', 'deploy']
        domain_matches = sum(1 for token in tokens if any(domain in token for domain in domain_indicators))
        domain_factor = min(domain_matches * 0.15, 0.4)
        
        # Factor 2: Action complexity 
        complex_actions = ['integrate', 'coordinate', 'orchestrate', 'manage']
        action_matches = sum(1 for token in tokens if token in complex_actions)
        action_factor = min(action_matches * 0.2, 0.3)
        
        # Factor 3: Scope indicators
        scope_words = ['multiple', 'several', 'many', 'all', 'complete', 'full']
        scope_matches = sum(1 for token in tokens if token in scope_words)
        scope_factor = min(scope_matches * 0.15, 0.25)
        
        # Combined complexity score
        total_complexity = 0.4 + domain_factor + action_factor + scope_factor  # Base standard score
        
        # Classification based on refined score
        if total_complexity < 0.45:
            return {'complexity_score': total_complexity, 'classification': ComplexityLevel.SIMPLE}
        elif total_complexity > 0.75:
            return {'complexity_score': total_complexity, 'classification': ComplexityLevel.COMPLEX}
        else:
            return {'complexity_score': total_complexity, 'classification': ComplexityLevel.STANDARD}
    
    def _estimate_tokens(self, description: str, complexity_score: float) -> int:
        """More realistic token estimation based on complexity and description length"""
        
        word_count = len(description.split())
        base_tokens = word_count * 200  # Higher multiplier for more realistic estimates
        
        if complexity_score < 0.4:
            # Simple tasks: 3K-8K tokens
            return max(3000, min(int(base_tokens * 2), 8000))
        elif complexity_score > 0.7:
            # Complex tasks: 12K-30K tokens  
            return max(12000, min(int(base_tokens * 6), 30000))
        else:
            # Standard tasks: 6K-18K tokens
            return max(6000, min(int(base_tokens * 4), 18000))
    
    def _estimate_time(self, complexity_score: float) -> int:
        """Estimate time in minutes based on complexity"""
        
        if complexity_score < 0.4:
            return 2  # Simple tasks: 2 minutes
        elif complexity_score > 0.7:
            return 15  # Complex tasks: 15+ minutes
        else:
            return 7   # Standard tasks: 7 minutes