"""
Optimization handlers
"""
from typing import Dict, Any
from ..helpers import validate_element_ids

def handle_optimize_cutting_list(args: Dict[str, Any]) -> Dict[str, Any]:
    """Handle optimize cutting list command"""
    try:
        # Import here to avoid import-time errors
        import element_controller as ec
        import attribute_controller as ac
        import geometry_controller as gc

        # Get element IDs
        element_ids_raw = args.get("element_ids")
        if element_ids_raw is not None:
            element_ids = validate_element_ids(element_ids_raw)
        else:
            element_ids = ec.get_all_identifiable_element_ids()
        
        if not element_ids:
            return {
                "status": "ok",
                "message": "No elements found for optimization",
                "optimized_cutting_list": [],
                "waste_analysis": {"total_waste": 0}
            }
        
        # Get configuration options
        stock_lengths = args.get("stock_lengths", [2000.0, 2500.0, 3000.0, 4000.0, 5000.0, 6000.0])
        optimization_algorithm = args.get("optimization_algorithm", "bin_packing")
        kerf_width = args.get("kerf_width", 3.0)
        min_offcut_length = args.get("min_offcut_length", 100.0)
        max_waste_percentage = args.get("max_waste_percentage", 5.0)
        priority_mode = args.get("priority_mode", "waste_minimization")
        
        # Validate parameters
        valid_algorithms = ["bin_packing", "genetic", "greedy", "advanced", "first_fit", "best_fit"]
        if optimization_algorithm not in valid_algorithms:
            raise ValueError(f"Invalid algorithm. Must be one of: {valid_algorithms}")
        
        if kerf_width < 0 or min_offcut_length < 0:
            raise ValueError("kerf_width and min_offcut_length must be non-negative")
        
        if max_waste_percentage < 0 or max_waste_percentage > 100:
            raise ValueError("max_waste_percentage must be between 0 and 100")
        
        # Collect element data for cutting optimization
        cutting_requirements = []
        for element_id in element_ids:
            try:
                length = gc.get_length(element_id)
                width = gc.get_width(element_id)
                height = gc.get_height(element_id)
                materials = ac.get_material([element_id])
                material_name = materials[0] if materials else "Unknown"
                
                cutting_requirements.append({
                    "element_id": element_id,
                    "required_length": length,
                    "width": width,
                    "height": height,
                    "material": material_name,
                    "cross_section": f"{width}x{height}"
                })
            except Exception:
                continue        
        # Group requirements by cross-section and material
        grouped_requirements = {}
        for req in cutting_requirements:
            key = f"{req['material']}_{req['cross_section']}"
            if key not in grouped_requirements:
                grouped_requirements[key] = {
                    "material": req['material'],
                    "cross_section": req['cross_section'],
                    "elements": []
                }
            grouped_requirements[key]["elements"].append(req)
        
        # Perform optimization for each group
        optimized_cutting_list = []
        total_waste_length = 0.0
        total_stock_used = 0.0
        
        for group_key, group_data in grouped_requirements.items():
            elements = group_data["elements"]
            required_lengths = [elem["required_length"] for elem in elements]
            
            # Simple bin packing algorithm (First Fit Decreasing)
            required_lengths.sort(reverse=True)  # Sort by length descending
            stock_pieces = []
            
            for req_length in required_lengths:
                placed = False
                
                # Try to fit in existing stock pieces
                for stock_piece in stock_pieces:
                    available_space = stock_piece["remaining_length"]
                    if available_space >= req_length + kerf_width:
                        # Add cut to this stock piece
                        stock_piece["cuts"].append({
                            "element_id": next(e["element_id"] for e in elements if e["required_length"] == req_length),
                            "length": req_length,
                            "start_position": stock_piece["stock_length"] - available_space,
                            "end_position": stock_piece["stock_length"] - available_space + req_length
                        })
                        stock_piece["remaining_length"] -= (req_length + kerf_width)
                        placed = True
                        break
                
                # If not placed, create new stock piece
                if not placed:
                    # Find best fitting stock length
                    best_stock_length = min([sl for sl in stock_lengths if sl >= req_length], default=max(stock_lengths))
                    
                    new_stock_piece = {
                        "stock_id": len(stock_pieces) + 1,
                        "stock_length": best_stock_length,
                        "remaining_length": best_stock_length - req_length - kerf_width,
                        "cuts": [{
                            "element_id": next(e["element_id"] for e in elements if e["required_length"] == req_length),
                            "length": req_length,
                            "start_position": 0,
                            "end_position": req_length
                        }]
                    }
                    stock_pieces.append(new_stock_piece)
            
            # Calculate waste for this group
            group_waste = sum(piece["remaining_length"] for piece in stock_pieces)
            group_stock_used = sum(piece["stock_length"] for piece in stock_pieces)
            
            total_waste_length += group_waste
            total_stock_used += group_stock_used
            
            optimized_cutting_list.append({
                "material": group_data["material"],
                "cross_section": group_data["cross_section"],
                "stock_pieces": stock_pieces,
                "total_stock_pieces": len(stock_pieces),
                "total_waste_length": group_waste,
                "total_stock_used": group_stock_used,
                "waste_percentage": (group_waste / group_stock_used * 100) if group_stock_used > 0 else 0
            })
        
        # Calculate overall statistics
        overall_waste_percentage = (total_waste_length / total_stock_used * 100) if total_stock_used > 0 else 0
        
        return {
            "status": "ok",
            "optimization_algorithm": optimization_algorithm,
            "priority_mode": priority_mode,
            "total_elements_processed": len(cutting_requirements),
            "total_material_groups": len(grouped_requirements),
            "optimized_cutting_list": optimized_cutting_list,
            "waste_analysis": {
                "total_waste_length": total_waste_length,
                "total_stock_used": total_stock_used,
                "overall_waste_percentage": overall_waste_percentage,
                "meets_waste_target": overall_waste_percentage <= max_waste_percentage
            },
            "optimization_parameters": {
                "stock_lengths": stock_lengths,
                "kerf_width": kerf_width,
                "min_offcut_length": min_offcut_length,
                "max_waste_percentage": max_waste_percentage
            },
            "message": f"Optimization completed: {overall_waste_percentage:.1f}% waste across {len(optimized_cutting_list)} material groups"
        }
        
    except ValueError as e:
        return {"status": "error", "message": f"Invalid input: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"optimize_cutting_list failed: {e}"}
