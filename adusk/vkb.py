from collections import namedtuple

import steamcontroller.uinput as sui

from adusk import config
from adusk import screen
from adusk import state
from adusk import utils
from adusk import vptr

kb = sui.Keyboard()


class VirtualKeyboard:
    padding_inner = 3
    padding_outer = 10
    key_width = []
    key_height = 0

    text_color = (255, 255, 255)

    key_color = {
        vptr.VirtualPointer.State.INACTIVE: (0x19, 0x3d, 0x55),
        vptr.VirtualPointer.State.HOVER: (0x25, 0x5f, 0x7e),
        vptr.VirtualPointer.State.CLICK: (0x7b, 0xb8, 0xd8),
    }

    KeyLayout = namedtuple("KeyLayout", "x y w h row col")

    def __init__(self, keys):
        self.keys = keys
        self.key_rows = len(keys)
        self.update_dimensions()

    def _uniform_key_width(self, row):
        unpadded_width = screen.size.w - self.padding_outer * 2 - (len(self.keys[row]) * self.padding_inner * 2)
        weights_total = 0
        for key in self.keys[row]:
            weights_total += key.width_weight

        return unpadded_width / weights_total

    def _uniform_key_height(self):
        return (screen.size.h - self.padding_outer * 2 - (self.key_rows * self.padding_inner * 2)) / self.key_rows

    def update_dimensions(self):
        self.key_height = self._uniform_key_height()
        self.key_width = []
        for i in range(0, self.key_rows):
            self.key_width.append(self._uniform_key_width(i))

    def find_key_row(self, y_coord):
        return int((y_coord - self.padding_outer) / (self.key_height + self.padding_inner * 2))

    def find_key(self, x_coord, y_coord):
        i_row = self.find_key_row(y_coord)
        i_row = utils.clamp(i_row, 0, self.key_rows - 1)

        iterated_x = self.padding_outer
        for key in self.keys[i_row]:
            adjusted_key_width = key.width_weight * self.key_width[i_row]
            iterated_x += adjusted_key_width + self.padding_inner * 2
            if x_coord < iterated_x:
                return key
        return None

    def gen_key_layouts(self):
        iterated_y = self.padding_outer

        for i_row, row in enumerate(self.keys):
            iterated_x = self.padding_outer

            for i_key, key in enumerate(row):
                adj_x = iterated_x + self.padding_inner
                adj_y = iterated_y + self.padding_inner
                adj_w = key.width_weight * self.key_width[i_row]
                adj_h = self.key_height

                yield self.KeyLayout(utils.round_to_int(adj_x), utils.round_to_int(adj_y),
                                     utils.round_to_int(adj_w), utils.round_to_int(adj_h),
                                     i_row, i_key)

                iterated_x += adj_w + self.padding_inner * 2
            iterated_y += self.key_height + self.padding_inner * 2


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


class VirtualKeyboardConfig(config.ObjectConfig):
    @staticmethod
    def decode_keycode(str):
        try:
            return sui.Keys[str]
        except KeyError:
            assert False, "Invalid keycode `{}`".format(str)

    @staticmethod
    def decode_callback(str):
        if str == "generic":
            pass
        elif str == "shift":
            return on_key_shift
        elif str == "alt":
            return on_key_alt
        elif str == "done":
            return on_key_done
        else:
            assert False, "Invalid behavior `{}`".format(str)
        return on_key_generic

    def construct(self):
        keys = []

        yaml_rows = self.objects["keys"]

        for yaml_row in yaml_rows:
            row = []
            for yaml_key in yaml_row:
                label = "" if "label" not in yaml_key else yaml_key["label"]
                keycode = 0 if "keycode" not in yaml_key else self.decode_keycode(yaml_key["keycode"])
                behavior = "generic" if "behavior" not in yaml_key else yaml_key["behavior"]
                width_weight = 1.0 if "width_weight" not in yaml_key else yaml_key["width_weight"]

                callback = self.decode_callback(behavior)
                row.append(KeyButton(label, keycode, callback, width_weight))

            keys.append(row)
        return VirtualKeyboard(keys)


def process_click_queue(virtual_kb, queue):
    while len(queue) > 0:
        x, y = queue.popleft().to_absolute()
        key = virtual_kb.find_key(x, y)
        if key is None:
            continue
        key.callback(virtual_kb, key.keycode)
