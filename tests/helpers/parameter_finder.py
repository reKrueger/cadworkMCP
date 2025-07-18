"""
Parameter Finder Class
=====================

Automatically generates realistic parameters for Cadwork MCP function testing.
Provides default values, coordinate systems, and parameter validation.
"""

import random
from typing import Dict, Any, List, Optional, Union, Tuple


class ParameterFinder:
    """
    Generates realistic parameters for Cadwork MCP function testing.
    Handles coordinate generation, dimensions, materials, colors, etc.
    """
    
    # Standard materials used in Cadwork
    STANDARD_MATERIALS = [
        "Wood", "GLT", "KVH", "BSH", "OSB", "Steel", "Concrete", 
        "Plywood", "MDF", "Chipboard", "Hardwood", "Softwood"
    ]
    
    # Standard wood dimensions (width, height) in mm
    STANDARD_WOOD_DIMENSIONS = [
        (80, 120), (80, 160), (80, 200), (80, 240),
        (100, 120), (100, 160), (100, 200), (100, 240),
        (120, 120), (120, 160), (120, 200), (120, 240),
        (140, 160), (140, 200), (140, 240), (160, 160),
        (160, 200), (160, 240), (200, 200), (200, 240)
    ]
    
    # Standard panel thicknesses in mm
    STANDARD_PANEL_THICKNESS = [18, 19, 22, 25, 30, 35, 40, 45, 50, 60]
    
    # Cadwork color IDs (1-255)
    STANDARD_COLORS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 40]
    
    def __init__(self, coordinate_range: Tuple[float, float] = (-5000, 5000)):
        """
        Initialize parameter finder
        
        Args:
            coordinate_range: Min/max values for coordinate generation
        """
        self.coord_min, self.coord_max = coordinate_range
        self.random = random.Random(42)  # Fixed seed for reproducible tests
    
    def get_random_coordinate(self) -> float:
        """Get random coordinate within range"""
        return self.random.uniform(self.coord_min, self.coord_max)
    
    def get_random_point_3d(self) -> List[float]:
        """Generate random 3D point [x, y, z]"""
        return [
            self.get_random_coordinate(),
            self.get_random_coordinate(), 
            self.get_random_coordinate()
        ]
    
    def get_test_beam_points(self) -> Tuple[List[float], List[float], Optional[List[float]]]:
        """
        Generate realistic beam points (p1, p2, p3)
        
        Returns:
            Tuple of (start_point, end_point, orientation_point)
        """
        # Start point
        p1 = [0, 0, 0]
        
        # End point - create beam along X-axis
        length = self.random.uniform(1000, 8000)  # 1-8m typical beam length
        p2 = [length, 0, 0]
        
        # Orientation point - slightly offset in Y direction
        p3 = [length/2, 100, 0]
        
        return p1, p2, p3
    
    def get_test_panel_points(self) -> Tuple[List[float], List[float], Optional[List[float]]]:
        """
        Generate realistic panel points (p1, p2, p3)
        
        Returns:
            Tuple of (start_point, end_point, orientation_point)
        """
        # Start point
        p1 = [0, 0, 0]
        
        # End point - create panel along X-axis
        width = self.random.uniform(1000, 3000)  # 1-3m typical panel width
        p2 = [width, 0, 0]
        
        # Orientation point - offset in Z direction (height)
        height = self.random.uniform(2000, 3000)  # 2-3m typical wall height
        p3 = [width/2, 0, height]
        
        return p1, p2, p3
    
    def get_standard_wood_dimensions(self) -> Tuple[float, float]:
        """Get random standard wood cross-section dimensions"""
        return self.random.choice(self.STANDARD_WOOD_DIMENSIONS)
    
    def get_standard_panel_thickness(self) -> float:
        """Get random standard panel thickness"""
        return self.random.choice(self.STANDARD_PANEL_THICKNESS)
    
    def get_standard_material(self) -> str:
        """Get random standard material name"""
        return self.random.choice(self.STANDARD_MATERIALS)
    
    def get_standard_color_id(self) -> int:
        """Get random standard color ID"""
        return self.random.choice(self.STANDARD_COLORS)
    
    def get_beam_parameters(self) -> Dict[str, Any]:
        """Generate complete beam creation parameters"""
        p1, p2, p3 = self.get_test_beam_points()
        width, height = self.get_standard_wood_dimensions()
        
        return {
            "p1": p1,
            "p2": p2, 
            "p3": p3,
            "width": width,
            "height": height
        }
    
    def get_panel_parameters(self) -> Dict[str, Any]:
        """Generate complete panel creation parameters"""
        p1, p2, p3 = self.get_test_panel_points()
        thickness = self.get_standard_panel_thickness()
        width = self.random.uniform(2000, 3000)  # Panel height
        
        return {
            "p1": p1,
            "p2": p2,
            "p3": p3,
            "width": width,
            "thickness": thickness
        }
    
    def get_circular_beam_parameters(self) -> Dict[str, Any]:
        """Generate circular beam parameters"""
        p1, p2, p3 = self.get_test_beam_points()
        diameter = self.random.choice([80, 100, 120, 140, 160, 180, 200])
        
        return {
            "diameter": diameter,
            "p1": p1,
            "p2": p2,
            "p3": p3
        }
    
    def get_square_beam_parameters(self) -> Dict[str, Any]:
        """Generate square beam parameters"""
        p1, p2, p3 = self.get_test_beam_points()
        width = self.random.choice([80, 100, 120, 140, 160, 180, 200])
        
        return {
            "width": width,
            "p1": p1,
            "p2": p2,
            "p3": p3
        }
    
    def get_drilling_parameters(self) -> Dict[str, Any]:
        """Generate drilling parameters"""
        p1, p2, _ = self.get_test_beam_points()
        # Shorter drilling length
        p2 = [p1[0] + 200, p1[1], p1[2]]  # 200mm deep
        diameter = self.random.choice([8, 10, 12, 16, 20, 25, 30])
        
        return {
            "diameter": diameter,
            "p1": p1,
            "p2": p2
        }
    
    def get_move_vector(self) -> List[float]:
        """Generate movement vector"""
        return [
            self.random.uniform(-1000, 1000),
            self.random.uniform(-1000, 1000),
            self.random.uniform(-500, 500)
        ]
    
    def get_scale_factor(self) -> float:
        """Generate scale factor"""
        return self.random.uniform(0.5, 2.0)
    
    def get_rotation_parameters(self) -> Dict[str, Any]:
        """Generate rotation parameters"""
        return {
            "origin": [0, 0, 0],
            "rotation_axis": [0, 0, 1],  # Rotate around Z-axis
            "rotation_angle": self.random.uniform(-180, 180)
        }
    
    def get_mirror_parameters(self) -> Dict[str, Any]:
        """Generate mirror parameters"""
        return {
            "mirror_plane_point": [0, 0, 0],
            "mirror_plane_normal": [1, 0, 0]  # Mirror across YZ-plane
        }
    
    def get_region_parameters(self) -> Dict[str, Any]:
        """Generate bounding box region parameters"""
        x1, y1, z1 = -2000, -2000, -1000
        x2, y2, z2 = 2000, 2000, 1000
        
        return {
            "min_point": [x1, y1, z1],
            "max_point": [x2, y2, z2],
            "include_partially": True
        }
    
    def get_dimension_range_parameters(self) -> Dict[str, Any]:
        """Generate dimension range filter parameters"""
        dimension_types = ["width", "height", "length", "volume", "weight"]
        dimension_type = self.random.choice(dimension_types)
        
        if dimension_type in ["width", "height", "length"]:
            min_val = 50
            max_val = 300
        elif dimension_type == "volume":
            min_val = 1000000  # 1000 cm³
            max_val = 100000000  # 100000 cm³
        else:  # weight
            min_val = 1  # 1 kg
            max_val = 100  # 100 kg
        
        return {
            "dimension_type": dimension_type,
            "min_value": min_val,
            "max_value": max_val
        }
    
    def get_export_parameters(self, export_format: str = "dxf") -> Dict[str, Any]:
        """Generate export parameters for different formats"""
        base_params = {
            "file_path": None,  # Will be generated automatically
        }
        
        format_specific = {
            "dxf": {
                "dxf_version": "R2018",
                "view_type": "plan",
                "include_dimensions": True,
                "line_weight": 0.25
            },
            "ifc": {
                "ifc_version": "IFC4",
                "coordinate_system": "project",
                "include_geometry": True,
                "include_materials": True,
                "include_properties": True
            },
            "step": {
                "step_version": "AP214",
                "units": "mm",
                "precision": 0.01
            },
            "stl": {
                "stl_format": "binary",
                "mesh_quality": "medium",
                "units": "mm",
                "merge_elements": True
            }
        }
        
        base_params.update(format_specific.get(export_format, {}))
        return base_params
