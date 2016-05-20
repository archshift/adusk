pub struct Rect {
    pub pos: (f32, f32),
    pub size: (f32, f32),
}

pub struct RelCoords {
    pub rel_coords: (f32, f32),
}

impl RelCoords {
    pub fn new(abs: (f32, f32), area: &Rect) -> RelCoords {
        let (abs_x, abs_y) = abs;
        RelCoords {
            rel_coords: ((abs_x - area.pos.0) / area.size.0, (abs_y - area.pos.1) / area.size.1),
        }
    }

    pub fn copy(rel: (f32, f32)) -> RelCoords {
        RelCoords {
            rel_coords: rel,
        }
    }

    pub fn to_abs(&self, area: &Rect) -> (f32, f32) {
        (self.rel_coords.0 * area.size.0 + area.pos.0, self.rel_coords.1 * area.size.1 + area.pos.1)
    }
}

pub struct RelArea {
    pub pos: RelCoords,
    pub size: (f32, f32),
}

impl RelArea {
    pub fn new(abs: Rect, area: &Rect) -> RelArea {
        let (abs_w, abs_h) = abs.size;

        RelArea {
            pos: RelCoords::new(abs.pos, area),
            size: (abs_w / area.size.0, abs_h / area.size.1),
        }
    }

    pub fn copy(rel_pos: (f32, f32), rel_size: (f32, f32)) -> RelArea {
        RelArea {
            pos: RelCoords::copy(rel_pos),
            size: rel_size,
        }
    }

    pub fn to_abs(&self, area: &Rect) -> Rect {
        Rect {
            pos: self.pos.to_abs(area),
            size: (self.size.0 * area.size.0, self.size.1 * area.size.1),
        }
    }
}
