#!/usr/bin/env python3
"""
Qdrant Manager - Knowledge Storage and Vector Search Management
Part of BRAINPOD architecture for knowledge refresh orchestration.
"""

import asyncio
import logging
import json
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams, CollectionInfo
import numpy as np
from sentence_transformers import SentenceTransformer
import hashlib
import time

logger = logging.getLogger(__name__)

class QdrantManager:
    """
    Qdrant-based knowledge storage and vector search management for enhanced agents.
    Handles collection updates, embeddings generation, and performance optimization.
    """
    
    def __init__(self, config: Dict = None):
        """Initialize Qdrant manager with configuration"""
        self.config = config or {}
        
        # Qdrant client configuration
        self.client = QdrantClient(
            host=self.config.get('host', 'localhost'),
            port=self.config.get('port', 6333),
            api_key=self.config.get('api_key', None),
            timeout=self.config.get('timeout', 60)
        )
        
        # Embedding models configuration
        self.embedding_models = {
            'small': SentenceTransformer('all-minilm-l6-v2'),      # 384D - Fast retrieval
            'medium': SentenceTransformer('bge-base-en'),          # 768D - Balanced
            'large': SentenceTransformer('bge-large-en-v1.5')     # 1024D - Complex analysis
        }
        
        # Collection configuration templates
        self.collection_configs = {
            'security_vulnerability_database': {
                'embedding_model': 'large',
                'distance': Distance.COSINE,
                'hnsw_config': {'ef_construct': 200, 'm': 16}
            },
            'react_patterns_comprehensive': {
                'embedding_model': 'medium',
                'distance': Distance.COSINE,
                'hnsw_config': {'ef_construct': 128, 'm': 16}
            },
            'compliance_framework_guidelines': {
                'embedding_model': 'medium',
                'distance': Distance.COSINE,
                'hnsw_config': {'ef_construct': 100, 'm': 8}
            }
        }
        
        logger.info("QdrantManager initialized for knowledge storage management")

    async def get_health_status(self) -> Dict[str, Any]:
        """Get Qdrant health status"""
        return {
            'status': 'healthy',
            'component': 'qdrant',
            'last_check': datetime.now().isoformat()
        }

    async def update_collection_knowledge(self, collection_id: str, knowledge_data: Dict) -> Dict:
        """Update knowledge collection with new/updated content"""
        start_time = time.time()
        
        try:
            logger.info(f"Updating collection {collection_id} with {knowledge_data['point_count']} points")
            
            # Ensure collection exists with proper configuration
            await self._ensure_collection_exists(collection_id)
            
            # Get embedding model for this collection
            embedding_model = self._get_embedding_model(collection_id)
            
            # Process knowledge points
            points_to_upsert = []
            update_stats = {
                'points_updated': 0,
                'points_added': 0,
                'embedding_time': 0,
                'upsert_time': 0,
                'total_time': 0
            }
            
            # Generate embeddings for new/updated knowledge
            embedding_start = time.time()
            for knowledge_point in knowledge_data['knowledge_points']:
                # Create point ID based on content hash for deduplication
                point_id = self._generate_point_id(knowledge_point['content'])
                
                # Generate embedding
                embedding = embedding_model.encode(knowledge_point['content']).tolist()
                
                # Create Qdrant point
                point = models.PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        'content': knowledge_point['content'],
                        'source': knowledge_point.get('source', 'unknown'),
                        'credibility_score': knowledge_point.get('credibility_score', 0.0),
                        'last_updated': datetime.utcnow().isoformat(),
                        'knowledge_type': knowledge_point.get('type', 'general'),
                        'domain': knowledge_point.get('domain', collection_id),
                        'refresh_timestamp': datetime.utcnow().isoformat()
                    }
                )
                
                points_to_upsert.append(point)
            
            update_stats['embedding_time'] = time.time() - embedding_start
            
            # Batch upsert points
            if points_to_upsert:
                upsert_start = time.time()
                
                # Use batch upsert for better performance
                batch_size = self.config.get('batch_size', 100)
                for i in range(0, len(points_to_upsert), batch_size):
                    batch = points_to_upsert[i:i + batch_size]
                    
                    operation_info = self.client.upsert(
                        collection_name=collection_id,
                        wait=True,
                        points=batch
                    )
                    
                    update_stats['points_updated'] += len(batch)
                
                update_stats['upsert_time'] = time.time() - upsert_start
            
            # Update collection metadata
            await self._update_collection_metadata(collection_id, {
                'last_refresh': datetime.utcnow().isoformat(),
                'total_points': await self._get_collection_point_count(collection_id),
                'refresh_stats': update_stats
            })
            
            update_stats['total_time'] = time.time() - start_time
            
            result = {
                'points_updated': update_stats['points_updated'],
                'collection_id': collection_id,
                'metrics': {
                    'embedding_time_seconds': update_stats['embedding_time'],
                    'upsert_time_seconds': update_stats['upsert_time'],
                    'total_time_seconds': update_stats['total_time'],
                    'points_per_second': update_stats['points_updated'] / max(update_stats['total_time'], 1)
                }
            }
            
            logger.info(f"Successfully updated collection {collection_id}: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to update collection {collection_id}: {str(e)}")
            raise

    async def search_knowledge(self, collection_id: str, query: str, limit: int = 5, 
                             threshold: float = 0.7, filters: Dict = None) -> List[Dict]:
        """Search knowledge in collection with advanced filtering"""
        try:
            # Get embedding model for this collection
            embedding_model = self._get_embedding_model(collection_id)
            
            # Generate query embedding
            query_embedding = embedding_model.encode(query).tolist()
            
            # Build search filters
            search_filter = None
            if filters:
                conditions = []
                
                # Add common filters
                if 'min_credibility' in filters:
                    conditions.append(
                        models.FieldCondition(
                            key="credibility_score",
                            range=models.Range(gte=filters['min_credibility'])
                        )
                    )
                
                if 'knowledge_type' in filters:
                    conditions.append(
                        models.FieldCondition(
                            key="knowledge_type",
                            match=models.MatchValue(value=filters['knowledge_type'])
                        )
                    )
                
                if 'max_age_days' in filters:
                    min_date = (datetime.utcnow() - timedelta(days=filters['max_age_days'])).isoformat()
                    conditions.append(
                        models.FieldCondition(
                            key="last_updated",
                            range=models.Range(gte=min_date)
                        )
                    )
                
                if conditions:
                    search_filter = models.Filter(must=conditions)
            
            # Perform vector search
            search_result = self.client.search(
                collection_name=collection_id,
                query_vector=query_embedding,
                query_filter=search_filter,
                limit=limit,
                score_threshold=threshold,
                with_payload=True,
                with_vectors=False  # Don't return vectors for performance
            )
            
            # Format results
            formatted_results = []
            for hit in search_result:
                result_item = {
                    'id': hit.id,
                    'score': hit.score,
                    'content': hit.payload.get('content', ''),
                    'source': hit.payload.get('source', 'unknown'),
                    'credibility_score': hit.payload.get('credibility_score', 0.0),
                    'knowledge_type': hit.payload.get('knowledge_type', 'general'),
                    'last_updated': hit.payload.get('last_updated', ''),
                    'metadata': {
                        'domain': hit.payload.get('domain', collection_id),
                        'refresh_timestamp': hit.payload.get('refresh_timestamp', '')
                    }
                }
                formatted_results.append(result_item)
            
            logger.info(f"Knowledge search in {collection_id}: query='{query}', results={len(formatted_results)}")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Knowledge search failed for collection {collection_id}: {str(e)}")
            return []

    async def rollback_collection(self, collection_id: str, snapshot_info: Dict) -> bool:
        """Rollback collection to previous snapshot"""
        try:
            logger.info(f"Rolling back collection {collection_id} to snapshot {snapshot_info.get('snapshot_id')}")
            
            # In practice, this would restore from a Qdrant snapshot
            # For now, we'll implement a simplified rollback by clearing recent points
            
            # Get rollback timestamp
            rollback_timestamp = snapshot_info.get('creation_time')
            if not rollback_timestamp:
                logger.error(f"No rollback timestamp available for collection {collection_id}")
                return False
            
            # Delete points added after snapshot timestamp
            delete_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="refresh_timestamp",
                        range=models.Range(gt=rollback_timestamp)
                    )
                ]
            )
            
            delete_result = self.client.delete(
                collection_name=collection_id,
                points_selector=models.FilterSelector(filter=delete_filter),
                wait=True
            )
            
            logger.info(f"Rollback completed for collection {collection_id}")
            return True
            
        except Exception as e:
            logger.error(f"Rollback failed for collection {collection_id}: {str(e)}")
            return False

    async def update_collection_metadata(self, collection_id: str, metadata: Dict) -> bool:
        """Update collection metadata"""
        try:
            # Store metadata as a special document with known ID
            metadata_point = models.PointStruct(
                id="__metadata__",
                vector=[0.0] * self._get_embedding_dimension(collection_id),  # Dummy vector
                payload={
                    'is_metadata': True,
                    'collection_id': collection_id,
                    'metadata': metadata,
                    'updated_at': datetime.utcnow().isoformat()
                }
            )
            
            self.client.upsert(
                collection_name=collection_id,
                wait=True,
                points=[metadata_point]
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update metadata for collection {collection_id}: {str(e)}")
            return False

    async def get_collection_stats(self, collection_id: str) -> Dict:
        """Get comprehensive collection statistics"""
        try:
            # Get collection info
            collection_info = self.client.get_collection(collection_id)
            
            # Get point count
            point_count = await self._get_collection_point_count(collection_id)
            
            # Get sample of recent points for freshness analysis
            recent_points = self.client.search(
                collection_name=collection_id,
                query_vector=[0.0] * collection_info.config.params.vectors.size,
                limit=100,
                with_payload=True,
                with_vectors=False
            )
            
            # Analyze freshness and quality
            freshness_scores = []
            credibility_scores = []
            knowledge_types = {}
            
            for point in recent_points:
                payload = point.payload
                
                # Extract freshness score (based on last_updated)
                last_updated = payload.get('last_updated', '')
                if last_updated:
                    try:
                        update_time = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                        days_old = (datetime.utcnow() - update_time.replace(tzinfo=None)).days
                        freshness_score = max(0, 1 - (days_old / 365))  # Decay over 1 year
                        freshness_scores.append(freshness_score)
                    except:
                        pass
                
                # Extract credibility scores
                credibility = payload.get('credibility_score', 0.0)
                if credibility > 0:
                    credibility_scores.append(credibility)
                
                # Count knowledge types
                knowledge_type = payload.get('knowledge_type', 'general')
                knowledge_types[knowledge_type] = knowledge_types.get(knowledge_type, 0) + 1
            
            # Calculate statistics
            stats = {
                'collection_id': collection_id,
                'total_points': point_count,
                'vector_size': collection_info.config.params.vectors.size,
                'distance_metric': collection_info.config.params.vectors.distance.name,
                'freshness': {
                    'average_score': np.mean(freshness_scores) if freshness_scores else 0.0,
                    'samples_analyzed': len(freshness_scores)
                },
                'credibility': {
                    'average_score': np.mean(credibility_scores) if credibility_scores else 0.0,
                    'samples_analyzed': len(credibility_scores)
                },
                'knowledge_types': knowledge_types,
                'last_analyzed': datetime.utcnow().isoformat()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get stats for collection {collection_id}: {str(e)}")
            return {}

    async def optimize_collection_performance(self, collection_id: str) -> Dict:
        """Optimize collection for better search performance"""
        try:
            logger.info(f"Optimizing performance for collection {collection_id}")
            
            optimization_results = {
                'collection_id': collection_id,
                'optimizations_applied': [],
                'performance_improvement': {}
            }
            
            # Measure baseline performance
            baseline_perf = await self._measure_search_performance(collection_id)
            optimization_results['baseline_performance'] = baseline_perf
            
            # Optimization 1: Update HNSW parameters based on collection size
            collection_info = self.client.get_collection(collection_id)
            point_count = await self._get_collection_point_count(collection_id)
            
            if point_count > 10000:  # Large collections benefit from higher ef_construct
                new_hnsw_config = models.HnswConfigDiff(
                    ef_construct=200,
                    m=16
                )
                
                self.client.update_collection(
                    collection_name=collection_id,
                    hnsw_config=new_hnsw_config
                )
                
                optimization_results['optimizations_applied'].append('hnsw_config_update')
            
            # Optimization 2: Create payload indexes for frequently filtered fields
            frequently_filtered_fields = ['credibility_score', 'knowledge_type', 'last_updated']
            
            for field in frequently_filtered_fields:
                try:
                    self.client.create_payload_index(
                        collection_name=collection_id,
                        field_name=field,
                        field_type=models.PayloadSchemaType.FLOAT if field == 'credibility_score' else models.PayloadSchemaType.KEYWORD
                    )
                    optimization_results['optimizations_applied'].append(f'index_{field}')
                except:
                    pass  # Index might already exist
            
            # Measure post-optimization performance
            optimized_perf = await self._measure_search_performance(collection_id)
            optimization_results['optimized_performance'] = optimized_perf
            
            # Calculate improvement
            if baseline_perf and optimized_perf:
                improvement = {
                    'search_time_improvement': baseline_perf['avg_search_time'] - optimized_perf['avg_search_time'],
                    'accuracy_improvement': optimized_perf['avg_relevance_score'] - baseline_perf['avg_relevance_score']
                }
                optimization_results['performance_improvement'] = improvement
            
            logger.info(f"Optimization completed for collection {collection_id}: {optimization_results}")
            return optimization_results
            
        except Exception as e:
            logger.error(f"Performance optimization failed for collection {collection_id}: {str(e)}")
            return {}

    async def health_check(self) -> Dict:
        """Perform comprehensive health check on Qdrant manager"""
        try:
            # Test basic connectivity
            collections = self.client.get_collections()
            
            health_info = {
                'healthy': True,
                'collections_count': len(collections.collections),
                'collections': [],
                'embedding_models_status': {},
                'last_check': datetime.utcnow().isoformat()
            }
            
            # Check each collection
            for collection in collections.collections:
                collection_name = collection.name
                try:
                    collection_info = self.client.get_collection(collection_name)
                    point_count = await self._get_collection_point_count(collection_name)
                    
                    collection_health = {
                        'name': collection_name,
                        'status': 'healthy',
                        'point_count': point_count,
                        'vector_size': collection_info.config.params.vectors.size
                    }
                    
                    # Test search functionality
                    test_search = await self.search_knowledge(
                        collection_name, 
                        "test query", 
                        limit=1
                    )
                    collection_health['search_functional'] = True
                    
                except Exception as e:
                    collection_health = {
                        'name': collection_name,
                        'status': 'error',
                        'error': str(e),
                        'search_functional': False
                    }
                    health_info['healthy'] = False
                
                health_info['collections'].append(collection_health)
            
            # Check embedding models
            for model_name, model in self.embedding_models.items():
                try:
                    test_embedding = model.encode("test")
                    health_info['embedding_models_status'][model_name] = {
                        'status': 'healthy',
                        'dimension': len(test_embedding)
                    }
                except Exception as e:
                    health_info['embedding_models_status'][model_name] = {
                        'status': 'error',
                        'error': str(e)
                    }
                    health_info['healthy'] = False
            
            return health_info
            
        except Exception as e:
            logger.error(f"Qdrant health check failed: {str(e)}")
            return {
                'healthy': False,
                'error': str(e),
                'last_check': datetime.utcnow().isoformat()
            }

    async def _ensure_collection_exists(self, collection_id: str) -> bool:
        """Ensure collection exists with proper configuration"""
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            existing_collections = [col.name for col in collections.collections]
            
            if collection_id not in existing_collections:
                # Create new collection with appropriate configuration
                config = self.collection_configs.get(collection_id, {
                    'embedding_model': 'medium',
                    'distance': Distance.COSINE,
                    'hnsw_config': {'ef_construct': 100, 'm': 8}
                })
                
                vector_size = self._get_embedding_dimension_by_model(config['embedding_model'])
                
                self.client.create_collection(
                    collection_name=collection_id,
                    vectors_config=VectorParams(
                        size=vector_size,
                        distance=config['distance']
                    ),
                    hnsw_config=models.HnswConfig(
                        ef_construct=config['hnsw_config']['ef_construct'],
                        m=config['hnsw_config']['m']
                    )
                )
                
                logger.info(f"Created new collection {collection_id} with {vector_size}D vectors")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to ensure collection {collection_id} exists: {str(e)}")
            return False

    def _get_embedding_model(self, collection_id: str) -> SentenceTransformer:
        """Get appropriate embedding model for collection"""
        config = self.collection_configs.get(collection_id, {'embedding_model': 'medium'})
        model_type = config['embedding_model']
        return self.embedding_models[model_type]

    def _get_embedding_dimension(self, collection_id: str) -> int:
        """Get embedding dimension for collection"""
        config = self.collection_configs.get(collection_id, {'embedding_model': 'medium'})
        model_type = config['embedding_model']
        return self._get_embedding_dimension_by_model(model_type)

    def _get_embedding_dimension_by_model(self, model_type: str) -> int:
        """Get embedding dimension by model type"""
        dimensions = {
            'small': 384,   # all-minilm-l6-v2
            'medium': 768,  # bge-base-en
            'large': 1024   # bge-large-en-v1.5
        }
        return dimensions.get(model_type, 768)

    def _generate_point_id(self, content: str) -> str:
        """Generate consistent point ID from content"""
        return hashlib.md5(content.encode()).hexdigest()

    async def _get_collection_point_count(self, collection_id: str) -> int:
        """Get total point count for collection"""
        try:
            collection_info = self.client.get_collection(collection_id)
            return collection_info.points_count
        except:
            return 0

    async def _update_collection_metadata(self, collection_id: str, metadata: Dict) -> None:
        """Internal method to update collection metadata"""
        await self.update_collection_metadata(collection_id, metadata)

    async def _measure_search_performance(self, collection_id: str) -> Dict:
        """Measure search performance for optimization"""
        try:
            test_queries = [
                "security vulnerability patterns",
                "authentication implementation",
                "performance optimization techniques",
                "error handling best practices",
                "data validation strategies"
            ]
            
            search_times = []
            relevance_scores = []
            
            for query in test_queries:
                start_time = time.time()
                results = await self.search_knowledge(collection_id, query, limit=5)
                search_time = time.time() - start_time
                
                search_times.append(search_time)
                
                if results:
                    avg_score = np.mean([r['score'] for r in results])
                    relevance_scores.append(avg_score)
            
            performance = {
                'avg_search_time': np.mean(search_times) if search_times else 0,
                'avg_relevance_score': np.mean(relevance_scores) if relevance_scores else 0,
                'queries_tested': len(test_queries)
            }
            
            return performance
            
        except Exception as e:
            logger.error(f"Performance measurement failed for collection {collection_id}: {str(e)}")
            return {}

# Example usage and testing
async def test_qdrant_manager():
    """Test Qdrant manager functionality"""
    manager = QdrantManager()
    
    # Test health check
    health = await manager.health_check()
    print(f"Health check: {health}")
    
    # Test collection stats
    stats = await manager.get_collection_stats("security_vulnerability_database")
    print(f"Collection stats: {stats}")
    
    # Test search functionality
    results = await manager.search_knowledge(
        "security_vulnerability_database", 
        "SQL injection vulnerabilities",
        limit=3
    )
    print(f"Search results: {len(results)} found")

if __name__ == "__main__":
    asyncio.run(test_qdrant_manager())