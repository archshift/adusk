from collections import namedtuple

Rect = namedtuple("Rect", "w h")


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def lowpass_filter(self, prev_point, alpha):
        self.x = compute_lowpass(self.x, prev_point.x, alpha)
        self.y = compute_lowpass(self.y, prev_point.y, alpha)


class CoordFraction:
    @staticmethod
    def from_absolute(x, y, screen_rect):
        return CoordFraction(x / screen_rect.w, y / screen_rect.h)

    def __init__(self, x_fraction, y_fraction):
        self.x_fraction = x_fraction
        self.y_fraction = y_fraction

    def to_absolute(self, screen_rect):
        return self.x_fraction * screen_rect.w, self.y_fraction * screen_rect.h

    def update_absolute(self, x, y, screen_rect):
        self.x_fraction = x / screen_rect.w
        self.y_fraction = y / screen_rect.h

    def lowpass_filter(self, prev_coords, alpha):
        self.x_fraction = compute_lowpass(self.x_fraction, prev_coords.x_fraction, alpha)
        self.y_fraction = compute_lowpass(self.y_fraction, prev_coords.y_fraction, alpha)


def round_to_int(f):
    return int(round(f))


def clamp(i, min_val, max_val):
    return max(min_val, min(max_val, i))


def compute_lowpass(curr, prev, alpha):
    return prev + alpha * (curr - prev)
