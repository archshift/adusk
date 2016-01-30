import copy
from collections import deque, namedtuple
from threading import Lock

from steamcontroller import SteamController, SCStatus

from adusk import utils

InputState = namedtuple("InputState", "buttons pad_pos trigger_pos")
ButtonEvent = namedtuple("ButtonEvent", "button input_state")


class ControllerState:
    event_queue = deque()

    watched_buttons = []
    _watched_buttons_lock = Lock()

    def set_watched_buttons(self, buttons):
        with self._watched_buttons_lock:
            self.watched_buttons.clear()
            self.watched_buttons.extend(buttons)

    def get_watched_buttons(self):
        with self._watched_buttons_lock:
            return copy.deepcopy(self.watched_buttons)

    input_state = None
    _input_state_lock = Lock()

    def set_input_state(self, input_state):
        with self._input_state_lock:
            self.input_state = input_state

    def get_input_state(self):
        with self._input_state_lock:
            return copy.deepcopy(self.input_state)


class ControllerManager:
    pad_smoothing = 0.15
    trigger_smoothing = 0.15

    def __init__(self, controller_state):
        self.controller_state = controller_state

        self.prev_input_state = InputState(0, (utils.Point(0, 0), utils.Point(0, 0)), (0, 0))
        self.touch_left = utils.Point(0, 0)
        self.touch_right = utils.Point(0, 0)
        self.trigger_left = 0
        self.trigger_right = 0

    def handle_watched_buttons(self, buttons, input_state):
        for button in buttons:
            # If the individual button changed pressed status
            if input_state.buttons ^ self.prev_input_state.buttons & button:
                self.controller_state.click_queue.append(ButtonEvent(button, input_state))

    def handle_input(self, sc, sc_input):
        self.touch_left.x = utils.compute_lowpass(sc_input.lpad_x / 0x20000, self.touch_left.x, self.pad_smoothing)
        self.touch_left.y = utils.compute_lowpass(sc_input.lpad_y / 0x10000, self.touch_left.y, self.pad_smoothing)
        self.touch_right.x = utils.compute_lowpass(sc_input.rpad_x / 0x20000, self.touch_right.x, self.pad_smoothing)
        self.touch_right.y = utils.compute_lowpass(sc_input.rpad_y / 0x10000, self.touch_right.y, self.pad_smoothing)
        self.trigger_left = utils.compute_lowpass(sc_input.ltrig, self.trigger_left, self.trigger_smoothing)
        self.trigger_right = utils.compute_lowpass(sc_input.rtrig, self.trigger_right, self.trigger_smoothing)

        input_state = InputState(sc_input.buttons, (self.touch_left, self.touch_right),
                                 (self.trigger_left, self.trigger_right))

        self.prev_input_state = input_state

        self.controller_state.set_input_state(input_state)


def update(sc, sc_input, manager):
    if sc_input.status != SCStatus.INPUT:
        return
    manager.handle_input(sc, sc_input)


def input_thread(controller_state):
    manager = ControllerManager(controller_state)
    sc = SteamController(callback=update, callback_args=(manager,))
    sc.run()
