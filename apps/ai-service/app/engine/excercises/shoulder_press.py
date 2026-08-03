import math

class ShoulderPressTracker:
    def __init__(self, target_reps=10, weight_type="dumbbells", weight_amount=15.0):
        # Independent tracking for both arms
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
        req_left = ['LEFT_SHOULDER', 'LEFT_ELBOW', 'LEFT_WRIST']
        if all(point in landmarks for point in req_left):
            left_angle = self.calculate_angle(
                landmarks['LEFT_SHOULDER'], landmarks['LEFT_ELBOW'], landmarks['LEFT_WRIST']
            )

            # Arms pushed fully straight up
            if left_angle > 150:
                if self.stage_left == "down":
                    self.stage_left = "up"
                    self.counter_left += 1
                    print(f"🏋️ LEFT PRESS: {self.counter_left}/{self.target_reps} | Load: {weight_display}")
                elif self.stage_left == "halfway":
                    self.stage_left = "up"
                    self.feedback = "PRESS ALL THE WAY UP!"

            # Arms brought down to the shoulders
            elif left_angle < 90:
                self.stage_left = "down"
                
            # Cheat Zone (half rep)
            elif 90 <= left_angle <= 130 and self.stage_left == "down":
                self.stage_left = "halfway"

        # ---------------- RIGHT ARM LOGIC ----------------
        req_right = ['RIGHT_SHOULDER', 'RIGHT_ELBOW', 'RIGHT_WRIST']
        if all(point in landmarks for point in req_right):
            right_angle = self.calculate_angle(
                landmarks['RIGHT_SHOULDER'], landmarks['RIGHT_ELBOW'], landmarks['RIGHT_WRIST']
            )

            if right_angle > 150:
                if self.stage_right == "down":
                    self.stage_right = "up"
                    self.counter_right += 1
                    print(f"🏋️ RIGHT PRESS: {self.counter_right}/{self.target_reps} | Load: {weight_display}")
                elif self.stage_right == "halfway":
                    self.stage_right = "up"
                    self.feedback = "PRESS ALL THE WAY UP!"

            elif right_angle < 90:
                self.stage_right = "down"
                
            elif 90 <= right_angle <= 130 and self.stage_right == "down":
                self.stage_right = "halfway"

        # ---------------- SET COMPLETION ----------------
        if self.counter_left >= self.target_reps and self.counter_right >= self.target_reps and not self.set_complete:
            print("🎉 SHOULDER PRESS COMPLETE! Boulder shoulders activated!")
            self.set_complete = True

        return {
            "left": {"reps": self.counter_left, "stage": self.stage_left, "angle": int(left_angle)},
            "right": {"reps": self.counter_right, "stage": self.stage_right, "angle": int(right_angle)},
            "feedback": self.feedback,
            "set_complete": self.set_complete
        }