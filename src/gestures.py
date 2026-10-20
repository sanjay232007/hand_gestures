import math
import cv2
import pyautogui

from config import (
    CAM_H,
    PINCH_THRESHOLD,
)


def get_distance(p1, p2):
    return math.hypot(
        p2[0] - p1[0],
        p2[1] - p1[1],
    )


class GestureController:
    def __init__(self, cursor):
        self.cursor = cursor
        self.is_dragging = False

    def process(self, img, lm_list):
        if not lm_list:
            return

        thumb_tip = lm_list[4]
        index_tip = lm_list[8]
        middle_tip = lm_list[12]

        index_up = lm_list[8][1] < lm_list[6][1]
        middle_up = lm_list[12][1] < lm_list[10][1]
        ring_up = lm_list[16][1] < lm_list[14][1]
        pinky_up = lm_list[20][1] < lm_list[18][1]

        curr_x, curr_y = self.cursor.get_target_position(index_tip)

        # 1. MOVE CURSOR: Only Index Finger Up
        if index_up and not middle_up and not ring_up:
            pyautogui.moveTo(curr_x, curr_y)

            cv2.circle(
                img, index_tip, 10,
                (255, 0, 0), cv2.FILLED
            )

            self.cursor.prev_x = curr_x
            self.cursor.prev_y = curr_y

        # 2. LEFT CLICK: Index & Middle Up, tapped together
        if index_up and middle_up and not ring_up:
            if get_distance(index_tip, middle_tip) < 30:
                cv2.circle(
                    img, index_tip, 12,
                    (0, 0, 255), cv2.FILLED
                )

                pyautogui.click()
                pyautogui.sleep(0.2)

        # 3. RIGHT CLICK: Thumb & Middle Pinch
        if get_distance(thumb_tip, middle_tip) < 30 and index_up:
            cv2.circle(
                img, middle_tip, 12,
                (255, 255, 0), cv2.FILLED
            )

            pyautogui.rightClick()
            pyautogui.sleep(0.3)

        # 4. DRAG / SELECT: Pinch Thumb & Index
        if (
            get_distance(thumb_tip, index_tip) < PINCH_THRESHOLD
            and not middle_up
        ):
            if not self.is_dragging:
                pyautogui.mouseDown()
                self.is_dragging = True

            pyautogui.moveTo(curr_x, curr_y)

            self.cursor.prev_x = curr_x
            self.cursor.prev_y = curr_y

            cv2.circle(
                img, index_tip, 12,
                (0, 255, 255), cv2.FILLED
            )

        else:
            if self.is_dragging:
                pyautogui.mouseUp()
                self.is_dragging = False

        # 5. SCROLL: Index, Middle, Ring Up
        if index_up and middle_up and ring_up and not pinky_up:
            if index_tip[1] < CAM_H // 2 - 40:
                pyautogui.scroll(40)

            elif index_tip[1] > CAM_H // 2 + 40:
                pyautogui.scroll(-40)