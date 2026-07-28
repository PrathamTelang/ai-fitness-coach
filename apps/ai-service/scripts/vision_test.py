print("🚨 THE SCRIPT IS SUCCESSFULLY RUNNING! 🚨")
import cv2
from app.engine.pose import PoseEngine

def run_local_test():
    print("1. Initializing AI Engine (MediaPipe)...")
    engine = PoseEngine()
    
    print("2. Connecting to Webcam (Bypassing Windows Bug)...")
    # THE MAGIC FIX: Add cv2.CAP_DSHOW to prevent the Windows freeze
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 

    print("3. Starting webcam... Press 'q' to quit.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Failed to access webcam.")
            break

        # Process frame
        landmarks, results = engine.extract_landmarks(frame)
        
        # Draw skeleton on screen
        annotated_frame = engine.draw_skeleton(frame, results)

        # Print Left Knee landmarks in terminal if visible
        if "LEFT_KNEE" in landmarks:
            print(f"Left Knee Pos: {landmarks['LEFT_KNEE']}")

        cv2.imshow("RepSense Vision Test", annotated_frame)

        # Break loop on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# THIS IS THE CRITICAL PART. IT MUST BE AT THE VERY BOTTOM.
# MUST BE FLUSH AGAINST THE LEFT WALL
if __name__ == "__main__":
    run_local_test()