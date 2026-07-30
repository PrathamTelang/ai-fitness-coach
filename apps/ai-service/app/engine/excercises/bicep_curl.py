import math

class BicepCurlTracker:
    def __init__(self, target_reps=10, weight_type="external_weight", weight_amount=15.0):
        self.counter = 0
        self.stage = None  # Tracks if the arm is "up" or "down"
        
        # New Settings for Set Tracking
        self.target_reps = target_reps
        self.weight_type = weight_type      # "body_weight" or "external_weight"
        self.weight_amount = weight_amount  # e.g., 15 (can be kg or lbs)
        self.set_complete = False           # Triggers when target is reached

    def calculate_angle(self, a, b, c):
        """Calculates the angle between three points."""
        radians = math.atan2(c['y'] - b['y'], c['x'] - b['x']) - \
                  math.atan2(a['y'] - b['y'], a['x'] - b['x'])
        
        angle = abs(radians * 180.0 / math.pi)
        
        if angle > 180.0:
            angle = 360 - angle
            
        return angle

    def process_frame(self, landmarks):
        """Processes the landmarks to count reps and track sets."""
        required_points = ['LEFT_SHOULDER', 'LEFT_ELBOW', 'LEFT_WRIST']
        
        # If the camera can't see the full arm, return the current data safely
        if not all(point in landmarks for point in required_points):
            return self.counter, self.stage, 0

        shoulder = landmarks['LEFT_SHOULDER']
        elbow = landmarks['LEFT_ELBOW']
        wrist = landmarks['LEFT_WRIST']

        # Calculate the angle of the elbow
        angle = self.calculate_angle(shoulder, elbow, wrist)

        # Rep counting logic
        if angle > 160:
            self.stage = "down"
            
        if angle < 30 and self.stage == "down":
            self.stage = "up"
            self.counter += 1
            
            # Format how the weight is displayed in the terminal
            if self.weight_type == "body_weight":
                weight_display = "Body Weight"
            else:
                weight_display = f"{self.weight_amount} lbs/kg"
            
            print(f"💪 REP: {self.counter}/{self.target_reps} | Resistance: {weight_display}")

            # Check if the user reached their goal!
            if self.counter >= self.target_reps and not self.set_complete:
                print("🎉 SET COMPLETE! Outstanding work!")
                self.set_complete = True

        return self.counter, self.stage, angle