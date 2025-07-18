"""
Mock Cadwork Connection
======================

Mock implementation for testing without real Cadwork connection.
"""

from typing import Dict, Any
import random


class MockCadworkConnection:
    """Mock connection that simulates Cadwork responses"""
    
    def __init__(self):
        self.next_element_id = 10000
        self.elements = {}  # Track created elements
        
    def send_command(self, operation: str, args: Dict[str, Any] = None) -> Dict[str, Any]:
        """Simulate command processing"""
        args = args or {}
        
        # Connection commands
        if operation == "ping":
            return {"status": "ok", "message": "Mock bridge responding"}
        
        # Element creation commands
        elif operation == "create_beam":
            element_id = self._create_mock_element("beam", args)
            return {"status": "ok", "element_id": element_id}
        
        elif operation == "create_panel":
            element_id = self._create_mock_element("panel", args)
            return {"status": "ok", "element_id": element_id}
        
        elif operation == "create_circular_beam_points":
            element_id = self._create_mock_element("circular_beam", args)
            return {"status": "ok", "element_id": element_id}
        
        elif operation == "create_square_beam_points":
            element_id = self._create_mock_element("square_beam", args)
            return {"status": "ok", "element_id": element_id}
        
        # Element query commands
        elif operation == "get_all_element_ids":
            element_ids = list(self.elements.keys())
            # Add some default elements if none exist
            if not element_ids:
                element_ids = [1001, 1002, 1003]
            return {"status": "ok", "element_ids": element_ids}
        
        elif operation == "get_element_info":
            element_id = args.get("element_id")
            if element_id in self.elements:
                element = self.elements[element_id]
                return {
                    "status": "ok",
                    "element_type": element["type"],
                    "width": element.get("width", 200),
                    "height": element.get("height", 300),
                    "length": element.get("length", 1000),
                    "material": "Wood"
                }
            return {"status": "error", "message": f"Element {element_id} not found"}
        
        # Element dimension commands
        elif operation == "get_element_width":
            element_id = args.get("element_id")
            return {"status": "ok", "width": self._get_element_dimension(element_id, "width", 200)}
        
        elif operation == "get_element_height":
            element_id = args.get("element_id")
            return {"status": "ok", "height": self._get_element_dimension(element_id, "height", 300)}
        
        elif operation == "get_element_length":
            element_id = args.get("element_id")
            return {"status": "ok", "length": self._get_element_dimension(element_id, "length", 1000)}
        
        elif operation == "get_element_volume":
            element_id = args.get("element_id")
            volume = 200 * 300 * 1000  # width * height * length in mm³
            return {"status": "ok", "volume": volume}
        
        elif operation == "get_element_weight":
            element_id = args.get("element_id")
            weight = 50.5  # kg
            return {"status": "ok", "weight": weight}
        
        # Element point commands
        elif operation == "get_element_p1":
            return {"status": "ok", "point": [0, 0, 0]}
        
        elif operation == "get_element_p2":
            return {"status": "ok", "point": [1000, 0, 0]}
        
        elif operation == "get_bounding_box":
            return {"status": "ok", "bounding_box": [0, 0, 0, 1000, 200, 300]}
        
        elif operation == "get_center_of_gravity":
            return {"status": "ok", "center_of_gravity": [500, 100, 150]}
        
        # Element manipulation commands
        elif operation == "delete_elements":
            element_ids = args.get("element_ids", [])
            for eid in element_ids:
                if eid in self.elements:
                    del self.elements[eid]
            return {"status": "ok", "deleted_count": len(element_ids)}
        
        elif operation == "copy_elements":
            element_ids = args.get("element_ids", [])
            new_ids = []
            for _ in element_ids:
                new_id = self._get_next_element_id()
                new_ids.append(new_id)
                self.elements[new_id] = {"type": "copied_element"}
            return {"status": "ok", "element_ids": new_ids}
        
        elif operation == "move_element":
            return {"status": "ok", "moved_count": len(args.get("element_ids", []))}
        
        elif operation == "scale_elements":
            return {"status": "ok", "scaled_count": len(args.get("element_ids", []))}
        
        # Visualization commands
        elif operation == "show_all_elements":
            return {"status": "success", "visible_count": len(self.elements)}
        
        elif operation == "hide_all_elements":
            return {"status": "success", "hidden_count": len(self.elements)}
        
        elif operation == "get_visible_element_count":
            return {"status": "ok", "visible_count": len(self.elements), "total_count": len(self.elements)}
        
        elif operation == "set_color":
            element_ids = args.get("element_ids", [])
            return {"status": "ok", "updated_count": len(element_ids)}
        
        elif operation == "set_visibility":
            element_ids = args.get("element_ids", [])
            return {"status": "ok", "updated_count": len(element_ids)}
        
        elif operation == "set_transparency":
            element_ids = args.get("element_ids", [])
            return {"status": "ok", "updated_count": len(element_ids)}
        
        elif operation == "get_color":
            return {"status": "ok", "color_id": 1, "color_name": "Red"}
        
        elif operation == "refresh_display":
            return {"status": "ok", "message": "Display refreshed"}
        
        # Default fallback
        else:
            return {"status": "error", "message": f"Mock operation '{operation}' not implemented"}
    
    def _create_mock_element(self, element_type: str, args: Dict[str, Any]) -> int:
        """Create a mock element and return its ID"""
        element_id = self._get_next_element_id()
        
        # Store element data
        element_data = {
            "type": element_type,
            "width": args.get("width", 200),
            "height": args.get("height", 300),
            "thickness": args.get("thickness", 20),
            "diameter": args.get("diameter", 300),
            "p1": args.get("p1", [0, 0, 0]),
            "p2": args.get("p2", [1000, 0, 0]),
            "p3": args.get("p3")
        }
        
        self.elements[element_id] = element_data
        return element_id
    
    def _get_next_element_id(self) -> int:
        """Get next available element ID"""
        self.next_element_id += 1
        return self.next_element_id
    
    def _get_element_dimension(self, element_id: int, dimension: str, default: float) -> float:
        """Get element dimension or return default"""
        if element_id in self.elements:
            return self.elements[element_id].get(dimension, default)
        return default
