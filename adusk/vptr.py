from enum import IntEnum

from adusk import state


class VirtualPointer:
    class State(IntEnum):
        INACTIVE = 0
        HOVER = 1
        CLICK = 2

    def __init__(self, state, coord_frac):
        self.state = state
        self.coord_frac = coord_frac

    def get_radius(self):
        if self.state == state.InputState.INACTIVE:
            return 100
        elif self.state == state.InputState.HOVER:
            return 10
        elif self.state == state.InputState.CLICK:
            return 7
        else:
            assert False, "Invalid VirtualPointer state!"

    def in_box(self, bx, by, bw, bh):
        x, y = self.coord_frac.to_absolute()
        return x >= bx and y >= by and x <= bx + bw and y <= by + bh

    def smoothen(self, prev_vptr, alpha):
        self.coord_frac.lowpass_filter(prev_vptr.coord_frac, alpha)
