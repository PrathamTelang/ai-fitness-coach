import math

class BicepCurlTracker:
    def __init__(self, target_reps=10, weight_type="external_weight", weight_amount=15.0):
        # Independent counters and stages for each arm
        self.counter_left = 0
        self.stage_left = None
        self.counter_right = 0
        self.stage_right = None
        
        # Settings for Set Tracking
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
        """Processes the landmarks to count reps for both arms."""
        left_angle, right_angle = 0, 0
        
        if self.weight_type == "body_weight":
            weight_display = "Body Weight"
        else:
            weight_display = f"{self.weight_amount} lbs/kg"

        # ---------------- LEFT ARM LOGIC ----------------
        req_left = ['LEFT_SHOULDER', 'LEFT_ELBOW', 'LEFT_WRIST']
        if all(point in landmarks for point in req_left):
            shoulder = landmarks['LEFT_SHOULDER']
            elbow = landmarks['LEFT_ELBOW']
            wrist = landmarks['LEFT_WRIST']

            left_angle = self.calculate_angle(shoulder, elbow, wrist)

            # Relaxed angles: 140 for down, 60 for up
            if left_angle > 140:
                self.stage_left = "down"
            if left_angle < 60 and self.stage_left == "down":
                self.stage_left = "up"
                self.counter_left += 1
                print(f"💪 LEFT REP: {self.counter_left}/{self.target_reps} | Resistance: {weight_display}")

        # ---------------- RIGHT ARM LOGIC ----------------
        req_right = ['RIGHT_SHOULDER', 'RIGHT_ELBOW', 'RIGHT_WRIST']
        if all(point in landmarks for point in req_right):
            shoulder = landmarks['RIGHT_SHOULDER']
            elbow = landmarks['RIGHT_ELBOW']
            wrist = landmarks['RIGHT_WRIST']

            right_angle = self.calculate_angle(shoulder, elbow, wrist)

            # Relaxed angles: 140 for down, 60 for up
            if right_angle > 140:
                self.stage_right = "down"
            if right_angle < 60 and self.stage_right == "down":
                self.stage_right = "up"
                self.counter_right += 1
                print(f"💪 RIGHT REP: {self.counter_right}/{self.target_reps} | Resistance: {weight_display}")

        # ---------------- SET COMPLETION ----------------
        if self.counter_left >= self.target_reps and self.counter_right >= self.target_reps and not self.set_complete:
            print("🎉 SET COMPLETE! Both arms finished! Outstanding work!")
            self.set_complete = True

        return {
            "left": {"reps": self.counter_left, "stage": self.stage_left, "angle": int(left_angle)},
            "right": {"reps": self.counter_right, "stage": self.stage_right, "angle": int(right_angle)},
            "set_complete": self.set_complete
        }