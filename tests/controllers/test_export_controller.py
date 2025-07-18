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
    
    async def run_extended_tests(self) -> list:
        """Run extended export controller tests with 5 new export formats"""
        self.helper.print_header("EXPORT CONTROLLER EXTENDED TESTS")
        
        # Test 1: Export to BTL
        await self.helper.run_test(
            "Export to BTL",
            self.controller.export_to_btl,
            None,  # element_ids
            None,  # file_path  
            "10.5", # btl_version
            True,   # include_processing
            True    # include_geometry
        )
        
        # Test 2: Export to IFC
        await self.helper.run_test(
            "Export to IFC",
            self.controller.export_to_ifc,
            None,      # element_ids
            None,      # file_path
            "IFC4",    # ifc_version
            "project", # coordinate_system
            True,      # include_geometry
            True,      # include_materials
            True       # include_properties
        )
        
        # Test 3: Export to STEP
        await self.helper.run_test(
            "Export to STEP", 
            self.controller.export_to_step,
            None,     # element_ids
            None,     # file_path
            "AP214",  # step_version
            "mm",     # units
            0.01      # precision
        )
        
        # Test 4: Export to STL
        await self.helper.run_test(
            "Export to STL",
            self.controller.export_to_stl,
            None,      # element_ids
            None,      # file_path
            "binary",  # stl_format
            "medium",  # mesh_quality
            "mm",      # units
            True       # merge_elements
        )
        
        # Test 5: Export Workshop Drawings
        await self.helper.run_test(
            "Export Workshop Drawings",
            self.controller.export_workshop_drawings,
            None,    # element_ids
            "pdf",   # drawing_format
            True,    # include_dimensions
            True,    # include_processing
            "1:10",  # scale
            "A3"     # sheet_size
        )
        
        return self.helper.test_results
    
    async def run_quick_tests(self) -> list:
        self.helper.print_header("EXPORT CONTROLLER - QUICK TESTS")
        await self.helper.run_test("Quick Export Test", self._quick_test)
        return self.helper.test_results
    
    async def _quick_test(self): return {"status": "success", "message": "Export controller loaded"}
    def get_summary(self): return self.helper.get_summary()
    def print_summary(self): self.helper.print_summary()
