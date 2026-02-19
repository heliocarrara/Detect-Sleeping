"""
Core computer-vision logic for drowsiness detection.

This module contains everything related to:
    * Loading and configuring the MediaPipe Face Landmarker model
    * Computing the Eye Aspect Ratio (EAR) from eye landmarks
    * Applying a simple "consecutive frames below threshold" rule
      to decide when a drowsiness alert should be triggered.

The UI layer (Tkinter) is implemented separately in ``app.py`` and
only calls ``DrowsinessDetector.process_frame`` with each camera frame.
"""

import os
import urllib.request

import cv2
import numpy as np
from scipy.spatial import distance as dist
from mediapipe import Image as MpImage, ImageFormat
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision


# Indices of eye landmarks in the MediaPipe Face Mesh topology.
# These were chosen to form a polygon around each eye that works
# well with the EAR formula.
LEFT_EYE_IDXS = [33, 160, 158, 133, 153, 144]
RIGHT_EYE_IDXS = [362, 385, 387, 263, 373, 380]


class DrowsinessDetector:
    def __init__(self, model_path: str = "face_landmarker.task", consec_frames: int = 15):
        """
        Create a new drowsiness detector instance.

        Parameters
        ----------
        model_path:
            Path where the MediaPipe ``face_landmarker.task`` model
            should be stored / loaded from.
        consec_frames:
            Minimum number of consecutive frames below the EAR threshold
            before the system considers that drowsiness has been detected.
        """
        self.model_path = model_path
        self.consec_frames = consec_frames
        # Number of consecutive frames where EAR stayed below threshold.
        self.counter = 0
        # Whether an alarm is currently active.
        self.alarm_on = False
        # MediaPipe FaceLandmarker instance.
        self.face_mesh = self._create_face_landmarker()

    def _ensure_model_file(self) -> None:
        """
        Download the Face Landmarker model if it does not exist locally.
        """
        if os.path.exists(self.model_path):
            return
        url = (
            "https://storage.googleapis.com/mediapipe-models/face_landmarker/"
            "face_landmarker/float16/latest/face_landmarker.task"
        )
        urllib.request.urlretrieve(url, self.model_path)

    def _create_face_landmarker(self):
        """
        Configure and create the MediaPipe FaceLandmarker instance.
        """
        self._ensure_model_file()
        base_options = mp_python.BaseOptions(model_asset_path=self.model_path)
        options = mp_vision.FaceLandmarkerOptions(
            base_options=base_options,
            num_faces=1,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=False,
        )
        return mp_vision.FaceLandmarker.create_from_options(options)

    def _calculate_ear(self, eye_landmarks: np.ndarray) -> float:
        """
        Compute the Eye Aspect Ratio (EAR) for a single eye.

        EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)

        where p1..p6 are arranged around the eye contour.
        A lower EAR means the eye is more closed.
        """
        A = dist.euclidean(eye_landmarks[1], eye_landmarks[5])
        B = dist.euclidean(eye_landmarks[2], eye_landmarks[4])
        C = dist.euclidean(eye_landmarks[0], eye_landmarks[3])
        if C == 0:
            return 0.0
        return (A + B) / (2.0 * C)

    def process_frame(self, frame_bgr, threshold: float):
        """
        Process a BGR frame and return drowsiness analysis and overlays.

        Parameters
        ----------
        frame_bgr:
            OpenCV image in BGR format captured from the webcam.
        threshold:
            EAR threshold below which the eyes are considered closed.

        Returns
        -------
        frame:
            Frame with landmarks and text overlays drawn on it.
        ear_display:
            Final EAR value used for display.
        status_text:
            Text describing the current state ("Olhos Abertos" or alert).
        alarm_on:
            Boolean indicating whether an alert is currently active.
        """
        # Normalize frame size to keep MediaPipe and UI behavior consistent.
        frame = cv2.resize(frame_bgr, (640, 480))
        # MediaPipe expects RGB input.
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = MpImage(image_format=ImageFormat.SRGB, data=rgb_frame)
        results = self.face_mesh.detect(mp_image)

        ear_display = 0.0
        # Default text when no drowsiness is detected.
        status_text = "Olhos Abertos"
        alarm_on = False

        if results.face_landmarks:
            for face_landmarks in results.face_landmarks:
                h, w, _ = frame.shape
                points = np.array([[int(l.x * w), int(l.y * h)] for l in face_landmarks])

                left_eye = points[LEFT_EYE_IDXS]
                right_eye = points[RIGHT_EYE_IDXS]

                cv2.polylines(frame, [left_eye], True, (0, 255, 0), 1)
                cv2.polylines(frame, [right_eye], True, (0, 255, 0), 1)

                left_ear = self._calculate_ear(left_eye)
                right_ear = self._calculate_ear(right_eye)
                ear_display = (left_ear + right_ear) / 2.0

                if ear_display < threshold:
                    self.counter += 1
                    if self.counter >= self.consec_frames:
                        alarm_on = True
                        status_text = "ALERTA: SONO DETECTADO!"
                        cv2.putText(
                            frame,
                            "ACORDE!",
                            (200, 240),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            2,
                            (0, 0, 255),
                            3,
                        )
                else:
                    self.counter = 0
                    alarm_on = False

        # Draw EAR text in green when safe and red when alarm is active.
        color_bgr = (0, 255, 0) if not alarm_on else (0, 0, 255)
        cv2.putText(
            frame,
            f"EAR: {ear_display:.2f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color_bgr,
            2,
        )

        self.alarm_on = alarm_on
        return frame, ear_display, status_text, alarm_on

