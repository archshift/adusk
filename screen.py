import pygame
import pygame.freetype

import vkb

width = 640
height = 320


class Screen:
    bg_color = (0x0f, 0x28, 0x3c)
    text_color = (255, 255, 255)

    key_color = {
        vkb.KeyState.INACTIVE: (0x19, 0x3d, 0x55),
        vkb.KeyState.HOVER: (0x25, 0x5f, 0x7e),
        vkb.KeyState.CLICK: (0x7b, 0xb8, 0xd8),
    }

    ptr_color_left = (255, 128, 128)
    ptr_color_right = (128, 255, 128)

    def __init__(self):
        pygame.init()
        self.text_font = pygame.freetype.SysFont("Sans", 18)
        self.surface = pygame.display.set_mode((width, height))
        self.clear()

    def clear(self):
        self.surface.fill(self.bg_color)

    def render_key(self, txt, x, y, w, h, key_state):
        pygame.draw.rect(self.surface, self.key_color[key_state], (x, y, w, h))
        text_surf = self.text_font.render(txt, self.text_color)[0]
        text_rect = text_surf.get_rect(center=(x + w//2, y + h//2))
        self.surface.blit(text_surf, text_rect)

    def render_ptrs(self, ptr_left, ptr_right):
        pygame.draw.circle(self.surface, self.ptr_color_left, (ptr_left.x, ptr_left.y), ptr_left.get_radius(), 2)
        pygame.draw.circle(self.surface, self.ptr_color_right, (ptr_right.x, ptr_right.y), ptr_right.get_radius(), 2)

    def render_vkb(self, virtual_kb, ptr_left, ptr_right):
        self.clear()
        iterated_y = 0

        for i_row, row in enumerate(virtual_kb.keys):
            iterated_x = 0

            for key in row:
                adj_x = iterated_x + virtual_kb.padding
                adj_y = iterated_y + virtual_kb.padding
                adj_w = key.width_weight * virtual_kb.key_width[i_row]
                adj_h = virtual_kb.key_height

                state = vkb.KeyState.INACTIVE
                if ptr_left.in_box(adj_x, adj_y, adj_w, adj_h):
                    state = max(ptr_left.state, state)
                if ptr_right.in_box(adj_x, adj_y, adj_w, adj_h):
                    state = max(ptr_right.state, state)
                self.render_key(key.str, adj_x, adj_y, adj_w, adj_h, state)

                iterated_x += adj_w + virtual_kb.padding * 2

            iterated_y += virtual_kb.key_height + virtual_kb.padding * 2

        self.render_ptrs(ptr_left, ptr_right)
        pygame.display.update()