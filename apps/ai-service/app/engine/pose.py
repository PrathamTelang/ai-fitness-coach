import cv2
import mediapipe as mp
from typing import Dict, Any, Tuple, Optional

class PoseEngine:
    """
    Core Computer Vision engine responsible for processing frames
    and extracting 33 3D skeletal landmarks using MediaPipe.
    """
    def __init__(
        self,
        static_image_mode: bool = False,
        model_complexity: int = 1,
        smooth_landmarks: bool = True,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Initialize MediaPipe Pose Model
        self.pose = self.mp_pose.Pose(
            static_image_mode=static_image_mode,
            model_complexity=model_complexity,
            smooth_landmarks=smooth_landmarks,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def extract_landmarks(self, frame) -> Tuple[Dict[str, Dict[str, float]], Optional[Any]]:
        """
        Converts BGR image frame to RGB, processes it with MediaPipe,
        and returns a dictionary of normalized body coordinates.
        """
        # MediaPipe requires RGB images; OpenCV defaults to BGR
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)

        landmarks_data = {}

        if results.pose_landmarks:
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                landmark_name = self.mp_pose.PoseLandmark(idx).name
                landmarks_data[landmark_name] = {
                    "x": round(landmark.x, 4),
                    "y": round(landmark.y, 4),
                    "z": round(landmark.z, 4),
                    "visibility": round(landmark.visibility, 4),
                }

        return landmarks_data, results

    def draw_skeleton(self, frame, results) -> Any:
        """
        Draws the visual skeletal connections directly onto an image frame.
        """
        if results and results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2),
            )
        return frame