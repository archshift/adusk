from steamcontroller import SteamController, SCButtons, SCStatus
from steamcontroller.events import EventMapper
import steamcontroller.uinput as sui

import screen
import state
import vkb
import vptr

evm = None
sc_input_previous = None
kb = sui.Keyboard()


def on_button_exit(evm, btn, pressed):
    if not pressed:
        state.close()


def on_generic_press(virtual_kb, keycode):
    kb.pressEvent([keycode])
    kb.releaseEvent([keycode])


def on_shift_press(virtual_kb, keycode):
    return


def on_alt_press(virtual_kb, keycode):
    return


def on_done_press(virtual_kb, keycode):
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
    return round(screen.width * (center_fraction + scalar * raw_x/abs_max))


def adjust_raw_y(raw_y, center_fraction, scalar=6 / 5):
    abs_max = 0x10000
    return round(screen.height * (center_fraction + scalar * -raw_y/abs_max))


def update(sc, sc_input):
    global sc_input_previous

    if sc_input.status != SCStatus.INPUT:
        return

    evm.process(sc, sc_input)

    if sc_input_previous is None:
        sc_input_previous = sc_input
        return

    pressed_right, pressed_left = False, False

    ptr_left = vptr.VirtualPointer(vkb.KeyState.INACTIVE, adjust_raw_x(sc_input.lpad_x, 1 / 4),
                                   adjust_raw_y(sc_input.lpad_y, 1 / 2))
    ptr_right = vptr.VirtualPointer(vkb.KeyState.INACTIVE, adjust_raw_x(sc_input.rpad_x, 3 / 4),
                                    adjust_raw_y(sc_input.rpad_y, 1 / 2))

    key_left = virtual_kb.find_key(ptr_left.x, ptr_left.y)
    key_right = virtual_kb.find_key(ptr_right.x, ptr_right.y)

    if sc_input.buttons & SCButtons.RPADTOUCH:
        if sc_input.buttons & SCButtons.RT:
            ptr_right.state = vkb.KeyState.CLICK
            # Handle click if previous buttons did not include both RPADTOUCH and RT
            pressed_right = ~sc_input_previous.buttons & (SCButtons.RPADTOUCH | SCButtons.RT) != 0
        else:
            ptr_right.state = vkb.KeyState.HOVER

    if sc_input.buttons & SCButtons.LPADTOUCH:
        if sc_input.buttons & SCButtons.LT:
            ptr_left.state = vkb.KeyState.CLICK
            # Handle click if previous buttons did not include both LPADTOUCH and LT
            pressed_left = ~sc_input_previous.buttons & (SCButtons.LPADTOUCH | SCButtons.LT) != 0
        else:
            ptr_left.state = vkb.KeyState.HOVER

    if pressed_left and (key_left is not None):
        key_left.callback(virtual_kb, key_left.keycode)
    if pressed_right and (key_right is not None):
        key_right.callback(virtual_kb, key_right.keycode)

    sc_input_previous = sc_input

    state.submit_gui_state(state.GuiState(virtual_kb, ptr_left, ptr_right))


virtual_kb = vkb.VirtualKeyboard([
    [
        vkb.KeyButton('1', sui.Keys.KEY_1, on_generic_press),
        vkb.KeyButton('2', sui.Keys.KEY_2, on_generic_press),
        vkb.KeyButton('3', sui.Keys.KEY_3, on_generic_press),
        vkb.KeyButton('4', sui.Keys.KEY_4, on_generic_press),
        vkb.KeyButton('5', sui.Keys.KEY_5, on_generic_press),
        vkb.KeyButton('6', sui.Keys.KEY_6, on_generic_press),
        vkb.KeyButton('7', sui.Keys.KEY_7, on_generic_press),
        vkb.KeyButton('8', sui.Keys.KEY_8, on_generic_press),
        vkb.KeyButton('9', sui.Keys.KEY_9, on_generic_press),
        vkb.KeyButton('0', sui.Keys.KEY_0, on_generic_press),
        vkb.KeyButton('-', sui.Keys.KEY_MINUS, on_generic_press),
        vkb.KeyButton('\u2190', sui.Keys.KEY_BACKSPACE, on_generic_press),
    ], [
        vkb.KeyButton('q', sui.Keys.KEY_Q, on_generic_press),
        vkb.KeyButton('w', sui.Keys.KEY_W, on_generic_press),
        vkb.KeyButton('e', sui.Keys.KEY_E, on_generic_press),
        vkb.KeyButton('r', sui.Keys.KEY_R, on_generic_press),
        vkb.KeyButton('t', sui.Keys.KEY_T, on_generic_press),
        vkb.KeyButton('y', sui.Keys.KEY_Y, on_generic_press),
        vkb.KeyButton('u', sui.Keys.KEY_U, on_generic_press),
        vkb.KeyButton('i', sui.Keys.KEY_I, on_generic_press),
        vkb.KeyButton('o', sui.Keys.KEY_O, on_generic_press),
        vkb.KeyButton('p', sui.Keys.KEY_P, on_generic_press),
        vkb.KeyButton('\\', sui.Keys.KEY_BACKSLASH, on_generic_press),
    ], [
        vkb.KeyButton('Alt', 0, on_alt_press, 0.9),
        vkb.KeyButton('a', sui.Keys.KEY_A, on_generic_press),
        vkb.KeyButton('s', sui.Keys.KEY_S, on_generic_press),
        vkb.KeyButton('d', sui.Keys.KEY_D, on_generic_press),
        vkb.KeyButton('f', sui.Keys.KEY_F, on_generic_press),
        vkb.KeyButton('g', sui.Keys.KEY_G, on_generic_press),
        vkb.KeyButton('h', sui.Keys.KEY_H, on_generic_press),
        vkb.KeyButton('j', sui.Keys.KEY_J, on_generic_press),
        vkb.KeyButton('k', sui.Keys.KEY_K, on_generic_press),
        vkb.KeyButton('l', sui.Keys.KEY_L, on_generic_press),
        vkb.KeyButton(';', sui.Keys.KEY_SEMICOLON, on_generic_press),
        vkb.KeyButton('\'', sui.Keys.KEY_APOSTROPHE, on_generic_press),
        vkb.KeyButton('\u21B5', sui.Keys.KEY_ENTER, on_generic_press, 1.7),
    ], [
        vkb.KeyButton('\u2191', sui.Keys.KEY_LEFTSHIFT, on_shift_press, 1.2),
        vkb.KeyButton('z', sui.Keys.KEY_Z, on_generic_press),
        vkb.KeyButton('x', sui.Keys.KEY_X, on_generic_press),
        vkb.KeyButton('c', sui.Keys.KEY_C, on_generic_press),
        vkb.KeyButton('v', sui.Keys.KEY_V, on_generic_press),
        vkb.KeyButton('b', sui.Keys.KEY_B, on_generic_press),
        vkb.KeyButton('n', sui.Keys.KEY_N, on_generic_press),
        vkb.KeyButton('m', sui.Keys.KEY_M, on_generic_press),
        vkb.KeyButton(',', sui.Keys.KEY_COMMA, on_generic_press),
        vkb.KeyButton('.', sui.Keys.KEY_DOT, on_generic_press),
        vkb.KeyButton('/', sui.Keys.KEY_SLASH, on_generic_press),
        vkb.KeyButton('?', sui.Keys.KEY_QUESTION, on_generic_press),
        vkb.KeyButton('\u2191', sui.Keys.KEY_RIGHTSHIFT, on_shift_press, 1.2),
    ], [
        vkb.KeyButton(' ', sui.Keys.KEY_SPACE, on_generic_press),
        vkb.KeyButton('Done', 0, on_done_press, 0.3),
    ]
])


def input_thread():
    sc = SteamController(callback=update)
    sc.run()
