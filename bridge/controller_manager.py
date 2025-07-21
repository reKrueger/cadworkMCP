# bridge/controller_manager.py
"""
Centralized Controller Manager for consistent API calls
CORRECTED VERSION - All functions properly mapped without C prefix
"""
from typing import Any, Dict, List

# Mapping: function_name -> primary_controller  
FUNCTION_CONTROLLER_MAP = {
    # ======= VISUALIZATION CONTROLLER =======
    'set_color': 'visualization_controller',
    'set_visibility': 'visualization_controller', 
    'set_transparency': 'visualization_controller',
    'get_color': 'visualization_controller',
    'get_transparency': 'visualization_controller',
    'show_all_elements': 'visualization_controller',
    'hide_all_elements': 'visualization_controller',
    'refresh_display': 'visualization_controller',
    'get_visible_element_count': 'visualization_controller',
    'create_visual_filter': 'visualization_controller',
    'apply_color_scheme': 'visualization_controller',
    'create_assembly_animation': 'visualization_controller',
    'set_camera_position': 'visualization_controller',
    'create_walkthrough': 'visualization_controller',
    
    # ======= ATTRIBUTE CONTROLLER =======
    'get_standard_attributes': 'attribute_controller',
    'get_user_attributes': 'attribute_controller',
    'list_defined_user_attributes': 'attribute_controller',
    'set_name': 'attribute_controller',
    'set_material': 'attribute_controller',
    'set_group': 'attribute_controller',
    'set_comment': 'attribute_controller',
    'set_subgroup': 'attribute_controller',
    'set_user_attribute': 'attribute_controller',
    'get_element_attribute_display_name': 'attribute_controller',
    'clear_user_attribute': 'attribute_controller',
    'copy_attributes': 'attribute_controller',
    'batch_set_user_attributes': 'attribute_controller',
    'validate_attribute_consistency': 'attribute_controller',
    'search_elements_by_attributes': 'attribute_controller',
    'export_attribute_report': 'attribute_controller',
    
    # ======= ELEMENT CONTROLLER =======
    'create_beam': 'element_controller',
    'create_panel': 'element_controller',
    'get_active_element_ids': 'element_controller',
    'get_all_element_ids': 'element_controller',
    'get_visible_element_ids': 'element_controller',
    'get_element_info': 'element_controller',
    'delete_elements': 'element_controller',
    'copy_elements': 'element_controller',
    'move_element': 'element_controller',  # Singular form!
    'get_user_element_ids': 'element_controller',
    'duplicate_elements': 'element_controller',
    'stretch_elements': 'element_controller',
    'scale_elements': 'element_controller',
    'mirror_elements': 'element_controller',
    'create_solid_wood_panel': 'element_controller',
    'create_circular_beam_points': 'element_controller',
    'create_square_beam_points': 'element_controller',
    'create_standard_beam_points': 'element_controller',
    'create_standard_panel_points': 'element_controller',
    'create_drilling_points': 'element_controller',
    'create_polygon_beam': 'element_controller',
    'get_elements_by_type': 'element_controller',
    'filter_elements_by_material': 'element_controller',
    'get_elements_in_group': 'element_controller',
    'get_elements_by_color': 'element_controller',
    'get_elements_by_layer': 'element_controller',
    'get_elements_by_dimension_range': 'element_controller',
    'get_element_count_by_type': 'element_controller',
    'get_material_statistics': 'element_controller',
    'get_group_statistics': 'element_controller',
    'join_elements': 'element_controller',
    'unjoin_elements': 'element_controller',
    'cut_corner_lap': 'element_controller',
    'cut_cross_lap': 'element_controller',
    'cut_half_lap': 'element_controller',
    'cut_double_tenon': 'element_controller',
    'cut_scarf_joint': 'element_controller',
    'cut_shoulder': 'element_controller',
    'create_auxiliary_beam_points': 'element_controller',
    'convert_beam_to_panel': 'element_controller',
    'convert_panel_to_beam': 'element_controller',
    'convert_auxiliary_to_beam': 'element_controller',
    'create_auto_container_from_standard': 'element_controller',
    'get_container_content_elements': 'element_controller',
    'create_surface': 'element_controller',
    'chamfer_edge': 'element_controller',
    'round_edge': 'element_controller',
    'split_element': 'element_controller',
    'create_beam_from_points': 'element_controller',
    'create_auxiliary_line': 'element_controller',
    'get_elements_in_region': 'element_controller',
    
    # ======= GEOMETRY CONTROLLER =======
    'get_element_width': 'geometry_controller',
    'get_element_height': 'geometry_controller',
    'get_element_length': 'geometry_controller',
    'get_element_volume': 'geometry_controller',
    'get_element_weight': 'geometry_controller',
    'get_element_xl': 'geometry_controller',
    'get_element_yl': 'geometry_controller',
    'get_element_zl': 'geometry_controller',
    'get_element_p1': 'geometry_controller',
    'get_element_p2': 'geometry_controller',
    'get_element_p3': 'geometry_controller',
    'get_center_of_gravity': 'geometry_controller',
    'get_center_of_gravity_for_list': 'geometry_controller',
    'get_element_vertices': 'geometry_controller',
    'get_minimum_distance_between_elements': 'geometry_controller',
    'get_closest_point_on_element': 'geometry_controller',
    'get_element_facets': 'geometry_controller',
    'get_element_reference_face_area': 'geometry_controller',
    'get_total_area_of_all_faces': 'geometry_controller',
    'rotate_elements': 'geometry_controller',
    'apply_global_scale': 'geometry_controller',
    'invert_model': 'geometry_controller',
    'rotate_height_axis_90': 'geometry_controller',
    'rotate_length_axis_90': 'geometry_controller',
    'get_element_type': 'geometry_controller',
    'calculate_total_volume': 'geometry_controller',
    'calculate_total_weight': 'geometry_controller',
    'get_bounding_box': 'geometry_controller',
    'get_element_outline': 'geometry_controller',
    'get_section_outline': 'geometry_controller',
    'intersect_elements': 'geometry_controller',
    'subtract_elements': 'geometry_controller',
    'unite_elements': 'geometry_controller',
    'project_point_to_element': 'geometry_controller',
    'calculate_center_of_mass': 'geometry_controller',
    'check_collisions': 'geometry_controller',
    'validate_joints': 'geometry_controller',
    
    # ======= UTILITY CONTROLLER =======
    'disable_auto_display_refresh': 'utility_controller',
    'enable_auto_display_refresh': 'utility_controller',
    'print_error': 'utility_controller',
    'print_warning': 'utility_controller',
    'get_3d_file_path': 'utility_controller',
    'get_project_data': 'utility_controller',
    'get_cadwork_version_info': 'utility_controller',
    
    # ======= EXPORT CONTROLLER =======
    'export_to_btl': 'export_controller',
    'get_export_formats': 'export_controller',
    'export_element_list': 'export_controller',
    'export_cutting_list': 'export_controller',
    'export_to_ifc': 'export_controller',
    'export_to_dxf': 'export_controller',
    'export_workshop_drawings': 'export_controller',
    'export_to_step': 'export_controller',
    'export_to_3dm': 'export_controller',
    'export_to_obj': 'export_controller',
    'export_to_ply': 'export_controller',
    'export_to_stl': 'export_controller',
    'export_to_gltf': 'export_controller',
    'export_to_x3d': 'export_controller',
    'export_production_data': 'export_controller',
    'export_to_fbx': 'export_controller',
    'export_to_webgl': 'export_controller',
    'export_to_sat': 'export_controller',
    'export_to_dstv': 'export_controller',
    'export_step_with_drillings': 'export_controller',
    'export_btl_for_nesting': 'export_controller',
    
    # ======= IMPORT CONTROLLER =======
    'import_from_step': 'import_controller',
    'import_from_sat': 'import_controller',
    'import_from_rhino': 'import_controller',
    'import_from_btl': 'import_controller',
    
    # ======= SHOP DRAWING CONTROLLER =======
    'add_wall_section_x': 'shop_drawing_controller',
    'add_wall_section_y': 'shop_drawing_controller',
    'add_wall_section_vertical': 'shop_drawing_controller',
    'export_2d_wireframe': 'shop_drawing_controller',
    
    # ======= MATERIAL CONTROLLER =======
    'create_material': 'material_controller',
    'get_material_properties': 'material_controller',
    'list_available_materials': 'material_controller',
    
    # ======= MEASUREMENT CONTROLLER =======
    'measure_distance': 'measurement_controller',
    'measure_angle': 'measurement_controller',
    'measure_area': 'measurement_controller',
    
    # ======= ROOF CONTROLLER =======
    'get_roof_surfaces': 'roof_controller',
    'calculate_roof_area': 'roof_controller',
    
    # ======= MACHINE CONTROLLER =======
    'check_production_list_discrepancies': 'machine_controller',
    
    # ======= LIST CONTROLLER =======
    'create_element_list': 'list_controller',
    'generate_material_list': 'list_controller',
    
    # ======= OPTIMIZATION CONTROLLER =======
    'optimize_cutting_list': 'optimization_controller',
}

# Extended fallback controller order
FALLBACK_CONTROLLERS = [
    'element_controller',
    'attribute_controller',
    'visualization_controller', 
    'geometry_controller',
    'export_controller',
    'import_controller',
    'utility_controller',
    'shop_drawing_controller',
    'material_controller',
    'measurement_controller',
    'roof_controller',
    'machine_controller',
    'list_controller',
    'optimization_controller',
    'transformation_controller',
    'container_controller'
]

class ControllerManager:
    """Central manager for controller calls"""
    
    def __init__(self):
        self._controller_cache = {}
    
    def _get_controller(self, controller_name: str):
        """Load controller with caching"""
        if controller_name not in self._controller_cache:
            try:
                # Import with correct path
                module_path = f"controllers.{controller_name}"
                module = __import__(module_path, fromlist=[controller_name])
                
                # Create controller instance based on class name
                class_name = self._get_controller_class_name(controller_name)
                controller_class = getattr(module, class_name)
                self._controller_cache[controller_name] = controller_class()
                
            except ImportError as e:
                raise ImportError(f"Controller {controller_name} not available: {e}")
            except AttributeError as e:
                raise AttributeError(f"Controller class for {controller_name} not found: {e}")
                
        return self._controller_cache[controller_name]
    
    def _get_controller_class_name(self, controller_name: str) -> str:
        """Convert controller name to class name"""
        # Remove '_controller' suffix and convert to CamelCase
        # element_controller -> ElementController
        parts = controller_name.replace('_controller', '').split('_')
        class_name = ''.join(word.capitalize() for word in parts) + 'Controller'
        return class_name
    
    def call_function(self, function_name: str, *args, **kwargs) -> Any:
        """
        Call a function in the correct controller
        
        Args:
            function_name: Name of the function to call
            *args, **kwargs: Parameters for the function
            
        Returns:
            Return value of the controller function
            
        Raises:
            AttributeError: If function is not found in any controller
        """
        
        # 1. Try mapped controller
        if function_name in FUNCTION_CONTROLLER_MAP:
            controller_name = FUNCTION_CONTROLLER_MAP[function_name]
            try:
                controller = self._get_controller(controller_name)
                if hasattr(controller, function_name):
                    return getattr(controller, function_name)(*args, **kwargs)
                else:
                    print(f"Warning: Function {function_name} not found in mapped controller {controller_name}")
            except Exception as e:
                print(f"Warning: Primary controller {controller_name} failed for {function_name}: {e}")
        
        # 2. Fallback: Try all controllers in order
        for controller_name in FALLBACK_CONTROLLERS:
            try:
                controller = self._get_controller(controller_name)
                if hasattr(controller, function_name):
                    result = getattr(controller, function_name)(*args, **kwargs)
                    print(f"Success: Found {function_name} in fallback controller {controller_name}")
                    
                    # Update mapping for future calls
                    FUNCTION_CONTROLLER_MAP[function_name] = controller_name
                    return result
            except Exception as e:
                print(f"Fallback controller {controller_name} failed for {function_name}: {e}")
                continue
        
        raise AttributeError(f"Function '{function_name}' not found in any available controller")

# Global instance
controller_manager = ControllerManager()

def call_cadwork_function(function_name: str, *args, **kwargs) -> Any:
    """Convenience function for controller calls"""
    return controller_manager.call_function(function_name, *args, **kwargs)
