import ctypes

import sdl2
import sdl2.ext
import sdl2.sdlgfx

import state
import utils

width = 640
height = 320


class Screen:
    bg_color = sdl2.ext.Color(0x0f, 0x28, 0x3c)
    text_color = sdl2.ext.Color(255, 255, 255)

    key_color = {
        state.InputState.INACTIVE: sdl2.ext.Color(0x19, 0x3d, 0x55),
        state.InputState.HOVER: sdl2.ext.Color(0x25, 0x5f, 0x7e),
        state.InputState.CLICK: sdl2.ext.Color(0x7b, 0xb8, 0xd8),
    }

    ptr_color_left = sdl2.ext.Color(255, 128, 128)
    ptr_color_right = sdl2.ext.Color(128, 255, 128)

    def __init__(self):
        self.window = sdl2.ext.Window("", (width, height), flags=sdl2.SDL_WINDOW_BORDERLESS)
        self.renderer = sdl2.ext.Renderer(self.window)
        self.font_manager = sdl2.ext.FontManager("/usr/share/fonts/ttf-dejavu-ib/DejaVuSans.ttf")

        self.frame_rate_manager = sdl2.sdlgfx.FPSManager()
        sdl2.sdlgfx.SDL_initFramerate(ctypes.byref(self.frame_rate_manager))
        sdl2.sdlgfx.SDL_setFramerate(ctypes.byref(self.frame_rate_manager), 60)

        self.clear()
        self.window.show()

    def clear(self):
        self.renderer.clear(color=self.bg_color)

    def delay(self):
        sdl2.sdlgfx.SDL_framerateDelay(ctypes.byref(self.frame_rate_manager))

    def render_key(self, txt, x, y, w, h, key_state):
        x, y = utils.round_to_int(x), utils.round_to_int(y)
        w, h = utils.round_to_int(w), utils.round_to_int(h)
        self.renderer.fill([(x, y, w, h)], color=self.key_color[key_state])

        key_center = (x + w//2, y + h//2)
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
        sdl2.sdlgfx.aacircleRGBA(self.renderer.renderer, ptr.x, ptr.y, ptr.get_radius(),
                                 color.r, color.g, color.b, color.a)

    def render_vkb(self, virtual_kb, ptr_state):
        iterated_y = 0

        for i_row, row in enumerate(virtual_kb.keys):
            iterated_x = 0

            for key in row:
                adj_x = iterated_x + virtual_kb.padding
                adj_y = iterated_y + virtual_kb.padding
                adj_w = key.width_weight * virtual_kb.key_width[i_row]
                adj_h = virtual_kb.key_height

                input_state = state.InputState.INACTIVE
                if ptr_state.ptr_left.in_box(adj_x, adj_y, adj_w, adj_h):
                    input_state = max(ptr_state.ptr_left.state, input_state)
                if ptr_state.ptr_right.in_box(adj_x, adj_y, adj_w, adj_h):
                    input_state = max(ptr_state.ptr_right.state, input_state)
                self.render_key(key.str, adj_x, adj_y, adj_w, adj_h, input_state)

                iterated_x += adj_w + virtual_kb.padding * 2

            iterated_y += virtual_kb.key_height + virtual_kb.padding * 2

    def render(self, virtual_kb, ptr_state):
        self.clear()
        self.render_vkb(virtual_kb, ptr_state)
        self.render_ptr(ptr_state.ptr_left, self.ptr_color_left)
        self.render_ptr(ptr_state.ptr_right, self.ptr_color_right)
        self.renderer.present()
        self.window.refresh()
