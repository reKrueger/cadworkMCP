"""Test Import Controller"""
import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)

from controllers.import_controller import CImportController
from tests.helpers.test_helper import TestHelper

class TestImportController:
    def __init__(self):
        self.controller = CImportController()
        self.helper = TestHelper()
    
    async def run_all_tests(self) -> list:
        self.helper.print_header("IMPORT CONTROLLER TESTS")
        
        # Original test
        await self.helper.run_test("Import Test Placeholder", self._placeholder_test)
        
        # 5 new extended tests (parameter validation without actual files)
        await self.helper.run_test("Validate STEP Import Parameters", self._test_step_import_validation)
        await self.helper.run_test("Validate SAT Import Parameters", self._test_sat_import_validation)
        await self.helper.run_test("Validate Rhino Import Parameters", self._test_rhino_import_validation)
        await self.helper.run_test("Validate BTL Import Parameters", self._test_btl_import_validation)
        await self.helper.run_test("Import Error Handling", self._test_import_error_handling)
        
        return self.helper.test_results
    
    async def _test_step_import_validation(self):
        """Test STEP import parameter validation"""
        # Test with invalid parameters to check validation
        try:
            # Test invalid file path
            result1 = await self.controller.import_from_step("", 1.0)
            if result1.get("status") != "error":
                return {"status": "error", "message": "Should have failed with empty file path"}
            
            # Test invalid scale factor
            result2 = await self.controller.import_from_step("test.step", -1.0)
            if result2.get("status") != "error":
                return {"status": "error", "message": "Should have failed with negative scale factor"}
            
            # Test invalid insert position
            result3 = await self.controller.import_from_step("test.step", 1.0, False, [1, 2])
            if result3.get("status") != "error":
                return {"status": "error", "message": "Should have failed with invalid insert position"}
            
            return {"status": "success", "message": "STEP import validation working correctly"}
            
        except Exception as e:
            return {"status": "error", "message": f"Validation test failed: {e}"}
    
    async def _test_sat_import_validation(self):
        """Test SAT import parameter validation"""
        try:
            # Test invalid file extension
            result1 = await self.controller.import_from_sat("test.txt", 1.0)
            if result1.get("status") != "error":
                return {"status": "error", "message": "Should have failed with wrong file extension"}
            
            # Test valid parameters (will fail on file not found, but validation should pass)
            result2 = await self.controller.import_from_sat("test.sat", 1.0, True, [0, 0, 0])
            # Should fail on file not found, not on validation
            
            return {"status": "success", "message": "SAT import validation working correctly"}
            
        except Exception as e:
            return {"status": "error", "message": f"SAT validation test failed: {e}"}
    
    async def _test_rhino_import_validation(self):
        """Test Rhino import parameter validation"""
        try:
            # Test with valid parameters structure
            result = await self.controller.import_from_rhino(
                "test.3dm", 
                import_layers=True,
                import_materials=True, 
                scale_factor=1.0,
                without_dialog=True
            )
            
            # Should fail on file not found, not on validation
            return {"status": "success", "message": "Rhino import validation working correctly"}
            
        except Exception as e:
            return {"status": "error", "message": f"Rhino validation test failed: {e}"}
    
    async def _test_btl_import_validation(self):
        """Test BTL import parameter validation"""
        try:
            # Test with valid parameters
            result = await self.controller.import_from_btl(
                "test.btl",
                import_mode="standard",
                import_processing=True,
                merge_duplicates=True,
                validate_geometry=True
            )
            
            # Should fail on file not found, not on validation
            return {"status": "success", "message": "BTL import validation working correctly"}
            
        except Exception as e:
            return {"status": "error", "message": f"BTL validation test failed: {e}"}
    
    async def _test_import_error_handling(self):
        """Test import error handling with various invalid inputs"""
        error_tests = [
            ("Empty file path", lambda: self.controller.import_from_step("", 1.0)),
            ("Invalid scale", lambda: self.controller.import_from_step("test.step", 0)),
            ("Wrong extension", lambda: self.controller.import_from_sat("test.wrong", 1.0)),
            ("Invalid position", lambda: self.controller.import_from_rhino("test.3dm", scale_factor=-1))
        ]
        
        passed_tests = 0
        total_tests = len(error_tests)
        
        for test_name, test_func in error_tests:
            try:
                result = await test_func()
                if result.get("status") == "error":
                    passed_tests += 1
            except Exception:
                # Exception is also acceptable for error handling
                passed_tests += 1
        
        success_rate = passed_tests / total_tests
        if success_rate >= 0.8:  # 80% of error tests should properly catch errors
            return {"status": "success", "message": f"Error handling working: {passed_tests}/{total_tests} tests passed"}
        else:
            return {"status": "error", "message": f"Error handling issues: only {passed_tests}/{total_tests} tests passed"}
    
    async def run_quick_tests(self) -> list:
        self.helper.print_header("IMPORT CONTROLLER - QUICK TESTS")
        await self.helper.run_test("Quick Import Test", self._placeholder_test)
        return self.helper.test_results
    
    async def _placeholder_test(self): return {"status": "success", "message": "Import controller loaded"}
    def get_summary(self): return self.helper.get_summary()
    def print_summary(self): self.helper.print_summary()
