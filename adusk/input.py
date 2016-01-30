from enum import Enum
from threading import Thread

from steamcontroller.events import SCButtons

from adusk import controller
from adusk import screen
from adusk import utils
from adusk import vptr


class InputModeVkb:
    def on_select(self, button, input_state):
        pass

    def on_send_keycode(self, button, input_state):
        pass

    def on_quit(self, button, input_state):
        pass

    watched_buttons = {
        SCButtons.LT: on_select,
        SCButtons.RT: on_select,
        SCButtons.LB: on_send_keycode,
        SCButtons.RB: on_send_keycode,
        SCButtons.A: on_send_keycode,
        SCButtons.B: on_quit,
        SCButtons.LGRIP: on_send_keycode
    }

    def __init__(self):
        pass

    @staticmethod
    def adjust_raw_x(raw_x, center_fraction, scalar=6/5):
        return utils.round_to_int(screen.size.w * (center_fraction + scalar * raw_x))

    @staticmethod
    def adjust_raw_y(raw_y, center_fraction, scalar=6/5):
        return utils.round_to_int(screen.size.h * (center_fraction + scalar * -raw_y))

    def handle_buttons(self, event_queue):
        while len(event_queue) > 0:
            event = event_queue.popleft()
            self.watched_buttons[event.button](event.button, event.input_state)

    def handle(self, controller_state):
        input_state = controller_state.get_input_state()
        touch_left, touch_right = input_state.pad_pos

        ptr_left_coords = utils.CoordFraction.from_absolute(self.adjust_raw_x(touch_left.x, 1/4),
                                                            self.adjust_raw_y(touch_left.y, 1/2),
                                                            screen.size)
        ptr_right_coords = utils.CoordFraction.from_absolute(self.adjust_raw_x(touch_right.x, 3/4),
                                                             self.adjust_raw_y(touch_right.y, 1/2),
                                                             screen.size)

        touch_left = vptr.VirtualPointer(vptr.VirtualPointer.State.INACTIVE, ptr_left_coords)
        touch_right = vptr.VirtualPointer(vptr.VirtualPointer.State.INACTIVE, ptr_right_coords)
        pass

    def get_watched_buttons(self):
        return self.watched_buttons.keys()


class InputModeWindow:
    def __init__(self, controller_state):
        self.controller_state = controller_state

    def handle(self):
        pass


class InputHandler:
    def __init__(self):
        self.controller_state = controller.ControllerState()
        # controller_state.set_pad_pos(
        #         vptr.VirtualPointer(vptr.VirtualPointer.State.INACTIVE, utils.CoordFraction(1/4, 1/2)),
        #         vptr.VirtualPointer(vptr.VirtualPointer.State.INACTIVE, utils.CoordFraction(3/4, 1/2))
        # )

        self.active_mode_id = -1
        self.next_mode_id = 0

        self.input_modes = {
            self.Mode.VKB_INPUT: InputModeVkb(controller_state),
            self.Mode.WINDOW_MGMT: InputModeWindow(controller_state),
        }
        self.activate_mode(active_mode)

        self.sc_thread = Thread(target=controller.input_thread, args=(controller_state,), daemon=True)
        self.sc_thread.start()


    def add_mode(self, input_mode):
        while self.next_mode_id not in self.input_modes:
            self.next_mode_id += 1

        self.input_modes[self.next_mode_id] = input_mode
        self.next_mode_id += 1

    def del_mode(self, mode_id):
        del self.input_modes[mode_id]
        if self.active_mode_id == mode_id:
            self.active_mode_id = -1

    def activate_mode(self, mode_id):
        self.active_mode_id = mode_id
        self.controller_state.set_watched_buttons(self.input_modes[mode_id].get_watched_buttons())

    def handle(self):
        self.input_modes[self.active_mode_id].handle()
