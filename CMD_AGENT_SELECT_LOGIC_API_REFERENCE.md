# CMD Agent Select Logic - API Reference

## Overview

This document provides comprehensive API reference for the @cmd-agent-select-logic agent, including input/output formats, confidence scoring breakdown, escalation triggers, and routing decision matrices.

## API Endpoints

### Primary Interface

#### `analyze_and_route(task_description: str) -> RoutingDecision`

**Purpose**: Main entry point for intelligent agent selection and routing.

**Input Format**:
```python
{
    "task_description": str,      # Required: Natural language task description
    "context": {                  # Optional: Additional context
        "project_type": str,      # e.g., "web_app", "api", "mobile"
        "urgency": str,          # "low", "normal", "high", "critical"  
        "complexity_hint": str,   # "simple", "standard", "complex"
        "preferred_agents": list, # List of preferred agent names
        "resource_constraints": {
            "max_tokens": int,    # Token budget limit
            "time_limit": int,    # Time constraint in seconds
            "concurrent_limit": int # Max concurrent agents
        }
    },
    "performance_mode": str       # Optional: "fast", "balanced", "thorough"
}
```

**Output Format**:
```python
{
    "routing_decision": {
        "action": str,           # "DIRECT_AGENT_ROUTING" | "ORCHESTRATION_ROUTING" | "ESCALATE_TO_ORGANIZER"
        "selected_agent": str,   # Agent name (for direct routing)
        "orchestration_type": str, # "tasks" | "agents" | "agents-adv" (for orchestration)
        "confidence": float,     # 0.0-1.0 confidence score
        "reasoning": str         # Human-readable explanation
    },
    
    "analysis_results": {
        "complexity_score": float,        # 0.0-1.0 complexity assessment
        "complexity_classification": str, # "SIMPLE" | "STANDARD" | "COMPLEX"
        "domains": [                     # List of detected domains
            {
                "domain": str,           # Domain name
                "confidence": float,     # Domain detection confidence
                "complexity_bias": float, # Domain-specific complexity adjustment
                "preferred_agents": list  # Recommended agents for domain
            }
        ],
        "domain_count": int,            # Number of detected domains
        "total_domain_confidence": float # Aggregate domain confidence
    },
    
    "performance_metrics": {
        "analysis_time_ms": float,      # Total analysis time
        "cache_hit": bool,              # Whether cache was used
        "decision_path": str,           # Which decision path was taken
        "circuit_breaker_state": str    # "CLOSED" | "OPEN" | "HALF_OPEN"
    },
    
    "confidence_breakdown": {
        "pattern_match": float,         # Pattern matching confidence (0.0-1.0)
        "historical_success": float,    # Historical success rate (0.0-1.0)
        "context_completeness": float,  # Context adequacy score (0.0-1.0)
        "resource_availability": float  # Resource availability score (0.0-1.0)
    },
    
    "escalation_info": {               # Present if action == "ESCALATE_TO_ORGANIZER"
        "escalation_score": float,     # 0.0-1.0 escalation necessity score
        "triggered_conditions": list,  # List of escalation triggers
        "context_package": dict        # Enhanced context for @agent-organizer
    }
}
```

## Confidence Scoring System

### Overall Confidence Formula

```python
total_confidence = (
    pattern_matching_confidence * 0.4 +
    historical_success_rate * 0.3 +
    context_completeness_score * 0.2 +
    resource_availability_score * 0.1
)
```

### Pattern Matching Confidence

**Range**: 0.0 - 1.0  
**Weight**: 40% of total confidence

**Calculation Method**:
```python
def calculate_pattern_confidence(task_description: str, agent_capabilities: dict) -> float:
    """
    Calculate semantic similarity between task and agent capabilities.
    Uses TF-IDF vectorization and cosine similarity.
    """
    
    # Preprocessing
    task_vector = vectorize_text(task_description)
    
    max_similarity = 0.0
    for agent_name, capabilities in agent_capabilities.items():
        capability_vector = vectorize_text(capabilities['description'])
        similarity = cosine_similarity(task_vector, capability_vector)
        max_similarity = max(max_similarity, similarity)
    
    return min(max_similarity, 0.95)  # Cap at 95%
```

**Confidence Levels**:
- **0.9 - 1.0**: Excellent match, high certainty
- **0.7 - 0.89**: Good match, confident selection
- **0.5 - 0.69**: Moderate match, acceptable confidence
- **0.3 - 0.49**: Poor match, low confidence
- **0.0 - 0.29**: Very poor match, escalation likely

### Historical Success Rate

**Range**: 0.0 - 1.0  
**Weight**: 30% of total confidence

**Calculation Method**:
```python
def calculate_historical_confidence(task_signature: str) -> float:
    """
    Calculate confidence based on historical success rates for similar tasks.
    """
    
    # Generate task signature
    signature = generate_task_signature(task_signature)
    
    # Look up historical data
    historical_data = get_historical_performance(signature)
    
    if not historical_data:
        return 0.5  # Default neutral confidence
    
    # Calculate weighted success rate (more recent data has higher weight)
    weighted_success_rate = calculate_weighted_average(
        historical_data['success_rates'],
        historical_data['timestamps'],
        decay_factor=0.1  # 10% decay per day
    )
    
    return weighted_success_rate
```

**Data Sources**:
- Task completion success rates
- User satisfaction scores  
- Agent performance metrics
- Error rates and failure patterns

### Context Completeness Score

**Range**: 0.0 - 1.0  
**Weight**: 20% of total confidence

**Assessment Criteria**:
```python
def assess_context_completeness(task_description: str) -> float:
    """
    Assess how complete the task description is for routing decisions.
    """
    
    completeness_factors = {
        'has_clear_objective': check_clear_objective(task_description) * 0.3,
        'specifies_technology': check_technology_stack(task_description) * 0.2,
        'includes_constraints': check_constraints(task_description) * 0.2,
        'provides_context': check_context_information(task_description) * 0.15,
        'defines_success_criteria': check_success_criteria(task_description) * 0.15
    }
    
    return sum(completeness_factors.values())
```

**Completeness Factors**:
- **Clear Objective** (30%): Task has well-defined goal
- **Technology Stack** (20%): Mentions specific technologies/frameworks
- **Constraints** (20%): Includes time, resource, or quality constraints
- **Context** (15%): Provides background or situational context
- **Success Criteria** (15%): Defines what success looks like

### Resource Availability Score

**Range**: 0.0 - 1.0  
**Weight**: 10% of total confidence

**Assessment Method**:
```python
def assess_resource_availability(estimated_resources: dict) -> float:
    """
    Assess system resource availability for task execution.
    """
    
    current_resources = get_current_system_resources()
    
    availability_factors = {
        'token_availability': min(
            current_resources['available_tokens'] / estimated_resources['required_tokens'],
            1.0
        ) * 0.4,
        
        'agent_availability': (
            current_resources['available_agents'] / estimated_resources['required_agents']
        ) * 0.3,
        
        'system_load': (1.0 - current_resources['cpu_usage']) * 0.2,
        
        'memory_availability': (
            current_resources['available_memory'] / estimated_resources['required_memory']
        ) * 0.1
    }
    
    return min(sum(availability_factors.values()), 1.0)
```

## Escalation Trigger Conditions

### Primary Escalation Triggers

```python
escalation_triggers = {
    'low_confidence': {
        'threshold': 0.4,
        'description': 'Overall routing confidence below 40%',
        'weight': 0.35
    },
    
    'high_complexity': {
        'threshold': 0.8,
        'description': 'Task complexity score above 80%',
        'weight': 0.25
    },
    
    'multi_domain': {
        'threshold': 3,
        'description': 'More than 3 domains detected',
        'weight': 0.15
    },
    
    'enterprise_scope': {
        'keywords': ['enterprise', 'platform', 'system-wide', 'strategic'],
        'description': 'Enterprise-level scope indicators detected',
        'weight': 0.10
    },
    
    'architectural_decisions': {
        'keywords': ['architecture', 'design', 'framework', 'patterns'],
        'description': 'Architectural decision-making required',
        'weight': 0.10
    },
    
    'ambiguous_requirements': {
        'threshold': 0.6,
        'description': 'Requirements ambiguity score above 60%',
        'weight': 0.05
    }
}
```

### Escalation Score Formula

```python
escalation_score = (
    (1.0 - overall_confidence) * 0.35 +
    complexity_score * 0.25 +
    min(domain_count / 5.0, 1.0) * 0.15 +
    enterprise_indicator * 0.10 +
    architectural_indicator * 0.10 +
    ambiguity_score * 0.05
)
```

### Escalation Decision Matrix

| Escalation Score | Domain Count | Confidence | Action | Routing Target |
|-----------------|--------------|------------|---------|----------------|
| ≥ 0.7 | Any | Any | ESCALATE | @agent-organizer |
| 0.4 - 0.69 | ≥ 4 | Any | ESCALATE | @agent-organizer |
| 0.4 - 0.69 | 2-3 | ≥ 0.6 | ORCHESTRATE | @orchestrate-agents |
| 0.4 - 0.69 | 2-3 | < 0.6 | ESCALATE | @agent-organizer |
| < 0.4 | 1 | ≥ 0.8 | DIRECT | Best matching agent |
| < 0.4 | 1 | 0.6-0.79 | ORCHESTRATE | @orchestrate-tasks |
| < 0.4 | 1 | < 0.6 | ESCALATE | @agent-organizer |

## Routing Decision Matrix

### Direct Agent Routing Patterns

**High-Confidence Routes** (Confidence ≥ 0.8):
```yaml
screenshot_analysis:
  patterns: ["analyze screenshot", "extract from image", "visual analysis"]
  target: "@analyze-screenshot"
  confidence_boost: 0.1

debugging_tasks:
  patterns: ["debug", "troubleshoot", "fix error", "investigate bug"]
  target: "@debugger"  
  confidence_boost: 0.05

test_automation:
  patterns: ["create test", "automate testing", "test coverage"]
  target: "@test-automator"
  confidence_boost: 0.08

code_review:
  patterns: ["review code", "code quality", "audit code"]
  target: "@code-reviewer"
  confidence_boost: 0.06

deployment:
  patterns: ["deploy", "deployment", "release", "publish"]
  target: "@deployment-engineer"
  confidence_boost: 0.07

documentation:
  patterns: ["document", "create docs", "write guide", "api docs"]
  target: "@documentation-expert"
  confidence_boost: 0.05

architecture:
  patterns: ["system design", "architecture", "design patterns"]
  target: "@architect-specialist"
  confidence_boost: 0.12

security_audit:
  patterns: ["security audit", "vulnerability scan", "security review"]
  target: "@security-auditor"
  confidence_boost: 0.10

performance:
  patterns: ["optimize", "performance", "speed up", "bottleneck"]
  target: "@performance-engineer"
  confidence_boost: 0.09
```

### Pattern-Based Routing Rules

**Frontend Development**:
```yaml
react_development:
  patterns: ["build react", "create component", "react app"]
  conditions:
    - domain: "frontend"
    - confidence: ≥ 0.7
  targets:
    primary: "@build-frontend"
    alternatives: ["@frontend-developer", "@react-specialist"]

ui_design:
  patterns: ["design ui", "user interface", "responsive design"]
  conditions:
    - domain: "frontend"
    - keywords: ["design", "ui", "ux"]
  targets:
    primary: "@ui-designer"
    alternatives: ["@frontend-developer"]
```

**Backend Development**:
```yaml
api_development:
  patterns: ["build api", "create endpoint", "rest api", "graphql"]
  conditions:
    - domain: "backend"
    - confidence: ≥ 0.7
  targets:
    primary: "@build-backend"
    alternatives: ["@full-stack-developer", "@api-specialist"]

database_work:
  patterns: ["database", "sql", "query", "schema"]
  conditions:
    - domain: "backend"
    - keywords: ["database", "sql", "nosql"]
  targets:
    primary: "@database-specialist"
    alternatives: ["@build-backend"]
```

### Orchestration Routing Logic

```python
def determine_orchestration_type(domain_count: int, complexity_score: float) -> str:
    """
    Select appropriate orchestration system based on task characteristics.
    """
    
    if domain_count >= 4 or complexity_score > 0.8:
        return "@orchestrate-agents-adv"  # Enterprise coordination
    elif domain_count >= 2 or complexity_score > 0.5:
        return "@orchestrate-agents"      # Standard coordination  
    else:
        return "@orchestrate-tasks"       # Intelligent analysis
```

**Orchestration Selection Matrix**:

| Domain Count | Complexity Score | Orchestration Type | Reasoning |
|--------------|------------------|-------------------|-----------|
| 1 | < 0.5 | @orchestrate-tasks | Simple analysis needed |
| 1 | 0.5-0.8 | @orchestrate-tasks | Single domain, moderate complexity |
| 1 | > 0.8 | @orchestrate-agents | High complexity requires coordination |
| 2-3 | < 0.5 | @orchestrate-agents | Multi-domain coordination |
| 2-3 | 0.5-0.8 | @orchestrate-agents | Standard multi-domain work |
| 2-3 | > 0.8 | @orchestrate-agents-adv | Complex multi-domain |
| ≥ 4 | Any | @orchestrate-agents-adv | Enterprise-level coordination |

## Domain Detection API

### Domain Signatures

```python
domain_signatures = {
    'frontend': {
        'keywords': {
            'primary': ['react', 'vue', 'angular', 'frontend', 'ui', 'component'],
            'secondary': ['css', 'responsive', 'styling', 'layout', 'design'],
            'frameworks': ['nextjs', 'nuxt', 'svelte', 'gatsby'],
            'tools': ['webpack', 'vite', 'parcel', 'rollup']
        },
        'file_patterns': [
            r'.*\.(jsx|tsx|vue|svelte)$',
            r'.*\.(css|scss|sass|less|styl)$',
            r'components?/.*',
            r'pages?/.*'
        ],
        'operations': ['create', 'build', 'style', 'implement', 'design'],
        'complexity_bias': 0.7,
        'confidence_threshold': 0.3
    },
    
    'backend': {
        'keywords': {
            'primary': ['api', 'server', 'backend', 'database', 'endpoint'],
            'secondary': ['nodejs', 'python', 'java', 'go', 'rust'],
            'frameworks': ['express', 'fastapi', 'spring', 'gin', 'actix'],
            'databases': ['mysql', 'postgresql', 'mongodb', 'redis']
        },
        'file_patterns': [
            r'.*\.(js|py|go|java|rs)$',
            r'controllers?/.*',
            r'models?/.*',
            r'api/.*'
        ],
        'operations': ['implement', 'create', 'build', 'secure'],
        'complexity_bias': 0.8,
        'confidence_threshold': 0.3
    },
    
    'security': {
        'keywords': {
            'primary': ['security', 'auth', 'vulnerability', 'audit', 'encrypt'],
            'secondary': ['compliance', 'privacy', 'oauth', 'jwt', 'ssl'],
            'threats': ['xss', 'csrf', 'injection', 'breach', 'attack'],
            'standards': ['owasp', 'pci', 'gdpr', 'hipaa']
        },
        'file_patterns': [
            r'.*auth.*',
            r'.*security.*',
            r'.*\.(pem|key|crt)$',
            r'config/security.*'
        ],
        'operations': ['scan', 'audit', 'secure', 'harden', 'encrypt'],
        'complexity_bias': 0.9,
        'confidence_threshold': 0.3
    },
    
    'infrastructure': {
        'keywords': {
            'primary': ['deploy', 'docker', 'k8s', 'cloud', 'ci/cd', 'devops'],
            'secondary': ['aws', 'azure', 'gcp', 'terraform', 'ansible'],
            'tools': ['jenkins', 'github-actions', 'gitlab-ci', 'circleci'],
            'containers': ['kubernetes', 'docker-compose', 'helm']
        },
        'file_patterns': [
            r'Dockerfile.*',
            r'.*\.ya?ml$',
            r'\.github/.*',
            r'terraform/.*'
        ],
        'operations': ['deploy', 'configure', 'setup', 'automate'],
        'complexity_bias': 0.8,
        'confidence_threshold': 0.3
    },
    
    'documentation': {
        'keywords': {
            'primary': ['document', 'readme', 'guide', 'docs', 'wiki'],
            'secondary': ['tutorial', 'manual', 'specification', 'api-docs'],
            'formats': ['markdown', 'rst', 'confluence', 'notion'],
            'types': ['user-guide', 'technical-docs', 'api-reference']
        },
        'file_patterns': [
            r'.*\.md$',
            r'.*\.rst$',
            r'docs?/.*',
            r'README.*'
        ],
        'operations': ['write', 'create', 'update', 'generate'],
        'complexity_bias': 0.4,
        'confidence_threshold': 0.3
    },
    
    'testing': {
        'keywords': {
            'primary': ['test', 'qa', 'validation', 'coverage', 'spec'],
            'secondary': ['unit-test', 'integration', 'e2e', 'performance'],
            'frameworks': ['jest', 'mocha', 'pytest', 'junit', 'cypress'],
            'types': ['smoke', 'regression', 'load', 'security']
        },
        'file_patterns': [
            r'.*\.test\.(js|ts|py)$',
            r'.*\.spec\.(js|ts|py)$',
            r'tests?/.*',
            r'__tests__/.*'
        ],
        'operations': ['test', 'validate', 'verify', 'check'],
        'complexity_bias': 0.6,
        'confidence_threshold': 0.3
    }
}
```

### Domain Confidence Calculation

```python
def calculate_domain_confidence(task_description: str, domain_signature: dict) -> float:
    """
    Calculate confidence score for domain detection.
    """
    
    # Tokenize and normalize task description
    tokens = preprocess_text(task_description.lower())
    
    # Keyword matching with different weights
    keyword_scores = {
        'primary': count_keyword_matches(tokens, domain_signature['keywords']['primary']) * 0.4,
        'secondary': count_keyword_matches(tokens, domain_signature['keywords']['secondary']) * 0.2,
        'frameworks': count_keyword_matches(tokens, domain_signature['keywords'].get('frameworks', [])) * 0.15,
        'tools': count_keyword_matches(tokens, domain_signature['keywords'].get('tools', [])) * 0.1
    }
    
    # File pattern matching
    file_pattern_score = check_file_patterns(task_description, domain_signature['file_patterns']) * 0.1
    
    # Operation matching  
    operation_score = count_keyword_matches(tokens, domain_signature['operations']) * 0.05
    
    # Calculate total confidence
    total_confidence = sum(keyword_scores.values()) + file_pattern_score + operation_score
    
    # Apply domain-specific adjustments
    if total_confidence > domain_signature['confidence_threshold']:
        # Boost confidence for strong matches
        total_confidence = min(total_confidence * 1.2, 0.95)
    
    return total_confidence
```

## Performance Monitoring API

### Metrics Collection

```python
performance_metrics = {
    'routing_performance': {
        'avg_decision_time_ms': float,      # Average routing decision time
        'p95_decision_time_ms': float,      # 95th percentile decision time
        'p99_decision_time_ms': float,      # 99th percentile decision time
        'cache_hit_rate': float,            # Percentage of cache hits
        'decisions_per_minute': float       # Throughput metric
    },
    
    'routing_accuracy': {
        'direct_routing_success_rate': float,    # Success rate for direct routing
        'orchestration_success_rate': float,     # Success rate for orchestration
        'escalation_appropriateness': float,     # Percentage of appropriate escalations
        'user_satisfaction_score': float        # User satisfaction (0-1 scale)
    },
    
    'system_health': {
        'circuit_breaker_state': str,           # CLOSED | OPEN | HALF_OPEN
        'error_rate': float,                    # Percentage of routing errors
        'escalation_rate': float,               # Percentage of tasks escalated
        'resource_utilization': float          # System resource usage
    },
    
    'domain_detection': {
        'detection_accuracy': float,            # Domain detection accuracy
        'false_positive_rate': float,           # Incorrect domain detections
        'multi_domain_accuracy': float         # Accuracy for multi-domain tasks
    }
}
```

### Health Check API

```python
def get_system_health() -> dict:
    """
    Return comprehensive system health status.
    """
    
    return {
        'status': 'healthy' | 'degraded' | 'unhealthy',
        'performance': {
            'avg_response_time_ms': float,
            'cache_performance': {
                'l1_hit_rate': float,
                'l2_hit_rate': float, 
                'l3_hit_rate': float
            },
            'throughput_rpm': float
        },
        'reliability': {
            'uptime_percentage': float,
            'error_rate': float,
            'circuit_breaker_trips': int
        },
        'resource_usage': {
            'memory_usage_mb': float,
            'cpu_usage_percent': float,
            'token_usage_percent': float
        },
        'recommendations': list  # List of optimization recommendations
    }
```

## Error Codes and Responses

### Standard Error Responses

```python
error_responses = {
    'ROUTING_001': {
        'message': 'Invalid task description format',
        'status': 'error',
        'action': 'user_clarification',
        'recommendation': 'Provide a clear, descriptive task description'
    },
    
    'ROUTING_002': {
        'message': 'No suitable agent found',
        'status': 'error',
        'action': 'escalate_to_organizer',
        'recommendation': 'Task requires strategic analysis'
    },
    
    'ROUTING_003': {
        'message': 'System overload - circuit breaker activated',
        'status': 'degraded',
        'action': 'fallback_routing',
        'recommendation': 'Retry after system recovery'
    },
    
    'ROUTING_004': {
        'message': 'Domain detection timeout',
        'status': 'warning',
        'action': 'use_cached_analysis',
        'recommendation': 'Analysis completed with reduced accuracy'
    },
    
    'ROUTING_005': {
        'message': 'Confidence threshold not met',
        'status': 'warning',
        'action': 'escalate_to_organizer',
        'recommendation': 'Strategic analysis recommended'
    }
}
```

## Integration Specifications

### Agent Organizer Context Package

```python
context_package_schema = {
    'routing_metadata': {
        'escalation_timestamp': float,
        'escalation_reason': str,
        'routing_agent_version': str
    },
    
    'task_analysis': {
        'original_request': str,
        'complexity_score': float,
        'complexity_factors': dict,
        'estimated_effort_hours': float,
        'risk_assessment': dict
    },
    
    'domain_intelligence': {
        'detected_domains': list,
        'domain_interactions': dict,
        'recommended_specialists': list
    },
    
    'confidence_intelligence': {
        'routing_confidence': float,
        'confidence_breakdown': dict,
        'uncertainty_factors': list
    },
    
    'system_context': {
        'available_agents': list,
        'resource_constraints': dict,
        'performance_requirements': dict
    },
    
    'strategic_recommendations': {
        'suggested_approach': str,
        'team_composition': list,
        'execution_sequence': list,
        'success_criteria': dict
    }
}
```

This comprehensive API reference provides all necessary specifications for integrating with and extending the @cmd-agent-select-logic system.