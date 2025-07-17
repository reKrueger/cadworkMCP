"""
Import handlers for Cadwork API bridge
"""
from typing import Dict, Any, List, Optional
import cadwork

def handle_import_from_step(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle STEP import operation"""
    try:
        # Get controller
        controller = cadwork.controller()
        file_controller = controller.get_file_controller()
        
        # Extract parameters
        file_path = params.get("file_path")
        scale_factor = params.get("scale_factor", 1.0)
        hide_messages = params.get("hide_messages", False)
        insert_position = params.get("insert_position")
        merge_with_existing = params.get("merge_with_existing", True)
        
        # Perform STEP import using Cadwork API
        if hide_messages:
            imported_elements = file_controller.import_step_file_with_message_option(
                file_path, scale_factor, True
            )
        else:
            imported_elements = file_controller.import_step_file(file_path, scale_factor)
        
        if imported_elements:
            return {
                "status": "success",
                "message": "STEP import completed successfully",
                "file_path": file_path,
                "imported_elements": imported_elements,
                "element_count": len(imported_elements),
                "scale_factor": scale_factor,
                "hide_messages": hide_messages,
                "merge_with_existing": merge_with_existing
            }
        else:
            return {
                "status": "error", 
                "message": "STEP import failed - check file path and format"
            }
            
    except Exception as e:
        return {"status": "error", "message": f"handle_import_from_step error: {e}"}

def handle_import_from_sat(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle SAT import operation"""
    try:
        # Get controller
        controller = cadwork.controller()
        file_controller = controller.get_file_controller()
        
        # Extract parameters
        file_path = params.get("file_path")
        scale_factor = params.get("scale_factor", 1.0)
        binary_format = params.get("binary_format", True)
        insert_position = params.get("insert_position")
        silent_mode = params.get("silent_mode", False)
        
        # Perform SAT import using Cadwork API
        if silent_mode:
            imported_elements = file_controller.import_sat_file_silently(
                file_path, scale_factor, binary_format
            )
        else:
            imported_elements = file_controller.import_sat_file(
                file_path, scale_factor, binary_format
            )
        
        if imported_elements:
            return {
                "status": "success",
                "message": "SAT import completed successfully",
                "file_path": file_path,
                "imported_elements": imported_elements,
                "element_count": len(imported_elements),
                "scale_factor": scale_factor,
                "binary_format": binary_format,
                "silent_mode": silent_mode
            }
        else:
            return {
                "status": "error", 
                "message": "SAT import failed - check file path and format"
            }
            
    except Exception as e:
        return {"status": "error", "message": f"handle_import_from_sat error: {e}"}

def handle_import_from_rhino(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle Rhino 3DM import operation"""
    try:
        # Get controller
        controller = cadwork.controller()
        file_controller = controller.get_file_controller()
        
        # Extract parameters
        file_path = params.get("file_path")
        without_dialog = params.get("without_dialog", False)
        import_layers = params.get("import_layers", True)
        import_materials = params.get("import_materials", True)
        scale_factor = params.get("scale_factor", 1.0)
        
        # Perform Rhino import using Cadwork API
        imported_elements = file_controller.import_rhino_file(file_path, without_dialog)
        
        if imported_elements:
            return {
                "status": "success",
                "message": "Rhino 3DM import completed successfully",
                "file_path": file_path,
                "imported_elements": imported_elements,
                "element_count": len(imported_elements),
                "without_dialog": without_dialog,
                "import_layers": import_layers,
                "import_materials": import_materials,
                "scale_factor": scale_factor
            }
        else:
            return {
                "status": "error", 
                "message": "Rhino import failed - check file path and format"
            }
            
    except Exception as e:
        return {"status": "error", "message": f"handle_import_from_rhino error: {e}"}

def handle_import_from_btl(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle BTL import operation"""
    try:
        # Get controller
        controller = cadwork.controller()
        file_controller = controller.get_file_controller()
        
        # Extract parameters
        file_path = params.get("file_path")
        import_mode = params.get("import_mode", "standard")
        merge_duplicates = params.get("merge_duplicates", True)
        validate_geometry = params.get("validate_geometry", True)
        import_processing = params.get("import_processing", True)
        
        # Perform BTL import using Cadwork API
        if import_mode == "nesting":
            file_controller.import_btl_file_for_nesting(file_path)
            return {
                "status": "success",
                "message": "BTL nesting import completed successfully",
                "file_path": file_path,
                "import_mode": import_mode,
                "note": "Nesting import completed - check nesting workspace"
            }
        else:
            file_controller.import_btl_file(file_path)
            return {
                "status": "success",
                "message": "BTL import completed successfully",
                "file_path": file_path,
                "import_mode": import_mode,
                "merge_duplicates": merge_duplicates,
                "validate_geometry": validate_geometry,
                "import_processing": import_processing
            }
            
    except Exception as e:
        return {"status": "error", "message": f"handle_import_from_btl error: {e}"}
