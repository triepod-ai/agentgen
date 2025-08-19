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
    analysis_time_ms: float = 0.0
    
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
    cache_hit: bool = False
    complexity_score: float = 0.0
    domain_count: int = 0