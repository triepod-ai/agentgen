# src/routing/router.py
import time
from typing import Dict, List, Optional
from ..core.models import RoutingDecision, RoutingAction, TaskAnalysis
from ..analysis.domain_detector import DomainDetectionEngine

class BasicRoutingEngine:
    def __init__(self):
        self.domain_detector = DomainDetectionEngine()
        
        # High-confidence agent mappings for direct routing
        self.agent_mappings = {
            'frontend': '@build-frontend',
            'backend': '@build-backend', 
            'security': '@security-auditor',
            'infrastructure': '@deploy-application',
            'testing': '@test-automation',
            'documentation': '@generate-documentation'
        }
        
        # Orchestration system selection based on complexity and domain count
        self.orchestration_mappings = {
            'simple': '@orchestrate-tasks',      # Single domain, low complexity
            'standard': '@orchestrate-agents',   # 2-3 domains, medium complexity
            'complex': '@orchestrate-agents-adv' # 4+ domains, high complexity
        }
        
        # Performance tracking
        self.routing_stats = {
            'total_requests': 0,
            'direct_routes': 0,
            'orchestration_routes': 0,
            'escalations': 0,
            'avg_response_time_ms': 0
        }
    
    def route_task(self, task_analysis: TaskAnalysis) -> RoutingDecision:
        """Route task using simple pattern-based logic with improved confidence thresholds"""
        
        start_time = time.perf_counter()
        self.routing_stats['total_requests'] += 1
        
        # Step 1: Analyze domains
        domain_analysis = self.domain_detector.detect_domains(task_analysis.description)
        
        # Step 2: Apply routing decision logic
        routing_decision = self._make_routing_decision(task_analysis, domain_analysis)
        
        # Step 3: Update performance metrics
        analysis_time = (time.perf_counter() - start_time) * 1000
        routing_decision.analysis_time_ms = analysis_time
        self._update_stats(routing_decision, analysis_time)
        
        return routing_decision
    
    def _make_routing_decision(self, task_analysis: TaskAnalysis, domain_analysis: Dict) -> RoutingDecision:
        """Core routing logic with improved thresholds"""
        
        domain_count = domain_analysis['domain_count']
        domains = domain_analysis['domains']
        complexity_score = task_analysis.complexity_score
        
        # Input validation
        if not task_analysis.description.strip():
            return self._create_error_decision("Empty task description provided")
        
        # Decision Path 1: No clear domain detected 
        if domain_count == 0:
            # For simple tasks with no clear domain, try direct routing to orchestrate-tasks
            if complexity_score < 0.4:
                self.routing_stats['direct_routes'] += 1
                return RoutingDecision(
                    action=RoutingAction.DIRECT_AGENT,
                    selected_agent='@orchestrate-tasks',  # Safe default for simple tasks
                    orchestration_type=None,
                    confidence=0.5,
                    reasoning="Simple task with no specific domain - routing to general task orchestrator",
                    analysis_time_ms=0,
                    domain_count=domain_count,
                    complexity_score=complexity_score
                )
            else:
                # Complex tasks with no clear domain should escalate
                self.routing_stats['escalations'] += 1
                return RoutingDecision(
                    action=RoutingAction.ESCALATE,
                    selected_agent=None,
                    orchestration_type=None,
                    confidence=0.3,
                    reasoning="Complex task with no clear domain - requires strategic analysis by @agent-organizer",
                    analysis_time_ms=0,
                    domain_count=domain_count,
                    complexity_score=complexity_score
                )
        
        # Decision Path 2: Single domain with good confidence -> Direct routing
        elif domain_count == 1 and domains[0]['confidence'] >= 0.6:
            primary_domain = domains[0]
            agent = self.agent_mappings.get(primary_domain['domain'], '@orchestrate-tasks')
            
            self.routing_stats['direct_routes'] += 1
            return RoutingDecision(
                action=RoutingAction.DIRECT_AGENT,
                selected_agent=agent,
                orchestration_type=None,
                confidence=primary_domain['confidence'],
                reasoning=f"High-confidence single domain ({primary_domain['domain']}) detected: {primary_domain['confidence']:.2f}",
                analysis_time_ms=0,
                domain_count=domain_count,
                complexity_score=complexity_score
            )
        
        # Decision Path 3: Single domain with lower confidence -> Consider complexity
        elif domain_count == 1 and domains[0]['confidence'] >= 0.3:
            primary_domain = domains[0]
            
            # For complex tasks even with single domain, use orchestration
            if complexity_score >= 0.8:
                orchestration_type = self._select_orchestration_type(domain_count, complexity_score)
                self.routing_stats['orchestration_routes'] += 1
                return RoutingDecision(
                    action=RoutingAction.ORCHESTRATION,
                    selected_agent=None,
                    orchestration_type=orchestration_type,
                    confidence=min(primary_domain['confidence'] * 0.9, 0.8),
                    reasoning=f"Single domain ({primary_domain['domain']}) but high complexity ({complexity_score:.2f}) requires orchestration",
                    analysis_time_ms=0,
                    domain_count=domain_count,
                    complexity_score=complexity_score
                )
            else:
                # Medium confidence, low-medium complexity -> Direct route
                agent = self.agent_mappings.get(primary_domain['domain'], '@orchestrate-tasks')
                self.routing_stats['direct_routes'] += 1
                return RoutingDecision(
                    action=RoutingAction.DIRECT_AGENT,
                    selected_agent=agent,
                    orchestration_type=None,
                    confidence=primary_domain['confidence'],
                    reasoning=f"Medium-confidence single domain ({primary_domain['domain']}): {primary_domain['confidence']:.2f}",
                    analysis_time_ms=0,
                    domain_count=domain_count,
                    complexity_score=complexity_score
                )
        
        # Decision Path 4: Multiple domains -> Orchestration
        elif domain_count >= 2:
            orchestration_type = self._select_orchestration_type(domain_count, complexity_score)
            average_confidence = sum(d['confidence'] for d in domains) / len(domains)
            
            self.routing_stats['orchestration_routes'] += 1
            return RoutingDecision(
                action=RoutingAction.ORCHESTRATION,
                selected_agent=None,
                orchestration_type=orchestration_type,
                confidence=min(average_confidence, 0.85),
                reasoning=f"Multiple domains ({domain_count}) require coordination: {[d['domain'] for d in domains[:3]]}",
                analysis_time_ms=0,
                domain_count=domain_count,
                complexity_score=complexity_score
            )
        
        # Decision Path 5: Very low confidence -> Use orchestrate-tasks as safe default
        else:
            self.routing_stats['direct_routes'] += 1
            return RoutingDecision(
                action=RoutingAction.DIRECT_AGENT,
                selected_agent='@orchestrate-tasks',  # Safe default
                orchestration_type=None,
                confidence=0.4,
                reasoning=f"Low domain confidence - using general task orchestrator as safe default",
                analysis_time_ms=0,
                domain_count=domain_count,
                complexity_score=complexity_score
            )
    
    def _select_orchestration_type(self, domain_count: int, complexity_score: float) -> str:
        """Select appropriate orchestration system based on complexity and domain count"""
        
        # Priority: complexity > domain count
        if complexity_score >= 0.8 or domain_count >= 4:
            return '@orchestrate-agents-adv'
        elif domain_count >= 2 or complexity_score >= 0.5:
            return '@orchestrate-agents'
        else:
            return '@orchestrate-tasks'
    
    def _create_error_decision(self, error_message: str) -> RoutingDecision:
        """Create a fallback routing decision for error cases"""
        
        return RoutingDecision(
            action=RoutingAction.DIRECT_AGENT,  # Changed from ESCALATE to safer direct routing
            selected_agent='@orchestrate-tasks',  # Safe fallback
            orchestration_type=None,
            confidence=0.3,
            reasoning=f"Error in routing: {error_message}",
            analysis_time_ms=0,
            domain_count=0,
            complexity_score=0.0
        )
    
    def _update_stats(self, decision: RoutingDecision, analysis_time_ms: float):
        """Update routing performance statistics"""
        
        # Update rolling average response time
        current_avg = self.routing_stats['avg_response_time_ms']
        total_requests = self.routing_stats['total_requests']
        
        new_avg = ((current_avg * (total_requests - 1)) + analysis_time_ms) / total_requests
        self.routing_stats['avg_response_time_ms'] = new_avg
    
    def get_routing_stats(self) -> Dict:
        """Get current routing performance statistics"""
        
        total = self.routing_stats['total_requests']
        if total == 0:
            return self.routing_stats.copy()
        
        stats = self.routing_stats.copy()
        stats.update({
            'direct_route_percentage': (self.routing_stats['direct_routes'] / total) * 100,
            'orchestration_percentage': (self.routing_stats['orchestration_routes'] / total) * 100,
            'escalation_percentage': (self.routing_stats['escalations'] / total) * 100
        })
        
        return stats

class RoutingValidator:
    """Input validation and error handling for routing requests"""
    
    @staticmethod
    def validate_task_description(description: str) -> tuple[bool, str]:
        """Validate task description input"""
        
        if not isinstance(description, str):
            return False, "Task description must be a string"
        
        if not description.strip():
            return False, "Task description cannot be empty"
        
        if len(description) > 2000:  # Reasonable limit
            return False, "Task description too long (max 2000 characters)"
        
        # Check for potential security issues
        suspicious_patterns = ['eval(', 'exec(', '__import__', 'subprocess']
        if any(pattern in description.lower() for pattern in suspicious_patterns):
            return False, "Task description contains potentially unsafe content"
        
        return True, "Valid"
    
    @staticmethod
    def sanitize_input(description: str) -> str:
        """Basic input sanitization"""
        
        if not isinstance(description, str):
            description = str(description)
        
        # Basic cleanup
        description = description.strip()
        description = ' '.join(description.split())  # Normalize whitespace
        
        return description