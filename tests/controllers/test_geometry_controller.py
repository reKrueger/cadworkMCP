"""Test Geometry Controller - Tests for geometric operations and calculations"""
import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)

from controllers.geometry_controller import GeometryController
from helpers.test_helper import TestHelper, TestResult
from helpers.parameter_finder import ParameterFinder
from typing import List

class TestGeometryController:
    def __init__(self):
        self.controller = GeometryController()
        self.helper = TestHelper()
        self.param_finder = ParameterFinder()
    
    async def run_all_tests(self) -> List[TestResult]:
        self.helper.print_header("GEOMETRY CONTROLLER TESTS")
        
        # Get test element for geometry operations
        from controllers.element_controller import ElementController
        element_ctrl = ElementController()
        beam_params = self.param_finder.get_beam_parameters()
        
        # Create test element
        result = await element_ctrl.create_beam(**beam_params)
        if result.get("status") == "success":
            element_id = result.get("element_id")
            
            # Test geometric queries
            await self.helper.run_test("Get Element Width", self.controller.get_element_width, element_id)
            await self.helper.run_test("Get Element Height", self.controller.get_element_height, element_id)
            await self.helper.run_test("Get Element Length", self.controller.get_element_length, element_id)
            await self.helper.run_test("Get Element Volume", self.controller.get_element_volume, element_id)
            await self.helper.run_test("Get Element P1", self.controller.get_element_p1, element_id)
            await self.helper.run_test("Get Element P2", self.controller.get_element_p2, element_id)
            await self.helper.run_test("Get Bounding Box", self.controller.get_bounding_box, element_id)
            await self.helper.run_test("Get Center of Gravity", self.controller.get_center_of_gravity, element_id)
            
            # Cleanup
            await element_ctrl.delete_elements([element_id])
        
        return self.helper.test_results
    
    async def run_quick_tests(self) -> List[TestResult]:
        self.helper.print_header("GEOMETRY CONTROLLER - QUICK TESTS") 
        # Quick geometry tests without element creation
        await self.helper.run_test("Quick Geometry Test", self._quick_test)
        return self.helper.test_results
    
    async def _quick_test(self):
        return {"status": "success", "message": "Geometry controller loaded"}
    
    def get_summary(self): return self.helper.get_summary()
    def print_summary(self): self.helper.print_summary()
 element_id)
            await self.helper.run_test("Get Element P3", self.controller.get_element_p3, element_id)
            await self.helper.run_test("Get Element Vertices", self.controller.get_element_vertices, element_id)
            await self.helper.run_test("Get Element Outline", self.controller.get_element_outline, element_id)
            await self.helper.run_test("Get Reference Face Area", self.controller.get_element_reference_face_area, element_id)
            await self.helper.run_test("Get Total Face Area", self.controller.get_total_area_of_all_faces, element_id)
            
            # Test distance and projection calculations
            test_point = [500, 500, 500]
            await self.helper.run_test("Get Closest Point On Element", self.controller.get_closest_point_on_element, element_id, test_point)
            await self.helper.run_test("Project Point To Element", self.controller.project_point_to_element, test_point, element_id)
            
            # Create second element for distance testing
            beam_params2 = self.param_finder.get_beam_parameters()
            beam_params2["p1"] = [2000, 0, 0]  # Offset second beam
            beam_params2["p2"] = [3000, 0, 0]
            
            result2 = await element_ctrl.create_beam(**beam_params2)
            if result2.get("status") == "success":
                element_id2 = result2.get("element_id")
                
                # Test distance between elements
                await self.helper.run_test("Get Minimum Distance Between Elements", 
                                         self.controller.get_minimum_distance_between_elements, 
                                         element_id, element_id2)
                
                # Test center of gravity for multiple elements
                await self.helper.run_test("Get Center of Gravity for List", 
                                         self.controller.get_center_of_gravity_for_list, 
                                         [element_id, element_id2])
                
                # Test calculate center of mass
                await self.helper.run_test("Calculate Center of Mass", 
                                         self.controller.calculate_center_of_mass, 
                                         [element_id, element_id2], True)
                
                # Test section outline
                section_plane_point = [1500, 0, 0]
                section_plane_normal = [1, 0, 0]
                await self.helper.run_test("Get Section Outline", 
                                         self.controller.get_section_outline, 
                                         element_id, section_plane_point, section_plane_normal)
                
                # Cleanup both elements
                await element_ctrl.delete_elements([element_id, element_id2])
            else:
                # Cleanup first element only
                await element_ctrl.delete_elements([element_id])
        
        return self.helper.test_results
    async def run_calculation_tests(self) -> List[TestResult]:
        """Run additional calculation and analysis tests"""
        self.helper.print_header("GEOMETRY CONTROLLER - CALCULATION TESTS")
        
        # Create test elements for calculations
        from controllers.element_controller import ElementController
        element_ctrl = ElementController()
        
        # Create multiple elements for multi-element calculations
        test_elements = []
        for i in range(3):
            beam_params = self.param_finder.get_beam_parameters()
            beam_params["p1"][0] += i * 1500  # Offset beams
            beam_params["p2"][0] += i * 1500
            
            result = await element_ctrl.create_beam(**beam_params)
            if result.get("status") == "success":
                element_id = result.get("element_id")
                if element_id:
                    test_elements.append(element_id)
        
        if len(test_elements) >= 2:
            # Test 1: Calculate total volume for multiple elements
            await self.helper.run_test(
                "Calculate Total Volume",
                self.controller.calculate_total_volume,
                test_elements
            )
            
            # Test 2: Calculate total weight for multiple elements
            await self.helper.run_test(
                "Calculate Total Weight",
                self.controller.calculate_total_weight,
                test_elements
            )
            
            # Test 3: Get center of gravity for element list
            await self.helper.run_test(
                "Get Center of Gravity for List",
                self.controller.get_center_of_gravity_for_list,
                test_elements
            )
            
            # Test 4: Calculate center of mass with material properties
            await self.helper.run_test(
                "Calculate Center of Mass",
                self.controller.calculate_center_of_mass,
                test_elements,
                True  # include_material_properties
            )
            
            # Test 5: Get minimum distance between elements
            await self.helper.run_test(
                "Get Minimum Distance Between Elements",
                self.controller.get_minimum_distance_between_elements,
                test_elements[0],
                test_elements[1]
            )
        
        # Cleanup test elements
        if test_elements:
            await element_ctrl.delete_elements(test_elements)
        
        return self.helper.test_results
    
    async def run_spatial_analysis_tests(self) -> List[TestResult]:
        """Run advanced spatial analysis and geometric calculations"""
        self.helper.print_header("GEOMETRY CONTROLLER - SPATIAL ANALYSIS")
        
        # Create complex geometry for spatial analysis
        from controllers.element_controller import ElementController
        element_ctrl = ElementController()
        spatial_elements = []
        
        # Create elements at specific positions for spatial testing
        spatial_configs = [
            {"p1": [0, 0, 0], "p2": [1000, 0, 0], "width": 100, "height": 100},  # X-axis beam
            {"p1": [0, 0, 0], "p2": [0, 1000, 0], "width": 100, "height": 100},  # Y-axis beam
            {"p1": [0, 0, 0], "p2": [0, 0, 1000], "width": 100, "height": 100},  # Z-axis beam
            {"p1": [500, 500, 500], "p2": [1500, 1500, 1500], "width": 150, "height": 150}  # Diagonal beam
        ]
        
        for config in spatial_configs:
            result = await element_ctrl.create_beam(**config)
            if result.get("status") == "success":
                element_id = result.get("element_id")
                if element_id:
                    spatial_elements.append(element_id)
        
        if len(spatial_elements) >= 4:
            # Test 1: Advanced geometric queries
            for i, element_id in enumerate(spatial_elements):
                await self.helper.run_test(
                    f"Get Element Facets {i+1}",
                    self.controller.get_element_facets,
                    element_id
                )
                
                await self.helper.run_test(
                    f"Get Reference Face Area {i+1}",
                    self.controller.get_element_reference_face_area,
                    element_id
                )
                
                await self.helper.run_test(
                    f"Get Total Face Area {i+1}",
                    self.controller.get_total_area_of_all_faces,
                    element_id
                )
            
            # Test 2: Spatial relationships
            test_points = [
                [250, 250, 250],  # Near origin
                [750, 750, 750],  # Middle diagonal
                [1250, 1250, 1250],  # Far diagonal
                [0, 500, 1000]  # Off-axis point
            ]
            
            for i, point in enumerate(test_points):
                for j, element_id in enumerate(spatial_elements[:2]):  # Test with first 2 elements
                    await self.helper.run_test(
                        f"Project Point {i+1} to Element {j+1}",
                        self.controller.project_point_to_element,
                        point,
                        element_id
                    )
                    
                    await self.helper.run_test(
                        f"Get Closest Point {i+1} on Element {j+1}",
                        self.controller.get_closest_point_on_element,
                        element_id,
                        point
                    )
            
            # Test 3: Element-to-element spatial analysis
            element_pairs = [
                (spatial_elements[0], spatial_elements[1]),  # X-axis to Y-axis
                (spatial_elements[0], spatial_elements[2]),  # X-axis to Z-axis
                (spatial_elements[1], spatial_elements[2]),  # Y-axis to Z-axis
                (spatial_elements[0], spatial_elements[3])   # X-axis to diagonal
            ]
            
            for i, (elem1, elem2) in enumerate(element_pairs):
                await self.helper.run_test(
                    f"Minimum Distance Pair {i+1}",
                    self.controller.get_minimum_distance_between_elements,
                    elem1,
                    elem2
                )
            
            # Test 4: Section analysis
            section_planes = [
                {"point": [500, 0, 0], "normal": [1, 0, 0], "name": "YZ-Plane Section"},
                {"point": [0, 500, 0], "normal": [0, 1, 0], "name": "XZ-Plane Section"},
                {"point": [0, 0, 500], "normal": [0, 0, 1], "name": "XY-Plane Section"},
                {"point": [500, 500, 500], "normal": [1, 1, 1], "name": "Diagonal Section"}
            ]
            
            for section in section_planes:
                for element_id in spatial_elements[:2]:  # Test with first 2 elements
                    await self.helper.run_test(
                        f"{section['name']} - Element {element_id}",
                        self.controller.get_section_outline,
                        element_id,
                        section["point"],
                        section["normal"]
                    )
            
            # Test 5: Complex spatial calculations
            await self.helper.run_test(
                "Multi-Element Center of Mass",
                self.controller.calculate_center_of_mass,
                spatial_elements,
                True  # include_material_properties
            )
            
            await self.helper.run_test(
                "Multi-Element Total Volume",
                self.controller.calculate_total_volume,
                spatial_elements
            )
            
            await self.helper.run_test(
                "Multi-Element Total Weight",
                self.controller.calculate_total_weight,
                spatial_elements
            )
        
        # Cleanup
        if spatial_elements:
            try:
                await element_ctrl.delete_elements(spatial_elements)
            except:
                pass
        
        return self.helper.test_results
    
    async def run_precision_tests(self) -> List[TestResult]:
        """Test geometric precision and edge cases"""
        self.helper.print_header("GEOMETRY CONTROLLER - PRECISION TESTS")
        
        # Create elements with very precise dimensions
        from controllers.element_controller import ElementController
        element_ctrl = ElementController()
        precision_elements = []
        
        # High precision configurations
        precision_configs = [
            {"p1": [0.001, 0.001, 0.001], "p2": [0.999, 0.999, 0.999], "width": 0.1, "height": 0.1},  # Micro beam
            {"p1": [0, 0, 0], "p2": [10000.123456, 0, 0], "width": 200.789, "height": 150.456},  # High precision
            {"p1": [-5000.5, -3000.3, -1000.1], "p2": [5000.5, 3000.3, 1000.1], "width": 100.05, "height": 100.05}  # Negative coords
        ]
        
        for i, config in enumerate(precision_configs):
            result = await element_ctrl.create_beam(**config)
            if result.get("status") == "success":
                element_id = result.get("element_id")
                if element_id:
                    precision_elements.append(element_id)
                    
                    # Test precision of geometric queries
                    await self.helper.run_test(
                        f"Precision Length {i+1}",
                        self.controller.get_element_length,
                        element_id
                    )
                    
                    await self.helper.run_test(
                        f"Precision Volume {i+1}",
                        self.controller.get_element_volume,
                        element_id
                    )
                    
                    await self.helper.run_test(
                        f"Precision Bounding Box {i+1}",
                        self.controller.get_bounding_box,
                        element_id
                    )
        
        # Test edge cases with extreme coordinates
        extreme_test_points = [
            [0, 0, 0],  # Origin
            [999999.999, 999999.999, 999999.999],  # Very large
            [-999999.999, -999999.999, -999999.999],  # Very negative
            [0.000001, 0.000001, 0.000001]  # Very small
        ]
        
        if precision_elements:
            for i, point in enumerate(extreme_test_points):
                await self.helper.run_test(
                    f"Extreme Point Projection {i+1}",
                    self.controller.project_point_to_element,
                    point,
                    precision_elements[0]
                )
        
        # Cleanup
        if precision_elements:
            try:
                await element_ctrl.delete_elements(precision_elements)
            except:
                pass
        
        return self.helper.test_results
