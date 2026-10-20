import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math
import os
import urllib.request

# Safety settings for PyAutoGUI
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False
screen_w, screen_h = pyautogui.size()

# 1. Download the required modern MediaPipe model automatically
model_path = "hand_landmarker.task"
if not os.path.exists(model_path):
    print("Downloading MediaPipe Hand Tracking model (this only happens once)...")
    url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
    urllib.request.urlretrieve(url, model_path)
    print("Download complete!")

# 2. Configure the new Tasks API
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7
)
landmarker = HandLandmarker.create_from_options(options)

# 3. Webcam Setup
cam_w, cam_h = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, cam_w)
cap.set(4, cam_h)

# Smoothing and Bounding Box variables
frame_margin = 100
smooth_factor = 5
prev_x, prev_y = 0, 0
is_dragging = False

def get_distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

while True:
    success, img = cap.read()
    if not success:
        break

    # Flip image horizontally for natural mirroring
    img = cv2.flip(img, 1)
    
    # MediaPipe Tasks requires a specific Image object
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
    
    # Process the frame
    result = landmarker.detect(mp_image)

    # Draw active movement boundary box
    cv2.rectangle(img, (frame_margin, frame_margin), (cam_w - frame_margin, cam_h - frame_margin), (255, 0, 255), 2)

    if result.hand_landmarks:
        for hand_lms in result.hand_landmarks:
            lm_list = []
            
            # Extract coordinates for all 21 landmarks
            for lm in hand_lms:
                px, py = int(lm.x * cam_w), int(lm.y * cam_h)
                lm_list.append((px, py))

            # Draw circles on fingertips for visual feedback
            for tip_id in [4, 8, 12, 16, 20]:
                cv2.circle(img, lm_list[tip_id], 5, (0, 255, 0), cv2.FILLED)

            if lm_list:
                thumb_tip = lm_list[4]
                index_tip = lm_list[8]
                middle_tip = lm_list[12]
                ring_tip = lm_list[16]
                pinky_tip = lm_list[20]

                # Check which fingers are UP (comparing tip Y to lower PIP joint Y)
                index_up = lm_list[8][1] < lm_list[6][1]
                middle_up = lm_list[12][1] < lm_list[10][1]
                ring_up = lm_list[16][1] < lm_list[14][1]
                pinky_up = lm_list[20][1] < lm_list[18][1]

                # Convert Index Finger position to full screen coordinates
                target_x = np.interp(index_tip[0], (frame_margin, cam_w - frame_margin), (0, screen_w))
                target_y = np.interp(index_tip[1], (frame_margin, cam_h - frame_margin), (0, screen_h))

                curr_x = prev_x + (target_x - prev_x) / smooth_factor
                curr_y = prev_y + (target_y - prev_y) / smooth_factor

                # 1. MOVE CURSOR: Only Index Finger Up
                if index_up and not middle_up and not ring_up:
                    pyautogui.moveTo(curr_x, curr_y)
                    cv2.circle(img, index_tip, 10, (255, 0, 0), cv2.FILLED)
                    prev_x, prev_y = curr_x, curr_y

                # 2. LEFT CLICK: Index & Middle Up, tapped together
                if index_up and middle_up and not ring_up:
                    if get_distance(index_tip, middle_tip) < 30:
                        cv2.circle(img, index_tip, 12, (0, 0, 255), cv2.FILLED)
                        pyautogui.click()
                        pyautogui.sleep(0.2)

                # 3. RIGHT CLICK: Thumb & Middle Pinch
                if get_distance(thumb_tip, middle_tip) < 30 and index_up:
                    cv2.circle(img, middle_tip, 12, (255, 255, 0), cv2.FILLED)
                    pyautogui.rightClick()
                    pyautogui.sleep(0.3)

                # 4. DRAG / SELECT: Pinch Thumb & Index
                if get_distance(thumb_tip, index_tip) < 30 and not middle_up:
                    if not is_dragging:
                        pyautogui.mouseDown()
                        is_dragging = True
                    pyautogui.moveTo(curr_x, curr_y)
                    prev_x, prev_y = curr_x, curr_y
                    cv2.circle(img, index_tip, 12, (0, 255, 255), cv2.FILLED)
                else:
                    if is_dragging:
                        pyautogui.mouseUp()
                        is_dragging = False

                # 5. SCROLL: Index, Middle, Ring Up
                if index_up and middle_up and ring_up and not pinky_up:
                    if index_tip[1] < cam_h // 2 - 40:
                        pyautogui.scroll(40)
                    elif index_tip[1] > cam_h // 2 + 40:
                        pyautogui.scroll(-40)

    cv2.imshow("Hand Gesture Cursor Controller", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()