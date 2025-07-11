"""
Geometry operation handlers
"""
from typing import Dict, Any
from ..helpers import validate_element_id, validate_element_ids

def handle_get_element_width(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get element width command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_id = validate_element_id(args.get("element_id"))
        width = gc.get_width(element_id)
        
        if isinstance(width, (int, float)):
            return {"status": "ok", "width": float(width)}
        else:
            return {
                "status": "error", 
                "message": f"Invalid width value returned: {width}"
            }
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_get_element_height(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get element height command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_id = validate_element_id(args.get("element_id"))
        height = gc.get_height(element_id)
        
        if isinstance(height, (int, float)):
            return {"status": "ok", "height": float(height)}
        else:
            return {
                "status": "error", 
                "message": f"Invalid height value returned: {height}"
            }
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_get_element_length(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get element length command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_id = validate_element_id(args.get("element_id"))
        length = gc.get_length(element_id)
        
        if isinstance(length, (int, float)):
            return {"status": "ok", "length": float(length)}
        else:
            return {
                "status": "error", 
                "message": f"Invalid length value returned: {length}"
            }
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_get_element_volume(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get element volume command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_id = validate_element_id(args.get("element_id"))
        volume = gc.get_volume(element_id)
        
        if isinstance(volume, (int, float)):
            return {"status": "ok", "volume": float(volume)}
        else:
            return {
                "status": "error", 
                "message": f"Invalid volume value returned: {volume}"
            }
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_get_element_weight(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get element weight command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_id = validate_element_id(args.get("element_id"))
        weight = gc.get_weight(element_id)
        
        if isinstance(weight, (int, float)):
            return {"status": "ok", "weight": float(weight)}
        else:
            return {
                "status": "error", 
                "message": f"Invalid weight value returned: {weight}"
            }
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_get_element_xl(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get element xl vector command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_id = validate_element_id(args.get("element_id"))
        xl_vector = gc.get_xl(element_id)
        
        # Convert point_3d to list
        from ..helpers import point_3d_to_list
        xl_list = point_3d_to_list(xl_vector)
        
        return {"status": "ok", "xl_vector": xl_list}
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_get_element_yl(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get element yl vector command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_id = validate_element_id(args.get("element_id"))
        yl_vector = gc.get_yl(element_id)
        
        # Convert point_3d to list
        from ..helpers import point_3d_to_list
        yl_list = point_3d_to_list(yl_vector)
        
        return {"status": "ok", "yl_vector": yl_list}
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_get_element_zl(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get element zl vector command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_id = validate_element_id(args.get("element_id"))
        zl_vector = gc.get_zl(element_id)
        
        # Convert point_3d to list
        from ..helpers import point_3d_to_list
        zl_list = point_3d_to_list(zl_vector)
        
        return {"status": "ok", "zl_vector": zl_list}
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_get_element_p1(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get element p1 point command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_id = validate_element_id(args.get("element_id"))
        p1_point = gc.get_p1(element_id)
        
        # Convert point_3d to list
        from ..helpers import point_3d_to_list
        p1_list = point_3d_to_list(p1_point)
        
        return {"status": "ok", "p1_point": p1_list}
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_get_element_p2(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get element p2 point command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_id = validate_element_id(args.get("element_id"))
        p2_point = gc.get_p2(element_id)
        
        # Convert point_3d to list
        from ..helpers import point_3d_to_list
        p2_list = point_3d_to_list(p2_point)
        
        return {"status": "ok", "p2_point": p2_list}
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_get_element_p3(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get element p3 point command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_id = validate_element_id(args.get("element_id"))
        p3_point = gc.get_p3(element_id)
        
        # Convert point_3d to list
        from ..helpers import point_3d_to_list
        p3_list = point_3d_to_list(p3_point)
        
        return {"status": "ok", "p3_point": p3_list}
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_get_center_of_gravity(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get center of gravity command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_id = validate_element_id(args.get("element_id"))
        cog_point = gc.get_center_of_gravity(element_id)
        
        # Convert point_3d to list
        from ..helpers import point_3d_to_list
        cog_list = point_3d_to_list(cog_point)
        
        return {"status": "ok", "center_of_gravity": cog_list}
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_get_center_of_gravity_for_list(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get center of gravity for list command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_ids = validate_element_ids(args.get("element_ids", []))
        
        if not element_ids:
            return {"status": "error", "message": "No elements specified"}
        
        cog_point = gc.get_center_of_gravity_for_list(element_ids)
        
        # Convert point_3d to list
        from ..helpers import point_3d_to_list
        cog_list = point_3d_to_list(cog_point)
        
        return {
            "status": "ok", 
            "center_of_gravity": cog_list,
            "element_count": len(element_ids)
        }
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_get_element_vertices(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get element vertices command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_id = validate_element_id(args.get("element_id"))
        vertices = gc.get_element_vertices(element_id)
        
        # Convert list of point_3d to list of lists
        from ..helpers import point_3d_to_list
        vertices_list = [point_3d_to_list(vertex) for vertex in vertices]
        
        return {
            "status": "ok", 
            "vertices": vertices_list,
            "vertex_count": len(vertices_list)
        }
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_get_minimum_distance_between_elements(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get minimum distance between elements command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        first_element_id = validate_element_id(args.get("first_element_id"))
        second_element_id = validate_element_id(args.get("second_element_id"))
        
        distance = gc.get_minimum_distance_between_elements(first_element_id, second_element_id)
        
        if isinstance(distance, (int, float)):
            return {
                "status": "ok", 
                "distance": float(distance),
                "first_element_id": first_element_id,
                "second_element_id": second_element_id
            }
        else:
            return {
                "status": "error", 
                "message": f"Invalid distance value returned: {distance}"
            }
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_get_element_facets(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get element facets command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_id = validate_element_id(args.get("element_id"))
        facets = gc.get_element_facets(element_id)
        
        # Convert facet_list to appropriate format
        # Note: facet_list is a special Cadwork type, we need to extract data from it
        facets_data = []
        
        # Try to iterate through facets and convert each facet
        try:
            # Assuming facets is iterable and contains point_3d objects
            from ..helpers import point_3d_to_list
            
            for facet in facets:
                # Each facet should be a list of points forming a face
                if hasattr(facet, '__iter__'):
                    facet_points = [point_3d_to_list(point) for point in facet]
                    facets_data.append(facet_points)
                else:
                    # Single point facet (degenerate case)
                    facets_data.append([point_3d_to_list(facet)])
                    
        except Exception as facet_error:
            # If facet conversion fails, return basic info
            return {
                "status": "ok",
                "facet_count": len(facets) if hasattr(facets, '__len__') else 0,
                "message": "Facets available but format conversion not fully supported",
                "raw_type": str(type(facets))
            }
        
        return {
            "status": "ok", 
            "facets": facets_data,
            "facet_count": len(facets_data)
        }
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_get_element_reference_face_area(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get element reference face area command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_id = validate_element_id(args.get("element_id"))
        area = gc.get_element_reference_face_area(element_id)
        
        if isinstance(area, (int, float)):
            return {"status": "ok", "reference_face_area": float(area)}
        else:
            return {
                "status": "error", 
                "message": f"Invalid area value returned: {area}"
            }
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_get_total_area_of_all_faces(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get total area of all faces command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_id = validate_element_id(args.get("element_id"))
        total_area = gc.get_total_area_of_all_faces(element_id)
        
        if isinstance(total_area, (int, float)):
            return {"status": "ok", "total_face_area": float(total_area)}
        else:
            return {
                "status": "error", 
                "message": f"Invalid area value returned: {total_area}"
            }
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_rotate_elements(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle rotate elements command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_ids = validate_element_ids(args.get("element_ids", []))
        origin_raw = args.get("origin")
        rotation_axis_raw = args.get("rotation_axis")
        rotation_angle = args.get("rotation_angle")
        
        if not element_ids:
            return {"status": "error", "message": "No elements specified for rotation"}
        
        if origin_raw is None:
            raise ValueError("Missing required argument: origin")
        if rotation_axis_raw is None:
            raise ValueError("Missing required argument: rotation_axis")
        if rotation_angle is None:
            raise ValueError("Missing required argument: rotation_angle")
        
        # Convert arguments
        from ..helpers import to_point_3d
        origin = to_point_3d(origin_raw)
        rotation_axis = to_point_3d(rotation_axis_raw)
        angle = float(rotation_angle)
        
        # Rotate elements
        ec.rotate_elements(element_ids, origin, rotation_axis, angle)
        
        return {
            "status": "ok", 
            "rotated_count": len(element_ids),
            "rotation_angle": angle,
            "message": f"Successfully rotated {len(element_ids)} elements by {angle}° around axis"
        }
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to rotate elements: {e}"}

def handle_apply_global_scale(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle apply global scale command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_ids = validate_element_ids(args.get("element_ids", []))
        scale = args.get("scale")
        origin_raw = args.get("origin")
        
        if not element_ids:
            return {"status": "error", "message": "No elements specified for scaling"}
        
        if scale is None:
            raise ValueError("Missing required argument: scale")
        if origin_raw is None:
            raise ValueError("Missing required argument: origin")
        
        # Convert arguments
        from ..helpers import to_point_3d
        scale_factor = float(scale)
        origin = to_point_3d(origin_raw)
        
        if scale_factor <= 0:
            raise ValueError(f"Scale factor must be positive, got: {scale_factor}")
        
        # Apply scaling
        gc.apply_global_scale(element_ids, scale_factor, origin)
        
        return {
            "status": "ok", 
            "scaled_count": len(element_ids),
            "scale_factor": scale_factor,
            "origin": origin_raw,
            "message": f"Successfully scaled {len(element_ids)} elements by factor {scale_factor}"
        }
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to scale elements: {e}"}

def handle_invert_model(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle invert model command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_ids = validate_element_ids(args.get("element_ids", []))
        
        if not element_ids:
            return {"status": "error", "message": "No elements specified for inversion"}
        
        # Invert model
        gc.invert_model(element_ids)
        
        return {
            "status": "ok", 
            "inverted_count": len(element_ids),
            "message": f"Successfully inverted {len(element_ids)} elements"
        }
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to invert elements: {e}"}

def handle_rotate_height_axis_90(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle rotate height axis 90 degrees command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_ids = validate_element_ids(args.get("element_ids", []))
        
        if not element_ids:
            return {"status": "error", "message": "No elements specified for rotation"}
        
        # Rotate height axis 90 degrees
        gc.rotate_height_axis_90(element_ids)
        
        return {
            "status": "ok", 
            "rotated_count": len(element_ids),
            "message": f"Successfully rotated height axis of {len(element_ids)} elements by 90°"
        }
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to rotate height axis: {e}"}

def handle_rotate_length_axis_90(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle rotate length axis 90 degrees command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        import geometry_controller as gc

        element_ids = validate_element_ids(args.get("element_ids", []))
        
        if not element_ids:
            return {"status": "error", "message": "No elements specified for rotation"}
        
        # Rotate length axis 90 degrees
        gc.rotate_length_axis_90(element_ids)
        
        return {
            "status": "ok", 
            "rotated_count": len(element_ids),
            "message": f"Successfully rotated length axis of {len(element_ids)} elements by 90°"
        }
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to rotate length axis: {e}"}

def handle_get_element_type(aParams: dict) -> dict:
    """Ruft Element-Typ ab"""
    try:
        import element_controller as ec
        
        lElementId = aParams.get("element_id")
        
        if lElementId is None:
            return {"status": "error", "message": "No element ID provided"}
        
        # Cadwork API aufrufen
        lElementType = ec.get_element_type(lElementId)
        
        # Element-Typ als String zurückgeben
        lTypeNames = {
            0: "none",
            1: "beam", 
            2: "panel",
            3: "drilling",
            4: "node",
            5: "line",
            6: "surface",
            7: "volume",
            8: "container",
            9: "auxiliary",
            10: "text_object",
            11: "dimension",
            12: "architectural"
        }
        
        lTypeName = lTypeNames.get(lElementType, f"unknown_type_{lElementType}")
        
        return {
            "status": "success",
            "element_id": lElementId,
            "element_type": lTypeName,
            "type_id": lElementType
        }
        
    except Exception as e:
        return {"status": "error", "message": f"get_element_type failed: {e}"}

def handle_calculate_total_volume(aParams: dict) -> dict:
    """Berechnet Gesamtvolumen einer Element-Liste"""
    try:
        import element_controller as ec
        
        lElementIds = aParams.get("element_ids", [])
        
        if not lElementIds:
            return {"status": "error", "message": "No element IDs provided"}
        
        lTotalVolumeMm3 = 0.0
        lProcessedElements = []
        lFailedElements = []
        
        # Volumen aller Elemente summieren
        for lElementId in lElementIds:
            try:
                lVolume = ec.get_element_volume(lElementId)
                if lVolume is not None and lVolume > 0:
                    lTotalVolumeMm3 += lVolume
                    lProcessedElements.append(lElementId)
                else:
                    lFailedElements.append(lElementId)
            except Exception as e:
                lFailedElements.append(lElementId)
        
        # Einheiten-Konvertierung
        lTotalVolumeCm3 = lTotalVolumeMm3 / 1000.0  # mm³ → cm³
        lTotalVolumeDm3 = lTotalVolumeMm3 / 1000000.0  # mm³ → dm³ (Liter)
        lTotalVolumeM3 = lTotalVolumeMm3 / 1000000000.0  # mm³ → m³
        
        return {
            "status": "success",
            "total_volume_mm3": lTotalVolumeMm3,
            "total_volume_cm3": lTotalVolumeCm3,
            "total_volume_dm3": lTotalVolumeDm3,
            "total_volume_m3": lTotalVolumeM3,
            "processed_elements": lProcessedElements,
            "failed_elements": lFailedElements,
            "processed_count": len(lProcessedElements),
            "failed_count": len(lFailedElements),
            "total_count": len(lElementIds)
        }
        
    except Exception as e:
        return {"status": "error", "message": f"calculate_total_volume failed: {e}"}

def handle_calculate_total_weight(aParams: dict) -> dict:
    """Berechnet Gesamtgewicht einer Element-Liste"""
    try:
        import element_controller as ec
        
        lElementIds = aParams.get("element_ids", [])
        
        if not lElementIds:
            return {"status": "error", "message": "No element IDs provided"}
        
        lTotalWeightKg = 0.0
        lProcessedElements = []
        lFailedElements = []
        
        # Gewicht aller Elemente summieren
        for lElementId in lElementIds:
            try:
                lWeight = ec.get_element_weight(lElementId)
                if lWeight is not None and lWeight > 0:
                    lTotalWeightKg += lWeight
                    lProcessedElements.append(lElementId)
                else:
                    lFailedElements.append(lElementId)
            except Exception as e:
                lFailedElements.append(lElementId)
        
        # Einheiten-Konvertierung
        lTotalWeightG = lTotalWeightKg * 1000.0      # kg → g
        lTotalWeightT = lTotalWeightKg / 1000.0      # kg → t (Tonnen)
        
        return {
            "status": "success",
            "total_weight_kg": lTotalWeightKg,
            "total_weight_g": lTotalWeightG,
            "total_weight_t": lTotalWeightT,
            "processed_elements": lProcessedElements,
            "failed_elements": lFailedElements,
            "processed_count": len(lProcessedElements),
            "failed_count": len(lFailedElements),
            "total_count": len(lElementIds)
        }
        
    except Exception as e:
        return {"status": "error", "message": f"calculate_total_weight failed: {e}"}
