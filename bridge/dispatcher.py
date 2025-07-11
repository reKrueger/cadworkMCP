"""
Command dispatcher for bridge operations
"""
from typing import Dict, Any

def dispatch_command(operation: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatch command to appropriate handler"""
    # Import handlers here to avoid circular imports
    from .handlers import element_handlers, geometry_handlers, attribute_handlers, utility_handlers, visualization_handlers
    
    # Map operations to their handlers
    OPERATION_HANDLERS = {
        # Utility operations
        "ping": utility_handlers.handle_ping,
        "get_version_info": utility_handlers.handle_get_version_info,
        "get_model_name": utility_handlers.handle_get_model_name,
        
        # Element operations
        "create_beam": element_handlers.handle_create_beam,
        "create_panel": element_handlers.handle_create_panel,
        "get_active_element_ids": element_handlers.handle_get_active_element_ids,
        "get_all_element_ids": element_handlers.handle_get_all_element_ids,
        "get_visible_element_ids": element_handlers.handle_get_visible_element_ids,
        "get_user_element_ids": element_handlers.handle_get_user_element_ids,
        "get_element_info": element_handlers.handle_get_element_info,
        "delete_elements": element_handlers.handle_delete_elements,
        "copy_elements": element_handlers.handle_copy_elements,
        "move_element": element_handlers.handle_move_element,
        
        # Extended element creation
        "create_circular_beam_points": element_handlers.handle_create_circular_beam_points,
        "create_square_beam_points": element_handlers.handle_create_square_beam_points,
        "create_standard_beam_points": element_handlers.handle_create_standard_beam_points,
        "create_standard_panel_points": element_handlers.handle_create_standard_panel_points,
        "create_drilling_points": element_handlers.handle_create_drilling_points,
        "create_polygon_beam": element_handlers.handle_create_polygon_beam,
        "get_elements_by_type": element_handlers.handle_get_elements_by_type,
        "filter_elements_by_material": element_handlers.handle_filter_elements_by_material,
        "get_elements_in_group": element_handlers.handle_get_elements_in_group,
        "get_element_count_by_type": element_handlers.handle_get_element_count_by_type,
        "get_material_statistics": element_handlers.handle_get_material_statistics,
        "get_group_statistics": element_handlers.handle_get_group_statistics,
        "duplicate_elements": element_handlers.handle_duplicate_elements,
        
        # Geometry operations
        "get_element_width": geometry_handlers.handle_get_element_width,
        "get_element_height": geometry_handlers.handle_get_element_height,
        "get_element_length": geometry_handlers.handle_get_element_length,
        "get_element_volume": geometry_handlers.handle_get_element_volume,
        "get_element_weight": geometry_handlers.handle_get_element_weight,
        "get_element_xl": geometry_handlers.handle_get_element_xl,
        "get_element_yl": geometry_handlers.handle_get_element_yl,
        "get_element_zl": geometry_handlers.handle_get_element_zl,
        "get_element_p1": geometry_handlers.handle_get_element_p1,
        "get_element_p2": geometry_handlers.handle_get_element_p2,
        "get_element_p3": geometry_handlers.handle_get_element_p3,
        "get_center_of_gravity": geometry_handlers.handle_get_center_of_gravity,
        "get_center_of_gravity_for_list": geometry_handlers.handle_get_center_of_gravity_for_list,
        "get_element_vertices": geometry_handlers.handle_get_element_vertices,
        "get_minimum_distance_between_elements": geometry_handlers.handle_get_minimum_distance_between_elements,
        "get_element_facets": geometry_handlers.handle_get_element_facets,
        "get_element_reference_face_area": geometry_handlers.handle_get_element_reference_face_area,
        "get_total_area_of_all_faces": geometry_handlers.handle_get_total_area_of_all_faces,
        "rotate_elements": geometry_handlers.handle_rotate_elements,
        "apply_global_scale": geometry_handlers.handle_apply_global_scale,
        "invert_model": geometry_handlers.handle_invert_model,
        "rotate_height_axis_90": geometry_handlers.handle_rotate_height_axis_90,
        "rotate_length_axis_90": geometry_handlers.handle_rotate_length_axis_90,
        "get_element_type": geometry_handlers.handle_get_element_type,
        "calculate_total_volume": geometry_handlers.handle_calculate_total_volume,
        "calculate_total_weight": geometry_handlers.handle_calculate_total_weight,
        
        # Attribute operations
        "get_standard_attributes": attribute_handlers.handle_get_standard_attributes,
        "get_user_attributes": attribute_handlers.handle_get_user_attributes,
        "list_defined_user_attributes": attribute_handlers.handle_list_defined_user_attributes,
        "set_name": attribute_handlers.handle_set_name,
        "set_material": attribute_handlers.handle_set_material,
        
        # Visualization operations
        "set_color": visualization_handlers.handle_set_color,
        "set_visibility": visualization_handlers.handle_set_visibility,
        "set_transparency": visualization_handlers.handle_set_transparency,
        "get_color": visualization_handlers.handle_get_color,
        "get_transparency": visualization_handlers.handle_get_transparency,
        "show_all_elements": visualization_handlers.handle_show_all_elements,
        "hide_all_elements": visualization_handlers.handle_hide_all_elements,
        "refresh_display": visualization_handlers.handle_refresh_display,
        "get_visible_element_count": visualization_handlers.handle_get_visible_element_count,
        
        # Extended attribute operations
        "set_group": attribute_handlers.handle_set_group,
        "set_comment": attribute_handlers.handle_set_comment,
        "set_subgroup": attribute_handlers.handle_set_subgroup,
    }
    if operation not in OPERATION_HANDLERS:
        return {
            "status": "error", 
            "message": f"Unknown operation: {operation}"
        }
    
    try:
        handler = OPERATION_HANDLERS[operation]
        return handler(args)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Handler error for {operation}: {str(e)}"
        }
