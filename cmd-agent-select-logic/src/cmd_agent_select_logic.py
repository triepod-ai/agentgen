# src/cmd_agent_select_logic.py
"""
CMD Agent Select Logic - Phase 1 Implementation
Core foundation with basic hierarchical classification and pattern-based routing
"""

import time
from typing import Dict, Optional

from .core.models import TaskAnalysis, RoutingDecision
from .core.classifier import HierarchicalClassifier
from .core.error_handling import RoutingCircuitBreaker, ErrorRecovery, GracefulDegradation
from .routing.router import BasicRoutingEngine, RoutingValidator
from .monitoring.performance_monitor import PerformanceMonitor

class CmdAgentSelectLogic:
    """
    Main interface for the CMD Agent Select Logic system
    Phase 1: Core foundation with <100ms routing targets
    """
    
    def __init__(self, enable_monitoring: bool = True, enable_circuit_breaker: bool = True):
        # Core components
        self.classifier = HierarchicalClassifier()
        self.router = BasicRoutingEngine()
        self.validator = RoutingValidator()
        self.error_recovery = ErrorRecovery()
        
        # Optional components
        self.monitor = PerformanceMonitor() if enable_monitoring else None
        self.circuit_breaker = RoutingCircuitBreaker() if enable_circuit_breaker else None
        
        # Performance targets from Phase 1 requirements
        self.performance_targets = {
            'simple_task_ms': 50,
            'standard_task_ms': 100,
            'complex_task_ms': 200
        }
        
    def route_task(self, task_description: str) -> RoutingDecision:
        """
        Main entry point for task routing
        
        Args:
            task_description: Natural language description of the task
            
        Returns:
            RoutingDecision with selected agent or orchestration type
        """
        
        start_time = time.perf_counter()
        
        try:
            # Step 1: Input validation
            is_valid, validation_message = self.validator.validate_task_description(task_description)
            if not is_valid:
                return self._create_validation_error_decision(validation_message)
            
            # Step 2: Sanitize input
            clean_description = self.validator.sanitize_input(task_description)
            
            # Step 3: Execute routing with circuit breaker protection
            if self.circuit_breaker:
                decision = self.circuit_breaker.execute(
                    self._execute_routing_pipeline,
                    clean_description
                )
            else:
                decision = self._execute_routing_pipeline(clean_description)
            
            # Step 4: Record performance metrics
            if self.monitor:
                total_time_ms = (time.perf_counter() - start_time) * 1000
                decision.analysis_time_ms = total_time_ms
                
                self.monitor.record_routing_decision({
                    'analysis_time_ms': total_time_ms,
                    'action': decision.action.value,
                    'confidence': decision.confidence,
                    'cache_hit': decision.cache_hit,
                    'complexity_score': decision.complexity_score,
                    'domain_count': decision.domain_count
                }, success=True)
            
            return decision
            
        except Exception as e:
            # Step 5: Error recovery
            error_decision = self.error_recovery.attempt_recovery(
                'routing_failure',
                {'task_description': task_description, 'error': str(e)}
            )
            
            if error_decision is None:
                error_decision = GracefulDegradation.get_emergency_routing(task_description)
            
            # Record failed routing
            if self.monitor:
                total_time_ms = (time.perf_counter() - start_time) * 1000
                error_decision.analysis_time_ms = total_time_ms
                
                self.monitor.record_routing_decision({
                    'analysis_time_ms': total_time_ms,
                    'action': error_decision.action.value,
                    'confidence': error_decision.confidence,
                    'cache_hit': False,
                    'complexity_score': 0.5,
                    'domain_count': 0
                }, success=False)
            
            return error_decision
    
    def _execute_routing_pipeline(self, task_description: str) -> RoutingDecision:
        """Execute the core routing pipeline"""
        
        # Step 1: Task classification
        task_analysis = self.classifier.classify_task(task_description)
        
        # Check performance target for classification
        if task_analysis.analysis_time_ms > self.performance_targets.get('simple_task_ms', 50):
            # Log performance issue but continue
            pass
        
        # Step 2: Route based on analysis
        routing_decision = self.router.route_task(task_analysis)
        
        return routing_decision
    
    def _create_validation_error_decision(self, error_message: str) -> RoutingDecision:
        """Create routing decision for validation errors"""
        
        return RoutingDecision(
            action='ESCALATE',
            selected_agent=None,
            orchestration_type=None,
            confidence=0.1,
            reasoning=f'Input validation failed: {error_message}',
            analysis_time_ms=0,
            cache_hit=False,
            domain_count=0,
            complexity_score=0.0
        )
    
    # Performance and monitoring methods
    
    def get_performance_report(self, hours: int = 24) -> Optional[Dict]:
        """Get comprehensive performance report"""
        
        if not self.monitor:
            return None
        
        return self.monitor.generate_performance_report(hours)
    
    def get_real_time_stats(self) -> Optional[Dict]:
        """Get real-time performance statistics"""
        
        if not self.monitor:
            return None
            
        stats = self.monitor.get_real_time_stats()
        
        # Add routing engine stats
        if hasattr(self.router, 'get_routing_stats'):
            routing_stats = self.router.get_routing_stats()
            stats.update({
                'routing_patterns': routing_stats
            })
        
        return stats
    
    def get_circuit_breaker_status(self) -> Optional[Dict]:
        """Get circuit breaker status"""
        
        if not self.circuit_breaker:
            return None
            
        return self.circuit_breaker.get_circuit_status()
    
    def get_system_health(self) -> Dict:
        """Get overall system health status"""
        
        health = {
            'status': 'healthy',
            'components': {
                'classifier': 'operational',
                'router': 'operational', 
                'validator': 'operational',
                'error_recovery': 'operational'
            },
            'performance': {},
            'alerts': []
        }
        
        # Check component health
        if self.monitor:
            health['components']['monitor'] = 'operational'
            real_time_stats = self.get_real_time_stats()
            if real_time_stats:
                health['performance'] = real_time_stats
                
                # Check for performance issues
                avg_response_time = real_time_stats.get('current_avg_response_time_ms', 0)
                if avg_response_time > 150:
                    health['alerts'].append('High average response time')
                    health['status'] = 'degraded'
                
                success_rate = real_time_stats.get('success_rate', 1.0)
                if success_rate < 0.9:
                    health['alerts'].append('Low success rate')
                    health['status'] = 'unhealthy'
        
        if self.circuit_breaker:
            health['components']['circuit_breaker'] = 'operational'
            cb_status = self.get_circuit_breaker_status()
            if cb_status and cb_status.get('state') != 'closed':
                health['alerts'].append(f"Circuit breaker {cb_status.get('state')}")
                health['status'] = 'degraded'
        
        return health
    
    # Test and validation methods
    
    def validate_performance_targets(self, test_cases: list) -> Dict:
        """Validate that system meets performance targets with test cases"""
        
        results = {
            'total_tests': len(test_cases),
            'passed': 0,
            'failed': 0,
            'performance_breakdown': {
                'simple': {'count': 0, 'passed': 0, 'avg_time_ms': 0},
                'standard': {'count': 0, 'passed': 0, 'avg_time_ms': 0}, 
                'complex': {'count': 0, 'passed': 0, 'avg_time_ms': 0}
            },
            'failed_cases': []
        }
        
        for i, test_case in enumerate(test_cases):
            description = test_case.get('description', '')
            expected_complexity = test_case.get('expected_complexity', 'standard')
            
            # Execute routing
            start_time = time.perf_counter()
            decision = self.route_task(description)
            actual_time_ms = (time.perf_counter() - start_time) * 1000
            
            # Determine target based on expected complexity
            target_ms = self.performance_targets.get(f'{expected_complexity}_task_ms', 100)
            
            # Update breakdown
            breakdown = results['performance_breakdown'][expected_complexity]
            breakdown['count'] += 1
            
            # Calculate running average
            current_avg = breakdown['avg_time_ms']
            current_count = breakdown['count']
            breakdown['avg_time_ms'] = ((current_avg * (current_count - 1)) + actual_time_ms) / current_count
            
            # Check if passed
            if actual_time_ms <= target_ms and decision.confidence > 0.3:
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
                    'reason': 'performance' if actual_time_ms > target_ms else 'confidence'
                })
        
        # Calculate pass rates
        results['pass_rate'] = results['passed'] / results['total_tests'] if results['total_tests'] > 0 else 0
        
        for complexity in results['performance_breakdown']:
            breakdown = results['performance_breakdown'][complexity]
            if breakdown['count'] > 0:
                breakdown['pass_rate'] = breakdown['passed'] / breakdown['count']
            else:
                breakdown['pass_rate'] = 0
        
        return results