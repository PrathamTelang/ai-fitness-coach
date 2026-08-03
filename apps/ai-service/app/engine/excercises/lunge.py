import math

class LungeTracker:
    def __init__(self, target_reps=10, weight_type="body_weight", weight_amount=0):
        # Independent counters for each leg
        self.counter_left = 0
        self.stage_left = "up"
        self.counter_right = 0
        self.stage_right = "up"
        
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
        
        # ---------------- LEFT LEG LUNGE ----------------
        req_left = ['LEFT_HIP', 'LEFT_KNEE', 'LEFT_ANKLE']
        if all(point in landmarks for point in req_left):
            left_angle = self.calculate_angle(
                landmarks['LEFT_HIP'], landmarks['LEFT_KNEE'], landmarks['LEFT_ANKLE']
            )
            
            # Standing back up
            if left_angle > 150:
                if self.stage_left == "down":
                    self.stage_left = "up"
                    self.counter_left += 1
                    print(f"🦵 LEFT LUNGE: {self.counter_left}/{self.target_reps}")
                elif self.stage_left == "halfway":
                    self.stage_left = "up"
                    self.feedback = "DROP KNEE LOWER!"

            # Deep lunge (knee at ~90 degrees)
            elif left_angle < 100:
                self.stage_left = "down"
                
            # Cheat Zone (Shallow lunge)
            elif 100 <= left_angle <= 135 and self.stage_left == "up":
                self.stage_left = "halfway"

        # ---------------- RIGHT LEG LUNGE ----------------
        req_right = ['RIGHT_HIP', 'RIGHT_KNEE', 'RIGHT_ANKLE']
        if all(point in landmarks for point in req_right):
            right_angle = self.calculate_angle(
                landmarks['RIGHT_HIP'], landmarks['RIGHT_KNEE'], landmarks['RIGHT_ANKLE']
            )
            
            if right_angle > 150:
                if self.stage_right == "down":
                    self.stage_right = "up"
                    self.counter_right += 1
                    print(f"🦵 RIGHT LUNGE: {self.counter_right}/{self.target_reps}")
                elif self.stage_right == "halfway":
                    self.stage_right = "up"
                    self.feedback = "DROP KNEE LOWER!"

            elif right_angle < 100:
                self.stage_right = "down"
                
            elif 100 <= right_angle <= 135 and self.stage_right == "up":
                self.stage_right = "halfway"

        # ---------------- SET COMPLETION ----------------
        if self.counter_left >= self.target_reps and self.counter_right >= self.target_reps and not self.set_complete:
            print("🎉 LUNGES COMPLETE! Legs of steel!")
            self.set_complete = True

        return {
            "left": {"reps": self.counter_left, "stage": self.stage_left, "angle": int(left_angle)},
            "right": {"reps": self.counter_right, "stage": self.stage_right, "angle": int(right_angle)},
            "feedback": self.feedback,
            "set_complete": self.set_complete
        }