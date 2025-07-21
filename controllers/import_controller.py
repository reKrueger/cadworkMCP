"""
Import controller for file import operations
"""
from typing import Dict, Any, List, Optional
from .base_controller import BaseController

class ImportController(BaseController):
    """Controller for import operations"""
    
    def __init__(self) -> None:
        super().__init__("ImportController")
    
    async def import_from_step(self, file_path: str, scale_factor: float = 1.0,
                              hide_messages: bool = False, insert_position: Optional[List[float]] = None,
                              merge_with_existing: bool = True) -> Dict[str, Any]:
        """Import elements from STEP files for CAD interoperability"""
        try:
            # Validate file path
            if not isinstance(file_path, str) or not file_path.strip():
                return {"status": "error", "message": "file_path must be a non-empty string"}
            
            # Check file extension
            file_path = file_path.strip()
            if not file_path.lower().endswith(('.step', '.stp')):
                return {"status": "error", "message": "file_path must have .step or .stp extension"}
            
            # Validate scale factor
            if not isinstance(scale_factor, (int, float)) or scale_factor <= 0:
                return {"status": "error", "message": "scale_factor must be a positive number"}
            
            # Validate insert position if provided
            if insert_position is not None:
                if not isinstance(insert_position, list) or len(insert_position) != 3:
                    return {"status": "error", "message": "insert_position must be a list of 3 numbers [x,y,z]"}
                
                try:
                    insert_position = [float(x) for x in insert_position]
                except (ValueError, TypeError):
                    return {"status": "error", "message": "insert_position must contain valid numbers"}
            
            # Prepare import parameters
            import_params: Dict[str, Any] = {
                "file_path": file_path,
                "scale_factor": float(scale_factor),
                "hide_messages": bool(hide_messages),
                "merge_with_existing": bool(merge_with_existing)
            }
            
            if insert_position:
                import_params["insert_position"] = insert_position
            
            return self.send_command("import_from_step", import_params)
            
        except Exception as e:
            return {"status": "error", "message": f"import_from_step failed: {e}"}
    
    async def import_from_sat(self, file_path: str, scale_factor: float = 1.0,
                             binary_format: bool = True, insert_position: Optional[List[float]] = None,
                             silent_mode: bool = False) -> Dict[str, Any]:
        """Import elements from SAT files (ACIS format) for solid modeling"""
        try:
            # Validate file path
            if not isinstance(file_path, str) or not file_path.strip():
                return {"status": "error", "message": "file_path must be a non-empty string"}
            
            # Check file extension
            file_path = file_path.strip()
            if not file_path.lower().endswith('.sat'):
                return {"status": "error", "message": "file_path must have .sat extension"}
            
            # Validate scale factor
            if not isinstance(scale_factor, (int, float)) or scale_factor <= 0:
                return {"status": "error", "message": "scale_factor must be a positive number"}
            
            # Validate insert position if provided
            if insert_position is not None:
                if not isinstance(insert_position, list) or len(insert_position) != 3:
                    return {"status": "error", "message": "insert_position must be a list of 3 numbers [x,y,z]"}
                
                try:
                    insert_position = [float(x) for x in insert_position]
                except (ValueError, TypeError):
                    return {"status": "error", "message": "insert_position must contain valid numbers"}
            
            # Prepare import parameters
            import_params: Dict[str, Any] = {
                "file_path": file_path,
                "scale_factor": float(scale_factor),
                "binary_format": bool(binary_format),
                "silent_mode": bool(silent_mode)
            }
            
            if insert_position:
                import_params["insert_position"] = insert_position
            
            return self.send_command("import_from_sat", import_params)
            
        except Exception as e:
            return {"status": "error", "message": f"import_from_sat failed: {e}"}
    
    async def import_from_rhino(self, file_path: str, without_dialog: bool = False,
                               import_layers: bool = True, import_materials: bool = True,
                               scale_factor: float = 1.0) -> Dict[str, Any]:
        """Import elements from Rhino 3DM files for parametric design workflows"""
        try:
            # Validate file path
            if not isinstance(file_path, str) or not file_path.strip():
                return {"status": "error", "message": "file_path must be a non-empty string"}
            
            # Check file extension
            file_path = file_path.strip()
            if not file_path.lower().endswith('.3dm'):
                return {"status": "error", "message": "file_path must have .3dm extension"}
            
            # Validate scale factor
            if not isinstance(scale_factor, (int, float)) or scale_factor <= 0:
                return {"status": "error", "message": "scale_factor must be a positive number"}
            
            # Prepare import parameters
            import_params: Dict[str, Any] = {
                "file_path": file_path,
                "without_dialog": bool(without_dialog),
                "import_layers": bool(import_layers),
                "import_materials": bool(import_materials),
                "scale_factor": float(scale_factor)
            }
            
            return self.send_command("import_from_rhino", import_params)
            
        except Exception as e:
            return {"status": "error", "message": f"import_from_rhino failed: {e}"}
    
    async def import_from_btl(self, file_path: str, import_mode: str = "standard",
                             merge_duplicates: bool = True, validate_geometry: bool = True,
                             import_processing: bool = True) -> Dict[str, Any]:
        """Import elements from BTL files for CNC data integration"""
        try:
            # Validate file path
            if not isinstance(file_path, str) or not file_path.strip():
                return {"status": "error", "message": "file_path must be a non-empty string"}
            
            # Check file extension
            file_path = file_path.strip()
            if not file_path.lower().endswith('.btl'):
                return {"status": "error", "message": "file_path must have .btl extension"}
            
            # Validate import mode
            valid_modes = ["standard", "nesting", "geometry_only", "processing_only"]
            if import_mode not in valid_modes:
                return {"status": "error", "message": f"import_mode must be one of: {', '.join(valid_modes)}"}
            
            # Prepare import parameters
            import_params: Dict[str, Any] = {
                "file_path": file_path,
                "import_mode": import_mode,
                "merge_duplicates": bool(merge_duplicates),
                "validate_geometry": bool(validate_geometry),
                "import_processing": bool(import_processing)
            }
            
            return self.send_command("import_from_btl", import_params)
            
        except Exception as e:
            return {"status": "error", "message": f"import_from_btl failed: {e}"}
