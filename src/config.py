import pyautogui

# PyAutoGUI safety settings
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

SCREEN_W, SCREEN_H = pyautogui.size()

# Webcam
CAM_W = 640
CAM_H = 480
CAM_INDEX = 0

# Cursor
FRAME_MARGIN = 100
SMOOTH_FACTOR = 5

# Gesture thresholds
PINCH_THRESHOLD = 30
LEFT_CLICK_THRESHOLD = 30
RIGHT_CLICK_THRESHOLD = 30

# MediaPipe confidence
MIN_DETECTION_CONFIDENCE = 0.7
MIN_PRESENCE_CONFIDENCE = 0.7

# Model
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/1/"
    "hand_landmarker.task"
)

# Window
WINDOW_NAME = "Hand Gesture Cursor Controller"