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
