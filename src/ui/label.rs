extern crate sdl2;

use ui;
use utils::units::Rect;

pub struct Label {
    text: String,
}

impl Label {
    pub fn new(text: String) -> Label {
        Label {
            text: text, 
        }
    }
}

impl ui::Renderable for Label {
    fn render(&self, renderer: &mut sdl2::render::Renderer, area: &Rect) {

    }
}
