import urllib.request
from pathlib import Path

import mediapipe as mp

from config import (
    MIN_DETECTION_CONFIDENCE,
    MIN_PRESENCE_CONFIDENCE,
    MODEL_URL,
)

PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODEL_DIR / "hand_landmarker.task"


def create_hand_landmarker():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    if not MODEL_PATH.exists():
        print("Downloading MediaPipe Hand Tracking model...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("Download complete!")

    options = mp.tasks.vision.HandLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(
            model_asset_path=str(MODEL_PATH)
        ),
        running_mode=mp.tasks.vision.RunningMode.IMAGE,
        num_hands=1,
        min_hand_detection_confidence=MIN_DETECTION_CONFIDENCE,
        min_hand_presence_confidence=MIN_PRESENCE_CONFIDENCE,
    )

    return mp.tasks.vision.HandLandmarker.create_from_options(options)


def detect_hands(landmarker, image):
    image_rgb = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=image,
    )

    return landmarker.detect(image_rgb)