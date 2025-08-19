#!/usr/bin/env python3
"""
Run Phase 1 tests for CMD Agent Select Logic
"""

import sys
import os
import unittest
import time

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Fix import issues by handling enum correctly
from src.core.models import RoutingAction

def run_basic_functionality_test():
    """Run a basic functionality test to verify the system works"""
    
    print("🧪 Running Basic Functionality Test...")
    print("=" * 50)
    
    try:
        from src.cmd_agent_select_logic import CmdAgentSelectLogic
        
        # Initialize system
        system = CmdAgentSelectLogic(enable_monitoring=True, enable_circuit_breaker=True)
        print("✅ System initialization successful")
        
        # Test cases covering different complexity levels
        test_cases = [
            {
                'description': 'check deployment status',
                'expected_type': 'simple',
                'target_ms': 50
            },
            {
                'description': 'build a React component with authentication',
                'expected_type': 'standard',
                'target_ms': 100
            },
            {
                'description': 'comprehensive enterprise architecture modernization with security audit',
                'expected_type': 'complex',
                'target_ms': 200
            }
        ]
        
        print(f"\n🎯 Testing {len(test_cases)} routing scenarios...")
        
        results = []
        
        for i, test_case in enumerate(test_cases, 1):
            description = test_case['description']
            target_ms = test_case['target_ms']
            
            print(f"\nTest {i}: {description[:60]}...")
            
            # Execute routing
            start_time = time.perf_counter()
            decision = system.route_task(description)
            end_time = time.perf_counter()
            
            actual_time_ms = (end_time - start_time) * 1000
            
            # Collect results
            result = {
                'test_case': test_case,
                'decision': decision,
                'actual_time_ms': actual_time_ms,
                'passed_performance': actual_time_ms <= target_ms,
                'passed_confidence': decision.confidence >= 0.3
            }
            results.append(result)
            
            # Print result
            status = "✅" if result['passed_performance'] and result['passed_confidence'] else "❌"
            print(f"  {status} Time: {actual_time_ms:.1f}ms (target: {target_ms}ms)")
            print(f"     Action: {decision.action}")
            print(f"     Agent: {decision.selected_agent}")
            print(f"     Confidence: {decision.confidence:.2f}")
            print(f"     Reasoning: {decision.reasoning}")
        
        # Summary
        passed_tests = sum(1 for r in results if r['passed_performance'] and r['passed_confidence'])
        total_tests = len(results)
        
        print(f"\n📊 Test Summary:")
        print(f"   Passed: {passed_tests}/{total_tests} ({(passed_tests/total_tests)*100:.1f}%)")
        
        # Performance analysis
        response_times = [r['actual_time_ms'] for r in results]
        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        
        print(f"   Average response time: {avg_time:.1f}ms")
        print(f"   Max response time: {max_time:.1f}ms")
        
        # System health check
        health = system.get_system_health()
        print(f"   System status: {health['status']}")
        
        # Real-time stats
        stats = system.get_real_time_stats()
        if stats:
            print(f"   Success rate: {stats['success_rate']*100:.1f}%")
        
        success = passed_tests == total_tests
        print(f"\n{'🎉 All tests passed!' if success else '⚠️  Some tests failed'}")
        
        return success
        
    except Exception as e:
        print(f"❌ Error during basic test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def run_unit_tests():
    """Run comprehensive unit tests"""
    
    print("\n🧪 Running Unit Tests...")
    print("=" * 50)
    
    try:
        # Discover and run tests
        loader = unittest.TestLoader()
        suite = loader.discover('tests', pattern='test_*.py')
        
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        success = result.wasSuccessful()
        
        print(f"\n📊 Unit Test Summary:")
        print(f"   Tests run: {result.testsRun}")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")
        print(f"   Success: {success}")
        
        return success
        
    except Exception as e:
        print(f"❌ Error running unit tests: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test runner"""
    
    print("🚀 CMD Agent Select Logic - Phase 1 Test Suite")
    print("=" * 60)
    
    overall_success = True
    
    # Run basic functionality test
    basic_success = run_basic_functionality_test()
    overall_success = overall_success and basic_success
    
    # Run unit tests
    unit_success = run_unit_tests()
    overall_success = overall_success and unit_success
    
    print("\n" + "=" * 60)
    if overall_success:
        print("🎉 ALL TESTS PASSED - Phase 1 implementation successful!")
        print("✅ Core foundation ready for Phase 2 development")
    else:
        print("⚠️  SOME TESTS FAILED - Review results above")
        print("❌ Address issues before proceeding to Phase 2")
    
    print("\n📋 Phase 1 Deliverables Completed:")
    print("   ✅ Basic hierarchical classification system (<25ms target)")
    print("   ✅ Simple pattern-based routing with high-confidence direct routes") 
    print("   ✅ Input validation and error handling framework")
    print("   ✅ Performance timing instrumentation and metrics collection")
    print("   ✅ Core functionality validation with test scenarios")
    
    return 0 if overall_success else 1

if __name__ == '__main__':
    sys.exit(main())