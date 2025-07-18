"""
Master Test Runner
=================

Orchestrates all Cadwork MCP test suites including:
- Individual Controller Tests
- Performance Tests
- Edge Case Tests
- Integration Tests
- Comprehensive Reporting
"""

import sys
import os
import asyncio
import time
from typing import Dict, Any, List
from datetime import datetime

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import all test suites
from tests.run_test import CadworkTestRunner
from tests.performance_test_suite import PerformanceTestSuite
from tests.edge_case_test_suite import EdgeCaseTestSuite
from tests.integration_test_suite import IntegrationTestSuite


class MasterTestRunner:
    """Master test runner for all Cadwork MCP test suites"""
    
    def __init__(self):
        self.start_time = None
        self.test_results = {}
        self.total_tests = 0
        self.total_passed = 0
        self.total_failed = 0
        self.total_errors = 0
    
    async def run_comprehensive_tests(self, include_stress_tests: bool = True) -> None:
        """Run all test suites comprehensively"""
        print("🚀 CADWORK MCP MASTER TEST SUITE")
        print("=" * 80)
        print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎯 Running comprehensive test coverage...")
        print("=" * 80)
        
        self.start_time = time.time()
        
        # Test Suite 1: Individual Controller Tests
        await self._run_controller_tests()
        
        if include_stress_tests:
            # Test Suite 2: Performance and Stress Tests
            await self._run_performance_tests()
            
            # Test Suite 3: Edge Case and Error Recovery Tests
            await self._run_edge_case_tests()
            
            # Test Suite 4: Integration Tests
            await self._run_integration_tests()
        
        # Generate comprehensive report
        await self._generate_master_report()
    
    async def run_quick_validation(self) -> None:
        """Run quick validation tests"""
        print("⚡ CADWORK MCP QUICK VALIDATION")
        print("=" * 60)
        print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎯 Running quick validation tests...")
        print("=" * 60)
        
        self.start_time = time.time()
        
        # Run only controller tests in quick mode
        await self._run_controller_tests(quick_mode=True)
        
        # Generate quick report
        await self._generate_quick_report()
    
    async def run_specific_suite(self, suite_name: str) -> None:
        """Run a specific test suite"""
        print(f"🎯 CADWORK MCP {suite_name.upper()} TEST SUITE")
        print("=" * 60)
        print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        self.start_time = time.time()
        
        if suite_name.lower() == "controllers":
            await self._run_controller_tests()
        elif suite_name.lower() == "performance":
            await self._run_performance_tests()
        elif suite_name.lower() == "edge":
            await self._run_edge_case_tests()
        elif suite_name.lower() == "integration":
            await self._run_integration_tests()
        else:
            print(f"❌ Unknown test suite: {suite_name}")
            return
        
        await self._generate_specific_report(suite_name)
    
    async def _run_controller_tests(self, quick_mode: bool = False) -> None:
        """Run individual controller tests"""
        print("\n🔧 RUNNING CONTROLLER TESTS")
        print("-" * 50)
        
        try:
            controller_runner = CadworkTestRunner(verbose=False)
            
            if quick_mode:
                print("⚡ Quick mode: Testing essential functions only")
                # Run quick tests for all controllers
                await controller_runner.run_all_tests(quick_mode=True)
            else:
                print("🔄 Full mode: Testing all controller functions")
                await controller_runner.run_all_tests(quick_mode=False)
            
            # Collect results
            if hasattr(controller_runner, 'all_results'):
                self.test_results["controllers"] = {
                    "total_tests": len(controller_runner.all_results),
                    "passed": len([r for r in controller_runner.all_results if r.status == "PASSED"]),
                    "failed": len([r for r in controller_runner.all_results if r.status == "FAILED"]),
                    "errors": len([r for r in controller_runner.all_results if r.status == "ERROR"]),
                    "skipped": len([r for r in controller_runner.all_results if r.status == "SKIPPED"]),
                    "execution_time": sum(r.execution_time for r in controller_runner.all_results),
                    "controller_summaries": getattr(controller_runner, 'controller_summaries', {})
                }
            else:
                self.test_results["controllers"] = {
                    "total_tests": 0,
                    "passed": 0,
                    "failed": 0,
                    "errors": 1,
                    "skipped": 0,
                    "execution_time": 0,
                    "error_message": "Controller runner did not complete properly"
                }
            
            print("✅ Controller tests completed")
            
        except Exception as e:
            print(f"❌ Controller tests failed: {e}")
            self.test_results["controllers"] = {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "errors": 1,
                "skipped": 0,
                "execution_time": 0,
                "error_message": str(e)
            }
    
    async def _run_performance_tests(self) -> None:
        """Run performance and stress tests"""
        print("\n🚀 RUNNING PERFORMANCE TESTS")
        print("-" * 50)
        
        try:
            performance_suite = PerformanceTestSuite()
            await performance_suite.run_all_performance_tests()
            
            summary = performance_suite.get_summary()
            self.test_results["performance"] = summary
            
            print("✅ Performance tests completed")
            
        except Exception as e:
            print(f"❌ Performance tests failed: {e}")
            self.test_results["performance"] = {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "errors": 1,
                "skipped": 0,
                "execution_time": 0,
                "error_message": str(e)
            }
    
    async def _run_edge_case_tests(self) -> None:
        """Run edge case and error recovery tests"""
        print("\n🎯 RUNNING EDGE CASE TESTS")
        print("-" * 50)
        
        try:
            edge_case_suite = EdgeCaseTestSuite()
            await edge_case_suite.run_all_edge_case_tests()
            
            summary = edge_case_suite.get_summary()
            self.test_results["edge_cases"] = summary
            
            print("✅ Edge case tests completed")
            
        except Exception as e:
            print(f"❌ Edge case tests failed: {e}")
            self.test_results["edge_cases"] = {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "errors": 1,
                "skipped": 0,
                "execution_time": 0,
                "error_message": str(e)
            }
    
    async def _run_integration_tests(self) -> None:
        """Run integration workflow tests"""
        print("\n🏗️  RUNNING INTEGRATION TESTS")
        print("-" * 50)
        
        try:
            integration_suite = IntegrationTestSuite()
            await integration_suite.run_all_integration_tests()
            
            summary = integration_suite.get_summary()
            self.test_results["integration"] = summary
            
            print("✅ Integration tests completed")
            
        except Exception as e:
            print(f"❌ Integration tests failed: {e}")
            self.test_results["integration"] = {
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "errors": 1,
                "skipped": 0,
                "execution_time": 0,
                "error_message": str(e)
            }
    
    async def _generate_master_report(self) -> None:
        """Generate comprehensive master test report"""
        total_time = time.time() - self.start_time if self.start_time else 0
        
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("=" * 80)
        
        # Calculate totals
        self._calculate_totals()
        
        print(f"⏱️  Total Execution Time: {total_time:.2f} seconds")
        print(f"📊 Total Tests: {self.total_tests}")
        print(f"✅ Passed: {self.total_passed}")
        print(f"❌ Failed: {self.total_failed}")
        print(f"⚠️  Errors: {self.total_errors}")
        
        success_rate = (self.total_passed / self.total_tests * 100) if self.total_tests > 0 else 0
        print(f"📈 Overall Success Rate: {success_rate:.1f}%")
        
        print("\n📋 TEST SUITE BREAKDOWN:")
        print("-" * 80)
        
        for suite_name, results in self.test_results.items():
            if "error_message" in results:
                print(f"❌ {suite_name.title()}: ERROR - {results['error_message']}")
            else:
                suite_success = (results['passed'] / results['total_tests'] * 100) if results['total_tests'] > 0 else 0
                status_icon = "✅" if suite_success >= 90 else "⚠️" if suite_success >= 70 else "❌"
                print(f"{status_icon} {suite_name.title()}: {results['passed']}/{results['total_tests']} ({suite_success:.1f}%) - {results['execution_time']:.2f}s")
                
                # Show controller breakdown for controller tests
                if suite_name == "controllers" and "controller_summaries" in results:
                    for controller, summary in results["controller_summaries"].items():
                        ctrl_success = summary.get('success_rate', 0)
                        ctrl_icon = "✅" if ctrl_success >= 80 else "⚠️" if ctrl_success >= 50 else "❌"
                        print(f"    {ctrl_icon} {controller.title()}: {summary.get('passed', 0)}/{summary.get('total_tests', 0)} ({ctrl_success:.1f}%)")
        
        # Performance insights
        print("\n📈 PERFORMANCE INSIGHTS:")
        print("-" * 80)
        
        if "performance" in self.test_results and "error_message" not in self.test_results["performance"]:
            perf_time = self.test_results["performance"]["execution_time"]
            perf_tests = self.test_results["performance"]["total_tests"]
            if perf_tests > 0:
                avg_perf_time = perf_time / perf_tests
                print(f"⚡ Performance Tests: {perf_tests} tests in {perf_time:.2f}s (avg: {avg_perf_time:.3f}s/test)")
        
        # Quality assessment
        print("\n🎯 QUALITY ASSESSMENT:")
        print("-" * 80)
        
        if success_rate >= 95:
            print("🎉 EXCELLENT: System is highly stable and robust!")
        elif success_rate >= 85:
            print("👍 GOOD: System is stable with minor issues to investigate.")
        elif success_rate >= 70:
            print("⚠️  ACCEPTABLE: System works but needs attention for failed tests.")
        elif success_rate >= 50:
            print("⚠️  CONCERNING: Multiple issues detected. Review required.")
        else:
            print("🚨 CRITICAL: Major issues detected. Immediate attention needed!")
        
        # Recommendations
        print("\n💡 RECOMMENDATIONS:")
        print("-" * 80)
        
        if self.total_failed > 0:
            print(f"🔍 Investigate {self.total_failed} failed tests for potential issues")
        
        if self.total_errors > 0:
            print(f"🛠️  Fix {self.total_errors} error conditions")
        
        if "performance" in self.test_results:
            print("📊 Review performance metrics for optimization opportunities")
        
        if "edge_cases" in self.test_results:
            print("🎯 Ensure edge cases are properly handled in production")
        
        print(f"\n📝 Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
    
    async def _generate_quick_report(self) -> None:
        """Generate quick validation report"""
        total_time = time.time() - self.start_time if self.start_time else 0
        
        print("\n" + "=" * 60)
        print("⚡ QUICK VALIDATION REPORT")
        print("=" * 60)
        
        self._calculate_totals()
        
        print(f"⏱️  Execution Time: {total_time:.2f} seconds")
        print(f"📊 Tests: {self.total_tests}")
        print(f"✅ Passed: {self.total_passed}")
        print(f"❌ Failed: {self.total_failed}")
        
        success_rate = (self.total_passed / self.total_tests * 100) if self.total_tests > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 VALIDATION PASSED: System ready for use!")
        elif success_rate >= 70:
            print("⚠️  VALIDATION PARTIAL: Some issues detected")
        else:
            print("❌ VALIDATION FAILED: Critical issues found")
        
        print("=" * 60)
    
    async def _generate_specific_report(self, suite_name: str) -> None:
        """Generate report for specific test suite"""
        total_time = time.time() - self.start_time if self.start_time else 0
        
        print(f"\n{'=' * 60}")
        print(f"📊 {suite_name.upper()} TEST SUITE REPORT")
        print("=" * 60)
        
        if suite_name.lower() in self.test_results:
            results = self.test_results[suite_name.lower()]
            
            if "error_message" in results:
                print(f"❌ Test suite failed: {results['error_message']}")
            else:
                print(f"⏱️  Execution Time: {total_time:.2f} seconds")
                print(f"📊 Total Tests: {results['total_tests']}")
                print(f"✅ Passed: {results['passed']}")
                print(f"❌ Failed: {results['failed']}")
                print(f"⚠️  Errors: {results['errors']}")
                
                success_rate = (results['passed'] / results['total_tests'] * 100) if results['total_tests'] > 0 else 0
                print(f"📈 Success Rate: {success_rate:.1f}%")
        
        print("=" * 60)
    
    def _calculate_totals(self) -> None:
        """Calculate total test statistics"""
        self.total_tests = 0
        self.total_passed = 0
        self.total_failed = 0
        self.total_errors = 0
        
        for results in self.test_results.values():
            if "error_message" not in results:
                self.total_tests += results.get('total_tests', 0)
                self.total_passed += results.get('passed', 0)
                self.total_failed += results.get('failed', 0)
                self.total_errors += results.get('errors', 0)
            else:
                self.total_errors += 1


async def main():
    """Main entry point for master test runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Cadwork MCP Master Test Runner")
    parser.add_argument('--mode', choices=['comprehensive', 'quick', 'controllers', 'performance', 'edge', 'integration'],
                       default='comprehensive', help='Test mode to run')
    parser.add_argument('--no-stress', action='store_true',
                       help='Skip stress tests in comprehensive mode')
    
    args = parser.parse_args()
    
    runner = MasterTestRunner()
    
    try:
        if args.mode == 'comprehensive':
            await runner.run_comprehensive_tests(include_stress_tests=not args.no_stress)
        elif args.mode == 'quick':
            await runner.run_quick_validation()
        else:
            await runner.run_specific_suite(args.mode)
            
    except KeyboardInterrupt:
        print("\n⏹️  Test execution interrupted by user")
    except Exception as e:
        print(f"\n❌ Master test runner error: {e}")


if __name__ == "__main__":
    print("🚀 CADWORK MCP MASTER TEST RUNNER")
    print("🔧 Ensure Cadwork 3D is running and MCP Bridge is started!")
    print()
    
    asyncio.run(main())
