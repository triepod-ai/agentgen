# CMD Agent Select Logic - Implementation Guide

## Overview

This guide provides a comprehensive roadmap for implementing the @cmd-agent-select-logic agent system, including a 3-phase implementation strategy, testing methodologies, integration patterns, and operational procedures.

## Implementation Roadmap

### Phase 1: Core Framework (Week 1)
**Objective**: Establish basic routing functionality with essential features
**Timeline**: 5 working days
**Success Criteria**: Basic agent selection with >80% accuracy for simple tasks

#### Day 1-2: Foundation Setup

**Task 1.1: Project Structure**
```bash
# Create implementation directory structure
mkdir -p cmd-agent-select-logic/{
    src/{core,analysis,routing,cache,monitoring},
    tests/{unit,integration,performance},
    config,
    docs,
    scripts
}

# Initialize version control and dependency management
cd cmd-agent-select-logic
git init
touch requirements.txt setup.py README.md
```

**Task 1.2: Core Data Models**
```python
# src/core/models.py
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class ComplexityLevel(Enum):
    SIMPLE = "simple"
    STANDARD = "standard" 
    COMPLEX = "complex"

class RoutingAction(Enum):
    DIRECT_AGENT = "direct_agent_routing"
    ORCHESTRATION = "orchestration_routing"
    ESCALATE = "escalate_to_organizer"

@dataclass
class TaskAnalysis:
    description: str
    complexity_score: float
    complexity_level: ComplexityLevel
    estimated_tokens: int
    estimated_time_minutes: int
    
@dataclass
class DomainDetection:
    domain: str
    confidence: float
    complexity_bias: float
    preferred_agents: List[str]

@dataclass
class RoutingDecision:
    action: RoutingAction
    selected_agent: Optional[str]
    orchestration_type: Optional[str]
    confidence: float
    reasoning: str
    analysis_time_ms: float
```

**Task 1.3: Basic Classification Engine**
```python
# src/core/classifier.py
import time
from typing import Tuple
from .models import ComplexityLevel, TaskAnalysis

class HierarchicalClassifier:
    def __init__(self):
        self.simple_keywords = [
            'read', 'check', 'status', 'get', 'show', 'list', 'display'
        ]
        self.complex_keywords = [
            'comprehensive', 'system-wide', 'enterprise', 'architecture',
            'modernize', 'platform', 'microservices', 'strategic'
        ]
    
    def classify_task(self, description: str) -> TaskAnalysis:
        """Basic task classification using keyword matching"""
        
        start_time = time.perf_counter()
        
        # Level 1: Fast coarse classification
        coarse_level, confidence = self._coarse_classification(description)
        
        # Level 2: Detailed analysis for standard tasks
        if coarse_level == "STANDARD":
            detailed_result = self._detailed_analysis(description)
            complexity_score = detailed_result['complexity_score']
            complexity_level = detailed_result['classification']
        else:
            complexity_score = 0.2 if coarse_level == "SIMPLE" else 0.9
            complexity_level = ComplexityLevel(coarse_level.lower())
        
        # Estimate resources
        estimated_tokens = self._estimate_tokens(description, complexity_score)
        estimated_time = self._estimate_time(complexity_score)
        
        analysis_time = (time.perf_counter() - start_time) * 1000
        
        return TaskAnalysis(
            description=description,
            complexity_score=complexity_score,
            complexity_level=complexity_level,
            estimated_tokens=estimated_tokens,
            estimated_time_minutes=estimated_time
        )
    
    def _coarse_classification(self, description: str) -> Tuple[str, float]:
        """Fast heuristic classification"""
        
        tokens = description.lower().split()
        
        simple_matches = sum(1 for token in tokens if token in self.simple_keywords)
        complex_matches = sum(1 for token in tokens if token in self.complex_keywords)
        
        simple_score = simple_matches / len(tokens) if tokens else 0
        complex_score = complex_matches / len(tokens) if tokens else 0
        
        if simple_score > 0.1 and complex_score == 0:
            return "SIMPLE", min(simple_score * 5, 0.9)
        elif complex_score > 0.05:
            return "COMPLEX", min(complex_score * 10, 0.9)
        else:
            return "STANDARD", 0.5
```

#### Day 3-4: Domain Detection System

**Task 1.4: Domain Processors**
```python
# src/analysis/domain_detector.py
from abc import ABC, abstractmethod
from typing import Dict, List
import re

class DomainProcessor(ABC):
    def __init__(self, domain_name: str, complexity_bias: float):
        self.domain_name = domain_name
        self.complexity_bias = complexity_bias
        
    @abstractmethod
    def analyze(self, task_description: str) -> float:
        """Return confidence score for domain detection"""
        pass

class FrontendDomainProcessor(DomainProcessor):
    def __init__(self):
        super().__init__("frontend", 0.7)
        self.keywords = {
            'primary': ['react', 'vue', 'angular', 'frontend', 'ui', 'component'],
            'secondary': ['css', 'responsive', 'styling', 'layout'],
            'frameworks': ['nextjs', 'nuxt', 'svelte', 'gatsby']
        }
        self.file_patterns = [
            r'.*\.(jsx|tsx|vue|svelte)$',
            r'.*\.(css|scss|sass)$'
        ]
    
    def analyze(self, task_description: str) -> float:
        tokens = task_description.lower().split()
        
        # Keyword matching
        primary_matches = sum(1 for token in tokens if token in self.keywords['primary'])
        secondary_matches = sum(1 for token in tokens if token in self.keywords['secondary'])
        framework_matches = sum(1 for token in tokens if token in self.keywords['frameworks'])
        
        # File pattern matching
        pattern_matches = sum(1 for pattern in self.file_patterns 
                            if re.search(pattern, task_description))
        
        # Calculate confidence
        keyword_score = (primary_matches * 0.4 + secondary_matches * 0.2 + 
                        framework_matches * 0.15) / len(tokens) if tokens else 0
        pattern_score = min(pattern_matches * 0.25, 0.25)
        
        total_confidence = min(keyword_score + pattern_score, 0.95)
        
        return total_confidence if total_confidence > 0.3 else 0.0

class DomainDetectionEngine:
    def __init__(self):
        self.processors = {
            'frontend': FrontendDomainProcessor(),
            'backend': BackendDomainProcessor(),
            'security': SecurityDomainProcessor(),
            'infrastructure': InfrastructureDomainProcessor(),
            'documentation': DocumentationDomainProcessor(),
            'testing': TestingDomainProcessor()
        }
    
    def detect_domains(self, task_description: str) -> Dict:
        """Detect all applicable domains for the task"""
        
        detected_domains = []
        total_confidence = 0
        
        for domain_name, processor in self.processors.items():
            confidence = processor.analyze(task_description)
            if confidence > 0.3:  # Threshold for domain activation
                detected_domains.append({
                    'domain': domain_name,
                    'confidence': confidence,
                    'complexity_bias': processor.complexity_bias
                })
                total_confidence += confidence
        
        return {
            'domains': detected_domains,
            'domain_count': len(detected_domains),
            'total_confidence': total_confidence
        }
```

#### Day 5: Basic Routing Engine

**Task 1.5: Simple Routing Logic**
```python
# src/routing/router.py
from typing import Dict
from ..core.models import RoutingDecision, RoutingAction
from ..analysis.domain_detector import DomainDetectionEngine

class BasicRoutingEngine:
    def __init__(self):
        self.domain_detector = DomainDetectionEngine()
        
        # Simple agent mapping
        self.agent_mappings = {
            'frontend': '@build-frontend',
            'backend': '@build-backend',
            'security': '@security-auditor',
            'infrastructure': '@deployment-engineer',
            'documentation': '@documentation-expert',
            'testing': '@test-automator'
        }
    
    def route_task(self, task_analysis, domain_analysis) -> RoutingDecision:
        """Basic routing logic without advanced features"""
        
        start_time = time.perf_counter()
        
        # Simple decision logic
        if domain_analysis['domain_count'] == 0:
            # No clear domain - escalate
            action = RoutingAction.ESCALATE
            selected_agent = None
            confidence = 0.3
            reasoning = "No clear domain detected - requires strategic analysis"
            
        elif domain_analysis['domain_count'] == 1:
            # Single domain - direct routing
            domain = domain_analysis['domains'][0]
            action = RoutingAction.DIRECT_AGENT
            selected_agent = self.agent_mappings.get(domain['domain'], '@orchestrate-tasks')
            confidence = domain['confidence']
            reasoning = f"Single domain ({domain['domain']}) detected with {confidence:.2f} confidence"
            
        else:
            # Multiple domains - orchestration
            action = RoutingAction.ORCHESTRATION
            selected_agent = None
            confidence = min(domain_analysis['total_confidence'] / domain_analysis['domain_count'], 0.8)
            reasoning = f"Multiple domains ({domain_analysis['domain_count']}) require coordination"
        
        analysis_time = (time.perf_counter() - start_time) * 1000
        
        return RoutingDecision(
            action=action,
            selected_agent=selected_agent,
            orchestration_type='@orchestrate-agents' if action == RoutingAction.ORCHESTRATION else None,
            confidence=confidence,
            reasoning=reasoning,
            analysis_time_ms=analysis_time
        )
```

**Phase 1 Testing Strategy**:
```python
# tests/test_basic_functionality.py
import pytest
from src.core.classifier import HierarchicalClassifier
from src.analysis.domain_detector import DomainDetectionEngine
from src.routing.router import BasicRoutingEngine

class TestPhase1:
    def test_simple_classification(self):
        classifier = HierarchicalClassifier()
        result = classifier.classify_task("check the status of deployment")
        
        assert result.complexity_level.value == "simple"
        assert result.complexity_score < 0.5
        assert result.estimated_tokens < 5000
    
    def test_complex_classification(self):
        classifier = HierarchicalClassifier()
        result = classifier.classify_task("comprehensive system-wide architecture modernization")
        
        assert result.complexity_level.value == "complex"
        assert result.complexity_score > 0.7
        assert result.estimated_tokens > 10000
    
    def test_frontend_domain_detection(self):
        detector = DomainDetectionEngine()
        result = detector.detect_domains("create a React component with responsive styling")
        
        assert result['domain_count'] == 1
        assert result['domains'][0]['domain'] == 'frontend'
        assert result['domains'][0]['confidence'] > 0.5
    
    def test_basic_routing(self):
        router = BasicRoutingEngine()
        
        # Mock task analysis and domain analysis
        task_analysis = MockTaskAnalysis()
        domain_analysis = {'domains': [{'domain': 'frontend', 'confidence': 0.8}], 'domain_count': 1}
        
        result = router.route_task(task_analysis, domain_analysis)
        
        assert result.action == RoutingAction.DIRECT_AGENT
        assert result.selected_agent == '@build-frontend'
        assert result.confidence > 0.7

# Performance benchmarks for Phase 1
def test_performance_targets():
    classifier = HierarchicalClassifier()
    
    # Test response time targets
    start = time.perf_counter()
    classifier.classify_task("simple task description")
    simple_time = (time.perf_counter() - start) * 1000
    
    assert simple_time < 50  # 50ms target for simple tasks
```

### Phase 2: Intelligence Layer (Week 2)
**Objective**: Add sophisticated analysis and strategic routing
**Timeline**: 5 working days
**Success Criteria**: >90% routing accuracy with strategic escalation

#### Day 6-7: Multi-Factor Complexity Scoring

**Task 2.1: Advanced Complexity Analysis**
```python
# src/analysis/complexity_analyzer.py
import re
from typing import Dict, List

class ComplexityAnalyzer:
    def __init__(self):
        # Load historical data for learning
        self.historical_patterns = self._load_historical_patterns()
        
    def multi_factor_analysis(self, task_description: str) -> Dict:
        """Research-based multi-factor complexity scoring"""
        
        factors = {
            'domain_complexity': self._analyze_domain_span(task_description) * 0.25,
            'parameter_complexity': self._analyze_parameters(task_description) * 0.20,
            'interdependency': self._analyze_dependencies(task_description) * 0.25,
            'resource_requirements': self._estimate_resources(task_description) * 0.15,
            'historical_difficulty': self._get_historical_difficulty(task_description) * 0.15
        }
        
        total_complexity = sum(factors.values())
        
        # Apply research-based thresholds
        if total_complexity < 0.3:
            classification = "SIMPLE_REFINED"
        elif total_complexity > 0.7:
            classification = "COMPLEX_REFINED"
        else:
            classification = "STANDARD_CONFIRMED"
            
        return {
            'complexity_score': total_complexity,
            'classification': classification,
            'factor_breakdown': factors,
            'confidence': self._calculate_complexity_confidence(factors)
        }
    
    def _analyze_domain_span(self, description: str) -> float:
        """Analyze how many domains the task spans"""
        domain_keywords = {
            'frontend': ['ui', 'component', 'react', 'vue'],
            'backend': ['api', 'server', 'database'],
            'security': ['auth', 'security', 'vulnerability'],
            'infrastructure': ['deploy', 'docker', 'cloud'],
            'testing': ['test', 'qa', 'validation']
        }
        
        detected_domains = set()
        tokens = description.lower().split()
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in tokens for keyword in keywords):
                detected_domains.add(domain)
        
        # Score based on domain count (normalized to 0-1)
        return min(len(detected_domains) / 4.0, 1.0)
    
    def _analyze_parameters(self, description: str) -> float:
        """Estimate parameter complexity based on linguistic analysis"""
        
        # Count conditional statements, constraints, and requirements
        complexity_indicators = [
            r'\b(if|when|unless|provided|given)\b',  # Conditionals
            r'\b(must|should|need|require)\b',       # Requirements
            r'\b(and|or|but|however)\b',             # Conjunctions
            r'\b(with|using|including)\b'            # Qualifiers
        ]
        
        total_matches = 0
        for pattern in complexity_indicators:
            matches = len(re.findall(pattern, description.lower()))
            total_matches += matches
            
        # Normalize to 0-1 scale (cap at 20 indicators)
        return min(total_matches / 20.0, 1.0)
```

**Task 2.2: Confidence Scoring Engine**
```python
# src/analysis/confidence_calculator.py
from typing import Dict, List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class ConfidenceCalculator:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.agent_capabilities = self._load_agent_capabilities()
        
    def calculate_routing_confidence(self, task_analysis: Dict, 
                                   domain_analysis: Dict) -> Dict:
        """Multi-metric confidence calculation"""
        
        # 1. Pattern Matching Confidence (40% weight)
        pattern_confidence = self._calculate_pattern_confidence(
            task_analysis['description']
        )
        
        # 2. Historical Success Confidence (30% weight)
        historical_confidence = self._get_historical_success_rate(
            self._generate_task_signature(task_analysis['description'])
        )
        
        # 3. Context Completeness Confidence (20% weight)
        context_confidence = self._assess_context_completeness(
            task_analysis['description']
        )
        
        # 4. Resource Availability Confidence (10% weight)
        resource_confidence = self._assess_resource_availability(
            task_analysis['estimated_tokens']
        )
        
        # Weighted combination
        components = {
            'pattern_match': pattern_confidence,
            'historical_success': historical_confidence,
            'context_completeness': context_confidence,
            'resource_availability': resource_confidence
        }
        
        total_confidence = (
            pattern_confidence * 0.4 +
            historical_confidence * 0.3 +
            context_confidence * 0.2 +
            resource_confidence * 0.1
        )
        
        return {
            'total_confidence': total_confidence,
            'components': components,
            'variance': self._calculate_confidence_variance(components)
        }
    
    def _calculate_pattern_confidence(self, description: str) -> float:
        """Calculate semantic similarity with agent capabilities"""
        
        # Vectorize task description
        task_vector = self.vectorizer.fit_transform([description])
        
        max_similarity = 0.0
        for agent_name, capability_text in self.agent_capabilities.items():
            capability_vector = self.vectorizer.transform([capability_text])
            similarity = cosine_similarity(task_vector, capability_vector)[0][0]
            max_similarity = max(max_similarity, similarity)
        
        return min(max_similarity, 0.95)  # Cap at 95%
```

#### Day 8-9: Strategic Escalation Engine

**Task 2.3: Escalation Decision Framework**
```python
# src/routing/escalation_engine.py
from typing import Dict, List
from ..core.models import RoutingDecision, RoutingAction

class EscalationEngine:
    def __init__(self):
        self.escalation_triggers = {
            'low_confidence': {'threshold': 0.4, 'weight': 0.35},
            'high_complexity': {'threshold': 0.8, 'weight': 0.25},
            'multi_domain': {'threshold': 3, 'weight': 0.15},
            'enterprise_scope': {'weight': 0.10},
            'architectural_decisions': {'weight': 0.10},
            'ambiguous_requirements': {'threshold': 0.6, 'weight': 0.05}
        }
    
    def should_escalate(self, complexity_score: float, domain_analysis: Dict,
                       confidence_analysis: Dict, task_description: str) -> Dict:
        """Multi-criteria escalation decision"""
        
        # Evaluate individual triggers
        triggers = {
            'low_confidence': confidence_analysis['total_confidence'] < 0.4,
            'high_complexity': complexity_score > 0.8,
            'multi_domain': domain_analysis['domain_count'] > 3,
            'enterprise_scope': self._detect_enterprise_scope(task_description),
            'architectural_decisions': self._detect_architectural_keywords(task_description),
            'ambiguous_requirements': self._assess_ambiguity(task_description) > 0.6
        }
        
        # Calculate escalation score
        escalation_score = self._calculate_escalation_score(
            complexity_score, domain_analysis, confidence_analysis, triggers
        )
        
        # Make escalation decision
        if escalation_score > 0.7 or triggers['enterprise_scope']:
            return {
                'should_escalate': True,
                'escalation_score': escalation_score,
                'triggered_conditions': [k for k, v in triggers.items() if v],
                'context_package': self._create_context_package(
                    task_description, complexity_score, domain_analysis, confidence_analysis
                )
            }
        
        return {
            'should_escalate': False,
            'escalation_score': escalation_score,
            'alternative_routing': self._determine_alternative_routing(
                domain_analysis, confidence_analysis
            )
        }
    
    def _create_context_package(self, task_description: str, complexity_score: float,
                              domain_analysis: Dict, confidence_analysis: Dict) -> Dict:
        """Create comprehensive context for @agent-organizer"""
        
        return {
            'routing_metadata': {
                'escalation_timestamp': time.time(),
                'escalation_reason': 'strategic_analysis_required',
                'routing_agent': '@cmd-agent-select-logic'
            },
            'task_analysis': {
                'original_request': task_description,
                'complexity_score': complexity_score,
                'estimated_effort': self._estimate_effort_hours(complexity_score)
            },
            'domain_intelligence': {
                'detected_domains': domain_analysis['domains'],
                'domain_interactions': self._analyze_domain_interactions(domain_analysis)
            },
            'confidence_intelligence': {
                'routing_confidence': confidence_analysis['total_confidence'],
                'confidence_breakdown': confidence_analysis['components']
            },
            'strategic_recommendations': {
                'suggested_approach': self._recommend_approach(complexity_score, domain_analysis),
                'team_composition': self._recommend_team(domain_analysis),
                'success_criteria': self._define_success_criteria(task_description)
            }
        }
```

#### Day 10: Orchestration Routing

**Task 2.4: Intelligent Orchestration Selection**
```python
# src/routing/orchestration_router.py

class OrchestrationRouter:
    def __init__(self):
        self.orchestration_systems = {
            '@orchestrate-tasks': {
                'domains': [1],
                'complexity': [0.0, 0.5],
                'description': 'Intelligent single-agent analysis'
            },
            '@orchestrate-agents': {
                'domains': [2, 3],
                'complexity': [0.5, 0.8],
                'description': 'Standard multi-agent coordination'
            },
            '@orchestrate-agents-adv': {
                'domains': [4, 5, 6],
                'complexity': [0.8, 1.0],
                'description': 'Enterprise-level coordination'
            }
        }
    
    def select_orchestration_type(self, domain_count: int, 
                                 complexity_score: float) -> str:
        """Select appropriate orchestration system"""
        
        # Priority: complexity > domain count
        if complexity_score > 0.8:
            return '@orchestrate-agents-adv'
        elif domain_count >= 4:
            return '@orchestrate-agents-adv'
        elif domain_count >= 2 or complexity_score > 0.5:
            return '@orchestrate-agents'
        else:
            return '@orchestrate-tasks'
```

**Phase 2 Testing Strategy**:
```python
# tests/test_intelligence_layer.py

class TestPhase2:
    def test_multi_factor_complexity(self):
        analyzer = ComplexityAnalyzer()
        
        # Test complex multi-domain task
        result = analyzer.multi_factor_analysis(
            "Build a secure React dashboard with real-time API integration, "
            "user authentication, and comprehensive testing"
        )
        
        assert result['complexity_score'] > 0.7
        assert result['classification'] in ['COMPLEX_REFINED']
        assert 'domain_complexity' in result['factor_breakdown']
        assert result['factor_breakdown']['domain_complexity'] > 0.5
    
    def test_confidence_calculation(self):
        calculator = ConfidenceCalculator()
        
        task_analysis = {'description': 'debug React component rendering issue'}
        domain_analysis = {'domains': [{'domain': 'frontend', 'confidence': 0.9}]}
        
        result = calculator.calculate_routing_confidence(task_analysis, domain_analysis)
        
        assert result['total_confidence'] > 0.7
        assert 'pattern_match' in result['components']
        assert result['components']['pattern_match'] > 0.5
    
    def test_escalation_decision(self):
        engine = EscalationEngine()
        
        # High complexity, multi-domain task should escalate
        result = engine.should_escalate(
            complexity_score=0.9,
            domain_analysis={'domain_count': 4, 'domains': []},
            confidence_analysis={'total_confidence': 0.3},
            task_description="comprehensive enterprise architecture modernization"
        )
        
        assert result['should_escalate'] == True
        assert result['escalation_score'] > 0.7
        assert 'context_package' in result
```

### Phase 3: Optimization (Week 3)
**Objective**: Implement caching, monitoring, and adaptive learning
**Timeline**: 5 working days
**Success Criteria**: <100ms response time, >80% cache hit rate

#### Day 11-12: Caching System

**Task 3.1: Multi-Layer Cache Implementation**
```python
# src/cache/intelligent_cache.py
import time
import hashlib
from typing import Dict, Optional, Any
from cachetools import TTLCache
from threading import Lock

class IntelligentCacheSystem:
    def __init__(self):
        # L1: High-frequency pattern cache
        self.l1_cache = TTLCache(maxsize=1000, ttl=3600)  # 1 hour
        self.l1_lock = Lock()
        
        # L2: Domain analysis cache
        self.l2_cache = TTLCache(maxsize=500, ttl=1800)   # 30 minutes
        self.l2_lock = Lock()
        
        # L3: Complexity calculation cache
        self.l3_cache = TTLCache(maxsize=200, ttl=300)    # 5 minutes
        self.l3_lock = Lock()
        
        # Cache statistics
        self.stats = {
            'l1_hits': 0, 'l1_misses': 0,
            'l2_hits': 0, 'l2_misses': 0,
            'l3_hits': 0, 'l3_misses': 0
        }
    
    def get_cached_result(self, cache_key: str, cache_level: int) -> Optional[Any]:
        """Get cached result from specified cache level"""
        
        cache_map = {1: (self.l1_cache, self.l1_lock, 'l1'),
                     2: (self.l2_cache, self.l2_lock, 'l2'),
                     3: (self.l3_cache, self.l3_lock, 'l3')}
        
        cache, lock, prefix = cache_map[cache_level]
        
        with lock:
            if cache_key in cache:
                self.stats[f'{prefix}_hits'] += 1
                return cache[cache_key]
            else:
                self.stats[f'{prefix}_misses'] += 1
                return None
    
    def cache_result(self, cache_key: str, result: Any, cache_level: int):
        """Cache result at specified level with metadata"""
        
        cache_map = {1: (self.l1_cache, self.l1_lock),
                     2: (self.l2_cache, self.l2_lock),
                     3: (self.l3_cache, self.l3_lock)}
        
        cache, lock = cache_map[cache_level]
        
        enriched_result = {
            'data': result,
            'cached_at': time.time(),
            'cache_level': cache_level,
            'access_count': 1
        }
        
        with lock:
            cache[cache_key] = enriched_result
    
    def generate_cache_key(self, data: str, prefix: str = "") -> str:
        """Generate consistent cache key"""
        
        # Create hash of the data
        hasher = hashlib.md5()
        hasher.update(data.encode('utf-8'))
        hash_value = hasher.hexdigest()
        
        return f"{prefix}:{hash_value}" if prefix else hash_value
    
    def get_cache_statistics(self) -> Dict:
        """Return comprehensive cache statistics"""
        
        total_requests = sum(self.stats.values())
        hit_rate = (
            (self.stats['l1_hits'] + self.stats['l2_hits'] + self.stats['l3_hits']) 
            / total_requests
        ) if total_requests > 0 else 0
        
        return {
            'overall_hit_rate': hit_rate,
            'l1_hit_rate': self.stats['l1_hits'] / (self.stats['l1_hits'] + self.stats['l1_misses']) if (self.stats['l1_hits'] + self.stats['l1_misses']) > 0 else 0,
            'l2_hit_rate': self.stats['l2_hits'] / (self.stats['l2_hits'] + self.stats['l2_misses']) if (self.stats['l2_hits'] + self.stats['l2_misses']) > 0 else 0,
            'l3_hit_rate': self.stats['l3_hits'] / (self.stats['l3_hits'] + self.stats['l3_misses']) if (self.stats['l3_hits'] + self.stats['l3_misses']) > 0 else 0,
            'total_requests': total_requests,
            'cache_efficiency': self._calculate_cache_efficiency()
        }
```

**Task 3.2: Circuit Breaker Pattern**
```python
# src/reliability/circuit_breaker.py
import time
from enum import Enum
from typing import Callable, Any, Dict

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class RoutingCircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 30,
                 success_threshold: int = 3):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def execute(self, routing_function: Callable, *args, **kwargs) -> Any:
        """Execute routing function with circuit breaker protection"""
        
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                self.success_count = 0
            else:
                return self._fallback_routing(*args, **kwargs)
        
        try:
            result = routing_function(*args, **kwargs)
            self._record_success()
            return result
            
        except Exception as e:
            self._record_failure()
            return self._fallback_routing(*args, **kwargs)
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        return (time.time() - self.last_failure_time) >= self.recovery_timeout
    
    def _record_success(self):
        """Record successful operation"""
        self.failure_count = 0
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0
    
    def _record_failure(self):
        """Record failed operation"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
    
    def _fallback_routing(self, task_description: str, *args, **kwargs) -> Dict:
        """Fallback to safe routing when circuit is open"""
        return {
            'action': 'FALLBACK_TO_ORCHESTRATE_TASKS',
            'selected_agent': '@orchestrate-tasks',
            'confidence': 0.6,
            'reasoning': f'Circuit breaker fallback - system in {self.state.value} state',
            'fallback': True
        }
```

#### Day 13-14: Performance Monitoring

**Task 3.3: Comprehensive Monitoring System**
```python
# src/monitoring/performance_monitor.py
import time
import statistics
from typing import Dict, List
from collections import deque
import logging

class PerformanceMonitoringSystem:
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        
        # Performance metrics storage
        self.response_times = deque(maxlen=max_history)
        self.routing_decisions = deque(maxlen=max_history)
        self.accuracy_metrics = deque(maxlen=max_history)
        
        # Real-time counters
        self.total_requests = 0
        self.successful_routes = 0
        self.escalations = 0
        self.cache_hits = 0
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
    
    def record_routing_decision(self, decision_data: Dict):
        """Record a routing decision with performance metrics"""
        
        self.total_requests += 1
        
        # Store decision data
        self.routing_decisions.append({
            'timestamp': time.time(),
            'decision_time_ms': decision_data.get('analysis_time_ms', 0),
            'action': decision_data.get('action'),
            'confidence': decision_data.get('confidence', 0),
            'cache_hit': decision_data.get('cache_hit', False),
            'complexity_score': decision_data.get('complexity_score', 0),
            'domain_count': decision_data.get('domain_count', 0)
        })
        
        # Update counters
        if decision_data.get('cache_hit'):
            self.cache_hits += 1
        
        if decision_data.get('action') == 'ESCALATE_TO_ORGANIZER':
            self.escalations += 1
        
        # Record response time
        self.response_times.append(decision_data.get('analysis_time_ms', 0))
    
    def record_outcome(self, routing_id: str, outcome_data: Dict):
        """Record the actual outcome of a routing decision"""
        
        if outcome_data.get('success', False):
            self.successful_routes += 1
        
        self.accuracy_metrics.append({
            'routing_id': routing_id,
            'success': outcome_data.get('success', False),
            'user_satisfaction': outcome_data.get('satisfaction', 0),
            'optimal_agent': outcome_data.get('optimal_agent', False),
            'timestamp': time.time()
        })
    
    def generate_performance_report(self, time_window_hours: int = 24) -> Dict:
        """Generate comprehensive performance report"""
        
        # Filter recent data
        cutoff_time = time.time() - (time_window_hours * 3600)
        recent_decisions = [d for d in self.routing_decisions 
                          if d['timestamp'] > cutoff_time]
        recent_outcomes = [o for o in self.accuracy_metrics 
                         if o['timestamp'] > cutoff_time]
        
        if not recent_decisions:
            return {'error': 'No data available for specified time window'}
        
        # Performance metrics
        response_times = [d['decision_time_ms'] for d in recent_decisions]
        
        performance_metrics = {
            'avg_response_time_ms': statistics.mean(response_times),
            'p50_response_time_ms': statistics.median(response_times),
            'p95_response_time_ms': self._percentile(response_times, 95),
            'p99_response_time_ms': self._percentile(response_times, 99),
            'max_response_time_ms': max(response_times),
            'cache_hit_rate': sum(1 for d in recent_decisions if d['cache_hit']) / len(recent_decisions),
            'requests_per_hour': len(recent_decisions) / time_window_hours
        }
        
        # Accuracy metrics
        if recent_outcomes:
            accuracy_metrics = {
                'success_rate': sum(1 for o in recent_outcomes if o['success']) / len(recent_outcomes),
                'user_satisfaction': statistics.mean([o['user_satisfaction'] for o in recent_outcomes]),
                'optimal_agent_rate': sum(1 for o in recent_outcomes if o['optimal_agent']) / len(recent_outcomes)
            }
        else:
            accuracy_metrics = {'note': 'No outcome data available'}
        
        # System health
        escalation_rate = sum(1 for d in recent_decisions 
                            if d['action'] == 'ESCALATE_TO_ORGANIZER') / len(recent_decisions)
        
        system_health = {
            'escalation_rate': escalation_rate,
            'avg_confidence': statistics.mean([d['confidence'] for d in recent_decisions]),
            'avg_complexity': statistics.mean([d['complexity_score'] for d in recent_decisions]),
            'avg_domains_per_task': statistics.mean([d['domain_count'] for d in recent_decisions])
        }
        
        return {
            'performance': performance_metrics,
            'accuracy': accuracy_metrics,
            'system_health': system_health,
            'recommendations': self._generate_recommendations(
                performance_metrics, system_health
            )
        }
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile value"""
        if not data:
            return 0.0
        
        sorted_data = sorted(data)
        index = (percentile / 100) * (len(sorted_data) - 1)
        
        if index.is_integer():
            return sorted_data[int(index)]
        else:
            lower = sorted_data[int(index)]
            upper = sorted_data[int(index) + 1]
            return lower + (upper - lower) * (index - int(index))
```

#### Day 15: Adaptive Learning System

**Task 3.4: Machine Learning Integration**
```python
# src/learning/adaptive_system.py
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from typing import Dict, List, Tuple

class AdaptiveLearningSystem:
    def __init__(self):
        self.routing_model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.confidence_model = RandomForestClassifier(n_estimators=50, random_state=42)
        
        self.pattern_weights = {}
        self.domain_weights = {}
        
        # Learning data storage
        self.training_data = []
        self.model_trained = False
    
    def update_from_outcome(self, routing_decision: Dict, outcome: Dict):
        """Update learning models based on routing outcomes"""
        
        # Prepare training sample
        features = self._extract_features(routing_decision)
        
        # Labels: successful routing (1) or not (0)
        routing_success = 1 if outcome.get('success', False) else 0
        
        # Confidence accuracy: how close predicted confidence was to actual success
        predicted_confidence = routing_decision.get('confidence', 0.5)
        actual_success = outcome.get('success', False)
        confidence_accuracy = 1.0 - abs(predicted_confidence - (1.0 if actual_success else 0.0))
        
        # Store training sample
        self.training_data.append({
            'features': features,
            'routing_success': routing_success,
            'confidence_accuracy': confidence_accuracy,
            'timestamp': time.time()
        })
        
        # Update pattern weights based on success
        self._update_pattern_weights(routing_decision, outcome.get('success', False))
        
        # Retrain models periodically
        if len(self.training_data) % 50 == 0:  # Retrain every 50 samples
            self._retrain_models()
    
    def predict_routing_success(self, task_features: Dict) -> float:
        """Predict probability of successful routing"""
        
        if not self.model_trained:
            return 0.5  # Default neutral prediction
        
        features = self._extract_features(task_features)
        feature_array = np.array([features]).reshape(1, -1)
        
        # Get probability of successful routing
        success_probability = self.routing_model.predict_proba(feature_array)[0][1]
        
        return success_probability
    
    def adjust_confidence_threshold(self, current_accuracy: float, target_accuracy: float = 0.85):
        """Dynamically adjust confidence thresholds based on performance"""
        
        if current_accuracy < target_accuracy:
            # Lower confidence threshold to be more conservative
            adjustment = (target_accuracy - current_accuracy) * 0.1
            return max(0.3, 0.4 - adjustment)  # Don't go below 0.3
        elif current_accuracy > target_accuracy + 0.05:
            # Raise confidence threshold to be more aggressive  
            adjustment = (current_accuracy - target_accuracy) * 0.1
            return min(0.7, 0.4 + adjustment)  # Don't go above 0.7
        else:
            return 0.4  # Default threshold
    
    def _extract_features(self, routing_data: Dict) -> List[float]:
        """Extract numerical features for machine learning"""
        
        features = [
            routing_data.get('complexity_score', 0.5),
            routing_data.get('domain_count', 1),
            routing_data.get('total_domain_confidence', 0.5),
            routing_data.get('pattern_match_confidence', 0.5),
            routing_data.get('context_completeness', 0.5),
            routing_data.get('estimated_tokens', 5000) / 20000,  # Normalized
            routing_data.get('cache_hit', 0),  # 1 if cache hit, 0 otherwise
            len(routing_data.get('task_description', '')) / 200,  # Normalized description length
        ]
        
        return features
    
    def _update_pattern_weights(self, routing_decision: Dict, success: bool):
        """Update pattern weights based on routing success"""
        
        patterns_used = routing_decision.get('patterns_matched', [])
        weight_adjustment = 0.1 if success else -0.05
        
        for pattern in patterns_used:
            current_weight = self.pattern_weights.get(pattern, 1.0)
            new_weight = max(0.1, min(2.0, current_weight + weight_adjustment))
            self.pattern_weights[pattern] = new_weight
    
    def _retrain_models(self):
        """Retrain machine learning models with accumulated data"""
        
        if len(self.training_data) < 20:  # Need minimum samples
            return
        
        # Prepare training data
        X = np.array([sample['features'] for sample in self.training_data])
        y_routing = np.array([sample['routing_success'] for sample in self.training_data])
        y_confidence = np.array([sample['confidence_accuracy'] for sample in self.training_data])
        
        # Train routing success model
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_routing, test_size=0.2, random_state=42
        )
        
        self.routing_model.fit(X_train, y_train)
        
        # Evaluate model performance
        y_pred = self.routing_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        self.model_trained = True
        
        print(f"Routing model retrained. Accuracy: {accuracy:.3f}")
```

**Phase 3 Testing Strategy**:
```python
# tests/test_optimization.py

class TestPhase3:
    def test_cache_performance(self):
        cache = IntelligentCacheSystem()
        
        # Test cache hit/miss
        key = cache.generate_cache_key("test task", "pattern")
        
        # First access should be miss
        result = cache.get_cached_result(key, 1)
        assert result is None
        
        # Cache a result
        cache.cache_result(key, {"confidence": 0.8}, 1)
        
        # Second access should be hit
        result = cache.get_cached_result(key, 1)
        assert result is not None
        assert result['data']['confidence'] == 0.8
        
        # Check statistics
        stats = cache.get_cache_statistics()
        assert stats['l1_hit_rate'] > 0
    
    def test_circuit_breaker(self):
        breaker = RoutingCircuitBreaker(failure_threshold=2, recovery_timeout=1)
        
        def failing_function(task_description):
            raise Exception("Test failure")
        
        def working_function(task_description):
            return {"success": True}
        
        # Trigger failures to open circuit
        result1 = breaker.execute(failing_function, "test task")
        result2 = breaker.execute(failing_function, "test task")
        
        assert breaker.state == CircuitState.OPEN
        assert result2.get('fallback') == True
        
        # Test recovery after timeout
        time.sleep(1.1)  # Wait for recovery timeout
        result3 = breaker.execute(working_function, "test task")
        
        assert result3.get('success') == True
        assert breaker.state == CircuitState.CLOSED
    
    def test_performance_monitoring(self):
        monitor = PerformanceMonitoringSystem()
        
        # Record some decisions
        for i in range(10):
            monitor.record_routing_decision({
                'analysis_time_ms': 50 + i * 5,
                'action': 'DIRECT_AGENT_ROUTING',
                'confidence': 0.8 + i * 0.01,
                'cache_hit': i % 2 == 0,
                'complexity_score': 0.5,
                'domain_count': 1
            })
        
        # Generate report
        report = monitor.generate_performance_report(24)
        
        assert 'performance' in report
        assert report['performance']['avg_response_time_ms'] > 0
        assert report['performance']['cache_hit_rate'] == 0.5
        assert len(report['recommendations']) > 0
```

## Testing Strategies

### Unit Testing Framework
```python
# tests/conftest.py - Pytest configuration
import pytest
from src.core.classifier import HierarchicalClassifier
from src.analysis.domain_detector import DomainDetectionEngine
from src.routing.router import AdvancedRoutingEngine
from src.cache.intelligent_cache import IntelligentCacheSystem

@pytest.fixture
def classifier():
    return HierarchicalClassifier()

@pytest.fixture  
def domain_detector():
    return DomainDetectionEngine()

@pytest.fixture
def routing_engine():
    return AdvancedRoutingEngine()

@pytest.fixture
def cache_system():
    return IntelligentCacheSystem()
```

### Integration Testing
```python
# tests/test_integration.py
class TestEndToEndIntegration:
    def test_complete_routing_pipeline(self):
        """Test the complete routing process"""
        
        # Initialize system components
        classifier = HierarchicalClassifier()
        domain_detector = DomainDetectionEngine()
        router = AdvancedRoutingEngine()
        
        # Test data
        test_cases = [
            {
                'description': 'Create a React component with user authentication',
                'expected_action': 'ORCHESTRATION_ROUTING',
                'expected_domains': ['frontend', 'security']
            },
            {
                'description': 'Check deployment status',
                'expected_action': 'DIRECT_AGENT_ROUTING', 
                'expected_agent': '@monitor-system'
            },
            {
                'description': 'Comprehensive enterprise architecture modernization',
                'expected_action': 'ESCALATE_TO_ORGANIZER'
            }
        ]
        
        for case in test_cases:
            # Execute pipeline
            task_analysis = classifier.classify_task(case['description'])
            domain_analysis = domain_detector.detect_domains(case['description'])
            routing_decision = router.route_task(task_analysis, domain_analysis)
            
            # Verify results
            assert routing_decision.action.value == case['expected_action']
            
            if 'expected_agent' in case:
                assert routing_decision.selected_agent == case['expected_agent']
            
            if 'expected_domains' in case:
                detected_domains = [d['domain'] for d in domain_analysis['domains']]
                for expected_domain in case['expected_domains']:
                    assert expected_domain in detected_domains
```

### Performance Testing
```python
# tests/test_performance.py
import time
import threading
from concurrent.futures import ThreadPoolExecutor

class TestPerformance:
    def test_response_time_targets(self):
        """Test that response times meet targets"""
        
        router = AdvancedRoutingEngine()
        
        test_cases = [
            ('check status', 50),      # Simple: <50ms
            ('build React app', 100),  # Standard: <100ms
            ('enterprise modernization', 200)  # Complex: <200ms
        ]
        
        for description, target_ms in test_cases:
            start_time = time.perf_counter()
            result = router.analyze_and_route(description)
            end_time = time.perf_counter()
            
            actual_time_ms = (end_time - start_time) * 1000
            
            assert actual_time_ms < target_ms, f"Response time {actual_time_ms:.1f}ms exceeded target {target_ms}ms"
    
    def test_cache_hit_rate(self):
        """Test cache performance targets"""
        
        cache = IntelligentCacheSystem()
        router = AdvancedRoutingEngine(cache_system=cache)
        
        # Execute same requests multiple times
        test_descriptions = [
            'debug React component',
            'deploy to production',
            'security audit'
        ]
        
        # First round - populate cache
        for description in test_descriptions:
            router.analyze_and_route(description)
        
        # Second round - should hit cache
        for description in test_descriptions:
            router.analyze_and_route(description)
        
        stats = cache.get_cache_statistics()
        assert stats['overall_hit_rate'] > 0.5  # >50% cache hit rate
    
    def test_concurrent_performance(self):
        """Test system under concurrent load"""
        
        router = AdvancedRoutingEngine()
        results = []
        
        def route_task(description):
            start_time = time.perf_counter()
            result = router.analyze_and_route(description)
            end_time = time.perf_counter()
            return (end_time - start_time) * 1000  # Convert to ms
        
        # Test with 10 concurrent requests
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(route_task, f'test task {i}')
                for i in range(50)
            ]
            
            response_times = [future.result() for future in futures]
        
        # Verify performance under load
        avg_response_time = sum(response_times) / len(response_times)
        max_response_time = max(response_times)
        
        assert avg_response_time < 150  # Average <150ms under load
        assert max_response_time < 500  # Max <500ms under load
```

## Deployment Strategy

### Environment Setup
```bash
# deployment/setup.sh
#!/bin/bash

# Create virtual environment
python -m venv cmd-agent-select-logic-env
source cmd-agent-select-logic-env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup configuration
cp config/config.template.yaml config/config.yaml

# Initialize database for historical data
python scripts/init_database.py

# Run initial tests
python -m pytest tests/ -v

echo "Deployment setup complete"
```

### Configuration Management
```yaml
# config/config.yaml
system:
  name: "cmd-agent-select-logic"
  version: "1.0.0"
  environment: "production"

performance:
  targets:
    simple_task_ms: 50
    standard_task_ms: 100
    complex_task_ms: 200
    cache_hit_rate: 0.8

routing:
  confidence_threshold: 0.4
  escalation_threshold: 0.7
  max_domains: 6

cache:
  l1_ttl_seconds: 3600
  l2_ttl_seconds: 1800
  l3_ttl_seconds: 300
  max_memory_mb: 256

circuit_breaker:
  failure_threshold: 5
  recovery_timeout_seconds: 30
  success_threshold: 3

monitoring:
  enable_performance_tracking: true
  enable_accuracy_tracking: true
  report_interval_minutes: 15
  alert_thresholds:
    response_time_ms: 200
    error_rate_percent: 5
    cache_hit_rate_percent: 70
```

### Health Checks and Monitoring
```python
# src/health/health_check.py
from typing import Dict
import psutil
import time

class HealthCheckService:
    def __init__(self, config):
        self.config = config
        self.start_time = time.time()
    
    def get_health_status(self) -> Dict:
        """Comprehensive health check"""
        
        return {
            'status': self._determine_overall_status(),
            'uptime_seconds': time.time() - self.start_time,
            'system': {
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent
            },
            'performance': self._check_performance_health(),
            'components': {
                'cache_system': self._check_cache_health(),
                'circuit_breaker': self._check_circuit_breaker_health(),
                'learning_system': self._check_learning_system_health()
            }
        }
    
    def _determine_overall_status(self) -> str:
        """Determine overall system health"""
        
        # Check critical components
        if psutil.virtual_memory().percent > 90:
            return 'unhealthy'
        
        if psutil.cpu_percent() > 90:
            return 'degraded'
        
        return 'healthy'
```

This comprehensive implementation guide provides a structured approach to building the @cmd-agent-select-logic system with proper testing, monitoring, and deployment procedures.