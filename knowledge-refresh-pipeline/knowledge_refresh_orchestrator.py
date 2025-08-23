#!/usr/bin/env python3
"""
Knowledge Refresh Orchestrator - Main Entry Point
Automated knowledge refresh cycles for enhanced agents with comprehensive monitoring and performance optimization.
"""

import asyncio
import argparse
import logging
import sys
import yaml
import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import signal

# Import orchestration components
from orchestration.brainpod_orchestrator import BrainpodOrchestrator, RefreshJob, RefreshPriority, RefreshStatus
from orchestration.chroma_coordinator import ChromaCoordinator
from orchestration.qdrant_manager import QdrantManager
from orchestration.redis_cache import RedisCache
from pipelines.source_monitor import SourceMonitor
from pipelines.quality_validator import QualityValidator
from monitoring.refresh_monitor import RefreshMonitor, AlertSeverity

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('knowledge_refresh.log')
    ]
)
logger = logging.getLogger(__name__)

class KnowledgeRefreshOrchestrator:
    """
    Main orchestrator for automated knowledge refresh cycles with performance optimization.
    Coordinates BRAINPOD components, scheduling, monitoring, and performance optimization.
    """
    
    def __init__(self, config_path: str = None):
        """Initialize the orchestrator with configuration"""
        self.config = self._load_configuration(config_path)
        self.shutdown_requested = False
        self._start_time = datetime.now()
        
        # Initialize components
        self.brainpod = BrainpodOrchestrator(self.config.get('infrastructure', {}).get('brainpod', {}))
        self.monitor = RefreshMonitor(self.config.get('global_settings', {}).get('monitoring', {}))
        
        # Scheduled jobs tracking
        self.scheduled_jobs = {}
        self.active_jobs = {}
        
        logger.info("KnowledgeRefreshOrchestrator initialized with performance optimization")

    def _load_configuration(self, config_path: str = None) -> Dict:
        """Load configuration from YAML file"""
        if config_path is None:
            config_path = Path(__file__).parent / "config" / "refresh_schedules.yaml"
        
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            logger.info(f"Configuration loaded from {config_path}")
            return config
        
        except Exception as e:
            logger.error(f"Failed to load configuration: {str(e)}")
            # Return minimal default configuration
            return {
                'agents': {},
                'global_settings': {
                    'scheduling': {'max_concurrent_refreshes': 1},
                    'quality_gates': {'min_overall_score': 0.85}
                }
            }

    async def start(self) -> None:
        """Start the orchestration system with performance optimization"""
        logger.info("Starting Knowledge Refresh Orchestrator with performance optimization")
        
        try:
            # Setup signal handlers for graceful shutdown
            self._setup_signal_handlers()
            
            # Initialize performance optimization and monitoring
            await self._initialize_performance_optimization()
            
            # Initialize monitoring
            await self._initialize_monitoring()
            
            # Schedule all configured agents
            await self._schedule_all_agents()
            
            # Start main orchestration loop
            await self._run_orchestration_loop()
            
        except Exception as e:
            logger.error(f"Orchestrator startup failed: {str(e)}")
            raise

    async def _initialize_performance_optimization(self) -> None:
        """Initialize performance optimization system"""
        logger.info("Initializing performance optimization")
        
        try:
            # Initialize performance optimizer
            from optimization.performance_optimizer import PerformanceOptimizer
            self.performance_optimizer = PerformanceOptimizer()
            
            # Start comprehensive performance optimization
            optimization_results = await self.performance_optimizer.optimize_system_performance()
            logger.info(f"Performance optimization completed: {optimization_results['total_optimization_time']:.2f}s")
            
            # Start real-time performance monitoring
            asyncio.create_task(self.performance_optimizer.monitor_real_time_performance())
            
            logger.info("Performance optimization initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize performance optimization: {str(e)}")
            # Continue without performance optimization if it fails
            self.performance_optimizer = None

    async def _initialize_monitoring(self) -> None:
        """Initialize monitoring and alerting system"""
        logger.info("Initializing monitoring system")
        
        # Setup notification handlers
        await self._setup_notification_handlers()
        
        # Start monitoring (non-blocking)
        monitoring_task = asyncio.create_task(self.monitor.start_monitoring())
        
        # Verify system health
        health_status = await self.brainpod.get_system_health_status()
        
        if not health_status['overall_status'] == 'healthy':
            logger.warning(f"System health check shows issues: {health_status}")
        
        logger.info("Monitoring system initialized")

    async def _setup_notification_handlers(self) -> None:
        """Setup notification handlers for alerts"""
        
        async def log_alert_handler(alert_data):
            """Log alert to file and console"""
            severity = alert_data['severity'].upper()
            message = alert_data['message']
            timestamp = alert_data['timestamp']
            
            log_message = f"ALERT[{severity}] {timestamp}: {message}"
            
            if severity in ['ERROR', 'CRITICAL']:
                logger.error(log_message)
            elif severity == 'WARNING':
                logger.warning(log_message)
            else:
                logger.info(log_message)
        
        async def webhook_alert_handler(alert_data):
            """Send alert via webhook if configured"""
            webhook_config = (
                self.config.get('global_settings', {})
                .get('notifications', {})
                .get('notification_channels', [])
            )
            
            webhook_url = None
            for channel in webhook_config:
                if channel.get('type') == 'webhook' and channel.get('enabled'):
                    webhook_url = channel.get('url')
                    break
            
            if webhook_url and alert_data['severity'] in ['error', 'critical']:
                try:
                    import aiohttp
                    async with aiohttp.ClientSession() as session:
                        await session.post(webhook_url, json=alert_data, timeout=10)
                    logger.info(f"Alert sent to webhook: {alert_data['alert_id']}")
                except Exception as e:
                    logger.error(f"Failed to send webhook alert: {str(e)}")
        
        # Register notification handlers
        self.monitor.add_notification_handler(log_alert_handler)
        self.monitor.add_notification_handler(webhook_alert_handler)

    async def _schedule_all_agents(self) -> None:
        """Schedule all configured agents for refresh"""
        logger.info("Scheduling agents for automated refresh")
        
        agents_config = self.config.get('agents', {})
        
        for agent_id, agent_config in agents_config.items():
            try:
                # Create refresh job
                job = RefreshJob(
                    job_id=f"{agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    agent_id=agent_id,
                    collections=agent_config.get('knowledge_collections', []),
                    schedule=agent_config.get('refresh_schedule', {}).get('frequency', 'weekly'),
                    priority=RefreshPriority(agent_config.get('refresh_schedule', {}).get('priority', 'normal')),
                    quality_threshold=agent_config.get('refresh_schedule', {}).get('quality_threshold', 0.85),
                    sources=agent_config.get('sources', []),
                    created_at=datetime.now()
                )
                
                # Calculate next run time
                job.next_run = self._calculate_next_run_time(job)
                
                # Store scheduled job
                self.scheduled_jobs[job.job_id] = job
                
                logger.info(f"Scheduled {agent_id} for {job.schedule} refresh (next: {job.next_run})")
                
            except Exception as e:
                logger.error(f"Failed to schedule agent {agent_id}: {str(e)}")

    async def _run_orchestration_loop(self) -> None:
        """Main orchestration loop with performance monitoring"""
        logger.info("Starting main orchestration loop")
        
        while not self.shutdown_requested:
            try:
                # Check for jobs ready to run
                await self._check_scheduled_jobs()
                
                # Monitor active jobs
                await self._monitor_active_jobs()
                
                # Performance health check
                await self._performance_health_check()
                
                # Wait before next cycle
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in orchestration loop: {str(e)}")
                await asyncio.sleep(60)  # Wait longer on error

    async def _check_scheduled_jobs(self) -> None:
        """Check for scheduled jobs ready to run"""
        current_time = datetime.now()
        max_concurrent = self.config.get('global_settings', {}).get('scheduling', {}).get('max_concurrent_refreshes', 2)
        
        # Count active jobs
        active_count = len(self.active_jobs)
        
        for job_id, job in list(self.scheduled_jobs.items()):
            if active_count >= max_concurrent:
                break
                
            if job.next_run and job.next_run <= current_time:
                # Start job
                await self._start_refresh_job(job)
                active_count += 1

    async def _start_refresh_job(self, job: RefreshJob) -> None:
        """Start a knowledge refresh job with performance monitoring"""
        logger.info(f"Starting refresh job for {job.agent_id}")
        
        try:
            # Move to active jobs
            job.status = RefreshStatus.IN_PROGRESS
            job.last_run = datetime.now()
            self.active_jobs[job.job_id] = job
            del self.scheduled_jobs[job.job_id]
            
            # Start job execution with performance monitoring
            asyncio.create_task(self._execute_refresh_job_with_monitoring(job))
            
        except Exception as e:
            logger.error(f"Failed to start refresh job {job.job_id}: {str(e)}")
            job.status = RefreshStatus.FAILED
            job.error_message = str(e)

    async def _execute_refresh_job_with_monitoring(self, job: RefreshJob) -> None:
        """Execute a knowledge refresh job with comprehensive performance monitoring"""
        start_time = time.time()
        
        try:
            logger.info(f"Executing refresh job {job.job_id} for agent {job.agent_id}")
            
            # Pre-execution performance check
            if self.performance_optimizer:
                pre_metrics = await self.performance_optimizer._collect_current_metrics()
                logger.debug(f"Pre-execution metrics: {pre_metrics}")
            
            # Execute refresh with BRAINPOD orchestration
            result = await self.brainpod.execute_knowledge_refresh(job)
            
            # Post-execution performance check
            if self.performance_optimizer:
                post_metrics = await self.performance_optimizer._collect_current_metrics()
                await self.performance_optimizer._check_performance_thresholds(post_metrics)
            
            # Update job status
            if result.get('success', False):
                job.status = RefreshStatus.COMPLETED
                logger.info(f"Refresh job {job.job_id} completed successfully")
            else:
                job.status = RefreshStatus.FAILED
                job.error_message = result.get('error', 'Unknown error')
                logger.error(f"Refresh job {job.job_id} failed: {job.error_message}")
            
            # Calculate next run time
            job.next_run = self._calculate_next_run_time(job)
            
            # Move back to scheduled jobs
            self.scheduled_jobs[job.job_id] = job
            
        except Exception as e:
            logger.error(f"Error executing refresh job {job.job_id}: {str(e)}")
            job.status = RefreshStatus.FAILED
            job.error_message = str(e)
            
        finally:
            # Remove from active jobs
            if job.job_id in self.active_jobs:
                del self.active_jobs[job.job_id]
            
            # Record metrics
            duration = time.time() - start_time
            await self.monitor.record_job_completion(job, duration)

    async def _monitor_active_jobs(self) -> None:
        """Monitor active jobs for performance and health"""
        for job_id, job in self.active_jobs.items():
            # Check for timeout
            if job.last_run:
                elapsed = datetime.now() - job.last_run
                max_duration = timedelta(hours=2)  # Default max duration
                
                if elapsed > max_duration:
                    logger.warning(f"Job {job_id} has been running for {elapsed}, may be stuck")
                    # Could implement job termination logic here

    async def _performance_health_check(self) -> None:
        """Perform performance health check"""
        try:
            # Check if performance optimizer is still running
            if hasattr(self, 'performance_optimizer') and self.performance_optimizer and self.performance_optimizer.monitoring_active:
                # Performance monitoring is active
                pass
            else:
                logger.warning("Performance monitoring not active, restarting...")
                if hasattr(self, 'performance_optimizer') and self.performance_optimizer:
                    asyncio.create_task(self.performance_optimizer.monitor_real_time_performance())
                    
        except Exception as e:
            logger.error(f"Performance health check failed: {str(e)}")

    def _calculate_next_run_time(self, job: RefreshJob) -> datetime:
        """Calculate next run time based on schedule"""
        base_time = job.last_run or datetime.now()
        
        if job.schedule == 'weekly':
            return base_time + timedelta(weeks=1)
        elif job.schedule == 'bi-weekly':
            return base_time + timedelta(weeks=2)
        elif job.schedule == 'monthly':
            return base_time + timedelta(days=30)
        elif job.schedule == 'daily':
            return base_time + timedelta(days=1)
        else:
            # Default to weekly
            return base_time + timedelta(weeks=1)

    def _setup_signal_handlers(self) -> None:
        """Setup signal handlers for graceful shutdown"""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, initiating graceful shutdown")
        self.shutdown_requested = True
        
        # Stop performance monitoring
        if hasattr(self, 'performance_optimizer') and self.performance_optimizer:
            self.performance_optimizer.stop_monitoring()

    async def force_refresh_agent(self, agent_id: str) -> Dict[str, Any]:
        """Force immediate refresh for specific agent"""
        logger.info(f"Forcing immediate refresh for agent {agent_id}")
        
        # Get agent configuration
        agent_config = self.config.get('agents', {}).get(agent_id)
        if not agent_config:
            raise ValueError(f"Agent {agent_id} not found in configuration")
        
        # Create immediate refresh job
        job = RefreshJob(
            job_id=f"{agent_id}_force_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            agent_id=agent_id,
            collections=agent_config.get('knowledge_collections', []),
            schedule='immediate',
            priority=RefreshPriority.CRITICAL,
            quality_threshold=agent_config.get('refresh_schedule', {}).get('quality_threshold', 0.85),
            sources=agent_config.get('sources', []),
            created_at=datetime.now()
        )
        
        # Execute immediately with performance monitoring
        await self._execute_refresh_job_with_monitoring(job)
        
        return {
            'job_id': job.job_id,
            'status': job.status.value,
            'agent_id': agent_id,
            'forced_refresh': True
        }

    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status including performance metrics"""
        return {
            'orchestrator_status': 'running' if not self.shutdown_requested else 'shutting_down',
            'scheduled_jobs': len(self.scheduled_jobs),
            'active_jobs': len(self.active_jobs),
            'performance_monitoring': hasattr(self, 'performance_optimizer') and self.performance_optimizer and self.performance_optimizer.monitoring_active,
            'uptime_seconds': (datetime.now() - self._start_time).total_seconds(),
            'last_health_check': datetime.now().isoformat(),
            'scheduled_jobs_details': [
                {
                    'job_id': job.job_id,
                    'agent_id': job.agent_id,
                    'next_run': job.next_run.isoformat() if job.next_run else None,
                    'priority': job.priority.value
                }
                for job in self.scheduled_jobs.values()
            ],
            'active_jobs_details': [
                {
                    'job_id': job.job_id,
                    'agent_id': job.agent_id,
                    'started': job.last_run.isoformat() if job.last_run else None,
                    'status': job.status.value
                }
                for job in self.active_jobs.values()
            ]
        }

    async def generate_performance_report(self, hours: int = 24) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        logger.info(f"Generating performance report for last {hours} hours")
        
        if hasattr(self, 'performance_optimizer') and self.performance_optimizer:
            return await self.performance_optimizer._generate_performance_report({
                'time_range_hours': hours,
                'report_type': 'comprehensive'
            })
        else:
            return {
                'error': 'Performance optimizer not initialized',
                'status': 'unavailable'
            }


async def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='Knowledge Refresh Orchestrator with Performance Optimization')
    parser.add_argument('--daemon', action='store_true', help='Run as daemon')
    parser.add_argument('--agent', type=str, help='Force refresh specific agent')
    parser.add_argument('--force', action='store_true', help='Force immediate refresh')
    parser.add_argument('--status', action='store_true', help='Show system status')
    parser.add_argument('--report', type=int, help='Generate performance report (hours)')
    parser.add_argument('--config', type=str, help='Configuration file path')
    
    args = parser.parse_args()
    
    try:
        # Initialize orchestrator
        orchestrator = KnowledgeRefreshOrchestrator(args.config)
        
        if args.status:
            # Show system status
            status = await orchestrator.get_system_status()
            print(json.dumps(status, indent=2))
            
        elif args.report:
            # Generate performance report
            report = await orchestrator.generate_performance_report(args.report)
            print(json.dumps(report, indent=2))
            
        elif args.agent and args.force:
            # Force refresh specific agent
            result = await orchestrator.force_refresh_agent(args.agent)
            print(json.dumps(result, indent=2))
            
        elif args.daemon:
            # Run as daemon
            logger.info("Starting Knowledge Refresh Orchestrator in daemon mode")
            await orchestrator.start()
            
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())