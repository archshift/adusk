from adusk import utils


class TestCoordFraction:
    def test_lowpass_1(self):
        frac_cur = utils.CoordFraction(0.5, 0.5)
        frac_prev = utils.CoordFraction(0.1, 0.1)
        frac_cur.lowpass_filter(frac_prev, 0.5)
        assert frac_cur.x_fraction == frac_cur.y_fraction

    def test_lowpass_2(self):
        frac_cur = utils.CoordFraction(0.5, 0.5)
        frac_prev = utils.CoordFraction(0.5, 0.5)
        frac_cur.lowpass_filter(frac_prev, 0.5)
        assert frac_cur.x_fraction == frac_prev.x_fraction
        assert frac_cur.y_fraction == frac_prev.y_fraction

    def test_lowpass_3(self):
        screen = utils.Rect(4, 2)
        frac_cur = utils.CoordFraction.from_absolute(2, 2, screen)
        frac_prev = utils.CoordFraction.from_absolute(0, 0, screen)

        frac_cur.lowpass_filter(frac_prev, 0.5)
        x_cur, y_cur = frac_cur.to_absolute(screen)
        x_prev, y_prev = frac_prev.to_absolute(screen)
        assert (x_cur - x_prev) == (y_cur - y_prev)

    def test_lowpass_4(self):
        screen = utils.Rect(5, 4)
        x_cur = y_cur = 5
        x_prev = y_prev = 2
        frac_cur = utils.CoordFraction.from_absolute(x_cur, y_cur, screen)
        frac_prev = utils.CoordFraction.from_absolute(x_prev, y_prev, screen)

        frac_cur.lowpass_filter(frac_prev, 0.5)
        x_from_frac, y_from_frac = frac_cur.to_absolute(screen)

        x_cur = utils.compute_lowpass(x_cur, x_prev, 0.5)
        y_cur = utils.compute_lowpass(y_cur, x_prev, 0.5)

        assert x_cur == x_from_frac and y_cur == y_from_frac

