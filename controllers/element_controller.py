"""
Element controller for element operations
"""
from typing import Dict, Any, List, Optional
from .base_controller import BaseController

class ElementController(BaseController):
    """Controller for element operations"""
    
    def __init__(self) -> None:
        super().__init__("ElementController")
    
    async def create_beam(self, p1: List[float], p2: List[float], width: float, height: float, 
                         p3: Optional[List[float]] = None) -> Dict[str, Any]:
        """Create a rectangular beam"""
        args: Dict[str, Any] = {
            "p1": p1,
            "p2": p2, 
            "width": width,
            "height": height
        }
        if p3 is not None:
            args["p3"] = p3
        
        return self.send_command("create_beam", args)
    
    async def create_panel(self, p1: List[float], p2: List[float], width: float, thickness: float,
                          p3: Optional[List[float]] = None) -> Dict[str, Any]:
        """Create a rectangular panel"""
        args: Dict[str, Any] = {
            "p1": p1,
            "p2": p2,
            "width": width, 
            "thickness": thickness
        }
        if p3 is not None:
            args["p3"] = p3
        
        return self.send_command("create_panel", args)
    
    async def get_active_element_ids(self) -> Dict[str, Any]:
        """Get active element IDs"""
        return self.send_command("get_active_element_ids")
    
    async def get_all_element_ids(self) -> Dict[str, Any]:
        """Get all element IDs in the model"""
        return self.send_command("get_all_element_ids")
    
    async def get_visible_element_ids(self) -> Dict[str, Any]:
        """Get visible element IDs"""
        return self.send_command("get_visible_element_ids")
    
    async def get_element_info(self, element_id: int) -> Dict[str, Any]:
        """Get element information"""
        element_id = self.validate_element_id(element_id)
        return self.send_command("get_element_info", {"element_id": element_id})
    
    async def delete_elements(self, element_ids: List[int]) -> Dict[str, Any]:
        """Delete elements from the model"""
        if not isinstance(element_ids, list):
            raise ValueError("element_ids must be a list")
        
        validated_ids = [self.validate_element_id(eid) for eid in element_ids]
        return self.send_command("delete_elements", {"element_ids": validated_ids})
    
    async def copy_elements(self, element_ids: List[int], copy_vector: List[float]) -> Dict[str, Any]:
        """Copy elements with a given vector offset"""
        if not isinstance(element_ids, list):
            raise ValueError("element_ids must be a list")
        if not isinstance(copy_vector, list) or len(copy_vector) != 3:
            raise ValueError("copy_vector must be a list of 3 numbers [x, y, z]")
        
        validated_ids = [self.validate_element_id(eid) for eid in element_ids]
        return self.send_command("copy_elements", {
            "element_ids": validated_ids,
            "copy_vector": copy_vector
        })
    
    async def move_element(self, element_ids: List[int], move_vector: List[float]) -> Dict[str, Any]:
        """Move elements by a given vector offset"""
        if not isinstance(element_ids, list):
            raise ValueError("element_ids must be a list")
        if not isinstance(move_vector, list) or len(move_vector) != 3:
            raise ValueError("move_vector must be a list of 3 numbers [x, y, z]")
        
        validated_ids = [self.validate_element_id(eid) for eid in element_ids]
        return self.send_command("move_element", {
            "element_ids": validated_ids,
            "move_vector": move_vector
        })
    
    async def get_user_element_ids(self, count: Optional[int] = None) -> Dict[str, Any]:
        """Get user-selected elements with optional count limit"""
        args: Dict[str, Any] = {}
        if count is not None:
            if not isinstance(count, int) or count <= 0:
                raise ValueError("count must be a positive integer")
            args["count"] = count
        
        return self.send_command("get_user_element_ids", args)
    
    async def duplicate_elements(self, element_ids: List[int]) -> Dict[str, Any]:
        """Duplicate elements at the same location (no offset)"""
        try:
            if not isinstance(element_ids, list) or not element_ids:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            return self.send_command("duplicate_elements", {"element_ids": validated_ids})
            
        except Exception as e:
            return {"status": "error", "message": f"duplicate_elements failed: {e}"}
    
    async def stretch_elements(self, element_ids: List[int], stretch_vector: List[float], 
                             stretch_factor: float = 1.0) -> Dict[str, Any]:
        """Stretch/extend elements along a specified vector with given factor"""
        try:
            if not isinstance(element_ids, list) or not element_ids:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            if not isinstance(stretch_vector, list) or len(stretch_vector) != 3:
                return {"status": "error", "message": "stretch_vector must be a list of 3 coordinates [x,y,z]"}
            
            if not isinstance(stretch_factor, (int, float)) or stretch_factor <= 0:
                return {"status": "error", "message": "stretch_factor must be a positive number"}
            
            validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            validated_vector = [float(coord) for coord in stretch_vector]
            
            args = {
                "element_ids": validated_ids,
                "stretch_vector": validated_vector,
                "stretch_factor": float(stretch_factor)
            }
            
            return self.send_command("stretch_elements", args)
            
        except Exception as e:
            return {"status": "error", "message": f"stretch_elements failed: {e}"}
    
    async def scale_elements(self, element_ids: List[int], scale_factor: float, 
                           origin_point: Optional[List[float]] = None) -> Dict[str, Any]:
        """Scale elements by a factor around an origin point"""
        try:
            if not isinstance(element_ids, list) or not element_ids:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            if not isinstance(scale_factor, (int, float)) or scale_factor <= 0:
                return {"status": "error", "message": "scale_factor must be a positive number"}
            
            validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            
            args = {
                "element_ids": validated_ids,
                "scale_factor": float(scale_factor)
            }
            
            # Add origin point if provided, otherwise use element center
            if origin_point is not None:
                if not isinstance(origin_point, list) or len(origin_point) != 3:
                    return {"status": "error", "message": "origin_point must be a list of 3 coordinates [x,y,z]"}
                args["origin_point"] = [float(coord) for coord in origin_point]
            
            return self.send_command("scale_elements", args)
            
        except Exception as e:
            return {"status": "error", "message": f"scale_elements failed: {e}"}
    
    async def mirror_elements(self, element_ids: List[int], mirror_plane_point: List[float], 
                            mirror_plane_normal: List[float]) -> Dict[str, Any]:
        """Mirror elements across a plane defined by a point and normal vector"""
        try:
            if not isinstance(element_ids, list) or not element_ids:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            if not isinstance(mirror_plane_point, list) or len(mirror_plane_point) != 3:
                return {"status": "error", "message": "mirror_plane_point must be a list of 3 coordinates [x,y,z]"}
            
            if not isinstance(mirror_plane_normal, list) or len(mirror_plane_normal) != 3:
                return {"status": "error", "message": "mirror_plane_normal must be a list of 3 coordinates [x,y,z]"}
            
            validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            validated_point = [float(coord) for coord in mirror_plane_point]
            validated_normal = [float(coord) for coord in mirror_plane_normal]
            
            # Check if normal vector is not zero
            normal_length = sum(coord ** 2 for coord in validated_normal) ** 0.5
            if normal_length < 1e-10:
                return {"status": "error", "message": "mirror_plane_normal cannot be a zero vector"}
            
            args = {
                "element_ids": validated_ids,
                "mirror_plane_point": validated_point,
                "mirror_plane_normal": validated_normal
            }
            
            return self.send_command("mirror_elements", args)
            
        except Exception as e:
            return {"status": "error", "message": f"mirror_elements failed: {e}"}
    
    async def create_solid_wood_panel(self, p1: List[float], p2: List[float], 
                                    thickness: float, wood_type: str = "Generic", 
                                    p3: Optional[List[float]] = None) -> Dict[str, Any]:
        """Create a solid wood panel with specified wood type and grain direction"""
        try:
            if not isinstance(p1, list) or len(p1) != 3:
                return {"status": "error", "message": "p1 must be a list of 3 coordinates [x,y,z]"}
            
            if not isinstance(p2, list) or len(p2) != 3:
                return {"status": "error", "message": "p2 must be a list of 3 coordinates [x,y,z]"}
            
            if not isinstance(thickness, (int, float)) or thickness <= 0:
                return {"status": "error", "message": "thickness must be a positive number"}
            
            if not isinstance(wood_type, str) or not wood_type.strip():
                return {"status": "error", "message": "wood_type must be a non-empty string"}
            
            validated_p1 = [float(coord) for coord in p1]
            validated_p2 = [float(coord) for coord in p2]
            
            args = {
                "p1": validated_p1,
                "p2": validated_p2,
                "thickness": float(thickness),
                "wood_type": wood_type.strip()
            }
            
            if p3 is not None:
                validated_p3 = self.validate_point_3d(p3, "p3")
                if validated_p3 is not None:
                    args["p3"] = validated_p3
            
            return self.send_command("create_solid_wood_panel", args)
            
        except Exception as e:
            return {"status": "error", "message": f"create_solid_wood_panel failed: {e}"}
    
    # --- EXTENDED ELEMENT CREATION METHODS ---
    
    async def create_circular_beam_points(self, diameter: float, p1: List[float], p2: List[float], 
                                        p3: Optional[List[float]] = None) -> Dict[str, Any]:
        """Create a circular beam using points"""
        try:
            if not isinstance(diameter, (int, float)) or diameter <= 0:
                return {"status": "error", "message": "diameter must be a positive number"}
            
            validated_p1 = self.validate_point_3d(p1, "p1")
            validated_p2 = self.validate_point_3d(p2, "p2")
            if validated_p1 is None or validated_p2 is None:
                return {"status": "error", "message": "Invalid p1 or p2 coordinates"}
            
            args = {
                "diameter": float(diameter),
                "p1": validated_p1,
                "p2": validated_p2
            }
            
            if p3 is not None:
                validated_p3 = self.validate_point_3d(p3, "p3")
                if validated_p3 is not None:
                    args["p3"] = validated_p3
            
            return self.send_command("create_circular_beam_points", args)
            
        except Exception as e:
            return {"status": "error", "message": f"create_circular_beam_points failed: {e}"}
    
    async def create_square_beam_points(self, width: float, p1: List[float], p2: List[float], 
                                      p3: Optional[List[float]] = None) -> Dict[str, Any]:
        """Create a square beam using points"""
        try:
            if not isinstance(width, (int, float)) or width <= 0:
                return {"status": "error", "message": "width must be a positive number"}
            
            validated_p1 = self.validate_point_3d(p1, "p1")
            validated_p2 = self.validate_point_3d(p2, "p2")
            if validated_p1 is None or validated_p2 is None:
                return {"status": "error", "message": "Invalid p1 or p2 coordinates"}
            
            args = {
                "width": float(width),
                "p1": validated_p1,
                "p2": validated_p2
            }
            
            if p3 is not None:
                validated_p3 = self.validate_point_3d(p3, "p3")
                if validated_p3 is not None:
                    args["p3"] = validated_p3
            
            return self.send_command("create_square_beam_points", args)
            
        except Exception as e:
            return {"status": "error", "message": f"create_square_beam_points failed: {e}"}
    
    async def create_standard_beam_points(self, standard_element_name: str, p1: List[float], p2: List[float], 
                                        p3: Optional[List[float]] = None) -> Dict[str, Any]:
        """Create a standard beam from library using points"""
        try:
            if not isinstance(standard_element_name, str) or not standard_element_name.strip():
                return {"status": "error", "message": "standard_element_name must be a non-empty string"}
            
            validated_p1 = self.validate_point_3d(p1, "p1")
            validated_p2 = self.validate_point_3d(p2, "p2")
            if validated_p1 is None or validated_p2 is None:
                return {"status": "error", "message": "Invalid p1 or p2 coordinates"}
            
            args = {
                "standard_element_name": standard_element_name.strip(),
                "p1": validated_p1,
                "p2": validated_p2
            }
            
            if p3 is not None:
                validated_p3 = self.validate_point_3d(p3, "p3")
                if validated_p3 is not None:
                    args["p3"] = validated_p3
            
            return self.send_command("create_standard_beam_points", args)
            
        except Exception as e:
            return {"status": "error", "message": f"create_standard_beam_points failed: {e}"}
    
    async def create_standard_panel_points(self, standard_element_name: str, p1: List[float], p2: List[float], 
                                         p3: Optional[List[float]] = None) -> Dict[str, Any]:
        """Create a standard panel from library using points"""
        try:
            if not isinstance(standard_element_name, str) or not standard_element_name.strip():
                return {"status": "error", "message": "standard_element_name must be a non-empty string"}
            
            validated_p1 = self.validate_point_3d(p1, "p1")
            validated_p2 = self.validate_point_3d(p2, "p2")
            if validated_p1 is None or validated_p2 is None:
                return {"status": "error", "message": "Invalid p1 or p2 coordinates"}
            
            args = {
                "standard_element_name": standard_element_name.strip(),
                "p1": validated_p1,
                "p2": validated_p2
            }
            
            if p3 is not None:
                validated_p3 = self.validate_point_3d(p3, "p3")
                if validated_p3 is not None:
                    args["p3"] = validated_p3
            
            return self.send_command("create_standard_panel_points", args)
            
        except Exception as e:
            return {"status": "error", "message": f"create_standard_panel_points failed: {e}"}
    
    async def create_drilling_points(self, diameter: float, p1: List[float], p2: List[float]) -> Dict[str, Any]:
        """Create a drilling element using points"""
        try:
            if not isinstance(diameter, (int, float)) or diameter <= 0:
                return {"status": "error", "message": "diameter must be a positive number"}
            
            validated_p1 = self.validate_point_3d(p1, "p1")
            validated_p2 = self.validate_point_3d(p2, "p2")
            if validated_p1 is None or validated_p2 is None:
                return {"status": "error", "message": "Invalid p1 or p2 coordinates"}
            
            args = {
                "diameter": float(diameter),
                "p1": validated_p1,
                "p2": validated_p2
            }
            
            return self.send_command("create_drilling_points", args)
            
        except Exception as e:
            return {"status": "error", "message": f"create_drilling_points failed: {e}"}
    
    async def create_polygon_beam(self, polygon_vertices: List[List[float]], thickness: float, 
                                xl: List[float], zl: List[float]) -> Dict[str, Any]:
        """Create a polygon beam element"""
        try:
            if not isinstance(polygon_vertices, list) or len(polygon_vertices) < 3:
                return {"status": "error", "message": "polygon_vertices must be a list with at least 3 points"}
            
            if not isinstance(thickness, (int, float)) or thickness <= 0:
                return {"status": "error", "message": "thickness must be a positive number"}
            
            # Validate all vertices
            validated_vertices = []
            for i, vertex in enumerate(polygon_vertices):
                validated_vertex = self.validate_point_3d(vertex, f"vertex_{i}")
                if validated_vertex is None:
                    return {"status": "error", "message": f"Invalid vertex at index {i}"}
                validated_vertices.append(validated_vertex)
            
            validated_xl = self.validate_point_3d(xl, "xl")
            validated_zl = self.validate_point_3d(zl, "zl")
            if validated_xl is None or validated_zl is None:
                return {"status": "error", "message": "Invalid xl or zl vector"}
            
            args = {
                "polygon_vertices": validated_vertices,
                "thickness": float(thickness),
                "xl": validated_xl,
                "zl": validated_zl
            }
            
            return self.send_command("create_polygon_beam", args)
            
        except Exception as e:
            return {"status": "error", "message": f"create_polygon_beam failed: {e}"}

    
    # --- ELEMENT QUERY/FILTER METHODS ---
    
    async def get_elements_by_type(self, element_type: str) -> Dict[str, Any]:
        """Find all elements of a specific type"""
        try:
            if not isinstance(element_type, str) or not element_type.strip():
                return {"status": "error", "message": "element_type must be a non-empty string"}
            
            return self.send_command("get_elements_by_type", {"element_type": element_type.strip()})
            
        except Exception as e:
            return {"status": "error", "message": f"get_elements_by_type failed: {e}"}
    
    async def filter_elements_by_material(self, material_name: str) -> Dict[str, Any]:
        """Filter elements by material name"""
        try:
            if not isinstance(material_name, str) or not material_name.strip():
                return {"status": "error", "message": "material_name must be a non-empty string"}
            
            return self.send_command("filter_elements_by_material", {"material_name": material_name.strip()})
            
        except Exception as e:
            return {"status": "error", "message": f"filter_elements_by_material failed: {e}"}
    
    async def get_elements_in_group(self, group_name: str) -> Dict[str, Any]:
        """Find all elements in a specific group"""
        try:
            if not isinstance(group_name, str) or not group_name.strip():
                return {"status": "error", "message": "group_name must be a non-empty string"}
            
            return self.send_command("get_elements_in_group", {"group_name": group_name.strip()})
            
        except Exception as e:
            return {"status": "error", "message": f"get_elements_in_group failed: {e}"}

    async def get_elements_by_color(self, color_id: int) -> Dict[str, Any]:
        """Find all elements with a specific color ID"""
        try:
            if not isinstance(color_id, int) or color_id < 1 or color_id > 255:
                return {"status": "error", "message": "color_id must be an integer between 1 and 255"}
            
            return self.send_command("get_elements_by_color", {"color_id": color_id})
            
        except Exception as e:
            return {"status": "error", "message": f"get_elements_by_color failed: {e}"}

    async def get_elements_by_layer(self, layer_name: str) -> Dict[str, Any]:
        """Find all elements on a specific layer"""
        try:
            if not isinstance(layer_name, str) or not layer_name.strip():
                return {"status": "error", "message": "layer_name must be a non-empty string"}
            
            return self.send_command("get_elements_by_layer", {"layer_name": layer_name.strip()})
            
        except Exception as e:
            return {"status": "error", "message": f"get_elements_by_layer failed: {e}"}

    async def get_elements_by_dimension_range(self, dimension_type: str, min_value: float, max_value: float) -> Dict[str, Any]:
        """Find all elements within a specific dimension range"""
        try:
            # Validate dimension type
            valid_dimensions = ["width", "height", "length", "volume", "weight"]
            if not isinstance(dimension_type, str) or dimension_type.lower() not in valid_dimensions:
                return {"status": "error", "message": f"dimension_type must be one of: {', '.join(valid_dimensions)}"}
            
            # Validate range values
            if not isinstance(min_value, (int, float)) or not isinstance(max_value, (int, float)):
                return {"status": "error", "message": "min_value and max_value must be numeric"}
            
            if min_value < 0 or max_value < 0:
                return {"status": "error", "message": "min_value and max_value must be non-negative"}
            
            if min_value > max_value:
                return {"status": "error", "message": "min_value must be less than or equal to max_value"}
            
            # Convert to float for consistency
            min_val = float(min_value)
            max_val = float(max_value)
            dim_type = dimension_type.lower()
            
            return self.send_command("get_elements_by_dimension_range", {
                "dimension_type": dim_type,
                "min_value": min_val,
                "max_value": max_val
            })
            
        except Exception as e:
            return {"status": "error", "message": f"get_elements_by_dimension_range failed: {e}"}
    
    # --- STATISTICS METHODS ---
    
    async def get_element_count_by_type(self) -> Dict[str, Any]:
        """Get count statistics of all elements by type"""
        try:
            return self.send_command("get_element_count_by_type")
            
        except Exception as e:
            return {"status": "error", "message": f"get_element_count_by_type failed: {e}"}
    
    async def get_material_statistics(self) -> Dict[str, Any]:
        """Get material usage statistics for the entire model"""
        try:
            return self.send_command("get_material_statistics")
            
        except Exception as e:
            return {"status": "error", "message": f"get_material_statistics failed: {e}"}
    
    async def get_group_statistics(self) -> Dict[str, Any]:
        """Get group usage statistics for the entire model"""
        try:
            return self.send_command("get_group_statistics")
            
        except Exception as e:
            return {"status": "error", "message": f"get_group_statistics failed: {e}"}
    
    # --- ELEMENT CONNECTION METHODS ---
    
    async def join_elements(self, element_ids: List[int]) -> Dict[str, Any]:
        """Join multiple elements together"""
        try:
            if not isinstance(element_ids, list) or len(element_ids) < 2:
                return {"status": "error", "message": "element_ids must be a list with at least 2 element IDs"}
            
            validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            return self.send_command("join_elements", {"element_ids": validated_ids})
            
        except Exception as e:
            return {"status": "error", "message": f"join_elements failed: {e}"}
    
    async def unjoin_elements(self, element_ids: List[int]) -> Dict[str, Any]:
        """Unjoin/disconnect previously joined elements"""
        try:
            if not isinstance(element_ids, list) or not element_ids:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            return self.send_command("unjoin_elements", {"element_ids": validated_ids})
            
        except Exception as e:
            return {"status": "error", "message": f"unjoin_elements failed: {e}"}
    
    # --- WOOD JOINT CUTTING METHODS ---
    
    async def cut_corner_lap(self, element_ids: List[int], cut_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create corner lap cuts between elements"""
        try:
            if not isinstance(element_ids, list) or len(element_ids) < 2:
                return {"status": "error", "message": "element_ids must be a list with at least 2 element IDs"}
            
            validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            
            args: Dict[str, Any] = {"element_ids": validated_ids}
            if cut_params is not None:
                args["cut_params"] = cut_params
            
            return self.send_command("cut_corner_lap", args)
            
        except Exception as e:
            return {"status": "error", "message": f"cut_corner_lap failed: {e}"}
    
    async def cut_cross_lap(self, element_ids: List[int], cut_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create cross lap cuts between elements"""
        try:
            if not isinstance(element_ids, list) or len(element_ids) < 2:
                return {"status": "error", "message": "element_ids must be a list with at least 2 element IDs"}
            
            validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            
            args: Dict[str, Any] = {"element_ids": validated_ids}
            if cut_params is not None:
                args["cut_params"] = cut_params
            
            return self.send_command("cut_cross_lap", args)
            
        except Exception as e:
            return {"status": "error", "message": f"cut_cross_lap failed: {e}"}
    
    async def cut_half_lap(self, element_ids: List[int], cut_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create half lap cuts between elements"""
        try:
            if not isinstance(element_ids, list) or len(element_ids) < 2:
                return {"status": "error", "message": "element_ids must be a list with at least 2 element IDs"}
            
            validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            
            args: Dict[str, Any] = {"element_ids": validated_ids}
            if cut_params is not None:
                args["cut_params"] = cut_params
            
            return self.send_command("cut_half_lap", args)
            
        except Exception as e:
            return {"status": "error", "message": f"cut_half_lap failed: {e}"}
    
    async def cut_double_tenon(self, element_ids: List[int], cut_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create double tenon and mortise connections"""
        try:
            if not isinstance(element_ids, list) or len(element_ids) != 2:
                return {"status": "error", "message": "element_ids must be a list with exactly 2 element IDs"}
            
            validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            
            args: Dict[str, Any] = {"element_ids": validated_ids}
            if cut_params is not None:
                args["cut_params"] = cut_params
            
            return self.send_command("cut_double_tenon", args)
            
        except Exception as e:
            return {"status": "error", "message": f"cut_double_tenon failed: {e}"}
    
    async def cut_scarf_joint(self, element_ids: List[int], cut_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create scarf joint connections between elements"""
        try:
            if not isinstance(element_ids, list) or len(element_ids) != 2:
                return {"status": "error", "message": "element_ids must be a list with exactly 2 element IDs"}
            
            validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            
            args: Dict[str, Any] = {"element_ids": validated_ids}
            if cut_params is not None:
                args["cut_params"] = cut_params
            
            return self.send_command("cut_scarf_joint", args)
            
        except Exception as e:
            return {"status": "error", "message": f"cut_scarf_joint failed: {e}"}
    
    async def cut_shoulder(self, element_ids: List[int], cut_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create shoulder cuts between elements"""
        try:
            if not isinstance(element_ids, list) or len(element_ids) < 2:
                return {"status": "error", "message": "element_ids must be a list with at least 2 element IDs"}
            
            validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            
            args: Dict[str, Any] = {"element_ids": validated_ids}
            if cut_params is not None:
                args["cut_params"] = cut_params
            
            return self.send_command("cut_shoulder", args)
            
        except Exception as e:
            return {"status": "error", "message": f"cut_shoulder failed: {e}"}
    
    # --- AUXILIARY AND CONVERSION METHODS ---
    
    async def create_auxiliary_beam_points(self, p1: List[float], p2: List[float], 
                                         p3: Optional[List[float]] = None) -> Dict[str, Any]:
        """Create an auxiliary beam element using points"""
        try:
            validated_p1 = self.validate_point_3d(p1, "p1")
            validated_p2 = self.validate_point_3d(p2, "p2")
            if validated_p1 is None or validated_p2 is None:
                return {"status": "error", "message": "Invalid p1 or p2 coordinates"}
            
            args = {
                "p1": validated_p1,
                "p2": validated_p2
            }
            
            if p3 is not None:
                validated_p3 = self.validate_point_3d(p3, "p3")
                if validated_p3 is not None:
                    args["p3"] = validated_p3
            
            return self.send_command("create_auxiliary_beam_points", args)
            
        except Exception as e:
            return {"status": "error", "message": f"create_auxiliary_beam_points failed: {e}"}
    
    async def convert_beam_to_panel(self, element_ids: List[int]) -> Dict[str, Any]:
        """Convert beam elements to panel elements"""
        try:
            if not isinstance(element_ids, list) or not element_ids:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            return self.send_command("convert_beam_to_panel", {"element_ids": validated_ids})
            
        except Exception as e:
            return {"status": "error", "message": f"convert_beam_to_panel failed: {e}"}
    
    async def convert_panel_to_beam(self, element_ids: List[int]) -> Dict[str, Any]:
        """Convert panel elements to beam elements"""
        try:
            if not isinstance(element_ids, list) or not element_ids:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            return self.send_command("convert_panel_to_beam", {"element_ids": validated_ids})
            
        except Exception as e:
            return {"status": "error", "message": f"convert_panel_to_beam failed: {e}"}
    
    async def convert_auxiliary_to_beam(self, element_ids: List[int]) -> Dict[str, Any]:
        """Convert auxiliary elements to regular beam elements"""
        try:
            if not isinstance(element_ids, list) or not element_ids:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            return self.send_command("convert_auxiliary_to_beam", {"element_ids": validated_ids})
            
        except Exception as e:
            return {"status": "error", "message": f"convert_auxiliary_to_beam failed: {e}"}
    
    # --- CONTAINER METHODS ---
    
    async def create_auto_container_from_standard(self, element_ids: List[int], container_name: str) -> Dict[str, Any]:
        """Create an automatic container from standard elements"""
        try:
            if not isinstance(element_ids, list) or not element_ids:
                return {"status": "error", "message": "element_ids must be a non-empty list"}
            
            if not isinstance(container_name, str) or not container_name.strip():
                return {"status": "error", "message": "container_name must be a non-empty string"}
            
            validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            
            args = {
                "element_ids": validated_ids,
                "container_name": container_name.strip()
            }
            
            return self.send_command("create_auto_container_from_standard", args)
            
        except Exception as e:
            return {"status": "error", "message": f"create_auto_container_from_standard failed: {e}"}
    
    async def get_container_content_elements(self, container_id: int) -> Dict[str, Any]:
        """Get all elements contained within a specific container"""
        try:
            validated_id = self.validate_element_id(container_id)
            return self.send_command("get_container_content_elements", {"container_id": validated_id})
            
        except Exception as e:
            return {"status": "error", "message": f"get_container_content_elements failed: {e}"}
    
    async def create_surface(self, vertices: List[List[float]], surface_type: str = "flat") -> Dict[str, Any]:
        """Create a surface element from vertices
        
        Args:
            vertices: List of vertex points as [x,y,z] coordinates (minimum 3 points)
            surface_type: Type of surface ("flat", "curved", "ruled") - default "flat"
        
        Returns:
            Dictionary with creation status and surface element ID if successful
        """
        try:
            if not isinstance(vertices, list) or len(vertices) < 3:
                return {"status": "error", "message": "vertices must be a list of at least 3 points"}
            
            # Validate each vertex point
            validated_vertices = []
            for i, vertex in enumerate(vertices):
                validated_point = self.validate_point_3d(vertex, f"vertex_{i}")
                if validated_point is None:
                    return {"status": "error", "message": f"Invalid vertex at index {i}: {vertex}"}
                validated_vertices.append(validated_point)
            
            if not isinstance(surface_type, str):
                return {"status": "error", "message": "surface_type must be a string"}
            
            valid_types = ["flat", "curved", "ruled"]
            if surface_type not in valid_types:
                return {"status": "error", "message": f"surface_type must be one of {valid_types}, got: {surface_type}"}
            
            args = {
                "vertices": validated_vertices,
                "surface_type": surface_type
            }
            
            return self.send_command("create_surface", args)
            
        except Exception as e:
            return {"status": "error", "message": f"create_surface failed: {e}"}
    
    async def chamfer_edge(self, element_id: int, edge_vertices: List[List[List[float]]], 
                          chamfer_distance: float, chamfer_type: str = "symmetric") -> Dict[str, Any]:
        """Create a chamfer on element edges
        
        Args:
            element_id: ID of the element to chamfer
            edge_vertices: List of edges, each edge is 2 vertices: [[[x1,y1,z1], [x2,y2,z2]], ...]
            chamfer_distance: Distance of the chamfer in mm
            chamfer_type: Type of chamfer ("symmetric", "asymmetric", "rounded") - default "symmetric"
        
        Returns:
            Dictionary with operation status and modified element info if successful
        """
        try:
            validated_id = self.validate_element_id(element_id)
            
            if not isinstance(edge_vertices, list) or len(edge_vertices) < 1:
                return {"status": "error", "message": "edge_vertices must be a list with at least 1 edge (2 vertices)"}
            
            # Validate edge vertices (each edge should have exactly 2 vertices)
            validated_edges = []
            for i, edge in enumerate(edge_vertices):
                if not isinstance(edge, list) or len(edge) != 2:
                    return {"status": "error", "message": f"Edge {i} must contain exactly 2 vertices"}
                
                # Ensure each vertex is a list of coordinates
                if not isinstance(edge[0], list) or not isinstance(edge[1], list):
                    return {"status": "error", "message": f"Edge {i} vertices must be [x,y,z] coordinate lists"}
                
                vertex1 = self.validate_point_3d(edge[0], f"edge_{i}_vertex1")
                vertex2 = self.validate_point_3d(edge[1], f"edge_{i}_vertex2")
                
                if vertex1 is None or vertex2 is None:
                    return {"status": "error", "message": f"Invalid vertices in edge {i}"}
                
                validated_edges.append([vertex1, vertex2])
            
            if not isinstance(chamfer_distance, (int, float)) or chamfer_distance <= 0:
                return {"status": "error", "message": "chamfer_distance must be a positive number"}
            
            if not isinstance(chamfer_type, str):
                return {"status": "error", "message": "chamfer_type must be a string"}
            
            valid_types = ["symmetric", "asymmetric", "rounded"]
            if chamfer_type not in valid_types:
                return {"status": "error", "message": f"chamfer_type must be one of {valid_types}, got: {chamfer_type}"}
            
            args = {
                "element_id": validated_id,
                "edge_vertices": validated_edges,
                "chamfer_distance": float(chamfer_distance),
                "chamfer_type": chamfer_type
            }
            
            return self.send_command("chamfer_edge", args)
            
        except Exception as e:
            return {"status": "error", "message": f"chamfer_edge failed: {e}"}
    
    async def round_edge(self, element_id: int, edge_vertices: List[List[List[float]]], 
                        round_radius: float, round_type: str = "full") -> Dict[str, Any]:
        """Create a rounded edge on element edges
        
        Args:
            element_id: ID of the element to round
            edge_vertices: List of edges, each edge is 2 vertices: [[[x1,y1,z1], [x2,y2,z2]], ...]
            round_radius: Radius of the rounding in mm
            round_type: Type of rounding ("full", "quarter", "half") - default "full"
        
        Returns:
            Dictionary with operation status and modified element info if successful
        """
        try:
            validated_id = self.validate_element_id(element_id)
            
            if not isinstance(edge_vertices, list) or len(edge_vertices) < 1:
                return {"status": "error", "message": "edge_vertices must be a list with at least 1 edge (2 vertices)"}
            
            # Validate edge vertices (each edge should have exactly 2 vertices)
            validated_edges = []
            for i, edge in enumerate(edge_vertices):
                if not isinstance(edge, list) or len(edge) != 2:
                    return {"status": "error", "message": f"Edge {i} must contain exactly 2 vertices"}
                
                # Ensure each vertex is a list of coordinates
                if not isinstance(edge[0], list) or not isinstance(edge[1], list):
                    return {"status": "error", "message": f"Edge {i} vertices must be [x,y,z] coordinate lists"}
                
                vertex1 = self.validate_point_3d(edge[0], f"edge_{i}_vertex1")
                vertex2 = self.validate_point_3d(edge[1], f"edge_{i}_vertex2")
                
                if vertex1 is None or vertex2 is None:
                    return {"status": "error", "message": f"Invalid vertices in edge {i}"}
                
                validated_edges.append([vertex1, vertex2])
            
            if not isinstance(round_radius, (int, float)) or round_radius <= 0:
                return {"status": "error", "message": "round_radius must be a positive number"}
            
            if not isinstance(round_type, str):
                return {"status": "error", "message": "round_type must be a string"}
            
            valid_types = ["full", "quarter", "half"]
            if round_type not in valid_types:
                return {"status": "error", "message": f"round_type must be one of {valid_types}, got: {round_type}"}
            
            args = {
                "element_id": validated_id,
                "edge_vertices": validated_edges,
                "round_radius": float(round_radius),
                "round_type": round_type
            }
            
            return self.send_command("round_edge", args)
            
        except Exception as e:
            return {"status": "error", "message": f"round_edge failed: {e}"}
    
    async def split_element(self, element_id: int, split_plane_point: List[float], 
                           split_plane_normal: List[float], keep_both_parts: bool = True) -> Dict[str, Any]:
        """Split an element with a cutting plane
        
        Args:
            element_id: ID of the element to split
            split_plane_point: Point on the splitting plane [x,y,z]
            split_plane_normal: Normal vector of the splitting plane [x,y,z]
            keep_both_parts: Whether to keep both parts after splitting
        
        Returns:
            Dictionary with operation status and resulting element IDs if successful
        """
        try:
            validated_id = self.validate_element_id(element_id)
            
            validated_point = self.validate_point_3d(split_plane_point, "split_plane_point")
            if validated_point is None:
                return {"status": "error", "message": "Invalid split_plane_point coordinates"}
            
            validated_normal = self.validate_point_3d(split_plane_normal, "split_plane_normal")
            if validated_normal is None:
                return {"status": "error", "message": "Invalid split_plane_normal coordinates"}
            
            # Check if normal vector is not zero
            normal_length = sum(coord ** 2 for coord in validated_normal) ** 0.5
            if normal_length < 1e-10:
                return {"status": "error", "message": "split_plane_normal cannot be a zero vector"}
            
            if not isinstance(keep_both_parts, bool):
                return {"status": "error", "message": "keep_both_parts must be a boolean value"}
            
            args = {
                "element_id": validated_id,
                "split_plane_point": validated_point,
                "split_plane_normal": validated_normal,
                "keep_both_parts": keep_both_parts
            }
            
            return self.send_command("split_element", args)
            
        except Exception as e:
            return {"status": "error", "message": f"split_element failed: {e}"}
    
    async def create_beam_from_points(self, points: List[List[float]], cross_section: Dict[str, Any], 
                                     material: str = "Wood") -> Dict[str, Any]:
        """Create a beam element from a series of points defining its centerline
        
        Args:
            points: List of [x,y,z] points defining the beam centerline (minimum 2 points)
            cross_section: Dictionary defining cross-section properties:
                          {"type": "rectangular", "width": float, "height": float} or
                          {"type": "circular", "diameter": float} or
                          {"type": "standard", "name": str}
            material: Material name for the beam (default: "Wood")
        
        Returns:
            Dictionary with creation status and beam element ID if successful
        """
        try:
            if not isinstance(points, list) or len(points) < 2:
                return {"status": "error", "message": "points must be a list with at least 2 points"}
            
            # Validate all points
            validated_points = []
            for i, point in enumerate(points):
                validated_point = self.validate_point_3d(point, f"point_{i}")
                if validated_point is None:
                    return {"status": "error", "message": f"Invalid point at index {i}: {point}"}
                validated_points.append(validated_point)
            
            if not isinstance(cross_section, dict):
                return {"status": "error", "message": "cross_section must be a dictionary"}
            
            # Validate cross section
            cs_type = cross_section.get("type")
            if cs_type not in ["rectangular", "circular", "standard"]:
                return {"status": "error", "message": "cross_section type must be 'rectangular', 'circular', or 'standard'"}
            
            if cs_type == "rectangular":
                if "width" not in cross_section or "height" not in cross_section:
                    return {"status": "error", "message": "rectangular cross_section must have 'width' and 'height'"}
                if not isinstance(cross_section["width"], (int, float)) or cross_section["width"] <= 0:
                    return {"status": "error", "message": "cross_section width must be a positive number"}
                if not isinstance(cross_section["height"], (int, float)) or cross_section["height"] <= 0:
                    return {"status": "error", "message": "cross_section height must be a positive number"}
            
            elif cs_type == "circular":
                if "diameter" not in cross_section:
                    return {"status": "error", "message": "circular cross_section must have 'diameter'"}
                if not isinstance(cross_section["diameter"], (int, float)) or cross_section["diameter"] <= 0:
                    return {"status": "error", "message": "cross_section diameter must be a positive number"}
            
            elif cs_type == "standard":
                if "name" not in cross_section:
                    return {"status": "error", "message": "standard cross_section must have 'name'"}
                if not isinstance(cross_section["name"], str) or not cross_section["name"].strip():
                    return {"status": "error", "message": "cross_section name must be a non-empty string"}
            
            if not isinstance(material, str):
                return {"status": "error", "message": "material must be a string"}
            
            args = {
                "points": validated_points,
                "cross_section": cross_section,
                "material": material.strip()
            }
            
            return self.send_command("create_beam_from_points", args)
            
        except Exception as e:
            return {"status": "error", "message": f"create_beam_from_points failed: {e}"}
    
    async def create_auxiliary_line(self, start_point: List[float], end_point: List[float], 
                                   line_type: str = "construction") -> Dict[str, Any]:
        """Create an auxiliary line element for construction purposes
        
        Args:
            start_point: Start point of the line [x,y,z]
            end_point: End point of the line [x,y,z]
            line_type: Type of auxiliary line ("construction", "reference", "dimension") - default "construction"
        
        Returns:
            Dictionary with creation status and auxiliary line element ID if successful
        """
        try:
            validated_start = self.validate_point_3d(start_point, "start_point")
            if validated_start is None:
                return {"status": "error", "message": "Invalid start_point coordinates"}
            
            validated_end = self.validate_point_3d(end_point, "end_point")
            if validated_end is None:
                return {"status": "error", "message": "Invalid end_point coordinates"}
            
            # Check that start and end points are different
            if validated_start == validated_end:
                return {"status": "error", "message": "start_point and end_point cannot be the same"}
            
            if not isinstance(line_type, str):
                return {"status": "error", "message": "line_type must be a string"}
            
            valid_types = ["construction", "reference", "dimension"]
            if line_type not in valid_types:
                return {"status": "error", "message": f"line_type must be one of {valid_types}, got: {line_type}"}
            
            args = {
                "start_point": validated_start,
                "end_point": validated_end,
                "line_type": line_type
            }
            
            return self.send_command("create_auxiliary_line", args)
            
        except Exception as e:
            return {"status": "error", "message": f"create_auxiliary_line failed: {e}"}
    
    async def get_elements_in_region(self, min_point: List[float], max_point: List[float], 
                                   include_partially: bool = True) -> Dict[str, Any]:
        """Find all elements within a 3D bounding box region"""
        try:
            # Validate input parameters
            validated_min = self.validate_point_3d(min_point, "min_point")
            validated_max = self.validate_point_3d(max_point, "max_point")
            
            if validated_min is None or validated_max is None:
                return {"status": "error", "message": "Both min_point and max_point are required"}
            
            # Check that min_point is actually smaller than max_point in all dimensions
            for i in range(3):
                if validated_min[i] >= validated_max[i]:
                    return {"status": "error", "message": f"min_point[{i}] must be less than max_point[{i}]"}
            
            if not isinstance(include_partially, bool):
                return {"status": "error", "message": "include_partially must be a boolean value"}
            
            args = {
                "min_point": validated_min,
                "max_point": validated_max,
                "include_partially": include_partially
            }
            
            return self.send_command("get_elements_in_region", args)
            
        except Exception as e:
            return {"status": "error", "message": f"get_elements_in_region failed: {e}"}
