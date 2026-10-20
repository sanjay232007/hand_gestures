import cv2
import mediapipe as mp

from config import (
    CAM_INDEX,
    CAM_W,
    CAM_H,
    FRAME_MARGIN,
    WINDOW_NAME,
)

from hand_tracker import create_hand_landmarker, detect_hands
from cursor_controller import CursorController
from gestures import GestureController


def main():
    landmarker = create_hand_landmarker()

    cap = cv2.VideoCapture(CAM_INDEX)
    cap.set(3, CAM_W)
    cap.set(4, CAM_H)

    cursor = CursorController()
    gestures = GestureController(cursor)

    try:
        while True:
            success, img = cap.read()

            if not success:
                break

            # Natural mirrored view
            img = cv2.flip(img, 1)

            img_rgb = cv2.cvtColor(
                img,
                cv2.COLOR_BGR2RGB,
            )

            result = detect_hands(landmarker, img_rgb)

            # Movement boundary
            cv2.rectangle(
                img,
                (FRAME_MARGIN, FRAME_MARGIN),
                (CAM_W - FRAME_MARGIN, CAM_H - FRAME_MARGIN),
                (255, 0, 255),
                2,
            )

            if result.hand_landmarks:
                for hand_lms in result.hand_landmarks:
                    lm_list = []

                    for lm in hand_lms:
                        px = int(lm.x * CAM_W)
                        py = int(lm.y * CAM_H)
                        lm_list.append((px, py))

                    # Fingertip feedback
                    for tip_id in [4, 8, 12, 16, 20]:
                        cv2.circle(
                            img,
                            lm_list[tip_id],
                            5,
                            (0, 255, 0),
                            cv2.FILLED,
                        )

                    gestures.process(img, lm_list)

            cv2.imshow(WINDOW_NAME, img)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        if gestures.is_dragging:
            import pyautogui
            pyautogui.mouseUp()

        cap.release()
        cv2.destroyAllWindows()
        landmarker.close()


if __name__ == "__main__":
    main()