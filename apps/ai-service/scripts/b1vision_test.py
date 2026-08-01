import cv2
from app.engine.pose import PoseEngine
from app.engine.excercises.bicep_curl import BicepCurlTracker

def run_local_test():
    print("1. Initializing AI Engine (MediaPipe)...")
    engine = PoseEngine()
    
    # Setting target to 5 reps for a quick test
    tracker = BicepCurlTracker(target_reps=5)

    print("2. Connecting to Webcam (Bypassing Windows Bug)...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    print("3. Starting webcam... Press 'q' to quit.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Failed to access webcam.")
            break

        landmarks, results = engine.extract_landmarks(frame)
        annotated_frame = engine.draw_skeleton(frame, results)

        # Get tracking data
        web_payload = tracker.process_frame(landmarks)

        # --- DRAW LEFT ARM STATS (Left side) ---
        cv2.putText(annotated_frame, f"L-REPS: {web_payload['left']['reps']}/{tracker.target_reps}", (10, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(annotated_frame, f"STAGE: {web_payload['left']['stage']}", (10, 75), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 165, 0), 2)
        cv2.putText(annotated_frame, f"ANGLE: {web_payload['left']['angle']}", (10, 110), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # --- DRAW RIGHT ARM STATS (Right side, shifted to X=400) ---
        cv2.putText(annotated_frame, f"R-REPS: {web_payload['right']['reps']}/{tracker.target_reps}", (400, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(annotated_frame, f"STAGE: {web_payload['right']['stage']}", (400, 75), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 165, 0), 2)
        cv2.putText(annotated_frame, f"ANGLE: {web_payload['right']['angle']}", (400, 110), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # --- DRAW SET COMPLETE ---
        if web_payload['set_complete']:
            cv2.putText(annotated_frame, "SET COMPLETE!", (150, 250), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 4)

        cv2.imshow("RepSense Vision Test", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_local_test()