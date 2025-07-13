"""
New clean Cadwork MCP Server
"""
import os
from core.server import create_mcp_server
from core.logging import get_logger
from controllers.element_controller import ElementController
from controllers.geometry_controller import GeometryController
from controllers.attribute_controller import AttributeController
from controllers.visualization_controller import CVisualizationController
from controllers.utility_controller import CUtilityController
from controllers.shop_drawing_controller import CShopDrawingController
from controllers.roof_controller import CRoofController
from controllers.machine_controller import CMachineController

# Create MCP server
mcp = create_mcp_server()

# Initialize controllers
element_ctrl = ElementController()
geometry_ctrl = GeometryController()
attribute_ctrl = AttributeController()
visualization_ctrl = CVisualizationController()
utility_ctrl = CUtilityController()
shop_drawing_ctrl = CShopDrawingController()
roof_ctrl = CRoofController()
machine_ctrl = CMachineController()

# --- ELEMENT TOOLS ---

@mcp.tool(
    name="create_beam",
    description="Creates a rectangular beam element. Requires start point p1 ([x,y,z]), end point p2 ([x,y,z]), width, and height. Optional orientation point p3 ([x,y,z])."
)
async def create_beam(p1: list, p2: list, width: float, height: float, p3: list = None) -> dict:
    return await element_ctrl.create_beam(p1, p2, width, height, p3)

@mcp.tool(
    name="create_panel", 
    description="Creates a rectangular panel element. Requires start point p1 ([x,y,z]), end point p2 ([x,y,z]), width, and thickness. Optional orientation point p3 ([x,y,z])."
)
async def create_panel(p1: list, p2: list, width: float, thickness: float, p3: list = None) -> dict:
    return await element_ctrl.create_panel(p1, p2, width, thickness, p3)

@mcp.tool(
    name="get_active_element_ids",
    description="Retrieves a list of integer IDs for all elements currently active (selected) in Cadwork 3D."
)
async def get_active_element_ids() -> dict:
    return await element_ctrl.get_active_element_ids()

@mcp.tool(
    name="get_all_element_ids", 
    description="Retrieves a list of integer IDs for ALL elements in the Cadwork 3D model, regardless of selection or visibility state."
)
async def get_all_element_ids() -> dict:
    return await element_ctrl.get_all_element_ids()

@mcp.tool(
    name="get_visible_element_ids",
    description="Retrieves a list of integer IDs for all elements that are currently visible in the Cadwork 3D viewport."
)
async def get_visible_element_ids() -> dict:
    return await element_ctrl.get_visible_element_ids()

@mcp.tool(
    name="get_element_info",
    description="Retrieves detailed geometric information and common attributes for a specific Cadwork element."
)
async def get_element_info(element_id: int) -> dict:
    return await element_ctrl.get_element_info(element_id)

@mcp.tool(
    name="delete_elements",
    description="Deletes a list of elements from the Cadwork 3D model. Takes a list of element IDs to delete. This operation cannot be undone."
)
async def delete_elements(element_ids: list) -> dict:
    return await element_ctrl.delete_elements(element_ids)

@mcp.tool(
    name="copy_elements", 
    description="Copies elements with a vector offset. Takes element IDs list and copy_vector [x,y,z]. Returns new element IDs of the copied elements."
)
async def copy_elements(element_ids: list, copy_vector: list) -> dict:
    return await element_ctrl.copy_elements(element_ids, copy_vector)

@mcp.tool(
    name="move_element",
    description="Moves elements by a vector offset. Takes element IDs list and move_vector [x,y,z]. Modifies the original elements in place."
)
async def move_element(element_ids: list, move_vector: list) -> dict:
    return await element_ctrl.move_element(element_ids, move_vector)

@mcp.tool(
    name="duplicate_elements",
    description="Duplicates elements at the same location (no offset). Takes element IDs and returns new element IDs of duplicated elements."
)
async def duplicate_elements(element_ids: list) -> dict:
    return await element_ctrl.duplicate_elements(element_ids)

@mcp.tool(
    name="get_user_element_ids", 
    description="Prompts user to select elements in Cadwork 3D and returns their IDs. Optional count parameter limits selection to specific number of elements."
)
async def get_user_element_ids(count: int = None) -> dict:
    return await element_ctrl.get_user_element_ids(count)

# --- EXTENDED ELEMENT CREATION TOOLS ---

@mcp.tool(
    name="create_circular_beam_points",
    description="Creates a circular beam element using points. Requires diameter, start point p1 ([x,y,z]), end point p2 ([x,y,z]), and optional orientation point p3 ([x,y,z])."
)
async def create_circular_beam_points(diameter: float, p1: list, p2: list, p3: list = None) -> dict:
    return await element_ctrl.create_circular_beam_points(diameter, p1, p2, p3)

@mcp.tool(
    name="create_square_beam_points", 
    description="Creates a square beam element using points. Requires width, start point p1 ([x,y,z]), end point p2 ([x,y,z]), and optional orientation point p3 ([x,y,z])."
)
async def create_square_beam_points(width: float, p1: list, p2: list, p3: list = None) -> dict:
    return await element_ctrl.create_square_beam_points(width, p1, p2, p3)

@mcp.tool(
    name="create_standard_beam_points",
    description="Creates a standard beam element using points from Cadwork library. Requires standard_element_name, start point p1 ([x,y,z]), end point p2 ([x,y,z]), and optional orientation point p3 ([x,y,z])."
)
async def create_standard_beam_points(standard_element_name: str, p1: list, p2: list, p3: list = None) -> dict:
    return await element_ctrl.create_standard_beam_points(standard_element_name, p1, p2, p3)

@mcp.tool(
    name="create_standard_panel_points",
    description="Creates a standard panel element using points from Cadwork library. Requires standard_element_name, start point p1 ([x,y,z]), end point p2 ([x,y,z]), and optional orientation point p3 ([x,y,z])."
)
async def create_standard_panel_points(standard_element_name: str, p1: list, p2: list, p3: list = None) -> dict:
    return await element_ctrl.create_standard_panel_points(standard_element_name, p1, p2, p3)

@mcp.tool(
    name="create_drilling_points",
    description="Creates a drilling element using points. Requires diameter and start point p1 ([x,y,z]), end point p2 ([x,y,z])."
)
async def create_drilling_points(diameter: float, p1: list, p2: list) -> dict:
    return await element_ctrl.create_drilling_points(diameter, p1, p2)

@mcp.tool(
    name="create_polygon_beam",
    description="Creates a polygon beam element. Requires polygon_vertices (list of [x,y,z] points), thickness, xl vector ([x,y,z] length direction), and zl vector ([x,y,z] height direction)."
)
async def create_polygon_beam(polygon_vertices: list, thickness: float, xl: list, zl: list) -> dict:
    return await element_ctrl.create_polygon_beam(polygon_vertices, thickness, xl, zl)

# --- ELEMENT QUERY/FILTER TOOLS ---

@mcp.tool(
    name="get_elements_by_type",
    description="Finds all elements of a specific type in the model. Takes element_type string ('beam', 'panel', 'drilling', etc.) and returns list of matching element IDs."
)
async def get_elements_by_type(element_type: str) -> dict:
    return await element_ctrl.get_elements_by_type(element_type)

@mcp.tool(
    name="filter_elements_by_material",
    description="Filters all elements by material name. Takes material_name string and returns list of element IDs with that material."
)
async def filter_elements_by_material(material_name: str) -> dict:
    return await element_ctrl.filter_elements_by_material(material_name)

@mcp.tool(
    name="get_elements_in_group",
    description="Finds all elements in a specific group. Takes group_name string and returns list of element IDs in that group."
)
async def get_elements_in_group(group_name: str) -> dict:
    return await element_ctrl.get_elements_in_group(group_name)

@mcp.tool(
    name="get_element_count_by_type",
    description="Gets count statistics of all elements by type in the model. Returns total counts and percentages for each element type."
)
async def get_element_count_by_type() -> dict:
    return await element_ctrl.get_element_count_by_type()

@mcp.tool(
    name="get_material_statistics",
    description="Gets material usage statistics for the entire model. Returns counts and percentages for each material used."
)
async def get_material_statistics() -> dict:
    return await element_ctrl.get_material_statistics()

@mcp.tool(
    name="get_group_statistics",
    description="Gets group usage statistics for the entire model. Returns counts and percentages for each group used."
)
async def get_group_statistics() -> dict:
    return await element_ctrl.get_group_statistics()

@mcp.tool(
    name="join_elements",
    description="Joins multiple elements together. Takes a list of element IDs (minimum 2 elements) to create connections between them."
)
async def join_elements(element_ids: list) -> dict:
    return await element_ctrl.join_elements(element_ids)

@mcp.tool(
    name="unjoin_elements", 
    description="Unjoins/disconnects previously joined elements. Takes a list of element IDs to remove their connections."
)
async def unjoin_elements(element_ids: list) -> dict:
    return await element_ctrl.unjoin_elements(element_ids)

@mcp.tool(
    name="cut_corner_lap",
    description="Creates corner lap cuts between elements for wood connections. Takes element IDs (minimum 2) and optional cut parameters (depth, width, etc.)."
)
async def cut_corner_lap(element_ids: list, cut_params: dict = None) -> dict:
    return await element_ctrl.cut_corner_lap(element_ids, cut_params)

@mcp.tool(
    name="cut_cross_lap", 
    description="Creates cross lap cuts between elements for wood connections. Takes element IDs (minimum 2) and optional cut parameters (depth, width, position, etc.)."
)
async def cut_cross_lap(element_ids: list, cut_params: dict = None) -> dict:
    return await element_ctrl.cut_cross_lap(element_ids, cut_params)

@mcp.tool(
    name="cut_half_lap",
    description="Creates half lap cuts between elements. One element is cut to half its thickness while the other is cut completely. Takes element IDs (minimum 2) and optional cut parameters."
)
async def cut_half_lap(element_ids: list, cut_params: dict = None) -> dict:
    return await element_ctrl.cut_half_lap(element_ids, cut_params)

@mcp.tool(
    name="cut_double_tenon",
    description="Creates double tenon and mortise connections between exactly 2 elements. Creates two parallel tenons on one element and corresponding mortises on the other."
)
async def cut_double_tenon(element_ids: list, cut_params: dict = None) -> dict:
    return await element_ctrl.cut_double_tenon(element_ids, cut_params)

@mcp.tool(
    name="cut_scarf_joint",
    description="Creates scarf joint connections between exactly 2 elements for beam extensions or seamless connections. Takes scarf type, length, angle parameters."
)
async def cut_scarf_joint(element_ids: list, cut_params: dict = None) -> dict:
    return await element_ctrl.cut_scarf_joint(element_ids, cut_params)

@mcp.tool(
    name="cut_shoulder",
    description="Creates shoulder cuts between elements for load-bearing connections. One element supports another with a shoulder cut. Takes depth, width, type parameters."
)
async def cut_shoulder(element_ids: list, cut_params: dict = None) -> dict:
    return await element_ctrl.cut_shoulder(element_ids, cut_params)

# --- GEOMETRY TOOLS ---

@mcp.tool(
    name="get_element_width",
    description="Retrieves the width of a specific Cadwork element in millimeters."
)
async def get_element_width(element_id: int) -> dict:
    return await geometry_ctrl.get_element_width(element_id)

@mcp.tool(
    name="get_element_height", 
    description="Retrieves the height of a specific Cadwork element in millimeters."
)
async def get_element_height(element_id: int) -> dict:
    return await geometry_ctrl.get_element_height(element_id)

@mcp.tool(
    name="get_element_length",
    description="Retrieves the length of a specific Cadwork element in millimeters."
)
async def get_element_length(element_id: int) -> dict:
    return await geometry_ctrl.get_element_length(element_id)

@mcp.tool(
    name="get_element_volume",
    description="Retrieves the volume of a specific Cadwork element in cubic millimeters."
)
async def get_element_volume(element_id: int) -> dict:
    return await geometry_ctrl.get_element_volume(element_id)

@mcp.tool(
    name="get_element_weight",
    description="Retrieves the weight of a specific Cadwork element in kilograms."
)
async def get_element_weight(element_id: int) -> dict:
    return await geometry_ctrl.get_element_weight(element_id)

# --- GEOMETRY VECTORS & POINTS ---

@mcp.tool(
    name="get_element_xl",
    description="Retrieves the XL vector (length direction) of a Cadwork element as [x,y,z]. This defines the element's length axis orientation."
)
async def get_element_xl(element_id: int) -> dict:
    return await geometry_ctrl.get_element_xl(element_id)

@mcp.tool(
    name="get_element_yl", 
    description="Retrieves the YL vector (width direction) of a Cadwork element as [x,y,z]. This defines the element's width axis orientation."
)
async def get_element_yl(element_id: int) -> dict:
    return await geometry_ctrl.get_element_yl(element_id)

@mcp.tool(
    name="get_element_zl",
    description="Retrieves the ZL vector (height direction) of a Cadwork element as [x,y,z]. This defines the element's height axis orientation."
)
async def get_element_zl(element_id: int) -> dict:
    return await geometry_ctrl.get_element_zl(element_id)

@mcp.tool(
    name="get_element_p1",
    description="Retrieves the P1 point (start point) of a Cadwork element as [x,y,z] coordinates in mm."
)
async def get_element_p1(element_id: int) -> dict:
    return await geometry_ctrl.get_element_p1(element_id)

@mcp.tool(
    name="get_element_p2",
    description="Retrieves the P2 point (end point) of a Cadwork element as [x,y,z] coordinates in mm."
)
async def get_element_p2(element_id: int) -> dict:
    return await geometry_ctrl.get_element_p2(element_id)

@mcp.tool(
    name="get_element_p3",
    description="Retrieves the P3 point (orientation point) of a Cadwork element as [x,y,z] coordinates in mm. Defines the element's local coordinate system."
)
async def get_element_p3(element_id: int) -> dict:
    return await geometry_ctrl.get_element_p3(element_id)

@mcp.tool(
    name="get_center_of_gravity",
    description="Retrieves the center of gravity (centroid) of a single Cadwork element as [x,y,z] coordinates in mm."
)
async def get_center_of_gravity(element_id: int) -> dict:
    return await geometry_ctrl.get_center_of_gravity(element_id)

@mcp.tool(
    name="get_center_of_gravity_for_list",
    description="Retrieves the combined center of gravity for multiple Cadwork elements as [x,y,z] coordinates in mm."
)
async def get_center_of_gravity_for_list(element_ids: list) -> dict:
    return await geometry_ctrl.get_center_of_gravity_for_list(element_ids)

@mcp.tool(
    name="get_element_vertices",
    description="Retrieves all corner points (vertices) of a Cadwork element as list of [x,y,z] coordinates in mm."
)
async def get_element_vertices(element_id: int) -> dict:
    return await geometry_ctrl.get_element_vertices(element_id)

# --- GEOMETRY ANALYSIS ---

@mcp.tool(
    name="get_minimum_distance_between_elements",
    description="Calculates the minimum distance between two Cadwork elements in mm. Useful for collision detection and clearance checks."
)
async def get_minimum_distance_between_elements(first_element_id: int, second_element_id: int) -> dict:
    return await geometry_ctrl.get_minimum_distance_between_elements(first_element_id, second_element_id)

@mcp.tool(
    name="get_element_facets",
    description="Retrieves all facets (faces) of a Cadwork element. Returns geometric face data for detailed mesh analysis."
)
async def get_element_facets(element_id: int) -> dict:
    return await geometry_ctrl.get_element_facets(element_id)

@mcp.tool(
    name="get_element_reference_face_area", 
    description="Retrieves the reference face area of a Cadwork element in mm². This is typically the main face used for calculations."
)
async def get_element_reference_face_area(element_id: int) -> dict:
    return await geometry_ctrl.get_element_reference_face_area(element_id)

@mcp.tool(
    name="get_total_area_of_all_faces",
    description="Retrieves the total surface area of all faces of a Cadwork element in mm². Useful for material calculations."
)
async def get_total_area_of_all_faces(element_id: int) -> dict:
    return await geometry_ctrl.get_total_area_of_all_faces(element_id)

# --- GEOMETRY TRANSFORMATIONS ---

@mcp.tool(
    name="rotate_elements",
    description="Rotates elements around a specified axis. Takes element IDs, origin point [x,y,z], rotation axis vector [x,y,z], and angle in degrees."
)
async def rotate_elements(element_ids: list, origin: list, rotation_axis: list, rotation_angle: float) -> dict:
    return await geometry_ctrl.rotate_elements(element_ids, origin, rotation_axis, rotation_angle)

@mcp.tool(
    name="apply_global_scale",
    description="Applies global scaling to elements. Takes element IDs, scale factor (e.g., 2.0 = double size), and origin point [x,y,z] for scaling."
)
async def apply_global_scale(element_ids: list, scale: float, origin: list) -> dict:
    return await geometry_ctrl.apply_global_scale(element_ids, scale, origin)

@mcp.tool(
    name="invert_model",
    description="Inverts/mirrors elements. This flips the element geometry. Useful for creating mirrored versions."
)
async def invert_model(element_ids: list) -> dict:
    return await geometry_ctrl.invert_model(element_ids)

@mcp.tool(
    name="rotate_height_axis_90",
    description="Rotates the height axis of elements by exactly 90 degrees. Quick rotation for standard orientations."
)
async def rotate_height_axis_90(element_ids: list) -> dict:
    return await geometry_ctrl.rotate_height_axis_90(element_ids)

@mcp.tool(
    name="rotate_length_axis_90", 
    description="Rotates the length axis of elements by exactly 90 degrees. Quick rotation for standard orientations."
)
async def rotate_length_axis_90(element_ids: list) -> dict:
    return await geometry_ctrl.rotate_length_axis_90(element_ids)

@mcp.tool(
    name="get_element_type",
    description="Retrieves the type of a Cadwork element (beam, panel, drilling, etc.). Takes element ID and returns type information."
)
async def get_element_type(element_id: int) -> dict:
    return await geometry_ctrl.get_element_type(element_id)

# --- GEOMETRY CALCULATIONS ---

@mcp.tool(
    name="calculate_total_volume",
    description="Calculates the total volume of a list of elements. Takes element IDs and returns total volume in multiple units (mm³, cm³, dm³, m³)."
)
async def calculate_total_volume(element_ids: list) -> dict:
    return await geometry_ctrl.calculate_total_volume(element_ids)

@mcp.tool(
    name="calculate_total_weight",
    description="Calculates the total weight of a list of elements. Takes element IDs and returns total weight in multiple units (g, kg, t)."
)
async def calculate_total_weight(element_ids: list) -> dict:
    return await geometry_ctrl.calculate_total_weight(element_ids)

# --- ATTRIBUTE TOOLS ---

@mcp.tool(
    name="get_standard_attributes",
    description="Retrieves common standard attributes (name, group, subgroup, material, comment) for a list of element IDs."
)
async def get_standard_attributes(element_ids: list) -> dict:
    return await attribute_ctrl.get_standard_attributes(element_ids)

@mcp.tool(
    name="get_user_attributes", 
    description="Retrieves specific user-defined attributes for a list of element IDs."
)
async def get_user_attributes(element_ids: list, attribute_numbers: list) -> dict:
    return await attribute_ctrl.get_user_attributes(element_ids, attribute_numbers)

@mcp.tool(
    name="list_defined_user_attributes",
    description="Retrieves a list of all user-defined attribute numbers that have names configured."
)
async def list_defined_user_attributes() -> dict:
    return await attribute_ctrl.list_defined_user_attributes()

# --- ATTRIBUTE SETTER TOOLS ---

@mcp.tool(
    name="set_name",
    description="Sets the name for a list of elements. Takes element IDs and the name string to set."
)
async def set_name(element_ids: list, name: str) -> dict:
    return await attribute_ctrl.set_name(element_ids, name)

@mcp.tool(
    name="set_material",
    description="Sets the material for a list of elements. Takes element IDs and the material name string to set."
)
async def set_material(element_ids: list, material: str) -> dict:
    return await attribute_ctrl.set_material(element_ids, material)

# --- VISUALIZATION TOOLS ---

@mcp.tool(
    name="set_color",
    description="Sets the color for a list of elements. Takes element IDs and color_id (1-255 from Cadwork color palette)."
)
async def set_color(element_ids: list, color_id: int) -> dict:
    return await visualization_ctrl.set_color(element_ids, color_id)

@mcp.tool(
    name="set_visibility", 
    description="Sets the visibility for a list of elements. Takes element IDs and visible flag (True=show, False=hide)."
)
async def set_visibility(element_ids: list, visible: bool) -> dict:
    return await visualization_ctrl.set_visibility(element_ids, visible)

@mcp.tool(
    name="set_transparency",
    description="Sets the transparency for a list of elements. Takes element IDs and transparency value (0-100, 0=opaque, 100=fully transparent)."
)
async def set_transparency(element_ids: list, transparency: int) -> dict:
    return await visualization_ctrl.set_transparency(element_ids, transparency)

# --- VISUALIZATION GETTERS ---

@mcp.tool(
    name="get_color",
    description="Gets the color of an element. Takes element ID and returns color information (color_id and color_name)."
)
async def get_color(element_id: int) -> dict:
    return await visualization_ctrl.get_color(element_id)

@mcp.tool(
    name="get_transparency",
    description="Gets the transparency of an element. Takes element ID and returns transparency value (0-100) and opacity info."
)
async def get_transparency(element_id: int) -> dict:
    return await visualization_ctrl.get_transparency(element_id)

# --- GLOBAL VISIBILITY TOOLS ---

@mcp.tool(
    name="show_all_elements",
    description="Makes all elements in the model visible. No parameters needed. Returns count of elements made visible."
)
async def show_all_elements() -> dict:
    return await visualization_ctrl.show_all_elements()

@mcp.tool(
    name="hide_all_elements",
    description="Hides all elements in the model. No parameters needed. Returns count of elements hidden."
)
async def hide_all_elements() -> dict:
    return await visualization_ctrl.hide_all_elements()

# --- DISPLAY MANAGEMENT TOOLS ---

@mcp.tool(
    name="refresh_display",
    description="Refreshes the display/viewport after changes. No parameters needed. Important for updating view after many operations."
)
async def refresh_display() -> dict:
    return await visualization_ctrl.refresh_display()

@mcp.tool(
    name="get_visible_element_count",
    description="Gets count of currently visible elements in the model. Returns visibility statistics and percentages."
)
async def get_visible_element_count() -> dict:
    return await visualization_ctrl.get_visible_element_count()

# --- EXTENDED ATTRIBUTE TOOLS ---

@mcp.tool(
    name="set_group",
    description="Sets the group for a list of elements. Takes element IDs and group name string."
)
async def set_group(element_ids: list, group: str) -> dict:
    return await attribute_ctrl.set_group(element_ids, group)

@mcp.tool(
    name="set_comment",
    description="Sets the comment for a list of elements. Takes element IDs and comment text string."
)
async def set_comment(element_ids: list, comment: str) -> dict:
    return await attribute_ctrl.set_comment(element_ids, comment)

@mcp.tool(
    name="set_subgroup",
    description="Sets the subgroup for a list of elements. Takes element IDs and subgroup name string."
)
async def set_subgroup(element_ids: list, subgroup: str) -> dict:
    return await attribute_ctrl.set_subgroup(element_ids, subgroup)

# --- UTILITY TOOLS ---

@mcp.tool(
    name="disable_auto_display_refresh",
    description="Disables automatic display refresh for performance during batch operations. Important: Remember to enable it again afterwards."
)
async def disable_auto_display_refresh() -> dict:
    return await utility_ctrl.disable_auto_display_refresh()

@mcp.tool(
    name="enable_auto_display_refresh", 
    description="Re-enables automatic display refresh after batch operations. Should be called after disable_auto_display_refresh()."
)
async def enable_auto_display_refresh() -> dict:
    return await utility_ctrl.enable_auto_display_refresh()

@mcp.tool(
    name="print_error",
    description="Displays an error message in Cadwork. Takes a message string to show in the Cadwork interface."
)
async def print_error(message: str) -> dict:
    return await utility_ctrl.print_error(message)

@mcp.tool(
    name="print_warning",
    description="Displays a warning message in Cadwork. Takes a message string to show in the Cadwork interface."
)
async def print_warning(message: str) -> dict:
    return await utility_ctrl.print_warning(message)

@mcp.tool(
    name="get_3d_file_path",
    description="Retrieves the file path of the currently opened 3D file in Cadwork. Returns file path and file information."
)
async def get_3d_file_path() -> dict:
    return await utility_ctrl.get_3d_file_path()

@mcp.tool(
    name="get_project_data", 
    description="Retrieves general project data and metadata from the current Cadwork project. Returns project information like name, path, etc."
)
async def get_project_data() -> dict:
    return await utility_ctrl.get_project_data()

# --- VERSION TOOL ---

@mcp.tool(
    name="get_cadwork_version_info",
    description="Retrieves version information from the connected Cadwork application."
)
async def get_cadwork_version_info() -> dict:
    from core.connection import get_connection
    try:
        connection = get_connection()
        return connection.send_command("get_version_info")
    except Exception as e:
        return {"status": "error", "message": f"Failed to get version info: {e}"}

@mcp.tool(
    name="create_auxiliary_beam_points",
    description="Creates an auxiliary beam element using points. Auxiliary elements are used for construction purposes and can be converted to regular beams later. Requires start point p1 ([x,y,z]), end point p2 ([x,y,z]), and optional orientation point p3 ([x,y,z])."
)
async def create_auxiliary_beam_points(p1: list, p2: list, p3: list = None) -> dict:
    return await element_ctrl.create_auxiliary_beam_points(p1, p2, p3)

@mcp.tool(
    name="convert_beam_to_panel", 
    description="Converts beam elements to panel elements. The geometry is adjusted accordingly - width becomes thickness, height becomes width of the resulting panel. Takes a list of element IDs to convert."
)
async def convert_beam_to_panel(element_ids: list) -> dict:
    return await element_ctrl.convert_beam_to_panel(element_ids)

@mcp.tool(
    name="convert_panel_to_beam",
    description="Converts panel elements to beam elements. The geometry is adjusted accordingly - thickness becomes width, width becomes height of the resulting beam. Takes a list of element IDs to convert."
)
async def convert_panel_to_beam(element_ids: list) -> dict:
    return await element_ctrl.convert_panel_to_beam(element_ids)

@mcp.tool(
    name="convert_auxiliary_to_beam",
    description="Converts auxiliary elements to regular beam elements. Auxiliary elements become full-featured beams while preserving their geometry. Takes a list of auxiliary element IDs to convert."
)
async def convert_auxiliary_to_beam(element_ids: list) -> dict:
    return await element_ctrl.convert_auxiliary_to_beam(element_ids)

@mcp.tool(
    name="create_auto_container_from_standard",
    description="Creates an automatic container from standard elements. Containers are groups that organize multiple elements together. Useful for complex structures and assemblies. Takes element IDs and container name."
)
async def create_auto_container_from_standard(element_ids: list, container_name: str) -> dict:
    return await element_ctrl.create_auto_container_from_standard(element_ids, container_name)

@mcp.tool(
    name="get_container_content_elements", 
    description="Retrieves all elements contained within a specific container. Returns list of element IDs and detailed information about each contained element. Takes container ID."
)
async def get_container_content_elements(container_id: int) -> dict:
    return await element_ctrl.get_container_content_elements(container_id)

@mcp.tool(
    name="add_wall_section_x",
    description="Adds a wall section in X-direction for technical drawings. Creates cross-sectional views parallel to X-axis for workshop drawings. Takes wall element ID and optional section parameters (position, depth, display options)."
)
async def add_wall_section_x(wall_id: int, section_params: dict = None) -> dict:
    return await shop_drawing_ctrl.add_wall_section_x(wall_id, section_params)

@mcp.tool(
    name="add_wall_section_y", 
    description="Adds a wall section in Y-direction for technical drawings. Creates cross-sectional views parallel to Y-axis for workshop drawings. Takes wall element ID and optional section parameters (position, depth, display options)."
)
async def add_wall_section_y(wall_id: int, section_params: dict = None) -> dict:
    return await shop_drawing_ctrl.add_wall_section_y(wall_id, section_params)

@mcp.tool(
    name="get_roof_surfaces",
    description="Retrieves roof surface information for specified elements. Analyzes roof elements and returns detailed information about roof surfaces, slopes, orientations and geometric properties. Takes list of element IDs to analyze as roof elements."
)
async def get_roof_surfaces(element_ids: list) -> dict:
    return await roof_ctrl.get_roof_surfaces(element_ids)

@mcp.tool(
    name="calculate_roof_area",
    description="Calculates total roof area for specified roof elements. Performs specialized roof area calculations considering slopes, overhangs and complex roof geometries. Takes list of roof element IDs for area calculation."
)
async def calculate_roof_area(roof_element_ids: list) -> dict:
    return await roof_ctrl.calculate_roof_area(roof_element_ids)

@mcp.tool(
    name="check_production_list_discrepancies",
    description="Checks production lists for discrepancies and conflicts. Analyzes production lists for potential issues like missing elements, inconsistent dimensions, material errors or CNC machining conflicts. Essential for quality-assured manufacturing. Takes production list ID."
)
async def check_production_list_discrepancies(production_list_id: int) -> dict:
    return await machine_ctrl.check_production_list_discrepancies(production_list_id)

if __name__ == "__main__":
    import argparse
    logger = get_logger()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Cadwork MCP Server")
    parser.add_argument("script_name", nargs='?', help="Script name (ignored)")
    parser.add_argument("--transport", choices=["stdio", "http"], default="stdio", 
                       help="Transport protocol to use")
    parser.add_argument("--port", type=int, default=8001, 
                       help="Port for HTTP transport")
    parser.add_argument("--host", default="localhost", 
                       help="Host for HTTP transport")
    
    args = parser.parse_args()
    
    if args.transport == "http":
        logger.info(f"Starting Cadwork MCP Server with HTTP transport on {args.host}:{args.port}...")
        try:
            # Use uvicorn for HTTP transport
            import uvicorn
            uvicorn.run(mcp, host=args.host, port=args.port)
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server failed: {e}")
            import sys
            sys.exit(1)
    else:
        logger.info("Starting Cadwork MCP Server with stdio transport...")
        try:
            mcp.run(transport='stdio')
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server failed: {e}")
            import sys
            sys.exit(1)
