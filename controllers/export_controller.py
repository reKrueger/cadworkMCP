"""
Export controller for file export operations
"""
from typing import Dict, Any, List, Optional
from .base_controller import BaseController

class ExportController(BaseController):
    """Controller for export operations"""
    
    def __init__(self) -> None:
        super().__init__("ExportController")
    
    async def export_to_btl(self, element_ids: Optional[List[int]] = None, 
                           file_path: Optional[str] = None,
                           btl_version: str = "10.5",
                           include_processing: bool = True,
                           include_geometry: bool = True) -> Dict[str, Any]:
        """Export elements to BTL (Biesse Transfer Language) format"""
        try:
            # Prepare export parameters
            export_params: Dict[str, Any] = {
                "btl_version": btl_version,
                "include_processing": include_processing,
                "include_geometry": include_geometry
            }
            
            # Validate BTL version
            valid_versions = ["10.0", "10.5", "11.0"]
            if btl_version not in valid_versions:
                return {"status": "error", "message": f"btl_version must be one of: {', '.join(valid_versions)}"}
            
            # Validate element IDs if provided
            if element_ids is not None:
                if not isinstance(element_ids, list) or len(element_ids) == 0:
                    return {"status": "error", "message": "element_ids must be a non-empty list when provided"}
                
                validated_ids = []
                for element_id in element_ids:
                    validated_id = self.validate_element_id(element_id)
                    validated_ids.append(validated_id)
                
                export_params["element_ids"] = validated_ids
            else:
                # Export all visible elements if none specified
                export_params["export_all_visible"] = True
            
            # Validate file path if provided
            if file_path is not None:
                if not isinstance(file_path, str) or not file_path.strip():
                    return {"status": "error", "message": "file_path must be a non-empty string when provided"}
                
                # Ensure .btl extension
                file_path = file_path.strip()
                if not file_path.lower().endswith('.btl'):
                    file_path += '.btl'
                
                export_params["file_path"] = file_path
            
            # Validate boolean parameters
            if not isinstance(include_processing, bool):
                export_params["include_processing"] = True
            
            if not isinstance(include_geometry, bool):
                export_params["include_geometry"] = True
            
            return self.send_command("export_to_btl", export_params)
            
        except Exception as e:
            return {"status": "error", "message": f"export_to_btl failed: {e}"}
    
    async def get_export_formats(self) -> Dict[str, Any]:
        """Get list of available export formats"""
        try:
            return self.send_command("get_export_formats", {})
            
        except Exception as e:
            return {"status": "error", "message": f"get_export_formats failed: {e}"}
    
    async def export_element_list(self, element_ids: List[int], 
                                 export_format: str = "csv",
                                 include_properties: bool = True,
                                 include_materials: bool = True,
                                 file_path: Optional[str] = None) -> Dict[str, Any]:
        """Export element list with properties to various formats"""
        try:
            # Validate element IDs
            if not isinstance(element_ids, list) or len(element_ids) == 0:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            validated_ids = []
            for element_id in element_ids:
                validated_id = self.validate_element_id(element_id)
                validated_ids.append(validated_id)
            
            # Validate export format
            valid_formats = ["csv", "xlsx", "json", "xml"]
            if export_format not in valid_formats:
                return {"status": "error", "message": f"export_format must be one of: {', '.join(valid_formats)}"}
            
            # Prepare export parameters
            export_params = {
                "element_ids": validated_ids,
                "export_format": export_format,
                "include_properties": bool(include_properties),
                "include_materials": bool(include_materials)
            }
            
            # Validate file path if provided
            if file_path is not None:
                if not isinstance(file_path, str) or not file_path.strip():
                    return {"status": "error", "message": "file_path must be a non-empty string when provided"}
                
                # Ensure correct extension
                file_path = file_path.strip()
                if not file_path.lower().endswith(f'.{export_format}'):
                    file_path += f'.{export_format}'
                
                export_params["file_path"] = file_path
            
            return self.send_command("export_element_list", export_params)
            
        except Exception as e:
            return {"status": "error", "message": f"export_element_list failed: {e}"}
    
    async def export_cutting_list(self, element_ids: Optional[List[int]] = None,
                                 group_by_material: bool = True,
                                 include_waste: bool = True,
                                 optimization_method: str = "length") -> Dict[str, Any]:
        """Export optimized cutting list for production"""
        try:
            # Prepare parameters
            cutting_params: Dict[str, Any] = {
                "group_by_material": bool(group_by_material),
                "include_waste": bool(include_waste),
                "optimization_method": optimization_method
            }
            
            # Validate optimization method
            valid_methods = ["length", "area", "volume", "cost", "none"]
            if optimization_method not in valid_methods:
                return {"status": "error", "message": f"optimization_method must be one of: {', '.join(valid_methods)}"}
            
            # Validate element IDs if provided
            if element_ids is not None:
                if not isinstance(element_ids, list) or len(element_ids) == 0:
                    return {"status": "error", "message": "element_ids must be a non-empty list when provided"}
                
                validated_ids = []
                for element_id in element_ids:
                    validated_id = self.validate_element_id(element_id)
                    validated_ids.append(validated_id)
                
                cutting_params["element_ids"] = validated_ids
            else:
                # Use all visible elements if none specified
                cutting_params["use_all_visible"] = True
            
            return self.send_command("export_cutting_list", cutting_params)
            
        except Exception as e:
            return {"status": "error", "message": f"export_cutting_list failed: {e}"}

    async def export_to_ifc(self, element_ids: Optional[List[int]] = None,
                           file_path: Optional[str] = None,
                           ifc_version: str = "IFC4",
                           include_geometry: bool = True,
                           include_materials: bool = True,
                           include_properties: bool = True,
                           coordinate_system: str = "project") -> Dict[str, Any]:
        """Export elements to IFC (Industry Foundation Classes) format for BIM applications"""
        try:
            # Validate IFC version
            valid_versions = ["IFC2x3", "IFC4", "IFC4x1", "IFC4x3"]
            if ifc_version not in valid_versions:
                return {"status": "error", "message": f"ifc_version must be one of: {', '.join(valid_versions)}"}
            
            # Validate coordinate system
            valid_coordinate_systems = ["project", "global", "local"]
            if coordinate_system not in valid_coordinate_systems:
                return {"status": "error", "message": f"coordinate_system must be one of: {', '.join(valid_coordinate_systems)}"}
            
            # Prepare export parameters
            export_params: Dict[str, Any] = {
                "ifc_version": ifc_version,
                "include_geometry": bool(include_geometry),
                "include_materials": bool(include_materials),
                "include_properties": bool(include_properties),
                "coordinate_system": coordinate_system
            }
            
            # Validate element IDs if provided
            if element_ids is not None:
                if not isinstance(element_ids, list) or len(element_ids) == 0:
                    return {"status": "error", "message": "element_ids must be a non-empty list when provided"}
                
                validated_ids = []
                for element_id in element_ids:
                    validated_id = self.validate_element_id(element_id)
                    validated_ids.append(validated_id)
                
                export_params["element_ids"] = validated_ids
            else:
                # Export all visible elements if none specified
                export_params["export_all_visible"] = True
            
            # Validate file path if provided
            if file_path is not None:
                if not isinstance(file_path, str) or not file_path.strip():
                    return {"status": "error", "message": "file_path must be a non-empty string when provided"}
                
                # Ensure .ifc extension
                file_path = file_path.strip()
                if not file_path.lower().endswith('.ifc'):
                    file_path += '.ifc'
                
                export_params["file_path"] = file_path
            
            return self.send_command("export_to_ifc", export_params)
            
        except Exception as e:
            return {"status": "error", "message": f"export_to_ifc failed: {e}"}

    async def export_to_dxf(self, element_ids: Optional[List[int]] = None,
                           file_path: Optional[str] = None,
                           dxf_version: str = "R2018",
                           view_type: str = "plan",
                           include_dimensions: bool = True,
                           line_weight: float = 0.25) -> Dict[str, Any]:
        """Export elements to DXF format for 2D CAD applications"""
        try:
            # Validate DXF version
            valid_versions = ["R12", "R14", "R2000", "R2004", "R2007", "R2010", "R2013", "R2018"]
            if dxf_version not in valid_versions:
                return {"status": "error", "message": f"dxf_version must be one of: {', '.join(valid_versions)}"}
            
            # Validate view type
            valid_views = ["plan", "elevation", "section", "3d", "isometric"]
            if view_type not in valid_views:
                return {"status": "error", "message": f"view_type must be one of: {', '.join(valid_views)}"}
            
            # Validate line weight
            if not isinstance(line_weight, (int, float)) or line_weight <= 0:
                return {"status": "error", "message": "line_weight must be a positive number (mm)"}
            
            # Prepare export parameters
            export_params: Dict[str, Any] = {
                "dxf_version": dxf_version,
                "view_type": view_type,
                "include_dimensions": bool(include_dimensions),
                "line_weight": float(line_weight)
            }
            
            # Validate element IDs if provided
            if element_ids is not None:
                if not isinstance(element_ids, list) or len(element_ids) == 0:
                    return {"status": "error", "message": "element_ids must be a non-empty list when provided"}
                
                validated_ids = []
                for element_id in element_ids:
                    validated_id = self.validate_element_id(element_id)
                    validated_ids.append(validated_id)
                
                export_params["element_ids"] = validated_ids
            else:
                export_params["export_all_visible"] = True
            
            # Validate file path if provided
            if file_path is not None:
                if not isinstance(file_path, str) or not file_path.strip():
                    return {"status": "error", "message": "file_path must be a non-empty string when provided"}
                
                # Ensure .dxf extension
                file_path = file_path.strip()
                if not file_path.lower().endswith('.dxf'):
                    file_path += '.dxf'
                
                export_params["file_path"] = file_path
            
            return self.send_command("export_to_dxf", export_params)
            
        except Exception as e:
            return {"status": "error", "message": f"export_to_dxf failed: {e}"}

    async def export_workshop_drawings(self, element_ids: Optional[List[int]] = None,
                                     drawing_format: str = "pdf",
                                     include_dimensions: bool = True,
                                     include_processing: bool = True,
                                     scale: str = "1:10",
                                     sheet_size: str = "A3") -> Dict[str, Any]:
        """Export workshop drawings for manufacturing"""
        try:
            # Validate drawing format
            valid_formats = ["pdf", "dxf", "dwg", "png", "jpg"]
            if drawing_format not in valid_formats:
                return {"status": "error", "message": f"drawing_format must be one of: {', '.join(valid_formats)}"}
            
            # Validate scale
            valid_scales = ["1:1", "1:2", "1:5", "1:10", "1:20", "1:50", "1:100", "auto"]
            if scale not in valid_scales:
                return {"status": "error", "message": f"scale must be one of: {', '.join(valid_scales)}"}
            
            # Validate sheet size
            valid_sizes = ["A0", "A1", "A2", "A3", "A4", "ANSI_A", "ANSI_B", "ANSI_C", "ANSI_D"]
            if sheet_size not in valid_sizes:
                return {"status": "error", "message": f"sheet_size must be one of: {', '.join(valid_sizes)}"}
            
            # Prepare export parameters
            export_params: Dict[str, Any] = {
                "drawing_format": drawing_format,
                "include_dimensions": bool(include_dimensions),
                "include_processing": bool(include_processing),
                "scale": scale,
                "sheet_size": sheet_size
            }
            
            # Validate element IDs if provided
            if element_ids is not None:
                if not isinstance(element_ids, list) or len(element_ids) == 0:
                    return {"status": "error", "message": "element_ids must be a non-empty list when provided"}
                
                validated_ids = []
                for element_id in element_ids:
                    validated_id = self.validate_element_id(element_id)
                    validated_ids.append(validated_id)
                
                export_params["element_ids"] = validated_ids
            else:
                export_params["export_all_visible"] = True
            
            return self.send_command("export_workshop_drawings", export_params)
            
        except Exception as e:
            return {"status": "error", "message": f"export_workshop_drawings failed: {e}"}

    async def export_to_step(self, element_ids: Optional[List[int]] = None,
                            file_path: Optional[str] = None,
                            step_version: str = "AP214",
                            units: str = "mm",
                            precision: float = 0.01) -> Dict[str, Any]:
        """Export elements to STEP format for CAD interoperability"""
        try:
            # Validate STEP version
            valid_versions = ["AP203", "AP214", "AP242"]
            if step_version not in valid_versions:
                return {"status": "error", "message": f"step_version must be one of: {', '.join(valid_versions)}"}
            
            # Validate units
            valid_units = ["mm", "cm", "m", "inch", "ft"]
            if units not in valid_units:
                return {"status": "error", "message": f"units must be one of: {', '.join(valid_units)}"}
            
            # Validate precision
            if not isinstance(precision, (int, float)) or precision <= 0:
                return {"status": "error", "message": "precision must be a positive number"}
            
            # Prepare export parameters
            export_params: Dict[str, Any] = {
                "step_version": step_version,
                "units": units,
                "precision": float(precision)
            }
            
            # Validate element IDs if provided
            if element_ids is not None:
                if not isinstance(element_ids, list) or len(element_ids) == 0:
                    return {"status": "error", "message": "element_ids must be a non-empty list when provided"}
                
                validated_ids = []
                for element_id in element_ids:
                    validated_id = self.validate_element_id(element_id)
                    validated_ids.append(validated_id)
                
                export_params["element_ids"] = validated_ids
            else:
                export_params["export_all_visible"] = True
            
            # Validate file path if provided
            if file_path is not None:
                if not isinstance(file_path, str) or not file_path.strip():
                    return {"status": "error", "message": "file_path must be a non-empty string when provided"}
                
                # Ensure .step or .stp extension
                file_path = file_path.strip()
                if not file_path.lower().endswith(('.step', '.stp')):
                    file_path += '.step'
                
                export_params["file_path"] = file_path
            
            return self.send_command("export_to_step", export_params)
            
        except Exception as e:
            return {"status": "error", "message": f"export_to_step failed: {e}"}

    async def export_to_3dm(self, element_ids: Optional[List[int]] = None,
                           file_path: Optional[str] = None,
                           rhino_version: str = "7",
                           include_materials: bool = True,
                           include_layers: bool = True,
                           mesh_quality: str = "medium") -> Dict[str, Any]:
        """Export elements to Rhino 3DM format"""
        try:
            # Validate Rhino version
            valid_versions = ["5", "6", "7", "8"]
            if rhino_version not in valid_versions:
                return {"status": "error", "message": f"rhino_version must be one of: {', '.join(valid_versions)}"}
            
            # Validate mesh quality
            valid_qualities = ["low", "medium", "high", "custom"]
            if mesh_quality not in valid_qualities:
                return {"status": "error", "message": f"mesh_quality must be one of: {', '.join(valid_qualities)}"}
            
            # Prepare export parameters
            export_params: Dict[str, Any] = {
                "rhino_version": rhino_version,
                "include_materials": bool(include_materials),
                "include_layers": bool(include_layers),
                "mesh_quality": mesh_quality
            }
            
            # Validate element IDs if provided
            if element_ids is not None:
                if not isinstance(element_ids, list) or len(element_ids) == 0:
                    return {"status": "error", "message": "element_ids must be a non-empty list when provided"}
                
                validated_ids = []
                for element_id in element_ids:
                    validated_id = self.validate_element_id(element_id)
                    validated_ids.append(validated_id)
                
                export_params["element_ids"] = validated_ids
            else:
                export_params["export_all_visible"] = True
            
            # Validate file path if provided
            if file_path is not None:
                if not isinstance(file_path, str) or not file_path.strip():
                    return {"status": "error", "message": "file_path must be a non-empty string when provided"}
                
                # Ensure .3dm extension
                file_path = file_path.strip()
                if not file_path.lower().endswith('.3dm'):
                    file_path += '.3dm'
                
                export_params["file_path"] = file_path
            
            return self.send_command("export_to_3dm", export_params)
            
        except Exception as e:
            return {"status": "error", "message": f"export_to_3dm failed: {e}"}

    async def export_to_obj(self, element_ids: Optional[List[int]] = None,
                           file_path: Optional[str] = None,
                           include_materials: bool = True,
                           include_normals: bool = True,
                           include_textures: bool = False,
                           mesh_resolution: str = "medium") -> Dict[str, Any]:
        """Export elements to OBJ format for 3D modeling and visualization"""
        try:
            # Validate mesh resolution
            valid_resolutions = ["low", "medium", "high", "ultra"]
            if mesh_resolution not in valid_resolutions:
                return {"status": "error", "message": f"mesh_resolution must be one of: {', '.join(valid_resolutions)}"}
            
            # Prepare export parameters
            export_params: Dict[str, Any] = {
                "include_materials": bool(include_materials),
                "include_normals": bool(include_normals),
                "include_textures": bool(include_textures),
                "mesh_resolution": mesh_resolution
            }
            
            # Validate element IDs if provided
            if element_ids is not None:
                if not isinstance(element_ids, list) or len(element_ids) == 0:
                    return {"status": "error", "message": "element_ids must be a non-empty list when provided"}
                
                validated_ids = []
                for element_id in element_ids:
                    validated_id = self.validate_element_id(element_id)
                    validated_ids.append(validated_id)
                
                export_params["element_ids"] = validated_ids
            else:
                export_params["export_all_visible"] = True
            
            # Validate file path if provided
            if file_path is not None:
                if not isinstance(file_path, str) or not file_path.strip():
                    return {"status": "error", "message": "file_path must be a non-empty string when provided"}
                
                # Ensure .obj extension
                file_path = file_path.strip()
                if not file_path.lower().endswith('.obj'):
                    file_path += '.obj'
                
                export_params["file_path"] = file_path
            
            return self.send_command("export_to_obj", export_params)
            
        except Exception as e:
            return {"status": "error", "message": f"export_to_obj failed: {e}"}

    async def export_to_ply(self, element_ids: Optional[List[int]] = None,
                           file_path: Optional[str] = None,
                           ply_format: str = "binary",
                           include_colors: bool = True,
                           include_normals: bool = True,
                           coordinate_precision: int = 6) -> Dict[str, Any]:
        """Export elements to PLY format for point clouds and mesh analysis"""
        try:
            # Validate PLY format
            valid_formats = ["ascii", "binary", "binary_little_endian", "binary_big_endian"]
            if ply_format not in valid_formats:
                return {"status": "error", "message": f"ply_format must be one of: {', '.join(valid_formats)}"}
            
            # Validate coordinate precision
            if not isinstance(coordinate_precision, int) or coordinate_precision < 1 or coordinate_precision > 10:
                return {"status": "error", "message": "coordinate_precision must be an integer between 1 and 10"}
            
            # Prepare export parameters
            export_params: Dict[str, Any] = {
                "ply_format": ply_format,
                "include_colors": bool(include_colors),
                "include_normals": bool(include_normals),
                "coordinate_precision": coordinate_precision
            }
            
            # Validate element IDs if provided
            if element_ids is not None:
                if not isinstance(element_ids, list) or len(element_ids) == 0:
                    return {"status": "error", "message": "element_ids must be a non-empty list when provided"}
                
                validated_ids = []
                for element_id in element_ids:
                    validated_id = self.validate_element_id(element_id)
                    validated_ids.append(validated_id)
                
                export_params["element_ids"] = validated_ids
            else:
                export_params["export_all_visible"] = True
            
            # Validate file path if provided
            if file_path is not None:
                if not isinstance(file_path, str) or not file_path.strip():
                    return {"status": "error", "message": "file_path must be a non-empty string when provided"}
                
                # Ensure .ply extension
                file_path = file_path.strip()
                if not file_path.lower().endswith('.ply'):
                    file_path += '.ply'
                
                export_params["file_path"] = file_path
            
            return self.send_command("export_to_ply", export_params)
            
        except Exception as e:
            return {"status": "error", "message": f"export_to_ply failed: {e}"}

    async def export_to_stl(self, element_ids: Optional[List[int]] = None,
                           file_path: Optional[str] = None,
                           stl_format: str = "binary",
                           mesh_quality: str = "medium",
                           units: str = "mm",
                           merge_elements: bool = True) -> Dict[str, Any]:
        """Export elements to STL format for 3D printing"""
        try:
            # Validate STL format
            valid_formats = ["ascii", "binary"]
            if stl_format not in valid_formats:
                return {"status": "error", "message": f"stl_format must be one of: {', '.join(valid_formats)}"}
            
            # Validate mesh quality
            valid_qualities = ["low", "medium", "high", "ultra"]
            if mesh_quality not in valid_qualities:
                return {"status": "error", "message": f"mesh_quality must be one of: {', '.join(valid_qualities)}"}
            
            # Validate units
            valid_units = ["mm", "cm", "m", "inch"]
            if units not in valid_units:
                return {"status": "error", "message": f"units must be one of: {', '.join(valid_units)}"}
            
            # Prepare export parameters
            export_params: Dict[str, Any] = {
                "stl_format": stl_format,
                "mesh_quality": mesh_quality,
                "units": units,
                "merge_elements": bool(merge_elements)
            }
            
            # Validate element IDs if provided
            if element_ids is not None:
                if not isinstance(element_ids, list) or len(element_ids) == 0:
                    return {"status": "error", "message": "element_ids must be a non-empty list when provided"}
                
                validated_ids = []
                for element_id in element_ids:
                    validated_id = self.validate_element_id(element_id)
                    validated_ids.append(validated_id)
                
                export_params["element_ids"] = validated_ids
            else:
                export_params["export_all_visible"] = True
            
            # Validate file path if provided
            if file_path is not None:
                if not isinstance(file_path, str) or not file_path.strip():
                    return {"status": "error", "message": "file_path must be a non-empty string when provided"}
                
                # Ensure .stl extension
                file_path = file_path.strip()
                if not file_path.lower().endswith('.stl'):
                    file_path += '.stl'
                
                export_params["file_path"] = file_path
            
            return self.send_command("export_to_stl", export_params)
            
        except Exception as e:
            return {"status": "error", "message": f"export_to_stl failed: {e}"}

    async def export_to_gltf(self, element_ids: Optional[List[int]] = None,
                            file_path: Optional[str] = None,
                            gltf_format: str = "glb",
                            include_materials: bool = True,
                            include_animations: bool = False,
                            texture_resolution: int = 1024,
                            compression_level: str = "medium") -> Dict[str, Any]:
        """Export elements to glTF format for web 3D and real-time rendering"""
        try:
            # Validate glTF format
            valid_formats = ["gltf", "glb"]
            if gltf_format not in valid_formats:
                return {"status": "error", "message": f"gltf_format must be one of: {', '.join(valid_formats)}"}
            
            # Validate texture resolution
            valid_resolutions = [256, 512, 1024, 2048, 4096]
            if texture_resolution not in valid_resolutions:
                return {"status": "error", "message": f"texture_resolution must be one of: {', '.join(map(str, valid_resolutions))}"}
            
            # Validate compression level
            valid_compressions = ["none", "low", "medium", "high"]
            if compression_level not in valid_compressions:
                return {"status": "error", "message": f"compression_level must be one of: {', '.join(valid_compressions)}"}
            
            # Prepare export parameters
            export_params: Dict[str, Any] = {
                "gltf_format": gltf_format,
                "include_materials": bool(include_materials),
                "include_animations": bool(include_animations),
                "texture_resolution": texture_resolution,
                "compression_level": compression_level
            }
            
            # Validate element IDs if provided
            if element_ids is not None:
                if not isinstance(element_ids, list) or len(element_ids) == 0:
                    return {"status": "error", "message": "element_ids must be a non-empty list when provided"}
                
                validated_ids = []
                for element_id in element_ids:
                    validated_id = self.validate_element_id(element_id)
                    validated_ids.append(validated_id)
                
                export_params["element_ids"] = validated_ids
            else:
                export_params["export_all_visible"] = True
            
            # Validate file path if provided
            if file_path is not None:
                if not isinstance(file_path, str) or not file_path.strip():
                    return {"status": "error", "message": "file_path must be a non-empty string when provided"}
                
                # Ensure correct extension based on format
                file_path = file_path.strip()
                expected_ext = f'.{gltf_format}'
                if not file_path.lower().endswith(expected_ext):
                    file_path += expected_ext
                
                export_params["file_path"] = file_path
            
            return self.send_command("export_to_gltf", export_params)
            
        except Exception as e:
            return {"status": "error", "message": f"export_to_gltf failed: {e}"}

    async def export_to_x3d(self, element_ids: Optional[List[int]] = None,
                           file_path: Optional[str] = None,
                           x3d_version: str = "4.0",
                           encoding: str = "xml",
                           include_materials: bool = True,
                           include_lighting: bool = True,
                           include_navigation: bool = True,
                           compression: bool = False) -> Dict[str, Any]:
        """Export elements to X3D format for web-based 3D visualization and VR/AR"""
        try:
            # Validate X3D version
            valid_versions = ["3.0", "3.1", "3.2", "3.3", "4.0"]
            if x3d_version not in valid_versions:
                return {"status": "error", "message": f"x3d_version must be one of: {', '.join(valid_versions)}"}
            
            # Validate encoding
            valid_encodings = ["xml", "classic", "json", "binary"]
            if encoding not in valid_encodings:
                return {"status": "error", "message": f"encoding must be one of: {', '.join(valid_encodings)}"}
            
            # Prepare export parameters
            export_params: Dict[str, Any] = {
                "x3d_version": x3d_version,
                "encoding": encoding,
                "include_materials": bool(include_materials),
                "include_lighting": bool(include_lighting),
                "include_navigation": bool(include_navigation),
                "compression": bool(compression)
            }
            
            # Validate element IDs if provided
            if element_ids is not None:
                if not isinstance(element_ids, list) or len(element_ids) == 0:
                    return {"status": "error", "message": "element_ids must be a non-empty list when provided"}
                
                validated_ids = []
                for element_id in element_ids:
                    validated_id = self.validate_element_id(element_id)
                    validated_ids.append(validated_id)
                
                export_params["element_ids"] = validated_ids
            else:
                export_params["export_all_visible"] = True
            
            # Validate file path if provided
            if file_path is not None:
                if not isinstance(file_path, str) or not file_path.strip():
                    return {"status": "error", "message": "file_path must be a non-empty string when provided"}
                
                # Set extension based on encoding
                file_path = file_path.strip()
                if encoding == "xml":
                    if not file_path.lower().endswith(('.x3d', '.x3dv')):
                        file_path += '.x3d'
                elif encoding == "classic":
                    if not file_path.lower().endswith('.x3dv'):
                        file_path += '.x3dv'
                elif encoding == "json":
                    if not file_path.lower().endswith('.x3dj'):
                        file_path += '.x3dj'
                elif encoding == "binary":
                    if not file_path.lower().endswith('.x3db'):
                        file_path += '.x3db'
                
                export_params["file_path"] = file_path
            
            return self.send_command("export_to_x3d", export_params)
            
        except Exception as e:
            return {"status": "error", "message": f"export_to_x3d failed: {e}"}

    async def export_production_data(self, element_ids: Optional[List[int]] = None,
                                   file_path: Optional[str] = None,
                                   data_format: str = "json",
                                   include_cutting_list: bool = True,
                                   include_assembly_instructions: bool = True,
                                   include_hardware_list: bool = True,
                                   include_processing_data: bool = True,
                                   include_material_optimization: bool = True,
                                   group_by_production_step: bool = True) -> Dict[str, Any]:
        """Export comprehensive production data for manufacturing and assembly"""
        try:
            # Validate data format
            valid_formats = ["json", "xml", "csv", "xlsx", "yaml"]
            if data_format not in valid_formats:
                return {"status": "error", "message": f"data_format must be one of: {', '.join(valid_formats)}"}
            
            # Prepare export parameters
            export_params: Dict[str, Any] = {
                "data_format": data_format,
                "include_cutting_list": bool(include_cutting_list),
                "include_assembly_instructions": bool(include_assembly_instructions),
                "include_hardware_list": bool(include_hardware_list),
                "include_processing_data": bool(include_processing_data),
                "include_material_optimization": bool(include_material_optimization),
                "group_by_production_step": bool(group_by_production_step)
            }
            
            # Validate element IDs if provided
            if element_ids is not None:
                if not isinstance(element_ids, list) or len(element_ids) == 0:
                    return {"status": "error", "message": "element_ids must be a non-empty list when provided"}
                
                validated_ids = []
                for element_id in element_ids:
                    validated_id = self.validate_element_id(element_id)
                    validated_ids.append(validated_id)
                
                export_params["element_ids"] = validated_ids
            else:
                export_params["export_all_visible"] = True
            
            # Validate file path if provided
            if file_path is not None:
                if not isinstance(file_path, str) or not file_path.strip():
                    return {"status": "error", "message": "file_path must be a non-empty string when provided"}
                
                # Ensure correct extension
                file_path = file_path.strip()
                expected_ext = f'.{data_format}'
                if not file_path.lower().endswith(expected_ext):
                    file_path += expected_ext
                
                export_params["file_path"] = file_path
            
            return self.send_command("export_production_data", export_params)
            
        except Exception as e:
            return {"status": "error", "message": f"export_production_data failed: {e}"}

    async def export_to_fbx(self, element_ids: Optional[List[int]] = None,
                           file_path: Optional[str] = None,
                           fbx_format: str = "binary",
                           fbx_version: str = "2020",
                           include_materials: bool = True,
                           include_textures: bool = True,
                           include_animations: bool = False) -> Dict[str, Any]:
        """Export elements to FBX format for animation, gaming, and 3D applications"""
        try:
            # Validate FBX format
            valid_formats = ["binary", "ascii", "encrypted"]
            if fbx_format not in valid_formats:
                return {"status": "error", "message": f"fbx_format must be one of: {', '.join(valid_formats)}"}
            
            # Validate FBX version
            valid_versions = ["2020", "2019", "2018", "2016", "2014", "2013", "6.0"]
            if fbx_version not in valid_versions:
                return {"status": "error", "message": f"fbx_version must be one of: {', '.join(valid_versions)}"}
            
            # Map format to API format codes
            format_map = {
                "binary": 1,
                "ascii": 2,
                "encrypted": 3,
                "6.0_binary": 4,
                "6.0_ascii": 5,
                "6.0_encrypted": 6
            }
            
            # Adjust format for 6.0 version
            api_format = format_map.get(fbx_format, 1)
            if fbx_version == "6.0":
                if fbx_format == "binary":
                    api_format = 4
                elif fbx_format == "ascii":
                    api_format = 5
                elif fbx_format == "encrypted":
                    api_format = 6
            
            # Prepare export parameters
            export_params: Dict[str, Any] = {
                "fbx_format": api_format,
                "fbx_version": fbx_version,
                "include_materials": bool(include_materials),
                "include_textures": bool(include_textures),
                "include_animations": bool(include_animations)
            }
            
            # Validate element IDs if provided
            if element_ids is not None:
                if not isinstance(element_ids, list) or len(element_ids) == 0:
                    return {"status": "error", "message": "element_ids must be a non-empty list when provided"}
                
                validated_ids = []
                for element_id in element_ids:
                    validated_id = self.validate_element_id(element_id)
                    validated_ids.append(validated_id)
                
                export_params["element_ids"] = validated_ids
            else:
                export_params["export_all_visible"] = True
            
            # Validate file path if provided
            if file_path is not None:
                if not isinstance(file_path, str) or not file_path.strip():
                    return {"status": "error", "message": "file_path must be a non-empty string when provided"}
                
                # Ensure .fbx extension
                file_path = file_path.strip()
                if not file_path.lower().endswith('.fbx'):
                    file_path += '.fbx'
                
                export_params["file_path"] = file_path
            
            return self.send_command("export_to_fbx", export_params)
            
        except Exception as e:
            return {"status": "error", "message": f"export_to_fbx failed: {e}"}

    async def export_to_webgl(self, element_ids: Optional[List[int]] = None,
                             file_path: Optional[str] = None,
                             web_quality: str = "medium",
                             include_materials: bool = True,
                             include_textures: bool = True,
                             compression: bool = True,
                             embed_viewer: bool = True) -> Dict[str, Any]:
        """Export elements to WebGL format for interactive web 3D visualization"""
        try:
            # Validate web quality
            valid_qualities = ["low", "medium", "high", "ultra"]
            if web_quality not in valid_qualities:
                return {"status": "error", "message": f"web_quality must be one of: {', '.join(valid_qualities)}"}
            
            # Prepare export parameters
            export_params: Dict[str, Any] = {
                "web_quality": web_quality,
                "include_materials": bool(include_materials),
                "include_textures": bool(include_textures),
                "compression": bool(compression),
                "embed_viewer": bool(embed_viewer)
            }
            
            # Validate element IDs if provided
            if element_ids is not None:
                if not isinstance(element_ids, list) or len(element_ids) == 0:
                    return {"status": "error", "message": "element_ids must be a non-empty list when provided"}
                
                validated_ids = []
                for element_id in element_ids:
                    validated_id = self.validate_element_id(element_id)
                    validated_ids.append(validated_id)
                
                export_params["element_ids"] = validated_ids
            else:
                export_params["export_all_visible"] = True
            
            # Validate file path if provided
            if file_path is not None:
                if not isinstance(file_path, str) or not file_path.strip():
                    return {"status": "error", "message": "file_path must be a non-empty string when provided"}
                
                # Ensure .html extension
                file_path = file_path.strip()
                if not file_path.lower().endswith('.html'):
                    file_path += '.html'
                
                export_params["file_path"] = file_path
            
            return self.send_command("export_to_webgl", export_params)
            
        except Exception as e:
            return {"status": "error", "message": f"export_to_webgl failed: {e}"}

    async def export_to_sat(self, element_ids: Optional[List[int]] = None,
                           file_path: Optional[str] = None,
                           scale_factor: float = 1.0,
                           binary_format: bool = True,
                           sat_version: int = 25000,
                           include_drillings: bool = False,
                           drilling_mode: str = "none") -> Dict[str, Any]:
        """Export elements to SAT format (ACIS) for advanced CAD applications"""
        try:
            # Validate scale factor
            if not isinstance(scale_factor, (int, float)) or scale_factor <= 0:
                return {"status": "error", "message": "scale_factor must be a positive number"}
            
            # Validate SAT version
            valid_versions = [20000, 21000, 22000, 23000, 24000, 25000, 26000, 27000, 28000]
            if sat_version not in valid_versions:
                return {"status": "error", "message": f"sat_version must be one of: {', '.join(map(str, valid_versions))}"}
            
            # Validate drilling mode
            valid_drilling_modes = ["none", "cut", "extrude"]
            if drilling_mode not in valid_drilling_modes:
                return {"status": "error", "message": f"drilling_mode must be one of: {', '.join(valid_drilling_modes)}"}
            
            # Prepare export parameters
            export_params: Dict[str, Any] = {
                "scale_factor": float(scale_factor),
                "binary_format": bool(binary_format),
                "sat_version": sat_version,
                "include_drillings": bool(include_drillings),
                "drilling_mode": drilling_mode
            }
            
            # Validate element IDs if provided
            if element_ids is not None:
                if not isinstance(element_ids, list) or len(element_ids) == 0:
                    return {"status": "error", "message": "element_ids must be a non-empty list when provided"}
                
                validated_ids = []
                for element_id in element_ids:
                    validated_id = self.validate_element_id(element_id)
                    validated_ids.append(validated_id)
                
                export_params["element_ids"] = validated_ids
            else:
                export_params["export_all_visible"] = True
            
            # Validate file path if provided
            if file_path is not None:
                if not isinstance(file_path, str) or not file_path.strip():
                    return {"status": "error", "message": "file_path must be a non-empty string when provided"}
                
                # Ensure .sat extension
                file_path = file_path.strip()
                if not file_path.lower().endswith('.sat'):
                    file_path += '.sat'
                
                export_params["file_path"] = file_path
            
            return self.send_command("export_to_sat", export_params)
            
        except Exception as e:
            return {"status": "error", "message": f"export_to_sat failed: {e}"}

    async def export_to_dstv(self, element_ids: Optional[List[int]] = None,
                            file_path: Optional[str] = None,
                            dstv_version: str = "NC1",
                            units: str = "mm",
                            include_material_info: bool = True,
                            include_processing: bool = True,
                            steel_grade: str = "S355") -> Dict[str, Any]:
        """Export elements to DSTV format for steel construction and CNC machines"""
        try:
            # Validate DSTV version
            valid_versions = ["NC1", "NC2", "NC3", "PSL", "DSTV2"]
            if dstv_version not in valid_versions:
                return {"status": "error", "message": f"dstv_version must be one of: {', '.join(valid_versions)}"}
            
            # Validate units
            valid_units = ["mm", "cm", "m", "inch"]
            if units not in valid_units:
                return {"status": "error", "message": f"units must be one of: {', '.join(valid_units)}"}
            
            # Validate steel grade
            valid_steel_grades = ["S235", "S275", "S355", "S420", "S460", "CUSTOM"]
            if steel_grade not in valid_steel_grades:
                return {"status": "error", "message": f"steel_grade must be one of: {', '.join(valid_steel_grades)}"}
            
            # Prepare export parameters
            export_params: Dict[str, Any] = {
                "dstv_version": dstv_version,
                "units": units,
                "include_material_info": bool(include_material_info),
                "include_processing": bool(include_processing),
                "steel_grade": steel_grade
            }
            
            # Validate element IDs if provided
            if element_ids is not None:
                if not isinstance(element_ids, list) or len(element_ids) == 0:
                    return {"status": "error", "message": "element_ids must be a non-empty list when provided"}
                
                validated_ids = []
                for element_id in element_ids:
                    validated_id = self.validate_element_id(element_id)
                    validated_ids.append(validated_id)
                
                export_params["element_ids"] = validated_ids
            else:
                export_params["export_all_visible"] = True
            
            # Validate file path if provided
            if file_path is not None:
                if not isinstance(file_path, str) or not file_path.strip():
                    return {"status": "error", "message": "file_path must be a non-empty string when provided"}
                
                # Ensure .nc or .dstv extension
                file_path = file_path.strip()
                if not file_path.lower().endswith(('.nc', '.dstv', '.nc1', '.nc2')):
                    if dstv_version.startswith('NC'):
                        file_path += '.nc'
                    else:
                        file_path += '.dstv'
                
                export_params["file_path"] = file_path
            
            return self.send_command("export_to_dstv", export_params)
            
        except Exception as e:
            return {"status": "error", "message": f"export_to_dstv failed: {e}"}

    async def export_step_with_drillings(self, element_ids: Optional[List[int]] = None,
                                        file_path: Optional[str] = None,
                                        drilling_mode: str = "extrude",
                                        scale_factor: float = 1.0,
                                        step_version: int = 214,
                                        text_mode: bool = False,
                                        imperial_units: bool = False) -> Dict[str, Any]:
        """Export elements to STEP format with drilling processing for manufacturing"""
        try:
            # Validate drilling mode
            valid_drilling_modes = ["extrude", "cut", "none"]
            if drilling_mode not in valid_drilling_modes:
                return {"status": "error", "message": f"drilling_mode must be one of: {', '.join(valid_drilling_modes)}"}
            
            # Validate scale factor
            if not isinstance(scale_factor, (int, float)) or scale_factor <= 0:
                return {"status": "error", "message": "scale_factor must be a positive number"}
            
            # Validate STEP version
            valid_versions = [203, 214, 242]
            if step_version not in valid_versions:
                return {"status": "error", "message": f"step_version must be one of: {', '.join(map(str, valid_versions))}"}
            
            # Prepare export parameters
            export_params: Dict[str, Any] = {
                "drilling_mode": drilling_mode,
                "scale_factor": float(scale_factor),
                "step_version": step_version,
                "text_mode": bool(text_mode),
                "imperial_units": bool(imperial_units)
            }
            
            # Validate element IDs if provided
            if element_ids is not None:
                if not isinstance(element_ids, list) or len(element_ids) == 0:
                    return {"status": "error", "message": "element_ids must be a non-empty list when provided"}
                
                validated_ids = []
                for element_id in element_ids:
                    validated_id = self.validate_element_id(element_id)
                    validated_ids.append(validated_id)
                
                export_params["element_ids"] = validated_ids
            else:
                export_params["export_all_visible"] = True
            
            # Validate file path if provided
            if file_path is not None:
                if not isinstance(file_path, str) or not file_path.strip():
                    return {"status": "error", "message": "file_path must be a non-empty string when provided"}
                
                # Ensure .step or .stp extension
                file_path = file_path.strip()
                if not file_path.lower().endswith(('.step', '.stp')):
                    file_path += '.step'
                
                export_params["file_path"] = file_path
            
            return self.send_command("export_step_with_drillings", export_params)
            
        except Exception as e:
            return {"status": "error", "message": f"export_step_with_drillings failed: {e}"}

    async def export_btl_for_nesting(self, file_path: Optional[str] = None,
                                    nesting_parameters: Optional[Dict[str, Any]] = None,
                                    optimization_method: str = "area",
                                    material_efficiency: bool = True,
                                    sheet_size: Optional[List[float]] = None,
                                    kerf_width: float = 3.0) -> Dict[str, Any]:
        """Export BTL file optimized for nesting operations and material efficiency"""
        try:
            # Validate optimization method
            valid_methods = ["area", "length", "perimeter", "cost", "waste_minimization"]
            if optimization_method not in valid_methods:
                return {"status": "error", "message": f"optimization_method must be one of: {', '.join(valid_methods)}"}
            
            # Validate kerf width
            if not isinstance(kerf_width, (int, float)) or kerf_width < 0:
                return {"status": "error", "message": "kerf_width must be a non-negative number (mm)"}
            
            # Validate sheet size if provided
            if sheet_size is not None:
                if not isinstance(sheet_size, list) or len(sheet_size) != 2:
                    return {"status": "error", "message": "sheet_size must be a list of 2 numbers [width, height] in mm"}
                
                try:
                    sheet_size = [float(x) for x in sheet_size]
                    if any(x <= 0 for x in sheet_size):
                        return {"status": "error", "message": "sheet_size dimensions must be positive numbers"}
                except (ValueError, TypeError):
                    return {"status": "error", "message": "sheet_size must contain valid numbers"}
            
            # Prepare nesting parameters
            default_nesting_params = {
                "auto_rotate": True,
                "allow_mirroring": False,
                "minimum_spacing": 5.0,
                "edge_spacing": 10.0,
                "grain_direction": "any",
                "priority_optimization": optimization_method
            }
            
            # Merge with user parameters
            final_nesting_params = default_nesting_params.copy()
            if nesting_parameters:
                final_nesting_params.update(nesting_parameters)
            
            # Prepare export parameters
            export_params: Dict[str, Any] = {
                "nesting_parameters": final_nesting_params,
                "optimization_method": optimization_method,
                "material_efficiency": bool(material_efficiency),
                "kerf_width": float(kerf_width)
            }
            
            if sheet_size:
                export_params["sheet_size"] = sheet_size
            
            # Validate file path if provided
            if file_path is not None:
                if not isinstance(file_path, str) or not file_path.strip():
                    return {"status": "error", "message": "file_path must be a non-empty string when provided"}
                
                # Ensure .btl extension
                file_path = file_path.strip()
                if not file_path.lower().endswith('.btl'):
                    file_path += '.btl'
                
                export_params["file_path"] = file_path
            
            return self.send_command("export_btl_for_nesting", export_params)
            
        except Exception as e:
            return {"status": "error", "message": f"export_btl_for_nesting failed: {e}"}