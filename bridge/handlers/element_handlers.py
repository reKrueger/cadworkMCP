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

def handle_get_elements_by_type(aParams: dict) -> dict:
    """Findet alle Elemente eines bestimmten Typs"""
    try:
        import element_controller as ec
        
        lElementType = aParams.get("element_type")
        
        if not lElementType:
            return {"status": "error", "message": "No element type provided"}
        
        # Typ-Mapping (String -> Cadwork API Nummer)
        lTypeMapping = {
            "beam": 1,
            "panel": 2, 
            "drilling": 3,
            "node": 4,
            "line": 5,
            "surface": 6,
            "volume": 7,
            "container": 8,
            "auxiliary": 9,
            "text_object": 10,
            "dimension": 11,
            "architectural": 12
        }
        
        if lElementType not in lTypeMapping:
            return {"status": "error", "message": f"Unknown element type: {lElementType}"}
        
        lTypeId = lTypeMapping[lElementType]
        
        # Alle Elemente des Typs finden
        lAllElements = ec.get_all_element_ids()
        lFilteredElements = []
        
        for lElementId in lAllElements:
            try:
                lCurrentType = ec.get_element_type(lElementId)
                if lCurrentType == lTypeId:
                    lFilteredElements.append(lElementId)
            except:
                continue  # Element überspringen bei Fehlern
        
        return {
            "status": "success",
            "element_type": lElementType,
            "type_id": lTypeId,
            "element_ids": lFilteredElements,
            "count": len(lFilteredElements)
        }
        
    except Exception as e:
        return {"status": "error", "message": f"get_elements_by_type failed: {e}"}

def handle_filter_elements_by_material(aParams: dict) -> dict:
    """Filtert Elemente nach Material"""
    try:
        import element_controller as ec
        import attribute_controller as ac
        
        lMaterialName = aParams.get("material_name")
        
        if not lMaterialName:
            return {"status": "error", "message": "No material name provided"}
        
        # Alle Elemente im Modell durchsuchen
        lAllElements = ec.get_all_element_ids()
        lFilteredElements = []
        
        for lElementId in lAllElements:
            try:
                lCurrentMaterial = ac.get_element_material_name(lElementId)
                if lCurrentMaterial and lCurrentMaterial.strip().lower() == lMaterialName.strip().lower():
                    lFilteredElements.append(lElementId)
            except:
                continue  # Element überspringen bei Fehlern
        
        return {
            "status": "success",
            "material_name": lMaterialName,
            "element_ids": lFilteredElements,
            "count": len(lFilteredElements)
        }
        
    except Exception as e:
        return {"status": "error", "message": f"filter_elements_by_material failed: {e}"}

def handle_get_elements_in_group(aParams: dict) -> dict:
    """Findet alle Elemente in einer bestimmten Gruppe"""
    try:
        import element_controller as ec
        import attribute_controller as ac
        
        lGroupName = aParams.get("group_name")
        
        if not lGroupName:
            return {"status": "error", "message": "No group name provided"}
        
        # Alle Elemente im Modell durchsuchen
        lAllElements = ec.get_all_element_ids()
        lFilteredElements = []
        
        for lElementId in lAllElements:
            try:
                lCurrentGroup = ac.get_element_group(lElementId)
                if lCurrentGroup and lCurrentGroup.strip().lower() == lGroupName.strip().lower():
                    lFilteredElements.append(lElementId)
            except:
                continue  # Element überspringen bei Fehlern
        
        return {
            "status": "success",
            "group_name": lGroupName,
            "element_ids": lFilteredElements,
            "count": len(lFilteredElements)
        }
        
    except Exception as e:
        return {"status": "error", "message": f"get_elements_in_group failed: {e}"}

def handle_get_element_count_by_type(aParams: dict) -> dict:
    """Ermittelt Anzahl Elemente pro Typ"""
    try:
        import element_controller as ec
        
        # Typ-Mapping
        lTypeMapping = {
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
        
        # Alle Elemente im Modell
        lAllElements = ec.get_all_element_ids()
        lTypeCounts = {}
        lTotalCount = 0
        
        # Elemente nach Typ zählen
        for lElementId in lAllElements:
            try:
                lTypeId = ec.get_element_type(lElementId)
                lTypeName = lTypeMapping.get(lTypeId, f"unknown_type_{lTypeId}")
                
                if lTypeName not in lTypeCounts:
                    lTypeCounts[lTypeName] = 0
                lTypeCounts[lTypeName] += 1
                lTotalCount += 1
            except:
                continue  # Element überspringen bei Fehlern
        
        # Prozentuale Verteilung berechnen
        lTypePercentages = {}
        if lTotalCount > 0:
            for lTypeName, lCount in lTypeCounts.items():
                lTypePercentages[lTypeName] = (lCount / lTotalCount) * 100.0
        
        return {
            "status": "success",
            "total_elements": lTotalCount,
            "type_counts": lTypeCounts,
            "type_percentages": lTypePercentages,
            "available_types": list(lTypeCounts.keys())
        }
        
    except Exception as e:
        return {"status": "error", "message": f"get_element_count_by_type failed: {e}"}

def handle_get_material_statistics(aParams: dict) -> dict:
    """Ermittelt Material-Statistiken des gesamten Modells"""
    try:
        import element_controller as ec
        import attribute_controller as ac
        
        # Alle Elemente im Modell
        lAllElements = ec.get_all_element_ids()
        lMaterialCounts = {}
        lTotalCount = 0
        lElementsWithoutMaterial = 0
        
        # Materialien aller Elemente zählen
        for lElementId in lAllElements:
            try:
                lMaterial = ac.get_element_material_name(lElementId)
                if lMaterial and lMaterial.strip():
                    lMaterialName = lMaterial.strip()
                    if lMaterialName not in lMaterialCounts:
                        lMaterialCounts[lMaterialName] = 0
                    lMaterialCounts[lMaterialName] += 1
                else:
                    lElementsWithoutMaterial += 1
                lTotalCount += 1
            except:
                lElementsWithoutMaterial += 1
                lTotalCount += 1
        
        # Prozentuale Verteilung berechnen
        lMaterialPercentages = {}
        if lTotalCount > 0:
            for lMaterialName, lCount in lMaterialCounts.items():
                lMaterialPercentages[lMaterialName] = (lCount / lTotalCount) * 100.0
        
        # Top Materialien sortieren
        lSortedMaterials = sorted(lMaterialCounts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "status": "success",
            "total_elements": lTotalCount,
            "elements_with_material": lTotalCount - lElementsWithoutMaterial,
            "elements_without_material": lElementsWithoutMaterial,
            "material_counts": lMaterialCounts,
            "material_percentages": lMaterialPercentages,
            "available_materials": list(lMaterialCounts.keys()),
            "top_materials": lSortedMaterials[:10],  # Top 10
            "unique_materials_count": len(lMaterialCounts)
        }
        
    except Exception as e:
        return {"status": "error", "message": f"get_material_statistics failed: {e}"}

def handle_get_group_statistics(aParams: dict) -> dict:
    """Ermittelt Gruppen-Statistiken des gesamten Modells"""
    try:
        import element_controller as ec
        import attribute_controller as ac
        
        # Alle Elemente im Modell
        lAllElements = ec.get_all_element_ids()
        lGroupCounts = {}
        lTotalCount = 0
        lElementsWithoutGroup = 0
        
        # Gruppen aller Elemente zählen
        for lElementId in lAllElements:
            try:
                lGroup = ac.get_element_group(lElementId)
                if lGroup and lGroup.strip():
                    lGroupName = lGroup.strip()
                    if lGroupName not in lGroupCounts:
                        lGroupCounts[lGroupName] = 0
                    lGroupCounts[lGroupName] += 1
                else:
                    lElementsWithoutGroup += 1
                lTotalCount += 1
            except:
                lElementsWithoutGroup += 1
                lTotalCount += 1
        
        # Prozentuale Verteilung berechnen
        lGroupPercentages = {}
        if lTotalCount > 0:
            for lGroupName, lCount in lGroupCounts.items():
                lGroupPercentages[lGroupName] = (lCount / lTotalCount) * 100.0
        
        # Top Gruppen sortieren
        lSortedGroups = sorted(lGroupCounts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "status": "success",
            "total_elements": lTotalCount,
            "elements_with_group": lTotalCount - lElementsWithoutGroup,
            "elements_without_group": lElementsWithoutGroup,
            "group_counts": lGroupCounts,
            "group_percentages": lGroupPercentages,
            "available_groups": list(lGroupCounts.keys()),
            "top_groups": lSortedGroups,
            "unique_groups_count": len(lGroupCounts)
        }
        
    except Exception as e:
        return {"status": "error", "message": f"get_group_statistics failed: {e}"}

def handle_duplicate_elements(aParams: dict) -> dict:
    """Dupliziert Elemente am gleichen Ort"""
    try:
        import element_controller as ec
        
        lElementIds = aParams.get("element_ids", [])
        
        if not lElementIds:
            return {"status": "error", "message": "No element IDs provided"}
        
        lNewElementIds = []
        lFailedElements = []
        
        # Elemente einzeln duplizieren
        for lElementId in lElementIds:
            try:
                # Kopieren mit Null-Vektor (kein Versatz)
                lCopyResult = ec.copy_elements([lElementId], [0.0, 0.0, 0.0])
                if lCopyResult and len(lCopyResult) > 0:
                    lNewElementIds.extend(lCopyResult)
                else:
                    lFailedElements.append(lElementId)
            except Exception as e:
                lFailedElements.append(lElementId)
        
        return {
            "status": "success",
            "message": f"Duplicated {len(lNewElementIds)} elements",
            "original_element_ids": lElementIds,
            "new_element_ids": lNewElementIds,
            "failed_elements": lFailedElements,
            "duplicated_count": len(lNewElementIds),
            "failed_count": len(lFailedElements),
            "total_count": len(lElementIds)
        }
        
    except Exception as e:
        return {"status": "error", "message": f"duplicate_elements failed: {e}"}


def handle_join_elements(aParams: dict) -> dict:
    """Verbindet Elemente miteinander"""
    try:
        import element_controller as ec
        
        lElementIds = aParams.get("element_ids", [])
        
        if len(lElementIds) < 2:
            return {"status": "error", "message": "At least 2 element IDs required for joining"}
        
        # Cadwork API aufrufen
        lJoinedCount = 0
        lFailedJoins = []
        
        # Join-Operation durchführen
        try:
            # Mit dem ersten Element als Basis joinen
            lBaseElement = lElementIds[0]
            lElementsToJoin = lElementIds[1:]
            
            for lElementId in lElementsToJoin:
                try:
                    ec.join_elements([lBaseElement, lElementId])
                    lJoinedCount += 1
                except Exception as e:
                    lFailedJoins.append({"element_id": lElementId, "error": str(e)})
            
        except Exception as e:
            return {"status": "error", "message": f"Join operation failed: {e}"}
        
        return {
            "status": "success",
            "message": f"Successfully joined {lJoinedCount} elements",
            "base_element": lElementIds[0],
            "joined_elements": lElementIds[1:],
            "joined_count": lJoinedCount,
            "failed_joins": lFailedJoins,
            "total_requested": len(lElementIds) - 1
        }
        
    except Exception as e:
        return {"status": "error", "message": f"join_elements failed: {e}"}

def handle_unjoin_elements(aParams: dict) -> dict:
    """Trennt verbundene Elemente"""
    try:
        import element_controller as ec
        
        lElementIds = aParams.get("element_ids", [])
        
        if not lElementIds:
            return {"status": "error", "message": "No element IDs provided"}
        
        # Cadwork API aufrufen
        lUnjoinedCount = 0
        lFailedUnjoins = []
        
        # Unjoin-Operation durchführen
        for lElementId in lElementIds:
            try:
                ec.unjoin_elements([lElementId])
                lUnjoinedCount += 1
            except Exception as e:
                lFailedUnjoins.append({"element_id": lElementId, "error": str(e)})
        
        return {
            "status": "success",
            "message": f"Successfully unjoined {lUnjoinedCount} elements",
            "processed_elements": lElementIds,
            "unjoined_count": lUnjoinedCount,
            "failed_unjoins": lFailedUnjoins,
            "total_requested": len(lElementIds)
        }
        
    except Exception as e:
        return {"status": "error", "message": f"unjoin_elements failed: {e}"}


def handle_cut_corner_lap(aParams: dict) -> dict:
    """Erstellt Eckblatt-Verbindung zwischen Elementen"""
    try:
        import element_controller as ec
        
        lElementIds = aParams.get("element_ids", [])
        lCutParams = aParams.get("cut_params", {})
        
        if len(lElementIds) < 2:
            return {"status": "error", "message": "At least 2 element IDs required for corner lap cut"}
        
        # Cadwork API aufrufen - Eckblatt-Verbindung
        lProcessedElements = []
        lFailedElements = []
        
        try:
            # Corner Lap Cut durchführen
            # Typischerweise wird das erste Element als "Master" verwendet
            lMasterElement = lElementIds[0]
            lTargetElements = lElementIds[1:]
            
            for lTargetElement in lTargetElements:
                try:
                    # Cadwork Cut-Operation ausführen
                    # Die genauen Parameter hängen von der Cadwork API ab
                    if lCutParams:
                        ec.cut_corner_lap_with_params([lMasterElement, lTargetElement], lCutParams)
                    else:
                        ec.cut_corner_lap([lMasterElement, lTargetElement])
                    
                    lProcessedElements.extend([lMasterElement, lTargetElement])
                except Exception as e:
                    lFailedElements.append({"elements": [lMasterElement, lTargetElement], "error": str(e)})
            
        except Exception as e:
            return {"status": "error", "message": f"Corner lap cut operation failed: {e}"}
        
        return {
            "status": "success",
            "message": f"Successfully created corner lap cuts for {len(lProcessedElements)} elements",
            "cut_type": "corner_lap",
            "master_element": lMasterElement,
            "target_elements": lTargetElements,
            "processed_elements": lProcessedElements,
            "failed_elements": lFailedElements,
            "cut_params": lCutParams
        }
        
    except Exception as e:
        return {"status": "error", "message": f"cut_corner_lap failed: {e}"}

def handle_cut_cross_lap(aParams: dict) -> dict:
    """Erstellt Kreuzblatt-Verbindung zwischen Elementen"""
    try:
        import element_controller as ec
        
        lElementIds = aParams.get("element_ids", [])
        lCutParams = aParams.get("cut_params", {})
        
        if len(lElementIds) < 2:
            return {"status": "error", "message": "At least 2 element IDs required for cross lap cut"}
        
        # Cadwork API aufrufen - Kreuzblatt-Verbindung
        lProcessedElements = []
        lFailedElements = []
        
        try:
            # Cross Lap Cut durchführen  
            # Bei Kreuzblatt werden beide Elemente geschnitten
            lElement1 = lElementIds[0]
            lElement2 = lElementIds[1]
            
            # Für mehrere Elemente: paarweise verarbeiten
            for i in range(0, len(lElementIds) - 1, 2):
                try:
                    lElem1 = lElementIds[i]
                    lElem2 = lElementIds[i + 1] if i + 1 < len(lElementIds) else lElementIds[0]
                    
                    # Cadwork Cut-Operation ausführen
                    if lCutParams:
                        ec.cut_cross_lap_with_params([lElem1, lElem2], lCutParams)
                    else:
                        ec.cut_cross_lap([lElem1, lElem2])
                    
                    lProcessedElements.extend([lElem1, lElem2])
                except Exception as e:
                    lFailedElements.append({"elements": [lElem1, lElem2], "error": str(e)})
            
        except Exception as e:
            return {"status": "error", "message": f"Cross lap cut operation failed: {e}"}
        
        return {
            "status": "success",
            "message": f"Successfully created cross lap cuts for {len(lProcessedElements)} elements",
            "cut_type": "cross_lap", 
            "processed_elements": lProcessedElements,
            "failed_elements": lFailedElements,
            "cut_params": lCutParams,
            "pairs_processed": len(lProcessedElements) // 2
        }
        
    except Exception as e:
        return {"status": "error", "message": f"cut_cross_lap failed: {e}"}


def handle_cut_half_lap(aParams: dict) -> dict:
    """Erstellt Halbes Blatt-Verbindung zwischen Elementen"""
    try:
        import element_controller as ec
        
        lElementIds = aParams.get("element_ids", [])
        lCutParams = aParams.get("cut_params", {})
        
        if len(lElementIds) < 2:
            return {"status": "error", "message": "At least 2 element IDs required for half lap cut"}
        
        # Cadwork API aufrufen - Halbes Blatt-Verbindung
        lProcessedElements = []
        lFailedElements = []
        
        try:
            # Half Lap Cut Parameter extrahieren
            lMasterElement = lCutParams.get("master_element", lElementIds[0])
            lCutDepthRatio = lCutParams.get("cut_depth_ratio", 0.5)
            lCutPosition = lCutParams.get("cut_position", "end")
            
            # Half Lap Cut durchführen
            # Das Master-Element wird zur Hälfte geschnitten, andere Elemente vollständig
            for lTargetElement in lElementIds:
                if lTargetElement == lMasterElement:
                    continue
                    
                try:
                    # Cadwork Half Lap Cut-Operation
                    if "cut_depth_ratio" in lCutParams:
                        ec.cut_half_lap_with_ratio([lMasterElement, lTargetElement], 
                                                 lCutDepthRatio, lCutPosition)
                    else:
                        ec.cut_half_lap([lMasterElement, lTargetElement])
                    
                    lProcessedElements.extend([lMasterElement, lTargetElement])
                except Exception as e:
                    lFailedElements.append({
                        "master": lMasterElement, 
                        "target": lTargetElement, 
                        "error": str(e)
                    })
            
        except Exception as e:
            return {"status": "error", "message": f"Half lap cut operation failed: {e}"}
        
        return {
            "status": "success",
            "message": f"Successfully created half lap cuts for {len(lProcessedElements)} elements",
            "cut_type": "half_lap",
            "master_element": lMasterElement,
            "cut_depth_ratio": lCutDepthRatio,
            "cut_position": lCutPosition,
            "processed_elements": lProcessedElements,
            "failed_elements": lFailedElements,
            "cut_params": lCutParams
        }
        
    except Exception as e:
        return {"status": "error", "message": f"cut_half_lap failed: {e}"}

def handle_cut_double_tenon(aParams: dict) -> dict:
    """Erstellt Doppelzapfen-Verbindung zwischen Elementen"""
    try:
        import element_controller as ec
        
        lElementIds = aParams.get("element_ids", [])
        lCutParams = aParams.get("cut_params", {})
        
        if len(lElementIds) != 2:
            return {"status": "error", "message": "Exactly 2 element IDs required for double tenon cut"}
        
        # Cadwork API aufrufen - Doppelzapfen-Verbindung
        try:
            # Double Tenon Parameter extrahieren
            lTenonElement = lCutParams.get("tenon_element", lElementIds[0])
            lMortiseElement = lCutParams.get("mortise_element", lElementIds[1])
            lTenonWidth = lCutParams.get("tenon_width", 40)
            lTenonHeight = lCutParams.get("tenon_height", 80)
            lTenonSpacing = lCutParams.get("tenon_spacing", 60)
            lTenonDepth = lCutParams.get("tenon_depth", 50)
            
            # Validation der Parameter
            if lTenonElement not in lElementIds or lMortiseElement not in lElementIds:
                return {"status": "error", "message": "Tenon and mortise elements must be from provided element IDs"}
            
            # Cadwork Double Tenon Cut-Operation ausführen
            lTenonParams = {
                "width": lTenonWidth,
                "height": lTenonHeight, 
                "spacing": lTenonSpacing,
                "depth": lTenonDepth
            }
            
            if all(param in lCutParams for param in ["tenon_width", "tenon_height", "tenon_spacing"]):
                ec.cut_double_tenon_with_params([lTenonElement, lMortiseElement], lTenonParams)
            else:
                ec.cut_double_tenon([lTenonElement, lMortiseElement])
            
        except Exception as e:
            return {"status": "error", "message": f"Double tenon cut operation failed: {e}"}
        
        return {
            "status": "success",
            "message": f"Successfully created double tenon connection",
            "cut_type": "double_tenon",
            "tenon_element": lTenonElement,
            "mortise_element": lMortiseElement,
            "tenon_specifications": {
                "width": lTenonWidth,
                "height": lTenonHeight,
                "spacing": lTenonSpacing,
                "depth": lTenonDepth
            },
            "processed_elements": lElementIds,
            "cut_params": lCutParams
        }
        
    except Exception as e:
        return {"status": "error", "message": f"cut_double_tenon failed: {e}"}


def handle_cut_scarf_joint(aParams: dict) -> dict:
    """Erstellt Stoßverbindung zwischen Elementen"""
    try:
        import element_controller as ec
        
        lElementIds = aParams.get("element_ids", [])
        lCutParams = aParams.get("cut_params", {})
        
        if len(lElementIds) != 2:
            return {"status": "error", "message": "Exactly 2 element IDs required for scarf joint"}
        
        # Cadwork API aufrufen - Stoßverbindung
        try:
            # Scarf Joint Parameter extrahieren
            lScarfType = lCutParams.get("scarf_type", "plain_scarf")
            lScarfLength = lCutParams.get("scarf_length", 400)
            lScarfAngle = lCutParams.get("scarf_angle", 30)
            lElement1 = lCutParams.get("element_1", lElementIds[0])
            lElement2 = lCutParams.get("element_2", lElementIds[1])
            lOverlapLength = lCutParams.get("overlap_length", 50)
            
            # Validation der Parameter
            if lElement1 not in lElementIds or lElement2 not in lElementIds:
                return {"status": "error", "message": "Element references must be from provided element IDs"}
            
            # Parameter-Validierung
            if lScarfLength <= 0 or lScarfAngle <= 0 or lScarfAngle >= 90:
                return {"status": "error", "message": "Invalid scarf parameters: length > 0, angle between 0-90 degrees"}
            
            # Cadwork Scarf Joint Cut-Operation ausführen
            lScarfParams = {
                "type": lScarfType,
                "length": lScarfLength,
                "angle": lScarfAngle,
                "overlap": lOverlapLength
            }
            
            if "scarf_length" in lCutParams and "scarf_angle" in lCutParams:
                ec.cut_scarf_joint_with_params([lElement1, lElement2], lScarfParams)
            else:
                ec.cut_scarf_joint([lElement1, lElement2])
            
        except Exception as e:
            return {"status": "error", "message": f"Scarf joint cut operation failed: {e}"}
        
        return {
            "status": "success",
            "message": f"Successfully created scarf joint connection",
            "cut_type": "scarf_joint",
            "scarf_specifications": {
                "type": lScarfType,
                "length": lScarfLength,
                "angle": lScarfAngle,
                "overlap_length": lOverlapLength
            },
            "element_1": lElement1,
            "element_2": lElement2,
            "processed_elements": lElementIds,
            "cut_params": lCutParams
        }
        
    except Exception as e:
        return {"status": "error", "message": f"cut_scarf_joint failed: {e}"}

def handle_cut_shoulder(aParams: dict) -> dict:
    """Erstellt Schulterschnitt zwischen Elementen"""
    try:
        import element_controller as ec
        
        lElementIds = aParams.get("element_ids", [])
        lCutParams = aParams.get("cut_params", {})
        
        if len(lElementIds) < 2:
            return {"status": "error", "message": "At least 2 element IDs required for shoulder cut"}
        
        # Cadwork API aufrufen - Schulterschnitt
        lProcessedPairs = []
        lFailedPairs = []
        
        try:
            # Shoulder Cut Parameter extrahieren
            lSupportingElement = lCutParams.get("supporting_element", lElementIds[0])
            lShoulderDepth = lCutParams.get("shoulder_depth", 40)
            lShoulderWidth = lCutParams.get("shoulder_width", 120)
            lShoulderType = lCutParams.get("shoulder_type", "simple_shoulder")
            lContactAngle = lCutParams.get("contact_angle", 90)
            
            # Parameter-Validierung
            if lShoulderDepth <= 0 or lShoulderWidth <= 0:
                return {"status": "error", "message": "Shoulder depth and width must be positive values"}
            
            if lContactAngle <= 0 or lContactAngle > 180:
                return {"status": "error", "message": "Contact angle must be between 0 and 180 degrees"}
            
            # Shoulder Cut für alle Elemente ausführen (außer dem tragenden Element)
            for lSupportedElement in lElementIds:
                if lSupportedElement == lSupportingElement:
                    continue
                    
                try:
                    # Cadwork Shoulder Cut-Operation
                    lShoulderParams = {
                        "depth": lShoulderDepth,
                        "width": lShoulderWidth,
                        "type": lShoulderType,
                        "angle": lContactAngle
                    }
                    
                    if all(param in lCutParams for param in ["shoulder_depth", "shoulder_width"]):
                        ec.cut_shoulder_with_params([lSupportingElement, lSupportedElement], lShoulderParams)
                    else:
                        ec.cut_shoulder([lSupportingElement, lSupportedElement])
                    
                    lProcessedPairs.append({
                        "supporting": lSupportingElement,
                        "supported": lSupportedElement
                    })
                except Exception as e:
                    lFailedPairs.append({
                        "supporting": lSupportingElement,
                        "supported": lSupportedElement,
                        "error": str(e)
                    })
            
        except Exception as e:
            return {"status": "error", "message": f"Shoulder cut operation failed: {e}"}
        
        return {
            "status": "success",
            "message": f"Successfully created shoulder cuts for {len(lProcessedPairs)} element pairs",
            "cut_type": "shoulder",
            "supporting_element": lSupportingElement,
            "shoulder_specifications": {
                "depth": lShoulderDepth,
                "width": lShoulderWidth,
                "type": lShoulderType,
                "contact_angle": lContactAngle
            },
            "processed_pairs": lProcessedPairs,
            "failed_pairs": lFailedPairs,
            "total_pairs": len(lProcessedPairs),
            "cut_params": lCutParams
        }
        
    except Exception as e:
        return {"status": "error", "message": f"cut_shoulder failed: {e}"}


def handle_create_auxiliary_beam_points(aParams: dict) -> dict:
    """Erstellt Hilfs-Balkenelement mit Punkten"""
    try:
        import element_controller as ec
        from bridge.helpers import to_point_3d
        
        # Parameter extrahieren
        lP1 = aParams.get("p1")
        lP2 = aParams.get("p2") 
        lP3 = aParams.get("p3")
        
        if not lP1 or not lP2:
            return {"status": "error", "message": "p1 and p2 points are required"}
        
        # Zu Cadwork Point3D konvertieren
        lCwP1 = to_point_3d(lP1)
        lCwP2 = to_point_3d(lP2)
        lCwP3 = to_point_3d(lP3) if lP3 else None
        
        # Cadwork API aufrufen
        if lCwP3:
            lElementId = ec.create_auxiliary_beam_points(lCwP1, lCwP2, lCwP3)
        else:
            lElementId = ec.create_auxiliary_beam_points(lCwP1, lCwP2)
        
        return {
            "status": "success",
            "element_id": lElementId,
            "element_type": "auxiliary_beam",
            "p1": lP1,
            "p2": lP2,
            "p3": lP3,
            "operation": "create_auxiliary_beam_points"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"create_auxiliary_beam_points failed: {e}"}

def handle_convert_beam_to_panel(aParams: dict) -> dict:
    """Konvertiert Balken zu Platten"""
    try:
        import element_controller as ec
        
        lElementIds = aParams.get("element_ids", [])
        
        if not lElementIds:
            return {"status": "error", "message": "No element IDs provided"}
        
        # Vor Konvertierung - Element-Informationen sammeln  
        lBeforeInfo = []
        for lId in lElementIds:
            try:
                lInfo = ec.get_element_info(lId)
                lBeforeInfo.append({"id": lId, "type": lInfo.get("type", "unknown")})
            except:
                lBeforeInfo.append({"id": lId, "type": "unknown"})
        
        # Cadwork API aufrufen
        lNewElementIds = ec.convert_beam_to_panel(lElementIds)
        
        return {
            "status": "success", 
            "converted_elements": len(lElementIds),
            "original_element_ids": lElementIds,
            "new_element_ids": lNewElementIds if isinstance(lNewElementIds, list) else [lNewElementIds],
            "before_conversion": lBeforeInfo,
            "operation": "convert_beam_to_panel"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"convert_beam_to_panel failed: {e}"}


def handle_convert_panel_to_beam(aParams: dict) -> dict:
    """Konvertiert Platten zu Balken"""
    try:
        import element_controller as ec
        
        lElementIds = aParams.get("element_ids", [])
        
        if not lElementIds:
            return {"status": "error", "message": "No element IDs provided"}
        
        # Vor Konvertierung - Element-Informationen sammeln  
        lBeforeInfo = []
        for lId in lElementIds:
            try:
                lInfo = ec.get_element_info(lId)
                lBeforeInfo.append({"id": lId, "type": lInfo.get("type", "unknown")})
            except:
                lBeforeInfo.append({"id": lId, "type": "unknown"})
        
        # Cadwork API aufrufen
        lNewElementIds = ec.convert_panel_to_beam(lElementIds)
        
        return {
            "status": "success", 
            "converted_elements": len(lElementIds),
            "original_element_ids": lElementIds,
            "new_element_ids": lNewElementIds if isinstance(lNewElementIds, list) else [lNewElementIds],
            "before_conversion": lBeforeInfo,
            "conversion_type": "panel_to_beam",
            "operation": "convert_panel_to_beam"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"convert_panel_to_beam failed: {e}"}

def handle_convert_auxiliary_to_beam(aParams: dict) -> dict:
    """Konvertiert Auxiliary Elemente zu regulären Balken"""
    try:
        import element_controller as ec
        
        lElementIds = aParams.get("element_ids", [])
        
        if not lElementIds:
            return {"status": "error", "message": "No element IDs provided"}
        
        # Vor Konvertierung - Element-Informationen sammeln  
        lBeforeInfo = []
        for lId in lElementIds:
            try:
                lInfo = ec.get_element_info(lId)
                lBeforeInfo.append({"id": lId, "type": lInfo.get("type", "unknown")})
            except:
                lBeforeInfo.append({"id": lId, "type": "auxiliary_unknown"})
        
        # Cadwork API aufrufen
        lNewElementIds = ec.convert_auxiliary_to_beam(lElementIds)
        
        return {
            "status": "success", 
            "converted_elements": len(lElementIds),
            "original_element_ids": lElementIds,
            "new_element_ids": lNewElementIds if isinstance(lNewElementIds, list) else [lNewElementIds],
            "before_conversion": lBeforeInfo,
            "conversion_type": "auxiliary_to_beam",
            "operation": "convert_auxiliary_to_beam"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"convert_auxiliary_to_beam failed: {e}"}


def handle_create_auto_container_from_standard(aParams: dict) -> dict:
    """Erstellt automatischen Container aus Standard-Elementen"""
    try:
        import element_controller as ec
        
        lElementIds = aParams.get("element_ids", [])
        lContainerName = aParams.get("container_name", "")
        
        if not lElementIds:
            return {"status": "error", "message": "No element IDs provided"}
        
        if not lContainerName:
            return {"status": "error", "message": "No container name provided"}
        
        # Vor Container-Erstellung - Element-Informationen sammeln
        lElementInfo = []
        for lId in lElementIds:
            try:
                lInfo = ec.get_element_info(lId)
                lElementInfo.append({
                    "id": lId, 
                    "type": lInfo.get("type", "unknown"),
                    "name": lInfo.get("name", "")
                })
            except:
                lElementInfo.append({"id": lId, "type": "unknown", "name": ""})
        
        # Cadwork API aufrufen
        lContainerId = ec.create_auto_container_from_standard(lElementIds, lContainerName)
        
        return {
            "status": "success",
            "container_id": lContainerId,
            "container_name": lContainerName,
            "element_count": len(lElementIds),
            "contained_elements": lElementIds,
            "element_info": lElementInfo,
            "operation": "create_auto_container_from_standard"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"create_auto_container_from_standard failed: {e}"}

def handle_get_container_content_elements(aParams: dict) -> dict:
    """Ruft Container-Inhalt ab"""
    try:
        import element_controller as ec
        
        lContainerId = aParams.get("container_id")
        
        if lContainerId is None:
            return {"status": "error", "message": "No container ID provided"}
        
        # Cadwork API aufrufen
        lContentElements = ec.get_container_content_elements(lContainerId)
        
        # Element-IDs in Liste konvertieren falls nötig
        if not isinstance(lContentElements, list):
            if lContentElements is None:
                lContentElements = []
            else:
                lContentElements = [lContentElements]
        
        # Zusätzliche Informationen über enthaltene Elemente sammeln
        lElementDetails = []
        for lElementId in lContentElements:
            try:
                lInfo = ec.get_element_info(lElementId)
                lElementDetails.append({
                    "id": lElementId,
                    "type": lInfo.get("type", "unknown"),
                    "name": lInfo.get("name", ""),
                    "material": lInfo.get("material", "")
                })
            except:
                lElementDetails.append({
                    "id": lElementId, 
                    "type": "unknown", 
                    "name": "", 
                    "material": ""
                })
        
        return {
            "status": "success",
            "container_id": lContainerId,
            "element_count": len(lContentElements),
            "content_element_ids": lContentElements,
            "element_details": lElementDetails,
            "operation": "get_container_content_elements"
        }
        
    except Exception as e:
        return {"status": "error", "message": f"get_container_content_elements failed: {e}"}
