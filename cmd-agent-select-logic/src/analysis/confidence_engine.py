# src/analysis/confidence_engine.py
import time
import hashlib
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import OrderedDict
import threading

@dataclass
class ConfidenceComponents:
    """Individual confidence scoring components"""
    pattern_match: float
    historical_success: float
    context_completeness: float
    resource_availability: float
    total_confidence: float

@dataclass
class CacheEntry:
    """Cache entry with TTL for all cache layers"""
    confidence: ConfidenceComponents
    timestamp: float
    access_count: int
    layer: str = "L1"  # Track which layer this came from

@dataclass
class AdaptiveWeights:
    """Adaptive learning weights for confidence calculation (SGD-based)"""
    pattern_weight: float = 0.4
    historical_weight: float = 0.3
    context_weight: float = 0.2
    resource_weight: float = 0.1
    
    # Adaptive learning parameters (Scikit-learn SGD patterns)
    learning_rate: float = 0.01
    decay: float = 0.001
    iteration: int = 0
    
    def update_weights(self, prediction_error: float, features: Dict[str, float]):
        """Update weights using simple SGD pattern from Scikit-learn
        
        Based on: sklearn.linear_model.SGDRegressor
        Formula: weight = weight - learning_rate * gradient
        """
        
        # Adaptive learning rate decay (standard SGD pattern)
        current_lr = self.learning_rate / (1 + self.decay * self.iteration)
        
        # Simple gradient calculation (prediction error * feature value)
        pattern_gradient = prediction_error * features.get('pattern_match', 0)
        historical_gradient = prediction_error * features.get('historical_success', 0)
        context_gradient = prediction_error * features.get('context_completeness', 0)
        resource_gradient = prediction_error * features.get('resource_availability', 0)
        
        # Weight updates (SGD step)
        self.pattern_weight -= current_lr * pattern_gradient
        self.historical_weight -= current_lr * historical_gradient
        self.context_weight -= current_lr * context_gradient
        self.resource_weight -= current_lr * resource_gradient
        
        # Normalize weights to sum to 1.0 (constraint from research)
        total = self.pattern_weight + self.historical_weight + self.context_weight + self.resource_weight
        if total > 0:
            self.pattern_weight /= total
            self.historical_weight /= total
            self.context_weight /= total
            self.resource_weight /= total
        
        self.iteration += 1
    
    def get_weights_dict(self) -> Dict[str, float]:
        """Get current weights as dictionary"""
        return {
            'pattern_weight': self.pattern_weight,
            'historical_weight': self.historical_weight,
            'context_weight': self.context_weight,
            'resource_weight': self.resource_weight,
            'learning_rate': self.learning_rate / (1 + self.decay * self.iteration),
            'iteration': self.iteration
        }

class L1ConfidenceCache:
    """High-performance 3-layer hierarchical cache with proven enterprise patterns
    
    Architecture:
    - L1: Hot cache (1hr TTL, 1000 entries) - Existing performance maintained
    - L2: Pattern cache (30min TTL, 500 entries) - Cache-Aside pattern
    - L3: Recent cache (5min TTL, 200 entries) - Write-Through pattern
    
    Based on AWS ElastiCache, Azure Cache for Redis, Google Cloud Memorystore patterns
    """
    
    def __init__(self, max_entries: int = 1000, ttl_seconds: int = 3600):
        # L1 Cache (existing - PRESERVE ALL FUNCTIONALITY)
        self.max_entries = max_entries
        self.ttl_seconds = ttl_seconds
        self.cache = OrderedDict()
        self.lock = threading.RLock()
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'invalidations': 0
        }
        
        # L2 Cache (Pattern cache - 30min TTL, 500 entries)
        self.l2_max_entries = 500
        self.l2_ttl_seconds = 1800  # 30 minutes
        self.l2_cache = OrderedDict()
        self.l2_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'invalidations': 0
        }
        
        # L3 Cache (Recent cache - 5min TTL, 200 entries)
        self.l3_max_entries = 200
        self.l3_ttl_seconds = 300  # 5 minutes
        self.l3_cache = OrderedDict()
        self.l3_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'invalidations': 0
        }
    
    def _generate_key(self, task_description: str, domain_analysis: Dict, 
                      available_agents: List[str]) -> str:
        """Generate cache key from inputs"""
        key_data = f"{task_description}:{len(domain_analysis.get('domains', []))}:{len(available_agents)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _is_expired(self, timestamp: float, ttl_seconds: int) -> bool:
        """Check if cache entry is expired"""
        return time.time() - timestamp > ttl_seconds
    
    def _l1_get(self, key: str) -> Optional[ConfidenceComponents]:
        """Get from L1 cache (existing logic preserved)"""
        current_time = time.time()
        
        if key in self.cache:
            entry = self.cache[key]
            
            # Check TTL
            if not self._is_expired(entry.timestamp, self.ttl_seconds):
                # Move to end (LRU)
                self.cache.move_to_end(key)
                entry.access_count += 1
                self.stats['hits'] += 1
                return entry.confidence
            else:
                # Expired entry
                del self.cache[key]
                self.stats['invalidations'] += 1
        
        return None
    
    def _l2_get(self, key: str) -> Optional[ConfidenceComponents]:
        """Get from L2 pattern cache (Cache-Aside pattern)"""
        current_time = time.time()
        
        if key in self.l2_cache:
            entry = self.l2_cache[key]
            
            # Check TTL
            if not self._is_expired(entry.timestamp, self.l2_ttl_seconds):
                # Move to end (LRU)
                self.l2_cache.move_to_end(key)
                entry.access_count += 1
                self.l2_stats['hits'] += 1
                return entry.confidence
            else:
                # Expired entry
                del self.l2_cache[key]
                self.l2_stats['invalidations'] += 1
        
        return None
    
    def _l3_get(self, key: str) -> Optional[ConfidenceComponents]:
        """Get from L3 recent cache"""
        current_time = time.time()
        
        if key in self.l3_cache:
            entry = self.l3_cache[key]
            
            # Check TTL
            if not self._is_expired(entry.timestamp, self.l3_ttl_seconds):
                # Move to end (LRU)
                self.l3_cache.move_to_end(key)
                entry.access_count += 1
                self.l3_stats['hits'] += 1
                return entry.confidence
            else:
                # Expired entry
                del self.l3_cache[key]
                self.l3_stats['invalidations'] += 1
        
        return None
    
    def _l1_put(self, key: str, confidence: ConfidenceComponents):
        """Put into L1 cache (existing logic preserved)"""
        current_time = time.time()
        
        # Evict oldest entries if at capacity
        while len(self.cache) >= self.max_entries:
            self.cache.popitem(last=False)
            self.stats['evictions'] += 1
        
        self.cache[key] = CacheEntry(
            confidence=confidence,
            timestamp=current_time,
            access_count=1,
            layer="L1"
        )
    
    def _l2_put(self, key: str, confidence: ConfidenceComponents):
        """Put into L2 pattern cache"""
        current_time = time.time()
        
        # Evict oldest entries if at capacity
        while len(self.l2_cache) >= self.l2_max_entries:
            self.l2_cache.popitem(last=False)
            self.l2_stats['evictions'] += 1
        
        self.l2_cache[key] = CacheEntry(
            confidence=confidence,
            timestamp=current_time,
            access_count=1,
            layer="L2"
        )
    
    def _l3_put(self, key: str, confidence: ConfidenceComponents):
        """Put into L3 recent cache"""
        current_time = time.time()
        
        # Evict oldest entries if at capacity
        while len(self.l3_cache) >= self.l3_max_entries:
            self.l3_cache.popitem(last=False)
            self.l3_stats['evictions'] += 1
        
        self.l3_cache[key] = CacheEntry(
            confidence=confidence,
            timestamp=current_time,
            access_count=1,
            layer="L3"
        )
    
    def get(self, task_description: str, domain_analysis: Dict, 
            available_agents: List[str]) -> Optional[ConfidenceComponents]:
        """Retrieve cached confidence using 3-layer hierarchical lookup (Cache-Aside pattern)"""
        
        key = self._generate_key(task_description, domain_analysis, available_agents)
        
        with self.lock:
            # Check L1 cache first (existing logic preserved)
            l1_result = self._l1_get(key)
            if l1_result:
                return l1_result
            
            # Check L2 pattern cache (Cache-Aside pattern)
            l2_result = self._l2_get(key)
            if l2_result:
                # Promote to L1 (Cache-Aside promotion)
                self._l1_put(key, l2_result)
                return l2_result
            
            # Check L3 recent cache (Cache-Aside pattern)
            l3_result = self._l3_get(key)
            if l3_result:
                # Promote to L2 and L1 (Cache-Aside promotion)
                self._l2_put(key, l3_result)
                self._l1_put(key, l3_result)
                return l3_result
            
            # Cache miss at all levels
            self.stats['misses'] += 1
            self.l2_stats['misses'] += 1
            self.l3_stats['misses'] += 1
            return None
    
    def put(self, task_description: str, domain_analysis: Dict, 
            available_agents: List[str], confidence: ConfidenceComponents):
        """Store confidence using Write-Through pattern to all cache layers"""
        
        key = self._generate_key(task_description, domain_analysis, available_agents)
        
        with self.lock:
            # Write-Through pattern: Write to all levels simultaneously
            self._l1_put(key, confidence)
            self._l2_put(key, confidence)
            self._l3_put(key, confidence)
    
    def get_hit_rate(self) -> float:
        """Calculate overall cache hit rate across all levels"""
        total_hits = self.stats['hits'] + self.l2_stats['hits'] + self.l3_stats['hits']
        total_misses = self.stats['misses']  # Only count final misses
        total_requests = total_hits + total_misses
        return total_hits / total_requests if total_requests > 0 else 0.0
    
    def get_stats(self) -> Dict:
        """Get comprehensive cache statistics for all levels"""
        return {
            'total_entries': len(self.cache) + len(self.l2_cache) + len(self.l3_cache),
            'overall_hit_rate': self.get_hit_rate(),
            'l1_cache': {
                'entries': len(self.cache),
                'hit_rate': self.stats['hits'] / (self.stats['hits'] + self.stats['misses']) if (self.stats['hits'] + self.stats['misses']) > 0 else 0.0,
                **self.stats
            },
            'l2_cache': {
                'entries': len(self.l2_cache),
                'hit_rate': self.l2_stats['hits'] / (self.l2_stats['hits'] + self.l2_stats['misses']) if (self.l2_stats['hits'] + self.l2_stats['misses']) > 0 else 0.0,
                **self.l2_stats
            },
            'l3_cache': {
                'entries': len(self.l3_cache),
                'hit_rate': self.l3_stats['hits'] / (self.l3_stats['hits'] + self.l3_stats['misses']) if (self.l3_stats['hits'] + self.l3_stats['misses']) > 0 else 0.0,
                **self.l3_stats
            }
        }
    
    def clear(self):
        """Clear all cache levels"""
        with self.lock:
            # Clear L1 (existing logic preserved)
            self.cache.clear()
            self.stats = {
                'hits': 0,
                'misses': 0,
                'evictions': 0,
                'invalidations': 0
            }
            
            # Clear L2
            self.l2_cache.clear()
            self.l2_stats = {
                'hits': 0,
                'misses': 0,
                'evictions': 0,
                'invalidations': 0
            }
            
            # Clear L3
            self.l3_cache.clear()
            self.l3_stats = {
                'hits': 0,
                'misses': 0,
                'evictions': 0,
                'invalidations': 0
            }

class ConfidenceEngine:
    """Multi-metric confidence calculation engine with 3-layer hierarchical caching and adaptive learning
    
    Enhanced with SGD-based adaptive learning patterns from Scikit-learn:
    - Simple weight updates based on prediction error
    - Adaptive learning rate with decay
    - Online learning for continuous improvement
    """
    
    def __init__(self):
        self.cache = L1ConfidenceCache()
        self.historical_success_db = {}  # Simplified historical tracking
        self.performance_stats = {
            'calculations': 0,
            'cache_hits': 0,
            'avg_calc_time_ms': 0
        }
        
        # Adaptive Learning (SGD-based, Scikit-learn patterns)
        self.adaptive_weights = AdaptiveWeights()
        self.learning_stats = {
            'weight_updates': 0,
            'prediction_errors': [],
            'accuracy_improvements': 0,
            'weight_evolution': []
        }
    
    def calculate_pattern_confidence(self, task_description: str, 
                                   available_agents: List[str]) -> float:
        """Calculate pattern matching confidence (adaptive weight)"""
        
        # Simplified pattern matching - in production this would use
        # sophisticated NLP and pattern matching algorithms
        task_tokens = set(task_description.lower().split())
        
        max_confidence = 0.0
        for agent in available_agents:
            # Extract agent domain from name (simplified)
            agent_keywords = self._extract_agent_keywords(agent)
            
            # Calculate overlap
            overlap = len(task_tokens.intersection(agent_keywords))
            pattern_score = min(overlap / max(len(task_tokens), 1), 1.0)
            max_confidence = max(max_confidence, pattern_score)
        
        return max_confidence
    
    def calculate_historical_confidence(self, task_signature: str) -> float:
        """Calculate historical success confidence (adaptive weight)"""
        
        # Simplified historical tracking - in production this would use
        # comprehensive success rate tracking
        if task_signature in self.historical_success_db:
            return self.historical_success_db[task_signature]
        
        # Default confidence for new patterns
        return 0.5
    
    def calculate_context_confidence(self, domain_analysis: Dict) -> float:
        """Calculate context completeness confidence (adaptive weight)"""
        
        # Base confidence on domain detection quality
        domains = domain_analysis.get('domains', [])
        if not domains:
            return 0.3  # Low confidence with no domain detection
        
        # Higher confidence with clear primary domain
        primary_confidence = domains[0]['confidence'] if domains else 0.0
        domain_clarity = primary_confidence - (domains[1]['confidence'] if len(domains) > 1 else 0.0)
        
        # Context completeness based on domain clarity and count
        context_score = min(primary_confidence + (domain_clarity * 0.3), 1.0)
        return context_score
    
    def calculate_resource_confidence(self, estimated_tokens: int) -> float:
        """Calculate resource availability confidence (adaptive weight)"""
        
        # Simplified resource availability - in production this would
        # check actual system resources, token quotas, etc.
        if estimated_tokens < 5000:
            return 0.9  # High confidence for simple tasks
        elif estimated_tokens < 15000:
            return 0.7  # Medium confidence for standard tasks
        else:
            return 0.5  # Lower confidence for complex tasks
    
    def _extract_agent_keywords(self, agent_name: str) -> set:
        """Extract keywords from agent name for pattern matching"""
        
        # Simplified keyword extraction
        agent_keywords = {
            '@analyze-screenshot': {'screenshot', 'image', 'visual', 'analyze'},
            '@debug-issue': {'debug', 'fix', 'error', 'issue', 'bug'},
            '@test-automation': {'test', 'testing', 'qa', 'validation', 'automation'},
            '@build-frontend': {'frontend', 'ui', 'component', 'react', 'vue', 'build'},
            '@build-backend': {'backend', 'api', 'server', 'database', 'service', 'build'},
            '@security-auditor': {'security', 'audit', 'vulnerability', 'secure'},
            '@performance-engineer': {'performance', 'optimize', 'speed', 'bottleneck'},
            '@documentation-expert': {'document', 'docs', 'guide', 'readme', 'write'},
            '@deploy-application': {'deploy', 'deployment', 'infrastructure', 'cloud'},
            '@architect-specialist': {'architecture', 'design', 'system', 'scalability'}
        }
        
        return agent_keywords.get(agent_name, set())
    
    def _estimate_tokens(self, task_description: str, domain_count: int) -> int:
        """Estimate token requirements for task"""
        
        base_tokens = len(task_description.split()) * 1.3  # Rough token estimation
        complexity_multiplier = 1 + (domain_count * 0.5)
        
        return int(base_tokens * complexity_multiplier * 200)  # Conservative estimate
    
    def calculate_routing_confidence(self, task_description: str, 
                                   domain_analysis: Dict, 
                                   available_agents: List[str]) -> ConfidenceComponents:
        """Calculate comprehensive routing confidence with 3-layer hierarchical caching and adaptive weights"""
        
        start_time = time.perf_counter()
        
        # Check 3-layer cache first (Cache-Aside + Write-Through patterns)
        cached_confidence = self.cache.get(task_description, domain_analysis, available_agents)
        if cached_confidence:
            self.performance_stats['cache_hits'] += 1
            return cached_confidence
        
        # Calculate individual components
        pattern_confidence = self.calculate_pattern_confidence(task_description, available_agents)
        
        # Create task signature for historical lookup
        task_signature = f"{len(task_description.split())}:{domain_analysis.get('domain_count', 0)}"
        historical_confidence = self.calculate_historical_confidence(task_signature)
        
        context_confidence = self.calculate_context_confidence(domain_analysis)
        
        estimated_tokens = self._estimate_tokens(
            task_description, 
            domain_analysis.get('domain_count', 0)
        )
        resource_confidence = self.calculate_resource_confidence(estimated_tokens)
        
        # Apply adaptive weighting formula (SGD-learned weights)
        total_confidence = (
            pattern_confidence * self.adaptive_weights.pattern_weight +
            historical_confidence * self.adaptive_weights.historical_weight +
            context_confidence * self.adaptive_weights.context_weight +
            resource_confidence * self.adaptive_weights.resource_weight
        )
        
        confidence_components = ConfidenceComponents(
            pattern_match=pattern_confidence,
            historical_success=historical_confidence,
            context_completeness=context_confidence,
            resource_availability=resource_confidence,
            total_confidence=total_confidence
        )
        
        # Store in 3-layer cache using Write-Through pattern
        self.cache.put(task_description, domain_analysis, available_agents, confidence_components)
        
        # Update performance stats
        calc_time_ms = (time.perf_counter() - start_time) * 1000
        self.performance_stats['calculations'] += 1
        self.performance_stats['avg_calc_time_ms'] = (
            (self.performance_stats['avg_calc_time_ms'] * (self.performance_stats['calculations'] - 1) 
             + calc_time_ms) / self.performance_stats['calculations']
        )
        
        return confidence_components
    
    def update_historical_success(self, task_signature: str, success: bool):
        """Update historical success rate for learning (existing functionality preserved)"""
        
        current_rate = self.historical_success_db.get(task_signature, 0.5)
        # Simple exponential moving average
        new_rate = current_rate * 0.8 + (1.0 if success else 0.0) * 0.2
        self.historical_success_db[task_signature] = new_rate
    
    def learn_from_outcome(self, task_description: str, domain_analysis: Dict, 
                          available_agents: List[str], actual_success: bool, 
                          predicted_confidence: float):
        """Learn from routing outcome using SGD-based adaptive learning
        
        Based on Scikit-learn SGD patterns for online learning
        """
        
        # Calculate prediction error (target - prediction)
        target_confidence = 1.0 if actual_success else 0.0
        prediction_error = target_confidence - predicted_confidence
        
        # Extract feature values for gradient calculation
        pattern_confidence = self.calculate_pattern_confidence(task_description, available_agents)
        
        task_signature = f"{len(task_description.split())}:{domain_analysis.get('domain_count', 0)}"
        historical_confidence = self.calculate_historical_confidence(task_signature)
        
        context_confidence = self.calculate_context_confidence(domain_analysis)
        
        estimated_tokens = self._estimate_tokens(task_description, domain_analysis.get('domain_count', 0))
        resource_confidence = self.calculate_resource_confidence(estimated_tokens)
        
        features = {
            'pattern_match': pattern_confidence,
            'historical_success': historical_confidence,
            'context_completeness': context_confidence,
            'resource_availability': resource_confidence
        }
        
        # Update adaptive weights using SGD
        old_weights = self.adaptive_weights.get_weights_dict().copy()
        self.adaptive_weights.update_weights(prediction_error, features)
        
        # Track learning statistics
        self.learning_stats['weight_updates'] += 1
        self.learning_stats['prediction_errors'].append(abs(prediction_error))
        
        # Keep only last 100 errors for statistics
        if len(self.learning_stats['prediction_errors']) > 100:
            self.learning_stats['prediction_errors'] = self.learning_stats['prediction_errors'][-100:]
        
        # Track if accuracy improved (error decreased)
        if len(self.learning_stats['prediction_errors']) > 1:
            recent_error = self.learning_stats['prediction_errors'][-1]
            previous_error = self.learning_stats['prediction_errors'][-2]
            if recent_error < previous_error:
                self.learning_stats['accuracy_improvements'] += 1
        
        # Track weight evolution (sample every 10 updates)
        if self.learning_stats['weight_updates'] % 10 == 0:
            self.learning_stats['weight_evolution'].append({
                'iteration': self.adaptive_weights.iteration,
                'weights': self.adaptive_weights.get_weights_dict().copy(),
                'avg_error': sum(self.learning_stats['prediction_errors'][-10:]) / min(10, len(self.learning_stats['prediction_errors']))
            })
        
        # Update historical success database as well
        self.update_historical_success(task_signature, actual_success)
    
    def get_learning_stats(self) -> Dict:
        """Get adaptive learning statistics"""
        
        recent_errors = self.learning_stats['prediction_errors'][-20:] if self.learning_stats['prediction_errors'] else []
        avg_recent_error = sum(recent_errors) / len(recent_errors) if recent_errors else 0.0
        
        accuracy_rate = (self.learning_stats['accuracy_improvements'] / 
                        max(self.learning_stats['weight_updates'] - 1, 1)) if self.learning_stats['weight_updates'] > 1 else 0.0
        
        return {
            'adaptive_learning': {
                'current_weights': self.adaptive_weights.get_weights_dict(),
                'weight_updates': self.learning_stats['weight_updates'],
                'avg_recent_error': avg_recent_error,
                'accuracy_improvement_rate': accuracy_rate,
                'learning_progress': len(self.learning_stats['weight_evolution']),
                'target_accuracy_improvement': '20-30%'  # Target from requirements
            },
            'learning_effectiveness': {
                'error_trend': 'decreasing' if len(recent_errors) > 5 and recent_errors[-1] < recent_errors[0] else 'stable',
                'weight_stability': 'converging' if self.adaptive_weights.iteration > 50 else 'learning',
                'meets_target': accuracy_rate >= 0.20  # 20% minimum improvement
            }
        }
    
    def get_performance_stats(self) -> Dict:
        """Get confidence engine performance statistics with 3-layer cache metrics and adaptive learning"""
        
        cache_stats = self.cache.get_stats()
        learning_stats = self.get_learning_stats()
        
        return {
            'confidence_engine': self.performance_stats,
            'hierarchical_cache': cache_stats,
            'meets_target_hit_rate': cache_stats['overall_hit_rate'] >= 0.6,
            'cache_layers': {
                'l1_performance': f"TTL: 1hr, Entries: {cache_stats['l1_cache']['entries']}, Hit Rate: {cache_stats['l1_cache']['hit_rate']:.2f}",
                'l2_performance': f"TTL: 30min, Entries: {cache_stats['l2_cache']['entries']}, Hit Rate: {cache_stats['l2_cache']['hit_rate']:.2f}",
                'l3_performance': f"TTL: 5min, Entries: {cache_stats['l3_cache']['entries']}, Hit Rate: {cache_stats['l3_cache']['hit_rate']:.2f}",
                'total_improvement': f"3-layer hit rate: {cache_stats['overall_hit_rate']:.2f} vs L1-only: {cache_stats['l1_cache']['hit_rate']:.2f}"
            },
            'adaptive_learning': learning_stats['adaptive_learning'],
            'learning_effectiveness': learning_stats['learning_effectiveness']
        }
    
    def clear_cache(self):
        """Clear all cache levels for testing/maintenance"""
        self.cache.clear()
    
    def reset_learning(self):
        """Reset adaptive learning weights for testing/maintenance"""
        self.adaptive_weights = AdaptiveWeights()
        self.learning_stats = {
            'weight_updates': 0,
            'prediction_errors': [],
            'accuracy_improvements': 0,
            'weight_evolution': []
        }