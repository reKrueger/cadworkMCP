"""
Helper functions for data conversion
"""
from typing import List, Union, TYPE_CHECKING

if TYPE_CHECKING:
    import cadwork

def to_point_3d(coords: Union[List, tuple]) -> 'cadwork.point_3d':
    """Convert [x,y,z] list/tuple to cadwork.point_3d"""
    # Import cadwork here to avoid import-time errors
    import cadwork
    
    if not isinstance(coords, (list, tuple)) or len(coords) != 3:
        raise ValueError(f"Invalid point format: {coords}. Expected list/tuple of 3 numbers.")
    
    try:
        return cadwork.point_3d(float(coords[0]), float(coords[1]), float(coords[2]))
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid coordinates in point {coords}: {e}")

def point_3d_to_list(pt: 'cadwork.point_3d') -> List[float]:
    """Convert cadwork.point_3d to [x, y, z] list"""
    # Import cadwork here to avoid import-time errors
    import cadwork
    
    if not isinstance(pt, cadwork.point_3d):
        return [0.0, 0.0, 0.0]  # Default fallback
    return [pt.x, pt.y, pt.z]

def validate_positive_number(value: Union[int, float], name: str) -> float:
    """Validate that a value is a positive number"""
    if not isinstance(value, (int, float)) or value <= 0:
        raise ValueError(f"{name} must be a positive number, got: {value}")
    return float(value)

def validate_element_id(element_id: Union[int, str]) -> int:
    """Validate element ID"""
    try:
        id_val = int(element_id)
        if id_val < 0:
            raise ValueError(f"Element ID must be non-negative, got: {id_val}")
        return id_val
    except (ValueError, TypeError):
        raise ValueError(f"Invalid element ID: {element_id}")

def validate_element_ids(element_ids: List[Union[int, str]]) -> List[int]:
    """Validate list of element IDs"""
    if not isinstance(element_ids, list):
        raise ValueError("element_ids must be a list")
    return [validate_element_id(eid) for eid in element_ids]
