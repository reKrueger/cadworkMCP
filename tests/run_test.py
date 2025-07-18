#!/usr/bin/env python3
"""
New Cadwork MCP Test Runner - Restructured & Organized
====================================================

Orchestrates all controller tests with modular structure.
Clean organization, detailed reporting, and easy extension.

Usage:
    python run_test.py [--quick] [--controller=element] [--verbose]
"""

import sys
import os
import asyncio
import argparse
from typing import Dict, Any, List, Optional
import time

# Add project root to path  
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import helper classes
from helpers.test_helper import TestHelper, TestResult
from helpers.parameter_finder import ParameterFinder
from helpers.result_validator import ResultValidator

# Import test controllers
try:
    from controllers.test_element_controller import TestElementController
    from controllers.test_geometry_controller import TestGeometryController
    from controllers.test_attribute_controller import TestAttributeController
    from controllers.test_visualization_controller import TestVisualizationController
    from controllers.test_utility_controller import TestUtilityController
    from controllers.test_export_controller import TestExportController
    from controllers.test_import_controller import TestImportController
    from controllers.test_material_controller import TestMaterialController
    from controllers.test_measurement_controller import TestMeasurementController
    from controllers.test_machine_controller import TestMachineController
    from controllers.test_roof_controller import TestRoofController
    from controllers.test_shop_drawing_controller import TestShopDrawingController
except ImportError as e:
    print(f"⚠️  Warning: Some test controllers not yet available: {e}")


class CadworkTestRunner:
    """Main test runner orchestrating all controller tests"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.helper = TestHelper()
        self.all_results: List[TestResult] = []
        self.controller_summaries: Dict[str, Dict[str, Any]] = {}
        
        # Available test controllers
        self.test_controllers = {
            'element': TestElementController,
            'geometry': TestGeometryController, 
            'attribute': TestAttributeController,
            'visualization': TestVisualizationController,
            'utility': TestUtilityController,
            'export': TestExportController,
            'import': TestImportController,
            'material': TestMaterialController,
            'measurement': TestMeasurementController,
            'machine': TestMachineController,
            'roof': TestRoofController,
            'shop_drawing': TestShopDrawingController,
        }
    
    async def run_all_tests(self, quick_mode: bool = False) -> None:
        """Run all available controller tests"""
        self.helper.print_header("🚀 CADWORK MCP TEST SUITE")
        print(f"Mode: {'Quick Tests' if quick_mode else 'Full Test Suite'}")
        print(f"Available Controllers: {len(self.test_controllers)}")
        print()
        
        total_start_time = time.time()
        
        for controller_name, controller_class in self.test_controllers.items():
            await self._run_controller_tests(controller_name, controller_class, quick_mode)
        
        total_time = time.time() - total_start_time
        self._print_final_summary(total_time)
    
    async def run_specific_controller(self, controller_name: str, quick_mode: bool = False) -> None:
        """Run tests for a specific controller"""
        if controller_name not in self.test_controllers:
            print(f"❌ Controller '{controller_name}' not found!")
            print(f"Available controllers: {list(self.test_controllers.keys())}")
            return
        
        self.helper.print_header(f"🎯 TESTING {controller_name.upper()} CONTROLLER")
        
        controller_class = self.test_controllers[controller_name]
        await self._run_controller_tests(controller_name, controller_class, quick_mode)
        
        self._print_final_summary()
    
    async def _run_controller_tests(self, name: str, controller_class, quick_mode: bool) -> None:
        """Run tests for a single controller"""
        try:
            print(f"🔧 Testing {name.title()} Controller...")
            
            # Initialize controller test suite
            test_suite = controller_class()
            
            # Run tests (quick or full)
            if quick_mode and hasattr(test_suite, 'run_quick_tests'):
                results = await test_suite.run_quick_tests()
            else:
                results = await test_suite.run_all_tests()
            
            # Collect results
            self.all_results.extend(results)
            
            # Get controller summary
            if hasattr(test_suite, 'get_summary'):
                summary = test_suite.get_summary()
                self.controller_summaries[name] = summary
                
                # Print brief controller summary
                print(f"   ✅ {summary['passed']}/{summary['total_tests']} tests passed " +
                      f"({summary['success_rate']:.1f}%)")
            
        except Exception as e:
            print(f"   ❌ Error testing {name} controller: {e}")
            if self.verbose:
                import traceback
                traceback.print_exc()
    
    def _print_final_summary(self, total_time: Optional[float] = None) -> None:
        """Print comprehensive final summary"""
        self.helper.print_header("📊 FINAL TEST SUMMARY")
        
        # Overall statistics
        total_tests = len(self.all_results)
        passed = len([r for r in self.all_results if r.status == "PASSED"])
        failed = len([r for r in self.all_results if r.status == "FAILED"])
        errors = len([r for r in self.all_results if r.status == "ERROR"])
        skipped = len([r for r in self.all_results if r.status == "SKIPPED"])
        
        success_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        avg_time = sum(r.execution_time for r in self.all_results) / total_tests if total_tests > 0 else 0
        
        print(f"🎯 Overall Results:")
        print(f"   Total Tests:    {total_tests}")
        print(f"   Passed:         {passed} ✅")
        print(f"   Failed:         {failed} ❌") 
        print(f"   Errors:         {errors} ⚠️")
        print(f"   Skipped:        {skipped} ⏭️")
        print(f"   Success Rate:   {success_rate:.1f}%")
        print(f"   Avg Test Time:  {avg_time:.3f}s")
        
        if total_time:
            print(f"   Total Runtime:  {total_time:.2f}s")
        
        # Controller breakdown
        if self.controller_summaries:
            print(f"\n📋 Controller Breakdown:")
            for controller, summary in self.controller_summaries.items():
                status_icon = "✅" if summary['success_rate'] >= 80 else "⚠️" if summary['success_rate'] >= 50 else "❌"
                print(f"   {status_icon} {controller.title():15} {summary['passed']:2}/{summary['total_tests']:2} " +
                      f"({summary['success_rate']:5.1f}%)")
        
        # Failed tests details
        failed_tests = [r for r in self.all_results if r.status in ["FAILED", "ERROR"]]
        if failed_tests and self.verbose:
            print(f"\n🔍 Failed Tests Details:")
            print("-" * 60)
            for test in failed_tests[:10]:  # Show first 10 failures
                print(f"{test.status}: {test.name}")
                print(f"    {test.message}")
                print()
            
            if len(failed_tests) > 10:
                print(f"... and {len(failed_tests) - 10} more failures")
        
        # Recommendations
        print(f"\n💡 Recommendations:")
        if success_rate >= 90:
            print("   🎉 Excellent! All systems working well.")
        elif success_rate >= 70:
            print("   👍 Good results. Minor issues to investigate.")
        elif success_rate >= 50:
            print("   ⚠️  Some issues detected. Check failed tests.")
        else:
            print("   🚨 Multiple failures. Check Cadwork connection.")
            print("   💡 Ensure Cadwork 3D is running and MCP Bridge is started.")


async def main():
    """Main entry point with command line arguments"""
    parser = argparse.ArgumentParser(description="Cadwork MCP Test Runner")
    parser.add_argument('--quick', action='store_true', 
                       help='Run quick tests only')
    parser.add_argument('--controller', type=str,
                       help='Run tests for specific controller only')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output with detailed error info')
    parser.add_argument('--list', action='store_true',
                       help='List available controllers')
    
    args = parser.parse_args()
    
    runner = CadworkTestRunner(verbose=args.verbose)
    
    if args.list:
        print("Available test controllers:")
        for name in runner.test_controllers.keys():
            print(f"  - {name}")
        return
    
    try:
        if args.controller:
            await runner.run_specific_controller(args.controller, args.quick)
        else:
            await runner.run_all_tests(args.quick)
            
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test runner error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    # Check if Cadwork connection would be available
    print("🔧 Cadwork MCP Test Runner")
    print("⚠️  Ensure Cadwork 3D is running and MCP Bridge is started!")
    print()
    
    asyncio.run(main())
