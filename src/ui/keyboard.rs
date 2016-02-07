extern crate sdl2;

use ui;
use utils::units::{Rect, RelArea};

pub struct Keyboard {
    area: RelArea,
    keys: Vec<ui::Key>,
}

impl Keyboard {
    pub fn new() -> Keyboard {
        Keyboard {
            area: RelArea::copy((0.02, 0.02), (0.96, 0.96)),
            keys: Vec::<ui::Key>::new(),
        }
    }
}

impl ui::Renderable for Keyboard {
    fn render(&self, renderer: &mut sdl2::render::Renderer, area: &Rect) {
        renderer.set_draw_color(sdl2::pixels::Color::RGB(255, 255, 255));

        let float_rect = self.area.to_abs(area);

        renderer.fill_rect(sdl2::rect::Rect::new_unwrap(
            float_rect.pos.0.round() as i32, float_rect.pos.1.round() as i32,
            float_rect.size.0.round() as u32, float_rect.size.1.round() as u32
            ));

        for key in &self.keys {
            key.render(renderer, &self.area.to_abs(area));
        }
    }
}
