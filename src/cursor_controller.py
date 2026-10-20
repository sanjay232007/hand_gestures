import numpy as np
import pyautogui

from config import (
    CAM_W,
    CAM_H,
    FRAME_MARGIN,
    SCREEN_W,
    SCREEN_H,
    SMOOTH_FACTOR,
)


class CursorController:
    def __init__(self):
        self.prev_x = 0
        self.prev_y = 0

    def get_target_position(self, index_tip):
        target_x = np.interp(
            index_tip[0],
            (FRAME_MARGIN, CAM_W - FRAME_MARGIN),
            (0, SCREEN_W),
        )

        target_y = np.interp(
            index_tip[1],
            (FRAME_MARGIN, CAM_H - FRAME_MARGIN),
            (0, SCREEN_H),
        )

        curr_x = self.prev_x + (
            target_x - self.prev_x
        ) / SMOOTH_FACTOR

        curr_y = self.prev_y + (
            target_y - self.prev_y
        ) / SMOOTH_FACTOR

        return curr_x, curr_y

    def move(self, index_tip):
        curr_x, curr_y = self.get_target_position(index_tip)

        pyautogui.moveTo(curr_x, curr_y)

        self.prev_x = curr_x
        self.prev_y = curr_y

        return curr_x, curr_y