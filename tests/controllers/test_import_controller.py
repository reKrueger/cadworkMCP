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
        await self.helper.run_test("Import Test Placeholder", self._placeholder_test)
        return self.helper.test_results
    
    async def run_quick_tests(self) -> list:
        self.helper.print_header("IMPORT CONTROLLER - QUICK TESTS")
        await self.helper.run_test("Quick Import Test", self._placeholder_test)
        return self.helper.test_results
    
    async def _placeholder_test(self): return {"status": "success", "message": "Import controller loaded"}
    def get_summary(self): return self.helper.get_summary()
    def print_summary(self): self.helper.print_summary()
