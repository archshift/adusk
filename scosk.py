#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Steam Controller On-Screen Keyboard - Proof of Concept"""

from steamcontroller import *
import steamcontroller.uinput as sui 
from steamcontroller.events import EventMapper, Pos
import math
import sys
import pygame

pygame.init()
screen_width, screen_height = 640, 320 # Screen Size <dim>
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill((0x0f, 0x28, 0x3c))
sc_input_previous = SCI_NULL

kb = sui.Keyboard()


def clamp(i, min_val, max_val):
    return max(min_val, min(max_val, i))


def render_key(txt, x, y, w, h, key_state):
    if key_state != KeyState.INACTIVE:
        pygame.draw.rect(screen, (0x25, 0x5f, 0x7e), (x, y, w, h))
    else:
        pygame.draw.rect(screen, (0x19, 0x3d, 0x55), (x, y, w, h))
        
    text_surf = pygame.font.SysFont("Sans", 20).render(txt, True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=(x + w//2, y + h//2))
    screen.blit(text_surf, text_rect)


def render_vkb(virtual_kb, ptr_left, ptr_right):
    iterated_y = 0

    for i_row, row in enumerate(virtual_kb.keys):
        iterated_x = 0

        for key in row:
            adj_x = iterated_x + virtual_kb.padding
            adj_y = iterated_y + virtual_kb.padding
            adj_w = key.width_weight * virtual_kb.key_width[i_row]
            adj_h = virtual_kb.key_height

            state = KeyState.INACTIVE
            if ptr_left.in_box(adj_x, adj_y, adj_w, adj_h):
                state = max(ptr_left.state, state)
            if ptr_right.in_box(adj_x, adj_y, adj_w, adj_h):
                state = max(ptr_right.state, state)
            render_key(key.str, adj_x, adj_y, adj_w, adj_h, state)

            iterated_x += adj_w + virtual_kb.padding * 2

        iterated_y += virtual_kb.key_height + virtual_kb.padding * 2

    pygame.draw.circle(screen, (255, 128, 128), (ptr_left.x, ptr_left.y), ptr_left.get_radius(), 2)
    pygame.draw.circle(screen, (128, 255, 128), (ptr_right.x, ptr_right.y), ptr_right.get_radius(), 2)
    pygame.display.update()


class KeyState(IntEnum):
    INACTIVE = 0
    HOVER = 1
    CLICK = 2


class KeyButton:
    def __init__(self, str, keycode, callback, width_weight=1.0):
        self.str = str
        self.keycode = keycode
        self.callback = callback
        self.width_weight = width_weight


class VirtualKeyboard:
    padding = 3
    key_width = []
    key_height = 0

    def __init__(self, keys):
        self.keys = keys
        self.key_rows = len(keys)
        self.update_dimensions()

    def _uniform_key_width(self, row):
        unpadded_width = screen_width - (len(self.keys[row]) * self.padding * 2)
        weights_total = 0
        for key in self.keys[row]:
            weights_total += key.width_weight

        return unpadded_width / weights_total

    def _uniform_key_height(self):
        return (screen_height - (self.key_rows * self.padding * 2)) / self.key_rows

    def update_dimensions(self):
        self.key_height = self._uniform_key_height()
        self.key_width = []
        for i in range(0, self.key_rows):
            self.key_width.append(self._uniform_key_width(i))

    def find_key_row(self, y_coord):
        return math.floor(y_coord / (self.key_height + self.padding * 2))

    def find_key(self, x_coord, y_coord):
        i_row = self.find_key_row(y_coord)
        i_row = clamp(i_row, 0, self.key_rows - 1)

        iterated_x = 0
        for key in self.keys[i_row]:
            adjusted_key_width = key.width_weight * self.key_width[i_row]
            iterated_x += adjusted_key_width + self.padding * 2
            if x_coord < iterated_x:
                return key
        return None


class VirtualPointer:
    def __init__(self, state, x, y):
        self.state = state
        self.x = x
        self.y = y

    def get_radius(self):
        if self.state == KeyState.INACTIVE:
            return 100
        elif self.state == KeyState.HOVER:
            return 10
        elif self.state == KeyState.CLICK:
            return 7
        else:
            assert "Invalid VirtualPointer state!"

    def in_box(self, bx, by, bw, bh):
        return self.x >= bx and self.y >= by and self.x <= bx + bw and self.y <= by + bh


def on_generic_press(keycode):
    kb.pressEvent([keycode])
    kb.releaseEvent([keycode])


def on_shift_press(keycode):
    return


def on_alt_press(keycode):
    return

virtual_kb = VirtualKeyboard([
    [
        KeyButton('1', sui.Keys.KEY_1, on_generic_press),
        KeyButton('2', sui.Keys.KEY_2, on_generic_press),
        KeyButton('3', sui.Keys.KEY_3, on_generic_press),
        KeyButton('4', sui.Keys.KEY_4, on_generic_press),
        KeyButton('5', sui.Keys.KEY_5, on_generic_press),
        KeyButton('6', sui.Keys.KEY_6, on_generic_press),
        KeyButton('7', sui.Keys.KEY_7, on_generic_press),
        KeyButton('8', sui.Keys.KEY_8, on_generic_press),
        KeyButton('9', sui.Keys.KEY_9, on_generic_press),
        KeyButton('0', sui.Keys.KEY_0, on_generic_press),
        KeyButton('-', sui.Keys.KEY_MINUS, on_generic_press),
        KeyButton('←', sui.Keys.KEY_BACKSPACE, on_generic_press),
    ], [
        KeyButton('q', sui.Keys.KEY_Q, on_generic_press),
        KeyButton('w', sui.Keys.KEY_W, on_generic_press),
        KeyButton('e', sui.Keys.KEY_E, on_generic_press),
        KeyButton('r', sui.Keys.KEY_R, on_generic_press),
        KeyButton('t', sui.Keys.KEY_T, on_generic_press),
        KeyButton('y', sui.Keys.KEY_Y, on_generic_press),
        KeyButton('u', sui.Keys.KEY_U, on_generic_press),
        KeyButton('i', sui.Keys.KEY_I, on_generic_press),
        KeyButton('o', sui.Keys.KEY_O, on_generic_press),
        KeyButton('p', sui.Keys.KEY_P, on_generic_press),
        KeyButton('\\', sui.Keys.KEY_BACKSLASH, on_generic_press),
    ], [
        KeyButton('alt', 0, on_alt_press, 0.9),
        KeyButton('a', sui.Keys.KEY_A, on_generic_press),
        KeyButton('s', sui.Keys.KEY_S, on_generic_press),
        KeyButton('d', sui.Keys.KEY_D, on_generic_press),
        KeyButton('f', sui.Keys.KEY_F, on_generic_press),
        KeyButton('g', sui.Keys.KEY_G, on_generic_press),
        KeyButton('h', sui.Keys.KEY_H, on_generic_press),
        KeyButton('j', sui.Keys.KEY_J, on_generic_press),
        KeyButton('k', sui.Keys.KEY_K, on_generic_press),
        KeyButton('l', sui.Keys.KEY_L, on_generic_press),
        KeyButton(';', sui.Keys.KEY_SEMICOLON, on_generic_press),
        KeyButton('\'', sui.Keys.KEY_APOSTROPHE, on_generic_press),
        KeyButton('↵', sui.Keys.KEY_ENTER, on_generic_press, 1.7),
    ], [
        KeyButton('↑', sui.Keys.KEY_LEFTSHIFT, on_shift_press, 1.2),
        KeyButton('z', sui.Keys.KEY_Z, on_generic_press),
        KeyButton('x', sui.Keys.KEY_X, on_generic_press),
        KeyButton('c', sui.Keys.KEY_C, on_generic_press),
        KeyButton('v', sui.Keys.KEY_V, on_generic_press),
        KeyButton('b', sui.Keys.KEY_B, on_generic_press),
        KeyButton('n', sui.Keys.KEY_N, on_generic_press),
        KeyButton('m', sui.Keys.KEY_M, on_generic_press),
        KeyButton(',', sui.Keys.KEY_COMMA, on_generic_press),
        KeyButton('.', sui.Keys.KEY_DOT, on_generic_press),
        KeyButton('/', sui.Keys.KEY_SLASH, on_generic_press),
        KeyButton('?', sui.Keys.KEY_QUESTION, on_generic_press),
        KeyButton('↑', sui.Keys.KEY_RIGHTSHIFT, on_shift_press, 1.2),
    ], [
        KeyButton(' ', sui.Keys.KEY_SPACE, on_generic_press),
    ]
])


def exitCallback(evm, btn, pressed):
    screen.fill((255, 0, 0))
    print("ABORT")
    if not pressed:
        sys.exit()


def evminit():
    evm = EventMapper()
    evm.setButtonAction(SCButtons.LGRIP, sui.Keys.KEY_LEFTSHIFT)
    evm.setButtonAction(SCButtons.LB, sui.Keys.KEY_BACKSPACE)
    evm.setButtonAction(SCButtons.RB, sui.Keys.KEY_SPACE)
    evm.setButtonAction(SCButtons.A, sui.Keys.KEY_ENTER)
    evm.setButtonCallback(SCButtons.B, exitCallback)
    return evm


def sc_adjust_x(raw_x, center_fraction, scalar=6/5):
    abs_max = 0x20000
    return round(screen_width * (center_fraction + scalar * raw_x/abs_max))


def sc_adjust_y(raw_y, center_fraction, scalar=6/5):
    abs_max = 0x10000
    return round(screen_height * (center_fraction + scalar * -raw_y/abs_max))


def update(sc, sc_input):
    if sc_input.status != SCStatus.INPUT:
        return

    screen.fill((0x0f, 0x28, 0x3c))

    evm.process(sc, sc_input)
    global sc_input_previous

    pressed_right, pressed_left = False, False

    ptr_left = VirtualPointer(KeyState.INACTIVE, sc_adjust_x(sc_input.lpad_x, 1/4),
                              sc_adjust_y(sc_input.lpad_y, 1/2))
    ptr_right = VirtualPointer(KeyState.INACTIVE, sc_adjust_x(sc_input.rpad_x, 3/4),
                               sc_adjust_y(sc_input.rpad_y, 1/2))

    key_left = virtual_kb.find_key(ptr_left.x, ptr_left.y)
    key_right = virtual_kb.find_key(ptr_right.x, ptr_right.y)

    if sc_input.buttons & SCButtons.RPADTOUCH:
        if sc_input.buttons & SCButtons.RPAD:
            ptr_right.state = KeyState.CLICK
            # Handle click if previous buttons did not include both RPADTOUCH and RPAD
            pressed_right = ~sc_input_previous.buttons & (SCButtons.RPADTOUCH | SCButtons.RPAD) != 0
        else:
            ptr_right.state = KeyState.HOVER

    if sc_input.buttons & SCButtons.LPADTOUCH:
        if sc_input.buttons & SCButtons.LPAD:
            ptr_left.state = KeyState.CLICK
            # Handle click if previous buttons did not include both LPADTOUCH and LPAD
            pressed_left = ~sc_input_previous.buttons & (SCButtons.LPADTOUCH | SCButtons.LPAD) != 0
        else:
            ptr_left.state = KeyState.HOVER

    if pressed_left and (key_left is not None):
        key_left.callback(key_left.keycode)
    if pressed_right and (key_right is not None):
        key_left.callback(key_right.keycode)

    render_vkb(virtual_kb, ptr_left, ptr_right)

    sc_input_previous = sc_input


if __name__ == '__main__':
    evm = evminit()
    sc = SteamController(callback=update)
    sc.run()
