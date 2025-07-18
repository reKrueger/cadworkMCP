"""Test Utility Controller"""
import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)

from controllers.utility_controller import CUtilityController
from tests.helpers.test_helper import TestHelper

class TestUtilityController:
    def __init__(self):
        self.controller = CUtilityController()
        self.helper = TestHelper()
    
    async def run_all_tests(self) -> list:
        self.helper.print_header("UTILITY CONTROLLER TESTS")
        
        # Original tests
        await self.helper.run_test("Get Project Data", self.controller.get_project_data)
        await self.helper.run_test("Get Cadwork Version", self.controller.get_cadwork_version_info)
        
        # 5 new extended tests
        await self.helper.run_test("Get 3D File Path", self._test_get_3d_file_path)
        await self.helper.run_test("Display Refresh Control", self._test_display_refresh_control)
        await self.helper.run_test("Print Error Message", self._test_print_error)
        await self.helper.run_test("Print Warning Message", self._test_print_warning)
        await self.helper.run_test("System Information", self._test_system_information)
        
        return self.helper.test_results
    
    async def _test_get_3d_file_path(self):
        """Test getting current 3D file path"""
        result = await self.controller.get_3d_file_path()
        return result
    
    async def _test_display_refresh_control(self):
        """Test disabling and enabling display refresh"""
        # Disable auto refresh
        disable_result = await self.controller.disable_auto_display_refresh()
        if disable_result.get("status") != "success":
            return {"status": "error", "message": "Failed to disable auto refresh"}
        
        # Re-enable auto refresh
        enable_result = await self.controller.enable_auto_display_refresh()
        if enable_result.get("status") != "success":
            return {"status": "error", "message": "Failed to enable auto refresh"}
        
        return {"status": "success", "message": "Display refresh control tested successfully"}
    
    async def _test_print_error(self):
        """Test printing error message to Cadwork"""
        test_message = "Test Error Message from MCP Test Suite"
        result = await self.controller.print_error(test_message)
        return result
    
    async def _test_print_warning(self):
        """Test printing warning message to Cadwork"""
        test_message = "Test Warning Message from MCP Test Suite"
        result = await self.controller.print_warning(test_message)
        return result
    
    async def _test_system_information(self):
        """Test getting comprehensive system information"""
        # Get multiple system info pieces
        version_result = await self.controller.get_cadwork_version_info()
        project_result = await self.controller.get_project_data()
        file_result = await self.controller.get_3d_file_path()
        
        # Count successful calls
        success_count = 0
        if version_result.get("status") == "success":
            success_count += 1
        if project_result.get("status") == "success":
            success_count += 1
        if file_result.get("status") == "success":
            success_count += 1
        
        return {
            "status": "success" if success_count >= 2 else "partial",
            "message": f"Retrieved {success_count}/3 system information items",
            "details": {
                "version_info": version_result,
                "project_data": project_result,
                "file_path": file_result
            }
        }
    
    async def run_quick_tests(self) -> list:
        self.helper.print_header("UTILITY CONTROLLER - QUICK TESTS")
        await self.helper.run_test("Quick Version Check", self.controller.get_cadwork_version_info)
        return self.helper.test_results
    
    def get_summary(self): return self.helper.get_summary()
    def print_summary(self): self.helper.print_summary()
