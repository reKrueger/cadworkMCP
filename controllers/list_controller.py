"""
List and report controller for generating various element lists and reports
"""
from typing import Dict, Any, List, Optional
from .base_controller import BaseController

class CListController(BaseController):
    """Controller for list and report generation operations"""
    
    def __init__(self) -> None:
        super().__init__("ListController")
    
    async def create_element_list(self, 
                                element_ids: Optional[List[int]] = None,
                                include_properties: bool = True,
                                include_materials: bool = True,
                                include_dimensions: bool = True,
                                group_by: str = "type",
                                sort_by: str = "name",
                                filter_criteria: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a comprehensive element list with optional filtering and grouping"""
        try:
            # Validate element IDs if provided
            validated_ids = None
            if element_ids is not None:
                validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            
            # Validate group_by parameter
            valid_group_options = ["type", "material", "group", "layer", "none"]
            if group_by not in valid_group_options:
                return {"status": "error", "message": f"Invalid group_by option. Must be one of: {valid_group_options}"}
            
            # Validate sort_by parameter
            valid_sort_options = ["name", "type", "material", "volume", "weight", "length", "id"]
            if sort_by not in valid_sort_options:
                return {"status": "error", "message": f"Invalid sort_by option. Must be one of: {valid_sort_options}"}
            
            # Validate filter criteria if provided
            if filter_criteria is not None and not isinstance(filter_criteria, dict):
                return {"status": "error", "message": "filter_criteria must be a dictionary"}
            
            return self.send_command("create_element_list", {
                "element_ids": validated_ids,
                "include_properties": include_properties,
                "include_materials": include_materials,
                "include_dimensions": include_dimensions,
                "group_by": group_by,
                "sort_by": sort_by,
                "filter_criteria": filter_criteria or {}
            })
            
        except ValueError as e:
            return {"status": "error", "message": f"Invalid input: {e}"}
        except Exception as e:
            return {"status": "error", "message": f"create_element_list failed: {e}"}
    
    async def generate_material_list(self,
                                   element_ids: Optional[List[int]] = None,
                                   include_waste: bool = True,
                                   waste_factor: float = 0.1,
                                   group_by_material: bool = True,
                                   include_costs: bool = False,
                                   cost_database: str = "default",
                                   optimization_mode: str = "length") -> Dict[str, Any]:
        """
        Generate comprehensive material list for production and ordering
        
        Args:
            element_ids: Specific elements or all if None
            include_waste: Include waste calculations
            waste_factor: Waste factor (0.1 = 10% waste)
            group_by_material: Group identical materials
            include_costs: Include cost calculations
            cost_database: Cost database to use
            optimization_mode: Optimization method (length, area, volume, count)
        
        Returns:
            dict: Detailed material list with quantities and specifications
        """
        try:
            # Validate element IDs if provided
            validated_ids = None
            if element_ids is not None:
                if not isinstance(element_ids, list):
                    return {"status": "error", "message": "element_ids must be a list if provided"}
                if element_ids:  # Only validate if not empty
                    validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            
            # Validate waste_factor
            if not isinstance(waste_factor, (int, float)) or waste_factor < 0 or waste_factor > 1:
                return {"status": "error", "message": "waste_factor must be between 0 and 1"}
            
            # Validate optimization_mode
            valid_optimization_modes = ["length", "area", "volume", "count", "weight", "cost"]
            if optimization_mode not in valid_optimization_modes:
                return {"status": "error", "message": f"Invalid optimization_mode. Must be one of: {valid_optimization_modes}"}
            
            # Validate cost_database if costs are included
            if include_costs:
                valid_cost_databases = ["default", "regional", "premium", "budget", "custom"]
                if cost_database not in valid_cost_databases:
                    return {"status": "error", "message": f"Invalid cost_database. Must be one of: {valid_cost_databases}"}
            
            return self.send_command("generate_material_list", {
                "element_ids": validated_ids,
                "include_waste": bool(include_waste),
                "waste_factor": float(waste_factor),
                "group_by_material": bool(group_by_material),
                "include_costs": bool(include_costs),
                "cost_database": cost_database,
                "optimization_mode": optimization_mode
            })
            
        except ValueError as e:
            return {"status": "error", "message": f"Invalid input: {e}"}
        except Exception as e:
            return {"status": "error", "message": f"generate_material_list failed: {e}"}
