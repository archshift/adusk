import ctypes

import sdl2
import sdl2.ext
import sdl2.sdlgfx

from adusk import resources
from adusk import state
from adusk import utils

size = utils.Rect(640, 320)


class Screen:
    bg_color = sdl2.ext.Color(0x0f, 0x28, 0x3c)

    ptr_color_left = sdl2.ext.Color(255, 128, 128)
    ptr_color_right = sdl2.ext.Color(128, 255, 128)

    def __init__(self):
        self.window = sdl2.ext.Window("", (size.w, size.h), flags=sdl2.SDL_WINDOW_BORDERLESS)
        self.renderer = sdl2.ext.Renderer(self.window)

        font_name = "fonts/DejaVuSansCondensed-Bold.ttf"
        font_path = resources.find_data_resource(font_name)
        assert font_path is not None, "Could not find font file `{}`!".format(font_name)
        print("Found font file at `{}`".format(font_path))
        self.font_manager = sdl2.ext.FontManager(font_path)

        self.frame_rate_manager = sdl2.sdlgfx.FPSManager()
        sdl2.sdlgfx.SDL_initFramerate(ctypes.byref(self.frame_rate_manager))
        sdl2.sdlgfx.SDL_setFramerate(ctypes.byref(self.frame_rate_manager), 60)

        self.clear()
        self.window.show()

    def clear(self):
        self.renderer.clear(color=self.bg_color)

    def delay(self):
        sdl2.sdlgfx.SDL_framerateDelay(ctypes.byref(self.frame_rate_manager))

    def render_key(self, txt, key, key_color):
        self.renderer.fill([(key.x, key.y, key.w, key.h)], color=key_color)

        # We don't need to continue rendering text if there's nothing to render!
        if txt == "":
            return

        key_center = (key.x + key.w//2, key.y + key.h//2)
        text_surface = self.font_manager.render(txt, color=self.text_color)
        text_texture_p = sdl2.SDL_CreateTextureFromSurface(self.renderer.renderer, ctypes.byref(text_surface))
        sdl2.SDL_FreeSurface(ctypes.byref(text_surface))

        src_rect = (text_surface.clip_rect.x, text_surface.clip_rect.y,
                    text_surface.clip_rect.w, text_surface.clip_rect.h)
        dst_rect = (key_center[0] - text_surface.clip_rect.w//2, key_center[1] - text_surface.clip_rect.h//2,
                    text_surface.clip_rect.w, text_surface.clip_rect.h)
        self.renderer.copy(text_texture_p[0], src_rect, dst_rect)
        sdl2.SDL_DestroyTexture(text_texture_p)

    def render_ptr(self, ptr, color):
        ptr_x, ptr_y = ptr.coord_frac.to_absolute()
        sdl2.sdlgfx.aacircleRGBA(self.renderer.renderer, utils.round_to_int(ptr_x), utils.round_to_int(ptr_y),
                                 ptr.get_radius(), color.r, color.g, color.b, color.a)

    def render_vkb(self, virtual_kb, pointers):
        for key in virtual_kb.gen_key_layouts():
            input_state = state.InputState.INACTIVE
            if pointers[0].in_box(key.x, key.y, key.w, key.h):
                input_state = max(pointers[0].state, input_state)
            if pointers[1].in_box(key.x, key.y, key.w, key.h):
                input_state = max(pointers[1].state, input_state)
            self.render_key(virtual_kb.keys[key.row][key.col].str, key, input_state)

    def render(self, virtual_kb, pointers):
        self.clear()
        self.render_vkb(virtual_kb, pointers)
        self.render_ptr(pointers[0], self.ptr_color_left)
        self.render_ptr(pointers[1], self.ptr_color_right)
        self.renderer.present()
        self.window.refresh()
