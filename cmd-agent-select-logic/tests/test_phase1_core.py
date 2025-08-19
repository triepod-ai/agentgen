# tests/test_phase1_core.py
"""
Phase 1 Core Functionality Tests
Validates basic hierarchical classification, pattern-based routing, and performance targets
"""

import unittest
import time
from src.cmd_agent_select_logic import CmdAgentSelectLogic
from src.core.classifier import HierarchicalClassifier
from src.core.models import ComplexityLevel, RoutingAction
from src.analysis.domain_detector import DomainDetectionEngine
from src.routing.router import BasicRoutingEngine, RoutingValidator

class TestPhase1CoreFunctionality(unittest.TestCase):
    """Test core Phase 1 functionality and requirements"""
    
    def setUp(self):
        """Set up test environment"""
        self.system = CmdAgentSelectLogic(enable_monitoring=True, enable_circuit_breaker=True)
        self.classifier = HierarchicalClassifier()
        self.domain_detector = DomainDetectionEngine()
        self.router = BasicRoutingEngine()
        self.validator = RoutingValidator()
    
    def test_hierarchical_classification_performance(self):
        """Test that hierarchical classification meets <25ms target"""
        
        test_cases = [
            "check the status of deployment",
            "build a React component with authentication",
            "comprehensive system-wide architecture modernization with microservices"
        ]
        
        for description in test_cases:
            start_time = time.perf_counter()
            result = self.classifier.classify_task(description)
            end_time = time.perf_counter()
            
            analysis_time_ms = (end_time - start_time) * 1000
            
            # Verify performance target
            self.assertLess(analysis_time_ms, 25, 
                          f"Classification took {analysis_time_ms:.1f}ms, exceeds 25ms target")
            
            # Verify result structure
            self.assertIsInstance(result.complexity_level, ComplexityLevel)
            self.assertGreaterEqual(result.complexity_score, 0.0)
            self.assertLessEqual(result.complexity_score, 1.0)
            self.assertGreater(result.estimated_tokens, 0)
            self.assertGreater(result.estimated_time_minutes, 0)
    
    def test_simple_task_classification(self):
        """Test classification of simple tasks"""
        
        simple_tasks = [
            "check status",
            "read the log file",
            "show me the deployment status",
            "list all users",
            "get current version"
        ]
        
        for task in simple_tasks:
            result = self.classifier.classify_task(task)
            
            self.assertEqual(result.complexity_level, ComplexityLevel.SIMPLE,
                           f"Task '{task}' should be classified as SIMPLE")
            self.assertLess(result.complexity_score, 0.5,
                          f"Simple task '{task}' has complexity score {result.complexity_score}")
            self.assertLess(result.estimated_tokens, 8000,
                          f"Simple task estimated tokens too high: {result.estimated_tokens}")
    
    def test_complex_task_classification(self):
        """Test classification of complex tasks"""
        
        complex_tasks = [
            "comprehensive system-wide architecture modernization",
            "enterprise platform migration with microservices",
            "complete infrastructure overhaul with security audit",
            "strategic transformation of legacy systems"
        ]
        
        for task in complex_tasks:
            result = self.classifier.classify_task(task)
            
            self.assertEqual(result.complexity_level, ComplexityLevel.COMPLEX,
                           f"Task '{task}' should be classified as COMPLEX")
            self.assertGreater(result.complexity_score, 0.7,
                             f"Complex task '{task}' has complexity score {result.complexity_score}")
            self.assertGreater(result.estimated_tokens, 10000,
                             f"Complex task estimated tokens too low: {result.estimated_tokens}")
    
    def test_domain_detection_accuracy(self):
        """Test domain detection accuracy and performance"""
        
        test_cases = [
            {
                'description': 'create a React component with responsive styling',
                'expected_domain': 'frontend',
                'min_confidence': 0.6
            },
            {
                'description': 'build REST API with database integration',
                'expected_domain': 'backend', 
                'min_confidence': 0.6
            },
            {
                'description': 'security audit for authentication vulnerabilities',
                'expected_domain': 'security',
                'min_confidence': 0.7
            },
            {
                'description': 'deploy application to AWS with Docker',
                'expected_domain': 'infrastructure',
                'min_confidence': 0.6
            }
        ]
        
        for case in test_cases:
            start_time = time.perf_counter()
            result = self.domain_detector.detect_domains(case['description'])
            end_time = time.perf_counter()
            
            analysis_time_ms = (end_time - start_time) * 1000
            
            # Performance check - domain detection should contribute <10ms
            self.assertLess(analysis_time_ms, 10,
                          f"Domain detection took {analysis_time_ms:.1f}ms, exceeds 10ms target")
            
            # Accuracy check
            self.assertGreater(result['domain_count'], 0,
                             f"No domains detected for: {case['description']}")
            
            primary_domain = result['primary_domain']
            self.assertEqual(primary_domain, case['expected_domain'],
                           f"Expected {case['expected_domain']}, got {primary_domain}")
            
            # Confidence check
            primary_confidence = result['domains'][0]['confidence']
            self.assertGreaterEqual(primary_confidence, case['min_confidence'],
                                  f"Confidence {primary_confidence} below minimum {case['min_confidence']}")
    
    def test_routing_decision_logic(self):
        """Test routing decision logic with various scenarios"""
        
        test_cases = [
            {
                'description': 'check deployment status',
                'expected_action': RoutingAction.DIRECT_AGENT,
                'expected_confidence_min': 0.5
            },
            {
                'description': 'build React app with backend API and security',
                'expected_action': RoutingAction.ORCHESTRATION,
                'expected_confidence_min': 0.4
            },
            {
                'description': 'comprehensive enterprise architecture modernization',
                'expected_action': RoutingAction.ESCALATE,
                'expected_confidence_min': 0.3
            }
        ]
        
        for case in test_cases:
            # First classify the task
            task_analysis = self.classifier.classify_task(case['description'])
            
            # Then route it
            decision = self.router.route_task(task_analysis)
            
            self.assertEqual(decision.action, case['expected_action'],
                           f"Wrong action for '{case['description']}': expected {case['expected_action']}, got {decision.action}")
            
            self.assertGreaterEqual(decision.confidence, case['expected_confidence_min'],
                                  f"Confidence too low for '{case['description']}': {decision.confidence}")
            
            self.assertIsNotNone(decision.reasoning,
                               f"No reasoning provided for '{case['description']}'")
    
    def test_input_validation(self):
        """Test input validation and error handling"""
        
        # Test valid inputs
        valid_inputs = [
            "create a React component",
            "deploy to production", 
            "analyze system performance"
        ]
        
        for valid_input in valid_inputs:
            is_valid, message = self.validator.validate_task_description(valid_input)
            self.assertTrue(is_valid, f"Valid input rejected: {valid_input}")
            self.assertEqual(message, "Valid")
        
        # Test invalid inputs
        invalid_inputs = [
            ("", "Task description cannot be empty"),
            ("   ", "Task description cannot be empty"), 
            ("x" * 2001, "Task description too long"),
            ("eval('malicious code')", "potentially unsafe content"),
            (123, "Task description must be a string")
        ]
        
        for invalid_input, expected_error in invalid_inputs:
            is_valid, message = self.validator.validate_task_description(invalid_input)
            self.assertFalse(is_valid, f"Invalid input accepted: {invalid_input}")
            self.assertIn(expected_error.lower(), message.lower())
    
    def test_end_to_end_routing_performance(self):
        """Test end-to-end routing performance targets"""
        
        test_cases = [
            {
                'description': 'check status',
                'expected_complexity': 'simple',
                'target_ms': 50
            },
            {
                'description': 'implement user authentication API',
                'expected_complexity': 'standard', 
                'target_ms': 100
            },
            {
                'description': 'comprehensive system architecture modernization with enterprise security',
                'expected_complexity': 'complex',
                'target_ms': 200
            }
        ]
        
        for case in test_cases:
            start_time = time.perf_counter()
            decision = self.system.route_task(case['description'])
            end_time = time.perf_counter()
            
            actual_time_ms = (end_time - start_time) * 1000
            
            self.assertLess(actual_time_ms, case['target_ms'],
                          f"Routing took {actual_time_ms:.1f}ms, exceeds {case['target_ms']}ms target for {case['expected_complexity']} task")
            
            self.assertGreater(decision.confidence, 0.3,
                             f"Very low confidence: {decision.confidence}")
            
            self.assertIsNotNone(decision.reasoning,
                               f"No reasoning provided for decision")
    
    def test_circuit_breaker_functionality(self):
        """Test circuit breaker error handling"""
        
        # This test would normally require injecting failures
        # For now, test that circuit breaker is initialized and accessible
        circuit_status = self.system.get_circuit_breaker_status()
        
        if circuit_status:  # Only test if circuit breaker is enabled
            self.assertEqual(circuit_status['state'], 'closed')
            self.assertEqual(circuit_status['failure_count'], 0)
            self.assertGreaterEqual(circuit_status['success_count'], 0)
    
    def test_performance_monitoring(self):
        """Test performance monitoring functionality"""
        
        # Execute several routing decisions
        test_descriptions = [
            "check status",
            "build React component", 
            "deploy to production",
            "security audit",
            "complex system modernization"
        ]
        
        for description in test_descriptions:
            self.system.route_task(description)
        
        # Check real-time stats
        stats = self.system.get_real_time_stats()
        
        if stats:  # Only test if monitoring is enabled
            self.assertGreater(stats['total_requests'], 0)
            self.assertGreaterEqual(stats['success_rate'], 0.8)
            self.assertGreaterEqual(stats['current_avg_response_time_ms'], 0)
    
    def test_system_health_check(self):
        """Test system health monitoring"""
        
        health = self.system.get_system_health()
        
        self.assertIn('status', health)
        self.assertIn(health['status'], ['healthy', 'degraded', 'unhealthy'])
        self.assertIn('components', health)
        
        # Check that all core components are operational
        components = health['components']
        self.assertEqual(components['classifier'], 'operational')
        self.assertEqual(components['router'], 'operational')
        self.assertEqual(components['validator'], 'operational')
        self.assertEqual(components['error_recovery'], 'operational')
    
    def test_batch_performance_validation(self):
        """Test system performance with batch of requests"""
        
        test_cases = [
            {'description': 'read config file', 'expected_complexity': 'simple'},
            {'description': 'check deployment status', 'expected_complexity': 'simple'},
            {'description': 'list database tables', 'expected_complexity': 'simple'},
            {'description': 'implement user login', 'expected_complexity': 'standard'},
            {'description': 'create REST API endpoints', 'expected_complexity': 'standard'},
            {'description': 'build responsive React dashboard', 'expected_complexity': 'standard'},
            {'description': 'enterprise architecture modernization', 'expected_complexity': 'complex'},
            {'description': 'comprehensive security audit and remediation', 'expected_complexity': 'complex'}
        ]
        
        validation_results = self.system.validate_performance_targets(test_cases)
        
        # Check overall pass rate (should be >80% for Phase 1)
        self.assertGreater(validation_results['pass_rate'], 0.8,
                         f"Overall pass rate {validation_results['pass_rate']} below 80% target")
        
        # Check that simple tasks are consistently fast
        simple_results = validation_results['performance_breakdown']['simple']
        if simple_results['count'] > 0:
            self.assertLess(simple_results['avg_time_ms'], 60,
                          f"Simple tasks average {simple_results['avg_time_ms']}ms, exceeds 60ms")
            self.assertGreater(simple_results['pass_rate'], 0.9,
                             f"Simple tasks pass rate {simple_results['pass_rate']} below 90%")
        
        # Print detailed results for debugging
        if validation_results['failed_cases']:
            print(f"\nFailed test cases ({len(validation_results['failed_cases'])}):")
            for case in validation_results['failed_cases']:
                print(f"  {case['test_index']}: {case['description'][:50]}... - "
                      f"{case['actual_time_ms']:.1f}ms (target: {case['target_ms']}ms) - "
                      f"confidence: {case['confidence']:.2f}")

if __name__ == '__main__':
    unittest.main()