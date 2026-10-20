
import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math
import time

# -------------------- MOUSE SETTINGS --------------------

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = True  # Move mouse to top-left corner for emergency stop

screen_w, screen_h = pyautogui.size()

# -------------------- WEBCAM SETTINGS --------------------

cam_w, cam_h = 640, 480
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, cam_w)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_h)

# -------------------- MEDIAPIPE SETTINGS --------------------

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# -------------------- CURSOR SETTINGS --------------------

frame_margin = 80
smooth_factor = 5

prev_x = None
prev_y = None

# Gesture thresholds in webcam pixels.
# Adjust these if your gestures are not detected.
click_threshold = 40
drag_threshold = 35

# -------------------- GESTURE STATE --------------------

is_dragging = False

last_left_click = 0.0
last_right_click = 0.0

click_cooldown = 0.35

left_gesture_active = False
right_gesture_active = False

# Scroll only when the hand moves vertically while
# the scroll gesture is held.
previous_scroll_y = None
scroll_threshold = 15
last_scroll_time = 0.0
scroll_cooldown = 0.08

# -------------------- HELPER FUNCTIONS --------------------

def get_distance(p1, p2):
    return math.hypot(
        p2[0] - p1[0],
        p2[1] - p1[1]
    )


def clamp(value, minimum, maximum):
    return max(minimum, min(int(value), maximum))


# -------------------- MAIN LOOP --------------------

try:
    while True:
        success, img = cap.read()

        if not success:
            break

        img = cv2.flip(img, 1)
        img_h, img_w = img.shape[:2]

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        cv2.rectangle(
            img,
            (frame_margin, frame_margin),
            (img_w - frame_margin, img_h - frame_margin),
            (255, 0, 255),
            2
        )

        status = "No hand detected"
        now = time.monotonic()

        if results.multi_hand_landmarks:
            hand_lms = results.multi_hand_landmarks[0]

            mp_draw.draw_landmarks(
                img,
                hand_lms,
                mp_hands.HAND_CONNECTIONS
            )

            lm_list = [
                (
                    int(lm.x * img_w),
                    int(lm.y * img_h)
                )
                for lm in hand_lms.landmark
            ]

            thumb_tip = lm_list[4]
            index_tip = lm_list[8]
            middle_tip = lm_list[12]
            ring_tip = lm_list[16]

            # Finger-up detection
            index_up = lm_list[8][1] < lm_list[6][1]
            middle_up = lm_list[12][1] < lm_list[10][1]
            ring_up = lm_list[16][1] < lm_list[14][1]
            pinky_up = lm_list[20][1] < lm_list[18][1]

            # Map fingertip to screen coordinates.
            # Clamp the values to the actual screen bounds.
            target_x = np.interp(
                index_tip[0],
                (frame_margin, img_w - frame_margin),
                (0, screen_w - 1)
            )

            target_y = np.interp(
                index_tip[1],
                (frame_margin, img_h - frame_margin),
                (0, screen_h - 1)
            )

            target_x = clamp(target_x, 0, screen_w - 1)
            target_y = clamp(target_y, 0, screen_h - 1)

            # Initialize at the detected position to avoid
            # an initial jump from (0, 0).
            if prev_x is None or prev_y is None:
                prev_x = target_x
                prev_y = target_y

            curr_x = prev_x + (target_x - prev_x) / smooth_factor
            curr_y = prev_y + (target_y - prev_y) / smooth_factor

            curr_x = clamp(curr_x, 0, screen_w - 1)
            curr_y = clamp(curr_y, 0, screen_h - 1)

            # Gesture distances
            index_middle_dist = get_distance(
                index_tip, middle_tip
            )

            thumb_middle_dist = get_distance(
                thumb_tip, middle_tip
            )

            thumb_index_dist = get_distance(
                thumb_tip, index_tip
            )

            # Define gestures
            scroll_gesture = (
                index_up
                and middle_up
                and ring_up
                and not pinky_up
            )

            right_gesture = (
                thumb_middle_dist < click_threshold
                and index_up
            )

            left_gesture = (
                index_up
                and middle_up
                and not ring_up
                and index_middle_dist < click_threshold
            )

            drag_gesture = (
                thumb_index_dist < drag_threshold
                and not middle_up
                and not scroll_gesture
                and not right_gesture
            )

            # ---------------- SCROLL ----------------

            if scroll_gesture:
                status = "SCROLL MODE"

                # Do not accidentally drag while scrolling.
                if is_dragging:
                    pyautogui.mouseUp()
                    is_dragging = False

                # Reset click edge states while changing modes.
                left_gesture_active = False
                right_gesture_active = False

                current_scroll_y = index_tip[1]

                if previous_scroll_y is not None:
                    delta_y = previous_scroll_y - current_scroll_y

                    if (
                        abs(delta_y) >= scroll_threshold
                        and now - last_scroll_time >= scroll_cooldown
                    ):
                        # Finger moves up = scroll up.
                        # Finger moves down = scroll down.
                        scroll_amount = 2 if delta_y > 0 else -2

                        pyautogui.scroll(scroll_amount)
                        last_scroll_time = now

                previous_scroll_y = current_scroll_y

                cv2.circle(
                    img, index_tip, 12, (255, 0, 255), cv2.FILLED
                )

            else:
                previous_scroll_y = None

                # ---------------- RIGHT CLICK ----------------

                if right_gesture:
                    status = "RIGHT CLICK"

                    if is_dragging:
                        pyautogui.mouseUp()
                        is_dragging = False

                    if (
                        not right_gesture_active
                        and now - last_right_click >= click_cooldown
                    ):
                        pyautogui.rightClick()
                        last_right_click = now

                    right_gesture_active = True
                    left_gesture_active = False

                    cv2.circle(
                        img, middle_tip, 12, (255, 0, 0), cv2.FILLED
                    )

                # ---------------- LEFT CLICK ----------------

                elif left_gesture:
                    status = "LEFT CLICK"

                    if is_dragging:
                        pyautogui.mouseUp()
                        is_dragging = False

                    if (
                        not left_gesture_active
                        and now - last_left_click >= click_cooldown
                    ):
                        pyautogui.click()
                        last_left_click = now

                    left_gesture_active = True
                    right_gesture_active = False

                    cv2.circle(
                        img, index_tip, 12, (0, 0, 255), cv2.FILLED
                    )

                # ---------------- DRAG ----------------

                elif drag_gesture:
                    status = "DRAGGING"

                    if not is_dragging:
                        pyautogui.moveTo(curr_x, curr_y)
                        pyautogui.mouseDown()
                        is_dragging = True

                    pyautogui.moveTo(curr_x, curr_y)

                    prev_x = curr_x
                    prev_y = curr_y

                    left_gesture_active = False
                    right_gesture_active = False

                    cv2.circle(
                        img, index_tip, 12, (0, 255, 255), cv2.FILLED
                    )

                # ---------------- CURSOR MOVEMENT ----------------

                else:
                    status = "MOVING"

                    if is_dragging:
                        pyautogui.mouseUp()
                        is_dragging = False

                    left_gesture_active = False
                    right_gesture_active = False

                    # Preserve your index-finger movement gesture.
                    if index_up and not middle_up and not ring_up:
                        pyautogui.moveTo(curr_x, curr_y)

                        prev_x = curr_x
                        prev_y = curr_y

                        cv2.circle(
                            img, index_tip, 10, (0, 255, 0), cv2.FILLED
                        )

        else:
            # Reset gesture states when the hand disappears.
            left_gesture_active = False
            right_gesture_active = False
            previous_scroll_y = None

            if is_dragging:
                pyautogui.mouseUp()
                is_dragging = False

        # Display current gesture status.
        cv2.putText(
            img,
            status,
            (10, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            img,
            "Press Q to quit",
            (10, img_h - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.imshow("Hand Gesture Cursor Controller", img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    # Always release mouse buttons and camera resources.
    try:
        pyautogui.mouseUp()
    except Exception:
        pass

    cap.release()
    hands.close()
    cv2.destroyAllWindows()
