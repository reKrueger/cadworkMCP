"""
List and report handlers
"""
from typing import Dict, Any
from ..helpers import validate_element_ids

def handle_create_element_list(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle create element list command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec
        import attribute_controller as ac
        import geometry_controller as gc

        # Get optional element IDs
        element_ids_raw = args.get("element_ids")
        if element_ids_raw is not None:
            element_ids = validate_element_ids(element_ids_raw)
        else:
            element_ids = ec.get_all_identifiable_element_ids()
        
        if not element_ids:
            return {
                "status": "ok",
                "message": "No elements found",
                "element_list": [],
                "total_count": 0
            }
        
        # Get configuration options
        include_properties = args.get("include_properties", True)
        include_materials = args.get("include_materials", True)
        include_dimensions = args.get("include_dimensions", True)
        group_by = args.get("group_by", "type")
        sort_by = args.get("sort_by", "name")
        
        # Collect element data
        element_list = []
        for element_id in element_ids:
            element_data = {"id": element_id}
            
            # Basic properties
            if include_properties:
                try:
                    element_data["type"] = gc.get_element_type(element_id)
                    names = ac.get_name([element_id])
                    element_data["name"] = names[0] if names else f"Element_{element_id}"
                except:
                    element_data["type"] = "unknown"
                    element_data["name"] = f"Element_{element_id}"            
            # Material information
            if include_materials:
                try:
                    materials = ac.get_material([element_id])
                    element_data["material"] = materials[0] if materials else "Unknown"
                except:
                    element_data["material"] = "Unknown"
            
            # Dimension information
            if include_dimensions:
                try:
                    element_data["width"] = gc.get_width(element_id)
                    element_data["height"] = gc.get_height(element_id)
                    element_data["length"] = gc.get_length(element_id)
                    element_data["volume"] = gc.get_volume(element_id)
                except:
                    pass
            
            element_list.append(element_data)
        
        # Simple sorting by specified criteria
        if sort_by in ["name", "type", "material"]:
            element_list.sort(key=lambda x: x.get(sort_by, ""))
        elif sort_by == "id":
            element_list.sort(key=lambda x: x["id"])
        
        return {
            "status": "ok",
            "element_list": element_list,
            "total_count": len(element_list),
            "group_by": group_by,
            "sort_by": sort_by,
            "options": {
                "include_properties": include_properties,
                "include_materials": include_materials,
                "include_dimensions": include_dimensions
            }
        }
    
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"create_element_list failed: {e}"}

def handle_generate_material_list(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle generate material list command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec
        import attribute_controller as ac
        import geometry_controller as gc

        # Get optional element IDs
        element_ids_raw = args.get("element_ids")
        if element_ids_raw is not None:
            element_ids = validate_element_ids(element_ids_raw)
        else:
            # Get all elements if none specified
            element_ids = ec.get_all_identifiable_element_ids()
        
        if not element_ids:
            return {
                "status": "ok",
                "message": "No elements found",
                "material_list": [],
                "total_materials": 0
            }
        
        # Get configuration options
        include_waste = args.get("include_waste", True)
        waste_factor = args.get("waste_factor", 0.1)
        group_by_material = args.get("group_by_material", True)
        include_costs = args.get("include_costs", False)
        cost_database = args.get("cost_database", "default")
        optimization_mode = args.get("optimization_mode", "length")
        
        # Validate parameters
        if not isinstance(waste_factor, (int, float)) or waste_factor < 0 or waste_factor > 1:
            raise ValueError("waste_factor must be between 0 and 1")
        
        valid_optimization_modes = ["length", "area", "volume", "count", "weight", "cost"]
        if optimization_mode not in valid_optimization_modes:
            raise ValueError(f"Invalid optimization_mode. Must be one of: {valid_optimization_modes}")
        
        # Collect material data from elements
        material_data = {}
        
        for element_id in element_ids:
            try:
                # Get material information
                materials = ac.get_material([element_id])
                material_name = materials[0] if materials else "Unknown"
                
                # Get element dimensions
                length = gc.get_length(element_id)
                width = gc.get_width(element_id)
                height = gc.get_height(element_id)
                volume = gc.get_volume(element_id)
                
                # Get element type for categorization
                element_type = gc.get_element_type(element_id)
                
                # Create material key
                if group_by_material:
                    material_key = f"{material_name}_{width}x{height}"
                else:
                    material_key = f"{material_name}_{element_id}"
                
                # Initialize material entry if not exists
                if material_key not in material_data:
                    material_data[material_key] = {
                        "material_name": material_name,
                        "dimensions": f"{width}x{height}",
                        "width": width,
                        "height": height,
                        "element_type": element_type,
                        "count": 0,
                        "total_length": 0.0,
                        "total_volume": 0.0,
                        "element_ids": []
                    }
                
                # Accumulate data
                material_data[material_key]["count"] += 1
                material_data[material_key]["total_length"] += length
                material_data[material_key]["total_volume"] += volume
                material_data[material_key]["element_ids"].append(element_id)
                
            except Exception as e:
                # Skip problematic elements but continue processing
                continue
        
        # Apply waste factor if requested
        if include_waste:
            for material_key in material_data:
                material_data[material_key]["total_length_with_waste"] = material_data[material_key]["total_length"] * (1 + waste_factor)
                material_data[material_key]["total_volume_with_waste"] = material_data[material_key]["total_volume"] * (1 + waste_factor)
                material_data[material_key]["waste_factor"] = waste_factor
        
        # Convert to list and sort based on optimization mode
        material_list = list(material_data.values())
        
        if optimization_mode == "length":
            material_list.sort(key=lambda x: x["total_length"], reverse=True)
        elif optimization_mode == "volume":
            material_list.sort(key=lambda x: x["total_volume"], reverse=True)
        elif optimization_mode == "count":
            material_list.sort(key=lambda x: x["count"], reverse=True)
        else:
            material_list.sort(key=lambda x: x["material_name"])
        
        # Calculate totals
        total_length = sum(item["total_length"] for item in material_list)
        total_volume = sum(item["total_volume"] for item in material_list)
        total_count = sum(item["count"] for item in material_list)
        
        if include_waste:
            total_length_with_waste = total_length * (1 + waste_factor)
            total_volume_with_waste = total_volume * (1 + waste_factor)
        
        result = {
            "status": "ok",
            "material_list": material_list,
            "summary": {
                "total_materials": len(material_list),
                "total_elements": total_count,
                "total_length": total_length,
                "total_volume": total_volume,
                "optimization_mode": optimization_mode,
                "grouped_by_material": group_by_material
            },
            "options": {
                "include_waste": include_waste,
                "waste_factor": waste_factor,
                "include_costs": include_costs,
                "cost_database": cost_database
            }
        }
        
        if include_waste:
            result["summary"]["total_length_with_waste"] = total_length_with_waste
            result["summary"]["total_volume_with_waste"] = total_volume_with_waste
            result["summary"]["waste_volume"] = total_volume_with_waste - total_volume
        
        return result
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"generate_material_list failed: {e}"}
