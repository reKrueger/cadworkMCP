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
