import cv2
from app.engine.pose import PoseEngine
from app.engine.excercises.push_up import PushUpTracker

def run_local_test():
    print("1. Initializing AI Engine (MediaPipe)...")
    engine = PoseEngine()
    
    print("2. Initializing Push-Up Tracker...")
    # Setting target to 5 reps for a quick test!
    tracker = PushUpTracker(target_reps=5)

    print("3. Connecting to Webcam...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    print("4. Starting webcam... Press 'q' to quit.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Failed to access webcam.")
            break

        landmarks, results = engine.extract_landmarks(frame)
        annotated_frame = engine.draw_skeleton(frame, results)

        # Process Push-Ups
        web_payload = tracker.process_frame(landmarks)

        # --- DRAW PUSH-UP STATS (Left side) ---
        cv2.putText(annotated_frame, f"REPS: {web_payload['left']['reps']}/{tracker.target_reps}", (10, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(annotated_frame, f"STAGE: {web_payload['left']['stage']}", (10, 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 165, 0), 2)
        
        # --- DRAW LIVE ANGLES FOR BOTH ARMS ---
        cv2.putText(annotated_frame, f"L-ANG: {web_payload['left']['angle']}", (10, 120), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(annotated_frame, f"R-ANG: {web_payload['right']['angle']}", (10, 150), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # --- DRAW FORM FEEDBACK (Anti-Cheat) ---
        if web_payload['feedback'] != "Good Form":
            # Draws the red warning at the bottom center of the screen
            cv2.putText(annotated_frame, f"WARNING: {web_payload['feedback']}", (50, 400), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        # --- DRAW SET COMPLETE ---
        if web_payload['set_complete']:
            cv2.putText(annotated_frame, "CHEST DAY CRUSHED!", (100, 250), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 4)

        cv2.imshow("RepSense Vision Test", annotated_frame)

        # Break loop on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_local_test()