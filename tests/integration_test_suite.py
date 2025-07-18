"""
Integration Test Suite
=====================

Tests integration between multiple controllers and complete workflows.
Simulates real-world usage scenarios with multiple controllers working together.
"""

import sys
import os
import asyncio
import time
from typing import List, Dict, Any

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from controllers.element_controller import ElementController
from controllers.geometry_controller import GeometryController
from controllers.visualization_controller import CVisualizationController
from controllers.attribute_controller import AttributeController
from controllers.material_controller import CMaterialController
from controllers.measurement_controller import CMeasurementController
from controllers.export_controller import CExportController
from tests.helpers.test_helper import TestHelper, TestResult
from tests.helpers.parameter_finder import ParameterFinder


class IntegrationTestSuite:
    """Integration tests for complete workflows"""
    
    def __init__(self):
        self.element_ctrl = ElementController()
        self.geometry_ctrl = GeometryController()
        self.viz_ctrl = CVisualizationController()
        self.attr_ctrl = AttributeController()
        self.material_ctrl = CMaterialController()
        self.measurement_ctrl = CMeasurementController()
        self.export_ctrl = CExportController()
        self.helper = TestHelper()
        self.param_finder = ParameterFinder()
        self.integration_elements: List[int] = []
    
    async def run_all_integration_tests(self) -> List[TestResult]:
        """Run comprehensive integration test suite"""
        self.helper.print_header("CADWORK MCP INTEGRATION TEST SUITE")
        
        # Complete building workflow
        await self._test_complete_building_workflow()
        
        # Manufacturing workflow
        await self._test_manufacturing_workflow()
        
        # Design validation workflow
        await self._test_design_validation_workflow()
        
        # Multi-controller data flow
        await self._test_multi_controller_data_flow()
        
        # Real-world scenarios
        await self._test_real_world_scenarios()
        
        # Cleanup
        await self._cleanup_integration_elements()
        
        return self.helper.test_results
    
    async def _test_complete_building_workflow(self) -> None:
        """Test complete building design and construction workflow"""
        self.helper.print_subheader("Complete Building Workflow")
        
        workflow_start = time.time()
        
        # Step 1: Create materials
        await self.helper.run_test(
            "Create Wood Material",
            self.material_ctrl.create_material,
            "StructuralWood",
            650.0,  # density
            0.15,   # thermal_conductivity
            11000.0,  # elastic_modulus
            5       # color_id
        )
        
        await self.helper.run_test(
            "Create Steel Material",
            self.material_ctrl.create_material,
            "StructuralSteel",
            7850.0,
            50.0,
            210000.0,
            15
        )
        
        # Step 2: Create building structure
        building_elements = await self._create_building_structure()
        
        # Step 3: Apply materials and attributes
        if building_elements:
            # Apply materials
            wood_elements = building_elements[:len(building_elements)//2]
            steel_elements = building_elements[len(building_elements)//2:]
            
            if wood_elements:
                await self.helper.run_test(
                    "Apply Wood Material",
                    self.attr_ctrl.set_material,
                    wood_elements,
                    "StructuralWood"
                )
                
                await self.helper.run_test(
                    "Set Wood Group",
                    self.attr_ctrl.set_group,
                    wood_elements,
                    "WoodStructure"
                )
            
            if steel_elements:
                await self.helper.run_test(
                    "Apply Steel Material",
                    self.attr_ctrl.set_material,
                    steel_elements,
                    "StructuralSteel"
                )
                
                await self.helper.run_test(
                    "Set Steel Group",
                    self.attr_ctrl.set_group,
                    steel_elements,
                    "SteelStructure"
                )
            
            # Step 4: Visualization setup
            await self._setup_building_visualization(building_elements)
            
            # Step 5: Calculate building metrics
            await self._calculate_building_metrics(building_elements)
            
            # Step 6: Export building data
            await self._export_building_data(building_elements)
        
        workflow_time = time.time() - workflow_start
        
        await self.helper.run_test(
            "Complete Building Workflow Summary",
            self._create_workflow_summary,
            "Building", len(building_elements) if building_elements else 0, workflow_time
        )
    
    async def _test_manufacturing_workflow(self) -> None:
        """Test manufacturing preparation workflow"""
        self.helper.print_subheader("Manufacturing Workflow")
        
        # Step 1: Create components for manufacturing
        components = await self._create_manufacturing_components()
        
        if components:
            # Step 2: Apply manufacturing attributes
            await self.helper.run_test(
                "Set Production Numbers",
                self.attr_ctrl.set_name,
                components,
                "PROD-2024-001"
            )
            
            await self.helper.run_test(
                "Set Manufacturing Group",
                self.attr_ctrl.set_group,
                components,
                "Production_Batch_A"
            )
            
            # Step 3: Perform quality measurements
            await self._perform_quality_measurements(components)
            
            # Step 4: Create manufacturing exports
            await self._create_manufacturing_exports(components)
            
            # Step 5: Visualization for production
            await self._setup_production_visualization(components)
    
    async def _test_design_validation_workflow(self) -> None:
        """Test design validation and analysis workflow"""
        self.helper.print_subheader("Design Validation Workflow")
        
        # Step 1: Create design elements
        design_elements = await self._create_design_elements()
        
        if design_elements:
            # Step 2: Validate geometry
            await self._validate_design_geometry(design_elements)
            
            # Step 3: Check structural requirements
            await self._check_structural_requirements(design_elements)
            
            # Step 4: Generate analysis reports
            await self._generate_analysis_reports(design_elements)
    
    async def _test_multi_controller_data_flow(self) -> None:
        """Test data flow between multiple controllers"""
        self.helper.print_subheader("Multi-Controller Data Flow")
        
        # Create test elements
        flow_elements = []
        
        # Create elements using ElementController
        for i in range(3):
            beam_params = self.param_finder.get_beam_parameters()
            beam_params["p1"][0] += i * 2000
            beam_params["p2"][0] += i * 2000
            
            result = await self.element_ctrl.create_beam(**beam_params)
            if result.get("status") == "success":
                element_id = result.get("element_id")
                if element_id:
                    flow_elements.append(element_id)
        
        if flow_elements:
            self.integration_elements.extend(flow_elements)
            
            # Test data flow: Element -> Geometry -> Visualization -> Attributes
            for element_id in flow_elements:
                # Get geometry data
                geometry_result = await self.helper.run_test(
                    f"Get Geometry Data - Element {element_id}",
                    self.geometry_ctrl.get_element_info,
                    element_id
                )
                
                # Use geometry data for visualization
                await self.helper.run_test(
                    f"Set Visualization - Element {element_id}",
                    self.viz_ctrl.set_color,
                    [element_id],
                    (element_id % 10) + 1  # Vary colors
                )
                
                # Set attributes based on element properties
                await self.helper.run_test(
                    f"Set Attributes - Element {element_id}",
                    self.attr_ctrl.set_name,
                    [element_id],
                    f"Element_{element_id}"
                )
    
    async def _test_real_world_scenarios(self) -> None:
        """Test real-world usage scenarios"""
        self.helper.print_subheader("Real-World Scenarios")
        
        # Scenario 1: Architect's workflow
        await self._test_architect_workflow()
        
        # Scenario 2: Engineer's workflow
        await self._test_engineer_workflow()
        
        # Scenario 3: Manufacturer's workflow
        await self._test_manufacturer_workflow()
    
    # Helper methods for workflow steps
    async def _create_building_structure(self) -> List[int]:
        """Create a basic building structure"""
        structure_elements = []
        
        # Create foundation beams
        foundation_configs = [
            {"p1": [0, 0, 0], "p2": [10000, 0, 0], "width": 300, "height": 400},  # Main beam
            {"p1": [0, 0, 0], "p2": [0, 8000, 0], "width": 300, "height": 400},  # Side beam
            {"p1": [10000, 0, 0], "p2": [10000, 8000, 0], "width": 300, "height": 400},  # Other side
            {"p1": [0, 8000, 0], "p2": [10000, 8000, 0], "width": 300, "height": 400}  # Back beam
        ]
        
        for config in foundation_configs:
            result = await self.element_ctrl.create_beam(**config)
            if result.get("status") == "success":
                element_id = result.get("element_id")
                if element_id:
                    structure_elements.append(element_id)
        
        # Create vertical columns
        column_positions = [(0, 0), (10000, 0), (0, 8000), (10000, 8000), (5000, 4000)]
        
        for x, y in column_positions:
            column_config = {
                "p1": [x, y, 0],
                "p2": [x, y, 3000],  # 3m high
                "width": 200,
                "height": 200
            }
            
            result = await self.element_ctrl.create_beam(**column_config)
            if result.get("status") == "success":
                element_id = result.get("element_id")
                if element_id:
                    structure_elements.append(element_id)
        
        # Create roof structure
        roof_configs = [
            {"p1": [0, 0, 3000], "p2": [10000, 0, 3000], "width": 200, "height": 300},
            {"p1": [0, 8000, 3000], "p2": [10000, 8000, 3000], "width": 200, "height": 300},
            {"p1": [0, 0, 3000], "p2": [0, 8000, 3000], "width": 200, "height": 300},
            {"p1": [10000, 0, 3000], "p2": [10000, 8000, 3000], "width": 200, "height": 300}
        ]
        
        for config in roof_configs:
            result = await self.element_ctrl.create_beam(**config)
            if result.get("status") == "success":
                element_id = result.get("element_id")
                if element_id:
                    structure_elements.append(element_id)
        
        self.integration_elements.extend(structure_elements)
        return structure_elements
    
    async def _setup_building_visualization(self, elements):
        """Setup visualization for building elements"""
        if not elements:
            return
        
        # Color code by function
        foundation_elements = elements[:4]  # First 4 are foundation
        column_elements = elements[4:9]     # Next 5 are columns
        roof_elements = elements[9:]        # Rest are roof
        
        if foundation_elements:
            await self.helper.run_test(
                "Color Foundation (Brown)",
                self.viz_ctrl.set_color,
                foundation_elements,
                5  # Brown
            )
        
        if column_elements:
            await self.helper.run_test(
                "Color Columns (Gray)",
                self.viz_ctrl.set_color,
                column_elements,
                10  # Gray
            )
        
        if roof_elements:
            await self.helper.run_test(
                "Color Roof (Red)",
                self.viz_ctrl.set_color,
                roof_elements,
                1  # Red
            )
    
    async def _calculate_building_metrics(self, elements):
        """Calculate building metrics"""
        if not elements:
            return
        
        await self.helper.run_test(
            "Calculate Total Building Volume",
            self.geometry_ctrl.calculate_total_volume,
            elements
        )
        
        await self.helper.run_test(
            "Calculate Total Building Weight",
            self.geometry_ctrl.calculate_total_weight,
            elements
        )
        
        await self.helper.run_test(
            "Calculate Building Center of Mass",
            self.geometry_ctrl.calculate_center_of_mass,
            elements,
            True
        )
    
    async def _export_building_data(self, elements):
        """Export building data in multiple formats"""
        if not elements:
            return
        
        # Export for different purposes
        await self.helper.run_test(
            "Export IFC for BIM",
            self.export_ctrl.export_to_ifc,
            elements,
            None,  # file_path
            "IFC4",
            "project",
            True, True, True
        )
        
        await self.helper.run_test(
            "Export STEP for CAD",
            self.export_ctrl.export_to_step,
            elements,
            None,
            "AP214",
            "mm",
            0.01
        )
    
    async def _create_manufacturing_components(self) -> List[int]:
        """Create components for manufacturing testing"""
        components = []
        
        # Create precision components
        precision_configs = [
            {"p1": [0, 0, 0], "p2": [1200, 0, 0], "width": 80, "height": 120},     # Standard beam
            {"p1": [1500, 0, 0], "p2": [2700, 0, 0], "width": 100, "height": 200}, # Larger beam
            {"p1": [3000, 0, 0], "p2": [4000, 0, 0], "width": 60, "height": 80}    # Small beam
        ]
        
        for config in precision_configs:
            result = await self.element_ctrl.create_beam(**config)
            if result.get("status") == "success":
                element_id = result.get("element_id")
                if element_id:
                    components.append(element_id)
        
        self.integration_elements.extend(components)
        return components
    
    async def _perform_quality_measurements(self, components):
        """Perform quality control measurements"""
        if not components:
            return
        
        for i, element_id in enumerate(components):
            await self.helper.run_test(
                f"QC Length Check - Component {i+1}",
                self.geometry_ctrl.get_element_length,
                element_id
            )
            
            await self.helper.run_test(
                f"QC Dimension Check - Component {i+1}",
                self.geometry_ctrl.get_element_width,
                element_id
            )
    
    async def _create_manufacturing_exports(self, components):
        """Create manufacturing exports"""
        if not components:
            return
        
        await self.helper.run_test(
            "Export BTL for CNC",
            self.export_ctrl.export_to_btl,
            components,
            None,
            "10.5",
            True, True
        )
        
        await self.helper.run_test(
            "Export Workshop Drawings",
            self.export_ctrl.export_workshop_drawings,
            components,
            "pdf",
            True, True,
            "1:10", "A3"
        )
    
    async def _setup_production_visualization(self, components):
        """Setup visualization for production"""
        if not components:
            return
        
        # Set production colors
        await self.helper.run_test(
            "Set Production Colors",
            self.viz_ctrl.set_color,
            components,
            25  # Production blue
        )
        
        # Set transparency for work-in-progress view
        await self.helper.run_test(
            "Set WIP Transparency",
            self.viz_ctrl.set_transparency,
            components,
            30  # 30% transparent
        )
    
    async def _create_design_elements(self) -> List[int]:
        """Create elements for design validation"""
        design_elements = []
        
        # Create design test structure
        design_configs = [
            {"p1": [0, 0, 0], "p2": [5000, 0, 0], "width": 150, "height": 200},
            {"p1": [2500, 0, 0], "p2": [2500, 3000, 0], "width": 100, "height": 100},
            {"p1": [0, 3000, 0], "p2": [5000, 3000, 0], "width": 150, "height": 200}
        ]
        
        for config in design_configs:
            result = await self.element_ctrl.create_beam(**config)
            if result.get("status") == "success":
                element_id = result.get("element_id")
                if element_id:
                    design_elements.append(element_id)
        
        self.integration_elements.extend(design_elements)
        return design_elements
    
    async def _validate_design_geometry(self, elements):
        """Validate design geometry"""
        if not elements:
            return
        
        for element_id in elements:
            await self.helper.run_test(
                f"Validate Bounding Box - {element_id}",
                self.geometry_ctrl.get_bounding_box,
                element_id
            )
    
    async def _check_structural_requirements(self, elements):
        """Check structural requirements"""
        if not elements:
            return
        
        await self.helper.run_test(
            "Check Total Load",
            self.geometry_ctrl.calculate_total_weight,
            elements
        )
    
    async def _generate_analysis_reports(self, elements):
        """Generate analysis reports"""
        if not elements:
            return
        
        await self.helper.run_test(
            "Generate Element List",
            self.export_ctrl.export_element_list,
            elements,
            "json",
            None,
            True, True
        )
    
    async def _test_architect_workflow(self):
        """Test typical architect workflow"""
        # Create basic design
        arch_beam_params = self.param_finder.get_beam_parameters()
        arch_beam_params["p1"] = [20000, 0, 0]  # Offset from other tests
        arch_beam_params["p2"] = [22000, 0, 0]
        
        result = await self.helper.run_test(
            "Architect: Create Design Element",
            self.element_ctrl.create_beam,
            **arch_beam_params
        )
        
        if result.status == "PASSED" and result.details:
            element_id = result.details.get("element_id")
            if element_id:
                self.integration_elements.append(element_id)
                
                # Typical architect workflow steps
                await self.helper.run_test(
                    "Architect: Set Design Name",
                    self.attr_ctrl.set_name,
                    [element_id],
                    "ARCH_BEAM_001"
                )
                
                await self.helper.run_test(
                    "Architect: Apply Visual Style",
                    self.viz_ctrl.set_color,
                    [element_id],
                    20  # Design color
                )
    
    async def _test_engineer_workflow(self):
        """Test typical engineer workflow"""
        # Engineer creates structural elements
        eng_beam_params = self.param_finder.get_beam_parameters()
        eng_beam_params["p1"] = [25000, 0, 0]  # Different offset
        eng_beam_params["p2"] = [27000, 0, 0]
        
        result = await self.helper.run_test(
            "Engineer: Create Structural Element",
            self.element_ctrl.create_beam,
            **eng_beam_params
        )
        
        if result.status == "PASSED" and result.details:
            element_id = result.details.get("element_id")
            if element_id:
                self.integration_elements.append(element_id)
                
                # Engineer workflow steps
                await self.helper.run_test(
                    "Engineer: Calculate Properties",
                    self.geometry_ctrl.get_element_volume,
                    element_id
                )
                
                await self.helper.run_test(
                    "Engineer: Set Structural Group",
                    self.attr_ctrl.set_group,
                    [element_id],
                    "STRUCTURAL"
                )
    
    async def _test_manufacturer_workflow(self):
        """Test typical manufacturer workflow"""
        # Manufacturer prepares for production
        mfg_beam_params = self.param_finder.get_beam_parameters()
        mfg_beam_params["p1"] = [30000, 0, 0]  # Another offset
        mfg_beam_params["p2"] = [32000, 0, 0]
        
        result = await self.helper.run_test(
            "Manufacturer: Create Production Element",
            self.element_ctrl.create_beam,
            **mfg_beam_params
        )
        
        if result.status == "PASSED" and result.details:
            element_id = result.details.get("element_id")
            if element_id:
                self.integration_elements.append(element_id)
                
                # Manufacturer workflow steps
                await self.helper.run_test(
                    "Manufacturer: Set Production ID",
                    self.attr_ctrl.set_name,
                    [element_id],
                    "MFG_2024_001"
                )
                
                await self.helper.run_test(
                    "Manufacturer: Prepare CNC Export",
                    self.export_ctrl.export_to_btl,
                    [element_id],
                    None, "10.5", True, True
                )
    
    async def _create_workflow_summary(self, workflow_name, element_count, time_taken):
        """Create workflow summary"""
        return {
            "status": "success",
            "message": f"{workflow_name} workflow: {element_count} elements processed in {time_taken:.2f}s",
            "workflow_metrics": {
                "workflow_type": workflow_name,
                "elements_processed": element_count,
                "time_seconds": time_taken,
                "elements_per_second": element_count / time_taken if time_taken > 0 else 0
            }
        }
    
    async def _cleanup_integration_elements(self):
        """Cleanup integration test elements"""
        if self.integration_elements:
            self.helper.print_subheader("Integration Test Cleanup")
            
            try:
                await self.element_ctrl.delete_elements(self.integration_elements)
                cleanup_count = len(self.integration_elements)
                self.integration_elements.clear()
                
                await self.helper.run_test(
                    "Integration Cleanup",
                    self._report_cleanup,
                    cleanup_count
                )
            except:
                pass
    
    async def _report_cleanup(self, count):
        """Report cleanup results"""
        return {
            "status": "success",
            "message": f"Cleaned up {count} integration test elements"
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get integration test summary"""
        return self.helper.get_summary()
    
    def print_summary(self) -> None:
        """Print integration test summary"""
        self.helper.print_summary()


# Convenience function for standalone testing
async def run_integration_tests() -> None:
    """Run integration test suite standalone"""
    test_suite = IntegrationTestSuite()
    await test_suite.run_all_integration_tests()
    test_suite.print_summary()


if __name__ == "__main__":
    print("🏗️  CADWORK MCP INTEGRATION TEST SUITE")
    print("⚠️  This will run complete workflows with multiple controllers!")
    print("⚠️  Ensure Cadwork 3D is running and ready for integration testing!")
    print()
    
    asyncio.run(run_integration_tests())
