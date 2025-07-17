"""
Measurement controller for distance and measurement operations
"""
from typing import Dict, Any, List, Optional
import math
from .base_controller import BaseController

class CMeasurementController(BaseController):
    """Controller for measurement operations"""
    
    def __init__(self) -> None:
        super().__init__("MeasurementController")
    
    async def measure_distance(self, point1: List[float], point2: List[float]) -> Dict[str, Any]:
        """Measure the distance between two 3D points"""
        try:
            # Validate input points
            validated_p1 = self.validate_point_3d(point1, "point1")
            validated_p2 = self.validate_point_3d(point2, "point2")
            
            if validated_p1 is None or validated_p2 is None:
                return {"status": "error", "message": "Both points must be valid 3D coordinates"}
            
            # Calculate Euclidean distance
            dx = validated_p2[0] - validated_p1[0]
            dy = validated_p2[1] - validated_p1[1]
            dz = validated_p2[2] - validated_p1[2]
            
            distance = math.sqrt(dx*dx + dy*dy + dz*dz)
            
            # Also calculate individual axis distances
            abs_dx = abs(dx)
            abs_dy = abs(dy)
            abs_dz = abs(dz)
            
            return {
                "status": "ok",
                "distance": distance,
                "distance_3d": distance,  # Alias for clarity
                "distance_x": abs_dx,
                "distance_y": abs_dy,
                "distance_z": abs_dz,
                "delta_x": dx,
                "delta_y": dy,
                "delta_z": dz,
                "point1": validated_p1,
                "point2": validated_p2,
                "units": "mm"  # Cadwork uses millimeters
            }
            
        except ValueError as e:
            return {"status": "error", "message": f"Invalid input: {e}"}
        except Exception as e:
            return {"status": "error", "message": f"measure_distance failed: {e}"}

    async def measure_angle(self, vector1: List[float], vector2: List[float]) -> Dict[str, Any]:
        """Measure the angle between two 3D vectors"""
        try:
            # Validate input vectors
            validated_v1 = self.validate_point_3d(vector1, "vector1")
            validated_v2 = self.validate_point_3d(vector2, "vector2")
            
            if validated_v1 is None or validated_v2 is None:
                return {"status": "error", "message": "Both vectors must be valid 3D coordinates"}
            
            # Calculate vector magnitudes
            magnitude1 = math.sqrt(validated_v1[0]**2 + validated_v1[1]**2 + validated_v1[2]**2)
            magnitude2 = math.sqrt(validated_v2[0]**2 + validated_v2[1]**2 + validated_v2[2]**2)
            
            # Check for zero vectors
            if magnitude1 == 0.0 or magnitude2 == 0.0:
                return {"status": "error", "message": "Cannot calculate angle with zero-length vector"}
            
            # Calculate dot product
            dot_product = (validated_v1[0] * validated_v2[0] + 
                          validated_v1[1] * validated_v2[1] + 
                          validated_v1[2] * validated_v2[2])
            
            # Calculate cosine of angle
            cos_angle = dot_product / (magnitude1 * magnitude2)
            
            # Clamp to valid range for acos (handle floating point precision errors)
            cos_angle = max(-1.0, min(1.0, cos_angle))
            
            # Calculate angle in radians
            angle_radians = math.acos(cos_angle)
            
            # Convert to degrees
            angle_degrees = math.degrees(angle_radians)
            
            # Calculate cross product for additional information
            cross_product = [
                validated_v1[1] * validated_v2[2] - validated_v1[2] * validated_v2[1],
                validated_v1[2] * validated_v2[0] - validated_v1[0] * validated_v2[2],
                validated_v1[0] * validated_v2[1] - validated_v1[1] * validated_v2[0]
            ]
            
            cross_magnitude = math.sqrt(cross_product[0]**2 + cross_product[1]**2 + cross_product[2]**2)
            
            return {
                "status": "ok",
                "angle_degrees": angle_degrees,
                "angle_radians": angle_radians,
                "dot_product": dot_product,
                "cross_product": cross_product,
                "cross_magnitude": cross_magnitude,
                "vector1": validated_v1,
                "vector2": validated_v2,
                "vector1_magnitude": magnitude1,
                "vector2_magnitude": magnitude2,
                "cos_angle": cos_angle,
                "is_perpendicular": abs(dot_product) < 1e-10,  # Nearly zero dot product
                "is_parallel": abs(abs(cos_angle) - 1.0) < 1e-10,  # cos(angle) ≈ ±1
                "units": {
                    "angle": "degrees",
                    "vectors": "mm"
                }
            }
            
        except ValueError as e:
            return {"status": "error", "message": f"Invalid input: {e}"}
        except Exception as e:
            return {"status": "error", "message": f"measure_angle failed: {e}"}

    async def measure_area(self, vertices: List[List[float]]) -> Dict[str, Any]:
        """Measure the area of a polygon defined by vertices"""
        try:
            # Validate input vertices
            if not isinstance(vertices, list) or len(vertices) < 3:
                return {"status": "error", "message": "vertices must be a list with at least 3 points"}
            
            validated_vertices = []
            for i, vertex in enumerate(vertices):
                validated_vertex = self.validate_point_3d(vertex, f"vertex[{i}]")
                if validated_vertex is None:
                    return {"status": "error", "message": f"vertex[{i}] must be valid 3D coordinates"}
                validated_vertices.append(validated_vertex)
            
            # Calculate area using the shoelace formula for 3D polygons
            # Project to best-fit plane and calculate 2D area
            n = len(validated_vertices)
            
            if n == 3:
                # Triangle area using cross product
                v1 = [validated_vertices[1][i] - validated_vertices[0][i] for i in range(3)]
                v2 = [validated_vertices[2][i] - validated_vertices[0][i] for i in range(3)]
                
                # Cross product
                cross = [
                    v1[1] * v2[2] - v1[2] * v2[1],
                    v1[2] * v2[0] - v1[0] * v2[2],
                    v1[0] * v2[1] - v1[1] * v2[0]
                ]
                
                # Area is half the magnitude of cross product
                cross_magnitude = math.sqrt(cross[0]**2 + cross[1]**2 + cross[2]**2)
                area = cross_magnitude / 2.0
                
                return {
                    "status": "ok",
                    "area": area,
                    "area_mm2": area,
                    "area_m2": area / 1000000.0,  # Convert mm² to m²
                    "polygon_type": "triangle",
                    "vertex_count": n,
                    "vertices": validated_vertices,
                    "perimeter": self._calculate_perimeter(validated_vertices),
                    "cross_product": cross,
                    "units": "mm²"
                }
            
            else:
                # For polygons with more than 3 vertices, use triangulation
                # Calculate normal vector for the plane
                normal = self._calculate_polygon_normal(validated_vertices)
                if normal is None:
                    return {"status": "error", "message": "Cannot determine polygon plane (vertices may be collinear)"}
                
                # Triangulate polygon and sum triangle areas
                total_area = 0.0
                triangles = []
                
                # Fan triangulation from first vertex
                for i in range(1, n - 1):
                    v1 = [validated_vertices[i][j] - validated_vertices[0][j] for j in range(3)]
                    v2 = [validated_vertices[i + 1][j] - validated_vertices[0][j] for j in range(3)]
                    
                    # Cross product for this triangle
                    cross = [
                        v1[1] * v2[2] - v1[2] * v2[1],
                        v1[2] * v2[0] - v1[0] * v2[2],
                        v1[0] * v2[1] - v1[1] * v2[0]
                    ]
                    
                    triangle_area = math.sqrt(cross[0]**2 + cross[1]**2 + cross[2]**2) / 2.0
                    total_area += triangle_area
                    triangles.append({
                        "vertices": [validated_vertices[0], validated_vertices[i], validated_vertices[i + 1]],
                        "area": triangle_area
                    })
                
                return {
                    "status": "ok",
                    "area": total_area,
                    "area_mm2": total_area,
                    "area_m2": total_area / 1000000.0,  # Convert mm² to m²
                    "polygon_type": "polygon",
                    "vertex_count": n,
                    "vertices": validated_vertices,
                    "perimeter": self._calculate_perimeter(validated_vertices),
                    "triangulation": triangles,
                    "normal_vector": normal,
                    "units": "mm²"
                }
            
        except ValueError as e:
            return {"status": "error", "message": f"Invalid input: {e}"}
        except Exception as e:
            return {"status": "error", "message": f"measure_area failed: {e}"}

    def _calculate_perimeter(self, vertices: List[List[float]]) -> float:
        """Calculate perimeter of polygon"""
        perimeter = 0.0
        n = len(vertices)
        
        for i in range(n):
            next_i = (i + 1) % n
            dx = vertices[next_i][0] - vertices[i][0]
            dy = vertices[next_i][1] - vertices[i][1]
            dz = vertices[next_i][2] - vertices[i][2]
            edge_length = math.sqrt(dx*dx + dy*dy + dz*dz)
            perimeter += edge_length
        
        return perimeter

    def _calculate_polygon_normal(self, vertices: List[List[float]]) -> Optional[List[float]]:
        """Calculate normal vector for polygon plane using Newell's method"""
        if len(vertices) < 3:
            return None
        
        normal = [0.0, 0.0, 0.0]
        n = len(vertices)
        
        for i in range(n):
            current = vertices[i]
            next_vertex = vertices[(i + 1) % n]
            
            normal[0] += (current[1] - next_vertex[1]) * (current[2] + next_vertex[2])
            normal[1] += (current[2] - next_vertex[2]) * (current[0] + next_vertex[0])
            normal[2] += (current[0] - next_vertex[0]) * (current[1] + next_vertex[1])
        
        # Normalize
        magnitude = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
        if magnitude < 1e-10:
            return None
        
        return [normal[0]/magnitude, normal[1]/magnitude, normal[2]/magnitude]