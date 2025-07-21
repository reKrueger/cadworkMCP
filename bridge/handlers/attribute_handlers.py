"""
Attribute operation handlers
"""
from typing import Dict, Any, List
from ..helpers import validate_element_ids

def handle_get_standard_attributes(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get standard attributes command"""
    try:
        # Import here to avoid import-time errors
        import attribute_controller as ac

        element_ids = validate_element_ids(args.get("element_ids", []))
        
        if not element_ids:
            return {"status": "ok", "attributes_by_id": {}}
        
        results = {}
        
        # Define standard attributes to fetch
        standard_attrs = {
            "name": ac.get_name,
            "group": ac.get_group,
            "subgroup": ac.get_subgroup,
            "comment": ac.get_comment
        }
        
        for eid in element_ids:
            elem_attrs = {}
            
            # Get standard attributes
            for attr_key, getter_func in standard_attrs.items():
                try:
                    value = getter_func(eid)
                    elem_attrs[attr_key] = value
                except Exception:
                    elem_attrs[attr_key] = None
            
            # Get material
            try:
                material_name = ac.get_element_material_name(eid)
                elem_attrs['material'] = material_name if material_name else None
            except Exception:
                elem_attrs['material'] = None
            
            results[eid] = elem_attrs
        
        return {"status": "ok", "attributes_by_id": results}
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_get_user_attributes(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle get user attributes command"""
    try:
        # Import here to avoid import-time errors
        import attribute_controller as ac

        element_ids = validate_element_ids(args.get("element_ids", []))
        attr_numbers = args.get("attribute_numbers", [])
        
        if not isinstance(attr_numbers, list):
            raise ValueError("attribute_numbers must be a list")
        
        # Validate attribute numbers
        attr_numbers = [int(num) for num in attr_numbers]
        if not all(num > 0 for num in attr_numbers):
            raise ValueError("Attribute numbers must be positive integers")
        
        if not element_ids or not attr_numbers:
            return {"status": "ok", "user_attributes_by_id": {}}
        
        results = {}
        
        for eid in element_ids:
            user_attrs = {}
            for num in attr_numbers:
                try:
                    value = ac.get_user_attribute(eid, num)
                    user_attrs[num] = value
                except Exception:
                    user_attrs[num] = None
            
            results[eid] = user_attrs
        
        return {"status": "ok", "user_attributes_by_id": results}
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_list_defined_user_attributes(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle list defined user attributes command"""
    try:
        # Import here to avoid import-time errors
        import attribute_controller as ac

        defined_attributes = {}
        
        # Check attributes 1-100
        for i in range(1, 101):
            try:
                name = ac.get_user_attribute_name(i)
                if name:
                    defined_attributes[i] = name
            except AttributeError:
                return {
                    "status": "error", 
                    "message": "Function get_user_attribute_name not available"
                }
            except Exception:
                continue  # Skip this attribute number
        
        return {"status": "ok", "defined_attributes": defined_attributes}
        
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

# --- ATTRIBUTE SETTERS ---

def handle_set_name(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle set name command"""
    try:
        # Import here to avoid import-time errors
        import attribute_controller as ac

        element_ids = validate_element_ids(args.get("element_ids", []))
        name = args.get("name", "")
        
        if not isinstance(name, str):
            raise ValueError("name must be a string")
        
        if not element_ids:
            return {"status": "error", "message": "No element IDs provided"}
        
        # Set name for all elements
        for eid in element_ids:
            try:
                ac.set_name(eid, name)
            except Exception as e:
                return {"status": "error", "message": f"Failed to set name for element {eid}: {e}"}
        
        return {
            "status": "ok", 
            "message": f"Name '{name}' set for {len(element_ids)} elements",
            "element_ids": element_ids
        }
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}

def handle_set_material(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle set material command"""
    try:
        # Import here to avoid import-time errors
        import attribute_controller as ac

        element_ids = validate_element_ids(args.get("element_ids", []))
        material = args.get("material", "")
        
        if not isinstance(material, str):
            raise ValueError("material must be a string")
        
        if not element_ids:
            return {"status": "error", "message": "No element IDs provided"}
        
        # Set material for all elements
        for eid in element_ids:
            try:
                # Try different possible function names for setting material
                if hasattr(ac, 'set_material_name'):
                    ac.set_material_name(eid, material)
                elif hasattr(ac, 'set_element_material'):
                    ac.set_element_material(eid, material)
                elif hasattr(ac, 'set_material'):
                    ac.set_material(eid, material)
                else:
                    # Fallback: try to find any material-related function
                    material_funcs = [attr for attr in dir(ac) if 'material' in attr.lower() and 'set' in attr.lower()]
                    if material_funcs:
                        func = getattr(ac, material_funcs[0])
                        func(eid, material)
                    else:
                        return {"status": "error", "message": f"No material setting function found in attribute_controller"}
            except Exception as e:
                return {"status": "error", "message": f"Failed to set material for element {eid}: {e}"}
        
        return {
            "status": "ok", 
            "message": f"Material '{material}' set for {len(element_ids)} elements",
            "element_ids": element_ids
        }
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"API error: {e}"}


def handle_set_group(aParams: dict) -> dict:
    """Setzt Gruppe für Elemente"""
    try:
        import attribute_controller as ac
        
        lElementIds = aParams.get("element_ids", [])
        lGroup = aParams.get("group")
        
        if not lElementIds:
            return {"status": "error", "message": "No element IDs provided"}
        
        if lGroup is None:
            return {"status": "error", "message": "No group name provided"}
        
        # Cadwork API aufrufen - alle IDs auf einmal übergeben
        ac.set_group(lElementIds, lGroup)
        
        return {
            "status": "success",
            "message": f"Group '{lGroup}' set for {len(lElementIds)} elements",
            "element_ids": lElementIds,
            "group": lGroup
        }
        
    except Exception as e:
        return {"status": "error", "message": f"set_group failed: {e}"}

def handle_set_comment(aParams: dict) -> dict:
    """Setzt Kommentar für Elemente"""
    try:
        import attribute_controller as ac
        
        lElementIds = aParams.get("element_ids", [])
        lComment = aParams.get("comment")
        
        if not lElementIds:
            return {"status": "error", "message": "No element IDs provided"}
        
        if lComment is None:
            return {"status": "error", "message": "No comment text provided"}
        
        # Cadwork API aufrufen - alle IDs auf einmal übergeben
        ac.set_comment(lElementIds, lComment)
        
        return {
            "status": "success",
            "message": f"Comment '{lComment}' set for {len(lElementIds)} elements",
            "element_ids": lElementIds,
            "comment": lComment
        }
        
    except Exception as e:
        return {"status": "error", "message": f"set_comment failed: {e}"}

def handle_set_subgroup(aParams: dict) -> dict:
    """Setzt Untergruppe für Elemente"""
    try:
        import attribute_controller as ac
        
        lElementIds = aParams.get("element_ids", [])
        lSubgroup = aParams.get("subgroup")
        
        if not lElementIds:
            return {"status": "error", "message": "No element IDs provided"}
        
        if lSubgroup is None:
            return {"status": "error", "message": "No subgroup name provided"}
        
        # Cadwork API aufrufen - alle IDs auf einmal übergeben
        ac.set_subgroup(lElementIds, lSubgroup)
        
        return {
            "status": "success",
            "message": f"Subgroup '{lSubgroup}' set for {len(lElementIds)} elements",
            "element_ids": lElementIds,
            "subgroup": lSubgroup
        }
        
    except Exception as e:
        return {"status": "error", "message": f"set_subgroup failed: {e}"}
