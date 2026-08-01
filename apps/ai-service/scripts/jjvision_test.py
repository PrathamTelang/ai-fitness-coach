import cv2
from app.engine.pose import PoseEngine
# IMPORT THE NEW TRACKER
from app.engine.excercises.jumping_jack import JumpingJackTracker

def run_local_test():
    print("1. Initializing AI Engine (MediaPipe)...")
    engine = PoseEngine()
    
    # Initialize Jumping Jacks for 10 reps
    tracker = JumpingJackTracker(target_reps=10)

    print("2. Connecting to Webcam...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    print("3. Starting webcam... Press 'q' to quit.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        landmarks, results = engine.extract_landmarks(frame)
        annotated_frame = engine.draw_skeleton(frame, results)

        # Process jumping jacks
        web_payload = tracker.process_frame(landmarks)

        # --- DRAW FULL BODY STATS (Top Left) ---
        cv2.putText(annotated_frame, f"JACKS: {web_payload['reps']}/{tracker.target_reps}", (10, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        cv2.putText(annotated_frame, f"STAGE: {web_payload['stage']}", (10, 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 165, 0), 2)
        
        # Show live angles for debugging
        cv2.putText(annotated_frame, f"L-ANG: {web_payload['left_angle']} | R-ANG: {web_payload['right_angle']}", (10, 115), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # --- DRAW SET COMPLETE ---
        if web_payload['set_complete']:
            cv2.putText(annotated_frame, "CARDIO COMPLETE!", (100, 250), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 4)

        cv2.imshow("RepSense Vision Test", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_local_test()