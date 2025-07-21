"""
Reparierter Visualization Handler mit ControllerManager
"""
from typing import Dict, Any, List
from .base_handler import BaseHandler, validate_element_ids
from ..controller_manager import call_cadwork_function

def handle_set_color(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Setzt Farbe für Elemente"""
    try:
        lElementIds = validate_element_ids(aParams.get("element_ids", []))
        lColorId = aParams.get("color_id")
        
        if lColorId is None:
            return {"status": "error", "message": "No color ID provided"}
        
        # Verwende Controller Manager
        call_cadwork_function('set_color', lElementIds, lColorId)
        
        return {
            "status": "success",
            "message": f"Color {lColorId} set for {len(lElementIds)} elements",
            "element_ids": lElementIds,
            "color_id": lColorId
        }
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"set_color failed: {e}"}

def handle_set_visibility(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Setzt Sichtbarkeit für Elemente"""
    try:
        lElementIds = validate_element_ids(aParams.get("element_ids", []))
        lVisible = aParams.get("visible")
        
        if lVisible is None:
            return {"status": "error", "message": "No visibility flag provided"}
        
        # Verwende Controller Manager
        if lVisible:
            call_cadwork_function('show_elements', lElementIds)
        else:
            call_cadwork_function('hide_elements', lElementIds)
        
        lAction = "shown" if lVisible else "hidden"
        return {
            "status": "success",
            "message": f"{len(lElementIds)} elements {lAction}",
            "element_ids": lElementIds,
            "visible": lVisible
        }
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"set_visibility failed: {e}"}

def handle_set_transparency(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Setzt Transparenz für Elemente"""
    try:
        lElementIds = validate_element_ids(aParams.get("element_ids", []))
        lTransparency = aParams.get("transparency")
        
        if lTransparency is None:
            return {"status": "error", "message": "No transparency value provided"}
        
        # Verwende Controller Manager
        call_cadwork_function('set_transparency', lElementIds, lTransparency)
        
        return {
            "status": "success",
            "message": f"Transparency {lTransparency}% set for {len(lElementIds)} elements",
            "element_ids": lElementIds,
            "transparency": lTransparency
        }
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"set_transparency failed: {e}"}

def handle_get_color(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Ruft Farbe eines Elements ab"""
    try:
        lElementId = aParams.get("element_id")
        
        if lElementId is None:
            return {"status": "error", "message": "No element ID provided"}
        
        # Verwende Controller Manager
        lColorId = call_cadwork_function('get_color', lElementId)
        
        # Farb-Namen-Mapping (optional, basierend auf Cadwork Standard-Farbpalette)
        lColorNames = {
            1: "Black", 2: "White", 3: "Red", 4: "Green", 5: "Blue",
            6: "Yellow", 7: "Magenta", 8: "Cyan", 9: "Orange", 10: "Purple"
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
        lElementId = aParams.get("element_id")
        
        if lElementId is None:
            return {"status": "error", "message": "No element ID provided"}
        
        # Verwende Controller Manager
        lTransparency = call_cadwork_function('get_transparency', lElementId)
        
        return {
            "status": "success",
            "element_id": lElementId,
            "transparency": lTransparency,
            "opacity": 100 - lTransparency
        }
        
    except Exception as e:
        return {"status": "error", "message": f"get_transparency failed: {e}"}

def handle_show_all_elements(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Zeigt alle Elemente"""
    try:
        # Verwende Controller Manager
        result = call_cadwork_function('show_all_elements')
        
        return {
            "status": "success",
            "message": "All elements made visible",
            "operation": "show_all_elements"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"show_all_elements failed: {e}"}

def handle_hide_all_elements(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Versteckt alle Elemente"""
    try:
        # Verwende Controller Manager
        result = call_cadwork_function('hide_all_elements')
        
        return {
            "status": "success",
            "message": "All elements hidden",
            "operation": "hide_all_elements"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"hide_all_elements failed: {e}"}

def handle_refresh_display(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Aktualisiert die Anzeige"""
    try:
        # Verwende Controller Manager
        result = call_cadwork_function('refresh_display')
        
        return {
            "status": "success",
            "message": "Display refreshed",
            "operation": "refresh_display"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"refresh_display failed: {e}"}

def handle_get_visible_element_count(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Zählt sichtbare Elemente"""
    try:
        # Verwende Controller Manager
        result = call_cadwork_function('get_visible_element_count')
        
        return {
            "status": "success",
            "visible_element_count": result,
            "operation": "get_visible_element_count"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"get_visible_element_count failed: {e}"}

# Weitere Handler können hier hinzugefügt werden...
def handle_create_visual_filter(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Erstellt visuellen Filter - Placeholder"""
    return {
        "status": "success",
        "message": "Visual filter created (placeholder)",
        "operation": "create_visual_filter"
    }

def handle_apply_color_scheme(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Wendet Farbschema an - Placeholder"""
    return {
        "status": "success", 
        "message": "Color scheme applied (placeholder)",
        "operation": "apply_color_scheme"
    }

def handle_create_assembly_animation(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Erstellt Montage-Animation - Placeholder"""
    return {
        "status": "success",
        "message": "Assembly animation created (placeholder)",
        "operation": "create_assembly_animation"
    }

def handle_set_camera_position(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Setzt Kameraposition - Placeholder"""
    return {
        "status": "success",
        "message": "Camera position set (placeholder)",
        "operation": "set_camera_position"
    }

def handle_create_walkthrough(aParams: Dict[str, Any]) -> Dict[str, Any]:
    """Erstellt Walkthrough - Placeholder"""
    return {
        "status": "success",
        "message": "Walkthrough created (placeholder)",
        "operation": "create_walkthrough"
    }
