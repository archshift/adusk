import vkb


class VirtualPointer:
    def __init__(self, state, x, y):
        self.state = state
        self.x = x
        self.y = y

    def get_radius(self):
        if self.state == vkb.KeyState.INACTIVE:
            return 100
        elif self.state == vkb.KeyState.HOVER:
            return 10
        elif self.state == vkb.KeyState.CLICK:
            return 7
        else:
            assert "Invalid VirtualPointer state!"

    def in_box(self, bx, by, bw, bh):
        return self.x >= bx and self.y >= by and self.x <= bx + bw and self.y <= by + bh