"""
Shop Drawing Handler für Cadwork Bridge
Verarbeitet Werkstattzeichnungs-spezifische Operationen
"""

def handle_add_wall_section_x(aParams: dict) -> dict:
    """Fügt Wandschnitt in X-Richtung hinzu"""
    try:
        import shop_drawing_controller as sdc
        
        lWallId = aParams.get("wall_id")
        lSectionParams = aParams.get("section_params", {})
        
        if lWallId is None:
            return {"status": "error", "message": "No wall ID provided"}
        
        # Standard-Parameter für X-Schnitt setzen falls nicht vorhanden
        lDefaultParams = {
            "direction": "x",
            "position": "center",
            "depth": "auto",
            "show_dimensions": True,
            "show_materials": True
        }
        
        # Merge default mit benutzer-parametern
        lFinalParams = {**lDefaultParams, **lSectionParams}
        
        # Cadwork API aufrufen
        lSectionId = sdc.add_wall_section_x(lWallId, lFinalParams)
        
        return {
            "status": "success",
            "section_id": lSectionId,
            "wall_id": lWallId,
            "section_direction": "x",
            "section_params": lFinalParams,
            "operation": "add_wall_section_x"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"add_wall_section_x failed: {e}"}

def handle_add_wall_section_y(aParams: dict) -> dict:
    """Fügt Wandschnitt in Y-Richtung hinzu"""
    try:
        import shop_drawing_controller as sdc
        
        lWallId = aParams.get("wall_id")
        lSectionParams = aParams.get("section_params", {})
        
        if lWallId is None:
            return {"status": "error", "message": "No wall ID provided"}
        
        # Standard-Parameter für Y-Schnitt setzen falls nicht vorhanden
        lDefaultParams = {
            "direction": "y",
            "position": "center",
            "depth": "auto",
            "show_dimensions": True,
            "show_materials": True
        }
        
        # Merge default mit benutzer-parametern
        lFinalParams = {**lDefaultParams, **lSectionParams}
        
        # Cadwork API aufrufen
        lSectionId = sdc.add_wall_section_y(lWallId, lFinalParams)
        
        return {
            "status": "success",
            "section_id": lSectionId,
            "wall_id": lWallId,
            "section_direction": "y",
            "section_params": lFinalParams,
            "operation": "add_wall_section_y"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"add_wall_section_y failed: {e}"}
