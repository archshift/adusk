#!/usr/env/python3
# -*- coding: utf-8 -*-

import sdl2
import sdl2.ext

from adusk import screen
from adusk import config
from adusk import state
from adusk import vkb


def load_kb_config():
    kb_config = vkb.VirtualKeyboardConfig()
    kb_layout_file = config.YamlFile("keyboard-layout.yaml")
    kb_layout_file.read()
    kb_layout_file.add_to_config("keys", kb_config)
    return kb_config


def main():
    virtual_kb = load_kb_config().construct()

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
        scr.render(virtual_kb, controller_state.get_pad_pos())
        scr.delay()

    sdl2.ext.quit()


if __name__ == '__main__':
    main()
