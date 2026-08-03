import cv2
from app.engine.pose import PoseEngine

# Import all 7 of our exercise trackers
from app.engine.excercises.bicep_curl import BicepCurlTracker
from app.engine.excercises.squat import SquatTracker
from app.engine.excercises.jumping_jack import JumpingJackTracker 
from app.engine.excercises.push_up import PushUpTracker
from app.engine.excercises.shoulder_press import ShoulderPressTracker
from app.engine.excercises.sit_up import SitUpTracker
from app.engine.excercises.lateral_raise import LateralRaiseTracker

def run_local_test():
    print("1. Initializing AI Engine (MediaPipe)...")
    engine = PoseEngine()
    
    print("2. Loading Exercise Modules...")
    # Dictionary holding all our trackers so we can switch between them easily
    exercises = {
        '1': {"name": "Bicep Curls", "tracker": BicepCurlTracker(target_reps=10)},
        '2': {"name": "Squats", "tracker": SquatTracker(target_reps=10)},
        '3': {"name": "Jumping Jacks", "tracker": JumpingJackTracker(target_reps=10)},
        '4': {"name": "Push-Ups", "tracker": PushUpTracker(target_reps=10)},
        '5': {"name": "Shoulder Press", "tracker": ShoulderPressTracker(target_reps=10)},
        '6': {"name": "Sit-Ups", "tracker": SitUpTracker(target_reps=15)},
        '7': {"name": "Lateral Raises", "tracker": LateralRaiseTracker(target_reps=10)}
    }
    
    # Start on Bicep Curls by default
    current_mode = '1'

    print("3. Connecting to Webcam...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    print("4. Starting webcam... Ready to work out!")
    print("Press 1-7 to switch exercises. Press 'q' to quit.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Failed to access webcam.")
            break

        landmarks, results = engine.extract_landmarks(frame)
        annotated_frame = engine.draw_skeleton(frame, results)

        # Get the currently selected tracker
        active_exercise_name = exercises[current_mode]["name"]
        active_tracker = exercises[current_mode]["tracker"]

        # Only process if we see a person
        if landmarks:
            web_payload = active_tracker.process_frame(landmarks)
            
            # --- DRAW UI OVERLAYS ---
            # Using .get() safely handles older trackers that might not output exact keys
            left_data = web_payload.get('left', {'reps': 0, 'stage': 'N/A', 'angle': 0})
            right_data = web_payload.get('right', {'reps': 0, 'stage': 'N/A', 'angle': 0})
            feedback = web_payload.get('feedback', 'Good Form')
            set_complete = web_payload.get('set_complete', False)

            # Left Arm/Leg Stats
            cv2.putText(annotated_frame, f"L-REPS: {left_data['reps']}", (10, 80), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"L-STAGE: {left_data['stage']}", (10, 110), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 165, 0), 2)
            
            # Right Arm/Leg Stats
            cv2.putText(annotated_frame, f"R-REPS: {right_data['reps']}", (450, 80), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"R-STAGE: {right_data['stage']}", (450, 110), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 165, 0), 2)

            # Draw Form Feedback (Anti-Cheat)
            if feedback != "Good Form":
                cv2.putText(annotated_frame, f"WARNING: {feedback}", (150, 400), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)

            # Draw Set Complete
            if set_complete:
                cv2.putText(annotated_frame, "SET COMPLETE!", (180, 250), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 4)

        # --- DRAW MENU SYSTEM ---
        # Top Header showing current exercise
        cv2.putText(annotated_frame, f"MODE: {active_exercise_name}", (10, 35), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)
        
        # Bottom Footer showing controls (Split into two lines so it fits on screen)
        menu_text_1 = "[1] Bicep [2] Squat [3] Jacks [4] Push-Up"
        menu_text_2 = "[5] Press [6] Sit-Up [7] Lat Raise [Q] Quit"
        cv2.putText(annotated_frame, menu_text_1, (10, 445), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        cv2.putText(annotated_frame, menu_text_2, (10, 465), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        cv2.imshow("RepSense AI Coach", annotated_frame)

        # Keyboard Input Logic
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('1'): current_mode = '1'
        elif key == ord('2'): current_mode = '2'
        elif key == ord('3'): current_mode = '3'
        elif key == ord('4'): current_mode = '4'
        elif key == ord('5'): current_mode = '5'
        elif key == ord('6'): current_mode = '6'
        elif key == ord('7'): current_mode = '7'

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_local_test()