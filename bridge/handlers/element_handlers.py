"""
Element operation handlers
"""
from typing import Dict, Any
from ..helpers import to_point_3d, point_3d_to_list, validate_positive_number, validate_element_ids

def handle_create_beam(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle create beam command"""
    try:
        # Import here to avoid import-time errors
        import cadwork

        # Import here to avoid import-time errors
        import element_controller as ec

        # Import here to avoid import-time errors
        
        # Validate required arguments
        required = ["p1", "p2", "width", "height"]
        for key in required:
            if key not in args:
                raise ValueError(f"Missing required argument: {key}")
        
        # Convert and validate arguments
        p1 = to_point_3d(args["p1"])
        p2 = to_point_3d(args["p2"])
        width = validate_positive_number(args["width"], "width")
        height = validate_positive_number(args["height"], "height")
        
        # Handle optional p3
        p3_raw = args.get("p3")
        if p3_raw is None:
            p3 = cadwork.point_3d(p1.x, p1.y, p1.z + 1.0)
        else:
            p3 = to_point_3d(p3_raw)
        
        # Create beam
        beam_id = ec.create_rectangular_beam_points(width, height, p1, p2, p3)
        
        if isinstance(beam_id, int) and beam_id >= 0:
            return {"status": "ok", "id": beam_id}
        else:
            return {
                "status": "error", 
                "message": f"Beam creation failed, returned: {beam_id}"
            }
            
    except ImportError as e:
        return {"status": "error", "message": f"Failed to import Cadwork modules: {e}"}
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Cadwork API error: {e}"}

def handle_create_panel(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle create panel command"""
    try:
        # Import here to avoid import-time errors
        import cadwork

        # Import here to avoid import-time errors
        import element_controller as ec

        # Validate required arguments
        required = ["p1", "p2", "width", "thickness"]
        for key in required:
            if key not in args:
                raise ValueError(f"Missing required argument: {key}")
        
        # Convert and validate arguments
        p1 = to_point_3d(args["p1"])
        p2 = to_point_3d(args["p2"])
        width = validate_positive_number(args["width"], "width")
        thickness = validate_positive_number(args["thickness"], "thickness")
        
        # Handle optional p3
        p3_raw = args.get("p3")
        if p3_raw is None:
            p3 = cadwork.point_3d(p1.x, p1.y, p1.z + 1.0)
        else:
            p3 = to_point_3d(p3_raw)
        
        # Create panel
        panel_id = ec.create_rectangular_panel_points(width, thickness, p1, p2, p3)
        
        if isinstance(panel_id, int) and panel_id >= 0:
            return {"status": "ok", "id": panel_id}
        else:
            return {
                "status": "error", 
                "message": f"Panel creation failed, returned: {panel_id}"
            }
            
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Cadwork API error: {e}"}

def handle_get_active_element_ids(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get active element IDs command"""
    try:
        # Import here to avoid import-time errors
        import cadwork

        # Import here to avoid import-time errors
        import element_controller as ec

        active_ids = ec.get_active_identifiable_element_ids()
        return {"status": "ok", "element_ids": active_ids}
    except Exception as e:
        return {"status": "error", "message": f"Failed to get active elements: {e}"}

def handle_get_all_element_ids(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get all element IDs command"""
    try:
        # Import here to avoid import-time errors
        import cadwork

        # Import here to avoid import-time errors
        import element_controller as ec

        all_ids = ec.get_all_identifiable_element_ids()
        return {"status": "ok", "element_ids": all_ids}
    except Exception as e:
        return {"status": "error", "message": f"Failed to get all elements: {e}"}

def handle_delete_elements(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle delete elements command"""
    try:
        # Import here to avoid import-time errors
        import cadwork

        # Import here to avoid import-time errors
        import element_controller as ec

        element_ids = validate_element_ids(args.get("element_ids", []))
        
        if not element_ids:
            return {"status": "ok", "message": "No elements to delete"}
        
        # Delete elements
        ec.delete_elements(element_ids)
        
        return {
            "status": "ok", 
            "message": f"Successfully deleted {len(element_ids)} elements",
            "deleted_count": len(element_ids)
        }
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to delete elements: {e}"}

def handle_move_element(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle move element command"""
    try:
        # Import here to avoid import-time errors
        import cadwork

        # Import here to avoid import-time errors
        import element_controller as ec

        element_ids = validate_element_ids(args.get("element_ids", []))
        move_vector_raw = args.get("move_vector")
        
        if not element_ids:
            return {"status": "error", "message": "No elements specified for moving"}
        
        if move_vector_raw is None:
            raise ValueError("Missing required argument: move_vector")
        
        # Convert move vector
        move_vector = to_point_3d(move_vector_raw)
        
        # Move elements
        ec.move_element(element_ids, move_vector)
        
        return {
            "status": "ok", 
            "moved_count": len(element_ids),
            "message": f"Successfully moved {len(element_ids)} elements"
        }
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to move elements: {e}"}

def handle_get_user_element_ids(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get user element IDs command"""
    try:
        # Import here to avoid import-time errors
        import cadwork

        # Import here to avoid import-time errors
        import element_controller as ec

        count = args.get("count")
        
        if count is not None:
            # Get specific number of user-selected elements
            try:
                count = int(count)
                if count <= 0:
                    raise ValueError("Count must be positive")
                user_ids = ec.get_user_element_ids_with_count(count)
            except (ValueError, TypeError):
                raise ValueError(f"Invalid count value: {count}")
        else:
            # Get user-selected elements without count limit
            user_ids = ec.get_user_element_ids()
        
        return {
            "status": "ok", 
            "element_ids": user_ids,
            "selected_count": len(user_ids)
        }
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to get user elements: {e}"}

def handle_copy_elements(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle copy elements command"""
    try:
        # Import here to avoid import-time errors
        import cadwork

        # Import here to avoid import-time errors
        import element_controller as ec

        element_ids = validate_element_ids(args.get("element_ids", []))
        copy_vector_raw = args.get("copy_vector")
        
        if not element_ids:
            return {"status": "error", "message": "No elements specified for copying"}
        
        if copy_vector_raw is None:
            raise ValueError("Missing required argument: copy_vector")
        
        # Convert copy vector
        copy_vector = to_point_3d(copy_vector_raw)
        
        # Copy elements
        new_element_ids = ec.copy_elements(element_ids, copy_vector)
        
        if isinstance(new_element_ids, list):
            return {
                "status": "ok", 
                "new_element_ids": new_element_ids,
                "copied_count": len(new_element_ids),
                "message": f"Successfully copied {len(element_ids)} elements"
            }
        else:
            return {
                "status": "error", 
                "message": f"Copy operation failed, returned: {new_element_ids}"
            }
            
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to copy elements: {e}"}

def handle_get_visible_element_ids(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get visible element IDs command"""
    try:
        # Import here to avoid import-time errors
        import cadwork

        # Import here to avoid import-time errors
        import element_controller as ec

        visible_ids = ec.get_visible_identifiable_element_ids()
        return {"status": "ok", "element_ids": visible_ids}
    except Exception as e:
        return {"status": "error", "message": f"Failed to get visible elements: {e}"}

def handle_get_element_info(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get element info command"""
    try:
        # Import here to avoid import-time errors
        import cadwork

        # Import here to avoid import-time errors
        import element_controller as ec

        element_id = args.get("element_id")
        if element_id is None:
            raise ValueError("Missing required argument: element_id")
        
        element_id = int(element_id)
        
        # Get geometry
        p1 = gc.get_p1(element_id)
        p2 = gc.get_p2(element_id)
        p3 = gc.get_p3(element_id)
        vec_x = gc.get_xl(element_id)
        vec_y = gc.get_yl(element_id)
        vec_z = gc.get_zl(element_id)
        
        # Get basic attributes
        attributes = {}
        try:
            attributes["name"] = ac.get_name(element_id)
        except:
            attributes["name"] = None
            
        try:
            attributes["group"] = ac.get_group(element_id)
        except:
            attributes["group"] = None
            
        try:
            attributes["subgroup"] = ac.get_subgroup(element_id)
        except:
            attributes["subgroup"] = None
            
        try:
            attributes["comment"] = ac.get_comment(element_id)
        except:
            attributes["comment"] = None
        
        # Get material
        try:
            material_name = ac.get_element_material_name(element_id)
            attributes["material"] = material_name if material_name else None
        except:
            attributes["material"] = None
        
        element_info = {
            "element_id": element_id,
            "geometry": {
                "p1": point_3d_to_list(p1),
                "p2": point_3d_to_list(p2),
                "p3": point_3d_to_list(p3),
                "vector_x": point_3d_to_list(vec_x),
                "vector_y": point_3d_to_list(vec_y),
                "vector_z": point_3d_to_list(vec_z),
            },
            "attributes": attributes
        }
        
        return {"status": "ok", "info": element_info}
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Element not found or API error: {e}"}

# --- EXTENDED ELEMENT CREATION HANDLERS ---

def handle_create_circular_beam_points(params):
    """Handle circular beam creation with points"""
    try:
        import element_controller as ec
        import cadwork
        
        diameter = params["diameter"]
        p1 = to_point_3d(params["p1"])
        p2 = to_point_3d(params["p2"])
        p3 = to_point_3d(params["p3"]) if params.get("p3") else None
        
        if p3:
            element_id = ec.create_circular_beam_points(diameter, p1, p2, p3)
        else:
            element_id = ec.create_circular_beam_points(diameter, p1, p2)
            
        return {"status": "ok", "element_id": element_id}
        
    except Exception as e:
        return {"status": "error", "message": f"Failed to create circular beam: {e}"}

def handle_create_square_beam_points(params):
    """Handle square beam creation with points"""
    try:
        import element_controller as ec
        import cadwork
        
        width = params["width"]
        p1 = to_point_3d(params["p1"])
        p2 = to_point_3d(params["p2"])
        p3 = to_point_3d(params["p3"]) if params.get("p3") else None
        
        if p3:
            element_id = ec.create_square_beam_points(width, p1, p2, p3)
        else:
            element_id = ec.create_square_beam_points(width, p1, p2)
            
        return {"status": "ok", "element_id": element_id}
        
    except Exception as e:
        return {"status": "error", "message": f"Failed to create square beam: {e}"}

def handle_create_standard_beam_points(params):
    """Handle standard beam creation with points"""
    try:
        import element_controller as ec
        import cadwork
        
        standard_element_name = params["standard_element_name"]
        p1 = to_point_3d(params["p1"])
        p2 = to_point_3d(params["p2"])
        p3 = to_point_3d(params["p3"]) if params.get("p3") else None
        
        if p3:
            element_id = ec.create_standard_beam_points(standard_element_name, p1, p2, p3)
        else:
            element_id = ec.create_standard_beam_points(standard_element_name, p1, p2)
            
        return {"status": "ok", "element_id": element_id}
        
    except Exception as e:
        return {"status": "error", "message": f"Failed to create standard beam: {e}"}

def handle_create_standard_panel_points(params):
    """Handle standard panel creation with points"""
    try:
        import element_controller as ec
        import cadwork
        
        standard_element_name = params["standard_element_name"]
        p1 = to_point_3d(params["p1"])
        p2 = to_point_3d(params["p2"])
        p3 = to_point_3d(params["p3"]) if params.get("p3") else None
        
        if p3:
            element_id = ec.create_standard_panel_points(standard_element_name, p1, p2, p3)
        else:
            element_id = ec.create_standard_panel_points(standard_element_name, p1, p2)
            
        return {"status": "ok", "element_id": element_id}
        
    except Exception as e:
        return {"status": "error", "message": f"Failed to create standard panel: {e}"}

def handle_create_drilling_points(params):
    """Handle drilling creation with points"""
    try:
        import element_controller as ec
        import cadwork
        
        diameter = params["diameter"]
        p1 = to_point_3d(params["p1"])
        p2 = to_point_3d(params["p2"])
        
        element_id = ec.create_drilling_points(diameter, p1, p2)
            
        return {"status": "ok", "element_id": element_id}
        
    except Exception as e:
        return {"status": "error", "message": f"Failed to create drilling: {e}"}

def handle_create_polygon_beam(params):
    """Handle polygon beam creation"""
    try:
        import element_controller as ec
        import cadwork
        
        polygon_vertices = [to_point_3d(vertex) for vertex in params["polygon_vertices"]]
        thickness = params["thickness"]
        xl = to_point_3d(params["xl"])
        zl = to_point_3d(params["zl"])
        
        element_id = ec.create_polygon_beam(polygon_vertices, thickness, xl, zl)
            
        return {"status": "ok", "element_id": element_id}
        
    except Exception as e:
        return {"status": "error", "message": f"Failed to create polygon beam: {e}"}
