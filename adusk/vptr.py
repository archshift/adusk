from adusk import state
from adusk import utils


class VirtualPointer:
    def __init__(self, state, x, y):
        self.state = state
        self.x = x
        self.y = y

    def get_radius(self):
        if self.state == state.InputState.INACTIVE:
            return 100
        elif self.state == state.InputState.HOVER:
            return 10
        elif self.state == state.InputState.CLICK:
            return 7
        else:
            assert "Invalid VirtualPointer state!"

    def in_box(self, bx, by, bw, bh):
        return self.x >= bx and self.y >= by and self.x <= bx + bw and self.y <= by + bh

    def smoothen(self, prev_vptr, alpha):
        self.x = utils.round_to_int(utils.compute_lowpass(self.x, prev_vptr.x, alpha))
        self.y = utils.round_to_int(utils.compute_lowpass(self.y, prev_vptr.y, alpha))
