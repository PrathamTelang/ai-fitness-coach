import math

class LateralRaiseTracker:
    def __init__(self, target_reps=10, weight_type="dumbbells", weight_amount=10.0):
        # Track both arms independently
        self.counter_left = 0
        self.stage_left = "down"
        self.counter_right = 0
        self.stage_right = "down"
        
        self.feedback = "Good Form"
        self.target_reps = target_reps
        self.weight_type = weight_type
        self.weight_amount = weight_amount
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
        
        weight_display = f"{self.weight_amount} lbs/kg" if self.weight_type != "body_weight" else "Body Weight"

        # ---------------- LEFT ARM LOGIC ----------------
        req_left = ['LEFT_HIP', 'LEFT_SHOULDER', 'LEFT_WRIST']
        if all(point in landmarks for point in req_left):
            left_angle = self.calculate_angle(
                landmarks['LEFT_HIP'], landmarks['LEFT_SHOULDER'], landmarks['LEFT_WRIST']
            )

            # Arm raised out to the side
            if left_angle > 75:
                if self.stage_left == "down":
                    self.stage_left = "up"
                    self.counter_left += 1
                    print(f"🦅 LEFT RAISE: {self.counter_left}/{self.target_reps} | Load: {weight_display}")
                elif self.stage_left == "halfway":
                    self.stage_left = "up"
                    self.feedback = "RAISE ALL THE WAY UP!"

            # Arm resting at the side
            elif left_angle < 30:
                self.stage_left = "down"
                
            # Cheat Zone (half rep)
            elif 30 <= left_angle <= 60 and self.stage_left == "down":
                self.stage_left = "halfway"

        # ---------------- RIGHT ARM LOGIC ----------------
        req_right = ['RIGHT_HIP', 'RIGHT_SHOULDER', 'RIGHT_WRIST']
        if all(point in landmarks for point in req_right):
            right_angle = self.calculate_angle(
                landmarks['RIGHT_HIP'], landmarks['RIGHT_SHOULDER'], landmarks['RIGHT_WRIST']
            )

            if right_angle > 75:
                if self.stage_right == "down":
                    self.stage_right = "up"
                    self.counter_right += 1
                    print(f"🦅 RIGHT RAISE: {self.counter_right}/{self.target_reps} | Load: {weight_display}")
                elif self.stage_right == "halfway":
                    self.stage_right = "up"
                    self.feedback = "RAISE ALL THE WAY UP!"

            elif right_angle < 30:
                self.stage_right = "down"
                
            elif 30 <= right_angle <= 60 and self.stage_right == "down":
                self.stage_right = "halfway"

        # ---------------- SET COMPLETION ----------------
        if self.counter_left >= self.target_reps and self.counter_right >= self.target_reps and not self.set_complete:
            print("🎉 LATERAL RAISES COMPLETE! Shoulders on fire!")
            self.set_complete = True

        return {
            "left": {"reps": self.counter_left, "stage": self.stage_left, "angle": int(left_angle)},
            "right": {"reps": self.counter_right, "stage": self.stage_right, "angle": int(right_angle)},
            "feedback": self.feedback,
            "set_complete": self.set_complete
        }