from adusk import screen
from adusk import utils


class TestCoordFraction:
    def test_lowpass_1(self):
        screen.width = 2
        screen.height = 2
        frac_cur = screen.CoordFraction(0.5, 0.5)
        frac_prev = screen.CoordFraction(0.1, 0.1)
        frac_cur.lowpass_filter(frac_prev, 0.5)
        assert frac_cur.x_fraction == frac_cur.y_fraction

    def test_lowpass_2(self):
        screen.width = 2
        screen.height = 2
        frac_cur = screen.CoordFraction(0.5, 0.5)
        frac_prev = screen.CoordFraction(0.5, 0.5)
        frac_cur.lowpass_filter(frac_prev, 0.5)
        assert frac_cur.x_fraction == frac_prev.x_fraction
        assert frac_cur.y_fraction == frac_prev.y_fraction

    def test_lowpass_3(self):
        screen.width = 4
        screen.height = 2
        frac_cur = screen.CoordFraction.from_absolute(2, 2)
        frac_prev = screen.CoordFraction.from_absolute(0, 0)
        frac_cur.lowpass_filter(frac_prev, 0.5)
        x_cur, y_cur = frac_cur.to_absolute()
        x_prev, y_prev = frac_prev.to_absolute()
        assert (x_cur - x_prev) == (y_cur - y_prev)

    def test_lowpass_4(self):
        screen.width = 5
        screen.height = 4
        x_cur = y_cur = 5
        x_prev = y_prev = 2
        frac_cur = screen.CoordFraction.from_absolute(x_cur, y_cur)
        frac_prev = screen.CoordFraction.from_absolute(x_prev, y_prev)

        frac_cur.lowpass_filter(frac_prev, 0.5)
        x_from_frac, y_from_frac = frac_cur.to_absolute()

        x_cur = utils.compute_lowpass(x_cur, x_prev, 0.5)
        y_cur = utils.compute_lowpass(y_cur, x_prev, 0.5)

        assert x_cur == x_from_frac and y_cur == y_from_frac

