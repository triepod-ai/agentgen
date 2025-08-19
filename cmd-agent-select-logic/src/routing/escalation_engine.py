# src/routing/escalation_engine.py
import time
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class EscalationAction(Enum):
    """Escalation decision outcomes"""
    DIRECT_AGENT_ROUTING = "DIRECT_AGENT_ROUTING"
    ORCHESTRATION_ROUTING = "ORCHESTRATION_ROUTING" 
    ESCALATE_TO_ORGANIZER = "ESCALATE_TO_ORGANIZER"

@dataclass
class EscalationTriggers:
    """Escalation trigger analysis results"""
    low_confidence: bool
    high_complexity: bool
    multi_domain: bool
    enterprise_scope: bool
    architectural_decisions: bool
    ambiguous_requirements: bool

@dataclass
class EscalationDecision:
    """Complete escalation decision with context"""
    action: EscalationAction
    reason: str
    confidence: float
    escalation_score: float
    triggers: List[str]
    recommended_agent: Optional[str]
    context_package: Optional[Dict]

class OrganizeContextPackage:
    """Context package builder for @agent-organizer handoff"""
    
    @staticmethod
    def create_context_package(task_description: str, 
                             task_analysis: Dict,
                             domain_analysis: Dict,
                             confidence_analysis: Dict,
                             available_agents: List[str],
                             escalation_triggers: EscalationTriggers) -> Dict:
        """Build comprehensive context package for strategic analysis"""
        
        return {
            'original_request': task_description,
            'routing_analysis': {
                'complexity_score': task_analysis.get('complexity_score', 0.5),
                'complexity_level': task_analysis.get('complexity_level', 'STANDARD'),
                'domains_detected': domain_analysis.get('domains', []),
                'primary_domain': domain_analysis.get('primary_domain'),
                'domain_count': domain_analysis.get('domain_count', 0),
                'confidence_breakdown': {
                    'total_confidence': confidence_analysis.get('total_confidence', 0.5),
                    'pattern_match': confidence_analysis.get('pattern_match', 0.5),
                    'historical_success': confidence_analysis.get('historical_success', 0.5),
                    'context_completeness': confidence_analysis.get('context_completeness', 0.5),
                    'resource_availability': confidence_analysis.get('resource_availability', 0.5)
                },
                'escalation_triggers': OrganizeContextPackage._extract_trigger_names(escalation_triggers)
            },
            'system_context': {
                'available_agents': available_agents,
                'agent_count': len(available_agents),
                'resource_constraints': OrganizeContextPackage._assess_resource_constraints(),
                'performance_requirements': OrganizeContextPackage._estimate_performance_needs(task_analysis)
            },
            'strategic_requirements': {
                'requires_enterprise_coordination': escalation_triggers.enterprise_scope,
                'requires_architectural_design': escalation_triggers.architectural_decisions,
                'requires_multi_domain_expertise': escalation_triggers.multi_domain,
                'complexity_management_needed': escalation_triggers.high_complexity
            },
            'expected_deliverable': 'Strategic analysis with agent team recommendations and execution plan',
            'escalation_timestamp': time.time(),
            'escalation_reason': OrganizeContextPackage._generate_escalation_reason(escalation_triggers)
        }
    
    @staticmethod
    def _extract_trigger_names(triggers: EscalationTriggers) -> List[str]:
        """Extract names of active triggers"""
        active_triggers = []
        if triggers.low_confidence:
            active_triggers.append('low_confidence')
        if triggers.high_complexity:
            active_triggers.append('high_complexity') 
        if triggers.multi_domain:
            active_triggers.append('multi_domain')
        if triggers.enterprise_scope:
            active_triggers.append('enterprise_scope')
        if triggers.architectural_decisions:
            active_triggers.append('architectural_decisions')
        if triggers.ambiguous_requirements:
            active_triggers.append('ambiguous_requirements')
        return active_triggers
    
    @staticmethod
    def _assess_resource_constraints() -> Dict:
        """Assess current system resource constraints"""
        return {
            'token_usage_high': False,  # Would integrate with actual monitoring
            'system_load_high': False,
            'concurrent_operations': 0,
            'resource_availability': 'normal'
        }
    
    @staticmethod
    def _estimate_performance_needs(task_analysis: Dict) -> Dict:
        """Estimate performance requirements for task"""
        complexity = task_analysis.get('complexity_score', 0.5)
        
        return {
            'estimated_duration_minutes': int(complexity * 30),
            'estimated_token_usage': int(complexity * 20000),
            'requires_parallel_processing': complexity > 0.7,
            'requires_specialized_agents': complexity > 0.6
        }
    
    @staticmethod
    def _generate_escalation_reason(triggers: EscalationTriggers) -> str:
        """Generate human-readable escalation reason"""
        reasons = []
        
        if triggers.enterprise_scope:
            reasons.append("enterprise-scale requirements")
        if triggers.architectural_decisions:
            reasons.append("architectural decision-making needed")
        if triggers.high_complexity:
            reasons.append("high complexity requiring strategic approach")
        if triggers.multi_domain:
            reasons.append("multi-domain coordination required")
        if triggers.low_confidence:
            reasons.append("low confidence in automated routing")
        if triggers.ambiguous_requirements:
            reasons.append("ambiguous requirements requiring clarification")
        
        return f"Strategic analysis required due to: {', '.join(reasons)}"

class StrategicEscalationEngine:
    """Research-based escalation decision engine with @agent-organizer integration"""
    
    def __init__(self):
        self.enterprise_keywords = {
            'scale_indicators': ['enterprise', 'large-scale', 'system-wide', 'comprehensive', 
                               'platform', 'organization', 'company-wide'],
            'strategic_indicators': ['strategy', 'roadmap', 'architecture', 'modernization',
                                   'transformation', 'migration', 'overhaul'],
            'coordination_indicators': ['coordinate', 'orchestrate', 'manage', 'govern',
                                      'standardize', 'centralize']
        }
        
        self.architectural_keywords = {
            'design_patterns': ['architecture', 'design', 'pattern', 'framework', 'structure'],
            'system_design': ['scalability', 'performance', 'reliability', 'availability',
                            'consistency', 'partition', 'distributed'],
            'decision_keywords': ['choose', 'select', 'decide', 'recommend', 'evaluate',
                                'compare', 'assess', 'analyze']
        }
        
        self.ambiguity_patterns = [
            r'\b(maybe|perhaps|might|could|should)\b',
            r'\b(not sure|unclear|vague|ambiguous)\b',
            r'\?.*\?',  # Multiple question marks
            r'\b(what|how|which|where|when|why)\b.*\b(what|how|which|where|when|why)\b'  # Multiple questions
        ]
    
    def analyze_escalation_triggers(self, task_description: str,
                                  complexity_score: float,
                                  domain_analysis: Dict,
                                  confidence_analysis: Dict) -> EscalationTriggers:
        """Analyze all escalation trigger conditions"""
        
        task_lower = task_description.lower()
        
        # Trigger 1: Low confidence (<0.4)
        low_confidence = confidence_analysis.get('total_confidence', 0.5) < 0.4
        
        # Trigger 2: High complexity (>0.8)
        high_complexity = complexity_score > 0.8
        
        # Trigger 3: Multi-domain (>3 domains)
        multi_domain = domain_analysis.get('domain_count', 0) > 3
        
        # Trigger 4: Enterprise scope
        enterprise_scope = self._check_enterprise_indicators(task_lower)
        
        # Trigger 5: Architectural decisions
        architectural_decisions = self._check_architectural_keywords(task_lower)
        
        # Trigger 6: Ambiguous requirements
        ambiguous_requirements = self._assess_requirement_ambiguity(task_description)
        
        return EscalationTriggers(
            low_confidence=low_confidence,
            high_complexity=high_complexity,
            multi_domain=multi_domain,
            enterprise_scope=enterprise_scope,
            architectural_decisions=architectural_decisions,
            ambiguous_requirements=ambiguous_requirements
        )
    
    def _check_enterprise_indicators(self, task_description: str) -> bool:
        """Check for enterprise-scale indicators"""
        
        for category, keywords in self.enterprise_keywords.items():
            if any(keyword in task_description for keyword in keywords):
                return True
        return False
    
    def _check_architectural_keywords(self, task_description: str) -> bool:
        """Check for architectural decision keywords"""
        
        design_matches = sum(1 for keyword in self.architectural_keywords['design_patterns']
                           if keyword in task_description)
        system_matches = sum(1 for keyword in self.architectural_keywords['system_design']
                           if keyword in task_description)
        decision_matches = sum(1 for keyword in self.architectural_keywords['decision_keywords']
                             if keyword in task_description)
        
        # Architectural indicators if multiple categories match
        return (design_matches > 0 and system_matches > 0) or decision_matches > 1
    
    def _assess_requirement_ambiguity(self, task_description: str) -> bool:
        """Assess if requirements are ambiguous"""
        
        ambiguity_score = 0
        for pattern in self.ambiguity_patterns:
            matches = len(re.findall(pattern, task_description, re.IGNORECASE))
            ambiguity_score += matches
        
        # Consider ambiguous if multiple ambiguity patterns detected
        return ambiguity_score > 2
    
    def calculate_escalation_score(self, complexity_score: float,
                                 domain_analysis: Dict,
                                 confidence_analysis: Dict,
                                 escalation_triggers: EscalationTriggers) -> float:
        """Calculate research-based escalation score"""
        
        # Research-based escalation formula
        escalation_score = (
            (1.0 - confidence_analysis.get('total_confidence', 0.5)) * 0.4 +
            complexity_score * 0.3 +
            (domain_analysis.get('domain_count', 0) / 5.0) * 0.2 +
            (1.0 if escalation_triggers.ambiguous_requirements else 0.0) * 0.1
        )
        
        # Bonus escalation for specific triggers
        if escalation_triggers.enterprise_scope:
            escalation_score += 0.2
        if escalation_triggers.architectural_decisions:
            escalation_score += 0.15
        
        return min(escalation_score, 1.0)
    
    def make_escalation_decision(self, task_description: str,
                               task_analysis: Dict,
                               domain_analysis: Dict,
                               confidence_analysis: Dict,
                               available_agents: List[str]) -> EscalationDecision:
        """Make comprehensive escalation decision with context"""
        
        complexity_score = task_analysis.get('complexity_score', 0.5)
        
        # Analyze escalation triggers
        triggers = self.analyze_escalation_triggers(
            task_description, complexity_score, domain_analysis, confidence_analysis
        )
        
        # Calculate escalation score
        escalation_score = self.calculate_escalation_score(
            complexity_score, domain_analysis, confidence_analysis, triggers
        )
        
        # Make decision based on research-based thresholds
        if escalation_score > 0.7 or triggers.enterprise_scope:
            return EscalationDecision(
                action=EscalationAction.ESCALATE_TO_ORGANIZER,
                reason="Strategic analysis required",
                confidence=escalation_score,
                escalation_score=escalation_score,
                triggers=OrganizeContextPackage._extract_trigger_names(triggers),
                recommended_agent="@agent-organizer",
                context_package=OrganizeContextPackage.create_context_package(
                    task_description, task_analysis, domain_analysis, 
                    confidence_analysis, available_agents, triggers
                )
            )
        
        elif (domain_analysis.get('domain_count', 0) >= 2 and 
              confidence_analysis.get('total_confidence', 0.5) > 0.6):
            
            # Multi-agent coordination needed
            orchestration_type = self._determine_orchestration_type(
                domain_analysis.get('domain_count', 0), complexity_score,
                confidence_analysis.get('total_confidence', 0.5)
            )
            
            return EscalationDecision(
                action=EscalationAction.ORCHESTRATION_ROUTING,
                reason="Multi-agent coordination needed",
                confidence=confidence_analysis.get('total_confidence', 0.5),
                escalation_score=escalation_score,
                triggers=OrganizeContextPackage._extract_trigger_names(triggers),
                recommended_agent=orchestration_type,
                context_package=None
            )
        
        else:
            # Direct agent routing
            recommended_agent = self._select_direct_agent(domain_analysis, available_agents)
            
            return EscalationDecision(
                action=EscalationAction.DIRECT_AGENT_ROUTING,
                reason="Single agent capable",
                confidence=confidence_analysis.get('total_confidence', 0.5),
                escalation_score=escalation_score,
                triggers=OrganizeContextPackage._extract_trigger_names(triggers),
                recommended_agent=recommended_agent,
                context_package=None
            )
    
    def _determine_orchestration_type(self, domain_count: int, 
                                    complexity_score: float, 
                                    confidence: float) -> str:
        """Select appropriate orchestration system"""
        
        if domain_count >= 4 or complexity_score > 0.8:
            return "@orchestrate-agents-adv"  # Enterprise coordination
        elif domain_count >= 2 or complexity_score > 0.5:
            return "@orchestrate-agents"      # Standard coordination  
        else:
            return "@orchestrate-tasks"       # Intelligent analysis
    
    def _select_direct_agent(self, domain_analysis: Dict, 
                           available_agents: List[str]) -> str:
        """Select best direct agent based on domain analysis"""
        
        domains = domain_analysis.get('domains', [])
        if not domains:
            return "@orchestrate-tasks"  # Safe fallback
        
        # Use highest confidence domain
        primary_domain = domains[0]
        preferred_agents = primary_domain.get('preferred_agents', [])
        
        # Find first available preferred agent
        for agent in preferred_agents:
            if agent in available_agents:
                return agent
        
        # Fallback to orchestration
        return "@orchestrate-tasks"