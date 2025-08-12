"""
Unified Command Dispatcher for Cadwork MCP Bridge
Combines controller management and command dispatching with type safety
"""
from typing import Dict, Any, Callable, Optional
from dataclasses import dataclass

@dataclass
class DispatchResult:
    """Type-safe result container for dispatch operations"""
    success: bool
    data: Any = None
    error: Optional[str] = None

class CommandDispatcher:
    """
    Unified dispatcher that handles all bridge operations with direct function calls
    No getattr, no complex exception handling - simple and type-safe
    """
    
    def __init__(self):
        self._controllers: Dict[str, Any] = {}
        self._function_map: Dict[str, Callable[[Dict[str, Any]], DispatchResult]] = {}
        self._initialize_controllers()
        self._build_function_map()
    
    def _initialize_controllers(self) -> None:
        """Initialize all controllers once on startup"""
        try:
            from controllers.element_controller import ElementController
            from controllers.geometry_controller import GeometryController
            from controllers.attribute_controller import AttributeController
            from controllers.visualization_controller import VisualizationController
            from controllers.utility_controller import UtilityController
            from controllers.export_controller import ExportController
            from controllers.import_controller import ImportController
            from controllers.material_controller import MaterialController
            from controllers.measurement_controller import MeasurementController
            from controllers.shop_drawing_controller import ShopDrawingController
            from controllers.roof_controller import RoofController
            from controllers.machine_controller import MachineController
            from controllers.list_controller import ListController
            from controllers.optimization_controller import OptimizationController
            
            # Create controller instances
            self._controllers = {
                'element': ElementController(),
                'geometry': GeometryController(),
                'attribute': AttributeController(),
                'visualization': VisualizationController(),
                'utility': UtilityController(),
                'export': ExportController(),
                'import': ImportController(),
                'material': MaterialController(),
                'measurement': MeasurementController(),
                'shop_drawing': ShopDrawingController(),
                'roof': RoofController(),
                'machine': MachineController(),
                'list': ListController(),
                'optimization': OptimizationController(),
            }
        except ImportError as e:
            # Simplified error handling - just log and continue
            print(f"Controller initialization warning: {e}")
    
    def _build_function_map(self) -> None:
        """Build direct function mapping - no getattr, explicit and type-safe"""
        
        # Element controller functions
        elem = self._controllers.get('element')
        if elem:
            self._function_map.update({
                'create_beam': lambda args: self._wrap_call(elem.create_beam, args),
                'create_panel': lambda args: self._wrap_call(elem.create_panel, args),
                'get_active_element_ids': lambda args: self._wrap_call(elem.get_active_element_ids, args),
                'get_all_element_ids': lambda args: self._wrap_call(elem.get_all_element_ids, args),
                'get_visible_element_ids': lambda args: self._wrap_call(elem.get_visible_element_ids, args),
                'get_element_info': lambda args: self._wrap_call(elem.get_element_info, args),
                'delete_elements': lambda args: self._wrap_call(elem.delete_elements, args),
                'copy_elements': lambda args: self._wrap_call(elem.copy_elements, args),
                'move_element': lambda args: self._wrap_call(elem.move_element, args),
                'duplicate_elements': lambda args: self._wrap_call(elem.duplicate_elements, args),
                'get_user_element_ids': lambda args: self._wrap_call(elem.get_user_element_ids, args),
                'create_solid_wood_panel': lambda args: self._wrap_call(elem.create_solid_wood_panel, args),
                'create_circular_beam_points': lambda args: self._wrap_call(elem.create_circular_beam_points, args),
                'create_square_beam_points': lambda args: self._wrap_call(elem.create_square_beam_points, args),
                'create_standard_beam_points': lambda args: self._wrap_call(elem.create_standard_beam_points, args),
                'create_standard_panel_points': lambda args: self._wrap_call(elem.create_standard_panel_points, args),
                'create_drilling_points': lambda args: self._wrap_call(elem.create_drilling_points, args),
                'create_polygon_beam': lambda args: self._wrap_call(elem.create_polygon_beam, args),
                'get_elements_by_type': lambda args: self._wrap_call(elem.get_elements_by_type, args),
                'filter_elements_by_material': lambda args: self._wrap_call(elem.filter_elements_by_material, args),
                'get_elements_in_group': lambda args: self._wrap_call(elem.get_elements_in_group, args),
                'get_elements_by_color': lambda args: self._wrap_call(elem.get_elements_by_color, args),
                'get_elements_by_layer': lambda args: self._wrap_call(elem.get_elements_by_layer, args),
                'get_elements_by_dimension_range': lambda args: self._wrap_call(elem.get_elements_by_dimension_range, args),
                'get_element_count_by_type': lambda args: self._wrap_call(elem.get_element_count_by_type, args),
                'get_material_statistics': lambda args: self._wrap_call(elem.get_material_statistics, args),
                'get_group_statistics': lambda args: self._wrap_call(elem.get_group_statistics, args),
                'join_elements': lambda args: self._wrap_call(elem.join_elements, args),
                'unjoin_elements': lambda args: self._wrap_call(elem.unjoin_elements, args),
                'cut_corner_lap': lambda args: self._wrap_call(elem.cut_corner_lap, args),
                'cut_cross_lap': lambda args: self._wrap_call(elem.cut_cross_lap, args),
                'cut_half_lap': lambda args: self._wrap_call(elem.cut_half_lap, args),
                'cut_double_tenon': lambda args: self._wrap_call(elem.cut_double_tenon, args),
                'cut_scarf_joint': lambda args: self._wrap_call(elem.cut_scarf_joint, args),
                'cut_shoulder': lambda args: self._wrap_call(elem.cut_shoulder, args),
                'create_auxiliary_beam_points': lambda args: self._wrap_call(elem.create_auxiliary_beam_points, args),
                'convert_beam_to_panel': lambda args: self._wrap_call(elem.convert_beam_to_panel, args),
                'convert_panel_to_beam': lambda args: self._wrap_call(elem.convert_panel_to_beam, args),
                'convert_auxiliary_to_beam': lambda args: self._wrap_call(elem.convert_auxiliary_to_beam, args),
                'create_auto_container_from_standard': lambda args: self._wrap_call(elem.create_auto_container_from_standard, args),
                'get_container_content_elements': lambda args: self._wrap_call(elem.get_container_content_elements, args),
                'create_surface': lambda args: self._wrap_call(elem.create_surface, args),
                'chamfer_edge': lambda args: self._wrap_call(elem.chamfer_edge, args),
                'round_edge': lambda args: self._wrap_call(elem.round_edge, args),
                'split_element': lambda args: self._wrap_call(elem.split_element, args),
                'create_beam_from_points': lambda args: self._wrap_call(elem.create_beam_from_points, args),
                'create_auxiliary_line': lambda args: self._wrap_call(elem.create_auxiliary_line, args),
                'get_elements_in_region': lambda args: self._wrap_call(elem.get_elements_in_region, args),
                'stretch_elements': lambda args: self._wrap_call(elem.stretch_elements, args),
                'scale_elements': lambda args: self._wrap_call(elem.scale_elements, args),
                'mirror_elements': lambda args: self._wrap_call(elem.mirror_elements, args),
            })
        
        # Geometry controller functions  
        geom = self._controllers.get('geometry')
        if geom:
            self._function_map.update({
                'get_element_width': lambda args: self._wrap_call(geom.get_element_width, args),
                'get_element_height': lambda args: self._wrap_call(geom.get_element_height, args),
                'get_element_length': lambda args: self._wrap_call(geom.get_element_length, args),
                'get_element_volume': lambda args: self._wrap_call(geom.get_element_volume, args),
                'get_element_weight': lambda args: self._wrap_call(geom.get_element_weight, args),
                'get_element_xl': lambda args: self._wrap_call(geom.get_element_xl, args),
                'get_element_yl': lambda args: self._wrap_call(geom.get_element_yl, args),
                'get_element_zl': lambda args: self._wrap_call(geom.get_element_zl, args),
                'get_element_p1': lambda args: self._wrap_call(geom.get_element_p1, args),
                'get_element_p2': lambda args: self._wrap_call(geom.get_element_p2, args),
                'get_element_p3': lambda args: self._wrap_call(geom.get_element_p3, args),
                'get_center_of_gravity': lambda args: self._wrap_call(geom.get_center_of_gravity, args),
                'get_center_of_gravity_for_list': lambda args: self._wrap_call(geom.get_center_of_gravity_for_list, args),
                'get_element_vertices': lambda args: self._wrap_call(geom.get_element_vertices, args),
                'get_minimum_distance_between_elements': lambda args: self._wrap_call(geom.get_minimum_distance_between_elements, args),
                'get_closest_point_on_element': lambda args: self._wrap_call(geom.get_closest_point_on_element, args),
                'get_element_facets': lambda args: self._wrap_call(geom.get_element_facets, args),
                'get_element_reference_face_area': lambda args: self._wrap_call(geom.get_element_reference_face_area, args),
                'get_total_area_of_all_faces': lambda args: self._wrap_call(geom.get_total_area_of_all_faces, args),
                'rotate_elements': lambda args: self._wrap_call(geom.rotate_elements, args),
                'apply_global_scale': lambda args: self._wrap_call(geom.apply_global_scale, args),
                'invert_model': lambda args: self._wrap_call(geom.invert_model, args),
                'rotate_height_axis_90': lambda args: self._wrap_call(geom.rotate_height_axis_90, args),
                'rotate_length_axis_90': lambda args: self._wrap_call(geom.rotate_length_axis_90, args),
                'get_element_type': lambda args: self._wrap_call(geom.get_element_type, args),
                'calculate_total_volume': lambda args: self._wrap_call(geom.calculate_total_volume, args),
                'calculate_total_weight': lambda args: self._wrap_call(geom.calculate_total_weight, args),
                'get_bounding_box': lambda args: self._wrap_call(geom.get_bounding_box, args),
                'get_element_outline': lambda args: self._wrap_call(geom.get_element_outline, args),
                'get_section_outline': lambda args: self._wrap_call(geom.get_section_outline, args),
                'intersect_elements': lambda args: self._wrap_call(geom.intersect_elements, args),
                'subtract_elements': lambda args: self._wrap_call(geom.subtract_elements, args),
                'unite_elements': lambda args: self._wrap_call(geom.unite_elements, args),
                'project_point_to_element': lambda args: self._wrap_call(geom.project_point_to_element, args),
                'calculate_center_of_mass': lambda args: self._wrap_call(geom.calculate_center_of_mass, args),
                'check_collisions': lambda args: self._wrap_call(geom.check_collisions, args),
                'validate_joints': lambda args: self._wrap_call(geom.validate_joints, args),
            })
        
        # Attribute controller functions
        attr = self._controllers.get('attribute')
        if attr:
            self._function_map.update({
                'get_standard_attributes': lambda args: self._wrap_call(attr.get_standard_attributes, args),
                'get_user_attributes': lambda args: self._wrap_call(attr.get_user_attributes, args),
                'list_defined_user_attributes': lambda args: self._wrap_call(attr.list_defined_user_attributes, args),
                'set_name': lambda args: self._wrap_call(attr.set_name, args),
                'set_material': lambda args: self._wrap_call(attr.set_material, args),
                'set_group': lambda args: self._wrap_call(attr.set_group, args),
                'set_comment': lambda args: self._wrap_call(attr.set_comment, args),
                'set_subgroup': lambda args: self._wrap_call(attr.set_subgroup, args),
                'set_user_attribute': lambda args: self._wrap_call(attr.set_user_attribute, args),
                'get_element_attribute_display_name': lambda args: self._wrap_call(attr.get_element_attribute_display_name, args),
                'clear_user_attribute': lambda args: self._wrap_call(attr.clear_user_attribute, args),
                'copy_attributes': lambda args: self._wrap_call(attr.copy_attributes, args),
                'batch_set_user_attributes': lambda args: self._wrap_call(attr.batch_set_user_attributes, args),
                'validate_attribute_consistency': lambda args: self._wrap_call(attr.validate_attribute_consistency, args),
                'search_elements_by_attributes': lambda args: self._wrap_call(attr.search_elements_by_attributes, args),
                'export_attribute_report': lambda args: self._wrap_call(attr.export_attribute_report, args),
            })
        
        # Visualization controller functions
        vis = self._controllers.get('visualization')
        if vis:
            self._function_map.update({
                'set_color': lambda args: self._wrap_call(vis.set_color, args),
                'set_visibility': lambda args: self._wrap_call(vis.set_visibility, args),
                'set_transparency': lambda args: self._wrap_call(vis.set_transparency, args),
                'get_color': lambda args: self._wrap_call(vis.get_color, args),
                'get_transparency': lambda args: self._wrap_call(vis.get_transparency, args),
                'show_all_elements': lambda args: self._wrap_call(vis.show_all_elements, args),
                'hide_all_elements': lambda args: self._wrap_call(vis.hide_all_elements, args),
                'refresh_display': lambda args: self._wrap_call(vis.refresh_display, args),
                'get_visible_element_count': lambda args: self._wrap_call(vis.get_visible_element_count, args),
                'create_visual_filter': lambda args: self._wrap_call(vis.create_visual_filter, args),
                'apply_color_scheme': lambda args: self._wrap_call(vis.apply_color_scheme, args),
                'create_assembly_animation': lambda args: self._wrap_call(vis.create_assembly_animation, args),
                'set_camera_position': lambda args: self._wrap_call(vis.set_camera_position, args),
                'create_walkthrough': lambda args: self._wrap_call(vis.create_walkthrough, args),
            })
        
        # Utility controller functions
        util = self._controllers.get('utility')
        if util:
            self._function_map.update({
                'disable_auto_display_refresh': lambda args: self._wrap_call(util.disable_auto_display_refresh, args),
                'enable_auto_display_refresh': lambda args: self._wrap_call(util.enable_auto_display_refresh, args),
                'print_error': lambda args: self._wrap_call(util.print_error, args),
                'print_warning': lambda args: self._wrap_call(util.print_warning, args),
                'get_3d_file_path': lambda args: self._wrap_call(util.get_3d_file_path, args),
                'get_project_data': lambda args: self._wrap_call(util.get_project_data, args),
                'get_cadwork_version_info': lambda args: self._wrap_call(util.get_cadwork_version_info, args),
                'ping': lambda args: self._wrap_call(util.ping, args),
                'get_version_info': lambda args: self._wrap_call(util.get_cadwork_version_info, args),
                'get_model_name': lambda args: self._wrap_call(util.get_project_data, args),
            })
        
        # Add remaining controllers with their key functions
        self._add_remaining_controllers()
    
    def _add_remaining_controllers(self) -> None:
        """Add remaining controller functions"""
        
        # Export controller
        export = self._controllers.get('export')
        if export:
            export_funcs = [
                'export_to_btl', 'export_element_list', 'export_to_ifc', 'export_to_dxf',
                'export_workshop_drawings', 'export_to_step', 'export_to_3dm', 'export_to_obj',
                'export_to_ply', 'export_to_stl', 'export_to_gltf', 'export_to_x3d',
                'export_production_data', 'export_to_fbx', 'export_to_webgl', 'export_to_sat',
                'export_to_dstv', 'export_step_with_drillings', 'export_btl_for_nesting',
                'export_cutting_list'
            ]
            for func_name in export_funcs:
                if hasattr(export, func_name):
                    self._function_map[func_name] = self._create_wrapper(export, func_name)
        
        # Import controller  
        import_ctrl = self._controllers.get('import')
        if import_ctrl:
            import_funcs = ['import_from_step', 'import_from_sat', 'import_from_rhino', 'import_from_btl']
            for func_name in import_funcs:
                if hasattr(import_ctrl, func_name):
                    self._function_map[func_name] = self._create_wrapper(import_ctrl, func_name)
        
        # Add other controllers (material, measurement, shop_drawing, roof, machine, list, optimization)
        controller_functions = {
            'material': ['create_material', 'get_material_properties', 'list_available_materials'],
            'measurement': ['measure_distance', 'measure_angle', 'measure_area'],
            'shop_drawing': ['add_wall_section_x', 'add_wall_section_y', 'add_wall_section_vertical', 'export_2d_wireframe'],
            'roof': ['get_roof_surfaces', 'calculate_roof_area'],
            'machine': ['check_production_list_discrepancies'],
            'list': ['create_element_list', 'generate_material_list'],
            'optimization': ['optimize_cutting_list']
        }
        
        for controller_name, functions in controller_functions.items():
            controller = self._controllers.get(controller_name)
            if controller:
                for func_name in functions:
                    if hasattr(controller, func_name):
                        self._function_map[func_name] = self._create_wrapper(controller, func_name)
    
    def _create_wrapper(self, controller: Any, func_name: str) -> Callable[[Dict[str, Any]], DispatchResult]:
        """Create a type-safe wrapper function for controller methods"""
        func = getattr(controller, func_name)
        return lambda args: self._wrap_call(func, args)
    
    def _wrap_call(self, func: Callable, args: Dict[str, Any]) -> DispatchResult:
        """Wrap controller function call with unified error handling"""
        try:
            result = func(**args) if args else func()
            return DispatchResult(success=True, data=result)
        except Exception as e:
            return DispatchResult(success=False, error=str(e))
    
    def dispatch(self, operation: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main dispatch method - replaces both old dispatcher and controller manager
        
        Args:
            operation: Function name to call
            args: Arguments for the function
            
        Returns:
            Dict with status, data, and optional error message
        """
        if operation not in self._function_map:
            return {
                "status": "error",
                "message": f"Unknown operation: {operation}",
                "available_operations": list(self._function_map.keys())[:20]  # Show first 20 for debugging
            }
        
        result = self._function_map[operation](args)
        
        if result.success:
            return {
                "status": "success",
                "data": result.data
            }
        else:
            return {
                "status": "error", 
                "message": f"Operation {operation} failed: {result.error}"
            }

# Global dispatcher instance
_dispatcher = CommandDispatcher()

def dispatch_command(operation: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """Main entry point for all bridge commands"""
    return _dispatcher.dispatch(operation, args)
