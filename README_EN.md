# Cadwork MCP Server

A **Model Context Protocol (MCP) Server** for Cadwork 3D software that enables Claude and other AI assistants to interact directly with Cadwork 3D.

## 🚀 Installation

### 1. Prerequisites
- **Python 3.8+** installed
- **Cadwork 3D** software
- **Claude Desktop** application

### 2. Clone repository and install dependencies
⚠️ **IMPORTANT:** Project MUST be located on C: drive: `C:\cadworkMCP`

```bash
git clone <repository-url> C:\cadworkMCP
cd C:\cadworkMCP
pip install -r requirements.txt
```

### 3. Setup Cadwork Bridge
Copy the `bridge` folder to the Cadwork API directory:
```
C:\Program Files\cadwork\<version>\API.x64\
```

### 4. Configure Claude Desktop

Add MCP configuration to Claude Desktop config.json:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

Add the following configuration:
```json
{
  "mcpServers": {
    "cadwork": {
      "command": "python",
      "args": ["C:\\cadworkMCP\\main.py"],
      "env": {}
    }
  }
}
```

### 5. Server starts automatically
The MCP server is automatically started by Claude Desktop when you chat with Claude.
No manual start required! 🚀

## 📋 Function Status

### ✅ Element Operations (54 Functions)
- **Creation:** `create_beam`, `create_panel`, `create_surface`, `create_beam_from_points`, `create_auxiliary_line`, `create_circular_beam_points`, `create_square_beam_points`, `create_standard_beam_points`, `create_standard_panel_points`, `create_drilling_points`, `create_polygon_beam`, `create_auxiliary_beam_points`, `create_solid_wood_panel`
- **Queries:** `get_active_element_ids`, `get_all_element_ids`, `get_visible_element_ids`, `get_element_info`, `get_user_element_ids`
- **Editing:** `delete_elements`, `copy_elements`, `move_element`, `duplicate_elements`, `stretch_elements`, `scale_elements`, `mirror_elements`, `chamfer_edge`, `round_edge`, `split_element`
- **Filtering:** `get_elements_by_type`, `filter_elements_by_material`, `get_elements_in_group`, `get_elements_by_color`, `get_elements_by_layer`, `get_elements_by_dimension_range`, `get_elements_in_region`
- **Statistics:** `get_element_count_by_type`, `get_material_statistics`, `get_group_statistics`
- **Connections:** `join_elements`, `unjoin_elements`
- **Wood Joints:** `cut_corner_lap`, `cut_cross_lap`, `cut_half_lap`, `cut_double_tenon`, `cut_scarf_joint`, `cut_shoulder`
- **Conversion:** `convert_beam_to_panel`, `convert_panel_to_beam`, `convert_auxiliary_to_beam`
- **Containers:** `create_auto_container_from_standard`, `get_container_content_elements`

### ✅ Geometry Operations (35 Functions)
- **Dimensions:** `get_element_width`, `get_element_height`, `get_element_length`, `get_element_volume`, `get_element_weight`
- **Bounding Box:** `get_bounding_box`
- **Outlines:** `get_element_outline`, `get_section_outline`
- **Boolean Operations:** `intersect_elements`, `subtract_elements`, `unite_elements`
- **Vectors & Points:** `get_element_xl`, `get_element_yl`, `get_element_zl`, `get_element_p1`, `get_element_p2`, `get_element_p3`
- **Center of Gravity:** `get_center_of_gravity`, `get_center_of_gravity_for_list`, `calculate_center_of_mass`
- **Vertices & Faces:** `get_element_vertices`, `get_element_facets`, `get_element_reference_face_area`, `get_total_area_of_all_faces`
- **Analysis:** `get_minimum_distance_between_elements`, `get_closest_point_on_element`, `get_element_type`, `project_point_to_element`
- **Transformations:** `rotate_elements`, `apply_global_scale`, `invert_model`, `rotate_height_axis_90`, `rotate_length_axis_90`
- **Calculations:** `calculate_total_volume`, `calculate_total_weight`

### ✅ Attribute Management (16 Functions)
- **Queries:** `get_standard_attributes`, `get_user_attributes`, `list_defined_user_attributes`, `get_element_attribute_display_name`
- **Setters:** `set_name`, `set_material`, `set_group`, `set_comment`, `set_subgroup`, `set_user_attribute`
- **Advanced:** `clear_user_attribute`, `copy_attributes`
- **Batch Operations:** `batch_set_user_attributes`, `validate_attribute_consistency`
- **Business Intelligence:** `search_elements_by_attributes`, `export_attribute_report`

### ✅ Visualization (12 Functions)
- **Properties:** `set_color`, `set_visibility`, `set_transparency`, `get_color`, `get_transparency`
- **Global Control:** `show_all_elements`, `hide_all_elements`, `refresh_display`, `get_visible_element_count`
- **Intelligent Visualization:** `create_visual_filter`, `apply_color_scheme`

### ✅ Utility Functions (6 Functions)
- **Display:** `disable_auto_display_refresh`, `enable_auto_display_refresh`
- **Messages:** `print_error`, `print_warning`
- **Project:** `get_3d_file_path`, `get_project_data`, `get_cadwork_version_info`

### ✅ Specialized Modules
- **Shop Drawings (2):** `add_wall_section_x`, `add_wall_section_y`
- **Roof Analysis (2):** `get_roof_surfaces`, `calculate_roof_area`
- **Machine Integration (1):** `check_production_list_discrepancies`
- **Measurements (3):** `measure_distance`, `measure_angle`, `measure_area`
- **Material Management (3):** `create_material`, `get_material_properties`, `list_available_materials`
- **Shop Drawings (4):** `add_wall_section_x`, `add_wall_section_y`, `add_wall_section_vertical`, `export_2d_wireframe`
- **Export/Import (24):** `export_to_btl`, `export_element_list`, `export_to_ifc`, `export_to_dxf`, `export_workshop_drawings`, `export_cutting_list`, `export_to_step`, `export_to_3dm`, `export_to_obj`, `export_to_ply`, `export_to_stl`, `export_to_gltf`, `export_to_x3d`, `export_production_data`, `export_to_fbx`, `export_to_webgl`, `export_to_sat`, `export_to_dstv`, `export_step_with_drillings`, `export_btl_for_nesting`, `import_from_step`, `import_from_sat`, `import_from_rhino`, `import_from_btl`

**Current Total: 156 available functions**

## ❌ Missing Cadwork API Functions (to be implemented)

**Remaining Functions: 82 of originally ~238 planned functions**

### 🏠 Building & Structures (9 Functions) - **HIGHEST PRIORITY**
- `create_wall_system`, `create_floor_system`, `create_roof_system`
- `generate_frame_structure`, `optimize_timber_structure`
- `perform_structural_analysis`, `create_foundation_elements`
- `generate_load_paths`, `calculate_load_distribution`

### 📊 Export & Import-Extended (12 Functions) - **CRITICAL**
- `export_to_hundegger`, `export_to_weinmann`, `export_to_krusi`
- `import_from_cad`, `export_assembly_instructions`
- `generate_production_data`, `create_cnc_program`
- `export_material_optimization`, `import_point_cloud`
- `export_vr_model`, `import_survey_data`, `export_energy_analysis`

### 📋 Lists & Reports (10 Functions) - **IMPORTANT**
- `create_element_list`, `generate_material_list`, `create_cost_calculation`
- `export_assembly_drawings`, `create_production_schedule`
- `generate_quality_report`, `create_delivery_note`
- `generate_waste_report`, `create_timeline_report`, `generate_compliance_report`

### 🔧 Element-Extended Operations (8 Functions)
- `get_nested_elements`, `get_parent_elements`, `get_child_elements`
- `create_dovetail_joint`, `create_mortise_tenon`, `create_finger_joint`
- `automatic_beam_processing`, `add_drilling_pattern`

### 🏭 Production Integration (7 Functions) - **INDUSTRY 4.0**
- `machine_time_estimation`, `production_line_optimization`
- `quality_control_integration`, `inventory_management`
- `supplier_integration`, `logistics_optimization`, `maintenance_scheduling`

### 📐 Advanced Geometry Analysis (6 Functions)
- `check_collisions`, `validate_joints`, `verify_dimensions`
- `analyze_material_usage`, `optimize_waste_reduction`, `calculate_static_properties`

### 🎨 Material & Texture-Extended (7 Functions)
- `assign_texture`, `set_element_density`, `set_thermal_properties`
- `create_custom_material`, `material_cost_calculation`
- `material_environmental_impact`, `material_fire_resistance`

### 🎬 Animation & Visualization-Extended (9 Functions)
- `create_assembly_animation`, `set_camera_position`, `create_walkthrough`
- `generate_renderings`, `set_lighting_conditions`, `create_exploded_view`
- `create_section_views`, `generate_panorama_view`, `create_time_lapse`

### ⚙️ System & Configuration (8 Functions)
- `get_system_settings`, `set_user_preferences`, `manage_templates`
- `backup_project`, `restore_project`, `sync_with_cloud`
- `manage_licenses`, `system_diagnostics`

### 🔗 Advanced Connections (6 Functions)
- `create_custom_processing`, `optimize_cutting_list`, `create_complex_joints`
- `validate_joint_strength`, `calculate_joint_forces`, `optimize_joint_placement`

**Current Progress: 65.5% (156/238 functions)**
**Remaining: 34.5% (82/238 functions)**

## 🏗️ Project Structure

```
C:\cadworkMCP/              # MUST be on C:\ drive!
├── main.py                 # Main MCP server with all tool definitions
├── requirements.txt        # Python dependencies
├── mypy.ini               # Mypy configuration for type safety
├── cadwork_bridge.py      # Legacy bridge (being replaced)
├── claude_desktop_config.json  # Example configuration
│
├── core/                  # Core functionalities
│   ├── server.py          # MCP server setup
│   ├── connection.py      # Cadwork connection management
│   └── logging.py         # Logging configuration
│
├── controllers/           # Function groups (Controller pattern)
│   ├── base_controller.py        # Base controller
│   ├── element_controller.py     # Element operations
│   ├── geometry_controller.py    # Geometry operations
│   ├── attribute_controller.py   # Attribute management
│   ├── visualization_controller.py # Visualization
│   ├── utility_controller.py     # Utility functions
│   ├── shop_drawing_controller.py # Shop drawings
│   ├── roof_controller.py        # Roof analysis
│   └── machine_controller.py     # Machine integration
│
├── bridge/                # Cadwork bridge (copy to API.x64)
│   ├── dispatcher.py      # Command dispatcher
│   ├── helpers.py         # Helper functions
│   └── handlers/          # Specific handlers
│
└── API.x64/              # Cadwork API files (for development)
```

## 📝 Code Guidelines

### Conventions
- **Async/Await:** All MCP tools are asynchronous
- **Type Safety:** Full mypy compatibility with `Dict[str, Any]` return types
- **Parameter Types:** Specific List types (`List[int]`, `List[float]`)
- **English Comments:** All code comments in English
- **Controller Pattern:** Functions grouped by domain

### Adding New Functions
1. **Extend controller** or create new one
2. **Specify types** (`List[int]`, `Dict[str, Any]`)
3. **Register MCP tool in main.py**
4. **Add tests** (if available)

### Debugging
- Logs configured in `core/logging.py`
- Debug mode via environment variables
- Monitor Cadwork connection via `core/connection.py`

---

*Last Update: July 2025 - 124/180-200 functions available (~69% completeness)*