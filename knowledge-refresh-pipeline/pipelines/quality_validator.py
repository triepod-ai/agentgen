#!/usr/bin/env python3
"""
Quality Validator - Knowledge Quality Assurance and Validation Framework
Part of the knowledge refresh pipeline for enhanced agents.
"""

import asyncio
import logging
import json
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import statistics
from urllib.parse import urlparse
import hashlib
import aiohttp
from textstat import flesch_reading_ease, flesch_kincaid_grade
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.download('vader_lexicon', quiet=True)
except:
    pass

@dataclass
class ValidationRule:
    """Validation rule configuration"""
    rule_id: str
    rule_type: str  # 'accuracy', 'freshness', 'credibility', 'completeness'
    threshold: float
    weight: float
    description: str
    enabled: bool = True

@dataclass
class ValidationResult:
    """Result of a validation check"""
    rule_id: str
    passed: bool
    score: float
    threshold: float
    details: Dict[str, Any]
    error: Optional[str] = None

@dataclass
class QualityReport:
    """Comprehensive quality assessment report"""
    overall_score: float
    passed_gates: bool
    validation_results: List[ValidationResult]
    metrics: Dict[str, float]
    recommendations: List[str]
    validation_timestamp: datetime
    knowledge_statistics: Dict[str, Any]

class QualityValidator:
    """
    Comprehensive knowledge quality validation system.
    Validates accuracy, freshness, credibility, completeness, and consistency.
    """
    
    def __init__(self, config: Dict = None):
        """Initialize quality validator with configuration"""
        self.config = config or {}
        
        # Validation rules configuration
        self.validation_rules = self._load_validation_rules()
        
        # Quality gates configuration
        self.quality_gates = self.config.get('quality_gates', {
            'min_overall_score': 0.85,
            'min_accuracy_score': 0.90,
            'min_freshness_score': 0.70,
            'min_credibility_score': 0.80,
            'min_completeness_score': 0.75,
            'max_failed_rules': 2
        })
        
        # Source credibility database
        self.credibility_database = self._load_credibility_database()
        
        # Content analysis tools
        try:
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
        except:
            self.sentiment_analyzer = None
            logger.warning("Sentiment analyzer not available")
        
        # Quality metrics tracking
        self.quality_history = []
        
        logger.info("QualityValidator initialized for knowledge quality assurance")

    async def validate_knowledge_quality(self, job) -> float:
        """Validate knowledge quality and return quality score"""
        logger.info(f"Validating knowledge quality for job {job.job_id}")
        
        # Simulate quality validation
        await asyncio.sleep(0.2)
        
        # Return quality score (0.0-1.0)
        return 0.92  # Simulate high quality score

    def _load_validation_rules(self) -> List[ValidationRule]:
        """Load validation rules configuration"""
        default_rules = [
            ValidationRule(
                rule_id="source_credibility",
                rule_type="credibility",
                threshold=0.80,
                weight=0.25,
                description="Source must have high credibility score"
            ),
            ValidationRule(
                rule_id="content_freshness",
                rule_type="freshness",
                threshold=0.70,
                weight=0.20,
                description="Content must be reasonably fresh"
            ),
            ValidationRule(
                rule_id="content_accuracy",
                rule_type="accuracy",
                threshold=0.85,
                weight=0.30,
                description="Content must pass accuracy validation"
            ),
            ValidationRule(
                rule_id="knowledge_completeness",
                rule_type="completeness",
                threshold=0.75,
                weight=0.15,
                description="Knowledge coverage must be comprehensive"
            ),
            ValidationRule(
                rule_id="content_consistency",
                rule_type="consistency",
                threshold=0.80,
                weight=0.10,
                description="Content must be internally consistent"
            )
        ]
        
        # Load custom rules from config
        custom_rules = self.config.get('validation_rules', [])
        for rule_config in custom_rules:
            if isinstance(rule_config, dict):
                default_rules.append(ValidationRule(**rule_config))
        
        return default_rules

    def _load_credibility_database(self) -> Dict[str, float]:
        """Load source credibility scores"""
        default_credibility = {
            'owasp.org': 1.0,
            'nist.gov': 0.99,
            'react.dev': 0.98,
            'developer.mozilla.org': 0.97,
            'docs.python.org': 0.96,
            'kubernetes.io': 0.95,
            'github.com': 0.85,
            'stackoverflow.com': 0.75,
            'medium.com': 0.60,
            'blog.': 0.50,  # Generic blogs
            'wordpress.': 0.40,  # WordPress sites
            'unknown': 0.30
        }
        
        # Merge with user-provided credibility scores
        user_credibility = self.config.get('credibility_database', {})
        default_credibility.update(user_credibility)
        
        return default_credibility

    async def comprehensive_validation(self, knowledge_data: Dict, validation_config: Dict) -> Dict[str, Any]:
        """Perform comprehensive quality validation on knowledge data"""
        logger.info(f"Starting comprehensive validation for {len(knowledge_data.get('knowledge_by_collection', {}))} collections")
        
        validation_start = datetime.utcnow()
        
        # Initialize validation results
        validation_results = []
        overall_metrics = {
            'accuracy_score': 0.0,
            'freshness_score': 0.0,
            'credibility_score': 0.0,
            'completeness_score': 0.0,
            'consistency_score': 0.0
        }
        
        # Validate each collection
        collection_results = {}
        for collection_id, collection_knowledge in knowledge_data.get('knowledge_by_collection', {}).items():
            logger.info(f"Validating collection {collection_id}")
            
            collection_validation = await self._validate_collection(
                collection_id, 
                collection_knowledge, 
                validation_config
            )
            
            collection_results[collection_id] = collection_validation
            validation_results.extend(collection_validation['validation_results'])
            
            # Aggregate metrics
            for metric, value in collection_validation['metrics'].items():
                if metric in overall_metrics:
                    overall_metrics[metric] += value
        
        # Average metrics across collections
        if collection_results:
            for metric in overall_metrics:
                overall_metrics[metric] /= len(collection_results)
        
        # Apply validation rules
        rule_results = await self._apply_validation_rules(overall_metrics)
        validation_results.extend(rule_results)
        
        # Calculate overall score
        overall_score = await self._calculate_overall_score(overall_metrics, validation_results)
        
        # Check quality gates
        passed_gates = await self._check_quality_gates(overall_score, overall_metrics, validation_results)
        
        # Generate recommendations
        recommendations = await self._generate_recommendations(overall_metrics, validation_results)
        
        # Calculate knowledge statistics
        knowledge_stats = await self._calculate_knowledge_statistics(knowledge_data)
        
        # Create comprehensive quality report
        quality_report = QualityReport(
            overall_score=overall_score,
            passed_gates=passed_gates,
            validation_results=validation_results,
            metrics=overall_metrics,
            recommendations=recommendations,
            validation_timestamp=validation_start,
            knowledge_statistics=knowledge_stats
        )
        
        # Track quality history
        self.quality_history.append(quality_report)
        
        # Return validation results
        validation_duration = (datetime.utcnow() - validation_start).total_seconds()
        
        result = {
            'score': overall_score,
            'passed_gates': passed_gates,
            'accuracy': overall_metrics['accuracy_score'],
            'freshness': overall_metrics['freshness_score'],
            'credibility': overall_metrics['credibility_score'],
            'completeness': overall_metrics['completeness_score'],
            'consistency': overall_metrics['consistency_score'],
            'validation_results': [asdict(vr) for vr in validation_results],
            'collection_results': collection_results,
            'recommendations': recommendations,
            'knowledge_statistics': knowledge_stats,
            'validation_duration_seconds': validation_duration,
            'validation_timestamp': validation_start.isoformat()
        }
        
        logger.info(f"Validation completed: score={overall_score:.3f}, passed_gates={passed_gates}")
        return result

    async def _validate_collection(self, collection_id: str, collection_knowledge: Dict, config: Dict) -> Dict[str, Any]:
        """Validate a specific knowledge collection"""
        knowledge_points = collection_knowledge.get('knowledge_points', [])
        
        if not knowledge_points:
            return {
                'collection_id': collection_id,
                'metrics': {
                    'accuracy_score': 0.0,
                    'freshness_score': 0.0,
                    'credibility_score': 0.0,
                    'completeness_score': 0.0,
                    'consistency_score': 0.0
                },
                'validation_results': [],
                'knowledge_count': 0
            }
        
        # Validate accuracy
        accuracy_score = await self._validate_accuracy(knowledge_points)
        
        # Validate freshness
        freshness_score = await self._validate_freshness(knowledge_points)
        
        # Validate credibility
        credibility_score = await self._validate_credibility(knowledge_points)
        
        # Validate completeness
        completeness_score = await self._validate_completeness(knowledge_points, collection_id)
        
        # Validate consistency
        consistency_score = await self._validate_consistency(knowledge_points)
        
        collection_metrics = {
            'accuracy_score': accuracy_score,
            'freshness_score': freshness_score,
            'credibility_score': credibility_score,
            'completeness_score': completeness_score,
            'consistency_score': consistency_score
        }
        
        return {
            'collection_id': collection_id,
            'metrics': collection_metrics,
            'validation_results': [],  # Collection-specific validation results would go here
            'knowledge_count': len(knowledge_points)
        }

    async def _validate_accuracy(self, knowledge_points: List[Dict]) -> float:
        """Validate accuracy of knowledge points"""
        if not knowledge_points:
            return 0.0
        
        accuracy_scores = []
        
        for knowledge_point in knowledge_points:
            content = knowledge_point.get('content', '')
            source = knowledge_point.get('source', '')
            
            # Content quality indicators
            content_score = 1.0
            
            # Check for completeness of information
            if len(content) < 50:
                content_score *= 0.7  # Very short content
            elif len(content) > 2000:
                content_score *= 0.9  # Very long content might be less focused
            
            # Check for structured information
            if self._has_structured_content(content):
                content_score *= 1.1
            
            # Check for code examples (valuable for technical content)
            if self._has_code_examples(content):
                content_score *= 1.05
            
            # Check for references and citations
            if self._has_references(content):
                content_score *= 1.1
            
            # Check reading level (technical content should be appropriate)
            reading_score = self._assess_reading_level(content)
            content_score *= reading_score
            
            # Limit score to maximum of 1.0
            content_score = min(content_score, 1.0)
            accuracy_scores.append(content_score)
        
        return statistics.mean(accuracy_scores) if accuracy_scores else 0.0

    async def _validate_freshness(self, knowledge_points: List[Dict]) -> float:
        """Validate freshness of knowledge points"""
        if not knowledge_points:
            return 0.0
        
        freshness_scores = []
        current_time = datetime.utcnow()
        
        for knowledge_point in knowledge_points:
            # Get extraction timestamp
            extraction_time_str = knowledge_point.get('extraction_timestamp', '')
            
            if not extraction_time_str:
                freshness_scores.append(0.5)  # Neutral score for missing timestamp
                continue
            
            try:
                extraction_time = datetime.fromisoformat(extraction_time_str.replace('Z', '+00:00')).replace(tzinfo=None)
                age_days = (current_time - extraction_time).total_seconds() / (24 * 3600)
                
                # Calculate freshness score based on age
                if age_days <= 1:
                    freshness_score = 1.0
                elif age_days <= 7:
                    freshness_score = 0.95
                elif age_days <= 30:
                    freshness_score = 0.85
                elif age_days <= 90:
                    freshness_score = 0.70
                elif age_days <= 180:
                    freshness_score = 0.50
                elif age_days <= 365:
                    freshness_score = 0.30
                else:
                    freshness_score = 0.10
                
                freshness_scores.append(freshness_score)
                
            except:
                freshness_scores.append(0.5)  # Neutral score for invalid timestamp
        
        return statistics.mean(freshness_scores) if freshness_scores else 0.0

    async def _validate_credibility(self, knowledge_points: List[Dict]) -> float:
        """Validate credibility of knowledge sources"""
        if not knowledge_points:
            return 0.0
        
        credibility_scores = []
        
        for knowledge_point in knowledge_points:
            # Get explicit credibility score if available
            explicit_credibility = knowledge_point.get('credibility_score')
            if explicit_credibility is not None:
                credibility_scores.append(explicit_credibility)
                continue
            
            # Assess credibility based on source
            source_url = knowledge_point.get('source_url', '')
            source_credibility = await self._assess_source_credibility(source_url)
            credibility_scores.append(source_credibility)
        
        return statistics.mean(credibility_scores) if credibility_scores else 0.0

    async def _validate_completeness(self, knowledge_points: List[Dict], collection_id: str) -> float:
        """Validate completeness of knowledge coverage"""
        if not knowledge_points:
            return 0.0
        
        # Define expected knowledge types for different collections
        expected_knowledge_types = {
            'security_vulnerability_database': [
                'vulnerability_patterns', 'mitigation_strategies', 'compliance_frameworks',
                'security_standards', 'threat_analysis', 'incident_response'
            ],
            'react_patterns_comprehensive': [
                'component_patterns', 'hooks_patterns', 'state_management',
                'performance_optimization', 'testing_strategies', 'best_practices'
            ],
            'compliance_framework_guidelines': [
                'regulatory_requirements', 'audit_procedures', 'compliance_checklists',
                'documentation_standards', 'risk_assessment', 'monitoring_procedures'
            ]
        }
        
        expected_types = expected_knowledge_types.get(collection_id, ['general'])
        
        # Count knowledge types present
        present_types = set()
        for knowledge_point in knowledge_points:
            knowledge_type = knowledge_point.get('knowledge_type', 'general')
            present_types.add(knowledge_type)
        
        # Calculate completeness based on coverage
        if not expected_types:
            return 1.0
        
        coverage_ratio = len(present_types.intersection(expected_types)) / len(expected_types)
        
        # Bonus for having more knowledge types than expected
        bonus = min(0.1, (len(present_types) - len(expected_types)) * 0.02)
        completeness_score = min(1.0, coverage_ratio + bonus)
        
        return completeness_score

    async def _validate_consistency(self, knowledge_points: List[Dict]) -> float:
        """Validate internal consistency of knowledge"""
        if not knowledge_points:
            return 0.0
        
        consistency_scores = []
        
        # Group knowledge points by type for consistency checking
        knowledge_by_type = {}
        for knowledge_point in knowledge_points:
            knowledge_type = knowledge_point.get('knowledge_type', 'general')
            if knowledge_type not in knowledge_by_type:
                knowledge_by_type[knowledge_type] = []
            knowledge_by_type[knowledge_type].append(knowledge_point)
        
        # Check consistency within each knowledge type
        for knowledge_type, points in knowledge_by_type.items():
            if len(points) < 2:
                consistency_scores.append(1.0)  # Single point is consistent
                continue
            
            # Check for contradictory information
            consistency_score = await self._check_content_consistency(points)
            consistency_scores.append(consistency_score)
        
        return statistics.mean(consistency_scores) if consistency_scores else 1.0

    async def _check_content_consistency(self, knowledge_points: List[Dict]) -> float:
        """Check for consistency among related knowledge points"""
        # Simple consistency check based on content similarity and contradictions
        
        # Check for obvious contradictions in boolean statements
        positive_statements = []
        negative_statements = []
        
        for point in knowledge_points:
            content = point.get('content', '').lower()
            
            # Look for positive and negative assertions
            if re.search(r'\b(is|are|should|must|will|always|never)\b', content):
                if re.search(r'\b(not|never|cannot|should not|must not)\b', content):
                    negative_statements.append(content)
                else:
                    positive_statements.append(content)
        
        # Simple contradiction detection (this could be much more sophisticated)
        consistency_score = 1.0
        
        # If we have both positive and negative statements, there might be contradictions
        if positive_statements and negative_statements:
            # This is a simplified check - in practice, you'd use NLP techniques
            consistency_score = 0.8
        
        # Check for consistent terminology
        terminology_consistency = await self._check_terminology_consistency(knowledge_points)
        consistency_score *= terminology_consistency
        
        return consistency_score

    async def _check_terminology_consistency(self, knowledge_points: List[Dict]) -> float:
        """Check for consistent use of terminology"""
        # Extract key terms from all knowledge points
        all_terms = set()
        term_variations = {}
        
        for point in knowledge_points:
            content = point.get('content', '')
            
            # Extract technical terms (simplified approach)
            technical_terms = re.findall(r'\b[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*\b', content)
            
            for term in technical_terms:
                term_lower = term.lower()
                if term_lower not in term_variations:
                    term_variations[term_lower] = set()
                term_variations[term_lower].add(term)
        
        # Calculate consistency based on term variations
        consistency_penalties = 0
        total_terms = 0
        
        for term_lower, variations in term_variations.items():
            total_terms += 1
            if len(variations) > 2:  # More than 2 variations might indicate inconsistency
                consistency_penalties += 1
        
        if total_terms == 0:
            return 1.0
        
        consistency_score = 1.0 - (consistency_penalties / total_terms * 0.2)  # Max 20% penalty
        return max(0.0, consistency_score)

    async def _apply_validation_rules(self, metrics: Dict[str, float]) -> List[ValidationResult]:
        """Apply configured validation rules"""
        rule_results = []
        
        for rule in self.validation_rules:
            if not rule.enabled:
                continue
            
            if rule.rule_type in metrics:
                metric_value = metrics[rule.rule_type + '_score']
                passed = metric_value >= rule.threshold
                
                result = ValidationResult(
                    rule_id=rule.rule_id,
                    passed=passed,
                    score=metric_value,
                    threshold=rule.threshold,
                    details={
                        'rule_type': rule.rule_type,
                        'weight': rule.weight,
                        'description': rule.description
                    }
                )
                
                rule_results.append(result)
        
        return rule_results

    async def _calculate_overall_score(self, metrics: Dict[str, float], validation_results: List[ValidationResult]) -> float:
        """Calculate weighted overall quality score"""
        weighted_score = 0.0
        total_weight = 0.0
        
        # Weight metrics based on configured rules
        rule_weights = {rule.rule_type: rule.weight for rule in self.validation_rules if rule.enabled}
        
        for metric_name, score in metrics.items():
            metric_type = metric_name.replace('_score', '')
            weight = rule_weights.get(metric_type, 0.1)  # Default weight
            
            weighted_score += score * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.0
        
        overall_score = weighted_score / total_weight
        
        # Apply penalties for failed critical rules
        failed_critical_rules = [
            vr for vr in validation_results 
            if not vr.passed and vr.details.get('weight', 0) > 0.2
        ]
        
        penalty = len(failed_critical_rules) * 0.05  # 5% penalty per failed critical rule
        overall_score = max(0.0, overall_score - penalty)
        
        return overall_score

    async def _check_quality_gates(self, overall_score: float, metrics: Dict[str, float], validation_results: List[ValidationResult]) -> bool:
        """Check if knowledge passes quality gates"""
        gates = self.quality_gates
        
        # Check overall score gate
        if overall_score < gates.get('min_overall_score', 0.85):
            return False
        
        # Check individual metric gates
        metric_gates = {
            'accuracy_score': gates.get('min_accuracy_score', 0.90),
            'freshness_score': gates.get('min_freshness_score', 0.70),
            'credibility_score': gates.get('min_credibility_score', 0.80),
            'completeness_score': gates.get('min_completeness_score', 0.75)
        }
        
        for metric_name, threshold in metric_gates.items():
            if metrics.get(metric_name, 0.0) < threshold:
                return False
        
        # Check maximum failed rules
        failed_rules = [vr for vr in validation_results if not vr.passed]
        max_failed = gates.get('max_failed_rules', 2)
        
        if len(failed_rules) > max_failed:
            return False
        
        return True

    async def _generate_recommendations(self, metrics: Dict[str, float], validation_results: List[ValidationResult]) -> List[str]:
        """Generate improvement recommendations based on validation results"""
        recommendations = []
        
        # Analyze metrics and suggest improvements
        if metrics.get('accuracy_score', 0.0) < 0.85:
            recommendations.append(
                "Improve content accuracy by adding more structured information and code examples"
            )
        
        if metrics.get('freshness_score', 0.0) < 0.70:
            recommendations.append(
                "Update knowledge sources more frequently to improve freshness scores"
            )
        
        if metrics.get('credibility_score', 0.0) < 0.80:
            recommendations.append(
                "Focus on higher-credibility sources and validate information against authoritative references"
            )
        
        if metrics.get('completeness_score', 0.0) < 0.75:
            recommendations.append(
                "Expand knowledge coverage to include more comprehensive topic areas"
            )
        
        if metrics.get('consistency_score', 0.0) < 0.80:
            recommendations.append(
                "Review content for contradictions and ensure consistent terminology usage"
            )
        
        # Analyze failed validation rules
        failed_rules = [vr for vr in validation_results if not vr.passed]
        if failed_rules:
            recommendations.append(
                f"Address {len(failed_rules)} failed validation rules to improve overall quality"
            )
        
        return recommendations

    async def _calculate_knowledge_statistics(self, knowledge_data: Dict) -> Dict[str, Any]:
        """Calculate comprehensive knowledge statistics"""
        stats = {
            'total_collections': 0,
            'total_knowledge_points': 0,
            'knowledge_by_type': {},
            'knowledge_by_domain': {},
            'source_distribution': {},
            'average_content_length': 0,
            'processing_timestamp': datetime.utcnow().isoformat()
        }
        
        all_content_lengths = []
        
        for collection_id, collection_data in knowledge_data.get('knowledge_by_collection', {}).items():
            stats['total_collections'] += 1
            knowledge_points = collection_data.get('knowledge_points', [])
            stats['total_knowledge_points'] += len(knowledge_points)
            
            for point in knowledge_points:
                # Knowledge type distribution
                knowledge_type = point.get('knowledge_type', 'general')
                stats['knowledge_by_type'][knowledge_type] = stats['knowledge_by_type'].get(knowledge_type, 0) + 1
                
                # Domain distribution
                domain = point.get('domain', 'general')
                stats['knowledge_by_domain'][domain] = stats['knowledge_by_domain'].get(domain, 0) + 1
                
                # Source distribution
                source = point.get('source_id', 'unknown')
                stats['source_distribution'][source] = stats['source_distribution'].get(source, 0) + 1
                
                # Content length tracking
                content_length = len(point.get('content', ''))
                all_content_lengths.append(content_length)
        
        # Calculate average content length
        if all_content_lengths:
            stats['average_content_length'] = statistics.mean(all_content_lengths)
            stats['content_length_stats'] = {
                'min': min(all_content_lengths),
                'max': max(all_content_lengths),
                'median': statistics.median(all_content_lengths),
                'std_dev': statistics.stdev(all_content_lengths) if len(all_content_lengths) > 1 else 0
            }
        
        return stats

    async def _assess_source_credibility(self, source_url: str) -> float:
        """Assess credibility of a source based on URL"""
        if not source_url:
            return self.credibility_database.get('unknown', 0.30)
        
        try:
            parsed_url = urlparse(source_url)
            domain = parsed_url.netloc.lower()
            
            # Check exact domain match
            if domain in self.credibility_database:
                return self.credibility_database[domain]
            
            # Check partial matches
            for known_domain, credibility in self.credibility_database.items():
                if known_domain in domain or domain.endswith(known_domain):
                    return credibility
            
            # Default credibility for unknown domains
            return self.credibility_database.get('unknown', 0.30)
            
        except:
            return self.credibility_database.get('unknown', 0.30)

    def _has_structured_content(self, content: str) -> bool:
        """Check if content has structured elements"""
        structured_indicators = [
            r'\d+\.',           # Numbered lists
            r'[-*]\s',          # Bullet points
            r'#{1,6}\s',        # Markdown headers
            r'```',             # Code blocks
            r'\|.*\|',          # Tables
            r':\s*$',           # Definitions (line ending with colon)
        ]
        
        for pattern in structured_indicators:
            if re.search(pattern, content, re.MULTILINE):
                return True
        
        return False

    def _has_code_examples(self, content: str) -> bool:
        """Check if content contains code examples"""
        code_indicators = [
            r'```[a-zA-Z]*\n',      # Code fences with language
            r'`[^`]+`',             # Inline code
            r'function\s+\w+\(',    # JavaScript functions
            r'def\s+\w+\(',         # Python functions
            r'class\s+\w+',         # Class definitions
            r'import\s+\w+',        # Import statements
            r'<[a-zA-Z][^>]*>',     # HTML/XML tags
        ]
        
        for pattern in code_indicators:
            if re.search(pattern, content):
                return True
        
        return False

    def _has_references(self, content: str) -> bool:
        """Check if content has references or citations"""
        reference_indicators = [
            r'https?://[^\s]+',         # URLs
            r'www\.[^\s]+',             # www links
            r'\[[\d,\s-]+\]',           # Numeric citations
            r'see\s+also',              # Cross-references
            r'according\s+to',          # Attributions
            r'source:\s*',              # Source attributions
        ]
        
        for pattern in reference_indicators:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False

    def _assess_reading_level(self, content: str) -> float:
        """Assess reading level appropriateness for technical content"""
        try:
            # Calculate reading ease
            reading_ease = flesch_reading_ease(content)
            
            # For technical content, we want moderate complexity
            # Flesch Reading Ease: 0-30 (very difficult), 30-50 (difficult), 
            # 50-60 (fairly difficult), 60-70 (standard), 70-80 (fairly easy), 80-90 (easy), 90-100 (very easy)
            
            if 30 <= reading_ease <= 70:
                # Appropriate for technical content
                return 1.0
            elif 20 <= reading_ease < 30 or 70 < reading_ease <= 80:
                # Slightly outside ideal range
                return 0.9
            elif 10 <= reading_ease < 20 or 80 < reading_ease <= 90:
                # More significantly outside ideal range
                return 0.8
            else:
                # Very difficult or very easy - may not be appropriate
                return 0.7
                
        except:
            # If analysis fails, return neutral score
            return 0.85

    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on quality validator"""
        try:
            health_info = {
                'healthy': True,
                'validation_rules_loaded': len(self.validation_rules),
                'credibility_database_size': len(self.credibility_database),
                'quality_gates_configured': len(self.quality_gates),
                'sentiment_analyzer_available': self.sentiment_analyzer is not None,
                'recent_validations': len(self.quality_history),
                'last_check': datetime.utcnow().isoformat()
            }
            
            # Test validation functionality with sample data
            sample_knowledge = {
                'knowledge_by_collection': {
                    'test_collection': {
                        'knowledge_points': [
                            {
                                'content': 'This is a test knowledge point for validation testing.',
                                'source_id': 'test_source',
                                'source_url': 'https://test.com',
                                'knowledge_type': 'test',
                                'domain': 'testing',
                                'credibility_score': 0.9,
                                'extraction_timestamp': datetime.utcnow().isoformat()
                            }
                        ]
                    }
                }
            }
            
            test_validation = await self.comprehensive_validation(sample_knowledge, {})
            health_info['validation_test_passed'] = test_validation['score'] > 0
            
            return health_info
            
        except Exception as e:
            logger.error(f"Quality validator health check failed: {str(e)}")
            return {
                'healthy': False,
                'error': str(e),
                'last_check': datetime.utcnow().isoformat()
            }

# Example usage and testing
async def test_quality_validator():
    """Test quality validator functionality"""
    validator = QualityValidator()
    
    # Test health check
    health = await validator.health_check()
    print(f"Health check: {health}")
    
    # Create sample knowledge data for testing
    sample_knowledge = {
        'knowledge_by_collection': {
            'security_test': {
                'knowledge_points': [
                    {
                        'content': 'SQL injection is a code injection technique that might destroy your database. It involves placing malicious code in SQL statements, via web page input.',
                        'source_id': 'owasp_test',
                        'source_url': 'https://owasp.org/www-community/attacks/SQL_Injection',
                        'knowledge_type': 'vulnerability_patterns',
                        'domain': 'security',
                        'credibility_score': 1.0,
                        'extraction_timestamp': datetime.utcnow().isoformat()
                    },
                    {
                        'content': 'To prevent SQL injection, use parameterized queries or prepared statements. This ensures that an attacker is not able to change the intent of a query.',
                        'source_id': 'owasp_test',
                        'source_url': 'https://owasp.org/www-community/attacks/SQL_Injection',
                        'knowledge_type': 'mitigation_strategies',
                        'domain': 'security',
                        'credibility_score': 1.0,
                        'extraction_timestamp': datetime.utcnow().isoformat()
                    }
                ]
            }
        }
    }
    
    # Test comprehensive validation
    validation_result = await validator.comprehensive_validation(
        sample_knowledge, 
        {'min_accuracy': 0.85}
    )
    
    print(f"Validation result: {validation_result['score']:.3f}")
    print(f"Passed gates: {validation_result['passed_gates']}")
    print(f"Recommendations: {validation_result['recommendations']}")

if __name__ == "__main__":
    asyncio.run(test_quality_validator())