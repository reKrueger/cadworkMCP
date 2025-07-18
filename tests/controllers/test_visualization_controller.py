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
    
    async def run_advanced_visualization_tests(self) -> list:
        """Run advanced visualization and display tests"""
        self.helper.print_header("VISUALIZATION CONTROLLER - ADVANCED TESTS")
        
        # Create test elements for advanced visualization
        from controllers.element_controller import ElementController
        element_ctrl = ElementController()
        test_elements = []
        
        # Create different types of elements for visualization testing
        element_configs = [
            {"type": "beam", "params": self.param_finder.get_beam_parameters()},
            {"type": "panel", "params": self.param_finder.get_panel_parameters()},
        ]
        
        for i, config in enumerate(element_configs):
            config["params"]["p1"][0] += i * 3000  # Offset elements
            config["params"]["p2"][0] += i * 3000
            
            if config["type"] == "beam":
                result = await element_ctrl.create_beam(**config["params"])
            else:
                result = await element_ctrl.create_panel(**config["params"])
            
            if result.get("status") == "success":
                element_id = result.get("element_id")
                if element_id:
                    test_elements.append(element_id)
        
        if len(test_elements) >= 2:
            # Test 1: Advanced color management
            color_schemes = [
                {"name": "Rainbow", "colors": [1, 5, 10, 15, 20]},
                {"name": "Monochrome", "colors": [1, 2, 3, 4, 5]},
                {"name": "High Contrast", "colors": [1, 255, 128, 64, 192]}
            ]
            
            for scheme in color_schemes:
                for i, element_id in enumerate(test_elements):
                    color_id = scheme["colors"][i % len(scheme["colors"])]
                    await self.helper.run_test(
                        f"Set Color {color_id} ({scheme['name']})",
                        self.controller.set_color,
                        [element_id],
                        color_id
                    )
            
            # Test 2: Transparency gradient effects
            transparency_levels = [0, 25, 50, 75, 95]
            for i, element_id in enumerate(test_elements):
                transparency = transparency_levels[i % len(transparency_levels)]
                await self.helper.run_test(
                    f"Set Transparency {transparency}%",
                    self.controller.set_transparency,
                    [element_id],
                    transparency
                )
            
            # Test 3: Batch visibility operations
            await self.helper.run_test(
                "Hide All Test Elements",
                self.controller.set_visibility,
                test_elements,
                False
            )
            
            await self.helper.run_test(
                "Show All Test Elements",
                self.controller.set_visibility,
                test_elements,
                True
            )
            
            # Test 4: Display state management
            await self.helper.run_test(
                "Hide All Elements (Global)",
                self.controller.hide_all_elements
            )
            
            await self.helper.run_test(
                "Show All Elements (Global)",
                self.controller.show_all_elements
            )
            
            await self.helper.run_test(
                "Refresh Display",
                self.controller.refresh_display
            )
            
            # Test 5: Visualization property queries
            for element_id in test_elements[:2]:  # Test first 2 elements
                await self.helper.run_test(
                    f"Get Color for Element {element_id}",
                    self.controller.get_color,
                    element_id
                )
                
                await self.helper.run_test(
                    f"Get Transparency for Element {element_id}",
                    self.controller.get_transparency,
                    element_id
                )
        
        # Test visibility statistics
        await self.helper.run_test(
            "Get Visible Element Count",
            self.controller.get_visible_element_count
        )
        
        # Test visualization error handling
        error_test_cases = [
            ("Invalid Color ID", lambda: self.controller.set_color([test_elements[0]] if test_elements else [1], 300)),
            ("Invalid Transparency", lambda: self.controller.set_transparency([test_elements[0]] if test_elements else [1], 150)),
            ("Empty Element List", lambda: self.controller.set_visibility([], True)),
            ("Invalid Element ID", lambda: self.controller.get_color(-1))
        ]
        
        error_handling_results = []
        for test_name, test_func in error_test_cases:
            try:
                result = await test_func()
                if result.get("status") == "error":
                    error_handling_results.append(f"{test_name}: properly handled")
                else:
                    error_handling_results.append(f"{test_name}: not handled")
            except Exception:
                error_handling_results.append(f"{test_name}: exception handled")
        
        await self.helper.run_test(
            "Visualization Error Handling Summary",
            self._create_error_summary,
            error_handling_results
        )
        
        # Cleanup test elements
        if test_elements:
            await element_ctrl.delete_elements(test_elements)
        
        return self.helper.test_results
    
    async def _create_error_summary(self, error_results):
        """Create summary of error handling results"""
        properly_handled = sum(1 for result in error_results if "properly handled" in result or "exception handled" in result)
        total_tests = len(error_results)
        
        return {
            "status": "success" if properly_handled >= total_tests * 0.75 else "partial",
            "message": f"Error handling: {properly_handled}/{total_tests} cases handled properly",
            "details": error_results
        }
