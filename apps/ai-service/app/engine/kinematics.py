import math
from typing import Dict

class KinematicsEngine:
    """
    Handles the mathematical calculations for human body biomechanics,
    specifically converting raw 3D spatial coordinates into joint angles.
    """
    
    @staticmethod
    def calculate_angle(
        point_a: Dict[str, float], 
        point_b: Dict[str, float], 
        point_c: Dict[str, float]
    ) -> float:
        """
        Calculates the 2D angle (in degrees) between three points.
        point_b is treated as the vertex (e.g., the knee).
        """
        # Extract X and Y coordinates for all three joints
        x1, y1 = point_a['x'], point_a['y']
        x2, y2 = point_b['x'], point_b['y'] # The middle joint (Vertex)
        x3, y3 = point_c['x'], point_c['y']

        # Calculate the angle using arctangent
        radians = math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2)
        angle = abs(radians * 180.0 / math.pi)

        # Ensure the angle never exceeds 180 degrees for standard joint tracking
        if angle > 180.0:
            angle = 360.0 - angle

        return round(angle, 2)

    @staticmethod
    def check_form(current_angle: float, target_min: float, target_max: float) -> bool:
        """
        A simple helper function to verify if a joint angle falls 
        within a target range for proper exercise form.
        """
        return target_min <= current_angle <= target_max