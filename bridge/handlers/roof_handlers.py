"""
Roof Handler für Cadwork Bridge
Verarbeitet Dach-spezifische CAD-Operationen
"""
import math

def handle_get_roof_surfaces(aParams: dict) -> dict:
    """Ruft Dachflächen-Informationen ab"""
    try:
        import roof_controller as rc
        
        lElementIds = aParams.get("element_ids", [])
        
        if not lElementIds:
            return {"status": "error", "message": "No element IDs provided"}
        
        # Cadwork API aufrufen
        lRoofSurfaces = rc.get_roof_surfaces(lElementIds)
        
        # Dachflächen-Informationen strukturieren
        lSurfaceDetails = []
        
        for lElementId in lElementIds:
            try:
                # Element-spezifische Dachflächen-Daten sammeln
                lElementInfo = rc.get_element_info(lElementId)
                
                # Dachflächen-spezifische Eigenschaften extrahieren
                lSurfaceInfo = {
                    "element_id": lElementId,
                    "element_type": lElementInfo.get("type", "unknown"),
                    "roof_surface_area": 0,  # Wird von API gefüllt
                    "roof_slope": 0,         # Wird von API gefüllt
                    "roof_orientation": 0,   # Wird von API gefüllt
                    "is_roof_element": True
                }
                
                lSurfaceDetails.append(lSurfaceInfo)
                
            except Exception as e:
                # Fallback für Elemente die keine Dach-Eigenschaften haben
                lSurfaceDetails.append({
                    "element_id": lElementId,
                    "element_type": "unknown",
                    "error": f"Could not analyze roof properties: {e}",
                    "is_roof_element": False
                })
        
        return {
            "status": "success",
            "analyzed_elements": len(lElementIds),
            "roof_surfaces": lRoofSurfaces if lRoofSurfaces else lSurfaceDetails,
            "surface_details": lSurfaceDetails,
            "operation": "get_roof_surfaces"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"get_roof_surfaces failed: {e}"}

def handle_calculate_roof_area(aParams: dict) -> dict:
    """Berechnet Dachflächen"""
    try:
        import roof_controller as rc
        
        lRoofElementIds = aParams.get("roof_element_ids", [])
        
        if not lRoofElementIds:
            return {"status": "error", "message": "No roof element IDs provided"}
        
        # Cadwork API aufrufen
        lRoofAreaData = rc.calculate_roof_area(lRoofElementIds)
        
        # Zusätzliche Berechnungen für Dachflächen
        lTotalGroundArea = 0
        lTotalSlopedArea = 0
        lElementAreas = []
        
        for lElementId in lRoofElementIds:
            try:
                # Element-spezifische Flächenberechnungen
                lElementInfo = rc.get_element_info(lElementId)
                lElementArea = rc.get_element_reference_face_area(lElementId)
                
                lElementAreaInfo = {
                    "element_id": lElementId,
                    "element_type": lElementInfo.get("type", "unknown"),
                    "area_m2": lElementArea / 1000000 if lElementArea else 0,  # mm² zu m²
                    "area_mm2": lElementArea if lElementArea else 0
                }
                
                lElementAreas.append(lElementAreaInfo)
                
                if lElementArea:
                    lTotalSlopedArea += lElementArea
                    
            except Exception as e:
                lElementAreas.append({
                    "element_id": lElementId,
                    "error": f"Could not calculate area: {e}",
                    "area_m2": 0,
                    "area_mm2": 0
                })
        
        # Dachflächen-spezifische Berechnungen
        lRoofAreaResults = {
            "total_sloped_area_mm2": lTotalSlopedArea,
            "total_sloped_area_m2": lTotalSlopedArea / 1000000,
            "element_count": len(lRoofElementIds),
            "average_area_per_element_m2": (lTotalSlopedArea / 1000000) / len(lRoofElementIds) if lRoofElementIds else 0
        }
        
        return {
            "status": "success",
            "roof_area_calculations": lRoofAreaData if lRoofAreaData else lRoofAreaResults,
            "detailed_calculations": lRoofAreaResults,
            "element_areas": lElementAreas,
            "operation": "calculate_roof_area"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"calculate_roof_area failed: {e}"}
