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
    
    async def run_advanced_3d_export_tests(self) -> list:
        """Run advanced 3D export tests with multiple formats and settings"""
        self.helper.print_header("EXPORT CONTROLLER - ADVANCED 3D EXPORTS")
        
        # Test 1: 3D Modeling exports (OBJ, PLY, FBX)
        modeling_formats = [
            {
                "name": "OBJ for Blender/Maya",
                "func": self.controller.export_to_obj,
                "params": {
                    "element_ids": None,
                    "file_path": None,
                    "include_materials": True,
                    "include_normals": True,
                    "include_textures": True,
                    "mesh_resolution": "high"
                }
            },
            {
                "name": "PLY for Point Clouds",
                "func": self.controller.export_to_ply,
                "params": {
                    "element_ids": None,
                    "file_path": None,
                    "ply_format": "binary",
                    "include_colors": True,
                    "include_normals": True,
                    "coordinate_precision": 6
                }
            },
            {
                "name": "FBX for Animation",
                "func": self.controller.export_to_fbx,
                "params": {
                    "element_ids": None,
                    "file_path": None,
                    "fbx_format": "binary",
                    "fbx_version": "2020",
                    "include_materials": True,
                    "include_textures": True,
                    "include_animations": False
                }
            }
        ]
        
        for format_config in modeling_formats:
            await self.helper.run_test(
                format_config["name"],
                format_config["func"],
                **format_config["params"]
            )
        
        # Test 2: Web and VR exports (glTF, X3D, WebGL)
        web_formats = [
            {
                "name": "glTF for Web3D",
                "func": self.controller.export_to_gltf,
                "params": {
                    "element_ids": None,
                    "file_path": None,
                    "gltf_format": "glb",
                    "include_materials": True,
                    "include_animations": False,
                    "texture_resolution": 1024,
                    "compression_level": "medium"
                }
            },
            {
                "name": "X3D for VR",
                "func": self.controller.export_to_x3d,
                "params": {
                    "element_ids": None,
                    "file_path": None,
                    "x3d_version": "4.0",
                    "encoding": "xml",
                    "include_materials": True,
                    "include_lighting": True,
                    "include_navigation": True,
                    "compression": False
                }
            },
            {
                "name": "WebGL Interactive",
                "func": self.controller.export_to_webgl,
                "params": {
                    "element_ids": None,
                    "file_path": None,
                    "web_quality": "high",
                    "include_materials": True,
                    "include_textures": True,
                    "embed_viewer": True,
                    "compression": True
                }
            }
        ]
        
        for format_config in web_formats:
            await self.helper.run_test(
                format_config["name"],
                format_config["func"],
                **format_config["params"]
            )
        
        # Test 3: Professional CAD exports (STEP with drilling, SAT, DSTV)
        cad_formats = [
            {
                "name": "STEP with CNC Drilling",
                "func": self.controller.export_step_with_drillings,
                "params": {
                    "element_ids": None,
                    "file_path": None,
                    "drilling_mode": "extrude",
                    "step_version": 214,
                    "scale_factor": 1.0,
                    "imperial_units": False,
                    "text_mode": False
                }
            },
            {
                "name": "SAT for ACIS",
                "func": self.controller.export_to_sat,
                "params": {
                    "element_ids": None,
                    "file_path": None,
                    "sat_version": 25000,
                    "binary_format": True,
                    "scale_factor": 1.0,
                    "include_drillings": True,
                    "drilling_mode": "cut"
                }
            },
            {
                "name": "DSTV for Steel",
                "func": self.controller.export_to_dstv,
                "params": {
                    "element_ids": None,
                    "file_path": None,
                    "dstv_version": "NC1",
                    "units": "mm",
                    "steel_grade": "S355",
                    "include_material_info": True,
                    "include_processing": True
                }
            }
        ]
        
        for format_config in cad_formats:
            await self.helper.run_test(
                format_config["name"],
                format_config["func"],
                **format_config["params"]
            )
        
        # Test 4: Batch export with optimization
        await self.helper.run_test(
            "BTL for Nesting Optimization",
            self.controller.export_btl_for_nesting,
            None,  # file_path
            {  # nesting_parameters
                "optimization_algorithm": "genetic",
                "material_waste_threshold": 5.0,
                "sheet_utilization_target": 85.0
            },
            "area",  # optimization_method
            True,  # material_efficiency
            [2440, 1220],  # sheet_size
            3  # kerf_width
        )
        
        # Test 5: Production data export
        await self.helper.run_test(
            "Comprehensive Production Data",
            self.controller.export_production_data,
            None,  # element_ids
            None,  # file_path
            "json",  # data_format
            True,  # include_cutting_list
            True,  # include_assembly_instructions
            True,  # include_hardware_list
            True,  # include_processing_data
            True,  # include_material_optimization
            True   # group_by_production_step
        )
        
        return self.helper.test_results
    
    async def run_export_quality_tests(self) -> list:
        """Test export quality and validation"""
        self.helper.print_header("EXPORT CONTROLLER - QUALITY TESTS")
        
        # Test different quality levels for mesh exports
        quality_tests = [
            ("Low Quality STL", "export_to_stl", {"mesh_quality": "low"}),
            ("Medium Quality STL", "export_to_stl", {"mesh_quality": "medium"}),
            ("High Quality STL", "export_to_stl", {"mesh_quality": "high"}),
            ("Ultra Quality OBJ", "export_to_obj", {"mesh_resolution": "ultra"}),
            ("Draft Quality glTF", "export_to_gltf", {"compression_level": "high"})
        ]
        
        for test_name, export_method, params in quality_tests:
            export_func = getattr(self.controller, export_method)
            default_params = {
                "element_ids": None,
                "file_path": None,
                "stl_format": "binary",
                "units": "mm",
                "merge_elements": True
            }
            default_params.update(params)
            
            await self.helper.run_test(
                test_name,
                export_func,
                **default_params
            )
        
        return self.helper.test_results
