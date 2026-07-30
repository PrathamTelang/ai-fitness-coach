import cv2
from app.engine.pose import PoseEngine
from app.engine.excercises.bicep_curl import BicepCurlTracker # NEW IMPORT

def run_local_test():
    print("1. Initializing AI Engine (MediaPipe)...")
    engine = PoseEngine()
    
    print("2. Initializing Bicep Tracker...")
    # Setting target to 5 reps for a quick test!
    tracker = BicepCurlTracker(target_reps=5, weight_type="external_weight", weight_amount=15.0)

    print("3. Connecting to Webcam (Bypassing Windows Bug)...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    print("4. Starting webcam... Press 'q' to quit.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Failed to access webcam.")
            break

        # Process frame
        landmarks, results = engine.extract_landmarks(frame)
        
        # Draw skeleton on screen
        annotated_frame = engine.draw_skeleton(frame, results)

        # --- PROCESS EXERCISE & CREATE WEB VARIABLE ---
        # Pass the skeleton data into our new tracker
        reps, stage, angle = tracker.process_frame(landmarks)
        
        # 🌐 THE WEB PAYLOAD 🌐
        # Later, we will send this exact dictionary to the frontend browser via WebSockets!
        web_payload = {
            "exercise": "Bicep Curl",
            "reps": reps,
            "target": tracker.target_reps,
            "stage": stage,
            "angle": int(angle),
            "set_complete": tracker.set_complete
        }

        # --- LOCAL VISUALIZATION (For testing today) ---
        # Draw the web payload data onto our local OpenCV window
        cv2.putText(annotated_frame, f"REPS: {web_payload['reps']}/{web_payload['target']}", (10, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    
        cv2.putText(annotated_frame, f"STAGE: {web_payload['stage']}", (10, 90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 165, 0), 2)
                    
        cv2.putText(annotated_frame, f"ANGLE: {web_payload['angle']}", (10, 130), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if web_payload['set_complete']:
            cv2.putText(annotated_frame, "SET COMPLETE!", (10, 200), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 4)

        cv2.imshow("RepSense Vision Test", annotated_frame)

        # Break loop on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# MUST BE FLUSH AGAINST THE LEFT WALL
if __name__ == "__main__":
    run_local_test()