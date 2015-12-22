#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Steam Controller On-Screen Keyboard - Proof of Concept"""

from threading import Thread

import sdl2
import sdl2.ext

import screen
import scinput
import state
import vkb
import vptr


def main():
    default_ptr_left = vptr.VirtualPointer(vkb.KeyState.INACTIVE, screen.width * 1//4, screen.height // 2)
    default_ptr_right = vptr.VirtualPointer(vkb.KeyState.INACTIVE, screen.width * 3//4, screen.height // 2)
    state.submit_gui_state(state.GuiState(scinput.virtual_kb, default_ptr_left, default_ptr_right))

    scinput.create_event_mapper()
    sc_thread = Thread(target=scinput.input_thread, daemon=True)
    sc_thread.start()

    sdl2.ext.init()
    scr = screen.Screen()

    while not state.should_close():
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                state.close()
                break

        scr.render(state.get_gui_state())
        scr.delay()

    sdl2.ext.quit()


if __name__ == '__main__':
    main()
