#!/usr/bin/env python3
"""
MCP Tools Audit Script
====================

Analyze all MCP tools and match them with existing tests
"""

import re

# Extract all MCP tools from main.py analysis
mcp_tools = [
    # ELEMENT TOOLS (52 functions)
    "create_beam", "create_panel", "get_active_element_ids", "get_all_element_ids", 
    "get_visible_element_ids", "get_element_info", "delete_elements", "copy_elements", 
    "move_element", "duplicate_elements", "stretch_elements", "scale_elements", 
    "mirror_elements", "create_solid_wood_panel", "get_user_element_ids", 
    "create_circular_beam_points", "create_square_beam_points", "create_standard_beam_points", 
    "create_standard_panel_points", "create_drilling_points", "create_polygon_beam", 
    "get_elements_by_type", "filter_elements_by_material", "get_elements_in_group", 
    "get_elements_by_color", "get_elements_by_layer", "get_elements_by_dimension_range", 
    "get_elements_in_region", "get_element_count_by_type", "get_material_statistics", 
    "get_group_statistics", "join_elements", "unjoin_elements", "cut_corner_lap", 
    "cut_cross_lap", "cut_half_lap", "cut_double_tenon", "cut_scarf_joint", 
    "cut_shoulder", "create_surface", "chamfer_edge", "round_edge", "split_element", 
    "create_beam_from_points", "create_auxiliary_line", "create_auxiliary_beam_points", 
    "convert_beam_to_panel", "convert_panel_to_beam", "convert_auxiliary_to_beam", 
    "create_auto_container_from_standard", "get_container_content_elements",
    
    # GEOMETRY TOOLS (33 functions)
    "get_element_width", "get_element_height", "get_element_length", "get_element_volume", 
    "get_element_weight", "get_element_xl", "get_element_yl", "get_element_zl", 
    "get_element_p1", "get_element_p2", "get_element_p3", "get_center_of_gravity", 
    "get_center_of_gravity_for_list", "calculate_center_of_mass", "get_element_vertices", 
    "get_bounding_box", "get_element_outline", "get_section_outline", "intersect_elements", 
    "subtract_elements", "unite_elements", "project_point_to_element", 
    "get_minimum_distance_between_elements", "get_closest_point_on_element", 
    "get_element_facets", "get_element_reference_face_area", "get_total_area_of_all_faces", 
    "rotate_elements", "apply_global_scale", "invert_model", "rotate_height_axis_90", 
    "rotate_length_axis_90", "get_element_type", "calculate_total_volume", "calculate_total_weight",
    
    # ATTRIBUTE TOOLS (8 functions)
    "get_standard_attributes", "get_user_attributes", "list_defined_user_attributes", 
    "set_name", "set_material", "set_group", "set_comment", "set_subgroup",
    
    # VISUALIZATION TOOLS (10 functions)
    "set_color", "set_visibility", "set_transparency", "get_color", "get_transparency", 
    "show_all_elements", "hide_all_elements", "refresh_display", "get_visible_element_count",
    
    # UTILITY TOOLS (6 functions)
    "disable_auto_display_refresh", "enable_auto_display_refresh", "print_error", 
    "print_warning", "get_3d_file_path", "get_project_data", "get_cadwork_version_info",
    
    # SHOP DRAWING TOOLS (4 functions)
    "add_wall_section_x", "add_wall_section_y", "add_wall_section_vertical", "export_2d_wireframe",
    
    # ROOF TOOLS (2 functions)
    "get_roof_surfaces", "calculate_roof_area",
    
    # MACHINE TOOLS (1 function)
    "check_production_list_discrepancies",
    
    # MEASUREMENT TOOLS (3 functions)
    "measure_distance", "measure_angle", "measure_area",
    
    # MATERIAL TOOLS (3 functions)
    "create_material", "get_material_properties", "list_available_materials",
    
    # EXPORT TOOLS (24 functions)
    "export_to_btl", "export_element_list", "export_to_ifc", "export_to_dxf", 
    "export_workshop_drawings", "export_to_step", "export_to_3dm", "export_to_obj", 
    "export_to_ply", "export_to_stl", "export_to_gltf", "export_to_x3d", 
    "export_production_data", "export_to_fbx", "export_to_webgl", "export_to_sat", 
    "export_to_dstv", "export_step_with_drillings", "export_btl_for_nesting", 
    "export_cutting_list",
    
    # IMPORT TOOLS (4 functions)
    "import_from_step", "import_from_sat", "import_from_rhino", "import_from_btl"
]

# Group by controller
tools_by_controller = {
    'element': [
        "create_beam", "create_panel", "get_active_element_ids", "get_all_element_ids", 
        "get_visible_element_ids", "get_element_info", "delete_elements", "copy_elements", 
        "move_element", "duplicate_elements", "stretch_elements", "scale_elements", 
        "mirror_elements", "create_solid_wood_panel", "get_user_element_ids", 
        "create_circular_beam_points", "create_square_beam_points", "create_standard_beam_points", 
        "create_standard_panel_points", "create_drilling_points", "create_polygon_beam", 
        "get_elements_by_type", "filter_elements_by_material", "get_elements_in_group", 
        "get_elements_by_color", "get_elements_by_layer", "get_elements_by_dimension_range", 
        "get_elements_in_region", "get_element_count_by_type", "get_material_statistics", 
        "get_group_statistics", "join_elements", "unjoin_elements", "cut_corner_lap", 
        "cut_cross_lap", "cut_half_lap", "cut_double_tenon", "cut_scarf_joint", 
        "cut_shoulder", "create_surface", "chamfer_edge", "round_edge", "split_element", 
        "create_beam_from_points", "create_auxiliary_line", "create_auxiliary_beam_points", 
        "convert_beam_to_panel", "convert_panel_to_beam", "convert_auxiliary_to_beam", 
        "create_auto_container_from_standard", "get_container_content_elements"
    ],
    'geometry': [
        "get_element_width", "get_element_height", "get_element_length", "get_element_volume", 
        "get_element_weight", "get_element_xl", "get_element_yl", "get_element_zl", 
        "get_element_p1", "get_element_p2", "get_element_p3", "get_center_of_gravity", 
        "get_center_of_gravity_for_list", "calculate_center_of_mass", "get_element_vertices", 
        "get_bounding_box", "get_element_outline", "get_section_outline", "intersect_elements", 
        "subtract_elements", "unite_elements", "project_point_to_element", 
        "get_minimum_distance_between_elements", "get_closest_point_on_element", 
        "get_element_facets", "get_element_reference_face_area", "get_total_area_of_all_faces", 
        "rotate_elements", "apply_global_scale", "invert_model", "rotate_height_axis_90", 
        "rotate_length_axis_90", "get_element_type", "calculate_total_volume", "calculate_total_weight"
    ],
    'attribute': [
        "get_standard_attributes", "get_user_attributes", "list_defined_user_attributes", 
        "set_name", "set_material", "set_group", "set_comment", "set_subgroup"
    ],
    'visualization': [
        "set_color", "set_visibility", "set_transparency", "get_color", "get_transparency", 
        "show_all_elements", "hide_all_elements", "refresh_display", "get_visible_element_count"
    ],
    'utility': [
        "disable_auto_display_refresh", "enable_auto_display_refresh", "print_error", 
        "print_warning", "get_3d_file_path", "get_project_data", "get_cadwork_version_info"
    ],
    'shop_drawing': [
        "add_wall_section_x", "add_wall_section_y", "add_wall_section_vertical", "export_2d_wireframe"
    ],
    'roof': [
        "get_roof_surfaces", "calculate_roof_area"
    ],
    'machine': [
        "check_production_list_discrepancies"
    ],
    'measurement': [
        "measure_distance", "measure_angle", "measure_area"
    ],
    'material': [
        "create_material", "get_material_properties", "list_available_materials"
    ],
    'export': [
        "export_to_btl", "export_element_list", "export_to_ifc", "export_to_dxf", 
        "export_workshop_drawings", "export_to_step", "export_to_3dm", "export_to_obj", 
        "export_to_ply", "export_to_stl", "export_to_gltf", "export_to_x3d", 
        "export_production_data", "export_to_fbx", "export_to_webgl", "export_to_sat", 
        "export_to_dstv", "export_step_with_drillings", "export_btl_for_nesting", 
        "export_cutting_list"
    ],
    'import': [
        "import_from_step", "import_from_sat", "import_from_rhino", "import_from_btl"
    ]
}

print("=== MCP TOOLS AUDIT ===")
print(f"Total MCP Tools Found: {len(mcp_tools)}")
print()

for controller, tools in tools_by_controller.items():
    print(f"{controller.upper()} CONTROLLER: {len(tools)} tools")
    for i, tool in enumerate(tools, 1):
        print(f"  {i:2d}. {tool}")
    print()

print("=== SUMMARY BY CONTROLLER ===")
total_tools = 0
for controller, tools in tools_by_controller.items():
    count = len(tools)
    total_tools += count
    print(f"{controller:15} {count:3d} tools")

print(f"{'='*25}")
print(f"{'TOTAL':15} {total_tools:3d} tools")
