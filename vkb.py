from enum import IntEnum
import math

import screen
import utils


class KeyState(IntEnum):
    INACTIVE = 0
    HOVER = 1
    CLICK = 2


class VirtualKeyboard:
    padding = 3
    key_width = []
    key_height = 0

    def __init__(self, keys):
        self.keys = keys
        self.key_rows = len(keys)
        self.update_dimensions()

    def _uniform_key_width(self, row):
        unpadded_width = screen.width - (len(self.keys[row]) * self.padding * 2)
        weights_total = 0
        for key in self.keys[row]:
            weights_total += key.width_weight

        return unpadded_width / weights_total

    def _uniform_key_height(self):
        return (screen.height - (self.key_rows * self.padding * 2)) / self.key_rows

    def update_dimensions(self):
        self.key_height = self._uniform_key_height()
        self.key_width = []
        for i in range(0, self.key_rows):
            self.key_width.append(self._uniform_key_width(i))

    def find_key_row(self, y_coord):
        return math.floor(y_coord / (self.key_height + self.padding * 2))

    def find_key(self, x_coord, y_coord):
        i_row = self.find_key_row(y_coord)
        i_row = utils.clamp(i_row, 0, self.key_rows - 1)

        iterated_x = 0
        for key in self.keys[i_row]:
            adjusted_key_width = key.width_weight * self.key_width[i_row]
            iterated_x += adjusted_key_width + self.padding * 2
            if x_coord < iterated_x:
                return key
        return None


class KeyButton:
    def __init__(self, str, keycode, callback, width_weight=1.0):
        self.str = str
        self.keycode = keycode
        self.callback = callback
        self.width_weight = width_weight
