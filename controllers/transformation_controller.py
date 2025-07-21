"""
Transformation controller for element transformation operations
"""
from typing import Dict, Any, List, Optional
from .base_controller import BaseController

class TransformationController(BaseController):
    """Controller for element transformation operations"""
    
    def __init__(self) -> None:
        super().__init__("TransformationController")
    
    async def rotate_elements(self, element_ids: List[int], origin: List[float], 
                            rotation_axis: List[float], rotation_angle: float) -> Dict[str, Any]:
        """Rotates elements around a specified axis"""
        self.validate_required_args({
            "element_ids": element_ids, 
            "origin": origin, 
            "rotation_axis": rotation_axis,
            "rotation_angle": rotation_angle
        }, ["element_ids", "origin", "rotation_axis", "rotation_angle"])
        
        if not element_ids:
            raise ValueError("Element IDs list cannot be empty")
        
        # Validate all element IDs
        validated_ids = [self.validate_element_id(id_val) for id_val in element_ids]
        
        # Validate origin point
        validated_origin = self.validate_point_3d(origin, "Origin")
        if validated_origin is None:
            raise ValueError("Origin point is required")
        
        # Validate rotation axis
        validated_axis = self.validate_point_3d(rotation_axis, "Rotation axis")
        if validated_axis is None:
            raise ValueError("Rotation axis is required")
        
        # Check if rotation axis is zero vector
        if all(abs(coord) < 1e-10 for coord in validated_axis):
            raise ValueError("Rotation axis cannot be zero vector")
        
        # Validate rotation angle
        try:
            angle = float(rotation_angle)
        except (ValueError, TypeError):
            raise ValueError(f"Rotation angle must be numeric, got: {rotation_angle}")
        
        args: Dict[str, Any] = {
            "element_ids": validated_ids,
            "origin": validated_origin,
            "rotation_axis": validated_axis,
            "rotation_angle": angle
        }
        
        return self.send_command("rotate_elements", args)
    
    async def apply_global_scale(self, element_ids: List[int], scale: float, origin: List[float]) -> Dict[str, Any]:
        """Applies global scaling to elements"""
        self.validate_required_args({
            "element_ids": element_ids,
            "scale": scale,
            "origin": origin
        }, ["element_ids", "scale", "origin"])
        
        if not element_ids:
            raise ValueError("Element IDs list cannot be empty")
        
        # Validate all element IDs
        validated_ids = [self.validate_element_id(id_val) for id_val in element_ids]
        
        # Validate scale factor
        try:
            scale_factor = float(scale)
            if scale_factor <= 0:
                raise ValueError(f"Scale factor must be positive, got: {scale_factor}")
        except (ValueError, TypeError):
            raise ValueError(f"Scale factor must be numeric, got: {scale}")
        
        # Validate origin point
        validated_origin = self.validate_point_3d(origin, "Origin")
        if validated_origin is None:
            raise ValueError("Origin point is required")
        
        args: Dict[str, Any] = {
            "element_ids": validated_ids,
            "scale": scale_factor,
            "origin": validated_origin
        }
        
        return self.send_command("apply_global_scale", args)
