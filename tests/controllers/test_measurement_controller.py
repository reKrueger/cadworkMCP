"""Test Measurement Controller"""
import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)

from controllers.measurement_controller import CMeasurementController
from tests.helpers.test_helper import TestHelper

class TestMeasurementController:
    def __init__(self):
        self.controller = CMeasurementController()
        self.helper = TestHelper()
    
    async def run_all_tests(self) -> list:
        self.helper.print_header("MEASUREMENT CONTROLLER TESTS")
        await self.helper.run_test("Measure Distance", self.controller.measure_distance, [0,0,0], [1000,0,0])
        await self.helper.run_test("Measure Angle", self.controller.measure_angle, [1,0,0], [0,1,0])
        return self.helper.test_results
    
    async def run_extended_tests(self) -> list:
        """Run extended measurement controller tests with 5 new test cases"""
        self.helper.print_header("MEASUREMENT CONTROLLER EXTENDED TESTS")
        
        # Test 1: Measure diagonal distance in 3D space
        await self.helper.run_test(
            "Measure 3D Diagonal Distance",
            self.controller.measure_distance,
            [0, 0, 0],
            [1000, 1000, 1000]
        )
        
        # Test 2: Measure angle between perpendicular vectors
        await self.helper.run_test(
            "Measure Perpendicular Angle",
            self.controller.measure_angle,
            [1, 0, 0],  # X-axis
            [0, 0, 1]   # Z-axis (should be 90 degrees)
        )
        
        # Test 3: Measure angle between parallel vectors
        await self.helper.run_test(
            "Measure Parallel Angle",
            self.controller.measure_angle,
            [1, 0, 0],   # X-axis
            [2, 0, 0]    # Same direction (should be 0 degrees)
        )
        
        # Test 4: Measure area of a rectangle
        rectangle_vertices = [
            [0, 0, 0],
            [1000, 0, 0],
            [1000, 500, 0],
            [0, 500, 0]
        ]
        await self.helper.run_test(
            "Measure Rectangle Area",
            self.controller.measure_area,
            rectangle_vertices
        )
        
        # Test 5: Measure area of a triangle
        triangle_vertices = [
            [0, 0, 0],
            [1000, 0, 0],
            [500, 866, 0]  # Equilateral triangle (approximately)
        ]
        await self.helper.run_test(
            "Measure Triangle Area",
            self.controller.measure_area,
            triangle_vertices
        )
        
        return self.helper.test_results
    
    async def run_quick_tests(self) -> list:
        self.helper.print_header("MEASUREMENT CONTROLLER - QUICK TESTS")
        await self.helper.run_test("Quick Distance", self.controller.measure_distance, [0,0,0], [100,0,0])
        return self.helper.test_results
    
    def get_summary(self): return self.helper.get_summary()
    def print_summary(self): self.helper.print_summary()
