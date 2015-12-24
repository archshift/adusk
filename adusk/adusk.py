#!/usr/env/python3
# -*- coding: utf-8 -*-

from enum import Enum
from threading import Thread

import sdl2
import sdl2.ext

from adusk import screen
from adusk.screen import CoordFraction
from adusk import config
from adusk import controller
from adusk import state
from adusk import vkb
from adusk import vptr


def load_kb_config():
    kb_config = vkb.VirtualKeyboardConfig()
    kb_layout_file = config.YamlFile("keyboard-layout.yaml")
    kb_layout_file.read()
    kb_layout_file.add_to_config("keys", kb_config)
    return kb_config


class ProgramMode(Enum):
    INPUT = 0
    WINDOW_MGMT = 1


def main():
    controller_state = controller.ControllerState()
    controller_state.set_pointers(
            vptr.VirtualPointer(state.InputState.INACTIVE, CoordFraction(1/4, 1/2)),
            vptr.VirtualPointer(state.InputState.INACTIVE, CoordFraction(3/4, 1/2))
    )

    virtual_kb = load_kb_config().construct()

    sc_thread = Thread(target=controller.input_thread, args=(controller_state,), daemon=True)
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
        vkb.process_click_queue(virtual_kb, controller_state.click_queue)
        scr.render(virtual_kb, controller_state.get_pointers())
        scr.delay()

    sdl2.ext.quit()


if __name__ == '__main__':
    main()
