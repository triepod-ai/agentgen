#!/usr/bin/env python3
"""
Refresh Monitor - Real-time Knowledge Refresh Monitoring and Alerting
Part of the knowledge refresh pipeline monitoring system.
"""

import asyncio
import logging
import json
import time
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import statistics
import aiohttp
from collections import defaultdict, deque

logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class MonitoringMetric(Enum):
    JOB_SUCCESS_RATE = "job_success_rate"
    AVERAGE_JOB_DURATION = "average_job_duration"
    KNOWLEDGE_QUALITY_SCORE = "knowledge_quality_score"
    SOURCE_AVAILABILITY = "source_availability"
    SYSTEM_PERFORMANCE = "system_performance"
    ROLLBACK_FREQUENCY = "rollback_frequency"

@dataclass
class Alert:
    """Alert configuration and state"""
    alert_id: str
    severity: AlertSeverity
    metric: MonitoringMetric
    threshold: float
    message: str
    enabled: bool = True
    last_triggered: Optional[datetime] = None
    trigger_count: int = 0
    cooldown_minutes: int = 30

@dataclass
class MetricValue:
    """Metric measurement with timestamp"""
    metric: MonitoringMetric
    value: float
    timestamp: datetime
    metadata: Dict[str, Any] = None

@dataclass
class MonitoringReport:
    """Comprehensive monitoring report"""
    report_id: str
    generated_at: datetime
    time_range: Dict[str, datetime]
    metrics_summary: Dict[str, Any]
    alerts_summary: Dict[str, Any]
    system_health: Dict[str, Any]
    recommendations: List[str]

class RefreshMonitor:
    """
    Real-time monitoring system for knowledge refresh operations.
    Tracks performance, quality, and system health with intelligent alerting.
    """
    
    def __init__(self, config: Dict = None):
        """Initialize refresh monitor with configuration"""
        self.config = config or {}
        
        # Monitoring configuration
        self.monitoring_interval = self.config.get('monitoring_interval_seconds', 30)
        self.retention_hours = self.config.get('metrics_retention_hours', 168)  # 1 week
        
        # Metric storage
        self.metrics_history: Dict[MonitoringMetric, deque] = {
            metric: deque(maxlen=1000) for metric in MonitoringMetric
        }
        
        # Alert configuration
        self.alerts = self._load_alert_configuration()
        
        # Active monitoring state
        self.monitoring_active = False
        self.last_health_check = None
        self.system_components = {}
        
        # Performance tracking
        self.performance_baselines = {}
        self.anomaly_detection = {}
        
        # External notification handlers
        self.notification_handlers: List[Callable] = []
        
        # Metrics aggregation
        self.metrics_aggregator = MetricsAggregator(self.config.get('aggregation', {}))
        
        logger.info("RefreshMonitor initialized for real-time monitoring and alerting")

    async def record_job_completion(self, job, duration: float) -> None:
        """Record job completion metrics"""
        logger.info(f"Recording completion for job {job.job_id}, duration: {duration:.2f}s")
        
        # Record metrics
        await self.record_job_metrics(job.job_id, {
            'duration_seconds': duration,
            'status': job.status.value,
            'agent_id': job.agent_id
        })

    def add_notification_handler(self, handler) -> None:
        """Add notification handler"""
        self.notification_handlers.append(handler)
        logger.debug(f"Added notification handler: {handler.__name__}")

    def _load_alert_configuration(self) -> Dict[str, Alert]:
        """Load alert configuration from config"""
        default_alerts = {
            'job_failure_rate_high': Alert(
                alert_id='job_failure_rate_high',
                severity=AlertSeverity.ERROR,
                metric=MonitoringMetric.JOB_SUCCESS_RATE,
                threshold=0.8,  # Alert if success rate drops below 80%
                message="Knowledge refresh job failure rate is high",
                cooldown_minutes=15
            ),
            'job_duration_excessive': Alert(
                alert_id='job_duration_excessive',
                severity=AlertSeverity.WARNING,
                metric=MonitoringMetric.AVERAGE_JOB_DURATION,
                threshold=3600,  # Alert if average duration exceeds 1 hour
                message="Knowledge refresh jobs taking excessive time",
                cooldown_minutes=30
            ),
            'knowledge_quality_degraded': Alert(
                alert_id='knowledge_quality_degraded',
                severity=AlertSeverity.WARNING,
                metric=MonitoringMetric.KNOWLEDGE_QUALITY_SCORE,
                threshold=0.85,  # Alert if quality drops below 85%
                message="Knowledge quality scores have degraded",
                cooldown_minutes=60
            ),
            'source_availability_low': Alert(
                alert_id='source_availability_low',
                severity=AlertSeverity.ERROR,
                metric=MonitoringMetric.SOURCE_AVAILABILITY,
                threshold=0.9,  # Alert if source availability drops below 90%
                message="Knowledge source availability is low",
                cooldown_minutes=20
            ),
            'system_performance_degraded': Alert(
                alert_id='system_performance_degraded',
                severity=AlertSeverity.WARNING,
                metric=MonitoringMetric.SYSTEM_PERFORMANCE,
                threshold=0.7,  # Alert if performance drops below 70% of baseline
                message="System performance has degraded significantly",
                cooldown_minutes=10
            ),
            'rollback_frequency_high': Alert(
                alert_id='rollback_frequency_high',
                severity=AlertSeverity.CRITICAL,
                metric=MonitoringMetric.ROLLBACK_FREQUENCY,
                threshold=0.1,  # Alert if more than 10% of jobs require rollback
                message="High frequency of knowledge refresh rollbacks detected",
                cooldown_minutes=5
            )
        }
        
        # Merge with user-provided alerts
        user_alerts = self.config.get('alerts', {})
        for alert_id, alert_config in user_alerts.items():
            if isinstance(alert_config, dict):
                default_alerts[alert_id] = Alert(**alert_config)
        
        return default_alerts

    async def start_monitoring(self) -> None:
        """Start continuous monitoring"""
        logger.info("Starting continuous monitoring system")
        self.monitoring_active = True
        
        # Start monitoring tasks
        monitoring_tasks = [
            self._metrics_collection_loop(),
            self._health_monitoring_loop(),
            self._alert_evaluation_loop(),
            self._performance_analysis_loop()
        ]
        
        try:
            await asyncio.gather(*monitoring_tasks)
        except Exception as e:
            logger.error(f"Monitoring system error: {str(e)}")
            self.monitoring_active = False

    async def stop_monitoring(self) -> None:
        """Stop continuous monitoring"""
        logger.info("Stopping monitoring system")
        self.monitoring_active = False

    async def record_job_metrics(self, job_id: str, metrics: Dict[str, Any]) -> None:
        """Record metrics from a completed job"""
        timestamp = datetime.utcnow()
        
        # Extract and record individual metrics
        if 'duration_seconds' in metrics:
            await self._record_metric(
                MonitoringMetric.AVERAGE_JOB_DURATION,
                metrics['duration_seconds'],
                timestamp,
                {'job_id': job_id}
            )
        
        if 'quality_score' in metrics:
            await self._record_metric(
                MonitoringMetric.KNOWLEDGE_QUALITY_SCORE,
                metrics['quality_score'],
                timestamp,
                {'job_id': job_id}
            )
        
        # Record job success/failure
        success_rate = 1.0 if not metrics.get('rollback_required', False) else 0.0
        await self._record_metric(
            MonitoringMetric.JOB_SUCCESS_RATE,
            success_rate,
            timestamp,
            {'job_id': job_id}
        )
        
        # Record rollback frequency
        rollback_rate = 1.0 if metrics.get('rollback_required', False) else 0.0
        await self._record_metric(
            MonitoringMetric.ROLLBACK_FREQUENCY,
            rollback_rate,
            timestamp,
            {'job_id': job_id}
        )
        
        logger.debug(f"Recorded metrics for job {job_id}")

    async def record_system_health(self, component: str, health_data: Dict[str, Any]) -> None:
        """Record system component health data"""
        self.system_components[component] = {
            'health_data': health_data,
            'last_update': datetime.utcnow(),
            'healthy': health_data.get('healthy', False)
        }
        
        # Calculate overall system performance metric
        performance_score = await self._calculate_system_performance()
        await self._record_metric(
            MonitoringMetric.SYSTEM_PERFORMANCE,
            performance_score,
            datetime.utcnow(),
            {'component': component}
        )

    async def record_source_availability(self, source_checks: Dict[str, bool]) -> None:
        """Record knowledge source availability"""
        if not source_checks:
            return
        
        available_sources = sum(1 for available in source_checks.values() if available)
        availability_rate = available_sources / len(source_checks)
        
        await self._record_metric(
            MonitoringMetric.SOURCE_AVAILABILITY,
            availability_rate,
            datetime.utcnow(),
            {'sources_checked': len(source_checks), 'available_sources': available_sources}
        )

    async def get_current_metrics(self, time_window_minutes: int = 60) -> Dict[str, Any]:
        """Get current metrics summary for specified time window"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=time_window_minutes)
        
        current_metrics = {}
        
        for metric_type in MonitoringMetric:
            recent_values = [
                mv for mv in self.metrics_history[metric_type]
                if mv.timestamp >= cutoff_time
            ]
            
            if recent_values:
                values = [mv.value for mv in recent_values]
                current_metrics[metric_type.value] = {
                    'current_value': values[-1],
                    'average': statistics.mean(values),
                    'min': min(values),
                    'max': max(values),
                    'count': len(values),
                    'trend': self._calculate_trend(values)
                }
            else:
                current_metrics[metric_type.value] = {
                    'current_value': None,
                    'average': None,
                    'min': None,
                    'max': None,
                    'count': 0,
                    'trend': 'no_data'
                }
        
        return current_metrics

    async def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Get currently active alerts"""
        active_alerts = []
        current_time = datetime.utcnow()
        
        for alert_id, alert in self.alerts.items():
            if not alert.enabled:
                continue
            
            # Check if alert is currently triggered
            is_triggered = await self._evaluate_alert(alert)
            
            if is_triggered:
                # Check cooldown period
                if (alert.last_triggered is None or 
                    (current_time - alert.last_triggered).total_seconds() > alert.cooldown_minutes * 60):
                    
                    active_alerts.append({
                        'alert_id': alert_id,
                        'severity': alert.severity.value,
                        'message': alert.message,
                        'metric': alert.metric.value,
                        'threshold': alert.threshold,
                        'trigger_count': alert.trigger_count,
                        'last_triggered': alert.last_triggered.isoformat() if alert.last_triggered else None
                    })
        
        return active_alerts

    async def generate_monitoring_report(self, hours_back: int = 24) -> MonitoringReport:
        """Generate comprehensive monitoring report"""
        report_id = f"monitor_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        generated_at = datetime.utcnow()
        start_time = generated_at - timedelta(hours=hours_back)
        
        # Get metrics summary
        metrics_summary = await self._generate_metrics_summary(start_time, generated_at)
        
        # Get alerts summary
        alerts_summary = await self._generate_alerts_summary(start_time, generated_at)
        
        # Get system health summary
        system_health = await self._generate_system_health_summary()
        
        # Generate recommendations
        recommendations = await self._generate_recommendations(metrics_summary, alerts_summary)
        
        report = MonitoringReport(
            report_id=report_id,
            generated_at=generated_at,
            time_range={'start': start_time, 'end': generated_at},
            metrics_summary=metrics_summary,
            alerts_summary=alerts_summary,
            system_health=system_health,
            recommendations=recommendations
        )
        
        logger.info(f"Generated monitoring report {report_id} for {hours_back}h period")
        return report

    async def _record_metric(self, metric: MonitoringMetric, value: float, timestamp: datetime, metadata: Dict = None) -> None:
        """Record a metric value"""
        metric_value = MetricValue(
            metric=metric,
            value=value,
            timestamp=timestamp,
            metadata=metadata or {}
        )
        
        self.metrics_history[metric].append(metric_value)
        
        # Aggregate metric for analysis
        await self.metrics_aggregator.process_metric(metric_value)

    async def _metrics_collection_loop(self) -> None:
        """Continuous metrics collection loop"""
        while self.monitoring_active:
            try:
                # Collect system metrics
                await self._collect_system_metrics()
                
                # Wait for next collection cycle
                await asyncio.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Metrics collection error: {str(e)}")
                await asyncio.sleep(self.monitoring_interval)

    async def _health_monitoring_loop(self) -> None:
        """Continuous health monitoring loop"""
        while self.monitoring_active:
            try:
                # Check system component health
                await self._check_component_health()
                
                # Update last health check timestamp
                self.last_health_check = datetime.utcnow()
                
                # Wait for next health check cycle
                await asyncio.sleep(self.monitoring_interval * 2)  # Less frequent than metrics
                
            except Exception as e:
                logger.error(f"Health monitoring error: {str(e)}")
                await asyncio.sleep(self.monitoring_interval)

    async def _alert_evaluation_loop(self) -> None:
        """Continuous alert evaluation loop"""
        while self.monitoring_active:
            try:
                # Evaluate all enabled alerts
                for alert_id, alert in self.alerts.items():
                    if alert.enabled:
                        await self._check_and_trigger_alert(alert)
                
                # Wait for next evaluation cycle
                await asyncio.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Alert evaluation error: {str(e)}")
                await asyncio.sleep(self.monitoring_interval)

    async def _performance_analysis_loop(self) -> None:
        """Continuous performance analysis and anomaly detection"""
        while self.monitoring_active:
            try:
                # Update performance baselines
                await self._update_performance_baselines()
                
                # Run anomaly detection
                await self._detect_performance_anomalies()
                
                # Wait for next analysis cycle
                await asyncio.sleep(self.monitoring_interval * 4)  # Less frequent analysis
                
            except Exception as e:
                logger.error(f"Performance analysis error: {str(e)}")
                await asyncio.sleep(self.monitoring_interval)

    async def _collect_system_metrics(self) -> None:
        """Collect current system metrics"""
        # This would integrate with actual system monitoring
        # For now, simulate metric collection
        pass

    async def _check_component_health(self) -> None:
        """Check health of all system components"""
        # This would check actual component health
        # For now, maintain existing component status
        pass

    async def _check_and_trigger_alert(self, alert: Alert) -> None:
        """Check alert condition and trigger if necessary"""
        is_triggered = await self._evaluate_alert(alert)
        
        if is_triggered:
            current_time = datetime.utcnow()
            
            # Check cooldown period
            if (alert.last_triggered is None or 
                (current_time - alert.last_triggered).total_seconds() > alert.cooldown_minutes * 60):
                
                # Trigger alert
                await self._trigger_alert(alert)
                alert.last_triggered = current_time
                alert.trigger_count += 1
                
                logger.warning(f"Alert triggered: {alert.alert_id} - {alert.message}")

    async def _evaluate_alert(self, alert: Alert) -> bool:
        """Evaluate if an alert condition is met"""
        recent_metrics = self.metrics_history[alert.metric]
        
        if not recent_metrics:
            return False
        
        # Get recent values (last 5 minutes)
        cutoff_time = datetime.utcnow() - timedelta(minutes=5)
        recent_values = [
            mv.value for mv in recent_metrics 
            if mv.timestamp >= cutoff_time
        ]
        
        if not recent_values:
            return False
        
        # Calculate current metric value
        current_value = statistics.mean(recent_values)
        
        # Compare against threshold based on alert type
        if alert.metric in [MonitoringMetric.JOB_SUCCESS_RATE, MonitoringMetric.SOURCE_AVAILABILITY, 
                           MonitoringMetric.KNOWLEDGE_QUALITY_SCORE, MonitoringMetric.SYSTEM_PERFORMANCE]:
            # For these metrics, alert if value drops below threshold
            return current_value < alert.threshold
        else:
            # For other metrics, alert if value exceeds threshold
            return current_value > alert.threshold

    async def _trigger_alert(self, alert: Alert) -> None:
        """Trigger an alert notification"""
        alert_data = {
            'alert_id': alert.alert_id,
            'severity': alert.severity.value,
            'metric': alert.metric.value,
            'message': alert.message,
            'timestamp': datetime.utcnow().isoformat(),
            'threshold': alert.threshold,
            'trigger_count': alert.trigger_count + 1
        }
        
        # Send to all registered notification handlers
        for handler in self.notification_handlers:
            try:
                await handler(alert_data)
            except Exception as e:
                logger.error(f"Notification handler error: {str(e)}")

    async def _calculate_system_performance(self) -> float:
        """Calculate overall system performance score"""
        if not self.system_components:
            return 0.5  # Neutral score if no components
        
        healthy_components = sum(1 for comp in self.system_components.values() if comp['healthy'])
        performance_score = healthy_components / len(self.system_components)
        
        return performance_score

    async def _update_performance_baselines(self) -> None:
        """Update performance baselines for anomaly detection"""
        # Calculate baselines for each metric over the last week
        one_week_ago = datetime.utcnow() - timedelta(days=7)
        
        for metric_type in MonitoringMetric:
            historical_values = [
                mv.value for mv in self.metrics_history[metric_type]
                if mv.timestamp >= one_week_ago
            ]
            
            if len(historical_values) >= 10:  # Need sufficient data
                baseline = {
                    'mean': statistics.mean(historical_values),
                    'std_dev': statistics.stdev(historical_values),
                    'min': min(historical_values),
                    'max': max(historical_values),
                    'updated_at': datetime.utcnow()
                }
                
                self.performance_baselines[metric_type] = baseline

    async def _detect_performance_anomalies(self) -> None:
        """Detect performance anomalies based on historical baselines"""
        current_time = datetime.utcnow()
        recent_window = current_time - timedelta(minutes=10)
        
        for metric_type, baseline in self.performance_baselines.items():
            recent_values = [
                mv.value for mv in self.metrics_history[metric_type]
                if mv.timestamp >= recent_window
            ]
            
            if recent_values and baseline:
                current_mean = statistics.mean(recent_values)
                
                # Check for significant deviation from baseline
                deviation = abs(current_mean - baseline['mean'])
                threshold = baseline['std_dev'] * 2  # 2 sigma threshold
                
                if deviation > threshold:
                    anomaly_data = {
                        'metric': metric_type.value,
                        'current_value': current_mean,
                        'baseline_mean': baseline['mean'],
                        'deviation': deviation,
                        'threshold': threshold,
                        'detected_at': current_time.isoformat()
                    }
                    
                    logger.warning(f"Performance anomaly detected: {anomaly_data}")

    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction for a series of values"""
        if len(values) < 3:
            return 'insufficient_data'
        
        # Simple trend calculation using first and last thirds
        first_third = values[:len(values)//3]
        last_third = values[-len(values)//3:]
        
        first_avg = statistics.mean(first_third)
        last_avg = statistics.mean(last_third)
        
        change_percent = (last_avg - first_avg) / first_avg * 100 if first_avg != 0 else 0
        
        if change_percent > 5:
            return 'increasing'
        elif change_percent < -5:
            return 'decreasing'
        else:
            return 'stable'

    async def _generate_metrics_summary(self, start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """Generate metrics summary for time period"""
        summary = {}
        
        for metric_type in MonitoringMetric:
            period_values = [
                mv for mv in self.metrics_history[metric_type]
                if start_time <= mv.timestamp <= end_time
            ]
            
            if period_values:
                values = [mv.value for mv in period_values]
                summary[metric_type.value] = {
                    'count': len(values),
                    'average': statistics.mean(values),
                    'min': min(values),
                    'max': max(values),
                    'std_dev': statistics.stdev(values) if len(values) > 1 else 0,
                    'trend': self._calculate_trend(values)
                }
            else:
                summary[metric_type.value] = {
                    'count': 0,
                    'average': None,
                    'min': None,
                    'max': None,
                    'std_dev': None,
                    'trend': 'no_data'
                }
        
        return summary

    async def _generate_alerts_summary(self, start_time: datetime, end_time: datetime) -> Dict[str, Any]:
        """Generate alerts summary for time period"""
        return {
            'total_alerts_configured': len(self.alerts),
            'enabled_alerts': len([a for a in self.alerts.values() if a.enabled]),
            'alerts_by_severity': {
                severity.value: len([a for a in self.alerts.values() 
                                   if a.severity == severity and a.enabled])
                for severity in AlertSeverity
            },
            'most_triggered_alerts': [
                {
                    'alert_id': alert_id,
                    'trigger_count': alert.trigger_count,
                    'last_triggered': alert.last_triggered.isoformat() if alert.last_triggered else None
                }
                for alert_id, alert in sorted(self.alerts.items(), 
                                            key=lambda x: x[1].trigger_count, reverse=True)[:5]
            ]
        }

    async def _generate_system_health_summary(self) -> Dict[str, Any]:
        """Generate system health summary"""
        if not self.system_components:
            return {'status': 'no_data', 'components': 0}
        
        healthy_components = [comp for comp in self.system_components.values() if comp['healthy']]
        health_percentage = len(healthy_components) / len(self.system_components) * 100
        
        return {
            'overall_health_percentage': health_percentage,
            'total_components': len(self.system_components),
            'healthy_components': len(healthy_components),
            'unhealthy_components': len(self.system_components) - len(healthy_components),
            'last_health_check': self.last_health_check.isoformat() if self.last_health_check else None,
            'component_status': {
                comp_name: {
                    'healthy': comp['healthy'],
                    'last_update': comp['last_update'].isoformat()
                }
                for comp_name, comp in self.system_components.items()
            }
        }

    async def _generate_recommendations(self, metrics_summary: Dict, alerts_summary: Dict) -> List[str]:
        """Generate monitoring recommendations based on current state"""
        recommendations = []
        
        # Check job success rate
        job_success = metrics_summary.get('job_success_rate', {})
        if job_success.get('average', 1.0) < 0.9:
            recommendations.append(
                "Job success rate is below 90%. Review failed jobs and improve error handling."
            )
        
        # Check average job duration
        job_duration = metrics_summary.get('average_job_duration', {})
        if job_duration.get('average', 0) > 1800:  # 30 minutes
            recommendations.append(
                "Average job duration is high. Consider optimizing knowledge extraction processes."
            )
        
        # Check knowledge quality
        quality_score = metrics_summary.get('knowledge_quality_score', {})
        if quality_score.get('average', 1.0) < 0.85:
            recommendations.append(
                "Knowledge quality scores are declining. Review source credibility and validation rules."
            )
        
        # Check system performance
        system_perf = metrics_summary.get('system_performance', {})
        if system_perf.get('trend') == 'decreasing':
            recommendations.append(
                "System performance is declining. Monitor resource usage and consider scaling."
            )
        
        # Check alert frequency
        total_triggers = sum(alert.trigger_count for alert in self.alerts.values())
        if total_triggers > 10:
            recommendations.append(
                "High alert frequency detected. Review alert thresholds and address root causes."
            )
        
        return recommendations

    def add_notification_handler(self, handler: Callable) -> None:
        """Add notification handler for alerts"""
        self.notification_handlers.append(handler)

    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on refresh monitor"""
        try:
            return {
                'healthy': True,
                'monitoring_active': self.monitoring_active,
                'alerts_configured': len(self.alerts),
                'metrics_tracked': len(MonitoringMetric),
                'system_components': len(self.system_components),
                'last_health_check': self.last_health_check.isoformat() if self.last_health_check else None,
                'notification_handlers': len(self.notification_handlers),
                'last_check': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Refresh monitor health check failed: {str(e)}")
            return {
                'healthy': False,
                'error': str(e),
                'last_check': datetime.utcnow().isoformat()
            }

class MetricsAggregator:
    """Aggregates and analyzes metrics for advanced monitoring"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.aggregated_metrics = defaultdict(list)
    
    async def process_metric(self, metric_value: MetricValue) -> None:
        """Process and aggregate a metric value"""
        # Store for aggregation
        self.aggregated_metrics[metric_value.metric].append(metric_value)
        
        # Keep only recent metrics (last 24 hours)
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        self.aggregated_metrics[metric_value.metric] = [
            mv for mv in self.aggregated_metrics[metric_value.metric]
            if mv.timestamp >= cutoff_time
        ]

# Example usage and testing
async def test_refresh_monitor():
    """Test refresh monitor functionality"""
    
    # Create notification handler
    async def simple_notification_handler(alert_data):
        print(f"ALERT: {alert_data['severity']} - {alert_data['message']}")
    
    monitor = RefreshMonitor()
    monitor.add_notification_handler(simple_notification_handler)
    
    # Test health check
    health = await monitor.health_check()
    print(f"Health check: {health}")
    
    # Simulate recording metrics
    await monitor.record_job_metrics('test_job_1', {
        'duration_seconds': 300,
        'quality_score': 0.92,
        'rollback_required': False
    })
    
    # Get current metrics
    current_metrics = await monitor.get_current_metrics(60)
    print(f"Current metrics: {current_metrics}")
    
    # Generate monitoring report
    report = await monitor.generate_monitoring_report(24)
    print(f"Monitoring report generated: {report.report_id}")

if __name__ == "__main__":
    asyncio.run(test_refresh_monitor())