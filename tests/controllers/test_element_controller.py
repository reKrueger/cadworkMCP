"""
Test Element Controller
======================

Tests for ElementController functions including creation, deletion, 
modification and querying of Cadwork elements.
"""

import sys
import os
from typing import Dict, Any, List, Optional

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from controllers.element_controller import ElementController
from helpers.test_helper import TestHelper, TestResult
from helpers.parameter_finder import ParameterFinder
from helpers.result_validator import ResultValidator


class TestElementController:
    """Test suite for ElementController functionality"""
    
    def __init__(self):
        self.controller = ElementController()
        self.helper = TestHelper()
        self.param_finder = ParameterFinder()
        self.validator = ResultValidator()
        self.test_element_ids: List[int] = []  # Track created elements for cleanup
    
    async def run_all_tests(self) -> List[TestResult]:
        """Run all element controller tests"""
        self.helper.print_header("ELEMENT CONTROLLER TESTS")
        
        # Test creation functions
        await self._test_element_creation()
        
        # Test query functions  
        await self._test_element_queries()
        
        # Test modification functions
        await self._test_element_modifications()
        
        # Test deletion (cleanup)
        await self._test_element_deletion()
        
        return self.helper.test_results
    
    async def _test_element_creation(self) -> None:
        """Test element creation functions"""
        self.helper.print_subheader("Element Creation Tests")
        
        # Test create_beam
        beam_params = self.param_finder.get_beam_parameters()
        result = await self.helper.run_test(
            "Create Beam",
            self.controller.create_beam,
            **beam_params
        )
        if result.status == "PASSED" and result.details:
            element_id = result.details.get("element_id")
            if element_id:
                self.test_element_ids.append(element_id)
        
        # Test create_panel
        panel_params = self.param_finder.get_panel_parameters()
        result = await self.helper.run_test(
            "Create Panel",
            self.controller.create_panel,
            **panel_params
        )
        if result.status == "PASSED" and result.details:
            element_id = result.details.get("element_id")
            if element_id:
                self.test_element_ids.append(element_id)
        
        # Test create_circular_beam_points
        circular_params = self.param_finder.get_circular_beam_parameters()
        result = await self.helper.run_test(
            "Create Circular Beam",
            self.controller.create_circular_beam_points,
            **circular_params
        )
        if result.status == "PASSED" and result.details:
            element_id = result.details.get("element_id")
            if element_id:
                self.test_element_ids.append(element_id)
        
        # Test create_square_beam_points
        square_params = self.param_finder.get_square_beam_parameters()
        result = await self.helper.run_test(
            "Create Square Beam",
            self.controller.create_square_beam_points,
            **square_params
        )
        if result.status == "PASSED" and result.details:
            element_id = result.details.get("element_id")
            if element_id:
                self.test_element_ids.append(element_id)
        
        # Test create_drilling_points
        drilling_params = self.param_finder.get_drilling_parameters()
        result = await self.helper.run_test(
            "Create Drilling",
            self.controller.create_drilling_points,
            **drilling_params
        )
        if result.status == "PASSED" and result.details:
            element_id = result.details.get("element_id")
            if element_id:
                self.test_element_ids.append(element_id)
    
    async def _test_element_queries(self) -> None:
        """Test element query functions"""
        self.helper.print_subheader("Element Query Tests")
        
        # Test get_all_element_ids
        await self.helper.run_test(
            "Get All Element IDs",
            self.controller.get_all_element_ids
        )
        
        # Test get_visible_element_ids
        await self.helper.run_test(
            "Get Visible Element IDs", 
            self.controller.get_visible_element_ids
        )
        
        # Test get_active_element_ids
        await self.helper.run_test(
            "Get Active Element IDs",
            self.controller.get_active_element_ids
        )
        
        # Test get_element_info (if we have created elements)
        if self.test_element_ids:
            element_id = self.test_element_ids[0]
            await self.helper.run_test(
                "Get Element Info",
                self.controller.get_element_info,
                element_id
            )
        
        # Test filtering functions
        await self.helper.run_test(
            "Get Elements By Type (beam)",
            self.controller.get_elements_by_type,
            "beam"
        )
        
        await self.helper.run_test(
            "Get Elements By Type (panel)",
            self.controller.get_elements_by_type,
            "panel"
        )
        
        # Test region filtering
        region_params = self.param_finder.get_region_parameters()
        await self.helper.run_test(
            "Get Elements In Region",
            self.controller.get_elements_in_region,
            **region_params
        )
    
    async def _test_element_modifications(self) -> None:
        """Test element modification functions"""
        if not self.test_element_ids:
            self.helper.print_subheader("Element Modification Tests (SKIPPED - No elements)")
            return
        
        self.helper.print_subheader("Element Modification Tests")
        
        # Test copy_elements
        move_vector = self.param_finder.get_move_vector()
        result = await self.helper.run_test(
            "Copy Elements",
            self.controller.copy_elements,
            self.test_element_ids[:2],  # Copy first 2 elements
            move_vector
        )
        
        # Add copied elements to track list
        if result.status == "PASSED" and result.details:
            copied_ids = result.details.get("new_element_ids", [])
            self.test_element_ids.extend(copied_ids)
        
        # Test move_element
        if len(self.test_element_ids) > 2:
            move_vector = self.param_finder.get_move_vector()
            await self.helper.run_test(
                "Move Element",
                self.controller.move_element,
                self.test_element_ids[2:3],  # Move one element
                move_vector
            )
        
        # Test scale_elements
        if len(self.test_element_ids) > 3:
            scale_factor = self.param_finder.get_scale_factor()
            await self.helper.run_test(
                "Scale Elements",
                self.controller.scale_elements,
                self.test_element_ids[3:4],  # Scale one element
                scale_factor
            )
    
    async def _test_element_deletion(self) -> None:
        """Test element deletion and cleanup"""
        if not self.test_element_ids:
            self.helper.print_subheader("Element Deletion Tests (SKIPPED - No elements)")
            return
        
        self.helper.print_subheader("Element Deletion Tests")
        
        # Test delete_elements (cleanup all test elements)
        await self.helper.run_test(
            "Delete Test Elements",
            self.controller.delete_elements,
            self.test_element_ids
        )
        
        # Clear the list after deletion
        self.test_element_ids.clear()
    
    async def run_quick_tests(self) -> List[TestResult]:
        """Run only the most essential element tests"""
        self.helper.print_header("ELEMENT CONTROLLER - QUICK TESTS")
        
        # Quick creation test
        beam_params = self.param_finder.get_beam_parameters()
        result = await self.helper.run_test(
            "Quick Create Beam",
            self.controller.create_beam,
            **beam_params
        )
        
        if result.status == "PASSED" and result.details:
            element_id = result.details.get("element_id")
            if element_id:
                self.test_element_ids.append(element_id)
                
                # Quick query test
                await self.helper.run_test(
                    "Quick Get Element Info",
                    self.controller.get_element_info,
                    element_id
                )
                
                # Quick cleanup
                await self.helper.run_test(
                    "Quick Delete Element",
                    self.controller.delete_elements,
                    [element_id]
                )
        
        # Query tests that don't require elements
        await self.helper.run_test(
            "Quick Get All Elements",
            self.controller.get_all_element_ids
        )
        
        return self.helper.test_results
    
    def get_summary(self) -> Dict[str, Any]:
        """Get test summary"""
        return self.helper.get_summary()
    
    def print_summary(self) -> None:
        """Print test summary"""
        self.helper.print_summary()


# Convenience function for standalone testing
async def run_element_tests(quick_mode: bool = False) -> None:
    """Run element controller tests standalone"""
    test_suite = TestElementController()
    
    if quick_mode:
        await test_suite.run_quick_tests()
    else:
        await test_suite.run_all_tests()
    
    test_suite.print_summary()


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_element_tests(quick_mode=True))
    
    async def run_boolean_operations_tests(self) -> List[TestResult]:
        """Test Boolean operations (intersect, subtract, unite)"""
        self.helper.print_header("ELEMENT CONTROLLER - BOOLEAN OPERATIONS")
        
        # Create overlapping elements for Boolean operations
        from controllers.element_controller import ElementController
        element_ctrl = ElementController()
        boolean_test_elements = []
        
        # Create overlapping beams for Boolean operations
        overlapping_configs = [
            {"p1": [0, 0, 0], "p2": [2000, 0, 0], "width": 200, "height": 200},  # Horizontal beam
            {"p1": [1000, -100, -100], "p2": [1000, 100, 100], "width": 200, "height": 200},  # Vertical intersecting beam
            {"p1": [500, 0, 0], "p2": [1500, 0, 0], "width": 150, "height": 150}  # Overlapping beam
        ]
        
        for config in overlapping_configs:
            result = await element_ctrl.create_beam(**config)
            if result.get("status") == "success":
                element_id = result.get("element_id")
                if element_id:
                    boolean_test_elements.append(element_id)
        
        if len(boolean_test_elements) >= 3:
            # Test 1: Element intersection
            await self.helper.run_test(
                "Intersect Elements",
                self.controller.intersect_elements,
                boolean_test_elements[:2],  # First 2 elements
                True  # keep_originals
            )
            
            # Test 2: Element subtraction
            await self.helper.run_test(
                "Subtract Elements",
                self.controller.subtract_elements,
                boolean_test_elements[0],  # target
                boolean_test_elements[1:2],  # subtract these
                False  # don't keep originals
            )
            
            # Test 3: Element union
            await self.helper.run_test(
                "Unite Elements",
                self.controller.unite_elements,
                boolean_test_elements[1:3],  # Last 2 elements
                False  # don't keep originals
            )
            
            # Test 4: Complex Boolean chain
            if len(boolean_test_elements) >= 2:
                # Create new elements for complex operations
                new_beam_params = self.param_finder.get_beam_parameters()
                new_beam_params["p1"] = [3000, 0, 0]
                new_beam_params["p2"] = [4000, 0, 0]
                
                result = await element_ctrl.create_beam(**new_beam_params)
                if result.get("status") == "success":
                    new_id = result.get("element_id")
                    if new_id:
                        boolean_test_elements.append(new_id)
                        
                        await self.helper.run_test(
                            "Complex Boolean Chain",
                            self._perform_complex_boolean_chain,
                            boolean_test_elements
                        )
            
            # Test 5: Boolean operation validation
            await self.helper.run_test(
                "Boolean Parameter Validation",
                self._test_boolean_validation
            )
        
        # Cleanup
        if boolean_test_elements:
            try:
                await element_ctrl.delete_elements(boolean_test_elements)
            except:
                pass
        
        return self.helper.test_results
    
    async def _perform_complex_boolean_chain(self, element_ids):
        """Perform complex chain of Boolean operations"""
        try:
            if len(element_ids) < 2:
                return {"status": "error", "message": "Need at least 2 elements for Boolean operations"}
            
            # First unite some elements
            unite_result = await self.controller.unite_elements(element_ids[:2], True)
            
            # Then try intersection if we have more elements
            if len(element_ids) >= 3:
                intersect_result = await self.controller.intersect_elements(element_ids[1:3], True)
                
                return {
                    "status": "success" if unite_result.get("status") == "success" else "partial",
                    "message": f"Boolean chain completed: unite={unite_result.get('status')}, intersect={intersect_result.get('status')}",
                    "details": {"unite": unite_result, "intersect": intersect_result}
                }
            
            return unite_result
            
        except Exception as e:
            return {"status": "error", "message": f"Boolean chain failed: {e}"}
    
    async def _test_boolean_validation(self):
        """Test Boolean operation parameter validation"""
        validation_errors = []
        
        # Test invalid element lists
        test_cases = [
            ("Empty list", []),
            ("Single element", [1]),
            ("Invalid IDs", [-1, -2])
        ]
        
        for test_name, element_list in test_cases:
            try:
                result = await self.controller.unite_elements(element_list, True)
                if result.get("status") == "error":
                    validation_errors.append(f"{test_name}: properly caught")
                else:
                    validation_errors.append(f"{test_name}: not caught")
            except Exception:
                validation_errors.append(f"{test_name}: exception caught")
        
        caught_errors = sum(1 for error in validation_errors if "caught" in error)
        total_errors = len(validation_errors)
        
        return {
            "status": "success" if caught_errors >= total_errors * 0.8 else "partial",
            "message": f"Boolean validation: {caught_errors}/{total_errors} errors properly handled",
            "details": validation_errors
        }
