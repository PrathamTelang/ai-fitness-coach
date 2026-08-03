import math

class PushUpTracker:
    def __init__(self, target_reps=10, weight_type="body_weight", weight_amount=0):
        # We will track the overall rep count (averaging both arms for stability)
        self.counter = 0
        self.stage = "up"  # Default starting position is the high plank
        self.feedback = "Good Form"
        
        self.target_reps = target_reps
        self.weight_type = weight_type
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
        self.feedback = "Good Form"
        left_angle, right_angle = 0, 0
        
        req_points = ['LEFT_SHOULDER', 'LEFT_ELBOW', 'LEFT_WRIST', 
                      'RIGHT_SHOULDER', 'RIGHT_ELBOW', 'RIGHT_WRIST']
                      
        if all(point in landmarks for point in req_points):
            # Calculate angles for both arms
            left_angle = self.calculate_angle(
                landmarks['LEFT_SHOULDER'], landmarks['LEFT_ELBOW'], landmarks['LEFT_WRIST']
            )
            right_angle = self.calculate_angle(
                landmarks['RIGHT_SHOULDER'], landmarks['RIGHT_ELBOW'], landmarks['RIGHT_WRIST']
            )
            
            # Average the angles in case the camera can only see one side well
            avg_angle = (left_angle + right_angle) / 2

            # --- PUSH-UP LOGIC ---
            # High plank position (arms nearly straight)
            if avg_angle > 150:
                if self.stage == "down":
                    self.stage = "up"
                    self.counter += 1
                    print(f"🔥 PUSH-UP REP: {self.counter}/{self.target_reps}")
                elif self.stage == "halfway":
                    self.stage = "up"
                    self.feedback = "LOWER YOUR CHEST!"

            # Chest lowered down (elbows bent past 90 degrees)
            elif avg_angle < 90:
                self.stage = "down"
                
            # The "Cheat Zone" - halfway down
            elif 90 <= avg_angle <= 120 and self.stage == "up":
                self.stage = "halfway"

        # Set Completion
        if self.counter >= self.target_reps and not self.set_complete:
            print("🎉 PUSH-UP SET COMPLETE! Chest day crushed!")
            self.set_complete = True

        # Output matches the unified dictionary structure for the UI
        return {
            "left": {"reps": self.counter, "stage": self.stage, "angle": int(left_angle)},
            "right": {"reps": self.counter, "stage": self.stage, "angle": int(right_angle)},
            "feedback": self.feedback,
            "set_complete": self.set_complete
        }