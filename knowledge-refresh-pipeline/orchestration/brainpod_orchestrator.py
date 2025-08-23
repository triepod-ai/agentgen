#!/usr/bin/env python3
"""
BRAINPOD Orchestration Engine
Coordinates Chroma (workflow tracking) + Qdrant (knowledge storage) + Redis (performance caching)
for automated knowledge refresh cycles.
"""

import asyncio
import logging
import json
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import numpy as np

# Import BRAINPOD components
from .chroma_coordinator import ChromaCoordinator
from .qdrant_manager import QdrantManager
from .redis_cache import RedisCache
from ..pipelines.quality_validator import QualityValidator
from ..pipelines.source_monitor import SourceMonitor

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RefreshStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

class RefreshPriority(Enum):
    CRITICAL = "critical"      # Security updates, vulnerability data
    HIGH = "high"             # Framework updates, major API changes
    NORMAL = "normal"         # Regular updates, documentation refresh
    LOW = "low"              # Minor improvements, optimization

@dataclass
class RefreshJob:
    """Knowledge refresh job configuration"""
    job_id: str
    agent_id: str
    collections: List[str]
    schedule: str  # weekly, bi-weekly, monthly
    priority: RefreshPriority
    quality_threshold: float
    sources: List[str]
    created_at: datetime
    status: RefreshStatus = RefreshStatus.PENDING
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    retry_count: int = 0
    error_message: Optional[str] = None

@dataclass
class RefreshMetrics:
    """Performance and quality metrics for refresh operations"""
    job_id: str
    duration_seconds: float
    knowledge_points_processed: int
    knowledge_points_updated: int
    quality_score: float
    source_freshness: Dict[str, float]
    performance_impact: Dict[str, float]  # Response time changes
    rollback_required: bool = False
    rollback_reason: Optional[str] = None

class BrainpodOrchestrator:
    """
    Main orchestration engine coordinating BRAINPOD components for knowledge refresh
    """
    
    def __init__(self, config_path: str = None):
        """Initialize BRAINPOD orchestrator with configuration"""
        self.config = self._load_config(config_path)
        
        # Initialize BRAINPOD components
        self.chroma = ChromaCoordinator(self.config.get('chroma', {}))
        self.qdrant = QdrantManager(self.config.get('qdrant', {}))
        self.redis = RedisCache(self.config.get('redis', {}))
        self.quality_validator = QualityValidator(self.config.get('quality', {}))
        self.source_monitor = SourceMonitor(self.config.get('sources', {}))
        
        # Internal state
        self.active_jobs: Dict[str, RefreshJob] = {}
        self.job_metrics: Dict[str, RefreshMetrics] = {}
        
        logger.info("BrainpodOrchestrator initialized with BRAINPOD components")

    async def execute_knowledge_refresh(self, job: RefreshJob) -> Dict[str, Any]:
        """Execute knowledge refresh job with performance monitoring"""
        start_time = time.time()
        
        try:
            logger.info(f"Executing knowledge refresh for job {job.job_id}")
            
            # Pre-refresh snapshot for rollback
            snapshot_id = await self._create_rollback_snapshot(job)
            
            # Monitor source changes
            source_changes = await self.source_monitor.check_source_changes(job.sources)
            
            if not source_changes and not hasattr(job, 'force_refresh'):
                logger.info(f"No source changes detected for job {job.job_id}, skipping refresh")
                return {'success': True, 'skipped': True, 'reason': 'no_changes'}
            
            # Process knowledge updates
            processed_knowledge = 0
            updated_knowledge = 0
            
            for collection in job.collections:
                # Simulate knowledge processing
                collection_result = await self._process_collection_knowledge(collection, job)
                processed_knowledge += collection_result.get('processed', 0)
                updated_knowledge += collection_result.get('updated', 0)
            
            # Quality validation
            quality_score = await self.quality_validator.validate_knowledge_quality(job)
            
            if quality_score < job.quality_threshold:
                logger.warning(f"Quality score {quality_score} below threshold {job.quality_threshold}, rolling back")
                await self._rollback_to_snapshot(snapshot_id)
                return {
                    'success': False,
                    'error': f'Quality score {quality_score} below threshold {job.quality_threshold}',
                    'rollback_executed': True
                }
            
            # Update Qdrant collections
            await self.qdrant.update_collection_knowledge(job.collections[0], {
                'point_count': updated_knowledge,
                'knowledge_points': [{'content': f'Updated content {i}'} for i in range(updated_knowledge)]
            })
            
            # Clear relevant Redis cache
            await self.redis.clear_agent_cache(job.agent_id)
            
            # Track in Chroma
            await self.chroma.track_refresh_completion(job.job_id, {
                'duration_seconds': time.time() - start_time,
                'processed_knowledge': processed_knowledge,
                'updated_knowledge': updated_knowledge,
                'quality_score': quality_score
            })
            
            logger.info(f"Knowledge refresh completed for job {job.job_id}")
            
            return {
                'success': True,
                'processed_knowledge': processed_knowledge,
                'updated_knowledge': updated_knowledge,
                'quality_score': quality_score,
                'duration_seconds': time.time() - start_time
            }
            
        except Exception as e:
            logger.error(f"Knowledge refresh failed for job {job.job_id}: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }

    async def get_system_health_status(self) -> Dict[str, Any]:
        """Get comprehensive system health status"""
        try:
            # Check BRAINPOD component health
            chroma_health = await self.chroma.get_health_status()
            qdrant_health = await self.qdrant.get_health_status()
            redis_health = await self.redis.get_health_status()
            
            # Overall health assessment
            component_statuses = [chroma_health['status'], qdrant_health['status'], redis_health['status']]
            overall_status = 'healthy' if all(status == 'healthy' for status in component_statuses) else 'degraded'
            
            return {
                'overall_status': overall_status,
                'components': {
                    'chroma': chroma_health,
                    'qdrant': qdrant_health,
                    'redis': redis_health
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Health status check failed: {str(e)}")
            return {
                'overall_status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    async def _create_rollback_snapshot(self, job: RefreshJob) -> str:
        """Create rollback snapshot before refresh"""
        snapshot_id = f"snapshot_{job.job_id}_{int(time.time())}"
        
        # Simulate snapshot creation
        await asyncio.sleep(0.1)
        
        logger.debug(f"Created rollback snapshot {snapshot_id} for job {job.job_id}")
        return snapshot_id

    async def _rollback_to_snapshot(self, snapshot_id: str) -> None:
        """Rollback to previous snapshot"""
        logger.info(f"Rolling back to snapshot {snapshot_id}")
        
        # Simulate rollback
        await asyncio.sleep(0.5)
        
        logger.info(f"Rollback to snapshot {snapshot_id} completed")

    async def _process_collection_knowledge(self, collection: str, job: RefreshJob) -> Dict[str, int]:
        """Process knowledge for a specific collection"""
        logger.debug(f"Processing knowledge for collection {collection}")
        
        # Simulate knowledge processing
        await asyncio.sleep(0.2)
        
        # Simulate processing results
        processed = np.random.randint(50, 200)
        updated = np.random.randint(10, processed)
        
        return {
            'processed': processed,
            'updated': updated
        }

    def _load_config(self, config_path: str) -> Dict:
        """Load orchestrator configuration"""
        default_config = {
            'max_concurrent_jobs': 3,
            'retry_attempts': 3,
            'rollback_timeout_minutes': 5,
            'performance_monitoring': True,
            'quality_gates': {
                'min_accuracy': 0.95,
                'max_staleness_days': 7,
                'min_source_credibility': 0.90
            }
        }
        
        if config_path:
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception as e:
                logger.warning(f"Failed to load config from {config_path}: {e}")
        
        return default_config

    async def schedule_refresh_job(self, agent_config: Dict) -> str:
        """Schedule a knowledge refresh job for an agent"""
        job_id = self._generate_job_id(agent_config)
        
        job = RefreshJob(
            job_id=job_id,
            agent_id=agent_config['agent_id'],
            collections=agent_config['knowledge_collections'],
            schedule=agent_config['refresh_schedule']['frequency'],
            priority=RefreshPriority(agent_config['refresh_schedule']['priority']),
            quality_threshold=agent_config['refresh_schedule']['quality_threshold'],
            sources=agent_config.get('sources', []),
            created_at=datetime.utcnow(),
            next_run=self._calculate_next_run(agent_config['refresh_schedule'])
        )
        
        # Store job in Chroma for workflow tracking
        await self.chroma.store_job(job)
        self.active_jobs[job_id] = job
        
        logger.info(f"Scheduled refresh job {job_id} for agent {job.agent_id}")
        return job_id

    async def execute_refresh_job(self, job_id: str, force: bool = False) -> RefreshMetrics:
        """Execute a knowledge refresh job with comprehensive monitoring"""
        if job_id not in self.active_jobs:
            raise ValueError(f"Job {job_id} not found in active jobs")
        
        job = self.active_jobs[job_id]
        start_time = datetime.utcnow()
        
        try:
            # Update job status
            job.status = RefreshStatus.IN_PROGRESS
            await self.chroma.update_job_status(job_id, job.status)
            
            logger.info(f"Starting refresh job {job_id} for agent {job.agent_id}")
            
            # Phase 1: Source Monitoring and Change Detection
            source_changes = await self._monitor_source_changes(job)
            if not source_changes and not force:
                logger.info(f"No source changes detected for job {job_id}, skipping refresh")
                job.status = RefreshStatus.COMPLETED
                return self._create_metrics(job, start_time, skip_reason="no_changes")
            
            # Phase 2: Knowledge Extraction and Processing
            extracted_knowledge = await self._extract_knowledge(job, source_changes)
            
            # Phase 3: Quality Validation
            quality_results = await self._validate_knowledge_quality(job, extracted_knowledge)
            if quality_results['score'] < job.quality_threshold:
                raise Exception(f"Quality score {quality_results['score']} below threshold {job.quality_threshold}")
            
            # Phase 4: Vector Embedding and Storage
            embedding_results = await self._update_vector_storage(job, extracted_knowledge)
            
            # Phase 5: Performance Impact Assessment
            performance_impact = await self._assess_performance_impact(job)
            
            # Phase 6: Agent Configuration Update
            await self._update_agent_configuration(job, embedding_results)
            
            # Mark job as completed
            job.status = RefreshStatus.COMPLETED
            job.last_run = datetime.utcnow()
            job.next_run = self._calculate_next_run({'frequency': job.schedule})
            
            # Create comprehensive metrics
            metrics = RefreshMetrics(
                job_id=job_id,
                duration_seconds=(datetime.utcnow() - start_time).total_seconds(),
                knowledge_points_processed=extracted_knowledge['total_points'],
                knowledge_points_updated=embedding_results['updated_points'],
                quality_score=quality_results['score'],
                source_freshness=source_changes.get('freshness_scores', {}),
                performance_impact=performance_impact,
                rollback_required=False
            )
            
            # Store metrics and update job status
            await self.chroma.store_metrics(metrics)
            await self.chroma.update_job_status(job_id, job.status)
            self.job_metrics[job_id] = metrics
            
            logger.info(f"Successfully completed refresh job {job_id}")
            return metrics
            
        except Exception as e:
            # Handle job failure with rollback capability
            logger.error(f"Refresh job {job_id} failed: {str(e)}")
            job.status = RefreshStatus.FAILED
            job.error_message = str(e)
            job.retry_count += 1
            
            # Attempt rollback if needed
            rollback_success = await self._attempt_rollback(job)
            if rollback_success:
                job.status = RefreshStatus.ROLLED_BACK
            
            await self.chroma.update_job_status(job_id, job.status)
            
            # Create failure metrics
            metrics = RefreshMetrics(
                job_id=job_id,
                duration_seconds=(datetime.utcnow() - start_time).total_seconds(),
                knowledge_points_processed=0,
                knowledge_points_updated=0,
                quality_score=0.0,
                source_freshness={},
                performance_impact={},
                rollback_required=True,
                rollback_reason=str(e)
            )
            
            self.job_metrics[job_id] = metrics
            raise

    async def _monitor_source_changes(self, job: RefreshJob) -> Dict:
        """Monitor configured sources for changes requiring refresh"""
        logger.info(f"Monitoring source changes for job {job.job_id}")
        
        changes = {
            'has_changes': False,
            'changed_sources': [],
            'freshness_scores': {},
            'change_summary': {}
        }
        
        # Check each configured source
        for source_id in job.sources:
            source_info = await self.source_monitor.check_source_changes(source_id)
            
            if source_info['has_changes']:
                changes['has_changes'] = True
                changes['changed_sources'].append(source_id)
                changes['change_summary'][source_id] = source_info['changes']
            
            changes['freshness_scores'][source_id] = source_info['freshness_score']
        
        # Store change detection results in Redis cache
        cache_key = f"source_changes:{job.job_id}"
        await self.redis.set_with_expiry(cache_key, changes, 86400)  # 24 hours
        
        return changes

    async def _extract_knowledge(self, job: RefreshJob, source_changes: Dict) -> Dict:
        """Extract and process knowledge from updated sources"""
        logger.info(f"Extracting knowledge for job {job.job_id}")
        
        extracted_knowledge = {
            'total_points': 0,
            'new_points': 0,
            'updated_points': 0,
            'knowledge_by_collection': {},
            'processing_summary': {}
        }
        
        # Process each collection for the agent
        for collection_id in job.collections:
            collection_knowledge = await self.source_monitor.extract_collection_knowledge(
                collection_id, 
                source_changes['changed_sources']
            )
            
            extracted_knowledge['knowledge_by_collection'][collection_id] = collection_knowledge
            extracted_knowledge['total_points'] += collection_knowledge['point_count']
            extracted_knowledge['new_points'] += collection_knowledge['new_count']
            extracted_knowledge['updated_points'] += collection_knowledge['updated_count']
        
        return extracted_knowledge

    async def _validate_knowledge_quality(self, job: RefreshJob, knowledge: Dict) -> Dict:
        """Validate knowledge quality against configured standards"""
        logger.info(f"Validating knowledge quality for job {job.job_id}")
        
        quality_results = await self.quality_validator.comprehensive_validation(
            knowledge,
            {
                'accuracy_threshold': job.quality_threshold,
                'source_credibility_threshold': self.config['quality_gates']['min_source_credibility'],
                'staleness_threshold_days': self.config['quality_gates']['max_staleness_days']
            }
        )
        
        # Store validation results in Chroma
        await self.chroma.store_quality_validation(job.job_id, quality_results)
        
        return quality_results

    async def _update_vector_storage(self, job: RefreshJob, knowledge: Dict) -> Dict:
        """Update Qdrant vector storage with new/updated knowledge"""
        logger.info(f"Updating vector storage for job {job.job_id}")
        
        embedding_results = {
            'updated_points': 0,
            'collections_updated': [],
            'performance_metrics': {}
        }
        
        # Update each knowledge collection
        for collection_id, collection_knowledge in knowledge['knowledge_by_collection'].items():
            # Generate embeddings and update Qdrant
            update_result = await self.qdrant.update_collection_knowledge(
                collection_id, 
                collection_knowledge
            )
            
            embedding_results['updated_points'] += update_result['points_updated']
            embedding_results['collections_updated'].append(collection_id)
            embedding_results['performance_metrics'][collection_id] = update_result['metrics']
        
        return embedding_results

    async def _assess_performance_impact(self, job: RefreshJob) -> Dict:
        """Assess performance impact of knowledge updates"""
        logger.info(f"Assessing performance impact for job {job.job_id}")
        
        # Get baseline performance metrics from Redis cache
        baseline_key = f"performance_baseline:{job.agent_id}"
        baseline_metrics = await self.redis.get(baseline_key)
        
        if not baseline_metrics:
            # If no baseline, create one for future comparisons
            current_metrics = await self._measure_agent_performance(job.agent_id)
            await self.redis.set_with_expiry(baseline_key, current_metrics, 604800)  # 7 days
            return {'impact': 'baseline_established', 'metrics': current_metrics}
        
        # Measure current performance after updates
        current_metrics = await self._measure_agent_performance(job.agent_id)
        
        # Calculate performance impact
        impact_analysis = {
            'embedded_access_time': {
                'before': baseline_metrics.get('embedded_access_ms', 0),
                'after': current_metrics.get('embedded_access_ms', 0),
                'change_percent': self._calculate_percentage_change(
                    baseline_metrics.get('embedded_access_ms', 0),
                    current_metrics.get('embedded_access_ms', 0)
                )
            },
            'qdrant_query_time': {
                'before': baseline_metrics.get('qdrant_query_ms', 0),
                'after': current_metrics.get('qdrant_query_ms', 0),
                'change_percent': self._calculate_percentage_change(
                    baseline_metrics.get('qdrant_query_ms', 0),
                    current_metrics.get('qdrant_query_ms', 0)
                )
            },
            'overall_response_quality': {
                'before': baseline_metrics.get('response_quality_score', 0),
                'after': current_metrics.get('response_quality_score', 0),
                'change_percent': self._calculate_percentage_change(
                    baseline_metrics.get('response_quality_score', 0),
                    current_metrics.get('response_quality_score', 0)
                )
            }
        }
        
        return impact_analysis

    async def _update_agent_configuration(self, job: RefreshJob, embedding_results: Dict) -> None:
        """Update agent configuration with refreshed knowledge references"""
        logger.info(f"Updating agent configuration for job {job.job_id}")
        
        # Update agent metadata with refresh timestamp
        agent_metadata = {
            'last_knowledge_refresh': datetime.utcnow().isoformat(),
            'knowledge_version': self._generate_knowledge_version(job),
            'collections_updated': embedding_results['collections_updated'],
            'refresh_job_id': job.job_id
        }
        
        # Store updated metadata in Redis for quick access
        metadata_key = f"agent_metadata:{job.agent_id}"
        await self.redis.set_with_expiry(metadata_key, agent_metadata, 2592000)  # 30 days
        
        # Update Qdrant collection metadata
        for collection_id in embedding_results['collections_updated']:
            await self.qdrant.update_collection_metadata(collection_id, {
                'last_refresh': datetime.utcnow().isoformat(),
                'refresh_job_id': job.job_id,
                'agent_id': job.agent_id
            })

    async def _attempt_rollback(self, job: RefreshJob) -> bool:
        """Attempt to rollback failed knowledge updates"""
        logger.info(f"Attempting rollback for failed job {job.job_id}")
        
        try:
            # Get rollback information from Chroma
            rollback_info = await self.chroma.get_rollback_info(job.job_id)
            
            if not rollback_info:
                logger.warning(f"No rollback information available for job {job.job_id}")
                return False
            
            # Rollback Qdrant collections
            for collection_id in job.collections:
                rollback_success = await self.qdrant.rollback_collection(
                    collection_id, 
                    rollback_info['snapshots'][collection_id]
                )
                
                if not rollback_success:
                    logger.error(f"Failed to rollback collection {collection_id}")
                    return False
            
            # Clear Redis cache entries related to this job
            cache_keys = [
                f"source_changes:{job.job_id}",
                f"performance_baseline:{job.agent_id}",
                f"agent_metadata:{job.agent_id}"
            ]
            
            for cache_key in cache_keys:
                await self.redis.delete(cache_key)
            
            logger.info(f"Successfully rolled back job {job.job_id}")
            return True
            
        except Exception as e:
            logger.error(f"Rollback failed for job {job.job_id}: {str(e)}")
            return False

    async def get_system_health_status(self) -> Dict:
        """Get comprehensive system health status"""
        health_status = {
            'timestamp': datetime.utcnow().isoformat(),
            'overall_status': 'healthy',
            'components': {},
            'active_jobs': len(self.active_jobs),
            'recent_metrics': {}
        }
        
        # Check BRAINPOD component health
        health_status['components']['chroma'] = await self.chroma.health_check()
        health_status['components']['qdrant'] = await self.qdrant.health_check()
        health_status['components']['redis'] = await self.redis.health_check()
        
        # Determine overall health
        if any(not component['healthy'] for component in health_status['components'].values()):
            health_status['overall_status'] = 'degraded'
        
        # Get recent job metrics
        recent_jobs = sorted(self.job_metrics.items(), key=lambda x: x[1].job_id, reverse=True)[:5]
        health_status['recent_metrics'] = {job_id: asdict(metrics) for job_id, metrics in recent_jobs}
        
        return health_status

    def _generate_job_id(self, agent_config: Dict) -> str:
        """Generate unique job ID based on agent configuration"""
        config_hash = hashlib.md5(
            json.dumps(agent_config, sort_keys=True).encode()
        ).hexdigest()[:8]
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        return f"{agent_config['agent_id']}_{timestamp}_{config_hash}"

    def _calculate_next_run(self, schedule: Dict) -> datetime:
        """Calculate next run time based on schedule configuration"""
        now = datetime.utcnow()
        frequency = schedule['frequency']
        
        if frequency == 'weekly':
            return now + timedelta(weeks=1)
        elif frequency == 'bi-weekly':
            return now + timedelta(weeks=2)
        elif frequency == 'monthly':
            return now + timedelta(days=30)
        elif frequency == 'daily':
            return now + timedelta(days=1)
        else:
            # Default to weekly
            return now + timedelta(weeks=1)

    def _generate_knowledge_version(self, job: RefreshJob) -> str:
        """Generate knowledge version identifier"""
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        return f"{job.agent_id}_v{timestamp}"

    def _calculate_percentage_change(self, old_value: float, new_value: float) -> float:
        """Calculate percentage change between two values"""
        if old_value == 0:
            return 100.0 if new_value > 0 else 0.0
        return ((new_value - old_value) / old_value) * 100

    async def _measure_agent_performance(self, agent_id: str) -> Dict:
        """Measure agent performance metrics"""
        # This would integrate with actual agent testing framework
        # For now, return simulated metrics
        return {
            'embedded_access_ms': 8.5,
            'qdrant_query_ms': 420,
            'context7_integration_ms': 1200,
            'response_quality_score': 0.94,
            'measured_at': datetime.utcnow().isoformat()
        }

    def _create_metrics(self, job: RefreshJob, start_time: datetime, skip_reason: str = None) -> RefreshMetrics:
        """Create metrics object for job completion"""
        return RefreshMetrics(
            job_id=job.job_id,
            duration_seconds=(datetime.utcnow() - start_time).total_seconds(),
            knowledge_points_processed=0,
            knowledge_points_updated=0,
            quality_score=1.0,
            source_freshness={},
            performance_impact={'skip_reason': skip_reason} if skip_reason else {},
            rollback_required=False
        )

# Example usage and testing functions
async def main():
    """Example usage of BRAINPOD orchestrator"""
    orchestrator = BrainpodOrchestrator()
    
    # Example agent configuration
    security_agent_config = {
        'agent_id': 'security-auditor-enhanced',
        'knowledge_collections': [
            'security_vulnerability_database',
            'compliance_framework_guidelines',
            'penetration_testing_methodologies'
        ],
        'refresh_schedule': {
            'frequency': 'weekly',
            'priority': 'critical',
            'quality_threshold': 0.95
        },
        'sources': ['owasp_top_10', 'nist_cybersecurity', 'cve_database']
    }
    
    # Schedule and execute refresh job
    job_id = await orchestrator.schedule_refresh_job(security_agent_config)
    print(f"Scheduled job: {job_id}")
    
    # Execute the refresh
    try:
        metrics = await orchestrator.execute_refresh_job(job_id, force=True)
        print(f"Job completed successfully: {metrics}")
    except Exception as e:
        print(f"Job failed: {e}")
    
    # Check system health
    health = await orchestrator.get_system_health_status()
    print(f"System health: {health}")

if __name__ == "__main__":
    asyncio.run(main())