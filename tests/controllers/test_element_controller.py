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
