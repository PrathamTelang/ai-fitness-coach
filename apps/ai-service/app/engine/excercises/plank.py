import math
import time

class PlankTracker:
    def __init__(self, target_time=30, weight_type="body_weight", weight_amount=0):
        # We track seconds instead of reps! Target is 30 seconds.
        self.elapsed_time = 0.0
        self.target_time = target_time
        
        self.stage = "resting"
        self.feedback = "Good Form"
        self.set_complete = False
        
        # Used to calculate how much time passes between camera frames
        self.last_frame_time = None

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
        
        # Figure out how much time has passed since the last frame
        current_time = time.time()
        if self.last_frame_time is None:
            self.last_frame_time = current_time
            
        delta_time = current_time - self.last_frame_time
        self.last_frame_time = current_time

        req_points = ['LEFT_SHOULDER', 'LEFT_HIP', 'LEFT_ANKLE',
                      'RIGHT_SHOULDER', 'RIGHT_HIP', 'RIGHT_ANKLE']
                      
        if all(point in landmarks for point in req_points):
            left_angle = self.calculate_angle(
                landmarks['LEFT_SHOULDER'], landmarks['LEFT_HIP'], landmarks['LEFT_ANKLE']
            )
            right_angle = self.calculate_angle(
                landmarks['RIGHT_SHOULDER'], landmarks['RIGHT_HIP'], landmarks['RIGHT_ANKLE']
            )
            
            # Average the sides to determine overall back straightness
            avg_angle = (left_angle + right_angle) / 2

            # --- PLANK TIME TRACKING LOGIC ---
            # If the body is straight, add time to the stopwatch!
            if avg_angle > 150:
                self.stage = "holding"
                self.elapsed_time += delta_time
            else:
                self.stage = "resting"
                # Only yell at them if they actually started the plank already
                if self.elapsed_time > 0 and not self.set_complete:
                    self.feedback = "STRAIGHTEN YOUR BACK!"

        # Set Completion
        if self.elapsed_time >= self.target_time and not self.set_complete:
            print("🎉 PLANK COMPLETE! Unbreakable core!")
            self.set_complete = True

        # We hijack the 'reps' key to pass our timer string (e.g., "15s") to the UI!
        display_time = f"{int(self.elapsed_time)}s"

        return {
            "left": {"reps": display_time, "stage": self.stage, "angle": int(left_angle)},
            "right": {"reps": display_time, "stage": self.stage, "angle": int(right_angle)},
            "feedback": self.feedback,
            "set_complete": self.set_complete
        }