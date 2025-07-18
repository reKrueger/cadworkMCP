"""
Optimization controller for material and production optimization
"""
from typing import Dict, Any, List, Optional
from .base_controller import BaseController

class COptimizationController(BaseController):
    """Controller for optimization operations"""
    
    def __init__(self) -> None:
        super().__init__("OptimizationController")
    
    async def optimize_cutting_list(self,
                                  element_ids: Optional[List[int]] = None,
                                  stock_lengths: Optional[List[float]] = None,
                                  optimization_algorithm: str = "bin_packing",
                                  kerf_width: float = 3.0,
                                  min_offcut_length: float = 100.0,
                                  max_waste_percentage: float = 5.0,
                                  material_groups: Optional[Dict[str, List[str]]] = None,
                                  priority_mode: str = "waste_minimization") -> Dict[str, Any]:
        """Optimize cutting lists for minimal material waste and efficient production"""
        try:
            # Validate element IDs
            validated_ids = None
            if element_ids is not None:
                if not isinstance(element_ids, list):
                    return {"status": "error", "message": "element_ids must be a list"}
                if element_ids:
                    validated_ids = [self.validate_element_id(eid) for eid in element_ids]
            
            # Set default stock lengths
            if stock_lengths is None:
                stock_lengths = [2000.0, 2500.0, 3000.0, 4000.0, 5000.0, 6000.0]
            
            # Validate parameters
            valid_algorithms = ["bin_packing", "genetic", "greedy", "advanced", "first_fit", "best_fit"]
            if optimization_algorithm not in valid_algorithms:
                return {"status": "error", "message": f"Invalid algorithm. Must be one of: {valid_algorithms}"}
            
            if kerf_width < 0 or min_offcut_length < 0:
                return {"status": "error", "message": "kerf_width and min_offcut_length must be non-negative"}
            
            if max_waste_percentage < 0 or max_waste_percentage > 100:
                return {"status": "error", "message": "max_waste_percentage must be between 0 and 100"}
            
            valid_modes = ["waste_minimization", "cost_reduction", "speed", "quality", "balanced"]
            if priority_mode not in valid_modes:
                return {"status": "error", "message": f"Invalid priority_mode. Must be one of: {valid_modes}"}
            
            return self.send_command("optimize_cutting_list", {
                "element_ids": validated_ids,
                "stock_lengths": stock_lengths,
                "optimization_algorithm": optimization_algorithm,
                "kerf_width": float(kerf_width),
                "min_offcut_length": float(min_offcut_length),
                "max_waste_percentage": float(max_waste_percentage),
                "material_groups": material_groups or {},
                "priority_mode": priority_mode
            })            
        except ValueError as e:
            return {"status": "error", "message": f"Invalid input: {e}"}
        except Exception as e:
            return {"status": "error", "message": f"optimize_cutting_list failed: {e}"}
