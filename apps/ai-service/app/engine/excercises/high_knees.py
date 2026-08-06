import math

class HighKneesTracker:
    def __init__(self, target_reps=20, weight_type="body_weight", weight_amount=0):
        # Independent counters for each leg. Target is usually higher for cardio!
        self.counter_left = 0
        self.stage_left = "down"
        self.counter_right = 0
        self.stage_right = "down"
        
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
        
        # ---------------- LEFT KNEE LOGIC ----------------
        req_left = ['LEFT_SHOULDER', 'LEFT_HIP', 'LEFT_KNEE']
        if all(point in landmarks for point in req_left):
            left_angle = self.calculate_angle(
                landmarks['LEFT_SHOULDER'], landmarks['LEFT_HIP'], landmarks['LEFT_KNEE']
            )
            
            # Leg is straight down
            if left_angle > 150:
                if self.stage_left == "up":
                    self.stage_left = "down"

            # Knee driven high
            elif left_angle < 100:
                if self.stage_left == "down":
                    self.stage_left = "up"
                    self.counter_left += 1
                    print(f"🏃 LEFT KNEE: {self.counter_left}/{self.target_reps}")
                
            # Cheat Zone (Shallow knee drive)
            elif 100 <= left_angle <= 135 and self.stage_left == "down":
                self.stage_left = "halfway"
                self.feedback = "DRIVE KNEES HIGHER!"

        # ---------------- RIGHT KNEE LOGIC ----------------
        req_right = ['RIGHT_SHOULDER', 'RIGHT_HIP', 'RIGHT_KNEE']
        if all(point in landmarks for point in req_right):
            right_angle = self.calculate_angle(
                landmarks['RIGHT_SHOULDER'], landmarks['RIGHT_HIP'], landmarks['RIGHT_KNEE']
            )
            
            if right_angle > 150:
                if self.stage_right == "up":
                    self.stage_right = "down"

            elif right_angle < 100:
                if self.stage_right == "down":
                    self.stage_right = "up"
                    self.counter_right += 1
                    print(f"🏃 RIGHT KNEE: {self.counter_right}/{self.target_reps}")
                
            elif 100 <= right_angle <= 135 and self.stage_right == "down":
                self.stage_right = "halfway"
                self.feedback = "DRIVE KNEES HIGHER!"

        # ---------------- SET COMPLETION ----------------
        if self.counter_left >= self.target_reps and self.counter_right >= self.target_reps and not self.set_complete:
            print("🎉 HIGH KNEES COMPLETE! Incredible cardio pace!")
            self.set_complete = True

        return {
            "left": {"reps": self.counter_left, "stage": self.stage_left, "angle": int(left_angle)},
            "right": {"reps": self.counter_right, "stage": self.stage_right, "angle": int(right_angle)},
            "feedback": self.feedback,
            "set_complete": self.set_complete
        }