"""
Visualization Handler für Cadwork Bridge
Verarbeitet Farb- und Sichtbarkeits-Operationen
"""

def handle_set_color(aParams: dict) -> dict:
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

def handle_set_visibility(aParams: dict) -> dict:
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

def handle_set_transparency(aParams: dict) -> dict:
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

def handle_get_color(aParams: dict) -> dict:
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

def handle_get_transparency(aParams: dict) -> dict:
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

def handle_show_all_elements(aParams: dict) -> dict:
    """Macht alle Elemente sichtbar"""
    try:
        import element_controller as ec
        
        # Alle Elemente im Modell finden
        lAllElements = ec.get_all_element_ids()
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

def handle_hide_all_elements(aParams: dict) -> dict:
    """Blendet alle Elemente aus"""
    try:
        import element_controller as ec
        
        # Alle Elemente im Modell finden
        lAllElements = ec.get_all_element_ids()
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


def handle_refresh_display(aParams: dict) -> dict:
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

def handle_get_visible_element_count(aParams: dict) -> dict:
    """Ermittelt Anzahl sichtbarer Elemente"""
    try:
        import element_controller as ec
        
        # Alle Elemente im Modell
        lAllElements = ec.get_all_element_ids()
        lVisibleElements = ec.get_visible_element_ids()
        
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
