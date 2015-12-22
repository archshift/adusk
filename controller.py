from steamcontroller import SteamController, SCButtons, SCStatus
from steamcontroller.events import EventMapper
import steamcontroller.uinput as sui

import screen
import state
import utils
import vptr

evm = None
sc_input_previous = None


def on_button_exit(evm, button, pressed):
    if not pressed:
        state.close()


def create_event_mapper():
    global evm
    evm = EventMapper()
    evm.setButtonAction(SCButtons.LGRIP, sui.Keys.KEY_LEFTSHIFT)
    evm.setButtonAction(SCButtons.LB, sui.Keys.KEY_BACKSPACE)
    evm.setButtonAction(SCButtons.RB, sui.Keys.KEY_SPACE)
    evm.setButtonAction(SCButtons.A, sui.Keys.KEY_ENTER)
    evm.setButtonCallback(SCButtons.B, on_button_exit)


def adjust_raw_x(raw_x, center_fraction, scalar=6 / 5):
    abs_max = 0x20000
    return utils.round_to_int(screen.width * (center_fraction + scalar * raw_x/abs_max))


def adjust_raw_y(raw_y, center_fraction, scalar=6 / 5):
    abs_max = 0x10000
    return utils.round_to_int(screen.height * (center_fraction + scalar * -raw_y/abs_max))


def handle_pad_input(x, y, buttons, prev_buttons, touch_button_mask, select_button_mask):
    if buttons & touch_button_mask:
        if buttons & select_button_mask:
            # Handle click if previous buttons did not include both `touch_button` and `select_button`
            if ~prev_buttons & (touch_button_mask | select_button_mask) != 0:
                state.gui_clicks.append((x, y))
            return state.InputState.CLICK
        else:
            return state.InputState.HOVER
    return state.InputState.INACTIVE


def update(sc, sc_input):
    global sc_input_previous

    if sc_input.status != SCStatus.INPUT:
        return

    evm.process(sc, sc_input)

    if sc_input_previous is None:
        sc_input_previous = sc_input
        return

    ptr_left_x, ptr_left_y = adjust_raw_x(sc_input.lpad_x, 1/4), adjust_raw_y(sc_input.lpad_y, 1/2)
    ptr_right_x, ptr_right_y = adjust_raw_x(sc_input.rpad_x, 3/4), adjust_raw_y(sc_input.rpad_y, 1/2)

    ptr_left_state = handle_pad_input(ptr_left_x, ptr_left_y, sc_input.buttons, sc_input_previous.buttons,
                                      SCButtons.LPADTOUCH, SCButtons.LT)
    ptr_right_state = handle_pad_input(ptr_right_x, ptr_right_y, sc_input.buttons, sc_input_previous.buttons,
                                       SCButtons.RPADTOUCH, SCButtons.RT)

    ptr_left = vptr.VirtualPointer(ptr_left_state, ptr_left_x, ptr_left_y)
    ptr_right = vptr.VirtualPointer(ptr_right_state, ptr_right_x, ptr_right_y)

    sc_input_previous = sc_input

    state.submit_ptr_state(state.PtrState(ptr_left, ptr_right))


def input_thread():
    sc = SteamController(callback=update)
    sc.run()
