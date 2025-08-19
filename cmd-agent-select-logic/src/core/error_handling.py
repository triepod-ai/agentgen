# src/core/error_handling.py
import time
import logging
from typing import Dict, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass
from ..core.models import RoutingDecision, RoutingAction

class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"

class CircuitBreakerState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class ErrorContext:
    error_type: str
    severity: ErrorSeverity
    message: str
    timestamp: float
    component: str
    recovery_suggestion: str

class RoutingCircuitBreaker:
    """Enhanced 3-State Circuit Breaker with Martin Fowler's proven pattern
    
    Implementation based on:
    - Martin Fowler's Circuit Breaker pattern
    - Spring Cloud Circuit Breaker
    - Resilience4j patterns
    
    States:
    - CLOSED: Normal operation, failures counted
    - OPEN: Circuit open, requests fail fast
    - HALF_OPEN: Testing recovery, limited requests allowed
    """
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 30, success_threshold: int = 3):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state = CircuitBreakerState.CLOSED
        self.error_log = []
        
        # Enhanced 3-State Pattern Metrics
        self.state_transitions = {
            'closed_to_open': 0,
            'open_to_half_open': 0,
            'half_open_to_closed': 0,
            'half_open_to_open': 0
        }
        self.uptime_stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'circuit_open_count': 0
        }
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def execute(self, routing_function: Callable, *args, **kwargs) -> Any:
        """Execute routing function with enhanced 3-state circuit breaker protection"""
        
        self.uptime_stats['total_requests'] += 1
        
        # OPEN State: Fail fast until recovery timeout
        if self.state == CircuitBreakerState.OPEN:
            if self._should_attempt_reset():
                self._transition_to_half_open()
            else:
                self.uptime_stats['circuit_open_count'] += 1
                return self._fallback_routing(*args, **kwargs)
        
        # HALF_OPEN State: Limited testing mode
        if self.state == CircuitBreakerState.HALF_OPEN:
            return self._execute_half_open(routing_function, *args, **kwargs)
        
        # CLOSED State: Normal operation with failure monitoring
        try:
            result = routing_function(*args, **kwargs)
            self._record_success()
            return result
            
        except Exception as e:
            error_context = ErrorContext(
                error_type=type(e).__name__,
                severity=self._classify_error_severity(e),
                message=str(e),
                timestamp=time.time(),
                component="routing_engine",
                recovery_suggestion=self._get_recovery_suggestion(e)
            )
            
            self._record_failure(error_context)
            return self._fallback_routing(*args, **kwargs)
    
    def _transition_to_half_open(self):
        """Transition from OPEN to HALF_OPEN state"""
        self.state = CircuitBreakerState.HALF_OPEN
        self.success_count = 0
        self.state_transitions['open_to_half_open'] += 1
        self.logger.info("Circuit breaker transitioning to HALF_OPEN state - testing recovery")
    
    def _execute_half_open(self, routing_function: Callable, *args, **kwargs) -> Any:
        """Execute request in HALF_OPEN state with careful monitoring"""
        try:
            result = routing_function(*args, **kwargs)
            self._record_half_open_success()
            return result
        except Exception as e:
            self._record_half_open_failure()
            error_context = ErrorContext(
                error_type=type(e).__name__,
                severity=self._classify_error_severity(e),
                message=str(e),
                timestamp=time.time(),
                component="routing_engine_half_open",
                recovery_suggestion=self._get_recovery_suggestion(e)
            )
            self.error_log.append(error_context)
            return self._fallback_routing(*args, **kwargs)
    
    def _record_half_open_success(self):
        """Record successful operation in HALF_OPEN state"""
        self.success_count += 1
        self.uptime_stats['successful_requests'] += 1
        
        # Transition to CLOSED after success threshold met
        if self.success_count >= self.success_threshold:
            self.state = CircuitBreakerState.CLOSED
            self.failure_count = 0
            self.state_transitions['half_open_to_closed'] += 1
            self.logger.info(f"Circuit breaker CLOSED - recovery successful after {self.success_count} tests")
    
    def _record_half_open_failure(self):
        """Record failed operation in HALF_OPEN state"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        self.uptime_stats['failed_requests'] += 1
        
        # Transition back to OPEN on any failure in HALF_OPEN
        self.state = CircuitBreakerState.OPEN
        self.state_transitions['half_open_to_open'] += 1
        self.logger.warning("Circuit breaker returned to OPEN state - recovery test failed")
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset to HALF_OPEN"""
        if self.last_failure_time is None:
            return True
        return (time.time() - self.last_failure_time) >= self.recovery_timeout
    
    def _record_success(self):
        """Record successful operation in CLOSED state"""
        self.failure_count = 0
        self.uptime_stats['successful_requests'] += 1
    
    def _record_failure(self, error_context: ErrorContext):
        """Record failed operation with enhanced state transition logic"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        self.error_log.append(error_context)
        self.uptime_stats['failed_requests'] += 1
        
        # Keep only last 50 errors
        if len(self.error_log) > 50:
            self.error_log = self.error_log[-50:]
        
        self.logger.warning(f"Circuit breaker failure recorded: {error_context.message}")
        
        # Transition to OPEN when failure threshold reached
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN
            self.state_transitions['closed_to_open'] += 1
            self.logger.error(f"Circuit breaker OPENED after {self.failure_count} failures")
    
    def _fallback_routing(self, task_description: str = "", *args, **kwargs) -> RoutingDecision:
        """Enhanced fallback routing with state-aware messaging"""
        
        state_messages = {
            CircuitBreakerState.OPEN: "Circuit breaker OPEN - system protection active",
            CircuitBreakerState.HALF_OPEN: "Circuit breaker HALF_OPEN - recovery testing",
            CircuitBreakerState.CLOSED: "Circuit breaker fallback - unexpected path"
        }
        
        reasoning = state_messages.get(self.state, f'Circuit breaker fallback - state: {self.state.value}')
        
        self.logger.info(f"Using fallback routing - {reasoning}")
        
        return RoutingDecision(
            action=RoutingAction.ESCALATE,
            selected_agent='@orchestrate-tasks',  # Safe fallback
            orchestration_type=None,
            confidence=0.6,
            reasoning=reasoning,
            analysis_time_ms=0,
            cache_hit=False,
            domain_count=0,
            complexity_score=0.5
        )
    
    def _classify_error_severity(self, error: Exception) -> ErrorSeverity:
        """Classify error severity based on error type"""
        
        critical_errors = ['SystemError', 'MemoryError', 'OSError']
        high_errors = ['ValueError', 'TypeError', 'AttributeError']
        medium_errors = ['KeyError', 'IndexError', 'ImportError']
        
        error_type = type(error).__name__
        
        if error_type in critical_errors:
            return ErrorSeverity.CRITICAL
        elif error_type in high_errors:
            return ErrorSeverity.HIGH
        elif error_type in medium_errors:
            return ErrorSeverity.MEDIUM
        else:
            return ErrorSeverity.LOW
    
    def _get_recovery_suggestion(self, error: Exception) -> str:
        """Get recovery suggestion based on error type"""
        
        error_type = type(error).__name__
        
        suggestions = {
            'ValueError': 'Check input validation and data formatting',
            'TypeError': 'Verify function arguments and data types',
            'KeyError': 'Check dictionary keys and configuration',
            'AttributeError': 'Verify object attributes and method names',
            'ImportError': 'Check module dependencies and installation',
            'MemoryError': 'Reduce processing load and check system resources',
            'OSError': 'Check system resources and file permissions'
        }
        
        return suggestions.get(error_type, 'Check system logs and configuration')
    
    def get_circuit_status(self) -> Dict:
        """Get comprehensive circuit breaker status with 3-state metrics"""
        
        recent_errors = [e for e in self.error_log 
                        if time.time() - e.timestamp < 300]  # Last 5 minutes
        
        # Calculate uptime percentage (99.9% target)
        uptime_percentage = (self.uptime_stats['successful_requests'] / 
                           max(self.uptime_stats['total_requests'], 1)) * 100
        
        return {
            'state': self.state.value,
            'failure_count': self.failure_count,
            'success_count': self.success_count,
            'last_failure_time': self.last_failure_time,
            'recent_errors_count': len(recent_errors),
            'total_errors_logged': len(self.error_log),
            'error_rate_last_5min': len(recent_errors) / 5 if recent_errors else 0,
            'time_to_next_attempt': max(0, self.recovery_timeout - (time.time() - (self.last_failure_time or 0))),
            
            # Enhanced 3-State Pattern Metrics
            'state_transitions': self.state_transitions.copy(),
            'uptime_stats': self.uptime_stats.copy(),
            'uptime_percentage': uptime_percentage,
            'meets_uptime_target': uptime_percentage >= 99.9,
            
            # State-specific information
            'state_info': self._get_state_specific_info()
        }
    
    def _get_state_specific_info(self) -> Dict:
        """Get information specific to current circuit breaker state"""
        
        if self.state == CircuitBreakerState.CLOSED:
            return {
                'description': 'Normal operation - monitoring failures',
                'failures_until_open': max(0, self.failure_threshold - self.failure_count)
            }
        elif self.state == CircuitBreakerState.OPEN:
            return {
                'description': 'Circuit open - failing fast for protection',
                'seconds_until_half_open': max(0, int(self.recovery_timeout - (time.time() - (self.last_failure_time or 0))))
            }
        elif self.state == CircuitBreakerState.HALF_OPEN:
            return {
                'description': 'Testing recovery - monitoring success rate',
                'successes_needed_to_close': max(0, self.success_threshold - self.success_count)
            }
        else:
            return {'description': 'Unknown state'}

class GracefulDegradation:
    """Graceful degradation strategies for system resilience"""
    
    @staticmethod
    def get_fallback_agent(domain: str, complexity_score: float) -> str:
        """Get fallback agent when primary routing fails"""
        
        # High complexity always goes to advanced orchestration
        if complexity_score > 0.8:
            return '@orchestrate-agents-adv'
        
        # Domain-specific fallbacks
        fallback_map = {
            'frontend': '@build-frontend',
            'backend': '@build-backend', 
            'security': '@security-auditor',
            'infrastructure': '@deploy-application',
            'testing': '@test-automation',
            'documentation': '@generate-documentation'
        }
        
        return fallback_map.get(domain, '@orchestrate-tasks')
    
    @staticmethod
    def reduce_complexity_threshold(current_threshold: float, degradation_level: int) -> float:
        """Reduce complexity thresholds during system stress"""
        
        # Progressive degradation
        degradation_factors = [1.0, 0.9, 0.8, 0.7, 0.6]  # 5 levels
        level = min(degradation_level, len(degradation_factors) - 1)
        
        return max(current_threshold * degradation_factors[level], 0.3)  # Never below 0.3
    
    @staticmethod
    def get_emergency_routing(task_description: str) -> RoutingDecision:
        """Emergency routing for critical system failures"""
        
        return RoutingDecision(
            action=RoutingAction.ESCALATE,
            selected_agent='@orchestrate-tasks',  # Most reliable fallback
            orchestration_type=None,
            confidence=0.5,
            reasoning='Emergency routing activated due to system degradation',
            analysis_time_ms=0,
            cache_hit=False,
            domain_count=1,
            complexity_score=0.5
        )

class ErrorRecovery:
    """Error recovery and self-healing mechanisms"""
    
    def __init__(self):
        self.recovery_strategies = {
            'classification_failure': self._recover_from_classification_failure,
            'domain_detection_failure': self._recover_from_domain_failure,
            'routing_failure': self._recover_from_routing_failure,
            'validation_failure': self._recover_from_validation_failure
        }
    
    def attempt_recovery(self, error_type: str, context: Dict) -> Optional[RoutingDecision]:
        """Attempt to recover from specific error types"""
        
        recovery_func = self.recovery_strategies.get(error_type)
        if recovery_func:
            return recovery_func(context)
        return None
    
    def _recover_from_classification_failure(self, context: Dict) -> RoutingDecision:
        """Recover from classification system failure"""
        
        # Use simple heuristics as fallback
        task_description = context.get('task_description', '')
        word_count = len(task_description.split())
        
        if word_count <= 5:
            complexity_score = 0.3
        elif word_count >= 15:
            complexity_score = 0.7
        else:
            complexity_score = 0.5
        
        return RoutingDecision(
            action=RoutingAction.ORCHESTRATION,
            selected_agent=None,
            orchestration_type='@orchestrate-tasks',
            confidence=0.5,
            reasoning='Recovered from classification failure using simple heuristics',
            analysis_time_ms=0,
            complexity_score=complexity_score,
            domain_count=1
        )
    
    def _recover_from_domain_failure(self, context: Dict) -> RoutingDecision:
        """Recover from domain detection failure"""
        
        return RoutingDecision(
            action=RoutingAction.ESCALATE,
            selected_agent=None,
            orchestration_type=None,
            confidence=0.4,
            reasoning='Recovered from domain detection failure - escalating for manual analysis',
            analysis_time_ms=0,
            complexity_score=0.5,
            domain_count=0
        )
    
    def _recover_from_routing_failure(self, context: Dict) -> RoutingDecision:
        """Recover from routing decision failure"""
        
        return GracefulDegradation.get_emergency_routing(
            context.get('task_description', '')
        )
    
    def _recover_from_validation_failure(self, context: Dict) -> RoutingDecision:
        """Recover from input validation failure"""
        
        return RoutingDecision(
            action=RoutingAction.ESCALATE,
            selected_agent=None,
            orchestration_type=None,
            confidence=0.2,
            reasoning='Input validation failed - manual review required',
            analysis_time_ms=0,
            complexity_score=0.3,
            domain_count=0
        )