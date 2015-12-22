#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Steam Controller On-Screen Keyboard - Proof of Concept"""

from threading import Thread

import sdl2
import sdl2.ext
import steamcontroller.uinput as sui

import screen
import controller
import state
import vkb
import vptr

virtual_kb = vkb.VirtualKeyboard([
    [
        vkb.KeyButton('1', sui.Keys.KEY_1, vkb.on_key_generic),
        vkb.KeyButton('2', sui.Keys.KEY_2, vkb.on_key_generic),
        vkb.KeyButton('3', sui.Keys.KEY_3, vkb.on_key_generic),
        vkb.KeyButton('4', sui.Keys.KEY_4, vkb.on_key_generic),
        vkb.KeyButton('5', sui.Keys.KEY_5, vkb.on_key_generic),
        vkb.KeyButton('6', sui.Keys.KEY_6, vkb.on_key_generic),
        vkb.KeyButton('7', sui.Keys.KEY_7, vkb.on_key_generic),
        vkb.KeyButton('8', sui.Keys.KEY_8, vkb.on_key_generic),
        vkb.KeyButton('9', sui.Keys.KEY_9, vkb.on_key_generic),
        vkb.KeyButton('0', sui.Keys.KEY_0, vkb.on_key_generic),
        vkb.KeyButton('-', sui.Keys.KEY_MINUS, vkb.on_key_generic),
        vkb.KeyButton('\u2190', sui.Keys.KEY_BACKSPACE, vkb.on_key_generic),
    ], [
        vkb.KeyButton('q', sui.Keys.KEY_Q, vkb.on_key_generic),
        vkb.KeyButton('w', sui.Keys.KEY_W, vkb.on_key_generic),
        vkb.KeyButton('e', sui.Keys.KEY_E, vkb.on_key_generic),
        vkb.KeyButton('r', sui.Keys.KEY_R, vkb.on_key_generic),
        vkb.KeyButton('t', sui.Keys.KEY_T, vkb.on_key_generic),
        vkb.KeyButton('y', sui.Keys.KEY_Y, vkb.on_key_generic),
        vkb.KeyButton('u', sui.Keys.KEY_U, vkb.on_key_generic),
        vkb.KeyButton('i', sui.Keys.KEY_I, vkb.on_key_generic),
        vkb.KeyButton('o', sui.Keys.KEY_O, vkb.on_key_generic),
        vkb.KeyButton('p', sui.Keys.KEY_P, vkb.on_key_generic),
        vkb.KeyButton('\\', sui.Keys.KEY_BACKSLASH, vkb.on_key_generic),
    ], [
        vkb.KeyButton('Alt', 0, vkb.on_key_alt, 0.9),
        vkb.KeyButton('a', sui.Keys.KEY_A, vkb.on_key_generic),
        vkb.KeyButton('s', sui.Keys.KEY_S, vkb.on_key_generic),
        vkb.KeyButton('d', sui.Keys.KEY_D, vkb.on_key_generic),
        vkb.KeyButton('f', sui.Keys.KEY_F, vkb.on_key_generic),
        vkb.KeyButton('g', sui.Keys.KEY_G, vkb.on_key_generic),
        vkb.KeyButton('h', sui.Keys.KEY_H, vkb.on_key_generic),
        vkb.KeyButton('j', sui.Keys.KEY_J, vkb.on_key_generic),
        vkb.KeyButton('k', sui.Keys.KEY_K, vkb.on_key_generic),
        vkb.KeyButton('l', sui.Keys.KEY_L, vkb.on_key_generic),
        vkb.KeyButton(';', sui.Keys.KEY_SEMICOLON, vkb.on_key_generic),
        vkb.KeyButton('\'', sui.Keys.KEY_APOSTROPHE, vkb.on_key_generic),
        vkb.KeyButton('\u21B5', sui.Keys.KEY_ENTER, vkb.on_key_generic, 1.7),
    ], [
        vkb.KeyButton('\u2191', sui.Keys.KEY_LEFTSHIFT, vkb.on_key_shift, 1.2),
        vkb.KeyButton('z', sui.Keys.KEY_Z, vkb.on_key_generic),
        vkb.KeyButton('x', sui.Keys.KEY_X, vkb.on_key_generic),
        vkb.KeyButton('c', sui.Keys.KEY_C, vkb.on_key_generic),
        vkb.KeyButton('v', sui.Keys.KEY_V, vkb.on_key_generic),
        vkb.KeyButton('b', sui.Keys.KEY_B, vkb.on_key_generic),
        vkb.KeyButton('n', sui.Keys.KEY_N, vkb.on_key_generic),
        vkb.KeyButton('m', sui.Keys.KEY_M, vkb.on_key_generic),
        vkb.KeyButton(',', sui.Keys.KEY_COMMA, vkb.on_key_generic),
        vkb.KeyButton('.', sui.Keys.KEY_DOT, vkb.on_key_generic),
        vkb.KeyButton('/', sui.Keys.KEY_SLASH, vkb.on_key_generic),
        vkb.KeyButton('?', sui.Keys.KEY_QUESTION, vkb.on_key_generic),
        vkb.KeyButton('\u2191', sui.Keys.KEY_RIGHTSHIFT, vkb.on_key_shift, 1.2),
    ], [
        vkb.KeyButton(' ', sui.Keys.KEY_SPACE, vkb.on_key_generic),
        vkb.KeyButton('Done', 0, vkb.on_key_done, 0.3),
    ]
])


def main():
    default_ptr_left = vptr.VirtualPointer(state.InputState.INACTIVE, screen.width * 1 // 4, screen.height // 2)
    default_ptr_right = vptr.VirtualPointer(state.InputState.INACTIVE, screen.width * 3 // 4, screen.height // 2)
    state.submit_ptr_state(state.PtrState(default_ptr_left, default_ptr_right))

    controller.create_event_mapper()
    sc_thread = Thread(target=controller.input_thread, daemon=True)
    sc_thread.start()

    sdl2.ext.init()
    scr = screen.Screen()

    while not state.should_close():
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                state.close()
                break
            if event.type == sdl2.SDL_WINDOWEVENT:
                if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                    screen.width = event.window.data1
                    screen.height = event.window.data2

        virtual_kb.update_dimensions()
        vkb.callback_clicks(virtual_kb)
        scr.render(virtual_kb, state.get_ptr_state())
        scr.delay()

    sdl2.ext.quit()


if __name__ == '__main__':
    main()
