import math

class CalfRaiseTracker:
    def __init__(self, target_reps=15, weight_type="body_weight", weight_amount=0):
        # Tracking overall reps by averaging both legs
        self.counter = 0
        self.stage = "down"  # Starting with heels on the floor
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
        
        # We need the Knees, Ankles, and the tips of the feet (Foot Index)
        req_points = ['LEFT_KNEE', 'LEFT_ANKLE', 'LEFT_FOOT_INDEX', 
                      'RIGHT_KNEE', 'RIGHT_ANKLE', 'RIGHT_FOOT_INDEX']
                      
        if all(point in landmarks for point in req_points):
            left_angle = self.calculate_angle(
                landmarks['LEFT_KNEE'], landmarks['LEFT_ANKLE'], landmarks['LEFT_FOOT_INDEX']
            )
            right_angle = self.calculate_angle(
                landmarks['RIGHT_KNEE'], landmarks['RIGHT_ANKLE'], landmarks['RIGHT_FOOT_INDEX']
            )
            
            # Average the angle
            avg_angle = (left_angle + right_angle) / 2

            # --- CALF RAISE LOGIC ---
            # Flexing up onto the toes
            if avg_angle > 135:
                if self.stage == "down":
                    self.stage = "up"
                    self.counter += 1
                    print(f"🔥 CALF RAISE: {self.counter}/{self.target_reps}")
                elif self.stage == "halfway":
                    self.stage = "up"
                    self.feedback = "SQUEEZE AT THE TOP!"

            # Heels flat on the floor
            elif avg_angle < 115:
                self.stage = "down"
                
            # The "Cheat Zone" - Didn't go high enough on the toes
            elif 115 <= avg_angle <= 135 and self.stage == "down":
                self.stage = "halfway"

        # Set Completion
        if self.counter >= self.target_reps and not self.set_complete:
            print("🎉 CALF RAISES COMPLETE! Ready for a marathon!")
            self.set_complete = True

        return {
            "left": {"reps": self.counter, "stage": self.stage, "angle": int(left_angle)},
            "right": {"reps": self.counter, "stage": self.stage, "angle": int(right_angle)},
            "feedback": self.feedback,
            "set_complete": self.set_complete
        }   