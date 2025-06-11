"""
Command dispatcher for bridge operations
"""
from typing import Dict, Any

def dispatch_command(operation: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatch command to appropriate handler"""
    # Import handlers here to avoid circular imports
    from .handlers import element_handlers, geometry_handlers, attribute_handlers, utility_handlers
    
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
        
        # Attribute operations
        "get_standard_attributes": attribute_handlers.handle_get_standard_attributes,
        "get_user_attributes": attribute_handlers.handle_get_user_attributes,
        "list_defined_user_attributes": attribute_handlers.handle_list_defined_user_attributes,
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
