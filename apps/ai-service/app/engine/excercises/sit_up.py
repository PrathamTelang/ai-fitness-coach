import math

class SitUpTracker:
    def __init__(self, target_reps=10, weight_type="body_weight", weight_amount=0):
        # We track overall reps for the core, averaging left and right sides
        self.counter = 0
        self.stage = "down"  # Starting flat on the back
        self.feedback = "Good Form"
        
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
        self.feedback = "Good Form"
        left_angle, right_angle = 0, 0
        
        # We need the Shoulders, Hips, and Knees
        req_points = ['LEFT_SHOULDER', 'LEFT_HIP', 'LEFT_KNEE', 
                      'RIGHT_SHOULDER', 'RIGHT_HIP', 'RIGHT_KNEE']
                      
        if all(point in landmarks for point in req_points):
            left_angle = self.calculate_angle(
                landmarks['LEFT_SHOULDER'], landmarks['LEFT_HIP'], landmarks['LEFT_KNEE']
            )
            right_angle = self.calculate_angle(
                landmarks['RIGHT_SHOULDER'], landmarks['RIGHT_HIP'], landmarks['RIGHT_KNEE']
            )
            
            # Average the core angle just in case one side is blocked from the camera view
            avg_angle = (left_angle + right_angle) / 2

            # --- SIT-UP LOGIC ---
            # Lying completely flat on the floor
            if avg_angle > 130:
                if self.stage == "up":
                    self.stage = "down"
                    self.counter += 1
                    print(f"🔥 SIT-UP REP: {self.counter}/{self.target_reps}")
                elif self.stage == "halfway":
                    self.stage = "down"
                    self.feedback = "COME ALL THE WAY UP!"

            # Sitting up and crunching the core
            elif avg_angle < 75:
                self.stage = "up"
                
            # The "Cheat Zone" - Didn't sit up high enough
            elif 75 <= avg_angle <= 105 and self.stage == "down":
                self.stage = "halfway"

        # Set Completion
        if self.counter >= self.target_reps and not self.set_complete:
            print("🎉 SIT-UP SET COMPLETE! Core of steel!")
            self.set_complete = True

        return {
            "left": {"reps": self.counter, "stage": self.stage, "angle": int(left_angle)},
            "right": {"reps": self.counter, "stage": self.stage, "angle": int(right_angle)},
            "feedback": self.feedback,
            "set_complete": self.set_complete
        }