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
