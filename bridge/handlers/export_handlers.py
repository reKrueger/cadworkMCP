"""
Export handlers for Cadwork API bridge
"""
from typing import Dict, Any, List, Optional
import cadwork

def handle_export_to_step(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle STEP export operation"""
    try:
        # Import here to avoid import-time errors
        import cadwork
        import file_controller as fc
        import element_controller as ec
        
        # Extract parameters
        element_ids = params.get("element_ids")
        file_path = params.get("file_path")
        step_version = params.get("step_version", "AP214")
        units = params.get("units", "mm")
        precision = params.get("precision", 0.01)
        export_all_visible = params.get("export_all_visible", False)
        
        # Use element IDs or get all visible
        if export_all_visible or element_ids is None:
            element_ids = ec.get_visible_identifiable_element_ids()
        
        # Map step version to API format
        version_map = {"AP203": 203, "AP214": 214, "AP242": 242}
        api_version = version_map.get(step_version, 214)
        
        # Determine scale factor based on units
        scale_map = {"mm": 1.0, "cm": 10.0, "m": 1000.0, "inch": 25.4, "ft": 304.8}
        scale_factor = scale_map.get(units, 1.0)
        
        # Perform STEP export using Cadwork API
        fc.export_step_file(element_ids, file_path, scale_factor, api_version, False)
        
        return {
            "status": "success",
            "message": "STEP export completed successfully",
            "file_path": file_path,
            "exported_elements": len(element_ids),
            "step_version": step_version,
            "units": units,
            "precision": precision
        }
            
    except Exception as e:
        return {"status": "error", "message": f"handle_export_to_step error: {e}"}

def handle_export_to_3dm(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle Rhino 3DM export operation"""
    try:
        # Get controller
        controller = cadwork.controller()
        export_controller = controller.get_export_controller()
        
        # Extract parameters
        element_ids = params.get("element_ids")
        file_path = params.get("file_path")
        rhino_version = params.get("rhino_version", "7")
        include_materials = params.get("include_materials", True)
        include_layers = params.get("include_layers", True)
        mesh_quality = params.get("mesh_quality", "medium")
        export_all_visible = params.get("export_all_visible", False)
        
        # Set export settings
        export_controller.set_rhino_version(rhino_version)
        export_controller.set_include_materials(include_materials)
        export_controller.set_include_layers(include_layers)
        export_controller.set_mesh_quality(mesh_quality)
        
        # Perform export
        if export_all_visible or element_ids is None:
            # Export all visible elements
            result = export_controller.export_visible_elements_to_3dm(file_path)
        else:
            # Export specific elements
            result = export_controller.export_elements_to_3dm(element_ids, file_path)
        
        if result:
            return {
                "status": "success",
                "message": "3DM export completed successfully",
                "file_path": file_path,
                "exported_elements": len(element_ids) if element_ids else "all_visible",
                "rhino_version": rhino_version,
                "include_materials": include_materials,
                "include_layers": include_layers,
                "mesh_quality": mesh_quality
            }
        else:
            return {
                "status": "error", 
                "message": "3DM export failed - check file path and element selection"
            }
            
    except Exception as e:
        return {"status": "error", "message": f"handle_export_to_3dm error: {e}"}

def handle_export_to_obj(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle OBJ export operation"""
    try:
        # Get controller
        controller = cadwork.controller()
        export_controller = controller.get_export_controller()
        
        # Extract parameters
        element_ids = params.get("element_ids")
        file_path = params.get("file_path")
        include_materials = params.get("include_materials", True)
        include_normals = params.get("include_normals", True)
        include_textures = params.get("include_textures", False)
        mesh_resolution = params.get("mesh_resolution", "medium")
        export_all_visible = params.get("export_all_visible", False)
        
        # Set export settings
        export_controller.set_include_materials(include_materials)
        export_controller.set_include_normals(include_normals)
        export_controller.set_include_textures(include_textures)
        export_controller.set_mesh_resolution(mesh_resolution)
        
        # Perform export
        if export_all_visible or element_ids is None:
            # Export all visible elements
            result = export_controller.export_visible_elements_to_obj(file_path)
        else:
            # Export specific elements
            result = export_controller.export_elements_to_obj(element_ids, file_path)
        
        if result:
            return {
                "status": "success",
                "message": "OBJ export completed successfully",
                "file_path": file_path,
                "exported_elements": len(element_ids) if element_ids else "all_visible",
                "include_materials": include_materials,
                "include_normals": include_normals,
                "include_textures": include_textures,
                "mesh_resolution": mesh_resolution
            }
        else:
            return {
                "status": "error", 
                "message": "OBJ export failed - check file path and element selection"
            }
            
    except Exception as e:
        return {"status": "error", "message": f"handle_export_to_obj error: {e}"}

def handle_export_to_ply(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle PLY export operation"""
    try:
        # Get controller
        controller = cadwork.controller()
        export_controller = controller.get_export_controller()
        
        # Extract parameters
        element_ids = params.get("element_ids")
        file_path = params.get("file_path")
        ply_format = params.get("ply_format", "binary")
        include_colors = params.get("include_colors", True)
        include_normals = params.get("include_normals", True)
        coordinate_precision = params.get("coordinate_precision", 6)
        export_all_visible = params.get("export_all_visible", False)
        
        # Set export settings
        export_controller.set_ply_format(ply_format)
        export_controller.set_include_colors(include_colors)
        export_controller.set_include_normals(include_normals)
        export_controller.set_coordinate_precision(coordinate_precision)
        
        # Perform export
        if export_all_visible or element_ids is None:
            # Export all visible elements
            result = export_controller.export_visible_elements_to_ply(file_path)
        else:
            # Export specific elements
            result = export_controller.export_elements_to_ply(element_ids, file_path)
        
        if result:
            return {
                "status": "success",
                "message": "PLY export completed successfully",
                "file_path": file_path,
                "exported_elements": len(element_ids) if element_ids else "all_visible",
                "ply_format": ply_format,
                "include_colors": include_colors,
                "include_normals": include_normals,
                "coordinate_precision": coordinate_precision
            }
        else:
            return {
                "status": "error", 
                "message": "PLY export failed - check file path and element selection"
            }
            
    except Exception as e:
        return {"status": "error", "message": f"handle_export_to_ply error: {e}"}

def handle_export_to_stl(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle STL export operation"""
    try:
        # Get controller
        controller = cadwork.controller()
        export_controller = controller.get_export_controller()
        
        # Extract parameters
        element_ids = params.get("element_ids")
        file_path = params.get("file_path")
        stl_format = params.get("stl_format", "binary")
        mesh_quality = params.get("mesh_quality", "medium")
        units = params.get("units", "mm")
        merge_elements = params.get("merge_elements", True)
        export_all_visible = params.get("export_all_visible", False)
        
        # Set export settings
        export_controller.set_stl_format(stl_format)
        export_controller.set_mesh_quality(mesh_quality)
        export_controller.set_export_units(units)
        export_controller.set_merge_elements(merge_elements)
        
        # Perform export
        if export_all_visible or element_ids is None:
            # Export all visible elements
            result = export_controller.export_visible_elements_to_stl(file_path)
        else:
            # Export specific elements
            result = export_controller.export_elements_to_stl(element_ids, file_path)
        
        if result:
            return {
                "status": "success",
                "message": "STL export completed successfully",
                "file_path": file_path,
                "exported_elements": len(element_ids) if element_ids else "all_visible",
                "stl_format": stl_format,
                "mesh_quality": mesh_quality,
                "units": units,
                "merge_elements": merge_elements
            }
        else:
            return {
                "status": "error", 
                "message": "STL export failed - check file path and element selection"
            }
            
    except Exception as e:
        return {"status": "error", "message": f"handle_export_to_stl error: {e}"}

def handle_export_to_gltf(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle glTF export operation"""
    try:
        # Get controller
        controller = cadwork.controller()
        export_controller = controller.get_export_controller()
        
        # Extract parameters
        element_ids = params.get("element_ids")
        file_path = params.get("file_path")
        gltf_format = params.get("gltf_format", "glb")
        include_materials = params.get("include_materials", True)
        include_animations = params.get("include_animations", False)
        texture_resolution = params.get("texture_resolution", 1024)
        compression_level = params.get("compression_level", "medium")
        export_all_visible = params.get("export_all_visible", False)
        
        # Set export settings
        export_controller.set_gltf_format(gltf_format)
        export_controller.set_include_materials(include_materials)
        export_controller.set_include_animations(include_animations)
        export_controller.set_texture_resolution(texture_resolution)
        export_controller.set_compression_level(compression_level)
        
        # Perform export
        if export_all_visible or element_ids is None:
            # Export all visible elements
            result = export_controller.export_visible_elements_to_gltf(file_path)
        else:
            # Export specific elements
            result = export_controller.export_elements_to_gltf(element_ids, file_path)
        
        if result:
            return {
                "status": "success",
                "message": "glTF export completed successfully",
                "file_path": file_path,
                "exported_elements": len(element_ids) if element_ids else "all_visible",
                "gltf_format": gltf_format,
                "include_materials": include_materials,
                "include_animations": include_animations,
                "texture_resolution": texture_resolution,
                "compression_level": compression_level
            }
        else:
            return {
                "status": "error", 
                "message": "glTF export failed - check file path and element selection"
            }
            
    except Exception as e:
        return {"status": "error", "message": f"handle_export_to_gltf error: {e}"}

def handle_export_to_x3d(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle X3D export operation"""
    try:
        # Get controller
        controller = cadwork.controller()
        export_controller = controller.get_export_controller()
        
        # Extract parameters
        element_ids = params.get("element_ids")
        file_path = params.get("file_path")
        x3d_version = params.get("x3d_version", "4.0")
        encoding = params.get("encoding", "xml")
        include_materials = params.get("include_materials", True)
        include_lighting = params.get("include_lighting", True)
        include_navigation = params.get("include_navigation", True)
        compression = params.get("compression", False)
        export_all_visible = params.get("export_all_visible", False)
        
        # Set export settings
        export_controller.set_x3d_version(x3d_version)
        export_controller.set_x3d_encoding(encoding)
        export_controller.set_include_materials(include_materials)
        export_controller.set_include_lighting(include_lighting)
        export_controller.set_include_navigation(include_navigation)
        export_controller.set_compression(compression)
        
        # Perform export
        if export_all_visible or element_ids is None:
            # Export all visible elements
            result = export_controller.export_visible_elements_to_x3d(file_path)
        else:
            # Export specific elements
            result = export_controller.export_elements_to_x3d(element_ids, file_path)
        
        if result:
            return {
                "status": "success",
                "message": "X3D export completed successfully",
                "file_path": file_path,
                "exported_elements": len(element_ids) if element_ids else "all_visible",
                "x3d_version": x3d_version,
                "encoding": encoding,
                "include_materials": include_materials,
                "include_lighting": include_lighting,
                "include_navigation": include_navigation,
                "compression": compression
            }
        else:
            return {
                "status": "error", 
                "message": "X3D export failed - check file path and element selection"
            }
            
    except Exception as e:
        return {"status": "error", "message": f"handle_export_to_x3d error: {e}"}

def handle_export_production_data(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle production data export operation"""
    try:
        # Get controller
        controller = cadwork.controller()
        export_controller = controller.get_export_controller()
        production_controller = controller.get_production_controller()
        
        # Extract parameters
        element_ids = params.get("element_ids")
        file_path = params.get("file_path")
        data_format = params.get("data_format", "json")
        include_cutting_list = params.get("include_cutting_list", True)
        include_assembly_instructions = params.get("include_assembly_instructions", True)
        include_hardware_list = params.get("include_hardware_list", True)
        include_processing_data = params.get("include_processing_data", True)
        include_material_optimization = params.get("include_material_optimization", True)
        group_by_production_step = params.get("group_by_production_step", True)
        export_all_visible = params.get("export_all_visible", False)
        
        # Set export settings
        production_controller.set_include_cutting_list(include_cutting_list)
        production_controller.set_include_assembly_instructions(include_assembly_instructions)
        production_controller.set_include_hardware_list(include_hardware_list)
        production_controller.set_include_processing_data(include_processing_data)
        production_controller.set_include_material_optimization(include_material_optimization)
        production_controller.set_group_by_production_step(group_by_production_step)
        
        # Perform export
        if export_all_visible or element_ids is None:
            # Export all visible elements
            result = production_controller.export_visible_production_data(file_path, data_format)
        else:
            # Export specific elements
            result = production_controller.export_elements_production_data(element_ids, file_path, data_format)
        
        if result:
            return {
                "status": "success",
                "message": "Production data export completed successfully",
                "file_path": file_path,
                "exported_elements": len(element_ids) if element_ids else "all_visible",
                "data_format": data_format,
                "include_cutting_list": include_cutting_list,
                "include_assembly_instructions": include_assembly_instructions,
                "include_hardware_list": include_hardware_list,
                "include_processing_data": include_processing_data,
                "include_material_optimization": include_material_optimization,
                "group_by_production_step": group_by_production_step
            }
        else:
            return {
                "status": "error", 
                "message": "Production data export failed - check file path and element selection"
            }
            
    except Exception as e:
        return {"status": "error", "message": f"handle_export_production_data error: {e}"}

def handle_export_to_fbx(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle FBX export operation"""
    try:
        # Get controller
        controller = cadwork.controller()
        file_controller = controller.get_file_controller()
        
        # Extract parameters
        element_ids = params.get("element_ids")
        file_path = params.get("file_path")
        fbx_format = params.get("fbx_format", 1)  # API format code
        fbx_version = params.get("fbx_version", "2020")
        include_materials = params.get("include_materials", True)
        include_textures = params.get("include_textures", True)
        include_animations = params.get("include_animations", False)
        export_all_visible = params.get("export_all_visible", False)
        
        # Use element IDs or get all visible
        if export_all_visible or element_ids is None:
            element_controller = controller.get_element_controller()
            element_ids = element_controller.get_visible_identifiable_element_ids()
        
        # Perform export using Cadwork API
        file_controller.export_fbx_file(element_ids, file_path, fbx_format)
        
        return {
            "status": "success",
            "message": "FBX export completed successfully",
            "file_path": file_path,
            "exported_elements": len(element_ids),
            "fbx_format": fbx_format,
            "fbx_version": fbx_version,
            "include_materials": include_materials,
            "include_textures": include_textures,
            "include_animations": include_animations
        }
            
    except Exception as e:
        return {"status": "error", "message": f"handle_export_to_fbx error: {e}"}

def handle_export_to_webgl(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle WebGL export operation"""
    try:
        # Get controller
        controller = cadwork.controller()
        file_controller = controller.get_file_controller()
        
        # Extract parameters
        element_ids = params.get("element_ids")
        file_path = params.get("file_path")
        web_quality = params.get("web_quality", "medium")
        include_materials = params.get("include_materials", True)
        include_textures = params.get("include_textures", True)
        compression = params.get("compression", True)
        embed_viewer = params.get("embed_viewer", True)
        export_all_visible = params.get("export_all_visible", False)
        
        # Use element IDs or get all visible
        if export_all_visible or element_ids is None:
            element_controller = controller.get_element_controller()
            element_ids = element_controller.get_visible_identifiable_element_ids()
        
        # Perform export using Cadwork API
        result = file_controller.export_webgl(element_ids, file_path)
        
        if result:
            return {
                "status": "success",
                "message": "WebGL export completed successfully",
                "file_path": file_path,
                "exported_elements": len(element_ids),
                "web_quality": web_quality,
                "include_materials": include_materials,
                "include_textures": include_textures,
                "compression": compression,
                "embed_viewer": embed_viewer
            }
        else:
            return {
                "status": "error", 
                "message": "WebGL export failed - check file path and element selection"
            }
            
    except Exception as e:
        return {"status": "error", "message": f"handle_export_to_webgl error: {e}"}

def handle_export_to_sat(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle SAT export operation"""
    try:
        # Get controller
        controller = cadwork.controller()
        file_controller = controller.get_file_controller()
        
        # Extract parameters
        element_ids = params.get("element_ids")
        file_path = params.get("file_path")
        scale_factor = params.get("scale_factor", 1.0)
        binary_format = params.get("binary_format", True)
        sat_version = params.get("sat_version", 25000)
        include_drillings = params.get("include_drillings", False)
        drilling_mode = params.get("drilling_mode", "none")
        export_all_visible = params.get("export_all_visible", False)
        
        # Use element IDs or get all visible
        if export_all_visible or element_ids is None:
            element_controller = controller.get_element_controller()
            element_ids = element_controller.get_visible_identifiable_element_ids()
        
        # Choose appropriate export method based on drilling mode
        if drilling_mode == "cut" and include_drillings:
            file_controller.export_sat_file_cut_drillings(
                element_ids, file_path, scale_factor, binary_format, sat_version
            )
        else:
            # Standard SAT export
            file_controller.export_sat_file(
                element_ids, file_path, scale_factor, binary_format, sat_version
            )
        
        return {
            "status": "success",
            "message": "SAT export completed successfully",
            "file_path": file_path,
            "exported_elements": len(element_ids),
            "scale_factor": scale_factor,
            "binary_format": binary_format,
            "sat_version": sat_version,
            "include_drillings": include_drillings,
            "drilling_mode": drilling_mode
        }
            
    except Exception as e:
        return {"status": "error", "message": f"handle_export_to_sat error: {e}"}

def handle_export_to_dstv(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle DSTV export operation"""
    try:
        # Get controller
        controller = cadwork.controller()
        file_controller = controller.get_file_controller()
        
        # Extract parameters
        element_ids = params.get("element_ids")
        file_path = params.get("file_path")
        dstv_version = params.get("dstv_version", "NC1")
        units = params.get("units", "mm")
        include_material_info = params.get("include_material_info", True)
        include_processing = params.get("include_processing", True)
        steel_grade = params.get("steel_grade", "S355")
        export_all_visible = params.get("export_all_visible", False)
        
        # Use element IDs or get all visible
        if export_all_visible or element_ids is None:
            element_controller = controller.get_element_controller()
            element_ids = element_controller.get_visible_identifiable_element_ids()
        
        # Perform DSTV export using Cadwork API
        result = file_controller.export_dstv_file(file_path)
        
        if result:
            return {
                "status": "success",
                "message": "DSTV export completed successfully",
                "file_path": file_path,
                "exported_elements": len(element_ids),
                "dstv_version": dstv_version,
                "units": units,
                "include_material_info": include_material_info,
                "include_processing": include_processing,
                "steel_grade": steel_grade
            }
        else:
            return {
                "status": "error", 
                "message": "DSTV export failed - check file path and element selection"
            }
            
    except Exception as e:
        return {"status": "error", "message": f"handle_export_to_dstv error: {e}"}

def handle_export_step_with_drillings(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle STEP export with drilling processing"""
    try:
        # Get controller
        controller = cadwork.controller()
        file_controller = controller.get_file_controller()
        
        # Extract parameters
        element_ids = params.get("element_ids")
        file_path = params.get("file_path")
        drilling_mode = params.get("drilling_mode", "extrude")
        scale_factor = params.get("scale_factor", 1.0)
        step_version = params.get("step_version", 214)
        text_mode = params.get("text_mode", False)
        imperial_units = params.get("imperial_units", False)
        export_all_visible = params.get("export_all_visible", False)
        
        # Use element IDs or get all visible
        if export_all_visible or element_ids is None:
            element_controller = controller.get_element_controller()
            element_ids = element_controller.get_visible_identifiable_element_ids()
        
        # Choose appropriate export method based on drilling mode
        if drilling_mode == "extrude":
            file_controller.export_step_file_extrude_drillings(
                element_ids, file_path, scale_factor, step_version, text_mode, imperial_units
            )
        elif drilling_mode == "cut":
            file_controller.export_step_file_cut_drillings(
                element_ids, file_path, scale_factor, step_version, text_mode, imperial_units
            )
        else:
            # Standard STEP export without drilling processing
            file_controller.export_step_file(
                element_ids, file_path, scale_factor, step_version, text_mode
            )
        
        return {
            "status": "success",
            "message": f"STEP export with {drilling_mode} drillings completed successfully",
            "file_path": file_path,
            "exported_elements": len(element_ids),
            "drilling_mode": drilling_mode,
            "scale_factor": scale_factor,
            "step_version": step_version,
            "text_mode": text_mode,
            "imperial_units": imperial_units
        }
            
    except Exception as e:
        return {"status": "error", "message": f"handle_export_step_with_drillings error: {e}"}

def handle_export_btl_for_nesting(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle BTL export for nesting operations"""
    try:
        # Get controller
        controller = cadwork.controller()
        file_controller = controller.get_file_controller()
        
        # Extract parameters
        file_path = params.get("file_path")
        nesting_parameters = params.get("nesting_parameters", {})
        optimization_method = params.get("optimization_method", "area")
        material_efficiency = params.get("material_efficiency", True)
        sheet_size = params.get("sheet_size")
        kerf_width = params.get("kerf_width", 3.0)
        
        # Perform BTL nesting export using Cadwork API
        file_controller.export_btl_file_for_nesting(file_path)
        
        return {
            "status": "success",
            "message": "BTL nesting export completed successfully",
            "file_path": file_path,
            "nesting_parameters": nesting_parameters,
            "optimization_method": optimization_method,
            "material_efficiency": material_efficiency,
            "kerf_width": kerf_width,
            "sheet_size": sheet_size
        }
            
    except Exception as e:
        return {"status": "error", "message": f"handle_export_btl_for_nesting error: {e}"}
