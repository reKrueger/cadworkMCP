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
