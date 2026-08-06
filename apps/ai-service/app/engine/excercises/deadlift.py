import math

class DeadliftTracker:
    def __init__(self, target_reps=8, weight_type="barbell", weight_amount=135.0):
        # We will track the overall rep count by averaging both sides for stability
        self.counter = 0
        self.stage = "up"
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
        left_hip_angle, right_hip_angle = 0, 0
        
        weight_display = f"{self.weight_amount} lbs/kg" if self.weight_type != "body_weight" else "Body Weight"
        
        req_points = ['LEFT_SHOULDER', 'LEFT_HIP', 'LEFT_KNEE', 'LEFT_ANKLE',
                      'RIGHT_SHOULDER', 'RIGHT_HIP', 'RIGHT_KNEE', 'RIGHT_ANKLE']
                      
        if all(point in landmarks for point in req_points):
            # Calculate Hip Angles (Hinge)
            left_hip_angle = self.calculate_angle(
                landmarks['LEFT_SHOULDER'], landmarks['LEFT_HIP'], landmarks['LEFT_KNEE']
            )
            right_hip_angle = self.calculate_angle(
                landmarks['RIGHT_SHOULDER'], landmarks['RIGHT_HIP'], landmarks['RIGHT_KNEE']
            )
            
            # Calculate Knee Angles (Bend)
            left_knee_angle = self.calculate_angle(
                landmarks['LEFT_HIP'], landmarks['LEFT_KNEE'], landmarks['LEFT_ANKLE']
            )
            right_knee_angle = self.calculate_angle(
                landmarks['RIGHT_HIP'], landmarks['RIGHT_KNEE'], landmarks['RIGHT_ANKLE']
            )
            
            avg_hip = (left_hip_angle + right_hip_angle) / 2
            avg_knee = (left_knee_angle + right_knee_angle) / 2

            # --- DEADLIFT LOGIC ---
            # Standing up straight (Hips and Knees locked out)
            if avg_hip > 160 and avg_knee > 150:
                if self.stage == "down":
                    self.stage = "up"
                    self.counter += 1
                    print(f"🏋️ DEADLIFT REP: {self.counter}/{self.target_reps} | Load: {weight_display}")
                elif self.stage == "halfway":
                    self.stage = "up"
                    self.feedback = "LOCK OUT HIPS!"

            # Bottom of the deadlift (Hips hinged, knees bent)
            elif avg_hip < 100 and avg_knee < 140:
                self.stage = "down"
                
            # The "Cheat Zone" - halfway up/down or stiff-legged
            elif 100 <= avg_hip <= 140 and self.stage == "up":
                self.stage = "halfway"
                
            # Form Correction: Knees bending too much (Turning it into a squat!)
            if avg_knee < 90 and avg_hip > 110:
                self.feedback = "TOO MUCH KNEE BEND! HINGE MORE."

        # Set Completion
        if self.counter >= self.target_reps and not self.set_complete:
            print("🎉 DEADLIFT SET COMPLETE! Huge pull!")
            self.set_complete = True

        return {
            "left": {"reps": self.counter, "stage": self.stage, "angle": int(left_hip_angle)},
            "right": {"reps": self.counter, "stage": self.stage, "angle": int(right_hip_angle)},
            "feedback": self.feedback,
            "set_complete": self.set_complete
        }