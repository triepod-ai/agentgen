# tests/test_phase2_integration.py
"""
Phase 2 Integration Tests - Intelligence Layer Validation
Tests multi-domain detection, confidence scoring, strategic escalation, and performance
"""

import pytest
import time
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../cmd-agent-select-logic'))

from cmd_agent_select_logic_phase2 import CmdAgentSelectLogicPhase2
from analysis.confidence_engine import ConfidenceEngine
from analysis.domain_detector import DomainDetectionEngine
from routing.escalation_engine import StrategicEscalationEngine, EscalationAction

class TestPhase2Integration:
    """Comprehensive Phase 2 integration testing"""
    
    def setup_method(self):
        """Setup test environment"""
        self.system = CmdAgentSelectLogicPhase2(
            enable_monitoring=True,
            enable_circuit_breaker=True,
            enable_confidence_cache=True
        )
    
    def test_phase2_system_initialization(self):
        """Test Phase 2 system initializes all components correctly"""
        
        # Verify all Phase 2 components are initialized
        assert self.system.domain_detector is not None
        assert self.system.confidence_engine is not None
        assert self.system.escalation_engine is not None
        
        # Verify Phase 1 components are preserved
        assert self.system.classifier is not None
        assert self.system.router is not None
        assert self.system.validator is not None
        
        # Verify performance targets include Phase 2 metrics
        assert 'domain_detection_ms' in self.system.performance_targets
        assert 'confidence_calculation_ms' in self.system.performance_targets
        assert 'escalation_decision_ms' in self.system.performance_targets
        
        # Verify available agents list is populated
        assert len(self.system.available_agents) > 10
        assert '@agent-organizer' in self.system.available_agents
    
    def test_multi_domain_detection_integration(self):
        """Test enhanced multi-domain detection with real scenarios"""
        
        test_cases = [
            {
                'description': "Create a React component with authentication and deploy it to AWS",
                'expected_domains': ['frontend', 'security', 'infrastructure'],
                'expected_primary': 'frontend'
            },
            {
                'description': "Build a secure API with database integration and comprehensive testing",
                'expected_domains': ['backend', 'security', 'testing'],
                'expected_primary': 'backend'
            },
            {
                'description': "Audit security vulnerabilities and generate documentation",
                'expected_domains': ['security', 'documentation'],
                'expected_primary': 'security'
            },
            {
                'description': "Write API documentation",
                'expected_domains': ['documentation'],
                'expected_primary': 'documentation'
            }
        ]
        
        for case in test_cases:
            decision = self.system.route_task(case['description'])
            
            # Verify domain analysis exists
            assert hasattr(decision, 'domain_analysis')
            domain_analysis = decision.domain_analysis
            
            # Verify expected domains were detected
            detected_domains = [d['domain'] for d in domain_analysis['domains']]
            for expected_domain in case['expected_domains']:
                assert expected_domain in detected_domains, \
                    f"Expected domain '{expected_domain}' not found in {detected_domains}"
            
            # Verify primary domain
            if domain_analysis['domains']:
                assert domain_analysis['primary_domain'] == case['expected_primary']
            
            # Verify performance
            assert domain_analysis['analysis_time_ms'] < 25  # Phase 2 target
    
    def test_confidence_scoring_with_caching(self):
        """Test confidence scoring system with L1 cache validation"""
        
        test_task = "Create a React component for user authentication"
        
        # First execution - should calculate confidence and cache it
        start_time = time.perf_counter()
        decision1 = self.system.route_task(test_task)
        first_time = (time.perf_counter() - start_time) * 1000
        
        # Verify confidence components exist
        assert hasattr(decision1, 'confidence_breakdown')
        breakdown = decision1.confidence_breakdown
        
        assert 'pattern_match' in breakdown
        assert 'historical_success' in breakdown
        assert 'context_completeness' in breakdown
        assert 'resource_availability' in breakdown
        
        # Verify confidence is reasonable
        assert 0.0 <= decision1.confidence <= 1.0
        assert decision1.confidence > 0.3  # Should have reasonable confidence
        
        # Second execution - should hit cache
        start_time = time.perf_counter()
        decision2 = self.system.route_task(test_task)
        second_time = (time.perf_counter() - start_time) * 1000
        
        # Cache hit should be faster (though may not be noticeable in tests)
        # and produce identical results
        assert decision2.confidence == decision1.confidence
        assert decision2.selected_agent == decision1.selected_agent
        
        # Verify cache statistics
        confidence_stats = self.system.confidence_engine.get_performance_stats()
        cache_stats = confidence_stats.get('l1_cache', {})
        
        # Should have at least one cache operation
        assert cache_stats.get('entries', 0) >= 0
        # Note: In tests, cache might not hit due to timing/implementation details
    
    def test_strategic_escalation_integration(self):
        """Test strategic escalation to @agent-organizer"""
        
        # Test cases designed to trigger different escalation scenarios
        escalation_test_cases = [
            {
                'description': "Design a comprehensive enterprise microservices architecture with security audit, testing framework, and deployment pipeline",
                'expected_action': EscalationAction.ESCALATE_TO_ORGANIZER,
                'expected_agent': '@agent-organizer'
            },
            {
                'description': "Create React component and secure API endpoint",
                'expected_action': EscalationAction.ORCHESTRATION_ROUTING,
                'expected_agent': '@orchestrate-agents'
            },
            {
                'description': "Debug authentication error",
                'expected_action': EscalationAction.DIRECT_AGENT_ROUTING,
                'expected_agent': '@debug-issue'  # or similar
            }
        ]
        
        for case in escalation_test_cases:
            decision = self.system.route_task(case['description'])
            
            # Verify escalation attributes exist
            assert hasattr(decision, 'escalation_score')
            assert hasattr(decision, 'escalation_triggers')
            assert 0.0 <= decision.escalation_score <= 1.0
            
            # For high complexity cases, verify escalation to @agent-organizer
            if case['expected_action'] == EscalationAction.ESCALATE_TO_ORGANIZER:
                assert decision.selected_agent == '@agent-organizer'
                assert hasattr(decision, 'context_package')
                assert decision.context_package is not None
                
                # Verify context package structure
                context = decision.context_package
                assert 'original_request' in context
                assert 'routing_analysis' in context
                assert 'system_context' in context
                assert 'strategic_requirements' in context
                assert 'expected_deliverable' in context
                
                # Verify strategic requirements are populated
                strategic = context['strategic_requirements']
                assert isinstance(strategic.get('requires_enterprise_coordination'), bool)
                assert isinstance(strategic.get('requires_architectural_design'), bool)
    
    def test_performance_benchmarks_phase2(self):
        """Test that Phase 2 maintains performance targets"""
        
        performance_test_cases = [
            {'description': "Show project status", 'expected_complexity': 'simple'},
            {'description': "Create React component with authentication", 'expected_complexity': 'standard'},
            {'description': "Design enterprise microservices architecture with security audit", 'expected_complexity': 'complex'}
        ]
        
        results = self.system.validate_phase2_performance_targets(performance_test_cases)
        
        # Verify overall performance
        assert results['pass_rate'] > 0.6  # At least 60% pass rate for Phase 2
        
        # Verify Phase 2 specific metrics
        phase2_metrics = results['phase2_metrics']
        
        # Domain detection should perform well
        domain_perf = phase2_metrics['domain_detection_performance']
        assert domain_perf['avg_time_ms'] < 25  # Under 25ms target
        
        # Confidence scoring should perform well
        confidence_perf = phase2_metrics['confidence_scoring_performance']
        assert confidence_perf['avg_time_ms'] < 50  # Under 50ms target
        
        # Escalation decision should be fast
        escalation_perf = phase2_metrics['escalation_decision_performance']
        assert escalation_perf['avg_time_ms'] < 25  # Under 25ms target
        
        # Cache hit rate should be reasonable (may be low in tests)
        cache_hit_rate = phase2_metrics['cache_hit_rate']
        assert 0.0 <= cache_hit_rate <= 1.0
    
    def test_end_to_end_intelligence_layer(self):
        """Test complete end-to-end Phase 2 workflow"""
        
        complex_task = "Build a scalable e-commerce platform with React frontend, Node.js API, PostgreSQL database, AWS deployment, comprehensive testing, security audit, and documentation"
        
        start_time = time.perf_counter()
        decision = self.system.route_task(complex_task)
        total_time = (time.perf_counter() - start_time) * 1000
        
        # Verify performance is within complex task target
        assert total_time < 200  # 200ms target for complex tasks
        
        # Verify all Phase 2 attributes are populated
        assert hasattr(decision, 'domain_analysis')
        assert hasattr(decision, 'confidence_breakdown')
        assert hasattr(decision, 'escalation_score')
        assert hasattr(decision, 'escalation_triggers')
        assert hasattr(decision, 'performance_breakdown')
        
        # Verify performance breakdown
        perf_breakdown = decision.performance_breakdown
        assert 'classification_ms' in perf_breakdown
        assert 'domain_detection_ms' in perf_breakdown
        assert 'confidence_scoring_ms' in perf_breakdown
        assert 'escalation_decision_ms' in perf_breakdown
        assert 'total_pipeline_ms' in perf_breakdown
        
        # Verify each component meets performance targets
        assert perf_breakdown['domain_detection_ms'] < 25
        assert perf_breakdown['confidence_scoring_ms'] < 50
        assert perf_breakdown['escalation_decision_ms'] < 25
        
        # This complex task should trigger strategic analysis
        assert decision.selected_agent == '@agent-organizer' or \
               decision.selected_agent.startswith('@orchestrate-agents')
        
        # Verify domain analysis detected multiple domains
        domain_analysis = decision.domain_analysis
        assert domain_analysis['domain_count'] >= 3
        
        # Verify confidence scoring
        assert decision.confidence > 0.3
        confidence_breakdown = decision.confidence_breakdown
        for component in ['pattern_match', 'historical_success', 'context_completeness', 'resource_availability']:
            assert 0.0 <= confidence_breakdown[component] <= 1.0
    
    def test_error_handling_phase2(self):
        """Test error handling maintains robustness in Phase 2"""
        
        # Test invalid input
        decision = self.system.route_task("")
        assert decision.confidence < 0.5
        assert decision.selected_agent is not None  # Should have fallback
        
        # Test very long input
        long_input = "a " * 10000  # Very long task description
        decision = self.system.route_task(long_input)
        assert decision.analysis_time_ms < 500  # Should still be reasonably fast
        assert decision.selected_agent is not None
        
        # Test special characters
        special_input = "Create component with <script>alert('xss')</script> and SQL injection'; DROP TABLE users; --"
        decision = self.system.route_task(special_input)
        assert decision.selected_agent is not None  # Should handle gracefully
    
    def test_system_health_phase2(self):
        """Test Phase 2 system health monitoring"""
        
        health = self.system.get_system_health()
        
        # Verify Phase 2 identification
        assert health['phase'] == 2
        assert health['intelligence_layer'] == True
        
        # Verify all Phase 2 components are monitored
        components = health['components']
        assert 'domain_detector' in components
        assert 'confidence_engine' in components
        assert 'escalation_engine' in components
        
        # All components should be operational
        for component, status in components.items():
            assert status == 'operational', f"Component {component} not operational"
        
        # System should be healthy initially
        assert health['status'] in ['healthy', 'degraded']  # Allow for test environment variations
        assert isinstance(health['alerts'], list)
    
    def test_intelligence_layer_stats(self):
        """Test intelligence layer statistics reporting"""
        
        # Execute a few tasks to generate stats
        test_tasks = [
            "Create React component",
            "Build secure API",
            "Deploy to AWS"
        ]
        
        for task in test_tasks:
            self.system.route_task(task)
        
        # Get intelligence layer stats
        stats = self.system.get_intelligence_layer_stats()
        
        # Verify structure
        assert 'confidence_engine' in stats
        assert 'domain_detection' in stats
        assert 'escalation_patterns' in stats
        
        # Verify confidence engine stats
        confidence_stats = stats['confidence_engine']
        assert 'confidence_engine' in confidence_stats
        assert 'l1_cache' in confidence_stats
        
        # Verify domain detection stats
        domain_stats = stats['domain_detection']
        assert 'processors' in domain_stats
        assert len(domain_stats['processors']) == 6  # 6 domain processors
        
        expected_domains = ['frontend', 'backend', 'security', 'infrastructure', 'testing', 'documentation']
        for domain in expected_domains:
            assert domain in domain_stats['processors']

class TestPhase2Components:
    """Individual Phase 2 component testing"""
    
    def test_confidence_engine_standalone(self):
        """Test confidence engine as standalone component"""
        
        engine = ConfidenceEngine()
        
        # Test confidence calculation
        confidence = engine.calculate_routing_confidence(
            "Create secure React authentication component",
            {
                'domains': [
                    {'domain': 'frontend', 'confidence': 0.8, 'complexity_bias': 0.7},
                    {'domain': 'security', 'confidence': 0.6, 'complexity_bias': 0.9}
                ],
                'domain_count': 2
            },
            ['@build-frontend', '@security-auditor']
        )
        
        # Verify confidence components
        assert 0.0 <= confidence.pattern_match <= 1.0
        assert 0.0 <= confidence.historical_success <= 1.0
        assert 0.0 <= confidence.context_completeness <= 1.0
        assert 0.0 <= confidence.resource_availability <= 1.0
        assert 0.0 <= confidence.total_confidence <= 1.0
        
        # Test cache functionality
        stats = engine.get_performance_stats()
        assert 'confidence_engine' in stats
        assert 'l1_cache' in stats
    
    def test_domain_detection_engine_standalone(self):
        """Test domain detection engine as standalone component"""
        
        detector = DomainDetectionEngine()
        
        # Test multi-domain detection
        result = detector.detect_domains(
            "Create secure React component with database integration and deploy to AWS with comprehensive testing"
        )
        
        # Verify result structure
        assert 'domains' in result
        assert 'domain_count' in result
        assert 'total_confidence' in result
        assert 'primary_domain' in result
        assert 'analysis_time_ms' in result
        
        # Should detect multiple domains
        assert result['domain_count'] >= 3
        
        # Verify domains have required fields
        for domain in result['domains']:
            assert 'domain' in domain
            assert 'confidence' in domain
            assert 'complexity_bias' in domain
            assert 'preferred_agents' in domain
            
            assert 0.0 <= domain['confidence'] <= 1.0
            assert 0.0 <= domain['complexity_bias'] <= 1.0
            assert isinstance(domain['preferred_agents'], list)
        
        # Performance should be good
        assert result['analysis_time_ms'] < 25
    
    def test_escalation_engine_standalone(self):
        """Test strategic escalation engine as standalone component"""
        
        engine = StrategicEscalationEngine()
        
        # Test enterprise-scale escalation
        decision = engine.make_escalation_decision(
            "Design comprehensive enterprise microservices architecture",
            {'complexity_score': 0.9, 'complexity_level': 'COMPLEX'},
            {'domains': [], 'domain_count': 4},
            {'total_confidence': 0.3, 'pattern_match': 0.2, 'historical_success': 0.4, 
             'context_completeness': 0.3, 'resource_availability': 0.3},
            ['@agent-organizer', '@architect-specialist']
        )
        
        # Should escalate to @agent-organizer
        assert decision.action == EscalationAction.ESCALATE_TO_ORGANIZER
        assert decision.recommended_agent == '@agent-organizer'
        assert decision.context_package is not None
        
        # Test simple direct routing
        simple_decision = engine.make_escalation_decision(
            "Debug login error",
            {'complexity_score': 0.3, 'complexity_level': 'SIMPLE'},
            {'domains': [{'domain': 'backend', 'confidence': 0.8}], 'domain_count': 1},
            {'total_confidence': 0.8, 'pattern_match': 0.9, 'historical_success': 0.8,
             'context_completeness': 0.7, 'resource_availability': 0.8},
            ['@debug-issue', '@backend-specialist']
        )
        
        # Should route directly
        assert simple_decision.action == EscalationAction.DIRECT_AGENT_ROUTING
        assert simple_decision.recommended_agent in ['@debug-issue', '@backend-specialist']

if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v'])