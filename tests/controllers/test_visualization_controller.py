"""Test Visualization Controller"""
import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)

from controllers.visualization_controller import CVisualizationController
from tests.helpers.test_helper import TestHelper, TestResult
from tests.helpers.parameter_finder import ParameterFinder

class TestVisualizationController:
    def __init__(self):
        self.controller = CVisualizationController()
        self.helper = TestHelper()
        self.param_finder = ParameterFinder()
    
    async def run_all_tests(self) -> list:
        self.helper.print_header("VISUALIZATION CONTROLLER TESTS")
        await self.helper.run_test("Show All Elements", self.controller.show_all_elements)
        await self.helper.run_test("Get Visible Count", self.controller.get_visible_element_count)
        await self.helper.run_test("Refresh Display", self.controller.refresh_display)
        return self.helper.test_results
    
    async def run_extended_tests(self) -> list:
        """Run extended visualization controller tests with element creation"""
        self.helper.print_header("VISUALIZATION CONTROLLER EXTENDED TESTS")
        
        # Create test elements first
        from controllers.element_controller import ElementController
        element_ctrl = ElementController()
        test_element_ids = []
        
        # Create 3 test beams
        for i in range(3):
            beam_params = self.param_finder.get_beam_parameters()
            beam_params["p1"][0] += i * 2000  # Offset each beam
            beam_params["p2"][0] += i * 2000
            
            result = await element_ctrl.create_beam(**beam_params)
            if result.get("status") == "success":
                element_id = result.get("element_id")
                if element_id:
                    test_element_ids.append(element_id)
        
        if len(test_element_ids) >= 3:
            # Test 1: Set different colors for elements
            colors = [5, 10, 15]  # Different color IDs
            for i, element_id in enumerate(test_element_ids):
                await self.helper.run_test(
                    f"Set Color {colors[i]} for Element {i+1}",
                    self.controller.set_color,
                    [element_id],
                    colors[i]
                )
            
            # Test 2: Set transparency for elements
            transparencies = [25, 50, 75]  # Different transparency levels
            for i, element_id in enumerate(test_element_ids):
                await self.helper.run_test(
                    f"Set Transparency {transparencies[i]}% for Element {i+1}",
                    self.controller.set_transparency,
                    [element_id],
                    transparencies[i]
                )
            
            # Test 3: Get color of an element
            await self.helper.run_test(
                "Get Element Color",
                self.controller.get_color,
                test_element_ids[0]
            )
            
            # Test 4: Get transparency of an element
            await self.helper.run_test(
                "Get Element Transparency", 
                self.controller.get_transparency,
                test_element_ids[1]
            )
            
            # Test 5: Hide and show specific elements
            await self.helper.run_test(
                "Hide Elements",
                self.controller.set_visibility,
                test_element_ids[:2],  # Hide first 2 elements
                False
            )
            
            await self.helper.run_test(
                "Show Hidden Elements",
                self.controller.set_visibility,
                test_element_ids[:2],  # Show first 2 elements again
                True
            )
            
            # Cleanup test elements
            await element_ctrl.delete_elements(test_element_ids)
        else:
            # Run basic tests if element creation failed
            await self.helper.run_test("Hide All Elements", self.controller.hide_all_elements)
            await self.helper.run_test("Show All Elements", self.controller.show_all_elements)
            await self.helper.run_test("Get Visible Count", self.controller.get_visible_element_count)
            await self.helper.run_test("Refresh Display", self.controller.refresh_display)
        
        return self.helper.test_results
    
    async def run_quick_tests(self) -> list:
        self.helper.print_header("VISUALIZATION CONTROLLER - QUICK TESTS")
        await self.helper.run_test("Quick Show All", self.controller.show_all_elements)
        return self.helper.test_results
    
    def get_summary(self): return self.helper.get_summary()
    def print_summary(self): self.helper.print_summary()
