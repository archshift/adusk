from steamcontroller import SteamController, SCButtons, SCStatus, SCI_NULL
from steamcontroller.events import EventMapper
import steamcontroller.uinput as sui

from adusk import screen
from adusk import state
from adusk import utils
from adusk import vptr

import copy


def on_button_exit(evm, button, pressed):
    if not pressed:
        state.close()


def adjust_raw_x(raw_x, center_fraction, scalar=6/5):
    abs_max = 0x20000
    return utils.round_to_int(screen.width * (center_fraction + scalar * raw_x/abs_max))


def adjust_raw_y(raw_y, center_fraction, scalar=6/5):
    abs_max = 0x10000
    return utils.round_to_int(screen.height * (center_fraction + scalar * -raw_y/abs_max))


class ControllerManager:
    pad_smoothing = 0.15
    sc_input_previous = SCI_NULL

    def __init__(self):
        prev_ptrs = state.get_ptr_state()
        self.prev_ptr_left = prev_ptrs[0]
        self.prev_ptr_right = prev_ptrs[1]

        self.evm = EventMapper()
        self._map_events()

    def _map_events(self):
        self.evm.setButtonAction(SCButtons.LGRIP, sui.Keys.KEY_LEFTSHIFT)
        self.evm.setButtonAction(SCButtons.LB, sui.Keys.KEY_BACKSPACE)
        self.evm.setButtonAction(SCButtons.RB, sui.Keys.KEY_SPACE)
        self.evm.setButtonAction(SCButtons.A, sui.Keys.KEY_ENTER)
        self.evm.setButtonCallback(SCButtons.B, on_button_exit)

    def handle_pad_input(self, x, y, buttons, touch_button_mask, select_button_mask):
        if buttons & touch_button_mask:
            if buttons & select_button_mask:
                # Handle click if previous buttons did not include both `touch_button` and `select_button`
                if ~self.sc_input_previous.buttons & (touch_button_mask | select_button_mask) != 0:
                    state.gui_clicks.append((x, y))
                return state.InputState.CLICK
            else:
                return state.InputState.HOVER
        return state.InputState.INACTIVE

    def handle_input(self, sc, sc_input):
        self.evm.process(sc, sc_input)

        if self.sc_input_previous == SCI_NULL:
            self.sc_input_previous = sc_input
            return

        ptr_left_x, ptr_left_y = adjust_raw_x(sc_input.lpad_x, 1/4), adjust_raw_y(sc_input.lpad_y, 1/2)
        ptr_right_x, ptr_right_y = adjust_raw_x(sc_input.rpad_x, 3/4), adjust_raw_y(sc_input.rpad_y, 1/2)

        input_state_left = self.handle_pad_input(ptr_left_x, ptr_left_y, sc_input.buttons,
                                                 SCButtons.LPADTOUCH, SCButtons.LT)
        input_state_right = self.handle_pad_input(ptr_right_x, ptr_right_y, sc_input.buttons,
                                                  SCButtons.RPADTOUCH, SCButtons.RT)

        ptr_left = vptr.VirtualPointer(input_state_left, ptr_left_x, ptr_left_y)
        ptr_right = vptr.VirtualPointer(input_state_right, ptr_right_x, ptr_right_y)

        ptr_left.smoothen(self.prev_ptr_left, self.pad_smoothing)
        ptr_right.smoothen(self.prev_ptr_right, self.pad_smoothing)
        self.prev_ptr_left = copy.deepcopy(ptr_left)
        self.prev_ptr_right = copy.deepcopy(ptr_right)
        self.sc_input_previous = sc_input

        state.submit_ptr_state(ptr_left, ptr_right)


def update(sc, sc_input, manager):
    if sc_input.status != SCStatus.INPUT:
        return
    manager.handle_input(sc, sc_input)


def input_thread():
    manager = ControllerManager()
    sc = SteamController(callback=update, callback_args=[manager])
    sc.run()
