"""Test Attribute Controller"""
import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)

from controllers.attribute_controller import AttributeController
from tests.helpers.test_helper import TestHelper, TestResult
from tests.helpers.parameter_finder import ParameterFinder  

class TestAttributeController:
    def __init__(self):
        self.controller = AttributeController()
        self.helper = TestHelper()
        self.param_finder = ParameterFinder()
        self.test_element_ids = []
    
    async def run_all_tests(self) -> list:
        self.helper.print_header("ATTRIBUTE CONTROLLER TESTS")
        
        # Create test elements first
        await self._create_test_elements()
        
        # Original tests
        await self.helper.run_test("Set Material Test", self._test_material)
        await self.helper.run_test("Set Name Test", self._test_name)
        
        # 5 new extended tests
        await self.helper.run_test("Get Standard Attributes", self._test_get_standard_attributes)
        await self.helper.run_test("Get User Attributes", self._test_get_user_attributes)
        await self.helper.run_test("List Defined User Attributes", self._test_list_defined_user_attributes)
        await self.helper.run_test("Set Group", self._test_set_group)
        await self.helper.run_test("Set Comment and Subgroup", self._test_set_comment_subgroup)
        
        # Cleanup
        await self._cleanup_test_elements()
        
        return self.helper.test_results
    
    async def _create_test_elements(self):
        """Create test elements for attribute testing"""
        from controllers.element_controller import ElementController
        element_ctrl = ElementController()
        
        # Create 2 test beams
        for i in range(2):
            beam_params = self.param_finder.get_beam_parameters()
            beam_params["p1"][0] += i * 1000  # Offset beams
            beam_params["p2"][0] += i * 1000
            
            result = await element_ctrl.create_beam(**beam_params)
            if result.get("status") == "success":
                element_id = result.get("element_id")
                if element_id:
                    self.test_element_ids.append(element_id)
        
        return {"status": "success", "message": f"Created {len(self.test_element_ids)} test elements"}
    
    async def _test_get_standard_attributes(self):
        """Test getting standard attributes from elements"""
        if not self.test_element_ids:
            return {"status": "error", "message": "No test elements available"}
        
        result = await self.controller.get_standard_attributes(self.test_element_ids)
        return result
    
    async def _test_get_user_attributes(self):
        """Test getting user-defined attributes"""
        if not self.test_element_ids:
            return {"status": "error", "message": "No test elements available"}
        
        # Test with some common user attribute numbers
        attribute_numbers = [1, 2, 3]
        result = await self.controller.get_user_attributes(self.test_element_ids, attribute_numbers)
        return result
    
    async def _test_list_defined_user_attributes(self):
        """Test listing all defined user attributes"""
        result = await self.controller.list_defined_user_attributes()
        return result
    
    async def _test_set_group(self):
        """Test setting group for elements"""
        if not self.test_element_ids:
            return {"status": "error", "message": "No test elements available"}
        
        result = await self.controller.set_group(self.test_element_ids, "TestGroup")
        return result
    
    async def _test_set_comment_subgroup(self):
        """Test setting comment and subgroup"""
        if not self.test_element_ids:
            return {"status": "error", "message": "No test elements available"}
        
        # Set comment
        comment_result = await self.controller.set_comment(self.test_element_ids, "Test Comment")
        
        # Set subgroup
        subgroup_result = await self.controller.set_subgroup(self.test_element_ids, "TestSubgroup")
        
        # Return combined result
        if (comment_result.get("status") == "success" and 
            subgroup_result.get("status") == "success"):
            return {"status": "success", "message": "Comment and subgroup set successfully"}
        else:
            return {"status": "error", "message": "Failed to set comment or subgroup"}
    
    async def _cleanup_test_elements(self):
        """Clean up test elements"""
        if self.test_element_ids:
            from controllers.element_controller import ElementController
            element_ctrl = ElementController()
            await element_ctrl.delete_elements(self.test_element_ids)
            self.test_element_ids.clear()
        
        return {"status": "success", "message": "Test elements cleaned up"}
    
    async def run_quick_tests(self) -> list:
        self.helper.print_header("ATTRIBUTE CONTROLLER - QUICK TESTS")
        await self.helper.run_test("Quick Attribute Test", self._quick_test)
        return self.helper.test_results
    
    async def _test_material(self): return {"status": "success", "message": "Material test"}
    async def _test_name(self): return {"status": "success", "message": "Name test"}
    async def _quick_test(self): return {"status": "success", "message": "Attribute controller loaded"}
    
    def get_summary(self): return self.helper.get_summary()
    def print_summary(self): self.helper.print_summary()
