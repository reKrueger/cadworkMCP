# cadwork_axis_config.py
"""
Cadwork Axis Configuration and Helper Functions
CRITICAL: Always follow these axis directions for correct beam creation!
"""

CADWORK_AXIS_INFO = """
CADWORK AXIS DIRECTIONS - CRITICAL FOR CORRECT BEAM CREATION:

For create_beam(p1, p2, width, height):
- p1, p2: Define the LONGITUDINAL AXIS of the beam
- width: Cross-section in X-direction  
- height: Cross-section in Y-direction

VERTICAL BEAMS (most important rule):
- p1 = [x, y, z_start] 
- p2 = [x, y, z_end]    <- Z-direction for longitudinal axis!
- width = 80 (X-direction)
- height = 80 (Y-direction)

HORIZONTAL BEAMS X-DIRECTION:
- p1 = [x_start, y, z]
- p2 = [x_end, y, z]    <- X-direction for longitudinal axis
- width = 80, height = 80

HORIZONTAL BEAMS Y-DIRECTION:
- p1 = [x, y_start, z]
- p2 = [x, y_end, z]    <- Y-direction for longitudinal axis
- width = 80, height = 80
"""

# Standard dimensions
STANDARD_BEAM_DIMENSIONS = {
    "80x80": {"width": 80, "height": 80},
    "100x100": {"width": 100, "height": 100},
    "120x120": {"width": 120, "height": 120},
    "160x160": {"width": 160, "height": 160},
    "200x200": {"width": 200, "height": 200},
}

# Standard materials
STANDARD_MATERIALS = {
    "SPRUCE": "Fichte",
    "PINE": "Kiefer", 
    "OAK": "Eiche",
    "BEECH": "Buche",
    "LARCH": "Lärche",
}

class CadworkAxisHelper:
    """Helper class for correct axis orientation in Cadwork beam creation"""
    
    @staticmethod
    def create_vertical_beam_points(x, y, z_start, z_end):
        """
        Creates points for vertical beam with correct Z-axis orientation
        
        Args:
            x (float): X coordinate
            y (float): Y coordinate  
            z_start (float): Start Z coordinate
            z_end (float): End Z coordinate
            
        Returns:
            tuple: (p1, p2) points for vertical beam
        """
        return [x, y, z_start], [x, y, z_end]
    
    @staticmethod
    def create_horizontal_beam_x_points(x_start, x_end, y, z):
        """
        Creates points for horizontal beam in X-direction
        
        Args:
            x_start (float): Start X coordinate
            x_end (float): End X coordinate
            y (float): Y coordinate
            z (float): Z coordinate
            
        Returns:
            tuple: (p1, p2) points for horizontal beam
        """
        return [x_start, y, z], [x_end, y, z]
    
    @staticmethod
    def create_horizontal_beam_y_points(x, y_start, y_end, z):
        """
        Creates points for horizontal beam in Y-direction
        
        Args:
            x (float): X coordinate
            y_start (float): Start Y coordinate
            y_end (float): End Y coordinate
            z (float): Z coordinate
            
        Returns:
            tuple: (p1, p2) points for horizontal beam
        """
        return [x, y_start, z], [x, y_end, z]
    
    @staticmethod
    def get_beam_dimensions(size_key="80x80"):
        """Get standard beam dimensions"""
        return STANDARD_BEAM_DIMENSIONS.get(size_key, {"width": 80, "height": 80})
    
    @staticmethod
    def validate_beam_orientation(p1, p2, expected_axis='Z'):
        """
        Validate if beam orientation matches expected axis
        
        Args:
            p1 (list): Start point [x, y, z]
            p2 (list): End point [x, y, z]
            expected_axis (str): Expected axis ('X', 'Y', or 'Z')
            
        Returns:
            bool: True if orientation is correct
        """
        if expected_axis == 'Z':
            return p1[0] == p2[0] and p1[1] == p2[1] and p1[2] != p2[2]
        elif expected_axis == 'X':
            return p1[0] != p2[0] and p1[1] == p2[1] and p1[2] == p2[2]
        elif expected_axis == 'Y':
            return p1[0] == p2[0] and p1[1] != p2[1] and p1[2] == p2[2]
        return False
