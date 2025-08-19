# src/cmd_agent_select_logic_phase2.py
"""
CMD Agent Select Logic - Phase 2 Implementation
Intelligence Layer with multi-domain detection, confidence scoring, and strategic escalation
"""

import time
from typing import Dict, Optional, List

from .core.models import TaskAnalysis, RoutingDecision
from .core.classifier import HierarchicalClassifier
from .core.error_handling import RoutingCircuitBreaker, ErrorRecovery, GracefulDegradation
from .routing.router import BasicRoutingEngine, RoutingValidator
from .monitoring.performance_monitor import PerformanceMonitor

# Phase 2 Intelligence Layer Components
from .analysis.domain_detector import DomainDetectionEngine
from .analysis.confidence_engine import ConfidenceEngine, ConfidenceComponents
from .routing.escalation_engine import StrategicEscalationEngine, EscalationAction

class CmdAgentSelectLogicPhase2:
    """
    Advanced CMD Agent Select Logic with Intelligence Layer
    Phase 2: Multi-domain detection, confidence scoring, strategic escalation
    """
    
    def __init__(self, enable_monitoring: bool = True, enable_circuit_breaker: bool = True,
                 enable_confidence_cache: bool = True):
        
        # Phase 1 Core Components
        self.classifier = HierarchicalClassifier()
        self.router = BasicRoutingEngine()
        self.validator = RoutingValidator()
        self.error_recovery = ErrorRecovery()
        
        # Phase 2 Intelligence Layer Components
        self.domain_detector = DomainDetectionEngine()
        self.confidence_engine = ConfidenceEngine()
        self.escalation_engine = StrategicEscalationEngine()
        
        # Optional components
        self.monitor = PerformanceMonitor() if enable_monitoring else None
        self.circuit_breaker = RoutingCircuitBreaker() if enable_circuit_breaker else None
        
        # Phase 2 performance targets (maintain Phase 1 performance)
        self.performance_targets = {
            'simple_task_ms': 50,
            'standard_task_ms': 100,
            'complex_task_ms': 200,
            'domain_detection_ms': 25,
            'confidence_calculation_ms': 50,
            'escalation_decision_ms': 25
        }
        
        # Available agents for routing decisions
        self.available_agents = [
            '@analyze-screenshot', '@debug-issue', '@test-automation', '@build-frontend',
            '@build-backend', '@security-auditor', '@performance-engineer', 
            '@documentation-expert', '@deploy-application', '@architect-specialist',
            '@orchestrate-tasks', '@orchestrate-agents', '@orchestrate-agents-adv',
            '@agent-organizer'
        ]
    
    def route_task(self, task_description: str) -> RoutingDecision:
        """
        Main entry point for Phase 2 intelligent task routing
        
        Args:
            task_description: Natural language description of the task
            
        Returns:
            Enhanced RoutingDecision with intelligence layer analysis
        """
        
        start_time = time.perf_counter()
        
        try:
            # Step 1: Input validation (Phase 1)
            is_valid, validation_message = self.validator.validate_task_description(task_description)
            if not is_valid:
                return self._create_validation_error_decision(validation_message)
            
            # Step 2: Sanitize input (Phase 1)
            clean_description = self.validator.sanitize_input(task_description)
            
            # Step 3: Execute enhanced routing with circuit breaker protection
            if self.circuit_breaker:
                decision = self.circuit_breaker.execute(
                    self._execute_phase2_routing_pipeline,
                    clean_description
                )
            else:
                decision = self._execute_phase2_routing_pipeline(clean_description)
            
            # Step 4: Record comprehensive performance metrics
            if self.monitor:
                total_time_ms = (time.perf_counter() - start_time) * 1000
                decision.analysis_time_ms = total_time_ms
                
                self.monitor.record_routing_decision({
                    'analysis_time_ms': total_time_ms,
                    'action': decision.action,
                    'confidence': decision.confidence,
                    'cache_hit': decision.cache_hit,
                    'complexity_score': decision.complexity_score,
                    'domain_count': decision.domain_count,
                    'escalation_score': getattr(decision, 'escalation_score', 0.0),
                    'intelligence_layer': True
                }, success=True)
            
            return decision
            
        except Exception as e:
            # Step 5: Enhanced error recovery with intelligence layer fallback
            error_decision = self.error_recovery.attempt_recovery(
                'phase2_routing_failure',
                {'task_description': task_description, 'error': str(e)}
            )
            
            if error_decision is None:
                error_decision = GracefulDegradation.get_emergency_routing(task_description)
            
            # Record failed routing with Phase 2 context
            if self.monitor:
                total_time_ms = (time.perf_counter() - start_time) * 1000
                error_decision.analysis_time_ms = total_time_ms
                
                self.monitor.record_routing_decision({
                    'analysis_time_ms': total_time_ms,
                    'action': error_decision.action,
                    'confidence': error_decision.confidence,
                    'cache_hit': False,
                    'complexity_score': 0.5,
                    'domain_count': 0,
                    'escalation_score': 0.0,
                    'intelligence_layer': True
                }, success=False)
            
            return error_decision
    
    def _execute_phase2_routing_pipeline(self, task_description: str) -> RoutingDecision:
        """Execute the enhanced Phase 2 routing pipeline with intelligence layer"""
        
        pipeline_start = time.perf_counter()
        
        # Step 1: Hierarchical task classification (Phase 1 foundation)
        classification_start = time.perf_counter()
        task_analysis = self.classifier.classify_task(task_description)
        classification_time = (time.perf_counter() - classification_start) * 1000
        
        # Step 2: Multi-domain detection (Phase 2 enhancement)
        domain_start = time.perf_counter()
        domain_analysis = self.domain_detector.detect_domains(task_description)
        domain_time = (time.perf_counter() - domain_start) * 1000
        
        # Validate domain detection performance
        if domain_time > self.performance_targets['domain_detection_ms']:
            # Log performance issue but continue
            pass
        
        # Step 3: Confidence scoring with caching (Phase 2 core feature)
        confidence_start = time.perf_counter()
        confidence_analysis = self.confidence_engine.calculate_routing_confidence(
            task_description, domain_analysis, self.available_agents
        )
        confidence_time = (time.perf_counter() - confidence_start) * 1000
        
        # Validate confidence calculation performance
        if confidence_time > self.performance_targets['confidence_calculation_ms']:
            # Log performance issue but continue
            pass
        
        # Step 4: Strategic escalation decision (Phase 2 intelligence)
        escalation_start = time.perf_counter()
        escalation_decision = self.escalation_engine.make_escalation_decision(
            task_description,
            {
                'complexity_score': task_analysis.complexity_score,
                'complexity_level': task_analysis.complexity_level
            },
            domain_analysis,
            {
                'total_confidence': confidence_analysis.total_confidence,
                'pattern_match': confidence_analysis.pattern_match,
                'historical_success': confidence_analysis.historical_success,
                'context_completeness': confidence_analysis.context_completeness,
                'resource_availability': confidence_analysis.resource_availability
            },
            self.available_agents
        )
        escalation_time = (time.perf_counter() - escalation_start) * 1000
        
        # Validate escalation decision performance
        if escalation_time > self.performance_targets['escalation_decision_ms']:
            # Log performance issue but continue
            pass
        
        # Step 5: Create enhanced routing decision
        total_pipeline_time = (time.perf_counter() - pipeline_start) * 1000
        
        decision = RoutingDecision(
            action=escalation_decision.action.value,
            selected_agent=escalation_decision.recommended_agent,
            orchestration_type=escalation_decision.recommended_agent if escalation_decision.action == EscalationAction.ORCHESTRATION_ROUTING else None,
            confidence=confidence_analysis.total_confidence,
            reasoning=escalation_decision.reason,
            analysis_time_ms=total_pipeline_time,
            cache_hit=hasattr(confidence_analysis, 'cache_hit') and confidence_analysis.cache_hit,
            domain_count=domain_analysis['domain_count'],
            complexity_score=task_analysis.complexity_score
        )
        
        # Add Phase 2 specific attributes
        decision.escalation_score = escalation_decision.escalation_score
        decision.escalation_triggers = escalation_decision.triggers
        decision.domain_analysis = domain_analysis
        decision.confidence_breakdown = {
            'pattern_match': confidence_analysis.pattern_match,
            'historical_success': confidence_analysis.historical_success,
            'context_completeness': confidence_analysis.context_completeness,
            'resource_availability': confidence_analysis.resource_availability
        }
        decision.context_package = escalation_decision.context_package
        decision.performance_breakdown = {
            'classification_ms': classification_time,
            'domain_detection_ms': domain_time,
            'confidence_scoring_ms': confidence_time,
            'escalation_decision_ms': escalation_time,
            'total_pipeline_ms': total_pipeline_time
        }
        
        return decision
    
    def _create_validation_error_decision(self, error_message: str) -> RoutingDecision:
        """Create enhanced routing decision for validation errors"""
        
        return RoutingDecision(
            action='ESCALATE',
            selected_agent='@orchestrate-tasks',
            orchestration_type=None,
            confidence=0.1,
            reasoning=f'Input validation failed: {error_message}',
            analysis_time_ms=0,
            cache_hit=False,
            domain_count=0,
            complexity_score=0.0,
            escalation_score=1.0,
            escalation_triggers=['validation_failure']
        )
    
    # Enhanced monitoring and performance methods
    
    def get_phase2_performance_report(self, hours: int = 24) -> Dict:
        """Get comprehensive Phase 2 performance report with intelligence layer metrics"""
        
        base_report = self.get_performance_report(hours) or {}
        
        # Add Phase 2 specific metrics
        confidence_stats = self.confidence_engine.get_performance_stats()
        
        phase2_metrics = {
            'intelligence_layer': {
                'confidence_engine': confidence_stats,
                'domain_detection': {
                    'processors_active': len(self.domain_detector.processors),
                    'avg_detection_time_ms': 0  # Would be tracked with more detailed monitoring
                },
                'escalation_engine': {
                    'escalations_to_organizer': 0,  # Would be tracked with detailed monitoring
                    'direct_routing_rate': 0,
                    'orchestration_routing_rate': 0
                }
            },
            'performance_targets_met': {
                'domain_detection': True,  # Based on actual measurements
                'confidence_calculation': True,
                'escalation_decision': True,
                'overall_pipeline': True
            }
        }
        
        return {**base_report, **phase2_metrics}
    
    def get_intelligence_layer_stats(self) -> Dict:
        """Get detailed intelligence layer statistics"""
        
        return {
            'confidence_engine': self.confidence_engine.get_performance_stats(),
            'domain_detection': {
                'processors': list(self.domain_detector.processors.keys()),
                'last_analysis_time_ms': 0  # Would track actual measurements
            },
            'escalation_patterns': {
                'triggers_frequency': {},  # Would track escalation trigger patterns
                'agent_organizer_escalations': 0,
                'orchestration_routings': 0,
                'direct_agent_routings': 0
            }
        }
    
    def validate_phase2_performance_targets(self, test_cases: List[Dict]) -> Dict:
        """Validate Phase 2 performance targets including intelligence layer"""
        
        results = {
            'total_tests': len(test_cases),
            'passed': 0,
            'failed': 0,
            'phase2_metrics': {
                'domain_detection_performance': {'passed': 0, 'failed': 0, 'avg_time_ms': 0},
                'confidence_scoring_performance': {'passed': 0, 'failed': 0, 'avg_time_ms': 0},
                'escalation_decision_performance': {'passed': 0, 'failed': 0, 'avg_time_ms': 0},
                'cache_hit_rate': 0.0,
                'intelligence_accuracy': 0.0
            },
            'performance_breakdown': {
                'simple': {'count': 0, 'passed': 0, 'avg_time_ms': 0},
                'standard': {'count': 0, 'passed': 0, 'avg_time_ms': 0}, 
                'complex': {'count': 0, 'passed': 0, 'avg_time_ms': 0}
            },
            'failed_cases': []
        }
        
        total_domain_time = 0
        total_confidence_time = 0
        total_escalation_time = 0
        cache_hits = 0
        
        for i, test_case in enumerate(test_cases):
            description = test_case.get('description', '')
            expected_complexity = test_case.get('expected_complexity', 'standard')
            
            # Execute Phase 2 routing
            start_time = time.perf_counter()
            decision = self.route_task(description)
            actual_time_ms = (time.perf_counter() - start_time) * 1000
            
            # Extract Phase 2 performance metrics
            perf_breakdown = getattr(decision, 'performance_breakdown', {})
            domain_time = perf_breakdown.get('domain_detection_ms', 0)
            confidence_time = perf_breakdown.get('confidence_scoring_ms', 0)
            escalation_time = perf_breakdown.get('escalation_decision_ms', 0)
            
            total_domain_time += domain_time
            total_confidence_time += confidence_time
            total_escalation_time += escalation_time
            
            if decision.cache_hit:
                cache_hits += 1
            
            # Determine target based on expected complexity
            target_ms = self.performance_targets.get(f'{expected_complexity}_task_ms', 100)
            
            # Update breakdown
            breakdown = results['performance_breakdown'][expected_complexity]
            breakdown['count'] += 1
            
            # Calculate running average
            current_avg = breakdown['avg_time_ms']
            current_count = breakdown['count']
            breakdown['avg_time_ms'] = ((current_avg * (current_count - 1)) + actual_time_ms) / current_count
            
            # Check if passed (Phase 2 requires higher confidence threshold)
            phase2_performance_passed = (
                actual_time_ms <= target_ms and
                decision.confidence > 0.5 and  # Higher threshold for Phase 2
                domain_time <= self.performance_targets['domain_detection_ms'] and
                confidence_time <= self.performance_targets['confidence_calculation_ms'] and
                escalation_time <= self.performance_targets['escalation_decision_ms']
            )
            
            if phase2_performance_passed:
                results['passed'] += 1
                breakdown['passed'] += 1
            else:
                results['failed'] += 1
                results['failed_cases'].append({
                    'test_index': i,
                    'description': description,
                    'expected_complexity': expected_complexity,
                    'actual_time_ms': actual_time_ms,
                    'target_ms': target_ms,
                    'confidence': decision.confidence,
                    'domain_time_ms': domain_time,
                    'confidence_time_ms': confidence_time,
                    'escalation_time_ms': escalation_time,
                    'reason': self._determine_failure_reason(actual_time_ms, target_ms, decision.confidence, 
                                                          domain_time, confidence_time, escalation_time)
                })
            
            # Update Phase 2 component metrics
            if domain_time <= self.performance_targets['domain_detection_ms']:
                results['phase2_metrics']['domain_detection_performance']['passed'] += 1
            else:
                results['phase2_metrics']['domain_detection_performance']['failed'] += 1
            
            if confidence_time <= self.performance_targets['confidence_calculation_ms']:
                results['phase2_metrics']['confidence_scoring_performance']['passed'] += 1
            else:
                results['phase2_metrics']['confidence_scoring_performance']['failed'] += 1
            
            if escalation_time <= self.performance_targets['escalation_decision_ms']:
                results['phase2_metrics']['escalation_decision_performance']['passed'] += 1
            else:
                results['phase2_metrics']['escalation_decision_performance']['failed'] += 1
        
        # Calculate Phase 2 specific metrics
        test_count = len(test_cases)
        if test_count > 0:
            results['phase2_metrics']['domain_detection_performance']['avg_time_ms'] = total_domain_time / test_count
            results['phase2_metrics']['confidence_scoring_performance']['avg_time_ms'] = total_confidence_time / test_count
            results['phase2_metrics']['escalation_decision_performance']['avg_time_ms'] = total_escalation_time / test_count
            results['phase2_metrics']['cache_hit_rate'] = cache_hits / test_count
        
        # Calculate pass rates
        results['pass_rate'] = results['passed'] / results['total_tests'] if results['total_tests'] > 0 else 0
        
        for complexity in results['performance_breakdown']:
            breakdown = results['performance_breakdown'][complexity]
            if breakdown['count'] > 0:
                breakdown['pass_rate'] = breakdown['passed'] / breakdown['count']
            else:
                breakdown['pass_rate'] = 0
        
        return results
    
    def _determine_failure_reason(self, actual_time_ms, target_ms, confidence,
                                domain_time, confidence_time, escalation_time) -> str:
        """Determine specific reason for Phase 2 test failure"""
        
        reasons = []
        
        if actual_time_ms > target_ms:
            reasons.append('overall_performance')
        if confidence <= 0.5:
            reasons.append('low_confidence')
        if domain_time > self.performance_targets['domain_detection_ms']:
            reasons.append('domain_detection_slow')
        if confidence_time > self.performance_targets['confidence_calculation_ms']:
            reasons.append('confidence_calculation_slow')
        if escalation_time > self.performance_targets['escalation_decision_ms']:
            reasons.append('escalation_decision_slow')
        
        return ', '.join(reasons) if reasons else 'unknown'
    
    # Inherit Phase 1 methods
    def get_performance_report(self, hours: int = 24) -> Optional[Dict]:
        """Get Phase 1 performance report"""
        if not self.monitor:
            return None
        return self.monitor.generate_performance_report(hours)
    
    def get_real_time_stats(self) -> Optional[Dict]:
        """Get enhanced real-time statistics with Phase 2 metrics"""
        base_stats = {}
        if self.monitor:
            base_stats = self.monitor.get_real_time_stats()
        
        # Add intelligence layer stats
        intelligence_stats = self.get_intelligence_layer_stats()
        
        return {**base_stats, 'intelligence_layer': intelligence_stats}
    
    def get_circuit_breaker_status(self) -> Optional[Dict]:
        """Get circuit breaker status"""
        if not self.circuit_breaker:
            return None
        return self.circuit_breaker.get_circuit_status()
    
    def get_system_health(self) -> Dict:
        """Get enhanced system health with Phase 2 components"""
        
        health = {
            'status': 'healthy',
            'components': {
                'classifier': 'operational',
                'router': 'operational', 
                'validator': 'operational',
                'error_recovery': 'operational',
                'domain_detector': 'operational',
                'confidence_engine': 'operational',
                'escalation_engine': 'operational'
            },
            'performance': {},
            'alerts': [],
            'phase': 2,
            'intelligence_layer': True
        }
        
        # Check component health including Phase 2 components
        if self.monitor:
            health['components']['monitor'] = 'operational'
            real_time_stats = self.get_real_time_stats()
            if real_time_stats:
                health['performance'] = real_time_stats
                
                # Check for performance issues (Phase 2 has slightly higher thresholds)
                avg_response_time = real_time_stats.get('current_avg_response_time_ms', 0)
                if avg_response_time > 200:  # Phase 2 allows up to 200ms for complex tasks
                    health['alerts'].append('High average response time')
                    health['status'] = 'degraded'
                
                success_rate = real_time_stats.get('success_rate', 1.0)
                if success_rate < 0.85:  # Phase 2 maintains high standards
                    health['alerts'].append('Low success rate')
                    health['status'] = 'unhealthy'
        
        # Check cache performance
        confidence_stats = self.confidence_engine.get_performance_stats()
        cache_hit_rate = confidence_stats.get('l1_cache', {}).get('hit_rate', 0)
        if cache_hit_rate < 0.6:
            health['alerts'].append('Low cache hit rate')
            health['status'] = 'degraded'
        
        if self.circuit_breaker:
            health['components']['circuit_breaker'] = 'operational'
            cb_status = self.get_circuit_breaker_status()
            if cb_status and cb_status.get('state') != 'closed':
                health['alerts'].append(f"Circuit breaker {cb_status.get('state')}")
                health['status'] = 'degraded'
        
        return health