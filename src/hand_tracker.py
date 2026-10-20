
import time
from pathlib import Path

import cv2
import mediapipe as mp


# Find the model relative to the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "hand_landmarker.task"

# Hand landmark connections: pairs of landmark indices
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17),
]


def main():
    if not MODEL_PATH.exists():
        print(f"Model file not found: {MODEL_PATH}")
        print("Download hand_landmarker.task into the models folder.")
        return

    # Configure MediaPipe Hand Landmarker for video
    options = mp.tasks.vision.HandLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(
            model_asset_path=str(MODEL_PATH)
        ),
        running_mode=mp.tasks.vision.RunningMode.VIDEO,
        num_hands=1,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
    )

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    try:
        with mp.tasks.vision.HandLandmarker.create_from_options(
            options
        ) as landmarker:

            print("Hand tracking started. Press 'q' to quit.")

            while True:
                success, frame = cap.read()

                if not success:
                    print("Could not read webcam frame.")
                    break

                # Mirror the webcam image
                frame = cv2.flip(frame, 1)

                height, width, _ = frame.shape

                # MediaPipe expects RGB input
                rgb_frame = cv2.cvtColor(
                    frame, cv2.COLOR_BGR2RGB
                )

                image = mp.Image(
                    image_format=mp.ImageFormat.SRGB,
                    data=rgb_frame
                )

                # Video mode requires increasing timestamps
                timestamp_ms = time.monotonic_ns() // 1_000_000

                result = landmarker.detect_for_video(
                    image, timestamp_ms
                )

                if result.hand_landmarks:
                    for hand in result.hand_landmarks:
                        # Convert normalized coordinates to pixels
                        points = [
                            (
                                int(point.x * width),
                                int(point.y * height)
                            )
                            for point in hand
                        ]

                        # Draw connections between landmarks
                        for start, end in HAND_CONNECTIONS:
                            cv2.line(
                                frame,
                                points[start],
                                points[end],
                                (255, 180, 0),
                                2
                            )

                        # Draw all 21 landmarks
                        for point in points:
                            cv2.circle(
                                frame,
                                point,
                                5,
                                (0, 255, 0),
                                cv2.FILLED
                            )

                        # Landmark 8 is the index fingertip
                        index_x, index_y = points[8]

                        cv2.circle(
                            frame,
                            (index_x, index_y),
                            12,
                            (0, 0, 255),
                            cv2.FILLED
                        )

                        cv2.putText(
                            frame,
                            f"Index: ({index_x}, {index_y})",
                            (index_x + 15, index_y - 15),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 0, 255),
                            2
                        )

                else:
                    cv2.putText(
                        frame,
                        "Show your hand to the camera",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 255),
                        2
                    )

                cv2.imshow("Hand Tracking", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
