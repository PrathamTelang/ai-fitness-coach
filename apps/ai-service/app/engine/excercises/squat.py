import math

class SquatTracker:
    def __init__(self, target_reps=10, weight_type="body_weight", weight_amount=0):
        self.counter = 0
        self.stage = "up"  
        self.target_reps = target_reps
        self.weight_type = weight_type
        self.weight_amount = weight_amount
        self.set_complete = False
        
        # ANTI-CHEAT: Track the highest point of the hips
        self.highest_hip_y = 10000 

    def calculate_angle(self, a, b, c):
        radians = math.atan2(c['y'] - b['y'], c['x'] - b['x']) - \
                  math.atan2(a['y'] - b['y'], a['x'] - b['x'])
        
        angle = abs(radians * 180.0 / math.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle

    def process_frame(self, landmarks):
        left_angle, right_angle = 0, 0
        
        if self.weight_type == "body_weight":
            weight_display = "Body Weight"
        else:
            weight_display = f"{self.weight_amount} lbs/kg"

        req_points = ['LEFT_HIP', 'LEFT_KNEE', 'LEFT_ANKLE', 
                      'RIGHT_HIP', 'RIGHT_KNEE', 'RIGHT_ANKLE',
                      'LEFT_SHOULDER']
                      
        if all(point in landmarks for point in req_points):
            left_angle = self.calculate_angle(landmarks['LEFT_HIP'], landmarks['LEFT_KNEE'], landmarks['LEFT_ANKLE'])
            right_angle = self.calculate_angle(landmarks['RIGHT_HIP'], landmarks['RIGHT_KNEE'], landmarks['RIGHT_ANKLE'])
            
            avg_angle = (left_angle + right_angle) / 2
            
            # Get the current Y position of the hip
            # (In OpenCV, Y gets larger as it goes DOWN the screen)
            current_hip_y = landmarks['LEFT_HIP']['y']

            # --- SQUAT TRACKING LOGIC ---
            
            # 1. User is standing up (calibrate hip height)
            if avg_angle > 160:
                self.stage = "up"
                # Record their standing hip height
                if current_hip_y < self.highest_hip_y:
                    self.highest_hip_y = current_hip_y
            
            # 2. User drops down
            # ANTI-CHEAT: The angle must compress AND the hips must physically drop significantly 
            # away from their standing position to count as a real squat!
            if avg_angle < 100 and current_hip_y > (self.highest_hip_y + 0.05):
                if self.stage == "up":
                    self.stage = "down"
            
            # 3. User stands back up to complete the rep
            if avg_angle > 160 and self.stage == "down":
                self.stage = "up"
                self.counter += 1
                print(f"🔥 LEGIT SQUAT REP: {self.counter}/{self.target_reps} | Load: {weight_display}")

        if self.counter >= self.target_reps and not self.set_complete:
            print("🎉 SQUAT SET COMPLETE! Awesome leg day!")
            self.set_complete = True

        return {
            "reps": self.counter,
            "stage": self.stage,
            "left_angle": int(left_angle),
            "right_angle": int(right_angle),
            "weight_display": weight_display,
            "set_complete": self.set_complete
        }   