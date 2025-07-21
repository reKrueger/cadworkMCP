"""
Container controller for container operations
"""
from typing import Dict, Any, List, Optional
from .base_controller import BaseController

class ContainerController(BaseController):
    """Controller for container operations"""
    
    def __init__(self) -> None:
        super().__init__("ContainerController")
    
    async def create_auto_container_from_standard(self, element_ids: List[int], container_name: str) -> Dict[str, Any]:
        """Creates an automatic container from standard elements"""
        self.validate_required_args({"element_ids": element_ids, "container_name": container_name}, 
                                   ["element_ids", "container_name"])
        
        if not element_ids:
            raise ValueError("Element IDs list cannot be empty")
        
        # Validate all element IDs
        validated_ids = [self.validate_element_id(id_val) for id_val in element_ids]
        
        if not container_name.strip():
            raise ValueError("Container name cannot be empty")
        
        args: Dict[str, Any] = {
            "element_ids": validated_ids,
            "container_name": container_name.strip()
        }
        
        return self.send_command("create_auto_container_from_standard", args)
    
    async def get_container_content_elements(self, container_id: int) -> Dict[str, Any]:
        """Retrieves all elements contained within a specific container"""
        validated_id = self.validate_element_id(container_id)
        
        args: Dict[str, Any] = {
            "container_id": validated_id
        }
        
        return self.send_command("get_container_content_elements", args)
