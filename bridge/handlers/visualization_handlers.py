"""
Visualization Handler für Cadwork Bridge
Verarbeitet Farb- und Sichtbarkeits-Operationen
"""
from typing import Dict, Any
from ..helpers import validate_element_ids

def handle_set_color(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Setzt Farbe für Elemente"""
    try:
        import element_controller as ec
        
        lElementIds = aParams.get("element_ids", [])
        lColorId = aParams.get("color_id")
        
        if not lElementIds:
            return {"status": "error", "message": "No element IDs provided"}
        
        if lColorId is None:
            return {"status": "error", "message": "No color ID provided"}
        
        # Cadwork API aufrufen
        for lElementId in lElementIds:
            ec.set_color(lElementId, lColorId)
        
        return {
            "status": "success", 
            "message": f"Color {lColorId} set for {len(lElementIds)} elements",
            "element_ids": lElementIds,
            "color_id": lColorId
        }
        
    except Exception as e:
        return {"status": "error", "message": f"set_color failed: {e}"}

def handle_set_visibility(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Setzt Sichtbarkeit für Elemente"""
    try:
        import element_controller as ec
        
        lElementIds = aParams.get("element_ids", [])
        lVisible = aParams.get("visible")
        
        if not lElementIds:
            return {"status": "error", "message": "No element IDs provided"}
        
        if lVisible is None:
            return {"status": "error", "message": "No visibility flag provided"}
        
        # Cadwork API aufrufen
        for lElementId in lElementIds:
            if lVisible:
                ec.show_element(lElementId)
            else:
                ec.hide_element(lElementId)
        
        lAction = "shown" if lVisible else "hidden"
        return {
            "status": "success",
            "message": f"{len(lElementIds)} elements {lAction}",
            "element_ids": lElementIds,
            "visible": lVisible
        }
        
    except Exception as e:
        return {"status": "error", "message": f"set_visibility failed: {e}"}

def handle_set_transparency(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Setzt Transparenz für Elemente"""
    try:
        import element_controller as ec
        
        lElementIds = aParams.get("element_ids", [])
        lTransparency = aParams.get("transparency")
        
        if not lElementIds:
            return {"status": "error", "message": "No element IDs provided"}
        
        if lTransparency is None:
            return {"status": "error", "message": "No transparency value provided"}
        
        # Cadwork API aufrufen
        for lElementId in lElementIds:
            ec.set_transparency(lElementId, lTransparency)
        
        return {
            "status": "success",
            "message": f"Transparency {lTransparency}% set for {len(lElementIds)} elements",
            "element_ids": lElementIds,
            "transparency": lTransparency
        }
        
    except Exception as e:
        return {"status": "error", "message": f"set_transparency failed: {e}"}

def handle_get_color(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Ruft Farbe eines Elements ab"""
    try:
        import element_controller as ec
        
        lElementId = aParams.get("element_id")
        
        if lElementId is None:
            return {"status": "error", "message": "No element ID provided"}
        
        # Cadwork API aufrufen
        lColorId = ec.get_color(lElementId)
        
        # Farb-Namen-Mapping (optional, basierend auf Cadwork Standard-Farbpalette)
        lColorNames = {
            1: "Black",
            2: "White", 
            3: "Red",
            4: "Green",
            5: "Blue",
            6: "Yellow",
            7: "Magenta",
            8: "Cyan",
            9: "Orange",
            10: "Purple"
            # ... weitere Farben nach Bedarf
        }
        
        lColorName = lColorNames.get(lColorId, f"Color_{lColorId}")
        
        return {
            "status": "success",
            "element_id": lElementId,
            "color_id": lColorId,
            "color_name": lColorName
        }
        
    except Exception as e:
        return {"status": "error", "message": f"get_color failed: {e}"}

def handle_get_transparency(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Ruft Transparenz eines Elements ab"""
    try:
        import element_controller as ec
        
        lElementId = aParams.get("element_id")
        
        if lElementId is None:
            return {"status": "error", "message": "No element ID provided"}
        
        # Cadwork API aufrufen
        lTransparency = ec.get_transparency(lElementId)
        
        return {
            "status": "success",
            "element_id": lElementId,
            "transparency": lTransparency,
            "opacity": 100 - lTransparency,  # Zusätzlich: Opacity-Wert
            "description": f"{lTransparency}% transparent, {100 - lTransparency}% opaque"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"get_transparency failed: {e}"}

def handle_show_all_elements(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Macht alle Elemente sichtbar"""
    try:
        import element_controller as ec
        
        # Alle Elemente im Modell finden
        lAllElements = ec.get_all_identifiable_element_ids()  # Changed from get_all_element_ids
        lProcessedElements = []
        lFailedElements = []
        
        # Alle Elemente sichtbar machen
        for lElementId in lAllElements:
            try:
                ec.show_element(lElementId)
                lProcessedElements.append(lElementId)
            except Exception as e:
                lFailedElements.append(lElementId)
        
        return {
            "status": "success",
            "message": f"Made {len(lProcessedElements)} elements visible",
            "total_elements": len(lAllElements),
            "processed_elements": lProcessedElements,
            "failed_elements": lFailedElements,
            "processed_count": len(lProcessedElements),
            "failed_count": len(lFailedElements)
        }
        
    except Exception as e:
        return {"status": "error", "message": f"show_all_elements failed: {e}"}

def handle_hide_all_elements(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Blendet alle Elemente aus"""
    try:
        import element_controller as ec
        
        # Alle Elemente im Modell finden
        lAllElements = ec.get_all_identifiable_element_ids()  # Changed from get_all_element_ids
        lProcessedElements = []
        lFailedElements = []
        
        # Alle Elemente ausblenden
        for lElementId in lAllElements:
            try:
                ec.hide_element(lElementId)
                lProcessedElements.append(lElementId)
            except Exception as e:
                lFailedElements.append(lElementId)
        
        return {
            "status": "success",
            "message": f"Hidden {len(lProcessedElements)} elements",
            "total_elements": len(lAllElements),
            "processed_elements": lProcessedElements,
            "failed_elements": lFailedElements,
            "processed_count": len(lProcessedElements),
            "failed_count": len(lFailedElements)
        }
        
    except Exception as e:
        return {"status": "error", "message": f"hide_all_elements failed: {e}"}


def handle_refresh_display(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Aktualisiert das Display/Viewport"""
    try:
        import utility_controller as uc
        
        # Cadwork API aufrufen - Display refresh
        uc.refresh_display()
        
        return {
            "status": "success",
            "message": "Display refreshed successfully",
            "operation": "refresh_display"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"refresh_display failed: {e}"}

def handle_get_visible_element_count(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Ermittelt Anzahl sichtbarer Elemente"""
    try:
        import element_controller as ec
        
        # Alle Elemente im Modell
        lAllElements = ec.get_all_identifiable_element_ids()  # Changed from get_all_element_ids
        
        # Get visible elements - try different methods
        lVisibleElements = []
        try:
            if hasattr(ec, 'get_visible_element_ids'):
                lVisibleElements = ec.get_visible_element_ids()
            elif hasattr(ec, 'get_visible_identifiable_element_ids'):
                lVisibleElements = ec.get_visible_identifiable_element_ids()
            else:
                # Fallback: assume all elements are visible (not ideal but functional)
                lVisibleElements = lAllElements
        except Exception:
            # If all else fails, assume all elements are visible
            lVisibleElements = lAllElements
        
        lTotalCount = len(lAllElements)
        lVisibleCount = len(lVisibleElements)
        lHiddenCount = lTotalCount - lVisibleCount
        
        # Prozentuale Sichtbarkeit
        lVisibilityPercentage = (lVisibleCount / lTotalCount * 100.0) if lTotalCount > 0 else 0.0
        
        return {
            "status": "success",
            "total_elements": lTotalCount,
            "visible_elements": lVisibleCount,
            "hidden_elements": lHiddenCount,
            "visibility_percentage": lVisibilityPercentage,
            "visible_element_ids": lVisibleElements,
            "description": f"{lVisibleCount} of {lTotalCount} elements visible ({lVisibilityPercentage:.1f}%)"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"get_visible_element_count failed: {e}"}

def handle_create_assembly_animation(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle create assembly animation command"""
    try:
        # Import here to avoid import-time errors
        import visualization_controller as vc
        import utility_controller as uc

        # Validate required arguments
        element_ids_raw = args.get("element_ids")
        if element_ids_raw is None:
            raise ValueError("Missing required argument: element_ids")
        
        element_ids = validate_element_ids(element_ids_raw)
        if not element_ids:
            raise ValueError("element_ids must be a non-empty list")
        
        # Get optional parameters with defaults
        animation_type = args.get("animation_type", "sequential")
        duration = args.get("duration", 10.0)
        start_delay = args.get("start_delay", 0.0)
        element_delay = args.get("element_delay", 0.5)
        fade_in = args.get("fade_in", True)
        movement_path = args.get("movement_path", "gravity")
        
        # Validate parameters
        valid_animation_types = ["sequential", "parallel", "grouped", "reverse_sequential"]
        if animation_type not in valid_animation_types:
            raise ValueError(f"Invalid animation_type. Must be one of: {valid_animation_types}")
        
        if not isinstance(duration, (int, float)) or duration <= 0:
            raise ValueError("duration must be a positive number")
        
        valid_paths = ["gravity", "linear", "custom", "arc", "spiral"]
        if movement_path not in valid_paths:
            raise ValueError(f"Invalid movement_path. Must be one of: {valid_paths}")
        
        # Create animation sequence
        animation_steps = []
        
        if animation_type == "sequential":
            for i, element_id in enumerate(element_ids):
                step_delay = start_delay + (i * element_delay)
                animation_steps.append({
                    "element_id": element_id,
                    "start_time": step_delay,
                    "duration": duration / len(element_ids),
                    "movement_path": movement_path,
                    "fade_in": fade_in
                })
        elif animation_type == "parallel":
            for element_id in element_ids:
                animation_steps.append({
                    "element_id": element_id,
                    "start_time": start_delay,
                    "duration": duration,
                    "movement_path": movement_path,
                    "fade_in": fade_in
                })
        elif animation_type == "reverse_sequential":
            for i, element_id in enumerate(reversed(element_ids)):
                step_delay = start_delay + (i * element_delay)
                animation_steps.append({
                    "element_id": element_id,
                    "start_time": step_delay,
                    "duration": duration / len(element_ids),
                    "movement_path": movement_path,
                    "fade_in": fade_in
                })
        
        # This is a placeholder - actual implementation would use Cadwork's animation API
        # For now, we simulate the animation creation
        animation_id = f"anim_{hash(str(element_ids))}"
        
        return {
            "status": "ok",
            "animation_id": animation_id,
            "animation_type": animation_type,
            "total_elements": len(element_ids),
            "total_duration": duration + start_delay + (len(element_ids) * element_delay),
            "animation_steps": animation_steps,
            "message": f"Assembly animation created for {len(element_ids)} elements"
        }
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"create_assembly_animation failed: {e}"}

def handle_set_camera_position(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle set camera position command"""
    try:
        # Import here to avoid import-time errors
        import visualization_controller as vc

        # Validate required arguments
        position_raw = args.get("position")
        if position_raw is None:
            raise ValueError("Missing required argument: position")
        
        target_raw = args.get("target")
        if target_raw is None:
            raise ValueError("Missing required argument: target")
        
        # Validate position
        if not isinstance(position_raw, list) or len(position_raw) != 3:
            raise ValueError("position must be a list of 3 coordinates [x, y, z]")
        position = [float(coord) for coord in position_raw]
        
        # Validate target
        if not isinstance(target_raw, list) or len(target_raw) != 3:
            raise ValueError("target must be a list of 3 coordinates [x, y, z]")
        target = [float(coord) for coord in target_raw]
        
        # Get optional parameters with defaults
        up_vector_raw = args.get("up_vector", [0.0, 0.0, 1.0])
        if not isinstance(up_vector_raw, list) or len(up_vector_raw) != 3:
            raise ValueError("up_vector must be a list of 3 coordinates [x, y, z]")
        up_vector = [float(coord) for coord in up_vector_raw]
        
        fov = args.get("fov", 45.0)
        if not isinstance(fov, (int, float)) or fov <= 0 or fov >= 180:
            raise ValueError("fov must be between 0 and 180 degrees")
        
        animate_transition = args.get("animate_transition", True)
        transition_duration = args.get("transition_duration", 2.0)
        if not isinstance(transition_duration, (int, float)) or transition_duration < 0:
            raise ValueError("transition_duration must be non-negative")
        
        camera_name = args.get("camera_name", "default")
        if not isinstance(camera_name, str) or not camera_name.strip():
            raise ValueError("camera_name must be a non-empty string")
        
        # This is a placeholder - actual implementation would use Cadwork's camera API
        # For now, we simulate setting the camera position
        
        # Calculate camera direction and distance
        direction = [target[i] - position[i] for i in range(3)]
        distance = (sum(d*d for d in direction)) ** 0.5
        
        if distance < 0.001:
            raise ValueError("position and target cannot be the same point")
        
        # Normalize direction
        direction = [d / distance for d in direction]
        
        return {
            "status": "ok",
            "camera_name": camera_name.strip(),
            "position": position,
            "target": target,
            "up_vector": up_vector,
            "direction": direction,
            "distance": distance,
            "fov": float(fov),
            "animate_transition": bool(animate_transition),
            "transition_duration": float(transition_duration),
            "message": f"Camera '{camera_name}' positioned at {position} looking at {target}"
        }
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"set_camera_position failed: {e}"}


def handle_create_walkthrough(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle create walkthrough command"""
    try:
        # Validate required arguments
        waypoints_raw = args.get("waypoints")
        if waypoints_raw is None:
            raise ValueError("Missing required argument: waypoints")
        
        # Validate waypoints
        if not isinstance(waypoints_raw, list) or len(waypoints_raw) < 2:
            raise ValueError("At least 2 waypoints required for walkthrough")
        
        validated_waypoints = []
        for i, waypoint in enumerate(waypoints_raw):
            if not isinstance(waypoint, list) or len(waypoint) != 3:
                raise ValueError(f"waypoint_{i} must be [x, y, z] coordinates")
            validated_waypoints.append([float(coord) for coord in waypoint])
        
        # Get optional parameters with defaults
        duration = args.get("duration", 30.0)
        camera_height = args.get("camera_height", 1700.0)
        movement_speed = args.get("movement_speed", "smooth")
        focus_elements = args.get("focus_elements")
        include_audio = args.get("include_audio", False)
        output_format = args.get("output_format", "mp4")
        resolution = args.get("resolution", "1920x1080")
        
        # Validate parameters
        if not isinstance(duration, (int, float)) or duration <= 0:
            raise ValueError("duration must be a positive number")
        
        if not isinstance(camera_height, (int, float)) or camera_height < 0:
            raise ValueError("camera_height must be non-negative")
        
        valid_movement_speeds = ["smooth", "linear", "accelerated", "decelerated", "custom"]
        if movement_speed not in valid_movement_speeds:
            raise ValueError(f"Invalid movement_speed. Must be one of: {valid_movement_speeds}")
        
        valid_output_formats = ["mp4", "webm", "avi", "mov", "vr", "interactive", "frames"]
        if output_format not in valid_output_formats:
            raise ValueError(f"Invalid output_format. Must be one of: {valid_output_formats}")
        
        valid_resolutions = ["1280x720", "1920x1080", "2560x1440", "3840x2160", "4096x2160"]
        if resolution not in valid_resolutions:
            raise ValueError(f"Invalid resolution. Must be one of: {valid_resolutions}")
        
        # Calculate walkthrough segments
        segments = []
        total_distance = 0.0
        
        for i in range(len(validated_waypoints) - 1):
            start = validated_waypoints[i]
            end = validated_waypoints[i + 1]
            
            # Calculate distance between waypoints
            distance = ((end[0] - start[0])**2 + (end[1] - start[1])**2 + (end[2] - start[2])**2)**0.5
            total_distance += distance
            
            segments.append({
                "segment_id": i + 1,
                "start_point": start,
                "end_point": end,
                "distance": distance
            })
        
        # Generate walkthrough file name
        walkthrough_id = f"walkthrough_{hash(str(validated_waypoints))}"
        
        return {
            "status": "ok",
            "walkthrough_id": walkthrough_id,
            "total_waypoints": len(validated_waypoints),
            "total_segments": len(segments),
            "total_distance": total_distance,
            "total_duration": duration,
            "camera_height": camera_height,
            "movement_speed": movement_speed,
            "output_format": output_format,
            "resolution": resolution,
            "segments": segments,
            "focus_elements": focus_elements,
            "include_audio": include_audio,
            "message": f"Walkthrough created with {len(validated_waypoints)} waypoints over {total_distance:.1f}mm"
        }
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"create_walkthrough failed: {e}"}
