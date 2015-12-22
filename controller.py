from steamcontroller import SteamController, SCButtons, SCStatus
from steamcontroller.events import EventMapper
import steamcontroller.uinput as sui

import screen
import state
import utils
import vptr

evm = None
sc_input_previous = None


def on_button_exit(evm, btn, pressed):
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


def update(sc, sc_input):
    global sc_input_previous

    if sc_input.status != SCStatus.INPUT:
        return

    evm.process(sc, sc_input)

    if sc_input_previous is None:
        sc_input_previous = sc_input
        return

    ptr_left = vptr.VirtualPointer(state.InputState.INACTIVE, adjust_raw_x(sc_input.lpad_x, 1 / 4),
                                   adjust_raw_y(sc_input.lpad_y, 1 / 2))
    ptr_right = vptr.VirtualPointer(state.InputState.INACTIVE, adjust_raw_x(sc_input.rpad_x, 3 / 4),
                                    adjust_raw_y(sc_input.rpad_y, 1 / 2))

    if sc_input.buttons & SCButtons.RPADTOUCH:
        if sc_input.buttons & SCButtons.RT:
            ptr_right.state = state.InputState.CLICK
            # Handle click if previous buttons did not include both RPADTOUCH and RT
            if ~sc_input_previous.buttons & (SCButtons.RPADTOUCH | SCButtons.RT) != 0:
                state.gui_clicks.append((ptr_right.x, ptr_right.y))
        else:
            ptr_right.state = state.InputState.HOVER

    if sc_input.buttons & SCButtons.LPADTOUCH:
        if sc_input.buttons & SCButtons.LT:
            ptr_left.state = state.InputState.CLICK
            # Handle click if previous buttons did not include both LPADTOUCH and LT
            if ~sc_input_previous.buttons & (SCButtons.LPADTOUCH | SCButtons.LT) != 0:
                state.gui_clicks.append((ptr_left.x, ptr_left.y))
        else:
            ptr_left.state = state.InputState.HOVER

    sc_input_previous = sc_input

    state.submit_ptr_state(state.PtrState(ptr_left, ptr_right))


def input_thread():
    sc = SteamController(callback=update)
    sc.run()
