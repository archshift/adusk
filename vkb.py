import steamcontroller.uinput as sui

import screen
import state
import utils

kb = sui.Keyboard()


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
        return int(y_coord / (self.key_height + self.padding * 2))

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


def on_key_generic(virtual_kb, keycode):
    kb.pressEvent([keycode])
    kb.releaseEvent([keycode])


def on_key_shift(virtual_kb, keycode):
    return


def on_key_alt(virtual_kb, keycode):
    return


def on_key_done(virtual_kb, keycode):
    state.close()


def callback_clicks(virtual_kb):
    while len(state.gui_clicks) > 0:
        x, y = state.gui_clicks.popleft()
        key = virtual_kb.find_key(x, y)
        if key is None:
            continue
        key.callback(virtual_kb, key.keycode)