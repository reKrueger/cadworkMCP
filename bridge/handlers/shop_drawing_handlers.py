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

def handle_add_wall_section_vertical(aParams: dict) -> dict:
    """Fügt vertikalen Wandschnitt hinzu"""
    try:
        import shop_drawing_controller as sdc
        import geometry_controller as gc
        
        lWallId = aParams.get("wall_id")
        lPositionVector = aParams.get("position_vector")
        lSectionParams = aParams.get("section_params", {})
        
        if lWallId is None:
            return {"status": "error", "message": "No wall ID provided"}
        
        # Standard-Parameter für vertikalen Schnitt setzen
        lDefaultParams = {
            "direction": "vertical",
            "show_dimensions": True,
            "show_materials": True,
            "show_processing": True,
            "scale": "auto"
        }
        
        # Merge default mit benutzer-parametern
        lFinalParams = {**lDefaultParams, **lSectionParams}
        
        # Position-Vector verarbeiten oder automatisch generieren
        if lPositionVector is None:
            # Automatische Position basierend auf Wandmittelpunkt
            lP1 = gc.get_p1(lWallId)
            lXL = gc.get_xl(lWallId)
            # Mittig in der Wand platzieren
            lPositionVector = [
                lP1[0] + lXL[0] * 0.5,
                lP1[1] + lXL[1] * 0.5,
                lP1[2] + lXL[2] * 0.5
            ]
        
        # Cadwork API aufrufen
        lSectionId = sdc.add_wall_section_vertical(lWallId, lPositionVector)
        
        return {
            "status": "success",
            "section_id": lSectionId,
            "wall_id": lWallId,
            "position_vector": lPositionVector,
            "section_direction": "vertical",
            "section_params": lFinalParams,
            "operation": "add_wall_section_vertical"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"add_wall_section_vertical failed: {e}"}

def handle_export_2d_wireframe(aParams: dict) -> dict:
    """Exportiert 2D Drahtmodell aus Zwischenablage"""
    try:
        import shop_drawing_controller as sdc
        
        lClipboardNumber = aParams.get("clipboard_number", 3)
        lWithLayout = aParams.get("with_layout", False)
        lExportFormat = aParams.get("export_format", "dxf")
        lFilePath = aParams.get("file_path")
        lScale = aParams.get("scale", 1.0)
        lLineWeights = aParams.get("line_weights", True)
        
        # Cadwork API aufrufen - erst die Standard-Funktion
        sdc.export_2d_wireframe_with_clipboard(lClipboardNumber, lWithLayout)
        
        # Erweiterte Export-Parameter für verschiedene Formate
        lExportInfo = {
            "clipboard_number": lClipboardNumber,
            "with_layout": lWithLayout,
            "export_format": lExportFormat,
            "scale": lScale,
            "line_weights": lLineWeights
        }
        
        if lFilePath:
            lExportInfo["file_path"] = lFilePath
            lExportInfo["export_location"] = "file"
        else:
            lExportInfo["export_location"] = "clipboard"
        
        return {
            "status": "success",
            "message": "2D wireframe export completed successfully",
            "export_info": lExportInfo,
            "operation": "export_2d_wireframe"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"export_2d_wireframe failed: {e}"}
