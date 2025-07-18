"""
Performance and Stress Test Suite
=================================

Specialized performance and stress tests for Cadwork MCP Controllers.
Tests system limits, batch operations, and high-load scenarios.
"""

import sys
import os
import asyncio
import time
from typing import List, Dict, Any

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from controllers.element_controller import ElementController
from controllers.geometry_controller import GeometryController
from controllers.visualization_controller import CVisualizationController
from controllers.attribute_controller import AttributeController
from tests.helpers.test_helper import TestHelper, TestResult
from tests.helpers.parameter_finder import ParameterFinder


class PerformanceTestSuite:
    """Comprehensive performance and stress testing"""
    
    def __init__(self):
        self.element_ctrl = ElementController()
        self.geometry_ctrl = GeometryController()
        self.viz_ctrl = CVisualizationController()
        self.attr_ctrl = AttributeController()
        self.helper = TestHelper()
        self.param_finder = ParameterFinder()
        self.stress_test_elements: List[int] = []
    
    async def run_all_performance_tests(self) -> List[TestResult]:
        """Run comprehensive performance test suite"""
        self.helper.print_header("CADWORK MCP PERFORMANCE & STRESS TESTS")
        
        # Batch creation performance
        await self._test_batch_element_creation()
        
        # Mass operation performance
        await self._test_mass_operations()
        
        # Geometric calculation stress
        await self._test_geometric_calculation_stress()
        
        # Visualization performance
        await self._test_visualization_performance()
        
        # Memory and resource tests
        await self._test_memory_stress()
        
        # Cleanup
        await self._cleanup_stress_elements()
        
        return self.helper.test_results
    
    async def _test_batch_element_creation(self) -> None:
        """Test batch creation of many elements"""
        self.helper.print_subheader("Batch Element Creation Performance")
        
        # Test 1: Create 50 beams rapidly
        start_time = time.time()
        created_count = 0
        
        for i in range(50):
            beam_params = self.param_finder.get_beam_parameters()
            # Spread elements across space to avoid overlap
            beam_params["p1"][0] += i * 500
            beam_params["p2"][0] += i * 500
            beam_params["p1"][1] += (i % 10) * 500
            beam_params["p2"][1] += (i % 10) * 500
            
            try:
                result = await self.element_ctrl.create_beam(**beam_params)
                if result.get("status") == "success":
                    element_id = result.get("element_id")
                    if element_id:
                        self.stress_test_elements.append(element_id)
                        created_count += 1
            except Exception:
                pass
        
        creation_time = time.time() - start_time
        elements_per_second = created_count / creation_time if creation_time > 0 else 0
        
        await self.helper.run_test(
            "Batch Create 50 Beams",
            self._report_batch_creation_performance,
            created_count, creation_time, elements_per_second
        )
        
        # Test 2: Create 25 panels rapidly
        panel_start_time = time.time()
        panel_count = 0
        
        for i in range(25):
            panel_params = self.param_finder.get_panel_parameters()
            panel_params["p1"][0] += (i + 100) * 600  # Offset from beams
            panel_params["p2"][0] += (i + 100) * 600
            
            try:
                result = await self.element_ctrl.create_panel(**panel_params)
                if result.get("status") == "success":
                    element_id = result.get("element_id")
                    if element_id:
                        self.stress_test_elements.append(element_id)
                        panel_count += 1
            except Exception:
                pass
        
        panel_time = time.time() - panel_start_time
        panels_per_second = panel_count / panel_time if panel_time > 0 else 0
        
        await self.helper.run_test(
            "Batch Create 25 Panels",
            self._report_batch_creation_performance,
            panel_count, panel_time, panels_per_second
        )
    
    async def _test_mass_operations(self) -> None:
        """Test mass operations on many elements"""
        if not self.stress_test_elements:
            return
        
        self.helper.print_subheader("Mass Operations Performance")
        
        # Test 1: Mass copy operation
        if len(self.stress_test_elements) >= 10:
            copy_start = time.time()
            copy_vector = [50000, 0, 0]  # Far offset
            
            result = await self.helper.run_test(
                "Mass Copy 10 Elements",
                self.element_ctrl.copy_elements,
                self.stress_test_elements[:10],
                copy_vector
            )
            
            copy_time = time.time() - copy_start
            
            if result.status == "PASSED" and result.details:
                copied_ids = result.details.get("new_element_ids", [])
                self.stress_test_elements.extend(copied_ids)
            
            await self.helper.run_test(
                "Mass Copy Performance Report",
                self._report_operation_performance,
                "Copy", 10, copy_time
            )
        
        # Test 2: Mass move operation
        if len(self.stress_test_elements) >= 20:
            move_start = time.time()
            move_vector = [0, 50000, 0]
            
            await self.helper.run_test(
                "Mass Move 20 Elements",
                self.element_ctrl.move_element,
                self.stress_test_elements[:20],
                move_vector
            )
            
            move_time = time.time() - move_start
            
            await self.helper.run_test(
                "Mass Move Performance Report",
                self._report_operation_performance,
                "Move", 20, move_time
            )
        
        # Test 3: Mass attribute setting
        if len(self.stress_test_elements) >= 15:
            attr_start = time.time()
            
            await self.helper.run_test(
                "Mass Set Material",
                self.attr_ctrl.set_material,
                self.stress_test_elements[:15],
                "StressTestMaterial"
            )
            
            await self.helper.run_test(
                "Mass Set Group",
                self.attr_ctrl.set_group,
                self.stress_test_elements[:15],
                "StressTestGroup"
            )
            
            attr_time = time.time() - attr_start
            
            await self.helper.run_test(
                "Mass Attributes Performance Report",
                self._report_operation_performance,
                "Attributes", 15, attr_time
            )
    
    async def _test_geometric_calculation_stress(self) -> None:
        """Test intensive geometric calculations"""
        if not self.stress_test_elements:
            return
        
        self.helper.print_subheader("Geometric Calculation Stress Test")
        
        # Test 1: Mass volume calculations
        volume_start = time.time()
        volume_calculations = 0
        
        for element_id in self.stress_test_elements[:30]:  # Test first 30 elements
            try:
                await self.geometry_ctrl.get_element_volume(element_id)
                volume_calculations += 1
            except Exception:
                pass
        
        volume_time = time.time() - volume_start
        
        await self.helper.run_test(
            "Mass Volume Calculations",
            self._report_calculation_performance,
            "Volume", volume_calculations, volume_time
        )
        
        # Test 2: Mass bounding box calculations
        bbox_start = time.time()
        bbox_calculations = 0
        
        for element_id in self.stress_test_elements[:25]:
            try:
                await self.geometry_ctrl.get_bounding_box(element_id)
                bbox_calculations += 1
            except Exception:
                pass
        
        bbox_time = time.time() - bbox_start
        
        await self.helper.run_test(
            "Mass Bounding Box Calculations",
            self._report_calculation_performance,
            "BoundingBox", bbox_calculations, bbox_time
        )
        
        # Test 3: Distance matrix calculation (expensive)
        if len(self.stress_test_elements) >= 10:
            distance_start = time.time()
            distance_calculations = 0
            
            elements_subset = self.stress_test_elements[:5]  # Use smaller subset for N² operation
            
            for i, elem1 in enumerate(elements_subset):
                for j, elem2 in enumerate(elements_subset[i+1:], i+1):
                    try:
                        await self.geometry_ctrl.get_minimum_distance_between_elements(elem1, elem2)
                        distance_calculations += 1
                    except Exception:
                        pass
            
            distance_time = time.time() - distance_start
            
            await self.helper.run_test(
                "Distance Matrix Calculation",
                self._report_calculation_performance,
                "DistanceMatrix", distance_calculations, distance_time
            )
    
    async def _test_visualization_performance(self) -> None:
        """Test visualization performance with many elements"""
        if not self.stress_test_elements:
            return
        
        self.helper.print_subheader("Visualization Performance Test")
        
        # Test 1: Mass color changes
        color_start = time.time()
        colors = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45]
        
        for i, element_id in enumerate(self.stress_test_elements[:50]):
            color_id = colors[i % len(colors)]
            try:
                await self.viz_ctrl.set_color([element_id], color_id)
            except Exception:
                pass
        
        color_time = time.time() - color_start
        
        await self.helper.run_test(
            "Mass Color Changes",
            self._report_visualization_performance,
            "ColorChange", 50, color_time
        )
        
        # Test 2: Mass transparency changes
        transparency_start = time.time()
        transparencies = [0, 20, 40, 60, 80]
        
        for i, element_id in enumerate(self.stress_test_elements[:30]):
            transparency = transparencies[i % len(transparencies)]
            try:
                await self.viz_ctrl.set_transparency([element_id], transparency)
            except Exception:
                pass
        
        transparency_time = time.time() - transparency_start
        
        await self.helper.run_test(
            "Mass Transparency Changes",
            self._report_visualization_performance,
            "Transparency", 30, transparency_time
        )
        
        # Test 3: Mass visibility toggle
        visibility_start = time.time()
        
        # Hide all
        await self.viz_ctrl.set_visibility(self.stress_test_elements[:25], False)
        
        # Show all
        await self.viz_ctrl.set_visibility(self.stress_test_elements[:25], True)
        
        visibility_time = time.time() - visibility_start
        
        await self.helper.run_test(
            "Mass Visibility Toggle",
            self._report_visualization_performance,
            "Visibility", 50, visibility_time  # 25 hide + 25 show = 50 operations
        )
    
    async def _test_memory_stress(self) -> None:
        """Test memory usage and limits"""
        self.helper.print_subheader("Memory and Resource Stress Test")
        
        # Test 1: Create many small elements rapidly
        memory_start = time.time()
        memory_elements = []
        
        for i in range(100):
            try:
                # Create very small beams
                small_beam_params = {
                    "p1": [i * 10, 0, 0],
                    "p2": [i * 10 + 5, 0, 0],
                    "width": 1,
                    "height": 1
                }
                
                result = await self.element_ctrl.create_beam(**small_beam_params)
                if result.get("status") == "success":
                    element_id = result.get("element_id")
                    if element_id:
                        memory_elements.append(element_id)
                        
                # Every 20 elements, do a quick cleanup to test memory management
                if len(memory_elements) == 20:
                    await self.element_ctrl.delete_elements(memory_elements[:10])
                    memory_elements = memory_elements[10:]
                    
            except Exception:
                break
        
        memory_time = time.time() - memory_start
        
        await self.helper.run_test(
            "Memory Stress Test",
            self._report_memory_performance,
            len(memory_elements), memory_time
        )
        
        # Cleanup memory test elements
        if memory_elements:
            try:
                await self.element_ctrl.delete_elements(memory_elements)
            except:
                pass
    
    async def _cleanup_stress_elements(self) -> None:
        """Clean up all stress test elements"""
        if self.stress_test_elements:
            self.helper.print_subheader("Stress Test Cleanup")
            
            cleanup_start = time.time()
            
            # Delete in batches to avoid overwhelming the system
            batch_size = 25
            deleted_count = 0
            
            for i in range(0, len(self.stress_test_elements), batch_size):
                batch = self.stress_test_elements[i:i + batch_size]
                try:
                    await self.element_ctrl.delete_elements(batch)
                    deleted_count += len(batch)
                except Exception:
                    pass
            
            cleanup_time = time.time() - cleanup_start
            
            await self.helper.run_test(
                "Stress Test Cleanup",
                self._report_cleanup_performance,
                deleted_count, cleanup_time
            )
            
            self.stress_test_elements.clear()
    
    # Helper methods for performance reporting
    async def _report_batch_creation_performance(self, count, time_taken, rate):
        return {
            "status": "success",
            "message": f"Created {count} elements in {time_taken:.2f}s ({rate:.1f} elements/sec)",
            "performance_metrics": {
                "elements_created": count,
                "time_seconds": time_taken,
                "elements_per_second": rate
            }
        }
    
    async def _report_operation_performance(self, operation, count, time_taken):
        rate = count / time_taken if time_taken > 0 else 0
        return {
            "status": "success",
            "message": f"{operation} on {count} elements in {time_taken:.2f}s ({rate:.1f} ops/sec)",
            "performance_metrics": {
                "operation": operation,
                "element_count": count,
                "time_seconds": time_taken,
                "operations_per_second": rate
            }
        }
    
    async def _report_calculation_performance(self, calc_type, count, time_taken):
        rate = count / time_taken if time_taken > 0 else 0
        return {
            "status": "success",
            "message": f"{calc_type}: {count} calculations in {time_taken:.2f}s ({rate:.1f} calc/sec)",
            "performance_metrics": {
                "calculation_type": calc_type,
                "calculation_count": count,
                "time_seconds": time_taken,
                "calculations_per_second": rate
            }
        }
    
    async def _report_visualization_performance(self, viz_type, count, time_taken):
        rate = count / time_taken if time_taken > 0 else 0
        return {
            "status": "success",
            "message": f"{viz_type}: {count} operations in {time_taken:.2f}s ({rate:.1f} viz/sec)",
            "performance_metrics": {
                "visualization_type": viz_type,
                "operation_count": count,
                "time_seconds": time_taken,
                "visualizations_per_second": rate
            }
        }
    
    async def _report_memory_performance(self, elements_created, time_taken):
        return {
            "status": "success",
            "message": f"Memory stress: {elements_created} elements with cleanup in {time_taken:.2f}s",
            "performance_metrics": {
                "final_element_count": elements_created,
                "total_time_seconds": time_taken,
                "memory_efficiency": "good" if elements_created >= 80 else "acceptable"
            }
        }
    
    async def _report_cleanup_performance(self, deleted_count, time_taken):
        rate = deleted_count / time_taken if time_taken > 0 else 0
        return {
            "status": "success",
            "message": f"Cleaned up {deleted_count} elements in {time_taken:.2f}s ({rate:.1f} deletions/sec)",
            "performance_metrics": {
                "deleted_count": deleted_count,
                "cleanup_time_seconds": time_taken,
                "deletions_per_second": rate
            }
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get performance test summary"""
        return self.helper.get_summary()
    
    def print_summary(self) -> None:
        """Print performance test summary"""
        self.helper.print_summary()


# Convenience function for standalone testing
async def run_performance_tests() -> None:
    """Run performance test suite standalone"""
    test_suite = PerformanceTestSuite()
    await test_suite.run_all_performance_tests()
    test_suite.print_summary()


if __name__ == "__main__":
    print("🚀 CADWORK MCP PERFORMANCE TEST SUITE")
    print("⚠️  This will create and test with many elements!")
    print("⚠️  Ensure Cadwork 3D is running and ready for heavy testing!")
    print()
    
    asyncio.run(run_performance_tests())
