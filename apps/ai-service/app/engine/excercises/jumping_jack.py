import math

class JumpingJackTracker:
    def __init__(self, target_reps=10):
        self.counter = 0
        self.stage = None
        self.target_reps = target_reps
        self.set_complete = False

    def calculate_angle(self, a, b, c):
        """Calculates the angle between three points."""
        radians = math.atan2(c['y'] - b['y'], c['x'] - b['x']) - \
                  math.atan2(a['y'] - b['y'], a['x'] - b['x'])
        
        angle = abs(radians * 180.0 / math.pi)
        if angle > 180.0:
            angle = 360 - angle
            
        return angle

    def process_frame(self, landmarks):
        """Processes landmarks to track full-body jumping jacks."""
        left_angle, right_angle = 0, 0
        
        # We need the Hips, Shoulders, and Wrists for this!
        req_points = ['LEFT_HIP', 'LEFT_SHOULDER', 'LEFT_WRIST', 
                      'RIGHT_HIP', 'RIGHT_SHOULDER', 'RIGHT_WRIST']
                      
        if all(point in landmarks for point in req_points):
            # Calculate Left Arm Angle (Hip -> Shoulder -> Wrist)
            left_angle = self.calculate_angle(
                landmarks['LEFT_HIP'], landmarks['LEFT_SHOULDER'], landmarks['LEFT_WRIST']
            )
            # Calculate Right Arm Angle
            right_angle = self.calculate_angle(
                landmarks['RIGHT_HIP'], landmarks['RIGHT_SHOULDER'], landmarks['RIGHT_WRIST']
            )
            
            # Average the two arms together to ensure symmetric movement
            avg_angle = (left_angle + right_angle) / 2

            # Stage tracking logic
            if avg_angle < 45:
                self.stage = "down"  # Arms by sides
            
            if avg_angle > 130 and self.stage == "down":
                self.stage = "up"    # Arms above head
                self.counter += 1
                print(f"🌟 JUMPING JACK REP: {self.counter}/{self.target_reps}")

        # Completion logic
        if self.counter >= self.target_reps and not self.set_complete:
            print("🎉 JUMPING JACKS COMPLETE! Great cardio!")
            self.set_complete = True

        # Return a unified dictionary for the frontend/vision UI
        return {
            "reps": self.counter,
            "stage": self.stage,
            "left_angle": int(left_angle),
            "right_angle": int(right_angle),
            "set_complete": self.set_complete
        }