#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Steam Controller On-Screen Keyboard - Proof of Concept"""

import pygame

import sys
from threading import Thread

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

    pygame.init()
    scr = screen.Screen()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if state.should_close():
            return

        gui_state = state.get_gui_state()
        scr.render_vkb(gui_state.virtual_kb, gui_state.ptr_left, gui_state.ptr_right)
        pygame.display.flip()


if __name__ == '__main__':
    main()
