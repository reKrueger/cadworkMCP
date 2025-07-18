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
    
    async def run_advanced_measurement_tests(self) -> list:
        """Run advanced measurement and calculation tests"""
        self.helper.print_header("MEASUREMENT CONTROLLER - ADVANCED TESTS")
        
        # Test 1: Complex polygon area calculations
        complex_polygons = [
            {
                "name": "Pentagon",
                "vertices": [
                    [0, 0, 0],
                    [1000, 0, 0],
                    [1500, 951, 0],
                    [500, 1539, 0],
                    [-500, 951, 0]
                ]
            },
            {
                "name": "L-Shape",
                "vertices": [
                    [0, 0, 0],
                    [2000, 0, 0],
                    [2000, 1000, 0],
                    [1000, 1000, 0],
                    [1000, 2000, 0],
                    [0, 2000, 0]
                ]
            },
            {
                "name": "Star Shape",
                "vertices": [
                    [1000, 0, 0],
                    [1200, 800, 0],
                    [2000, 800, 0],
                    [1400, 1200, 0],
                    [1600, 2000, 0],
                    [1000, 1600, 0],
                    [400, 2000, 0],
                    [600, 1200, 0],
                    [0, 800, 0],
                    [800, 800, 0]
                ]
            }
        ]
        
        for polygon in complex_polygons:
            await self.helper.run_test(
                f"Measure {polygon['name']} Area",
                self.controller.measure_area,
                polygon["vertices"]
            )
        
        # Test 2: Distance measurements in different coordinate systems
        distance_test_cases = [
            ("XY Plane Distance", [0, 0, 0], [1000, 1000, 0]),
            ("XZ Plane Distance", [0, 0, 0], [1000, 0, 1000]),
            ("YZ Plane Distance", [0, 0, 0], [0, 1000, 1000]),
            ("3D Diagonal", [0, 0, 0], [1000, 1000, 1000]),
            ("Negative Coordinates", [-500, -500, -500], [500, 500, 500])
        ]
        
        for test_name, p1, p2 in distance_test_cases:
            await self.helper.run_test(
                test_name,
                self.controller.measure_distance,
                p1, p2
            )
        
        # Test 3: Special angle measurements
        angle_test_cases = [
            ("90 Degree Angle", [1, 0, 0], [0, 1, 0]),
            ("180 Degree Angle", [1, 0, 0], [-1, 0, 0]),
            ("45 Degree Angle", [1, 0, 0], [1, 1, 0]),
            ("3D Angle", [1, 1, 1], [1, -1, 1]),
            ("Obtuse Angle", [1, 0, 0], [-1, 1, 0])
        ]
        
        for test_name, v1, v2 in angle_test_cases:
            await self.helper.run_test(
                test_name,
                self.controller.measure_angle,
                v1, v2
            )
        
        # Test 4: Measurement validation and error handling
        validation_test_cases = [
            ("Zero Length Vector", [0, 0, 0], [1, 0, 0]),
            ("Identical Points", [100, 100, 100], [100, 100, 100]),
            ("Invalid Polygon (2 points)", [[0, 0, 0], [1, 0, 0]]),
            ("Collinear Polygon", [[0, 0, 0], [1, 0, 0], [2, 0, 0]])
        ]
        
        validation_results = []
        for test_name, *args in validation_test_cases:
            try:
                if "Vector" in test_name:
                    result = await self.controller.measure_angle(*args)
                elif "Points" in test_name:
                    result = await self.controller.measure_distance(*args)
                else:
                    result = await self.controller.measure_area(args[0])
                
                validation_results.append(f"{test_name}: {result.get('status', 'unknown')}")
            except Exception as e:
                validation_results.append(f"{test_name}: exception handled")
        
        await self.helper.run_test(
            "Measurement Validation Summary",
            self._create_validation_summary,
            validation_results
        )
        
        # Test 5: Performance test with large datasets
        large_polygon = []
        for i in range(100):  # 100-sided polygon
            angle = 2 * 3.14159 * i / 100
            x = 1000 * (1 + 0.1 * (i % 10)) * round(1000 * (1 + 0.5 * __import__('math').cos(angle)))
            y = 1000 * (1 + 0.1 * (i % 10)) * round(1000 * (1 + 0.5 * __import__('math').sin(angle)))
            large_polygon.append([x, y, 0])
        
        await self.helper.run_test(
            "Large Polygon Performance Test",
            self.controller.measure_area,
            large_polygon
        )
        
        return self.helper.test_results
    
    async def _create_validation_summary(self, validation_results):
        """Create summary of validation test results"""
        successful_validations = sum(1 for result in validation_results if "error" in result or "exception" in result)
        total_validations = len(validation_results)
        
        return {
            "status": "success" if successful_validations >= total_validations * 0.5 else "partial",
            "message": f"Validation tests: {successful_validations}/{total_validations} handled appropriately",
            "details": validation_results
        }
