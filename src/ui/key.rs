extern crate sdl2;

use ui::label::Label;
use ui::renderable::Renderable;
use utils::units::{Rect, RelArea};

pub struct Key {
    area: RelArea,
    label: Label,
}

impl Key {
    pub fn new(text: String) -> Key {
        Key {
            area: RelArea::copy((0.0, 0.0), (1.0, 1.0)),
            label: Label::new(text),
        }
    }
}

impl Renderable for Key {
    fn render(&self, renderer: &mut sdl2::render::Renderer, area: &Rect) {
        self.label.render(renderer, &self.area.to_abs(area));
    }
}
