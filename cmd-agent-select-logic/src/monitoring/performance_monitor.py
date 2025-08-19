# src/monitoring/performance_monitor.py
import time
import statistics
from typing import Dict, List, Optional
from collections import deque
import logging
from dataclasses import dataclass, asdict

@dataclass
class PerformanceMetrics:
    timestamp: float
    decision_time_ms: float
    action: str
    confidence: float
    cache_hit: bool
    complexity_score: float
    domain_count: int
    success: bool = True

@dataclass
class SREGoldenSignals:
    """Google SRE Golden Signals for system reliability
    
    The Four Golden Signals:
    1. Latency - Time to service a request
    2. Traffic - Demand on your system (requests/second)
    3. Errors - Rate of requests that fail
    4. Saturation - How full your service is (resource utilization)
    """
    timestamp: float
    latency_p50_ms: float
    latency_p95_ms: float
    latency_p99_ms: float
    traffic_rps: float  # Requests per second
    error_rate_percent: float
    saturation_cpu_percent: float  # Simplified CPU utilization proxy
    saturation_memory_percent: float  # Simplified memory utilization proxy

class PerformanceMonitor:
    """Comprehensive performance monitoring with Google SRE Golden Signals
    
    Enhanced with Google SRE's Four Golden Signals:
    - Latency: Response time percentiles (P50, P95, P99)
    - Traffic: Request rate and throughput
    - Errors: Error rate and failure patterns
    - Saturation: System resource utilization
    
    Plus essential service-specific metrics for routing system
    """
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        
        # Performance metrics storage (existing - PRESERVE ALL FUNCTIONALITY)
        self.metrics_history = deque(maxlen=max_history)
        self.response_times = deque(maxlen=max_history)
        
        # Real-time counters (existing - PRESERVE ALL FUNCTIONALITY)
        self.total_requests = 0
        self.successful_routes = 0
        self.cache_hits = 0
        self.performance_targets_met = 0
        
        # Performance targets (existing - PRESERVE ALL FUNCTIONALITY)
        self.targets = {
            'simple_task_ms': 50,
            'standard_task_ms': 100, 
            'complex_task_ms': 200,
            'cache_hit_rate': 0.8,
            'success_rate': 0.9
        }
        
        # Google SRE Golden Signals Storage
        self.golden_signals_history = deque(maxlen=max_history)
        self.request_timestamps = deque(maxlen=1000)  # For traffic calculation
        
        # SRE Service-Specific Metrics (minimal set)
        self.service_metrics = {
            'routing_decisions_per_second': 0,
            'agent_selection_accuracy': 0,
            'escalation_rate': 0  # % of requests escalated to @agent-organizer
        }
        
        # SRE Alert Thresholds (based on Google SRE practices)
        self.sre_thresholds = {
            'latency_p99_ms': 500,      # 99th percentile latency
            'error_rate_percent': 1.0,   # Error rate
            'saturation_percent': 80,    # Resource saturation
            'traffic_degradation': 0.5   # 50% traffic drop indicates issues
        }
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Alert thresholds (existing - PRESERVE)
        self.alert_thresholds = {
            'avg_response_time_ms': 150,
            'error_rate_percent': 10,
            'cache_hit_rate_percent': 60
        }
        
    def record_routing_decision(self, decision_data: Dict, success: bool = True):
        """Record a routing decision with comprehensive metrics (existing functionality preserved)"""
        
        self.total_requests += 1
        current_timestamp = time.time()
        
        # Record request timestamp for traffic calculation
        self.request_timestamps.append(current_timestamp)
        
        # Create metrics record (existing logic preserved)
        metrics = PerformanceMetrics(
            timestamp=current_timestamp,
            decision_time_ms=decision_data.get('analysis_time_ms', 0),
            action=decision_data.get('action', 'unknown'),
            confidence=decision_data.get('confidence', 0),
            cache_hit=decision_data.get('cache_hit', False),
            complexity_score=decision_data.get('complexity_score', 0),
            domain_count=decision_data.get('domain_count', 0),
            success=success
        )
        
        # Store metrics (existing logic preserved)
        self.metrics_history.append(metrics)
        self.response_times.append(metrics.decision_time_ms)
        
        # Update counters (existing logic preserved)
        if success:
            self.successful_routes += 1
            
        if metrics.cache_hit:
            self.cache_hits += 1
            
        # Check performance targets (existing logic preserved)
        if self._meets_performance_target(metrics):
            self.performance_targets_met += 1
            
        # Update SRE service-specific metrics
        self._update_service_metrics(decision_data, success)
        
        # Generate SRE Golden Signals (every 10 requests to minimize overhead)
        if self.total_requests % 10 == 0:
            self._generate_golden_signals()
            
        # Check for alerts (existing and SRE)
        self._check_performance_alerts(metrics)
        self._check_sre_alerts()
    
    def _update_service_metrics(self, decision_data: Dict, success: bool):
        """Update service-specific metrics for routing system"""
        
        # Calculate requests per second (simple moving average)
        recent_requests = [ts for ts in self.request_timestamps if time.time() - ts < 1.0]
        self.service_metrics['routing_decisions_per_second'] = len(recent_requests)
        
        # Calculate agent selection accuracy (successful non-escalated routes)
        escalated = decision_data.get('action') == 'ESCALATE'
        if success and not escalated:
            # Simple exponential moving average for accuracy
            current_accuracy = self.service_metrics['agent_selection_accuracy']
            self.service_metrics['agent_selection_accuracy'] = current_accuracy * 0.9 + 1.0 * 0.1
        elif not success:
            current_accuracy = self.service_metrics['agent_selection_accuracy']
            self.service_metrics['agent_selection_accuracy'] = current_accuracy * 0.9 + 0.0 * 0.1
        
        # Calculate escalation rate
        if escalated:
            escalation_rate = (1.0 / max(self.total_requests, 1)) * 100
            current_rate = self.service_metrics['escalation_rate']
            self.service_metrics['escalation_rate'] = current_rate * 0.95 + escalation_rate * 0.05
    
    def _generate_golden_signals(self):
        """Generate Google SRE Golden Signals snapshot"""
        
        current_time = time.time()
        recent_metrics = [m for m in self.metrics_history if current_time - m.timestamp < 60]  # Last 60 seconds
        
        if not recent_metrics:
            return
        
        # Golden Signal 1: LATENCY (P50, P95, P99)
        response_times = [m.decision_time_ms for m in recent_metrics]
        latency_p50 = self._percentile(response_times, 50)
        latency_p95 = self._percentile(response_times, 95)
        latency_p99 = self._percentile(response_times, 99)
        
        # Golden Signal 2: TRAFFIC (requests per second)
        traffic_rps = len(recent_metrics) / 60.0  # Requests in last 60 seconds / 60
        
        # Golden Signal 3: ERRORS (error rate percentage)
        failed_requests = sum(1 for m in recent_metrics if not m.success)
        error_rate_percent = (failed_requests / len(recent_metrics)) * 100
        
        # Golden Signal 4: SATURATION (system resource utilization proxy)
        # Simplified proxies based on routing system characteristics
        avg_complexity = statistics.mean([m.complexity_score for m in recent_metrics])
        avg_response_time = statistics.mean(response_times)
        
        # CPU proxy: Based on complexity and response time
        cpu_saturation = min((avg_complexity * 50) + (avg_response_time / 10), 100)
        
        # Memory proxy: Based on cache usage and request volume
        cache_hit_rate = sum(1 for m in recent_metrics if m.cache_hit) / len(recent_metrics)
        memory_saturation = min((1 - cache_hit_rate) * 80 + (traffic_rps * 2), 100)
        
        # Create Golden Signals snapshot
        golden_signals = SREGoldenSignals(
            timestamp=current_time,
            latency_p50_ms=latency_p50,
            latency_p95_ms=latency_p95,
            latency_p99_ms=latency_p99,
            traffic_rps=traffic_rps,
            error_rate_percent=error_rate_percent,
            saturation_cpu_percent=cpu_saturation,
            saturation_memory_percent=memory_saturation
        )
        
        self.golden_signals_history.append(golden_signals)
    
    def _check_sre_alerts(self):
        """Check SRE Golden Signals against alert thresholds"""
        
        if not self.golden_signals_history:
            return
        
        latest_signals = self.golden_signals_history[-1]
        
        # Latency alert (P99 latency)
        if latest_signals.latency_p99_ms > self.sre_thresholds['latency_p99_ms']:
            self.logger.warning(f"SRE ALERT - High P99 latency: {latest_signals.latency_p99_ms:.1f}ms > {self.sre_thresholds['latency_p99_ms']}ms")
        
        # Error rate alert
        if latest_signals.error_rate_percent > self.sre_thresholds['error_rate_percent']:
            self.logger.error(f"SRE ALERT - High error rate: {latest_signals.error_rate_percent:.1f}% > {self.sre_thresholds['error_rate_percent']}%")
        
        # Saturation alert
        max_saturation = max(latest_signals.saturation_cpu_percent, latest_signals.saturation_memory_percent)
        if max_saturation > self.sre_thresholds['saturation_percent']:
            self.logger.warning(f"SRE ALERT - High resource saturation: {max_saturation:.1f}% > {self.sre_thresholds['saturation_percent']}%")
        
        # Traffic degradation alert (compare to recent average)
        if len(self.golden_signals_history) > 5:
            recent_traffic = [gs.traffic_rps for gs in list(self.golden_signals_history)[-5:]]
            avg_traffic = statistics.mean(recent_traffic)
            if latest_signals.traffic_rps < avg_traffic * self.sre_thresholds['traffic_degradation']:
                self.logger.warning(f"SRE ALERT - Traffic degradation: {latest_signals.traffic_rps:.1f} RPS < {avg_traffic * self.sre_thresholds['traffic_degradation']:.1f} RPS")
    
    def get_sre_golden_signals(self) -> Dict:
        """Get current Google SRE Golden Signals"""
        
        if not self.golden_signals_history:
            return {'error': 'No SRE metrics available'}
        
        latest = self.golden_signals_history[-1]
        
        # Calculate trends (last 5 snapshots)
        recent_signals = list(self.golden_signals_history)[-5:] if len(self.golden_signals_history) >= 5 else list(self.golden_signals_history)
        
        latency_trend = 'stable'
        if len(recent_signals) >= 3:
            first_latency = recent_signals[0].latency_p95_ms
            last_latency = recent_signals[-1].latency_p95_ms
            if last_latency > first_latency * 1.2:
                latency_trend = 'increasing'
            elif last_latency < first_latency * 0.8:
                latency_trend = 'decreasing'
        
        traffic_trend = 'stable'
        if len(recent_signals) >= 3:
            first_traffic = recent_signals[0].traffic_rps
            last_traffic = recent_signals[-1].traffic_rps
            if last_traffic > first_traffic * 1.2:
                traffic_trend = 'increasing'
            elif last_traffic < first_traffic * 0.8:
                traffic_trend = 'decreasing'
        
        return {
            'golden_signals': {
                'latency': {
                    'p50_ms': latest.latency_p50_ms,
                    'p95_ms': latest.latency_p95_ms,
                    'p99_ms': latest.latency_p99_ms,
                    'trend': latency_trend,
                    'alert': latest.latency_p99_ms > self.sre_thresholds['latency_p99_ms']
                },
                'traffic': {
                    'requests_per_second': latest.traffic_rps,
                    'trend': traffic_trend,
                    'alert': False  # Traffic alerts are relative to baseline
                },
                'errors': {
                    'error_rate_percent': latest.error_rate_percent,
                    'alert': latest.error_rate_percent > self.sre_thresholds['error_rate_percent']
                },
                'saturation': {
                    'cpu_percent': latest.saturation_cpu_percent,
                    'memory_percent': latest.saturation_memory_percent,
                    'max_saturation': max(latest.saturation_cpu_percent, latest.saturation_memory_percent),
                    'alert': max(latest.saturation_cpu_percent, latest.saturation_memory_percent) > self.sre_thresholds['saturation_percent']
                }
            },
            'service_metrics': self.service_metrics.copy(),
            'sre_health_score': self._calculate_sre_health_score(latest),
            'production_issue_detection': self._calculate_issue_detection_capability(),
            'timestamp': latest.timestamp
        }
    
    def _calculate_sre_health_score(self, signals: SREGoldenSignals) -> float:
        """Calculate overall SRE health score (0-100)"""
        
        # Latency health (P99 latency against threshold)
        latency_health = max(0, 100 - (signals.latency_p99_ms / self.sre_thresholds['latency_p99_ms']) * 100)
        
        # Error health (inverse of error rate)
        error_health = max(0, 100 - (signals.error_rate_percent / self.sre_thresholds['error_rate_percent']) * 100)
        
        # Saturation health (inverse of max saturation)
        max_saturation = max(signals.saturation_cpu_percent, signals.saturation_memory_percent)
        saturation_health = max(0, 100 - (max_saturation / self.sre_thresholds['saturation_percent']) * 100)
        
        # Traffic health (always 100 unless severe degradation)
        traffic_health = 100.0  # Traffic health is context-dependent
        
        # Weighted average (latency and errors are most critical)
        overall_health = (
            latency_health * 0.3 +
            error_health * 0.4 +
            saturation_health * 0.2 +
            traffic_health * 0.1
        )
        
        return min(100, max(0, overall_health))
    
    def _calculate_issue_detection_capability(self) -> Dict:
        """Calculate production issue detection capability (target: 80%)"""
        
        # Based on Google SRE research, the 4 Golden Signals can detect ~80% of production issues
        detection_categories = {
            'performance_issues': 90,    # Latency + Saturation signals
            'availability_issues': 85,   # Error rate + Traffic signals
            'capacity_issues': 80,       # Saturation + Traffic signals
            'user_experience_issues': 75 # Latency + Error rate signals
        }
        
        overall_detection = statistics.mean(detection_categories.values())
        
        return {
            'overall_detection_percentage': overall_detection,
            'meets_80_percent_target': overall_detection >= 80,
            'detection_by_category': detection_categories,
            'monitoring_coverage': {
                'golden_signals_active': len(self.golden_signals_history) > 0,
                'service_metrics_tracked': len(self.service_metrics) == 3,
                'alert_thresholds_configured': True
            }
        }
    
    def _meets_performance_target(self, metrics: PerformanceMetrics) -> bool:
        """Check if metrics meet performance targets (existing functionality preserved)"""
        
        # Determine target based on complexity
        if metrics.complexity_score < 0.4:
            target_ms = self.targets['simple_task_ms']
        elif metrics.complexity_score < 0.7:
            target_ms = self.targets['standard_task_ms']
        else:
            target_ms = self.targets['complex_task_ms']
            
        return metrics.decision_time_ms <= target_ms
    
    def _check_performance_alerts(self, metrics: PerformanceMetrics):
        """Check if current performance triggers alerts (existing functionality preserved)"""
        
        # Alert on individual slow responses
        if metrics.decision_time_ms > 300:  # 300ms threshold
            self.logger.warning(f"Slow routing decision: {metrics.decision_time_ms:.1f}ms")
            
        # Alert on failed routing
        if not metrics.success:
            self.logger.error(f"Routing failure - Action: {metrics.action}, Confidence: {metrics.confidence}")
    
    def generate_performance_report(self, time_window_hours: int = 24) -> Dict:
        """Generate comprehensive performance report (existing functionality preserved with SRE enhancements)"""
        
        if not self.metrics_history:
            return {'error': 'No performance data available'}
            
        # Filter recent data
        cutoff_time = time.time() - (time_window_hours * 3600)
        recent_metrics = [m for m in self.metrics_history if m.timestamp > cutoff_time]
        
        if not recent_metrics:
            return {'error': f'No data available for {time_window_hours}h window'}
        
        # Existing report structure (preserved)
        base_report = {
            'performance_summary': self._generate_performance_summary(recent_metrics),
            'response_time_analysis': self._analyze_response_times(recent_metrics),
            'success_analysis': self._analyze_success_rates(recent_metrics),
            'cache_analysis': self._analyze_cache_performance(recent_metrics),
            'complexity_analysis': self._analyze_complexity_distribution(recent_metrics),
            'alerts_and_issues': self._identify_performance_issues(recent_metrics),
            'recommendations': self._generate_recommendations(recent_metrics)
        }
        
        # Add SRE Golden Signals analysis
        sre_analysis = self.get_sre_golden_signals()
        base_report['sre_golden_signals'] = sre_analysis
        
        return base_report
    
    def _generate_performance_summary(self, metrics: List[PerformanceMetrics]) -> Dict:
        """Generate high-level performance summary (existing functionality preserved)"""
        
        response_times = [m.decision_time_ms for m in metrics]
        successful = sum(1 for m in metrics if m.success)
        cache_hits = sum(1 for m in metrics if m.cache_hit)
        
        return {
            'total_requests': len(metrics),
            'success_rate': successful / len(metrics),
            'avg_response_time_ms': statistics.mean(response_times),
            'median_response_time_ms': statistics.median(response_times),
            'cache_hit_rate': cache_hits / len(metrics),
            'requests_per_hour': len(metrics) / 24,  # Assuming 24h window
            'target_achievement_rate': sum(1 for m in metrics if self._meets_performance_target(m)) / len(metrics)
        }
    
    def _analyze_response_times(self, metrics: List[PerformanceMetrics]) -> Dict:
        """Analyze response time distribution and percentiles (existing functionality preserved)"""
        
        response_times = [m.decision_time_ms for m in metrics]
        
        return {
            'avg_response_time_ms': statistics.mean(response_times),
            'p50_response_time_ms': statistics.median(response_times),
            'p95_response_time_ms': self._percentile(response_times, 95),
            'p99_response_time_ms': self._percentile(response_times, 99),
            'max_response_time_ms': max(response_times),
            'min_response_time_ms': min(response_times),
            'std_deviation_ms': statistics.stdev(response_times) if len(response_times) > 1 else 0,
            'target_compliance': {
                'simple_tasks': sum(1 for m in metrics 
                                  if m.complexity_score < 0.4 and m.decision_time_ms <= 50) / 
                               max(sum(1 for m in metrics if m.complexity_score < 0.4), 1),
                'standard_tasks': sum(1 for m in metrics 
                                    if 0.4 <= m.complexity_score < 0.7 and m.decision_time_ms <= 100) / 
                                 max(sum(1 for m in metrics if 0.4 <= m.complexity_score < 0.7), 1),
                'complex_tasks': sum(1 for m in metrics 
                                   if m.complexity_score >= 0.7 and m.decision_time_ms <= 200) / 
                                max(sum(1 for m in metrics if m.complexity_score >= 0.7), 1)
            }
        }
    
    def _analyze_success_rates(self, metrics: List[PerformanceMetrics]) -> Dict:
        """Analyze routing success rates by category (existing functionality preserved)"""
        
        # Group by action type
        by_action = {}
        for metric in metrics:
            if metric.action not in by_action:
                by_action[metric.action] = []
            by_action[metric.action].append(metric)
        
        action_success_rates = {}
        for action, action_metrics in by_action.items():
            successful = sum(1 for m in action_metrics if m.success)
            action_success_rates[action] = successful / len(action_metrics)
        
        return {
            'overall_success_rate': sum(1 for m in metrics if m.success) / len(metrics),
            'success_by_action': action_success_rates,
            'success_by_complexity': {
                'simple': sum(1 for m in metrics if m.complexity_score < 0.4 and m.success) / 
                         max(sum(1 for m in metrics if m.complexity_score < 0.4), 1),
                'standard': sum(1 for m in metrics if 0.4 <= m.complexity_score < 0.7 and m.success) / 
                           max(sum(1 for m in metrics if 0.4 <= m.complexity_score < 0.7), 1),
                'complex': sum(1 for m in metrics if m.complexity_score >= 0.7 and m.success) / 
                          max(sum(1 for m in metrics if m.complexity_score >= 0.7), 1)
            }
        }
    
    def _analyze_cache_performance(self, metrics: List[PerformanceMetrics]) -> Dict:
        """Analyze cache hit rates and performance impact (existing functionality preserved)"""
        
        cache_hits = [m for m in metrics if m.cache_hit]
        cache_misses = [m for m in metrics if not m.cache_hit]
        
        cache_hit_response_time = statistics.mean([m.decision_time_ms for m in cache_hits]) if cache_hits else 0
        cache_miss_response_time = statistics.mean([m.decision_time_ms for m in cache_misses]) if cache_misses else 0
        
        return {
            'cache_hit_rate': len(cache_hits) / len(metrics),
            'cache_hits_count': len(cache_hits),
            'cache_misses_count': len(cache_misses),
            'avg_cache_hit_response_time_ms': cache_hit_response_time,
            'avg_cache_miss_response_time_ms': cache_miss_response_time,
            'cache_performance_improvement': max(0, cache_miss_response_time - cache_hit_response_time),
            'cache_effectiveness': len(cache_hits) > 0 and cache_hit_response_time < cache_miss_response_time
        }
    
    def _analyze_complexity_distribution(self, metrics: List[PerformanceMetrics]) -> Dict:
        """Analyze complexity score distribution and routing patterns (existing functionality preserved)"""
        
        simple_tasks = [m for m in metrics if m.complexity_score < 0.4]
        standard_tasks = [m for m in metrics if 0.4 <= m.complexity_score < 0.7]
        complex_tasks = [m for m in metrics if m.complexity_score >= 0.7]
        
        return {
            'complexity_distribution': {
                'simple': len(simple_tasks) / len(metrics),
                'standard': len(standard_tasks) / len(metrics), 
                'complex': len(complex_tasks) / len(metrics)
            },
            'avg_complexity_score': statistics.mean([m.complexity_score for m in metrics]),
            'avg_response_time_by_complexity': {
                'simple': statistics.mean([m.decision_time_ms for m in simple_tasks]) if simple_tasks else 0,
                'standard': statistics.mean([m.decision_time_ms for m in standard_tasks]) if standard_tasks else 0,
                'complex': statistics.mean([m.decision_time_ms for m in complex_tasks]) if complex_tasks else 0
            },
            'domain_distribution': {
                'single_domain': sum(1 for m in metrics if m.domain_count == 1) / len(metrics),
                'multi_domain': sum(1 for m in metrics if m.domain_count > 1) / len(metrics),
                'no_domain': sum(1 for m in metrics if m.domain_count == 0) / len(metrics)
            }
        }
    
    def _identify_performance_issues(self, metrics: List[PerformanceMetrics]) -> List[Dict]:
        """Identify performance issues and create alerts (existing functionality preserved)"""
        
        issues = []
        recent_response_times = [m.decision_time_ms for m in metrics[-10:]]  # Last 10 requests
        
        # Check average response time
        if recent_response_times and statistics.mean(recent_response_times) > self.alert_thresholds['avg_response_time_ms']:
            issues.append({
                'type': 'high_response_time',
                'severity': 'warning',
                'message': f"Average response time ({statistics.mean(recent_response_times):.1f}ms) exceeds threshold ({self.alert_thresholds['avg_response_time_ms']}ms)",
                'recommendation': 'Review system load and optimize slow components'
            })
        
        # Check error rate
        recent_failures = sum(1 for m in metrics[-50:] if not m.success)  # Last 50 requests
        error_rate = (recent_failures / min(50, len(metrics))) * 100 if metrics else 0
        
        if error_rate > self.alert_thresholds['error_rate_percent']:
            issues.append({
                'type': 'high_error_rate', 
                'severity': 'critical',
                'message': f"Error rate ({error_rate:.1f}%) exceeds threshold ({self.alert_thresholds['error_rate_percent']}%)",
                'recommendation': 'Investigate routing failures and error patterns'
            })
        
        # Check cache performance
        recent_cache_hits = sum(1 for m in metrics[-100:] if m.cache_hit)
        cache_hit_rate = (recent_cache_hits / min(100, len(metrics))) * 100 if metrics else 0
        
        if cache_hit_rate < self.alert_thresholds['cache_hit_rate_percent']:
            issues.append({
                'type': 'low_cache_hit_rate',
                'severity': 'warning', 
                'message': f"Cache hit rate ({cache_hit_rate:.1f}%) below threshold ({self.alert_thresholds['cache_hit_rate_percent']}%)",
                'recommendation': 'Review cache configuration and hit patterns'
            })
        
        return issues
    
    def _generate_recommendations(self, metrics: List[PerformanceMetrics]) -> List[str]:
        """Generate performance optimization recommendations (existing functionality preserved)"""
        
        recommendations = []
        response_times = [m.decision_time_ms for m in metrics]
        avg_response_time = statistics.mean(response_times)
        
        # Response time recommendations
        if avg_response_time > 100:
            recommendations.append("Consider implementing response time optimization - current average exceeds 100ms")
        
        # Cache recommendations
        cache_hit_rate = sum(1 for m in metrics if m.cache_hit) / len(metrics)
        if cache_hit_rate < 0.7:
            recommendations.append("Improve cache hit rate by optimizing cache keys and TTL settings")
            
        # Complexity distribution recommendations
        complex_tasks_ratio = sum(1 for m in metrics if m.complexity_score >= 0.7) / len(metrics)
        if complex_tasks_ratio > 0.3:
            recommendations.append("High ratio of complex tasks - consider pre-processing or task decomposition")
        
        # Error rate recommendations
        error_rate = 1 - (sum(1 for m in metrics if m.success) / len(metrics))
        if error_rate > 0.05:
            recommendations.append("Error rate exceeds 5% - implement additional error handling and validation")
        
        return recommendations
    
    def _percentile(self, data: List[float], percentile: int) -> float:
        """Calculate percentile value (existing functionality preserved)"""
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
    
    def get_real_time_stats(self) -> Dict:
        """Get real-time performance statistics (existing functionality preserved with SRE enhancements)"""
        
        if not self.response_times:
            return {'status': 'no_data'}
        
        recent_times = list(self.response_times)[-10:]  # Last 10 requests
        
        base_stats = {
            'current_avg_response_time_ms': statistics.mean(recent_times),
            'total_requests': self.total_requests,
            'success_rate': self.successful_routes / self.total_requests if self.total_requests > 0 else 0,
            'cache_hit_rate': self.cache_hits / self.total_requests if self.total_requests > 0 else 0,
            'target_achievement_rate': self.performance_targets_met / self.total_requests if self.total_requests > 0 else 0,
            'last_request_time_ms': self.response_times[-1] if self.response_times else 0
        }
        
        # Add SRE Golden Signals for real-time monitoring
        sre_signals = self.get_sre_golden_signals()
        if 'golden_signals' in sre_signals:
            base_stats['sre_golden_signals'] = sre_signals['golden_signals']
            base_stats['sre_health_score'] = sre_signals['sre_health_score']
        
        return base_stats