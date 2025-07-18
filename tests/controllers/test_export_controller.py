"""Test Export Controller"""
import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path: sys.path.insert(0, PROJECT_ROOT)

from controllers.export_controller import CExportController
from tests.helpers.test_helper import TestHelper
from tests.helpers.parameter_finder import ParameterFinder

class TestExportController:
    def __init__(self):
        self.controller = CExportController()
        self.helper = TestHelper()
        self.param_finder = ParameterFinder()
    
    async def run_all_tests(self) -> list:
        self.helper.print_header("EXPORT CONTROLLER TESTS")
        dxf_params = self.param_finder.get_export_parameters("dxf")
        await self.helper.run_test("Export to DXF", self.controller.export_to_dxf, **dxf_params)
        return self.helper.test_results
    
    async def run_quick_tests(self) -> list:
        self.helper.print_header("EXPORT CONTROLLER - QUICK TESTS")
        await self.helper.run_test("Quick Export Test", self._quick_test)
        return self.helper.test_results
    
    async def _quick_test(self): return {"status": "success", "message": "Export controller loaded"}
    def get_summary(self): return self.helper.get_summary()
    def print_summary(self): self.helper.print_summary()
